"""Train the CLIP linear head on the external garment photos and save ``clip_head.npz``.

1. Sanity check: head fitted on the "calib" half (≤300/class) is scored on the same 483
   "eval" photos as EXP-404 — must reproduce roughly the probe's 58% balanced accuracy,
   proving that the serving pipeline (512-px resize → CLIP → head) matches the experiment.
2. Final head: fitted on every collected photo (calib + eval, ≤600/class), since more data
   helps; its quality estimate is the number from step 1.

    python -m tools.train_clip_head --data-dir data/external --out reports/clip_head
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np


def main(argv=None):  # pragma: no cover - needs torch, transformers, data
    import torch
    from PIL import Image

    from backend.fabric_classifier.classes import MATERIAL_CLASSES
    from backend.fabric_classifier.clip_head import ClipEmbedder, LinearHead
    from backend.fabric_classifier.training.dataset import resize_max_side
    from backend.fabric_classifier.training.recalibrate import list_split
    from tools.backbone_probe import evaluate_scores
    from tools.patch_diagnostic import cap_per_class

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", default="data/external")
    p.add_argument("--out", default="reports/clip_head")
    p.add_argument("--cap", type=int, default=600)
    p.add_argument("--C", type=float, default=0.01, help="regularisation chosen by EXP-404")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    torch.set_grad_enabled(False)
    torch.set_num_threads(os.cpu_count() or 4)
    names = list(MATERIAL_CLASSES)

    embedder = ClipEmbedder(device="cpu")

    def embed_all(paths):
        out = []
        for n, path in enumerate(paths):
            with Image.open(path) as im:
                out.append(embedder.embed(resize_max_side(im.convert("RGB"), 512)))
            if n % 200 == 0:
                print(f"  {n}/{len(paths)}", flush=True)
        return np.stack(out)

    sets = {}
    for split in ("calib", "eval"):
        paths, labels = list_split(args.data_dir, split, names)
        keep = cap_per_class(labels, args.cap, args.seed)
        sets[split] = ([paths[i] for i in keep], labels[keep], keep)
    # nested subsets identical to EXP-404 (cap_per_class draws are prefix-stable per class)
    def subset(split, cap):
        paths, labels, _ = sets[split]
        all_paths, all_labels = list_split(args.data_dir, split, names)
        want = {all_paths[i] for i in cap_per_class(all_labels, cap, args.seed)}
        return np.array([i for i, q in enumerate(paths) if q in want])

    X, Y = {}, {}
    for split in ("calib", "eval"):
        print(f"embedding {split}: {len(sets[split][0])} photos", flush=True)
        X[split], Y[split] = embed_all(sets[split][0]), sets[split][1]

    ci, ei = subset("calib", 300), subset("eval", 150)
    check = LinearHead.fit(X["calib"][ci], Y["calib"][ci], names, C=args.C, seed=args.seed)
    res = evaluate_scores(Y["eval"][ei], np.log(check.probabilities(X["eval"][ei]) + 1e-12), names)
    print(f"sanity check (EXP-404 protocol): balanced acc {res['balanced_accuracy']:.3f} on {len(ei)} photos")

    X_all, Y_all = np.vstack([X["calib"], X["eval"]]), np.concatenate([Y["calib"], Y["eval"]])
    head = LinearHead.fit(X_all, Y_all, names, C=args.C, seed=args.seed)
    head.save(os.path.join(args.out, "clip_head.npz"))
    counts = {names[c]: int((Y_all == c).sum()) for c in range(len(names))}
    with open(os.path.join(args.out, "summary.json"), "w") as f:
        json.dump({"sanity_check": {k: v for k, v in res.items()}, "train_counts": counts,
                   "n_train": int(len(Y_all)), "C": args.C}, f, indent=1, default=float)
    print("trained on", len(Y_all), "photos:", counts)


if __name__ == "__main__":  # pragma: no cover
    main()
