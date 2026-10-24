"""Shared helpers for the test suite."""
import importlib.util
import io

import numpy as np
from PIL import Image

HAS_TORCH = importlib.util.find_spec("torch") is not None and importlib.util.find_spec("torchvision") is not None
TORCH_SKIP_REASON = "PyTorch/torchvision not installed"


def solid_image(color=(180, 160, 140), size=(400, 600), mode="RGB"):
    if mode == "RGBA" and len(color) == 3:
        color = tuple(color) + (255,)
    return Image.new(mode, size, color)


def checkerboard(size, cell, colors=((20, 20, 20), (200, 200, 200))):
    """Square RGB checkerboard of side `size` px with `cell` px squares.

    Default colours avoid near-white so the whole board counts as foreground.
    """
    yy, xx = np.mgrid[0:size, 0:size]
    board = ((yy // cell + xx // cell) % 2).astype(np.uint8)
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    arr[board == 0] = colors[0]
    arr[board == 1] = colors[1]
    return Image.fromarray(arr, "RGB")


def noise_image(size=(320, 320), seed=0):
    rng = np.random.default_rng(seed)
    arr = rng.integers(0, 200, size=(size[1], size[0], 3), dtype=np.uint8)
    return Image.fromarray(arr, "RGB")


def smooth_image(size=(400, 400), seed=0, grid=6):
    """Random low-frequency image (like the large-scale structure of a real photo)."""
    rng = np.random.default_rng(seed)
    small = rng.integers(0, 255, size=(grid, grid, 3), dtype=np.uint8)
    return Image.fromarray(small, "RGB").resize(size, Image.Resampling.BICUBIC)


def image_bytes(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf


def count_transitions(row):
    """Number of colour changes along a 1-D intensity row (binarised at mid-grey)."""
    b = (np.asarray(row) > 127).astype(np.int8)
    return int(np.abs(np.diff(b)).sum())
