import os
from PIL import Image
from tqdm import tqdm
import multiprocessing
import argparse

from .resource_manager import get_resource_manager

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tif', '.tiff')

def get_image_files(root_dir):
    """Recursively finds all image files in a directory."""
    image_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(IMAGE_EXTENSIONS):
                image_files.append(os.path.join(dirpath, filename))
    return image_files

def verify_images_worker(image_files_chunk, worker_id, total_workers):
    """
    Worker process to verify a chunk of image files.
    """
    deleted_count = 0
    # Each worker gets its own progress bar, positioned one below the other
    progress_bar = tqdm(image_files_chunk, desc=f"Worker {worker_id+1}/{total_workers}", position=worker_id)

    for file_path in progress_bar:
        try:
            with Image.open(file_path) as img:
                img.verify()  # Verifies image header and structure
        except Exception as e:
            # Using progress_bar.write to avoid interfering with the progress bar display
            progress_bar.write(f"Corrupted image: {file_path}. Error: {e}. Deleting file.")
            try:
                os.remove(file_path)
                deleted_count += 1
            except OSError as oe:
                progress_bar.write(f"Error deleting file {file_path}: {oe}")

    if deleted_count > 0:
        print(f"Worker {worker_id+1} finished. Deleted {deleted_count} corrupted images.")

def main():
    """
    Main function to orchestrate parallel image verification.
    """
    parser = argparse.ArgumentParser(description="Verify images in a directory in parallel.")
    parser.add_argument(
        "--data_dir",
        type=str,
        default="DATASETS/TextileNet-main/fabric",
        help="Directory to scan for images."
    )
    args = parser.parse_args()

    root_dir = args.data_dir
    manager = get_resource_manager(auto_start=True)
    manager.wait_until_ram_below_limit(limit_percent=75.0, poll_s=1.0)
    snapshot = manager.get_snapshot()
    num_workers = max(1, min(6, int(snapshot.dataloader_workers or 1)))
    print(
        f"Resource manager selected verify workers={num_workers} "
        f"(cpu={snapshot.cpu_percent:.1f}%, ram={snapshot.ram_percent:.1f}%)"
    )

    print("Collecting image files...")
    all_image_files = get_image_files(root_dir)
    total_files = len(all_image_files)
    print(f"Found {total_files} images to verify.")

    if total_files == 0:
        print("No images found. Exiting.")
        return

    # Split the list of files into chunks for each worker
    chunk_size = (total_files + num_workers - 1) // num_workers
    chunks = [all_image_files[i:i + chunk_size] for i in range(0, total_files, chunk_size)]

    processes = []
    print(f"Starting verification with {num_workers} workers...")

    # Create and start a process for each chunk
    for i, chunk in enumerate(chunks):
        p = multiprocessing.Process(target=verify_images_worker, args=(chunk, i, num_workers))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("\nAll workers finished. Image verification complete.")

if __name__ == "__main__":
    # This allows the script to be run from the command line.
    # The multiprocessing module requires this check.
    multiprocessing.freeze_support()
    main()
