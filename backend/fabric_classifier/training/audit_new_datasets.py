import json
import os
import re
from pathlib import Path

from PIL import Image, UnidentifiedImageError


MATERIAL_CLASSES = [
    "Cotton",
    "Polyester",
    "Silk",
    "Denim",
    "Linen",
    "Wool",
    "Leather",
    "Velvet",
    "Corduroy",
    "Fleece",
    "Nylon",
    "Satin",
    "Knitted",
    "Suede",
]

IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

DATASETS = [
    {
        "name": "Microscope images of fabric",
        "root": Path(r"DATASETS/Microscope images of fabric"),
        "license": "MIT",
        "capture_hint": "microscope texture close-up",
    },
    {
        "name": "The Fabrics Dataset by iBUG",
        "root": Path(r"DATASETS/The Fabrics Dataset by iBUG"),
        "license": "Research only",
        "capture_hint": "garment/material photos",
    },
]


def normalize_token(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
    return re.sub(r"_+", "_", lowered).strip("_")


def infer_target_class(folder_name: str):
    token = normalize_token(folder_name)

    rules = [
        (["cotton", "canvas", "chambray", "gingham", "lawn", "twill"], "Cotton", "cotton-family token"),
        (["polyester"], "Polyester", "polyester token"),
        (["silk", "chiffon", "organza", "taffeta", "crepe"], "Silk", "silk-family token"),
        (["denim"], "Denim", "denim token"),
        (["linen", "flax", "hemp", "ramie", "viscose"], "Linen", "linen-family token"),
        (["wool", "cashmere", "alpaca", "mohair", "angora", "camel", "yak", "llama", "flannel", "tweed", "felt"], "Wool", "wool-family token"),
        (["leather", "faux_leather", "artificial_leather", "vinyl"], "Leather", "leather-family token"),
        (["velvet", "chenille"], "Velvet", "velvet-family token"),
        (["corduroy"], "Corduroy", "corduroy token"),
        (["fleece", "fur", "faux_fur", "artificial_fur"], "Fleece", "fleece/fur token"),
        (["nylon", "lycra", "spandex", "elastane", "polyolefin", "aramid", "tulle", "neoprene"], "Nylon", "nylon/elastane token"),
        (["satin", "sateen"], "Satin", "satin/sateen token"),
        (["knit", "knitted", "knitwear", "jersey"], "Knitted", "knit/jersey token"),
        (["suede"], "Suede", "suede token"),
    ]

    for keywords, target, reason in rules:
        for key in keywords:
            if key in token:
                return target, reason

    if "blend" in token:
        return None, "blend token (ambiguous)"

    return None, "no reliable mapping token"


class RunningStats:
    def __init__(self):
        self.count = 0
        self.sum = 0.0
        self.min_val = None
        self.max_val = None

    def add(self, value: float):
        self.count += 1
        self.sum += float(value)
        if self.min_val is None or value < self.min_val:
            self.min_val = float(value)
        if self.max_val is None or value > self.max_val:
            self.max_val = float(value)

    def as_dict(self):
        if self.count == 0:
            return {"count": 0, "mean": 0.0, "min": None, "max": None}
        return {
            "count": self.count,
            "mean": self.sum / self.count,
            "min": self.min_val,
            "max": self.max_val,
        }


def audit_top_class(dataset_root: Path, top_class_dir: Path):
    image_count = 0
    valid_count = 0
    corrupt_count = 0
    corrupt_examples = []
    sample_images = []

    width_stats = RunningStats()
    height_stats = RunningStats()
    brightness_stats = RunningStats()

    scanned_subfolders = 0
    scanned_subfolders_with_images = 0
    direct_subfolder_image_counts = {}

    for current_root, _, files in os.walk(top_class_dir):
        scanned_subfolders += 1
        current_path = Path(current_root)
        rel_path = current_path.relative_to(dataset_root).as_posix()

        image_files = [f for f in files if Path(f).suffix.lower() in IMG_EXTENSIONS]
        direct_subfolder_image_counts[rel_path] = len(image_files)
        if image_files:
            scanned_subfolders_with_images += 1

        for filename in image_files:
            image_count += 1
            full_path = current_path / filename
            try:
                with Image.open(full_path) as img:
                    img.verify()
                with Image.open(full_path) as img:
                    rgb = img.convert("RGB")
                    width, height = rgb.size
                    width_stats.add(width)
                    height_stats.add(height)
                    gray = rgb.convert("L")
                    brightness_stats.add(sum(gray.getdata()) / float(width * height))
                    valid_count += 1
                    if len(sample_images) < 8:
                        sample_images.append(full_path.relative_to(dataset_root).as_posix())
            except (UnidentifiedImageError, OSError, ValueError, RuntimeError):
                corrupt_count += 1
                if len(corrupt_examples) < 20:
                    corrupt_examples.append(full_path.relative_to(dataset_root).as_posix())

    target_class, mapping_reason = infer_target_class(top_class_dir.name)

    return {
        "top_class": top_class_dir.name,
        "mapped_target_class": target_class,
        "mapping_reason": mapping_reason,
        "images_total": image_count,
        "images_valid": valid_count,
        "images_corrupt": corrupt_count,
        "scanned_subfolders_total": scanned_subfolders,
        "scanned_subfolders_with_images": scanned_subfolders_with_images,
        "resolution_width": width_stats.as_dict(),
        "resolution_height": height_stats.as_dict(),
        "brightness": brightness_stats.as_dict(),
        "sample_images": sample_images,
        "corrupt_examples": corrupt_examples,
        "direct_subfolder_image_counts": direct_subfolder_image_counts,
    }


def describe_lighting(mean_brightness: float) -> str:
    if mean_brightness < 70:
        return "mostly dark/underexposed"
    if mean_brightness < 120:
        return "moderately lit"
    if mean_brightness < 180:
        return "generally bright"
    return "very bright/high-key"


def get_semantic_class_depth(dataset_root: Path) -> int:
    top_level_dirs = sorted([p for p in dataset_root.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
    if len(top_level_dirs) != 1:
        return 1

    container = top_level_dirs[0]
    child_dirs = [p for p in container.iterdir() if p.is_dir()]
    if len(child_dirs) >= 2:
        return 2

    return 1


def audit_semantic_classes(dataset_root: Path, class_depth: int):
    rows = {}

    for image_path in dataset_root.rglob("*"):
        if not image_path.is_file() or image_path.suffix.lower() not in IMG_EXTENSIONS:
            continue

        rel_parts = image_path.relative_to(dataset_root).parts
        if not rel_parts:
            continue

        class_index = min(max(0, int(class_depth) - 1), len(rel_parts) - 1)
        semantic_class_name = rel_parts[class_index]

        if semantic_class_name not in rows:
            mapped_target, mapping_reason = infer_target_class(semantic_class_name)
            rows[semantic_class_name] = {
                "semantic_class": semantic_class_name,
                "mapped_target_class": mapped_target,
                "mapping_reason": mapping_reason,
                "images_total": 0,
                "images_valid": 0,
                "images_corrupt": 0,
                "resolution_width": RunningStats(),
                "resolution_height": RunningStats(),
                "brightness": RunningStats(),
                "sample_images": [],
                "corrupt_examples": [],
            }

        row = rows[semantic_class_name]
        row["images_total"] += 1

        try:
            with Image.open(image_path) as img:
                img.verify()
            with Image.open(image_path) as img:
                rgb = img.convert("RGB")
                width, height = rgb.size
                row["resolution_width"].add(width)
                row["resolution_height"].add(height)
                gray = rgb.convert("L")
                row["brightness"].add(sum(gray.getdata()) / float(width * height))
                row["images_valid"] += 1
                if len(row["sample_images"]) < 8:
                    row["sample_images"].append(image_path.relative_to(dataset_root).as_posix())
        except (UnidentifiedImageError, OSError, ValueError, RuntimeError):
            row["images_corrupt"] += 1
            if len(row["corrupt_examples"]) < 20:
                row["corrupt_examples"].append(image_path.relative_to(dataset_root).as_posix())

    out = []
    for name in sorted(rows.keys(), key=lambda x: x.lower()):
        row = rows[name]
        out.append({
            **row,
            "resolution_width": row["resolution_width"].as_dict(),
            "resolution_height": row["resolution_height"].as_dict(),
            "brightness": row["brightness"].as_dict(),
        })

    return out


def dataset_summary(audit_rows, semantic_rows, capture_hint):
    covered_targets = sorted(
        {
            row["mapped_target_class"]
            for row in semantic_rows
            if row["mapped_target_class"] in MATERIAL_CLASSES and row["images_valid"] > 0
        }
    )

    unmapped_classes = sorted(
        {
            row["semantic_class"]
            for row in semantic_rows
            if row["mapped_target_class"] is None and row["images_total"] > 0
        }
    )

    total_images = sum(row["images_total"] for row in audit_rows)
    total_valid = sum(row["images_valid"] for row in audit_rows)
    total_corrupt = sum(row["images_corrupt"] for row in audit_rows)

    width_weighted_sum = sum(
        row["resolution_width"]["mean"] * row["images_valid"]
        for row in audit_rows
        if row["images_valid"] > 0
    )
    height_weighted_sum = sum(
        row["resolution_height"]["mean"] * row["images_valid"]
        for row in audit_rows
        if row["images_valid"] > 0
    )
    brightness_weighted_sum = sum(
        row["brightness"]["mean"] * row["images_valid"]
        for row in audit_rows
        if row["images_valid"] > 0
    )

    avg_width = width_weighted_sum / total_valid if total_valid else 0.0
    avg_height = height_weighted_sum / total_valid if total_valid else 0.0
    avg_brightness = brightness_weighted_sum / total_valid if total_valid else 0.0

    return {
        "capture_type": capture_hint,
        "total_images": total_images,
        "total_valid_images": total_valid,
        "total_corrupt_images": total_corrupt,
        "covered_target_classes": covered_targets,
        "unmapped_top_classes_with_images": unmapped_classes,
        "average_resolution": {
            "width": avg_width,
            "height": avg_height,
        },
        "average_brightness": avg_brightness,
        "lighting_characterization": describe_lighting(avg_brightness),
    }


def write_markdown_report(output_path: Path, report_payload: dict):
    lines = []
    lines.append("# New Dataset Audit")
    lines.append("")

    for dataset in report_payload["datasets"]:
        lines.append(f"## {dataset['name']}")
        lines.append(f"- Root: {dataset['root']}")
        lines.append(f"- License: {dataset['license']}")
        lines.append(f"- Capture Type Hint: {dataset['summary']['capture_type']}")
        lines.append(f"- Semantic Class Folder Depth: {dataset['semantic_class_depth']}")
        lines.append(f"- Total Images: {dataset['summary']['total_images']}")
        lines.append(f"- Valid Images: {dataset['summary']['total_valid_images']}")
        lines.append(f"- Corrupt Images: {dataset['summary']['total_corrupt_images']}")
        lines.append(
            f"- Covered Target Classes: {', '.join(dataset['summary']['covered_target_classes']) if dataset['summary']['covered_target_classes'] else 'None'}"
        )
        lines.append(
            f"- Unmapped Classes With Images: {', '.join(dataset['summary']['unmapped_top_classes_with_images']) if dataset['summary']['unmapped_top_classes_with_images'] else 'None'}"
        )
        avg_res = dataset["summary"]["average_resolution"]
        lines.append(
            f"- Average Resolution: {avg_res['width']:.1f} x {avg_res['height']:.1f}"
        )
        lines.append(
            f"- Average Brightness: {dataset['summary']['average_brightness']:.2f} ({dataset['summary']['lighting_characterization']})"
        )
        lines.append("")
        lines.append("### Per Top-Level Class")
        lines.append("| Top Class | Mapped Target | Images | Valid | Corrupt | Avg WxH | Avg Brightness |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for row in dataset["per_top_class"]:
            w = row["resolution_width"]["mean"] if row["resolution_width"]["count"] else 0.0
            h = row["resolution_height"]["mean"] if row["resolution_height"]["count"] else 0.0
            b = row["brightness"]["mean"] if row["brightness"]["count"] else 0.0
            mapped = row["mapped_target_class"] if row["mapped_target_class"] else "UNMAPPED"
            lines.append(
                f"| {row['top_class']} | {mapped} | {row['images_total']} | {row['images_valid']} | {row['images_corrupt']} | {w:.1f} x {h:.1f} | {b:.2f} |"
            )
        lines.append("")

        lines.append("### Per Semantic Class")
        lines.append("| Semantic Class | Mapped Target | Images | Valid | Corrupt | Avg WxH | Avg Brightness |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for row in dataset["per_semantic_class"]:
            w = row["resolution_width"]["mean"] if row["resolution_width"]["count"] else 0.0
            h = row["resolution_height"]["mean"] if row["resolution_height"]["count"] else 0.0
            b = row["brightness"]["mean"] if row["brightness"]["count"] else 0.0
            mapped = row["mapped_target_class"] if row["mapped_target_class"] else "UNMAPPED"
            lines.append(
                f"| {row['semantic_class']} | {mapped} | {row['images_total']} | {row['images_valid']} | {row['images_corrupt']} | {w:.1f} x {h:.1f} | {b:.2f} |"
            )
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    results = {"datasets": []}

    for ds in DATASETS:
        root = ds["root"]
        if not root.exists() or not root.is_dir():
            results["datasets"].append(
                {
                    "name": ds["name"],
                    "root": root.as_posix(),
                    "license": ds["license"],
                    "error": "Dataset root not found",
                    "summary": {},
                    "per_top_class": [],
                }
            )
            continue

        top_level_dirs = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
        per_top_class = [audit_top_class(root, class_dir) for class_dir in top_level_dirs]
        semantic_depth = get_semantic_class_depth(root)
        per_semantic_class = audit_semantic_classes(root, semantic_depth)
        summary = dataset_summary(per_top_class, per_semantic_class, ds["capture_hint"])

        results["datasets"].append(
            {
                "name": ds["name"],
                "root": root.as_posix(),
                "license": ds["license"],
                "semantic_class_depth": semantic_depth,
                "summary": summary,
                "per_top_class": per_top_class,
                "per_semantic_class": per_semantic_class,
            }
        )

    output_dir = Path("backend/fabric_classifier/training")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "new_dataset_audit.json"
    md_path = output_dir / "new_dataset_audit.md"

    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_markdown_report(md_path, results)

    print(json.dumps({"json": json_path.as_posix(), "markdown": md_path.as_posix()}, ensure_ascii=True))


if __name__ == "__main__":
    main()
