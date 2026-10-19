import numpy as np
import cv2
from PIL import Image

def extract_patches(pil_image, n_patches=7, patch_size=160, input_size=224, rng=None):
    """
    Extracts n_patches texture patches from the garment interior.
    Returns a list of PIL Images, each resized to input_size x input_size.
    """
    if rng is None:
        rng = np.random.default_rng()

    # Cap very large images to avoid excessive memory usage on malformed files.
    max_side = 2048
    if max(pil_image.size) > max_side:
        scale = max_side / float(max(pil_image.size))
        new_size = (
            max(1, int(pil_image.size[0] * scale)),
            max(1, int(pil_image.size[1] * scale)),
        )
        pil_image = pil_image.resize(new_size, Image.Resampling.BILINEAR)

    # Ensure image is in RGBA format to access alpha channel
    img_rgba = pil_image.convert("RGBA")
    img_arr = np.array(img_rgba)

    # Fallback if decoded image shape is invalid.
    if img_arr.ndim != 3 or img_arr.shape[2] < 4:
        img_rgb = pil_image.convert("RGB").resize((input_size, input_size), Image.Resampling.BILINEAR)
        return [img_rgb] * n_patches

    # Build mask: non-transparent and not near-white background
    alpha = img_arr[:, :, 3]
    rgb = img_arr[:, :, :3]
    is_opaque = alpha > 200
    is_not_white = ~((rgb[:,:,0] > 230) & (rgb[:,:,1] > 230) & (rgb[:,:,2] > 230))
    mask = is_opaque & is_not_white

    # Erode mask to stay away from edges
    kernel = np.ones((15, 15), np.uint8)
    safe_mask = np.asarray(cv2.erode(mask.astype(np.uint8), kernel, iterations=1), dtype=np.uint8)

    ys, xs = np.where(safe_mask.astype(np.uint8) > 0)
    
    # Fallback to center crop if the mask is too small
    if len(ys) < (patch_size * patch_size * 0.1):
        img_rgb = pil_image.convert("RGB")
        # A simple center crop resize
        width, height = img_rgb.size
        new_size = min(width, height)
        left = (width - new_size)/2
        top = (height - new_size)/2
        right = (width + new_size)/2
        bottom = (height + new_size)/2
        img_rgb = img_rgb.crop((left, top, right, bottom))
        crop = img_rgb.resize((input_size, input_size), Image.Resampling.BILINEAR)
        return [crop] * n_patches

    patches = []
    max_attempts = n_patches * 20  # Increased attempts
    attempts = 0
    img_rgb = pil_image.convert("RGB") # Convert once

    while len(patches) < n_patches and attempts < max_attempts:
        attempts += 1
        idx = int(rng.integers(0, len(ys)))
        cy, cx = ys[idx], xs[idx]
        
        # Define crop box
        x1 = cx - patch_size // 2
        y1 = cy - patch_size // 2
        x2 = x1 + patch_size
        y2 = y1 + patch_size

        h, w, _ = img_arr.shape
        if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
            continue

        # Check if the patch is mostly valid pixels
        patch_mask = safe_mask[y1:y2, x1:x2]
        if patch_mask.mean() < 0.5:
            continue

        patch = img_rgb.crop((x1, y1, x2, y2))
        patch = patch.resize((input_size, input_size), Image.Resampling.BILINEAR)
        patches.append(patch)

    # If no patches found, return a resized version of the whole image, duplicated
    if not patches:
        resized_img = img_rgb.resize((input_size, input_size), Image.Resampling.BILINEAR)
        return [resized_img] * n_patches
        
    # If not enough patches were found, duplicate existing ones
    while len(patches) < n_patches:
        patches.extend(patches[:n_patches - len(patches)])

    return patches[:n_patches]
