"""Frozen-backbone comparison on external garment photos (no fine-tuning).

Question (EXP-404): is EfficientNet-B0 the limit, or is it the training data? For each
pretrained backbone we extract one embedding per photo, fit a small linear head on the
"calib" half of the external dataset, and score it on the held-out "eval" half — the same
eval images (≤150/class, seed 0) used to score the current app model (EXP-402/403), so the
numbers are directly comparable. CLIP is additionally scored zero-shot (text prompts only,
no training images at all).

Metrics are balanced accuracy / macro-F1 (Top-1 is dominated by Cotton). Differences against
the current model come with paired, class-stratified bootstrap intervals.

    python -m tools.backbone_probe --data-dir data/external --out reports/backbone_probe
"""
from __future__ import annotations

import argparse
import json
import os
import time
import warnings

import numpy as np

from backend.fabric_classifier.training.metrics import compute_classification_metrics

DEFAULT_TEMPLATES = (
    "a photo of a {} garment",
    "a photo of clothing made of {} fabric",
    "a person wearing a {} piece of clothing",
    "a close-up of {} cloth",
)

# Words CLIP sees for each contract class (Knitted/Fleece etc. need a bit more than the label).
CLASS_WORDS = {
    "Fleece": "fleece",
    "Knitted": "knitted",
}


# ----------------------------------------------------------------------------- helpers
def l2_normalize(X) -> np.ndarray:
    X = np.asarray(X, dtype=np.float64)
    norm = np.linalg.norm(X, axis=-1, keepdims=True)
    return np.divide(X, norm, out=np.zeros_like(X), where=norm > 0)


def build_prompts(class_names, templates=DEFAULT_TEMPLATES) -> dict:
    return {n: [t.format(CLASS_WORDS.get(n, n.lower())) for t in templates] for n in class_names}


def zero_shot_scores(image_embeddings, text_embeddings_per_class, scale: float = 100.0) -> np.ndarray:
    """Cosine similarity between each image and each class's mean (normalised) prompt embedding."""
    img = l2_normalize(image_embeddings)
    cls = l2_normalize(np.stack([l2_normalize(t).mean(axis=0) for t in text_embeddings_per_class]))
    return scale * img @ cls.T


def to_numpy(x) -> np.ndarray:
    """Tensor, ndarray or a transformers output object (uses ``pooler_output``) → ndarray."""
    if isinstance(x, np.ndarray):
        return x
    if hasattr(x, "pooler_output") and x.pooler_output is not None:
        return to_numpy(x.pooler_output)
    if hasattr(x, "numpy"):
        t = x.detach() if hasattr(x, "detach") else x
        t = t.cpu() if hasattr(t, "cpu") else t
        return t.numpy()
    raise TypeError(f"cannot convert {type(x).__name__} to a NumPy array")


def json_safe(obj):
    """Recursively convert NumPy scalars/arrays to JSON types; drops bulky ``scores`` entries."""
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items() if k != "scores"}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


# ----------------------------------------------------------------------------- linear head
def fit_predict_head(X_train, y_train, X_test, n_classes: int, C: float = 1.0, balanced: bool = True,
                     seed: int = 0) -> np.ndarray:
    """Standardise → multinomial logistic regression → log-probabilities for all ``n_classes``.

    Classes absent from ``y_train`` get a very low score so they are never predicted.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    X_train, X_test = np.asarray(X_train, dtype=np.float64), np.asarray(X_test, dtype=np.float64)
    scaler = StandardScaler().fit(X_train)
    clf = LogisticRegression(C=C, max_iter=3000, class_weight="balanced" if balanced else None,
                             random_state=seed)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        clf.fit(scaler.transform(X_train), np.asarray(y_train))
    logp = clf.predict_log_proba(scaler.transform(X_test))
    out = np.full((len(X_test), n_classes), -1e9)
    out[:, clf.classes_] = logp
    return out


def _balanced_accuracy(y, pred, n_classes) -> float:
    recalls = [np.mean(pred[y == c] == c) for c in range(n_classes) if np.any(y == c)]
    return float(np.mean(recalls))


def choose_C(X, y, n_classes: int, grid=(0.01, 0.1, 1.0), folds: int = 3, seed: int = 0) -> float:
    """Pick the regularisation strength by cross-validated balanced accuracy on the training half."""
    from sklearn.model_selection import StratifiedKFold

    X, y = np.asarray(X), np.asarray(y)
    counts = np.bincount(y, minlength=n_classes)
    k = min(folds, int(counts[counts > 0].min()))
    if k < 2 or len(grid) == 1:
        return grid[len(grid) // 2]
    best_c, best = grid[0], -1.0
    for c in grid:
        accs = []
        for tr, te in StratifiedKFold(k, shuffle=True, random_state=seed).split(X, y):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                s = fit_predict_head(X[tr], y[tr], X[te], n_classes, C=c, seed=seed)
            accs.append(_balanced_accuracy(y[te], s.argmax(1), n_classes))
        if np.mean(accs) > best:
            best_c, best = c, float(np.mean(accs))
    return best_c


# ----------------------------------------------------------------------------- evaluation
def evaluate_scores(y, scores, class_names) -> dict:
    from tools.patch_diagnostic import pairwise_auc

    y, scores = np.asarray(y), np.asarray(scores, dtype=np.float64)
    m = compute_classification_metrics(y, scores.argmax(1), class_names, scores=scores, top_k=3)
    auc = None
    if "Cotton" in class_names and "Polyester" in class_names:
        auc = pairwise_auc(scores, y, class_names.index("Cotton"), class_names.index("Polyester"))
    present = {c: m["per_class_metrics"][c]["recall"] for c in class_names if m["per_class_metrics"][c]["support"] > 0}
    return {
        "balanced_accuracy": m["balanced_accuracy"],
        "macro_f1": m["macro_f1"],
        "top1": m["top1_accuracy"],
        "top3": m.get("top3_accuracy"),
        "cotton_vs_polyester_auc": auc,
        "per_class_recall": present,
    }


def paired_bootstrap_diff(y, pred_a, pred_b, n_boot: int = 1000, seed: int = 0, alpha: float = 0.05) -> dict:
    """Balanced-accuracy difference (a − b) with a class-stratified paired bootstrap interval."""
    y, pred_a, pred_b = np.asarray(y), np.asarray(pred_a), np.asarray(pred_b)
    classes = [c for c in np.unique(y)]
    ok_a = [(pred_a[y == c] == c).astype(float) for c in classes]
    ok_b = [(pred_b[y == c] == c).astype(float) for c in classes]
    diff = float(np.mean([a.mean() for a in ok_a]) - np.mean([b.mean() for b in ok_b]))
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot)
    for i in range(n_boot):
        da = []
        for a, b in zip(ok_a, ok_b):
            idx = rng.integers(0, len(a), len(a))
            da.append(a[idx].mean() - b[idx].mean())
        boots[i] = np.mean(da)
    lo, hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
    return {"diff": diff, "lo": float(lo), "hi": float(hi)}


def run_probe(extractors, calib_paths, y_calib, eval_paths, y_eval, class_names, baselines=None,
              c_grid=(0.01, 0.1, 1.0), seed: int = 0, n_boot: int = 1000, templates=DEFAULT_TEMPLATES,
              train_sizes=()) -> dict:
    """Run every extractor; ``baselines`` maps name → eval-set score matrix (e.g. the current model)."""
    n_classes = len(class_names)
    y_calib, y_eval = np.asarray(y_calib), np.asarray(y_eval)
    results = {"models": {}, "errors": {}, "scores": {}, "vs_baseline": {}, "timing": {}}

    baselines = baselines or {}
    for name, sc in baselines.items():
        results["models"][name] = evaluate_scores(y_eval, sc, class_names)
        results["scores"][name] = np.asarray(sc)
    baseline_name = next(iter(baselines), None)
    results["baseline_name"] = baseline_name

    prompts = build_prompts(class_names, templates)
    for ex in extractors:
        t0 = time.time()
        try:
            Xc = l2_normalize(ex.embed_images(calib_paths))
            Xe = l2_normalize(ex.embed_images(eval_paths))
            text_emb = None
            if hasattr(ex, "embed_texts"):
                flat = [p for n in class_names for p in prompts[n]]
                emb = np.asarray(ex.embed_texts(flat))
                k = len(templates)
                text_emb = [emb[i * k:(i + 1) * k] for i in range(n_classes)]
        except Exception as e:  # one broken download must not sink the other models
            results["errors"][ex.name] = f"{type(e).__name__}: {e}"
            continue

        entry = {"dim": int(Xc.shape[1])}
        C = choose_C(Xc, y_calib, n_classes, grid=c_grid, seed=seed)
        scores = fit_predict_head(Xc, y_calib, Xe, n_classes, C=C, seed=seed)
        entry["linear"] = {**evaluate_scores(y_eval, scores, class_names), "C": C}
        results["scores"][f"{ex.name}/linear"] = scores

        if train_sizes:
            rng = np.random.default_rng(seed)
            curve = {}
            for n in train_sizes:
                keep = []
                for c in np.unique(y_calib):
                    idx = np.where(y_calib == c)[0]
                    keep.extend(rng.permutation(idx)[:n].tolist())
                s = fit_predict_head(Xc[keep], y_calib[keep], Xe, n_classes, C=C, seed=seed)
                curve[int(n)] = _balanced_accuracy(y_eval, s.argmax(1), n_classes)
            entry["curve"] = curve

        if text_emb is not None:
            zs = zero_shot_scores(Xe, text_emb)
            entry["zero_shot"] = evaluate_scores(y_eval, zs, class_names)
            results["scores"][f"{ex.name}/zero_shot"] = zs
        results["models"][ex.name] = entry
        results["timing"][ex.name] = round(time.time() - t0, 1)

        if baseline_name is not None:
            base_pred = results["scores"][baseline_name].argmax(1)
            results["vs_baseline"][ex.name] = paired_bootstrap_diff(y_eval, scores.argmax(1), base_pred, n_boot, seed)
            if "zero_shot" in entry:
                results["vs_baseline"][f"{ex.name}/zero_shot"] = paired_bootstrap_diff(
                    y_eval, results["scores"][f"{ex.name}/zero_shot"].argmax(1), base_pred, n_boot, seed)

    ranked = [n for n in results["models"] if n not in baselines]
    results["ranking"] = sorted(ranked, key=lambda n: -results["models"][n]["linear"]["balanced_accuracy"])
    return results


def _pct(x) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def render_report(res, class_names, per_class_cap=None, meta=None) -> str:
    base = res.get("baseline_name")
    lines = ["# Frozen-backbone probe (EXP-404)", ""]
    if meta:
        lines += [f"{meta.get('n_calib', '?')} training photos (calib half, ≤{meta.get('calib_cap', '?')}/class), "
                  f"{meta.get('n_eval', '?')} test photos (eval half, ≤{per_class_cap}/class). "
                  "Backbones are frozen; only a linear head is trained.", ""]
    lines += ["**Balanced accuracy** (mean recall over classes) is the headline number; chance ≈ "
              f"{100 / max(1, len(class_names)):.0f}%.", "",
              "| Model | Method | Balanced acc | Macro-F1 | Top-3 | Cotton↔Poly AUC | Δ vs current [95% CI] |",
              "|---|---|---|---|---|---|---|"]
    if base:
        b = res["models"][base]
        lines.append(f"| {base} | existing weights (legacy_512, prior-fixed) | {_pct(b['balanced_accuracy'])} | "
                     f"{_pct(b['macro_f1'])} | {_pct(b['top3'])} | {_auc(b)} | – |")
    for name in res["ranking"]:
        e = res["models"][name]
        for method, key, label in (("linear head", "linear", name), ("zero-shot prompts", "zero_shot", f"{name}/zero_shot")):
            if key not in e:
                continue
            m = e[key]
            v = res["vs_baseline"].get(label)
            delta = "–" if v is None else f"{100 * v['diff']:+.1f} pts [{100 * v['lo']:+.1f}, {100 * v['hi']:+.1f}]"
            lines.append(f"| {name} | {method} | {_pct(m['balanced_accuracy'])} | {_pct(m['macro_f1'])} | "
                         f"{_pct(m['top3'])} | {_auc(m)} | {delta} |")
    curves = {n: res["models"][n]["curve"] for n in res["ranking"] if "curve" in res["models"][n]}
    if curves:
        sizes = sorted({s for c in curves.values() for s in c})
        lines += ["", "## Data efficiency (balanced accuracy vs training photos per class)", "",
                  "| Model | " + " | ".join(str(s) for s in sizes) + " |", "|---|" + "---|" * len(sizes)]
        for n, c in curves.items():
            lines.append(f"| {n} | " + " | ".join(_pct(c.get(s)) for s in sizes) + " |")
    if res["ranking"]:
        best = res["ranking"][0]
        lines += ["", f"## Per-class recall — best linear head ({best})", "", "| Class | Recall |", "|---|---|"]
        for c, r in res["models"][best]["linear"]["per_class_recall"].items():
            lines.append(f"| {c} | {_pct(r)} |")
    if res["errors"]:
        lines += ["", "## Failed extractors", ""] + [f"- {k}: {v}" for k, v in res["errors"].items()]
    return "\n".join(lines) + "\n"


def _auc(m) -> str:
    a = m.get("cotton_vs_polyester_auc")
    return "n/a" if a is None else f"{a:.3f}"


# ----------------------------------------------------------------------------- real extractors
def _load_rgb(path):  # pragma: no cover
    from PIL import Image

    with Image.open(path) as im:
        return im.convert("RGB")


def _batched(paths, batch, loader=_load_rgb):  # pragma: no cover
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(4) as pool:
        for i in range(0, len(paths), batch):
            yield list(pool.map(loader, paths[i:i + batch]))


class ImageNetB0:  # pragma: no cover - needs torch + weight download
    name = "imagenet_b0"

    def __init__(self):
        import torch
        import torchvision

        weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT
        self.model = torchvision.models.efficientnet_b0(weights=weights).eval()
        self.model.classifier = torch.nn.Identity()
        import torchvision.transforms as T

        self.tf = T.Compose([T.Resize((224, 224)), T.ToTensor(),
                             T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    def embed_images(self, paths):
        import torch

        out = []
        with torch.no_grad():
            for imgs in _batched(paths, 32):
                out.append(self.model(torch.stack([self.tf(i) for i in imgs])).numpy())
        return np.concatenate(out)


class HFVision:  # pragma: no cover - needs transformers + weight download
    """DINOv2 (CLS + mean patch token) or CLIP (image embeddings, with a text encoder)."""

    def __init__(self, name: str, repo: str, kind: str):
        from transformers import AutoImageProcessor, AutoModel, AutoTokenizer, CLIPModel

        self.name, self.kind = name, kind
        self.processor = AutoImageProcessor.from_pretrained(repo)
        if kind == "clip":
            self.model = CLIPModel.from_pretrained(repo).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(repo)
            self.embed_texts = self._embed_texts
        else:
            self.model = AutoModel.from_pretrained(repo).eval()

    def embed_images(self, paths):
        import torch

        out = []
        with torch.no_grad():
            for imgs in _batched(paths, 16):
                inputs = self.processor(images=imgs, return_tensors="pt")
                if self.kind == "clip":
                    pooled = self.model.vision_model(pixel_values=inputs["pixel_values"]).pooler_output
                    out.append(to_numpy(self.model.visual_projection(pooled)))
                else:
                    h = self.model(**inputs).last_hidden_state
                    out.append(torch.cat([h[:, 0], h[:, 1:].mean(1)], dim=1).numpy())
        return np.concatenate(out)

    def _embed_texts(self, texts):
        import torch

        with torch.no_grad():
            tok = self.tokenizer(list(texts), padding=True, return_tensors="pt")
            pooled = self.model.text_model(**tok).pooler_output
            return to_numpy(self.model.text_projection(pooled))


class OurModel:  # pragma: no cover - needs torch + weights
    """The shipped EfficientNet-B0: 7 patches on the 512-px photo, averaged. Gives both
    1280-d features (for a fresh head) and the logits the app would produce (baseline)."""

    name = "our_b0_features"

    def __init__(self, weights):
        import torch

        from backend.fabric_classifier.inference import FabricClassifier

        self.model = FabricClassifier(weights, device="cpu").model.float().eval()
        self.torch = torch
        self.cache = {}

    def _run(self, paths):
        import torch

        from backend.fabric_classifier.inference import preprocess_patches
        from backend.fabric_classifier.training.dataset import extract_patches, resize_max_side
        import zlib

        feats, logits = [], []
        with torch.no_grad():
            for path in paths:
                if path in self.cache:
                    f, l = self.cache[path]
                else:
                    seed = zlib.crc32(os.path.normpath(path).encode()) & 0xFFFFFFFF
                    img = resize_max_side(_load_rgb(path), 512)
                    pats = extract_patches(img.convert("RGBA"), rng=np.random.default_rng(seed))
                    x = preprocess_patches(pats)
                    z = self.model.features(x)
                    z = self.model.avgpool(z).flatten(1)
                    f = z.mean(0).numpy()
                    l = self.model.classifier(z).mean(0).numpy()
                    self.cache[path] = (f, l)
                feats.append(f)
                logits.append(l)
        return np.stack(feats), np.stack(logits)

    def embed_images(self, paths):
        return self._run(paths)[0]

    def logits(self, paths):
        return self._run(paths)[1]


MODEL_SPECS = {
    "imagenet_b0": lambda a: ImageNetB0(),
    "dinov2_small": lambda a: HFVision("dinov2_small", "facebook/dinov2-small", "dino"),
    "dinov2_base": lambda a: HFVision("dinov2_base", "facebook/dinov2-base", "dino"),
    "clip_b16": lambda a: HFVision("clip_b16", "openai/clip-vit-base-patch16", "clip"),
    "our_b0_features": lambda a: OurModel(a.weights),
}


def main(argv=None):  # pragma: no cover - needs torch, transformers, data
    import torch

    from backend.fabric_classifier.classes import MATERIAL_CLASSES
    from backend.fabric_classifier.postprocess import prior_correction, softmax
    from backend.fabric_classifier.training.balancing import effective_training_prior
    from backend.fabric_classifier.training.recalibrate import list_split, load_train_counts_json
    from tools.patch_diagnostic import cap_per_class

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", default="data/external")
    p.add_argument("--weights", default=os.path.join("backend", "fabric_classifier", "weights", "fabric_clf_best.pt"))
    p.add_argument("--counts-json", default="imaterialist_processed_counts.json")
    p.add_argument("--models", default="our_b0_features,imagenet_b0,dinov2_small,clip_b16,dinov2_base")
    p.add_argument("--calib-cap", type=int, default=300)
    p.add_argument("--eval-cap", type=int, default=150)
    p.add_argument("--out", default="reports/backbone_probe")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    torch.set_grad_enabled(False)
    torch.set_num_threads(os.cpu_count() or 4)

    names = list(MATERIAL_CLASSES)
    cp, cy = list_split(args.data_dir, "calib", names)
    ep, ey = list_split(args.data_dir, "eval", names)
    ci, ei = cap_per_class(cy, args.calib_cap, args.seed), cap_per_class(ey, args.eval_cap, args.seed)
    cp, cy, ep, ey = [cp[i] for i in ci], cy[ci], [ep[i] for i in ei], ey[ei]
    print(f"calib {len(cp)} images, eval {len(ep)} images", flush=True)

    wanted = [m.strip() for m in args.models.split(",") if m.strip()]
    extractors, baselines = [], {}
    for m in wanted:
        try:
            extractors.append(MODEL_SPECS[m](args))
        except Exception as e:
            print(f"could not load {m}: {e}", flush=True)
    for ex in extractors:
        if isinstance(ex, OurModel):
            L = ex.logits(ep)
            counts = load_train_counts_json(args.counts_json, names)
            train_prior = effective_training_prior(counts, 0.0, True)
            uniform = np.full(len(names), 1.0 / len(names))
            probs = prior_correction(softmax(L), train_prior, uniform, strength=1.0)
            baselines["current_app_model"] = np.log(probs + 1e-12)

    res = run_probe(extractors, cp, cy, ep, ey, names, baselines=baselines, c_grid=(0.01, 0.1, 1.0),
                    seed=args.seed, train_sizes=(10, 50, 150), n_boot=2000)
    meta = {"n_calib": len(cp), "n_eval": len(ep), "calib_cap": args.calib_cap}
    report = render_report(res, names, per_class_cap=args.eval_cap, meta=meta)
    with open(os.path.join(args.out, "report.md"), "w") as f:
        f.write(report)
    with open(os.path.join(args.out, "results.json"), "w") as f:
        json.dump(json_safe(res), f, indent=1)
    np.savez_compressed(os.path.join(args.out, "scores.npz"), y_eval=ey, **{k.replace("/", "__"): v for k, v in res["scores"].items()})
    print(report)


if __name__ == "__main__":  # pragma: no cover
    main()
