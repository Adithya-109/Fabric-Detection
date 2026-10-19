import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, UnidentifiedImageError


IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

REPO_ROOT = Path(__file__).resolve().parents[3]
TRAINING_DIR = REPO_ROOT / "backend" / "fabric_classifier" / "training"
MANIFEST_PATH = TRAINING_DIR / "additional_data_manifest.json"

MICRO_ROOT = REPO_ROOT / "DATASETS" / "Microscope images of fabric" / "Microscope 1- Textile Factory samples"
IBUG_ROOT = REPO_ROOT / "DATASETS" / "The Fabrics Dataset by iBUG"

MICRO_INCLUDE = {
    "Contrado - Lycra": "Nylon",
    "Contrado-Crepe": "Silk",
    "Contrado-Jersey": "Knitted",
    "Contrado-Nylon": "Nylon",
    "Contrado-Satin": "Satin",
    "Contrado-Silk": "Silk",
    "Contrado-Velvet": "Velvet",
    "Cotton": "Cotton",
    "Linen": "Linen",
    "Polyester": "Polyester",
}

MICRO_EXCLUDE = {
    "Cotton Sateen",
    "Cotton-Linen-Blend1",
    "Cotton-Linen-Blend2",
    "Cotton-Silk-Blend",
}

IBUG_INCLUDE = {
    "Polyester": "Polyester",
    "Velvet": "Velvet",
    "Chenille": "Velvet",
    "Nylon": "Nylon",
    "Linen": "Linen",
    "Viscose": "Linen",
    "Fleece": "Fleece",
    "Artificial_fur": "Fleece",
    "Leather": "Leather",
    "Artificial_leather": "Leather",
    "Cotton": "Cotton",
    "Silk": "Silk",
    "Satin": "Satin",
    "Denim": "Denim",
    "Corduroy": "Corduroy",
    "Wool": "Wool",
    "Suede": "Suede",
    "Knitted": "Knitted",
}

IBUG_EXCLUDE_EXPLICIT = {
    "Acrylic",
    "Blended",
    "Lut",
    "Terrycloth",
    "Unclassified",
    "Utilities",
}

# Removed IBUG_TARGET_CAPS for Phase 3 policy (use all valid images)


def to_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def collect_images(folder: Path):
    if not folder.exists() or not folder.is_dir():
        return []
    paths = []
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXTENSIONS:
            paths.append(p)
    return sorted(paths)


def is_valid_image(path: Path):
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except (UnidentifiedImageError, OSError, ValueError, RuntimeError):
        return False


# Removed balanced_cap function for Phase 3 policy (use all valid images)


def build_microscope_block():
    by_target = defaultdict(list)
    included = {}
    excluded = {}
    invalid_paths = []

    if not MICRO_ROOT.exists():
        return {
            "license": "MIT",
            "research_only": False,
            "included_classes": {},
            "excluded_classes": {},
            "images_by_target": {},
            "counts_by_target": {},
            "invalid_images": [],
            "total_valid_images": 0,
            "missing_root": True,
        }

    for class_name, target in MICRO_INCLUDE.items():
        class_dir = MICRO_ROOT / class_name
        raw = collect_images(class_dir)
        valid = []
        for p in raw:
            if is_valid_image(p):
                valid.append(to_rel(p))
            else:
                invalid_paths.append(to_rel(p))
        included[class_name] = len(valid)
        by_target[target].extend(valid)

    for class_name in sorted(MICRO_EXCLUDE):
        excluded[class_name] = len(collect_images(MICRO_ROOT / class_name))

    images_by_target = {k: sorted(v) for k, v in by_target.items()}
    counts_by_target = {k: len(v) for k, v in images_by_target.items()}

    return {
        "license": "MIT",
        "research_only": False,
        "included_classes": dict(sorted(included.items())),
        "excluded_classes": excluded,
        "images_by_target": images_by_target,
        "counts_by_target": counts_by_target,
        "invalid_images": invalid_paths[:100],
        "total_valid_images": int(sum(counts_by_target.values())),
    }


def build_ibug_block():
    by_target_by_source = defaultdict(lambda: defaultdict(list))
    included = {}
    excluded = {}
    invalid_paths = []

    if not IBUG_ROOT.exists():
        return {
            "license": "Research-only",
            "research_only": True,
            "included_classes": {},
            "excluded_classes": {},
            "images_by_target": {},
            "counts_by_target": {},
            "invalid_images": [],
            "total_valid_images": 0,
            "missing_root": True,
        }

    for class_dir in sorted([p for p in IBUG_ROOT.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
        class_name = class_dir.name

        if class_name in IBUG_EXCLUDE_EXPLICIT:
            excluded[class_name] = len(collect_images(class_dir))
            continue

        target = IBUG_INCLUDE.get(class_name)
        if target is None:
            excluded[class_name] = len(collect_images(class_dir))
            continue

        raw = collect_images(class_dir)
        valid = []
        for p in raw:
            if is_valid_image(p):
                valid.append(to_rel(p))
            else:
                invalid_paths.append(to_rel(p))

        included[class_name] = len(valid)
        by_target_by_source[target][class_name].extend(valid)

    images_by_target = {}
    counts_by_target = {}

    for target, source_map in sorted(by_target_by_source.items(), key=lambda kv: kv[0]):
        selected = []
        for src, paths in source_map.items():
            selected.extend(paths)
        images_by_target[target] = selected
        counts_by_target[target] = len(selected)

    return {
        "license": "Research-only",
        "research_only": True,
        "included_classes": dict(sorted(included.items())),
        "excluded_classes": dict(sorted(excluded.items())),
        "images_by_target": images_by_target,
        "counts_by_target": counts_by_target,
        "invalid_images": invalid_paths[:100],
        "total_valid_images": int(sum(counts_by_target.values())),
    }


def main():
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "version": 1,
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "datasets": {
            "microscope_mit": build_microscope_block(),
            "ibug_research_only": build_ibug_block(),
        },
    }

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    compact = {
        "manifest": to_rel(MANIFEST_PATH),
        "microscope_total": manifest["datasets"]["microscope_mit"].get("total_valid_images", 0),
        "ibug_total": manifest["datasets"]["ibug_research_only"].get("total_valid_images", 0),
        "microscope_counts": manifest["datasets"]["microscope_mit"].get("counts_by_target", {}),
        "ibug_counts": manifest["datasets"]["ibug_research_only"].get("counts_by_target", {}),
    }
    print(json.dumps(compact, ensure_ascii=True))


if __name__ == "__main__":
    main()
