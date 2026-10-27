"""Diagnostic: how do the CLIP head, CLIP zero-shot and a blend of both do on (a) the app's
sample photos (close-ups of cloth) and (b) held-out everyday photos? Fits the head on the calib
half only (≤50/class) so the eval half stays unseen.

    python -m tools.sample_check --data-dir data/external --samples test_images/samples --out reports/sample_check
"""
from __future__ import annotations

import argparse
import glob
import json
import os

import numpy as np


def log_softmax(x):
    x = np.asarray(x, dtype=np.float64)
    x = x - x.max(axis=-1, keepdims=True)
    return x - np.log(np.exp(x).sum(axis=-1, keepdims=True))


def main(argv=None):  # pragma: no cover - needs torch, transformers, data
    import torch
    from PIL import Image

    from backend.fabric_classifier.classes import MATERIAL_CLASSES
    from backend.fabric_classifier.clip_head import ClipEmbedder, LinearHead, l2_normalize
    from backend.fabric_classifier.training.dataset import resize_max_side
    from backend.fabric_classifier.training.recalibrate import list_split
    from tools.backbone_probe import build_prompts, zero_shot_scores
    from tools.patch_diagnostic import cap_per_class

    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", default="data/external")
    p.add_argument("--samples", default="test_images/samples")
    p.add_argument("--out", default="reports/sample_check")
    p.add_argument("--calib-cap", type=int, default=50)
    p.add_argument("--eval-cap", type=int, default=150)
    args = p.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    torch.set_grad_enabled(False)
    torch.set_num_threads(os.cpu_count() or 4)
    names = list(MATERIAL_CLASSES)
    emb = ClipEmbedder(device="cpu")

    def embed(paths):
        out = []
        for n, path in enumerate(paths):
            with Image.open(path) as im:
                out.append(emb.embed(resize_max_side(im.convert("RGB"), 512)))
            if n % 100 == 0:
                print(f"  {n}/{len(paths)}", flush=True)
        return np.stack(out)

    cp, cy = list_split(args.data_dir, "calib", names)
    ep, ey = list_split(args.data_dir, "eval", names)
    ci, ei = cap_per_class(cy, args.calib_cap, 0), cap_per_class(ey, args.eval_cap, 0)
    Xc, yc = embed([cp[i] for i in ci]), cy[ci]
    Xe, ye = embed([ep[i] for i in ei]), ey[ei]
    sample_paths = sorted(glob.glob(os.path.join(args.samples, "*.jp*g")))
    Xs = embed(sample_paths)

    prompts = build_prompts(names)
    flat = [t for n in names for t in prompts[n]]
    T = np.asarray(emb.embed_texts(flat))
    k = len(prompts[names[0]])
    text = [T[i * k:(i + 1) * k] for i in range(len(names))]

    head = LinearHead.fit(Xc, yc, names, C=0.01)
    present = np.unique(ye)

    def bal_acc(scores):
        pred = scores.argmax(1)
        return float(np.mean([np.mean(pred[ye == c] == c) for c in present]))

    def combine(X, w):
        h = np.log(head.probabilities(X) + 1e-12)
        z = log_softmax(zero_shot_scores(X, text))
        return (1 - w) * h + w * z

    weights = [0.0, 0.25, 0.5, 0.75, 1.0]
    result = {"eval_balanced_accuracy": {str(w): bal_acc(combine(Xe, w)) for w in weights}, "samples": {}}
    for w in weights:
        sc = combine(Xs, w)
        for path, row in zip(sample_paths, sc):
            top = np.argsort(-row)[:3]
            probs = np.exp(log_softmax(row))
            result["samples"].setdefault(os.path.basename(path), {})[str(w)] = [
                f"{names[i]} {100 * probs[i]:.0f}%" for i in top]
    # old EfficientNet model for reference
    try:
        from backend.fabric_classifier.inference import FabricClassifier

        old = FabricClassifier(os.path.join("backend", "fabric_classifier", "weights", "fabric_clf_best.pt"), device="cpu")
        for path in sample_paths:
            with Image.open(path) as im:
                result["samples"][os.path.basename(path)]["efficientnet_old"] = [
                    f"{r['name']} {r['confidence']:.0f}%" for r in old.predict(im.convert("RGB"))]
    except Exception as e:
        result["efficientnet_error"] = str(e)
    with open(os.path.join(args.out, "results.json"), "w") as f:
        json.dump(result, f, indent=1)
    print(json.dumps(result, indent=1))


if __name__ == "__main__":  # pragma: no cover
    main()
