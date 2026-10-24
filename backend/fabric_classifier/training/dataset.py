import numpy as np
import cv2
from PIL import Image

MAX_SIDE = 2048
ERODE_KERNEL = 15


def foreground_mask(rgba: np.ndarray, white_threshold: int = 230, alpha_threshold: int = 200) -> np.ndarray:
    """Boolean mask of pixels that are opaque and not near-white.

    This heuristic suits product shots on white/transparent backgrounds. For
    general photos pass a garment-segmentation mask to ``extract_patches(mask=...)``.
    """
    rgba = np.asarray(rgba)
    if rgba.ndim != 3 or rgba.shape[2] != 4:
        raise ValueError(f"expected an RGBA array of shape (H, W, 4), got {rgba.shape}")
    rgb, alpha = rgba[:, :, :3], rgba[:, :, 3]
    is_opaque = alpha > alpha_threshold
    is_white = np.all(rgb > white_threshold, axis=2)
    return is_opaque & ~is_white


def compute_patch_size(width: int, height: int, fraction: float = 0.25,
                       min_size: int = 64, max_size: int = 512) -> int:
    """Patch side as a fraction of the region's short side, clamped to [min_size, max_size].

    Never exceeds the short side itself, so the patch always fits.
    """
    if not 0.0 < fraction <= 1.0:
        raise ValueError("fraction must be in (0, 1]")
    short = int(min(width, height))
    size = int(round(fraction * short))
    size = max(min_size, min(max_size, size))
    return max(1, min(size, short))


def _center_crop(img_rgb: Image.Image, input_size: int) -> Image.Image:
    width, height = img_rgb.size
    side = min(width, height)
    left, top = (width - side) / 2, (height - side) / 2
    return img_rgb.crop((left, top, left + side, top + side)).resize(
        (input_size, input_size), Image.Resampling.BILINEAR
    )


def extract_patches(pil_image, n_patches=7, patch_size=160, input_size=224, rng=None,
                    patch_fraction=None, mask=None, min_patch_size=64, max_patch_size=512,
                    min_coverage=0.5):
    """
    Extracts n_patches texture patches from the garment interior.
    Returns a list of PIL Images, each resized to input_size x input_size.

    Args:
        patch_size: fixed patch side in pixels (default behaviour, unchanged).
        patch_fraction: if given, the patch side is this fraction of the short side of
            the garment's bounding box instead, so texture scale is the same at any
            image resolution.
        mask: optional boolean (H, W) garment mask for the *input* image (e.g. from a
            segmentation model). Replaces the white-background heuristic.
        min_coverage: minimum fraction of a patch that must lie on the (eroded) garment
            mask. The legacy default 0.5 lets patches be half background; 0.9+ is
            recommended for general photos.
    """
    if not 0.0 <= min_coverage <= 1.0:
        raise ValueError("min_coverage must be in [0, 1]")
    if rng is None:
        rng = np.random.default_rng()

    if mask is not None:
        mask = np.asarray(mask).astype(bool)
        expected = (pil_image.size[1], pil_image.size[0])
        if mask.shape != expected:
            raise ValueError(f"mask shape {mask.shape} does not match image (H, W) {expected}")

    # Cap very large images to avoid excessive memory usage on malformed files.
    if max(pil_image.size) > MAX_SIDE:
        scale = MAX_SIDE / float(max(pil_image.size))
        new_size = (
            max(1, int(pil_image.size[0] * scale)),
            max(1, int(pil_image.size[1] * scale)),
        )
        pil_image = pil_image.resize(new_size, Image.Resampling.BILINEAR)
        if mask is not None:
            mask = np.asarray(
                Image.fromarray(mask.astype(np.uint8) * 255).resize(new_size, Image.Resampling.NEAREST)
            ) > 0

    img_rgba = pil_image.convert("RGBA")
    img_arr = np.array(img_rgba)
    img_rgb = pil_image.convert("RGB")

    # Fallback if decoded image shape is invalid.
    if img_arr.ndim != 3 or img_arr.shape[2] < 4:
        return [img_rgb.resize((input_size, input_size), Image.Resampling.BILINEAR)] * n_patches

    region = mask if mask is not None else foreground_mask(img_arr)

    # Erode mask to stay away from edges, seams and zippers.
    kernel = np.ones((ERODE_KERNEL, ERODE_KERNEL), np.uint8)
    safe_mask = np.asarray(cv2.erode(region.astype(np.uint8), kernel, iterations=1), dtype=np.uint8)
    ys, xs = np.where(safe_mask > 0)

    if patch_fraction is not None and len(ys) > 0:
        bbox_w = int(xs.max() - xs.min() + 1)
        bbox_h = int(ys.max() - ys.min() + 1)
        patch_size = compute_patch_size(bbox_w, bbox_h, patch_fraction, min_patch_size, max_patch_size)

    # Fallback to center crop if the mask is too small.
    if len(ys) < (patch_size * patch_size * 0.1):
        return [_center_crop(img_rgb, input_size)] * n_patches

    patches = []
    max_attempts = n_patches * 20
    attempts = 0
    h, w = img_arr.shape[:2]

    while len(patches) < n_patches and attempts < max_attempts:
        attempts += 1
        idx = int(rng.integers(0, len(ys)))
        cy, cx = ys[idx], xs[idx]

        x1 = cx - patch_size // 2
        y1 = cy - patch_size // 2
        x2 = x1 + patch_size
        y2 = y1 + patch_size
        if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
            continue

        # Require the patch to be mostly garment.
        if safe_mask[y1:y2, x1:x2].mean() < min_coverage:
            continue

        patch = img_rgb.crop((x1, y1, x2, y2))
        patches.append(patch.resize((input_size, input_size), Image.Resampling.BILINEAR))

    # If no patches found, return a resized version of the whole image, duplicated.
    if not patches:
        return [img_rgb.resize((input_size, input_size), Image.Resampling.BILINEAR)] * n_patches

    # If not enough patches were found, duplicate existing ones.
    while len(patches) < n_patches:
        patches.extend(patches[:n_patches - len(patches)])

    return patches[:n_patches]
