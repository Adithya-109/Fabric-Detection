"""Prepare an external, never-trained-on dataset for evaluating the current model.

Default source: Hugging Face ``0x-Jayveersinh-Raj/fabric_classification_dataset``
(~13k Indian e-commerce garment photos, column ``text`` = listed material).

Only unambiguous single-material labels are kept and mapped to the 14 contract
classes; blends and fabrics outside the contract are dropped. Near-duplicate photos
are grouped so that copies never straddle the two halves:

    <out>/calib/<Class>/*.jpg   → used to choose prior-correction strength + temperature
    <out>/eval/<Class>/*.jpg    → used only to report before/after

Usage::

    python -m tools.prepare_external_eval --out data/external --sheet reports/external_eval/sheet.png
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict

import numpy as np
from PIL import Image, ImageDraw

from backend.fabric_classifier.training.splits import average_hash, group_near_duplicates, grouped_stratified_split

# Listed material → contract class. Anything not here is dropped.
LABEL_MAP = {
    "cotton": "Cotton", "pure cotton": "Cotton", "organic cotton": "Cotton",
    "polyester": "Polyester",
    "silk": "Silk", "pure silk": "Silk", "raw silk": "Silk", "dupion silk": "Silk",
    "denim": "Denim",
    "linen": "Linen", "hemp": "Linen",
    "wool": "Wool", "pure wool": "Wool", "pashmina": "Wool",
    "leather": "Leather", "synthetic leather": "Leather",
    "velvet": "Velvet",
    "corduroy": "Corduroy",
    "fleece": "Fleece", "faux fur": "Fleece",
    "nylon": "Nylon", "elastane": "Nylon",
    "satin": "Satin",
    "suede": "Suede",
}

SPLITS = ("calib", "eval")


def map_label(text) -> str | None:
    if not isinstance(text, str):
        return None
    return LABEL_MAP.get(" ".join(text.lower().split()))


def assign_halves(labels, hashes, seed: int = 0, max_distance: int = 4) -> np.ndarray:
    """'calib' / 'eval' for each image: ~50/50 per class, near-duplicates kept on one side."""
    groups = group_near_duplicates(hashes, max_distance=max_distance)
    calib_idx, eval_idx, _ = grouped_stratified_split(labels, groups, val_fraction=0.5, test_fraction=0.0, seed=seed)
    halves = np.empty(len(labels), dtype=object)
    halves[calib_idx] = "calib"
    halves[eval_idx] = "eval"
    return halves


def write_split_folders(records, out_dir: str) -> list[str]:
    """records: iterable of (PIL image, class name, split, index) → ``out/split/class/{index:06d}.jpg``."""
    paths = []
    for image, cls, split, idx in records:
        d = os.path.join(out_dir, split, cls)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f"{int(idx):06d}.jpg")
        image.convert("RGB").save(path, "JPEG", quality=95)
        paths.append(path)
    return paths


def contact_sheet(paths_by_class: dict, out_path: str, per_class: int = 8, thumb: int = 128) -> str:
    """One row per class: a label column then up to ``per_class`` thumbnails (for eyeballing labels)."""
    label_w = 120
    classes = list(paths_by_class)
    sheet = Image.new("RGB", (label_w + per_class * thumb, max(1, len(classes)) * thumb), "white")
    draw = ImageDraw.Draw(sheet)
    for row, cls in enumerate(classes):
        y = row * thumb
        draw.text((6, y + thumb // 2 - 6), f"{cls} ({len(paths_by_class[cls])})", fill="black")
        for col, path in enumerate(paths_by_class[cls][:per_class]):
            with Image.open(path) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb, thumb))
                sheet.paste(im, (label_w + col * thumb + (thumb - im.width) // 2, y + (thumb - im.height) // 2))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    sheet.save(out_path)
    return out_path


def _find_columns(features):  # pragma: no cover - depends on the dataset
    image_col = next(k for k, v in features.items() if type(v).__name__ == "Image")
    text_col = "text" if "text" in features else next(k for k, v in features.items() if k != image_col)
    return image_col, text_col


def main(argv=None):  # pragma: no cover - needs network + `datasets`
    from datasets import load_dataset, load_from_disk
    from huggingface_hub import snapshot_download

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", default="0x-Jayveersinh-Raj/fabric_classification_dataset")
    p.add_argument("--out", default="data/external")
    p.add_argument("--sheet", default=None, help="write a contact sheet PNG of sample images per class")
    p.add_argument("--summary", default=None, help="write a JSON summary of label mapping and counts")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args(argv)

    local = snapshot_download(args.dataset, repo_type="dataset")
    try:
        ds = load_from_disk(local)
    except Exception:
        ds = load_dataset(args.dataset, split="train")
    if hasattr(ds, "keys") and not hasattr(ds, "features"):  # DatasetDict
        ds = ds[list(ds.keys())[0]]
    image_col, text_col = _find_columns(ds.features)

    texts = ds[text_col]
    source_counts = Counter(texts)
    keep = [i for i, t in enumerate(texts) if map_label(t)]
    print(f"{len(keep)} of {len(texts)} images have an unambiguous single-material label")

    staging = os.path.join(args.out, "_staging")
    os.makedirs(staging, exist_ok=True)
    labels, hashes, kept, bad = [], [], [], 0
    for n, i in enumerate(keep):
        try:
            img = ds[i][image_col].convert("RGB")
        except Exception:
            bad += 1
            continue
        hashes.append(average_hash(img))
        labels.append(map_label(texts[i]))
        kept.append(i)
        img.save(os.path.join(staging, f"{i:06d}.jpg"), "JPEG", quality=95)
        if n % 1000 == 0:
            print(f"  decoded {n}/{len(keep)}", flush=True)
    names = sorted(set(labels))
    halves = assign_halves(np.array([names.index(l) for l in labels]), hashes, seed=args.seed)

    by_class = defaultdict(list)
    counts = defaultdict(Counter)
    for i, cls, half in zip(kept, labels, halves):
        d = os.path.join(args.out, half, cls)
        os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, f"{i:06d}.jpg")
        os.replace(os.path.join(staging, f"{i:06d}.jpg"), dst)
        counts[half][cls] += 1
        if half == "eval":
            by_class[cls].append(dst)
    os.rmdir(staging)

    summary = {
        "dataset": args.dataset,
        "total_rows": len(texts),
        "kept": len(kept),
        "unreadable": bad,
        "counts": {h: dict(sorted(c.items())) for h, c in counts.items()},
        "source_labels_kept": {t: n for t, n in source_counts.most_common() if map_label(t)},
        "source_labels_dropped": {t: n for t, n in source_counts.most_common() if not map_label(t)},
    }
    print(json.dumps(summary["counts"], indent=2))
    if args.summary:
        os.makedirs(os.path.dirname(os.path.abspath(args.summary)), exist_ok=True)
        with open(args.summary, "w") as f:
            json.dump(summary, f, indent=2)
    if args.sheet:
        rng = np.random.default_rng(args.seed)
        sample = {c: list(rng.permutation(v)) for c, v in sorted(by_class.items())}
        contact_sheet(sample, args.sheet)
        print(f"contact sheet: {args.sheet}")


if __name__ == "__main__":  # pragma: no cover
    main()
