import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from multiprocessing import Pool, freeze_support
from pathlib import Path

from PIL import Image, ImageFile
from tqdm import tqdm

from .resource_manager import get_resource_manager


ImageFile.LOAD_TRUNCATED_IMAGES = True

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif", ".tiff", ".tif"}
SPLIT_DIR_NAMES = {"train", "test", "val", "validation"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def discover_class_files(root: Path) -> dict[str, list[str]]:
    """
    Discover class folders under dataset_type/split/class_name and collect image paths.
    Class key format: dataset_type/class_name (for example: fabric/denim).
    """
    class_to_files: defaultdict[str, list[str]] = defaultdict(list)

    for dataset_type_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for split_name in SPLIT_DIR_NAMES:
            split_dir = dataset_type_dir / split_name
            if not split_dir.is_dir():
                continue

            for class_dir in sorted(p for p in split_dir.iterdir() if p.is_dir()):
                class_key = f"{dataset_type_dir.name}/{class_dir.name}"
                for image_path in class_dir.rglob("*"):
                    if is_image_file(image_path):
                        class_to_files[class_key].append(str(image_path))

    return {k: sorted(v) for k, v in sorted(class_to_files.items(), key=lambda item: item[0])}


def validate_image(path_str: str) -> tuple[bool, str, str]:
    try:
        with Image.open(path_str) as img:
            img.verify()
        return True, path_str, ""
    except Exception as exc:
        return False, path_str, str(exc)


def scan_class(class_key: str, file_paths: list[str], pool: Pool) -> dict:
    valid_count = 0
    corrupt_count = 0
    corrupt_samples: list[dict[str, str]] = []

    iterator = pool.imap_unordered(validate_image, file_paths, chunksize=32)
    for ok, path_str, error_msg in tqdm(
        iterator,
        total=len(file_paths),
        desc=f"Scanning {class_key}",
        unit="img",
        leave=False,
    ):
        if ok:
            valid_count += 1
        else:
            corrupt_count += 1
            if len(corrupt_samples) < 10:
                corrupt_samples.append({"path": path_str, "error": error_msg})

    return {
        "total": len(file_paths),
        "valid": valid_count,
        "corrupt": corrupt_count,
        "corrupt_samples": corrupt_samples,
    }


def print_table(results: dict[str, dict]) -> None:
    rows = []
    total_valid = 0
    total_corrupt = 0
    total_images = 0

    for class_key in sorted(results.keys()):
        stats = results[class_key]
        valid = int(stats.get("valid", 0))
        corrupt = int(stats.get("corrupt", 0))
        total = int(stats.get("total", valid + corrupt))
        rows.append((class_key, valid, corrupt, total))
        total_valid += valid
        total_corrupt += corrupt
        total_images += total

    header = ("Class", "Valid", "Corrupt", "Total")
    width_class = max(len(header[0]), *(len(r[0]) for r in rows)) if rows else len(header[0])
    width_valid = max(len(header[1]), *(len(str(r[1])) for r in rows)) if rows else len(header[1])
    width_corrupt = max(len(header[2]), *(len(str(r[2])) for r in rows)) if rows else len(header[2])
    width_total = max(len(header[3]), *(len(str(r[3])) for r in rows)) if rows else len(header[3])

    separator = (
        "+"
        + "-" * (width_class + 2)
        + "+"
        + "-" * (width_valid + 2)
        + "+"
        + "-" * (width_corrupt + 2)
        + "+"
        + "-" * (width_total + 2)
        + "+"
    )

    print("\nDataset Integrity Summary")
    print(separator)
    print(
        f"| {header[0]:<{width_class}} | {header[1]:>{width_valid}} | "
        f"{header[2]:>{width_corrupt}} | {header[3]:>{width_total}} |"
    )
    print(separator)
    for class_key, valid, corrupt, total in rows:
        print(
            f"| {class_key:<{width_class}} | {valid:>{width_valid}} | "
            f"{corrupt:>{width_corrupt}} | {total:>{width_total}} |"
        )
    print(separator)
    print(
        f"| {'ALL_CLASSES':<{width_class}} | {total_valid:>{width_valid}} | "
        f"{total_corrupt:>{width_corrupt}} | {total_images:>{width_total}} |"
    )
    print(separator)


def build_arg_parser(default_root: Path, default_checkpoint: Path, default_report: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan TextileNet images in parallel and count valid vs corrupted files per class."
    )
    parser.add_argument("--root", type=Path, default=default_root, help="Path to TextileNet-main root")
    parser.add_argument("--workers", type=int, default=4, help="Number of worker processes")
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=default_checkpoint,
        help="JSON checkpoint file (saved after each completed class)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=default_report,
        help="Final JSON report output path",
    )
    parser.add_argument(
        "--force-rescan",
        action="store_true",
        help="Ignore checkpoint results and rescan all classes",
    )
    return parser


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    default_root = repo_root / "DATASETS" / "TextileNet-main"
    default_checkpoint = Path(__file__).resolve().parent / "scan_dataset_checkpoint.json"
    default_report = Path(__file__).resolve().parent / "scan_dataset_report.json"

    parser = build_arg_parser(default_root, default_checkpoint, default_report)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Dataset root not found: {root}")

    class_files = discover_class_files(root)
    if not class_files:
        raise RuntimeError(f"No class image folders found under: {root}")

    checkpoint_data = {
        "root": str(root),
        "workers": int(args.workers),
        "started_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "results": {},
    }

    if args.checkpoint.exists() and not args.force_rescan:
        try:
            existing = json.loads(args.checkpoint.read_text(encoding="utf-8"))
            if existing.get("root") == str(root):
                checkpoint_data.update(existing)
                checkpoint_data["workers"] = int(args.workers)
                print(f"Resuming from checkpoint: {args.checkpoint}")
            else:
                print("Checkpoint root does not match current root. Starting fresh scan.")
        except Exception as exc:
            print(f"Warning: Failed to load checkpoint ({exc}). Starting fresh scan.")

    results: dict[str, dict] = checkpoint_data.get("results", {})
    all_class_keys = sorted(class_files.keys())
    pending_classes = [c for c in all_class_keys if c not in results] if not args.force_rescan else all_class_keys

    if args.force_rescan:
        results = {}
        checkpoint_data["results"] = results

    print(f"Discovered {len(all_class_keys)} classes.")
    print(f"Pending scan count: {len(pending_classes)}")

    manager = get_resource_manager(auto_start=True)

    if pending_classes:
        last_scan_workers = None
        max_workers = max(1, int(args.workers))
        for class_key in tqdm(pending_classes, desc="Classes", unit="class"):
            manager.wait_until_ram_below_limit(limit_percent=75.0, poll_s=1.0)
            snapshot = manager.get_snapshot()
            scan_workers = max(1, min(max_workers, int(snapshot.dataloader_workers or 1), 6))
            if scan_workers != last_scan_workers:
                print(f"Resource manager adjusted scan workers to: {scan_workers}")
                last_scan_workers = scan_workers

            with Pool(processes=scan_workers) as pool:
                stats = scan_class(class_key, class_files[class_key], pool)

            results[class_key] = stats
            checkpoint_data["results"] = results
            checkpoint_data["updated_at"] = utc_now_iso()
            checkpoint_data["last_completed_class"] = class_key
            save_json_atomic(args.checkpoint, checkpoint_data)

    checkpoint_data["updated_at"] = utc_now_iso()
    checkpoint_data["completed"] = True
    checkpoint_data["class_count"] = len(all_class_keys)
    save_json_atomic(args.checkpoint, checkpoint_data)

    report_payload = {
        "root": str(root),
        "generated_at": utc_now_iso(),
        "workers": int(args.workers),
        "class_count": len(all_class_keys),
        "results": {k: results[k] for k in sorted(results.keys())},
    }
    save_json_atomic(args.report, report_payload)

    print_table(results)
    print(f"\nCheckpoint saved to: {args.checkpoint}")
    print(f"Report saved to: {args.report}")


if __name__ == "__main__":
    freeze_support()
    main()
