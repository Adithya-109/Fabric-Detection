import argparse
import json
import os
import random
import time
import uuid
from collections import defaultdict, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import requests
from PIL import Image
from tqdm import tqdm

from .resource_manager import get_resource_manager


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif", ".tif", ".tiff"}
MAX_AUTO_RETRIES = 5
MAX_CONSECUTIVE_FAILURES_BEFORE_SUCCESS_ABORT = 30


def safe_unlink(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except PermissionError:
        # Windows scanners can briefly lock newly created temp files.
        time.sleep(0.05)
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass


def replace_with_retry(src: Path, dst: Path, max_attempts: int = 6, delay_s: float = 0.05) -> bool:
    for attempt in range(max_attempts):
        try:
            os.replace(src, dst)
            return True
        except PermissionError:
            if attempt == max_attempts - 1:
                return False
            time.sleep(delay_s * (attempt + 1))
    return False


def parse_expected_content_length(headers: requests.structures.CaseInsensitiveDict) -> int | None:
    raw = headers.get("Content-Length")
    if not raw:
        return None
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


def verify_download_integrity(path: Path, expected_size: int | None) -> bool:
    try:
        if not path.exists():
            return False

        size = path.stat().st_size
        if size <= 0:
            return False

        if expected_size is not None and size != expected_size:
            return False

        if path.suffix.lower() in IMAGE_EXTENSIONS:
            with Image.open(path) as img:
                img.verify()

        return True
    except Exception:
        return False


def is_dns_error(exc: Exception) -> bool:
    message = str(exc).lower()
    dns_markers = [
        "name or service not known",
        "temporary failure in name resolution",
        "getaddrinfo failed",
        "nodename nor servname provided",
        "no such host is known",
        "failed to resolve",
    ]
    return any(marker in message for marker in dns_markers)


def retry_delay_seconds(exc: Exception, attempt: int) -> float:
    # Explicit DNS wait requested by the user.
    if is_dns_error(exc):
        return 10.0
    # Exponential backoff for transient network interruptions.
    return float(min(2 ** max(0, attempt - 1), 30))


def download_worker(task: tuple[str, str, int, int]) -> tuple[str, str]:
    destination, url, timeout_s, retries = task
    dest_path = Path(destination)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    effective_retries = min(max(int(retries), 0), MAX_AUTO_RETRIES)

    if dest_path.exists():
        if verify_download_integrity(dest_path, expected_size=None):
            return destination, "skipped"
        safe_unlink(dest_path)

    for attempt in range(1, effective_retries + 2):
        temp_path = dest_path.with_name(f"{dest_path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
        try:
            with requests.get(url, timeout=timeout_s, stream=True) as response:
                response.raise_for_status()
                expected_size = parse_expected_content_length(response.headers)

                with open(temp_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=64 * 1024):
                        if chunk:
                            f.write(chunk)

            if not verify_download_integrity(temp_path, expected_size):
                raise ValueError(f"Integrity check failed for partial/corrupt download: {url}")

            if dest_path.exists():
                if verify_download_integrity(dest_path, expected_size=None):
                    safe_unlink(temp_path)
                    return destination, "skipped"
                # Existing file is present but invalid/corrupt; replace it.
                safe_unlink(dest_path)

            replaced = replace_with_retry(temp_path, dest_path)
            if not replaced:
                if dest_path.exists():
                    safe_unlink(temp_path)
                    return destination, "skipped"
                raise PermissionError(f"Unable to atomically replace {dest_path} due to file lock")

            if not verify_download_integrity(dest_path, expected_size):
                safe_unlink(dest_path)
                raise ValueError(f"Final integrity check failed after move: {url}")

            return destination, "downloaded"
        except Exception as exc:
            if temp_path.exists():
                safe_unlink(temp_path)
            if attempt <= effective_retries:
                time.sleep(retry_delay_seconds(exc, attempt))

    return destination, "failed"


def load_partition_items(json_path: Path, split: str) -> list[tuple[str, str, str, str]]:
    items = json.loads(json_path.read_text(encoding="utf-8"))
    return [(split, fname, cls, url) for fname, cls, url in items]


def run_dynamic_downloads(
    tasks: list[tuple[str, str, int, int]],
    initial_workers: int,
    max_workers: int,
) -> tuple[int, int, int]:
    manager = get_resource_manager(auto_start=True)

    downloaded = 0
    skipped = 0
    failed = 0
    consecutive_failures_before_success = 0
    early_stop_triggered = False

    max_workers = manager.clamp_download_workers(int(max_workers))
    target_workers = manager.clamp_download_workers(min(int(initial_workers), max_workers))

    pending = deque(tasks)
    active: set = set()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        pbar = tqdm(total=len(tasks), desc=f"Downloading (workers={target_workers})")
        while pending or active:
            snapshot = manager.get_snapshot()
            if snapshot.download_paused:
                pbar.set_description("Downloading (paused by resource manager)")
                if active:
                    done, still_running = wait(active, timeout=0.5, return_when=FIRST_COMPLETED)
                    active = set(still_running)
                    for future in done:
                        try:
                            _, status = future.result()
                        except Exception:
                            status = "failed"

                        if status == "downloaded":
                            downloaded += 1
                            consecutive_failures_before_success = 0
                        elif status == "skipped":
                            skipped += 1
                        else:
                            failed += 1
                            if downloaded == 0:
                                consecutive_failures_before_success += 1

                        if (
                            not early_stop_triggered
                            and downloaded == 0
                            and consecutive_failures_before_success >= MAX_CONSECUTIVE_FAILURES_BEFORE_SUCCESS_ABORT
                            and pending
                        ):
                            pending.clear()
                            early_stop_triggered = True
                            print(
                                "Early stop: repeated download failures before first success; "
                                "aborting remaining queued tasks."
                            )

                        pbar.update(1)
                else:
                    manager.wait_until_download_allowed(poll_s=1.0)
                continue

            target_workers = max(1, min(int(snapshot.download_workers or 1), max_workers))
            pbar.set_description(f"Downloading (workers={target_workers})")

            while pending and len(active) < target_workers:
                active.add(executor.submit(download_worker, pending.popleft()))

            if not active:
                time.sleep(0.1)
                continue

            done, still_running = wait(active, timeout=0.5, return_when=FIRST_COMPLETED)
            active = set(still_running)
            for future in done:
                try:
                    _, status = future.result()
                except Exception:
                    status = "failed"

                if status == "downloaded":
                    downloaded += 1
                    consecutive_failures_before_success = 0
                elif status == "skipped":
                    skipped += 1
                else:
                    failed += 1
                    if downloaded == 0:
                        consecutive_failures_before_success += 1

                if (
                    not early_stop_triggered
                    and downloaded == 0
                    and consecutive_failures_before_success >= MAX_CONSECUTIVE_FAILURES_BEFORE_SUCCESS_ABORT
                    and pending
                ):
                    pending.clear()
                    early_stop_triggered = True
                    print(
                        "Early stop: repeated download failures before first success; "
                        "aborting remaining queued tasks."
                    )

                pbar.update(1)

        pbar.close()

    return downloaded, skipped, failed


def main() -> None:
    parser = argparse.ArgumentParser(description="Download capped subset of TextileNet classes.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("DATASETS/TextileNet-main"),
        help="TextileNet root containing json/ and fibre|fabric/",
    )
    parser.add_argument(
        "--subset",
        choices=["fibre", "fabric"],
        default="fibre",
        help="Which TextileNet subset to download into",
    )
    parser.add_argument(
        "--classes",
        nargs="+",
        default=["polyester", "flax_linen", "suede"],
        help="Fibre class names to download",
    )
    parser.add_argument(
        "--max-per-class",
        type=int,
        default=1200,
        help="Maximum number of URLs to use per class (across train+test)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Initial download workers; resource manager will adapt this dynamically",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Upper bound for dynamic download workers",
    )
    parser.add_argument("--timeout", type=int, default=15, help="Per-request timeout in seconds")
    parser.add_argument(
        "--retries",
        type=int,
        default=5,
        help="Retry attempts per URL after initial failure (capped at 5)",
    )
    parser.add_argument("--seed", type=int, default=42, help="Sampling random seed")
    args = parser.parse_args()

    random.seed(args.seed)

    root = args.root.resolve()
    json_dir = root / "json"
    subset_root = root / args.subset

    train_items = load_partition_items(json_dir / f"{args.subset}_train.json", "train")
    test_items = load_partition_items(json_dir / f"{args.subset}_test.json", "test")

    target_classes = {c.strip().lower() for c in args.classes if c.strip()}
    by_class: defaultdict[str, list[tuple[str, str, str, str]]] = defaultdict(list)

    for item in train_items + test_items:
        split, fname, cls, url = item
        cls_norm = cls.lower()
        if cls_norm in target_classes:
            by_class[cls_norm].append((split, fname, cls_norm, url))

    tasks: list[tuple[str, str, int, int]] = []
    selected_counts: dict[str, int] = {}
    queued_counts: dict[str, int] = {}
    already_valid_counts: dict[str, int] = {}
    seen_destinations: set[str] = set()
    duplicate_destinations = 0
    for cls in sorted(target_classes):
        items = by_class.get(cls, [])
        random.shuffle(items)
        selected = items[: args.max_per_class]
        selected_counts[cls] = len(selected)
        queued_for_class = 0
        already_valid_for_class = 0
        for split, fname, cls_name, url in selected:
            destination = subset_root / split / cls_name / fname
            destination_str = str(destination)
            if destination_str in seen_destinations:
                duplicate_destinations += 1
                continue
            seen_destinations.add(destination_str)

            # Skip URLs that already have a valid local destination file.
            if destination.exists() and verify_download_integrity(destination, expected_size=None):
                already_valid_for_class += 1
                continue

            tasks.append((destination_str, url, int(args.timeout), int(args.retries)))
            queued_for_class += 1

        queued_counts[cls] = queued_for_class
        already_valid_counts[cls] = already_valid_for_class

    print("Selected fibre download counts:")
    for cls, count in selected_counts.items():
        print(f"  {cls}: {count}")
    print("Already-valid destinations skipped:")
    for cls, count in already_valid_counts.items():
        print(f"  {cls}: {count}")
    print("Queued download tasks:")
    for cls, count in queued_counts.items():
        print(f"  {cls}: {count}")
    if duplicate_destinations:
        print(f"Skipped duplicate destination filenames: {duplicate_destinations}")
    print(f"Total selected URLs: {len(tasks)}")

    if not tasks:
        print("No download tasks found for requested classes.")
        return

    downloaded, skipped, failed = run_dynamic_downloads(
        tasks=tasks,
        initial_workers=int(args.workers),
        max_workers=int(args.max_workers),
    )

    print("\nDownload summary:")
    print(f"  downloaded: {downloaded}")
    print(f"  skipped: {skipped}")
    print(f"  failed: {failed}")


if __name__ == "__main__":
    main()
