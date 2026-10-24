"""Tests for the patch-strategy diagnostic (tools/patch_diagnostic.py) and the
``return_boxes`` option of ``extract_patches`` it relies on."""
import unittest

import numpy as np
from PIL import Image

from tests import ROOT  # noqa: F401
from tests.helpers import noise_image, solid_image
from backend.fabric_classifier.training.dataset import extract_patches
from tools.patch_diagnostic import (
    CLOTHING_LABELS,
    cap_per_class,
    central_mask,
    draw_boxes,
    garment_mask,
    pairwise_auc,
    rank_metrics,
    resize_max_side,
)


class TestExtractPatchesBoxes(unittest.TestCase):
    def test_boxes_match_patches(self):
        img = noise_image((500, 400), seed=3)
        patches, boxes = extract_patches(img, n_patches=5, rng=np.random.default_rng(0), return_boxes=True)
        self.assertEqual(len(boxes), 5)
        for patch, (x1, y1, x2, y2) in zip(patches, boxes):
            self.assertTrue(0 <= x1 < x2 <= 500 and 0 <= y1 < y2 <= 400)
            expected = img.crop((x1, y1, x2, y2)).resize((224, 224), Image.Resampling.BILINEAR)
            np.testing.assert_array_equal(np.asarray(patch), np.asarray(expected))

    def test_default_return_is_unchanged(self):
        out = extract_patches(noise_image((300, 300)), n_patches=2, rng=np.random.default_rng(0))
        self.assertIsInstance(out, list)

    def test_boxes_are_in_original_coordinates_for_huge_images(self):
        img = noise_image((4096, 1024), seed=1)
        _, boxes = extract_patches(img, n_patches=3, rng=np.random.default_rng(0), return_boxes=True)
        for x1, y1, x2, y2 in boxes:
            self.assertLessEqual(x2, 4096)
            self.assertLessEqual(y2, 1024)
            self.assertAlmostEqual(x2 - x1, 320, delta=2)  # 160 px at half scale → 320 px original

    def test_fallback_box_is_centre_square(self):
        _, boxes = extract_patches(solid_image((255, 255, 255), (300, 200)), n_patches=2, return_boxes=True)
        self.assertEqual(boxes[0], (50, 0, 250, 200))


class TestMasks(unittest.TestCase):
    def test_central_mask_is_centred_rectangle(self):
        m = central_mask(100, 200, width_frac=0.5, height_frac=0.6)
        self.assertEqual(m.shape, (100, 200))
        ys, xs = np.where(m)
        self.assertEqual((xs.min(), xs.max() + 1), (50, 150))
        self.assertEqual((ys.min(), ys.max() + 1), (20, 80))

    def test_garment_mask_largest_clothing_class(self):
        labels = np.zeros((10, 10), dtype=np.int64)
        labels[:6, :] = 4  # upper clothes: 60 px
        labels[6:, :5] = 6  # pants: 20 px
        labels[6:, 5:] = 11  # face/skin: not clothing
        largest = garment_mask(labels, mode="largest")
        self.assertEqual(int(largest.sum()), 60)
        union = garment_mask(labels, mode="any")
        self.assertEqual(int(union.sum()), 80)

    def test_garment_mask_empty_when_no_clothing(self):
        self.assertFalse(garment_mask(np.full((5, 5), 11)).any())

    def test_clothing_labels_exclude_skin_hair_background(self):
        self.assertTrue({4, 5, 6, 7}.issubset(CLOTHING_LABELS))
        self.assertTrue({0, 2, 11, 14, 15}.isdisjoint(CLOTHING_LABELS))


class TestMetrics(unittest.TestCase):
    def test_rank_metrics(self):
        logits = np.array([[3.0, 2.0, 1.0], [1.0, 3.0, 2.0], [3.0, 2.0, 1.0]])
        labels = np.array([0, 2, 2])  # ranks: 1, 2, 3
        m = rank_metrics(logits, labels)
        self.assertEqual(m["median_true_rank"], 2.0)
        self.assertAlmostEqual(m["top1"], 1 / 3)
        self.assertAlmostEqual(m["top3"], 1.0)
        self.assertAlmostEqual(m["mean_reciprocal_rank"], (1 + 0.5 + 1 / 3) / 3)

    def test_pairwise_auc(self):
        logits = np.array([[2.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.0, 2.0], [5.0, 5.0]])
        labels = np.array([0, 0, 1, 1, 2])
        self.assertAlmostEqual(pairwise_auc(logits, labels, 0, 1), 1.0)
        self.assertIsNone(pairwise_auc(logits, labels, 0, 3))


class TestHelpers(unittest.TestCase):
    def test_cap_per_class_is_deterministic_and_capped(self):
        labels = np.array([0] * 50 + [1] * 3)
        idx = cap_per_class(labels, cap=10, seed=0)
        self.assertEqual(int((labels[idx] == 0).sum()), 10)
        self.assertEqual(int((labels[idx] == 1).sum()), 3)
        np.testing.assert_array_equal(idx, cap_per_class(labels, cap=10, seed=0))

    def test_resize_max_side(self):
        self.assertEqual(resize_max_side(noise_image((1024, 768)), 512).size, (512, 384))
        self.assertEqual(resize_max_side(noise_image((300, 200)), 512).size, (300, 200))

    def test_draw_boxes_keeps_size_and_marks_pixels(self):
        img = solid_image((10, 10, 10), (50, 50))
        out = draw_boxes(img, [(5, 5, 20, 20)], color=(255, 0, 0))
        self.assertEqual(out.size, (50, 50))
        self.assertEqual(out.getpixel((5, 10)), (255, 0, 0))
        self.assertEqual(img.getpixel((5, 10)), (10, 10, 10))  # original untouched


if __name__ == "__main__":
    unittest.main()


from tests.helpers import HAS_TORCH, TORCH_SKIP_REASON  # noqa: E402


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestDiagnosticEndToEnd(unittest.TestCase):
    """Runs main() on tiny synthetic data with a fake segmenter (no network)."""

    def test_main_writes_report_results_logits_and_examples(self):
        import json
        import os
        import shutil
        import tempfile

        import torch

        import tools.patch_diagnostic as diag
        from backend.fabric_classifier.classes import MATERIAL_CLASSES
        from backend.fabric_classifier.model import get_model
        from tools.prepare_external_eval import write_split_folders

        class FakeSegmenter:
            def __call__(self, image):
                lab = np.zeros(image.size[::-1], dtype=np.int64)
                h, w = lab.shape
                lab[h // 4: 3 * h // 4, w // 4: 3 * w // 4] = 4  # "upper clothes" in the middle
                return lab

        tmp = tempfile.mkdtemp()
        original = diag._Segmenter
        try:
            records, i = [], 0
            for cls in ("Cotton", "Polyester", "Silk"):
                for _ in range(2):
                    records.append((noise_image((700, 900), seed=i), cls, "eval", i))
                    i += 1
            data = os.path.join(tmp, "ext")
            write_split_folders(records, data)
            weights = os.path.join(tmp, "w.pt")
            torch.manual_seed(0)
            torch.save({"model_state_dict": get_model(14, pretrained=False).state_dict(),
                        "present_class_names": MATERIAL_CLASSES}, weights)
            diag._Segmenter = FakeSegmenter
            out = os.path.join(tmp, "out")
            diag.main(["--data-dir", data, "--weights", weights, "--out", out, "--cap", "5",
                       "--counts-json", os.path.join(ROOT, "imaterialist_processed_counts.json")])
            with open(os.path.join(out, "results.json")) as f:
                res = json.load(f)
            for v in diag.VARIANTS:
                self.assertIn(v, res)
                self.assertIn("balanced_accuracy", res[v]["prior_fixed"])
            self.assertEqual(res["meta"]["images"], 6)
            self.assertIn("garment_512", res["meta"]["single_crop_fallbacks"])
            self.assertTrue(os.path.exists(os.path.join(out, "report.md")))
            self.assertTrue(os.path.exists(os.path.join(out, "patch_examples.jpg")))
            self.assertTrue(os.path.exists(os.path.join(out, "logits.npz")))
        finally:
            diag._Segmenter = original
            shutil.rmtree(tmp, ignore_errors=True)
