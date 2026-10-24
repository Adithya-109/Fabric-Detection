"""Tests for evaluating on an external dataset (tools/prepare_external_eval.py) and the
recalibrate options it needs (custom split names, training counts from JSON)."""
import json
import os
import shutil
import tempfile
import unittest

import numpy as np
from PIL import Image

from tests import ROOT  # noqa: F401
from tests.helpers import HAS_TORCH, TORCH_SKIP_REASON, noise_image, smooth_image
from backend.fabric_classifier.classes import MATERIAL_CLASSES
from backend.fabric_classifier.training.recalibrate import load_train_counts_json
from tools.prepare_external_eval import (
    assign_halves,
    contact_sheet,
    map_label,
    write_split_folders,
)


class TestMapLabel(unittest.TestCase):
    def test_single_material_labels_map_to_contract_classes(self):
        cases = {
            "Cotton": "Cotton", "Pure Cotton": "Cotton", "Organic Cotton": "Cotton",
            "Polyester": "Polyester", "Silk": "Silk", "Pure Silk": "Silk", "Raw Silk": "Silk",
            "Denim": "Denim", "Linen": "Linen", "Hemp": "Linen", "Wool": "Wool", "Pure Wool": "Wool",
            "Pashmina": "Wool", "Leather": "Leather", "Synthetic Leather": "Leather", "Velvet": "Velvet",
            "Corduroy": "Corduroy", "Fleece": "Fleece", "Faux Fur": "Fleece", "Nylon": "Nylon",
            "Elastane": "Nylon", "Satin": "Satin", "Suede": "Suede",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(map_label(text), expected)

    def test_blends_synthetic_lookalikes_and_unknowns_are_dropped(self):
        for text in ("Cotton Blend", "Silk Blend", "Art Silk", "Poly Silk", "Polycotton", "Cotton Silk",
                     "Viscose Rayon", "Georgette", "Net", "Acrylic", "Other", "PU", "", None):
            with self.subTest(text=text):
                self.assertIsNone(map_label(text))

    def test_case_and_whitespace_insensitive(self):
        self.assertEqual(map_label("  pure COTTON "), "Cotton")

    def test_all_targets_are_contract_classes(self):
        from tools.prepare_external_eval import LABEL_MAP

        self.assertTrue(set(LABEL_MAP.values()) <= set(MATERIAL_CLASSES))


class TestAssignHalves(unittest.TestCase):
    def test_roughly_half_per_class_and_duplicates_stay_together(self):
        rng = np.random.default_rng(0)
        labels = np.array([0] * 200 + [1] * 60)
        hashes = [int(h) for h in rng.integers(0, 2 ** 62, size=len(labels))]
        hashes[5] = hashes[4]  # an exact duplicate pair
        halves = assign_halves(labels, hashes, seed=1)
        self.assertEqual(set(halves.tolist()), {"calib", "eval"})
        self.assertEqual(halves[4], halves[5])
        for cls in (0, 1):
            frac = np.mean(halves[labels == cls] == "eval")
            self.assertAlmostEqual(frac, 0.5, delta=0.1)

    def test_deterministic(self):
        labels = np.array([0, 1] * 50)
        hashes = list(range(100))
        np.testing.assert_array_equal(assign_halves(labels, hashes, seed=3), assign_halves(labels, hashes, seed=3))


class TestWriteFolders(unittest.TestCase):
    def test_layout_is_split_class_file(self):
        tmp = tempfile.mkdtemp()
        try:
            records = [
                (noise_image((40, 30)), "Cotton", "calib", 0),
                (noise_image((40, 30)).convert("RGBA"), "Silk", "eval", 7),
            ]
            paths = write_split_folders(records, tmp)
            self.assertEqual(len(paths), 2)
            self.assertTrue(os.path.exists(os.path.join(tmp, "calib", "Cotton", "000000.jpg")))
            self.assertTrue(os.path.exists(os.path.join(tmp, "eval", "Silk", "000007.jpg")))
            with Image.open(os.path.join(tmp, "eval", "Silk", "000007.jpg")) as im:
                self.assertEqual(im.mode, "RGB")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestContactSheet(unittest.TestCase):
    def test_grid_has_one_row_per_class(self):
        tmp = tempfile.mkdtemp()
        try:
            by_class = {}
            for cls in ("Cotton", "Silk"):
                by_class[cls] = []
                for i in range(3):
                    p = os.path.join(tmp, f"{cls}_{i}.jpg")
                    smooth_image((120, 80), seed=i).save(p)
                    by_class[cls].append(p)
            out = os.path.join(tmp, "sheet.png")
            contact_sheet(by_class, out, per_class=4, thumb=50)
            with Image.open(out) as im:
                w, h = im.size
            self.assertGreaterEqual(h, 2 * 50)
            self.assertGreaterEqual(w, 4 * 50)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestTrainCountsJson(unittest.TestCase):
    def test_reads_nested_and_flat_formats(self):
        tmp = tempfile.mkdtemp()
        try:
            nested = os.path.join(tmp, "a.json")
            with open(nested, "w") as f:
                json.dump({"splits": {"train": 5}, "classes": {"Silk": 3, "Cotton": 10}}, f)
            flat = os.path.join(tmp, "b.json")
            with open(flat, "w") as f:
                json.dump({"Cotton": 1, "Polyester": 2}, f)
            names = ["Cotton", "Polyester", "Silk"]
            np.testing.assert_array_equal(load_train_counts_json(nested, names), [10, 0, 3])
            np.testing.assert_array_equal(load_train_counts_json(flat, names), [1, 2, 0])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_repo_counts_file_covers_all_classes(self):
        counts = load_train_counts_json(os.path.join(ROOT, "imaterialist_processed_counts.json"), MATERIAL_CLASSES)
        self.assertTrue(np.all(counts > 0))


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestRecalibrateCustomSplits(unittest.TestCase):
    def test_calib_eval_splits_with_counts_json_and_no_train_folder(self):
        import torch

        from backend.fabric_classifier.model import get_model
        from backend.fabric_classifier.training.recalibrate import main

        tmp = tempfile.mkdtemp()
        try:
            data = os.path.join(tmp, "ext")
            records, i = [], 0
            for split in ("calib", "eval"):
                for cls in ("Cotton", "Polyester", "Silk"):
                    for _ in range(3):
                        records.append((noise_image((80, 80), seed=i), cls, split, i))
                        i += 1
            write_split_folders(records, data)
            os.makedirs(os.path.join(tmp, "m", "weights"))
            weights = os.path.join(tmp, "m", "weights", "w.pt")
            torch.manual_seed(0)
            torch.save({"model_state_dict": get_model(14, pretrained=False).state_dict(),
                        "present_class_names": MATERIAL_CLASSES}, weights)
            out = os.path.join(tmp, "out")
            results = main([
                "--weights", weights, "--data-dir", data, "--select-split", "calib", "--test-split", "eval",
                "--train-counts-json", os.path.join(ROOT, "imaterialist_processed_counts.json"),
                "--out", out, "--device", "cpu", "--num-workers", "0", "--report-test",
            ])
            self.assertIn("calib", results)
            self.assertIn("eval", results)
            self.assertEqual(results["eval"]["before"]["num_samples"], 9)
            self.assertTrue(os.path.exists(os.path.join(out, "logits_eval.npz")))
            # absent classes must not drag worst recall to zero
            self.assertGreaterEqual(results["eval"]["before"]["worst_class_recall"], 0.0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
