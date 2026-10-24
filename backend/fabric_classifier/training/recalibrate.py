"""Recalibrate the EXISTING model — no training (Colab plan, Phase 1).

What it does
------------
1. Runs the current weights over the iMaterialist **val** images (and **test** with
   ``--report-test``) and caches the raw logits, so later runs are instant.
2. Measures the baseline (plain argmax, exactly what the model does today).
3. Sweeps the prior-correction strength on val and picks the best setting
   (macro-F1, preferring settings where every class keeps ≥ 40% recall).
4. Fits the temperature on val so confidences are honest.
5. Reports before → after for val (and test, read once), per class.
6. With ``--write``, saves the settings to ``calibration/temperature.json`` next to the
   weights, which the web app/``FabricClassifier`` loads automatically.

Why iMaterialist only: its train/val/test split is fixed by folders on disk, so no
image the model was trained on can appear in evaluation. The legacy TextileNet split
depended on Windows directory order and cannot be reproduced reliably elsewhere.

Run (Mac, Colab or the Windows PC — wherever the data is)::

    python -m backend.fabric_classifier.training.recalibrate \\
        --imaterialist-dir /path/to/DATASETS/imaterialist_processed --report-test --write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import zlib

import numpy as np
from scipy.optimize import minimize_scalar

from ..postprocess import softmax
from .balancing import effective_training_prior
from .prior_sweep import best_result, evaluate_with_prior_correction, sweep_prior_correction

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
HEADLINE_METRICS = ("top1_accuracy", "top3_accuracy", "macro_f1", "balanced_accuracy", "worst_class_recall")
METRIC_LABELS = {
    "top1_accuracy": "Top-1",
    "top3_accuracy": "Top-3",
    "macro_f1": "Macro-F1",
    "balanced_accuracy": "Balanced acc.",
    "worst_class_recall": "Worst-class recall",
}


# ----------------------------------------------------------------------------- data listing

def list_split(root: str, split: str, class_names, limit_per_class: int | None = None):
    """Image paths and integer labels for ``root/split/<ClassName>/*``, sorted for determinism."""
    split_dir = os.path.join(root, split)
    if not os.path.isdir(split_dir):
        raise FileNotFoundError(f"Split folder not found: {split_dir}")
    paths, labels = [], []
    for idx, name in enumerate(class_names):
        class_dir = os.path.join(split_dir, name)
        if not os.path.isdir(class_dir):
            continue
        files = sorted(f for f in os.listdir(class_dir) if f.lower().endswith(IMAGE_EXTENSIONS))
        if limit_per_class is not None:
            files = files[:limit_per_class]
        paths.extend(os.path.join(class_dir, f) for f in files)
        labels.extend([idx] * len(files))
    order = np.argsort(np.array(paths, dtype=object), kind="stable")
    return [paths[i] for i in order], np.asarray(labels, dtype=np.int64)[order]


def load_train_counts_json(path: str, class_names) -> np.ndarray:
    """Per-class training counts from JSON: ``{"classes": {name: n}}`` or a flat ``{name: n}``."""
    with open(path) as f:
        data = json.load(f)
    table = data.get("classes", data) if isinstance(data, dict) else {}
    return np.array([int(table.get(name, 0)) for name in class_names], dtype=np.int64)


def count_split(root: str, split: str, class_names) -> np.ndarray:
    counts = np.zeros(len(class_names), dtype=np.int64)
    for idx, name in enumerate(class_names):
        class_dir = os.path.join(root, split, name)
        if os.path.isdir(class_dir):
            counts[idx] = sum(1 for f in os.listdir(class_dir) if f.lower().endswith(IMAGE_EXTENSIONS))
    return counts


# ----------------------------------------------------------------------------- calibration

def fit_temperature(logits, labels, offset=None, bounds=(0.05, 10.0)) -> float:
    """Temperature T minimising val NLL of ``softmax(logits / T + offset)``.

    ``offset`` is the prior-correction term (strength · log(target/train)); it is added
    after scaling, matching the order used at inference.
    """
    logits = np.asarray(logits, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.int64)
    offset = np.zeros(logits.shape[1]) if offset is None else np.asarray(offset, dtype=np.float64)
    rows = np.arange(len(labels))

    def nll(t):
        p = softmax(logits / t + offset)
        return -np.mean(np.log(p[rows, labels] + 1e-12))

    return float(minimize_scalar(nll, bounds=bounds, method="bounded").x)


def expected_calibration_error(probs, labels, n_bins: int = 15) -> float:
    probs = np.asarray(probs, dtype=np.float64)
    conf, pred = probs.max(axis=1), probs.argmax(axis=1)
    correct = pred == np.asarray(labels)
    edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        in_bin = (conf > lo) & (conf <= hi)
        if in_bin.any():
            ece += in_bin.mean() * abs(conf[in_bin].mean() - correct[in_bin].mean())
    return float(ece)


# ----------------------------------------------------------------------------- caching

def save_logits(path: str, logits, labels, paths, meta: dict | None = None) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp.npz"
    np.savez_compressed(tmp, logits=np.asarray(logits, dtype=np.float32), labels=np.asarray(labels),
                        paths=np.asarray(paths, dtype=object), meta=json.dumps(meta or {}))
    os.replace(tmp, path)


def load_logits(path: str):
    if not os.path.exists(path):
        return None
    with np.load(path, allow_pickle=True) as data:
        return {
            "logits": data["logits"],
            "labels": data["labels"],
            "paths": [str(p) for p in data["paths"]],
            "meta": json.loads(str(data["meta"])) if "meta" in data else {},
        }


def _file_fingerprint(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


# ----------------------------------------------------------------------------- reporting

def compare_metrics(before: dict, after: dict) -> list[dict]:
    return [
        {"metric": m, "before": float(before[m]), "after": float(after[m]), "delta": float(after[m] - before[m])}
        for m in HEADLINE_METRICS if m in before and m in after
    ]


def _pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def render_report(split: str, before: dict, after: dict, class_names, settings: dict, n_images: int) -> str:
    lines = [
        f"## Recalibration on {split} ({n_images} images)",
        "",
        f"Settings: prior-correction strength **{settings['strength']}**, temperature **{settings['temperature']:.3g}**",
        "",
        "| Metric | Before | After | Change |",
        "|---|---|---|---|",
    ]
    for row in compare_metrics(before, after):
        lines.append(f"| {METRIC_LABELS[row['metric']]} | {_pct(row['before'])} | {_pct(row['after'])} | "
                     f"{100 * row['delta']:+.1f} pts |")
    if "ece" in before and "ece" in after:
        lines.append(f"| Calibration error (ECE, lower is better) | {_pct(before['ece'])} | {_pct(after['ece'])} | "
                     f"{100 * (after['ece'] - before['ece']):+.1f} pts |")
    lines += ["", "| Class | Recall before → after | Precision before → after | Images |", "|---|---|---|---|"]
    for name in class_names:
        b, a = before["per_class_metrics"][name], after["per_class_metrics"][name]
        lines.append(f"| {name} | {_pct(b['recall'])} → {_pct(a['recall'])} | "
                     f"{_pct(b['precision'])} → {_pct(a['precision'])} | {a.get('support', '')} |")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------- model pass (torch)

def _pick_device(requested: str) -> str:  # pragma: no cover - hardware dependent
    import torch

    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class EvalDataset:
    """Map-style dataset (no torch import at module load; picklable for macOS/Windows workers).

    Returns (7 patches tensor, index); unreadable files return a negative index and are dropped.
    """

    def __init__(self, paths, n_patches: int = 7):
        self.paths = list(paths)
        self.n_patches = n_patches

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, i):
        import torch
        from PIL import Image

        from ..inference import preprocess_patches
        from .dataset import extract_patches

        # Same seeding rule as the legacy evaluator: deterministic patches per file.
        seed = zlib.crc32(os.path.normpath(self.paths[i]).encode("utf-8")) & 0xFFFFFFFF
        try:
            with Image.open(self.paths[i]) as img:
                patches = extract_patches(img.convert("RGBA"), n_patches=self.n_patches,
                                          rng=np.random.default_rng(seed))
            return preprocess_patches(patches), i
        except Exception:
            return torch.zeros(self.n_patches, 3, 224, 224), -1 - i


def collect_logits(model, paths, labels, device, batch_size=16, num_workers=2):
    """Mean-over-7-patches logits for each image (the rule used at inference). Skips unreadable files."""
    import torch
    from torch.utils.data import DataLoader

    loader = DataLoader(EvalDataset(paths), batch_size=batch_size, shuffle=False, num_workers=num_workers,
                        persistent_workers=False)
    model = model.to(device).float().eval()
    out_logits, out_idx = [], []
    start, done = time.time(), 0
    with torch.no_grad():
        for batch, idx in loader:
            bs, n, c, h, w = batch.shape
            with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=(device == "cuda")):
                logits = model(batch.to(device).view(-1, c, h, w))
            out_logits.append(logits.float().view(bs, n, -1).mean(1).cpu().numpy())
            out_idx.append(idx.numpy())
            done += bs
            if done % (batch_size * 50) < batch_size or done == len(paths):
                rate = done / max(1e-6, time.time() - start)
                eta = (len(paths) - done) / max(rate, 1e-6)
                print(f"  {done}/{len(paths)} images  ({rate:.1f} img/s, ~{eta / 60:.1f} min left)", flush=True)
    logits, idx = np.concatenate(out_logits), np.concatenate(out_idx)
    ok = idx >= 0
    if (~ok).any():
        print(f"  skipped {int((~ok).sum())} unreadable image(s)")
    keep = idx[ok]
    return logits[ok], np.asarray(labels)[keep], [paths[i] for i in keep]


# ----------------------------------------------------------------------------- CLI

def _evaluate(logits, labels, names, train_priors, target_priors, strength, temperature):
    m = evaluate_with_prior_correction(logits, labels, names, train_priors, target_priors, strength, temperature)
    probs = softmax(np.asarray(logits, dtype=np.float64) / temperature)
    if strength:
        from ..postprocess import prior_correction

        probs = prior_correction(probs, train_priors, target_priors, strength)
    m["ece"] = expected_calibration_error(probs, labels)
    return m


def main(argv=None):
    from ..inference import FabricClassifier

    default_weights = os.path.join(os.path.dirname(os.path.dirname(__file__)), "weights", "fabric_clf_best.pt")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--weights", default=default_weights)
    p.add_argument("--imaterialist-dir", "--data-dir", dest="imaterialist_dir",
                   default=os.environ.get("FABRIC_IMATERIALIST_DIR"),
                   help="folder containing <split>/<Class>/ images (or set FABRIC_IMATERIALIST_DIR)")
    p.add_argument("--select-split", default="val", help="split used to choose settings")
    p.add_argument("--test-split", default="test", help="split reported once with --report-test")
    p.add_argument("--train-counts-json", default=None,
                   help="per-class training counts (JSON) instead of counting a train/ folder")
    p.add_argument("--target-priors", default="select-split", choices=["select-split", "train-counts"],
                   help="deployment class frequencies: estimated from the select split, or the training data's")
    p.add_argument("--prior-smoothing", type=float, default=1.0,
                   help="add-k smoothing when estimating priors from the select split (no class gets 0)")
    p.add_argument("--out", default="runs/recalibration", help="where logits cache and reports go")
    p.add_argument("--device", default="auto", help="auto | cuda | mps | cpu")
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--num-workers", type=int, default=2)
    p.add_argument("--limit-per-class", type=int, default=None, help="quick trial on a subset")
    p.add_argument("--metric", default="macro_f1", choices=["macro_f1", "top1_accuracy", "balanced_accuracy"])
    p.add_argument("--min-worst-recall", type=float, default=0.40)
    p.add_argument("--sampler-power", type=float, default=0.0, help="legacy weights: 0 (balanced sampler)")
    p.add_argument("--unweighted-loss", action="store_true", help="set if trained WITHOUT class-weighted loss")
    p.add_argument("--report-test", action="store_true", help="also evaluate test (do this once)")
    p.add_argument("--write", action="store_true", help="save settings to calibration/temperature.json")
    args = p.parse_args(argv)
    if not args.imaterialist_dir:
        p.error("--imaterialist-dir is required (or set FABRIC_IMATERIALIST_DIR)")

    clf = FabricClassifier(args.weights, device="cpu")
    names = list(clf.class_names)
    fingerprint = _file_fingerprint(args.weights)
    device = None

    def get_logits(split):
        nonlocal device
        cache_path = os.path.join(args.out, f"logits_{split}.npz")
        meta = {"weights": fingerprint, "split": split, "limit_per_class": args.limit_per_class,
                "data_root": os.path.abspath(args.imaterialist_dir)}
        cached = load_logits(cache_path)
        if cached is not None and cached["meta"] == meta:
            print(f"[{split}] using cached logits ({len(cached['labels'])} images): {cache_path}")
            return cached["logits"], cached["labels"]
        paths, labels = list_split(args.imaterialist_dir, split, names, args.limit_per_class)
        device = device or _pick_device(args.device)
        print(f"[{split}] running the model on {len(paths)} images (device: {device}) ...")
        logits, labels, paths = collect_logits(clf.model, paths, labels, device, args.batch_size, args.num_workers)
        save_logits(cache_path, logits, labels, paths, meta)
        return logits, labels

    sel, tst = args.select_split, args.test_split
    val_logits, val_y = get_logits(sel)
    n = len(names)
    if args.train_counts_json:
        train_counts = load_train_counts_json(args.train_counts_json, names)
    else:
        train_counts = count_split(args.imaterialist_dir, "train", names)
    train_priors = effective_training_prior(train_counts, args.sampler_power, not args.unweighted_loss)
    if args.target_priors == "train-counts":
        target_priors = train_counts / train_counts.sum()
    else:
        smoothed = np.bincount(val_y, minlength=n) + args.prior_smoothing
        target_priors = smoothed / smoothed.sum()

    results = sweep_prior_correction(val_logits, val_y, names, train_priors, target_priors)
    best = best_result(results, args.metric, args.min_worst_recall)
    strength = float(best["strength"])
    offset = strength * np.log(np.clip(target_priors, 1e-12, None) / np.clip(train_priors, 1e-12, None))
    temperature = fit_temperature(val_logits, val_y, offset=offset)
    settings = {"strength": strength, "temperature": temperature}

    report = ["# Recalibration report", "",
              f"Weights: `{os.path.basename(args.weights)}` ({fingerprint}) · data: `{args.imaterialist_dir}`", "",
              f"Settings chosen on `{sel}`; target class frequencies from: {args.target_priors}.", "",
              "Before = the model as it is today (argmax, no correction).", ""]
    all_results = {"settings": settings, "sweep": [{"strength": r["strength"], **{k: r["metrics"][k] for k in
                   ("top1_accuracy", "macro_f1", "worst_class_recall")}} for r in results]}
    for split, (logits, y) in [(sel, (val_logits, val_y))] + (
            [(tst, get_logits(tst))] if args.report_test else []):
        before = _evaluate(logits, y, names, train_priors, target_priors, 0.0, 1.0)
        after = _evaluate(logits, y, names, train_priors, target_priors, strength, temperature)
        report.append(render_report(split, before, after, names, settings, len(y)))
        all_results[split] = {"before": before, "after": after}

    os.makedirs(args.out, exist_ok=True)
    report_text = "\n".join(report)
    with open(os.path.join(args.out, "recalibration_report.md"), "w") as f:
        f.write(report_text)
    with open(os.path.join(args.out, "recalibration_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)
    print("\n" + report_text)

    if args.write:
        calib_path = os.path.abspath(os.path.join(os.path.dirname(args.weights), "..", "calibration",
                                                  "temperature.json"))
        calib = {}
        if os.path.exists(calib_path):
            with open(calib_path) as f:
                calib = json.load(f)
        calib["temperature"] = temperature
        calib["prior_correction"] = {
            "target_priors": target_priors.tolist(),
            "train_priors": train_priors.tolist(),
            "strength": strength,
            "selected_on": f"{args.imaterialist_dir} [{sel}]",
            "target_priors_from": args.target_priors,
            "metric": args.metric,
            "weights_fingerprint": fingerprint,
        }
        os.makedirs(os.path.dirname(calib_path), exist_ok=True)
        with open(calib_path, "w") as f:
            json.dump(calib, f, indent=4)
        print(f"Saved calibration to {calib_path}")
    return all_results


if __name__ == "__main__":  # pragma: no cover
    main()
