"""Tests for patch extraction (training/dataset.py).

Covers the existing contract (exactly n square patches of input_size, deterministic
for a seeded RNG, safe fallbacks) and the new options: pluggable garment mask and
scale-relative patch size (plan §3.4, §3.5).
"""
import unittest

import numpy as np
from PIL import Image

from tests import ROOT  # noqa: F401
from tests.helpers import checkerboard, count_transitions, noise_image, solid_image
from backend.fabric_classifier.training.dataset import (
    compute_patch_size,
    extract_patches,
    foreground_mask,
)


class TestForegroundMask(unittest.TestCase):
    def test_white_and_transparent_pixels_are_background(self):
        arr = np.zeros((2, 3, 4), dtype=np.uint8)
        arr[..., 3] = 255
        arr[0, 0, :3] = 250  # near white
        arr[0, 1, 3] = 0  # transparent
        arr[0, 2, :3] = (120, 40, 40)  # cloth
        mask = foreground_mask(arr)
        self.assertEqual(mask.dtype, bool)
        self.assertEqual(mask.shape, (2, 3))
        self.assertFalse(mask[0, 0])
        self.assertFalse(mask[0, 1])
        self.assertTrue(mask[0, 2])

    def test_thresholds_are_configurable(self):
        arr = np.full((1, 1, 4), 240, dtype=np.uint8)
        arr[..., 3] = 255
        self.assertFalse(foreground_mask(arr)[0, 0])
        self.assertTrue(foreground_mask(arr, white_threshold=245)[0, 0])

    def test_rejects_non_rgba(self):
        with self.assertRaises(ValueError):
            foreground_mask(np.zeros((4, 4, 3), dtype=np.uint8))


class TestComputePatchSize(unittest.TestCase):
    def test_fraction_of_short_side(self):
        self.assertEqual(compute_patch_size(1000, 800, fraction=0.25), 200)

    def test_clamped_to_min_and_max(self):
        self.assertEqual(compute_patch_size(100, 100, fraction=0.1, min_size=64), 64)
        self.assertEqual(compute_patch_size(8000, 8000, fraction=0.5, max_size=512), 512)

    def test_never_larger_than_the_image(self):
        self.assertEqual(compute_patch_size(50, 40, fraction=0.5, min_size=64), 40)

    def test_invalid_fraction_raises(self):
        for f in (0.0, -0.2, 1.5):
            with self.assertRaises(ValueError):
                compute_patch_size(100, 100, fraction=f)


class TestExtractPatchesContract(unittest.TestCase):
    def test_returns_n_patches_of_input_size(self):
        patches = extract_patches(noise_image((500, 400)), n_patches=7, rng=np.random.default_rng(0))
        self.assertEqual(len(patches), 7)
        for p in patches:
            self.assertIsInstance(p, Image.Image)
            self.assertEqual(p.size, (224, 224))
            self.assertEqual(p.mode, "RGB")

    def test_seeded_rng_is_deterministic(self):
        img = noise_image((500, 400), seed=5)
        a = extract_patches(img, rng=np.random.default_rng(42))
        b = extract_patches(img, rng=np.random.default_rng(42))
        for x, y in zip(a, b):
            np.testing.assert_array_equal(np.asarray(x), np.asarray(y))

    def test_all_white_image_falls_back_to_center_crop(self):
        patches = extract_patches(solid_image((255, 255, 255), (300, 200)), n_patches=5)
        self.assertEqual(len(patches), 5)
        self.assertTrue(all(p.size == (224, 224) for p in patches))

    def test_tiny_image_still_returns_patches(self):
        patches = extract_patches(noise_image((40, 30)), n_patches=3, rng=np.random.default_rng(0))
        self.assertEqual(len(patches), 3)

    def test_palette_and_grayscale_inputs(self):
        for mode in ("L", "P", "RGBA"):
            img = noise_image((300, 300)).convert(mode)
            self.assertEqual(len(extract_patches(img, n_patches=2, rng=np.random.default_rng(0))), 2)

    def _garment_on_white(self):
        img = solid_image((255, 255, 255), (600, 600))
        img.paste(solid_image((150, 30, 30), (300, 300)), (150, 150))
        return img

    @staticmethod
    def _white_fraction(patch):
        arr = np.asarray(patch).reshape(-1, 3)
        return float((arr.min(axis=1) > 230).mean())

    def test_default_coverage_allows_at_most_half_background(self):
        # Documents legacy behaviour (kept so training data does not change silently).
        for p in extract_patches(self._garment_on_white(), n_patches=7, rng=np.random.default_rng(1)):
            self.assertLessEqual(self._white_fraction(p), 0.55)

    def test_high_min_coverage_keeps_patches_on_garment(self):
        patches = extract_patches(self._garment_on_white(), n_patches=7, min_coverage=0.95,
                                  rng=np.random.default_rng(1))
        self.assertEqual(len(patches), 7)
        for p in patches:
            self.assertLess(self._white_fraction(p), 0.05)

    def test_invalid_min_coverage_raises(self):
        for value in (-0.1, 1.1):
            with self.assertRaises(ValueError):
                extract_patches(noise_image(), min_coverage=value)


class TestExtractPatchesMask(unittest.TestCase):
    def test_external_mask_restricts_patch_location(self):
        arr = np.zeros((400, 800, 3), dtype=np.uint8)
        arr[:, :400] = (200, 20, 20)  # left half red ("garment")
        arr[:, 400:] = (20, 20, 200)  # right half blue ("background/person")
        mask = np.zeros((400, 800), dtype=bool)
        mask[:, :400] = True
        patches = extract_patches(Image.fromarray(arr), n_patches=7, mask=mask, min_coverage=1.0,
                                  rng=np.random.default_rng(0))
        for p in patches:
            mean = np.asarray(p).reshape(-1, 3).mean(axis=0)
            self.assertGreater(mean[0], 150)
            self.assertLess(mean[2], 60)

    def test_mask_shape_must_match_image(self):
        with self.assertRaises(ValueError):
            extract_patches(noise_image((300, 200)), mask=np.ones((10, 10), dtype=bool))


class TestExtractPatchesScale(unittest.TestCase):
    def _transitions(self, image, **kwargs):
        patches = extract_patches(image, n_patches=5, rng=np.random.default_rng(0), **kwargs)
        rows = [count_transitions(np.asarray(p.convert("L"))[112]) for p in patches]
        return float(np.median(rows))

    def test_patch_fraction_sees_same_texture_scale_at_any_resolution(self):
        # Same cloth photographed at two resolutions: cells scale with the image.
        low = checkerboard(400, cell=20)
        high = checkerboard(1600, cell=80)
        t_low = self._transitions(low, patch_fraction=0.25)
        t_high = self._transitions(high, patch_fraction=0.25)
        self.assertLessEqual(abs(t_low - t_high), 1)

    def test_fixed_patch_size_default_is_unchanged(self):
        # Backwards compatibility: default is still a fixed 160 px crop.
        low = checkerboard(400, cell=20)
        high = checkerboard(1600, cell=80)
        self.assertGreater(self._transitions(low) - self._transitions(high), 3)


if __name__ == "__main__":
    unittest.main()
