"""Compare patch-selection strategies on external garment photos (no training).

Question: does the current model do better when its 7 patches actually land on the
garment? Variants, each run with the SAME weights:

  legacy_orig  – today's behaviour: "not near-white" mask on the original-resolution photo
  legacy_512   – same, after resizing the photo to max side 512 (the training data's scale)
  centre_512   – patches only from the central region (width 50%, height 60%)
  garment_512  – patches only from the largest clothing region found by a clothes
                 segmentation model (mattmdjaga/segformer_b2_clothes)
  whole        – no patches: the whole photo resized to 224×224 (reference)

Metrics are reported raw and after undoing the training-prior inversion
(train prior ∝ 1/count → uniform). The eval set is capped per class so every class
counts; Cotton-vs-Polyester AUC is independent of class priors.
"""
from __future__ import annotations

import argparse
import json
import os
import zlib

import numpy as np
from PIL import Image, ImageDraw

from backend.fabric_classifier.classes import MATERIAL_CLASSES

# segformer_b2_clothes label ids that are garments (not skin, hair, shoes, bags, background)
CLOTHING_LABELS = {4: "Upper-clothes", 5: "Skirt", 6: "Pants", 7: "Dress", 17: "Scarf"}
VARIANTS = ("legacy_orig", "legacy_512", "centre_512", "garment_512", "whole")
VARIANT_COLOURS = {"legacy_orig": (255, 60, 60), "legacy_512": (255, 150, 0), "centre_512": (40, 120, 255),
                   "garment_512": (0, 200, 80)}


def central_mask(height: int, width: int, width_frac: float = 0.5, height_frac: float = 0.6) -> np.ndarray:
    mask = np.zeros((height, width), dtype=bool)
    w, h = int(round(width * width_frac)), int(round(height * height_frac))
    x0, y0 = (width - w) // 2, (height - h) // 2
    mask[y0:y0 + h, x0:x0 + w] = True
    return mask


def garment_mask(label_map, clothing_ids=CLOTHING_LABELS, mode: str = "largest") -> np.ndarray:
    """Clothing pixels from a segmentation label map; ``largest`` keeps only the biggest garment class."""
    label_map = np.asarray(label_map)
    ids = [i for i in clothing_ids if np.any(label_map == i)]
    if not ids:
        return np.zeros(label_map.shape, dtype=bool)
    if mode == "any":
        return np.isin(label_map, ids)
    biggest = max(ids, key=lambda i: int((label_map == i).sum()))
    return label_map == biggest


def rank_metrics(logits, labels) -> dict:
    logits, labels = np.asarray(logits, dtype=np.float64), np.asarray(labels)
    true = logits[np.arange(len(labels)), labels]
    ranks = 1 + (logits > true[:, None]).sum(axis=1)
    return {
        "median_true_rank": float(np.median(ranks)),
        "mean_reciprocal_rank": float(np.mean(1.0 / ranks)),
        "top1": float(np.mean(ranks == 1)),
        "top3": float(np.mean(ranks <= 3)),
    }


def pairwise_auc(logits, labels, a: int, b: int):
    """AUC of (logit_a − logit_b) separating true-a from true-b images; None if a class is missing."""
    from sklearn.metrics import roc_auc_score

    logits, labels = np.asarray(logits), np.asarray(labels)
    sel = (labels == a) | (labels == b)
    if not np.any(labels == a) or not np.any(labels == b):
        return None
    return float(roc_auc_score(labels[sel] == a, logits[sel, a] - logits[sel, b]))


def cap_per_class(labels, cap: int, seed: int = 0) -> np.ndarray:
    labels = np.asarray(labels)
    rng = np.random.default_rng(seed)
    keep = []
    for c in np.unique(labels):
        idx = np.where(labels == c)[0]
        keep.extend(sorted(rng.permutation(idx)[:cap].tolist()))
    return np.array(sorted(keep), dtype=np.int64)


def resize_max_side(image: Image.Image, max_side: int) -> Image.Image:
    if max(image.size) <= max_side:
        return image
    scale = max_side / max(image.size)
    return image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))),
                        Image.Resampling.BILINEAR)


def draw_boxes(image: Image.Image, boxes, color=(255, 0, 0), width: int = 2) -> Image.Image:
    out = image.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    for box in boxes:
        draw.rectangle(box, outline=color, width=width)
    return out


# ----------------------------------------------------------------------------- heavy parts

class _Segmenter:  # pragma: no cover - needs transformers + network
    def __init__(self, model_id="mattmdjaga/segformer_b2_clothes"):
        import torch
        from transformers import AutoModelForSemanticSegmentation, SegformerImageProcessor

        self.torch = torch
        self.processor = SegformerImageProcessor.from_pretrained(model_id)
        self.model = AutoModelForSemanticSegmentation.from_pretrained(model_id).eval()

    def __call__(self, image: Image.Image) -> np.ndarray:
        torch = self.torch
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt")
            logits = self.model(**inputs).logits
            up = torch.nn.functional.interpolate(logits, size=image.size[::-1], mode="bilinear", align_corners=False)
        return up.argmax(dim=1)[0].numpy()


def main(argv=None):  # pragma: no cover - needs torch, transformers, data
    import torch

    from backend.fabric_classifier.inference import FabricClassifier, preprocess_patches
    from backend.fabric_classifier.postprocess import prior_correction, softmax
    from backend.fabric_classifier.training.balancing import effective_training_prior
    from backend.fabric_classifier.training.dataset import extract_patches
    from backend.fabric_classifier.training.metrics import compute_classification_metrics
    from backend.fabric_classifier.training.recalibrate import list_split, load_train_counts_json

    default_weights = os.path.join("backend", "fabric_classifier", "weights", "fabric_clf_best.pt")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", default="data/external")
    p.add_argument("--split", default="eval")
    p.add_argument("--cap", type=int, default=150, help="max images per class")
    p.add_argument("--weights", default=default_weights)
    p.add_argument("--counts-json", default="imaterialist_processed_counts.json")
    p.add_argument("--out", default="reports/patch_diagnostic")
    p.add_argument("--viz-per-class", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    torch.set_grad_enabled(False)

    names = list(MATERIAL_CLASSES)
    paths, labels = list_split(args.data_dir, args.split, names)
    keep = cap_per_class(labels, args.cap, args.seed)
    paths, labels = [paths[i] for i in keep], labels[keep]
    print(f"{len(paths)} images (cap {args.cap}/class)")

    model = FabricClassifier(args.weights, device="cpu").model.float().eval()
    segment = _Segmenter()

    def run(patches):
        return model(preprocess_patches(patches)).mean(0).numpy()

    logits = {v: [] for v in VARIANTS}
    garment_fallbacks, garment_cover = 0, []
    viz_rows, viz_count = [], {}
    for n, (path, y) in enumerate(zip(paths, labels)):
        seed = zlib.crc32(os.path.normpath(path).encode()) & 0xFFFFFFFF
        with Image.open(path) as im:
            img = im.convert("RGB")
        small = resize_max_side(img, 512)
        H, W = small.size[1], small.size[0]
        seg = segment(small)
        gmask = garment_mask(seg)
        garment_cover.append(float(gmask.mean()))
        if gmask.sum() < 160 * 160 * 0.1:
            garment_fallbacks += 1

        boxes = {}
        pats, boxes["legacy_orig"] = extract_patches(img.convert("RGBA"), rng=np.random.default_rng(seed),
                                                     return_boxes=True)
        logits["legacy_orig"].append(run(pats))
        pats, boxes["legacy_512"] = extract_patches(small.convert("RGBA"), rng=np.random.default_rng(seed),
                                                    return_boxes=True)
        logits["legacy_512"].append(run(pats))
        pats, boxes["centre_512"] = extract_patches(small.convert("RGBA"), mask=central_mask(H, W),
                                                    min_coverage=0.9, rng=np.random.default_rng(seed),
                                                    return_boxes=True)
        logits["centre_512"].append(run(pats))
        pats, boxes["garment_512"] = extract_patches(small.convert("RGBA"), mask=gmask, min_coverage=0.9,
                                                     rng=np.random.default_rng(seed), return_boxes=True)
        logits["garment_512"].append(run(pats))
        logits["whole"].append(run([img.resize((224, 224), Image.Resampling.BILINEAR)]))

        cls = names[y]
        if viz_count.get(cls, 0) < args.viz_per_class:
            viz_count[cls] = viz_count.get(cls, 0) + 1
            scale = W / img.width
            orig_boxes = [tuple(int(c * scale) for c in b) for b in boxes["legacy_orig"]]
            panels = [draw_boxes(small, orig_boxes, VARIANT_COLOURS["legacy_orig"])]
            for v in ("legacy_512", "centre_512", "garment_512"):
                panels.append(draw_boxes(small, boxes[v], VARIANT_COLOURS[v]))
            overlay = small.copy()
            tint = Image.new("RGB", small.size, (0, 200, 80))
            overlay.paste(Image.blend(small, tint, 0.45), mask=Image.fromarray((gmask * 255).astype(np.uint8)))
            panels.append(overlay)
            viz_rows.append((cls, panels))
        if n % 50 == 0:
            print(f"  {n}/{len(paths)}", flush=True)

    # ---- metrics
    counts = load_train_counts_json(args.counts_json, names)
    train_prior = effective_training_prior(counts, 0.0, True)
    uniform = np.full(len(names), 1.0 / len(names))
    cot, pol = names.index("Cotton"), names.index("Polyester")
    results, table = {}, []
    for v in VARIANTS:
        L = np.stack(logits[v])
        probs_raw = softmax(L)
        probs_fix = prior_correction(probs_raw, train_prior, uniform, strength=1.0)
        res = {"cotton_vs_polyester_auc": pairwise_auc(L, labels, cot, pol)}
        for tag, pr in (("raw", probs_raw), ("prior_fixed", probs_fix)):
            m = compute_classification_metrics(labels, pr.argmax(1), names, scores=pr, top_k=3)
            res[tag] = {**rank_metrics(np.log(pr + 1e-12), labels),
                        "macro_f1": m["macro_f1"], "balanced_accuracy": m["balanced_accuracy"],
                        "per_class_recall": {c: m["per_class_metrics"][c]["recall"] for c in names
                                             if m["per_class_metrics"][c]["support"] > 0},
                        "prediction_counts": dict(zip(*np.unique([names[i] for i in pr.argmax(1)],
                                                                 return_counts=True)))}
        results[v] = res
        f = res["prior_fixed"]
        auc = res["cotton_vs_polyester_auc"]
        auc_txt = "n/a" if auc is None else f"{auc:.3f}"
        table.append(f"| {v} | {100 * f['balanced_accuracy']:.1f}% | {100 * f['macro_f1']:.1f}% | "
                     f"{100 * f['top3']:.1f}% | {f['median_true_rank']:.0f} | "
                     f"{auc_txt} | {100 * res['raw']['balanced_accuracy']:.1f}% |")
    results["meta"] = {"images": len(paths), "per_class": {c: int((labels == i).sum()) for i, c in enumerate(names)
                                                          if (labels == i).any()},
                       "garment_mask_fallbacks": garment_fallbacks,
                       "mean_garment_fraction": float(np.mean(garment_cover))}
    for k in results:
        if k in VARIANTS:
            for tag in ("raw", "prior_fixed"):
                results[k][tag]["prediction_counts"] = {a: int(b) for a, b in results[k][tag]["prediction_counts"].items()}

    present = [c for c in names if (labels == names.index(c)).any()]
    recall_rows = ["| Class | n | " + " | ".join(VARIANTS) + " |", "|---|---|" + "---|" * len(VARIANTS)]
    for c in present:
        recall_rows.append(f"| {c} | {results['meta']['per_class'][c]} | " + " | ".join(
            f"{100 * results[v]['prior_fixed']['per_class_recall'][c]:.0f}%" for v in VARIANTS) + " |")

    report = "\n".join([
        "# Patch-strategy diagnostic", "",
        f"{len(paths)} images from `{args.data_dir}/{args.split}` (≤{args.cap} per class). Weights: `{args.weights}`.",
        f"Garment mask too small → centre-crop fallback on {garment_fallbacks} images; "
        f"garment covers {100 * results['meta']['mean_garment_fraction']:.0f}% of a photo on average.", "",
        "Chance level: balanced accuracy ≈ 1/13 = 7.7%, median rank ≈ 7, AUC = 0.5.", "",
        "| Variant | Balanced acc. | Macro-F1 | Top-3 | Median true rank | Cotton-vs-Poly AUC | Balanced acc. (raw) |",
        "|---|---|---|---|---|---|---|", *table, "",
        "Columns 2–5 are after undoing the training-prior inversion (no tuning on this data).", "",
        "## Recall per class (prior-fixed)", "", *recall_rows, "",
    ])
    with open(os.path.join(args.out, "report.md"), "w") as f:
        f.write(report)
    with open(os.path.join(args.out, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    np.savez_compressed(os.path.join(args.out, "logits.npz"), labels=labels,
                        **{v: np.stack(logits[v]) for v in VARIANTS})

    # ---- visual grid: one row per example, columns = variants + garment mask
    th = 256
    rows = []
    for cls, panels in viz_rows:
        scaled = [pn.resize((max(1, int(pn.width * th / pn.height)), th)) for pn in panels]
        row = Image.new("RGB", (110 + sum(s.width for s in scaled) + 4 * len(scaled), th), "white")
        ImageDraw.Draw(row).text((4, th // 2), cls, fill="black")
        x = 110
        for s in scaled:
            row.paste(s, (x, 0))
            x += s.width + 4
        rows.append(row)
    if rows:
        header = Image.new("RGB", (max(r.width for r in rows), 22), "white")
        ImageDraw.Draw(header).text((114, 4), "legacy_orig (red) | legacy_512 (orange) | centre_512 (blue) | "
                                               "garment_512 (green) | garment mask", fill="black")
        grid = Image.new("RGB", (header.width, 22 + th * len(rows)), "white")
        grid.paste(header, (0, 0))
        for i, r in enumerate(rows):
            grid.paste(r, (0, 22 + i * th))
        grid.save(os.path.join(args.out, "patch_examples.jpg"), quality=85)
    print(report)


if __name__ == "__main__":  # pragma: no cover
    main()
