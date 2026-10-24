"""Tests for the recalibration tool (training/recalibrate.py).

Recalibration = post-hoc prior correction + temperature scaling on the EXISTING
weights, evaluated on the iMaterialist val/test folders (whose split is fixed on
disk, so no training image can leak into evaluation).
"""
import json
import os
import shutil
import tempfile
import unittest

import numpy as np

from tests import ROOT  # noqa: F401
from tests.helpers import HAS_TORCH, TORCH_SKIP_REASON, noise_image
from backend.fabric_classifier.postprocess import softmax
from backend.fabric_classifier.training.recalibrate import (
    compare_metrics,
    count_split,
    fit_temperature,
    list_split,
    load_logits,
    render_report,
    save_logits,
)

CLASSES = ["Cotton", "Polyester", "Silk"]


def _make_tree(root, counts):
    """counts: {split: {class: n}} → creates JPEGs under root/split/class/."""
    for split, per_class in counts.items():
        for cls, n in per_class.items():
            d = os.path.join(root, split, cls)
            os.makedirs(d, exist_ok=True)
            for i in range(n):
                noise_image((64, 64), seed=i).save(os.path.join(d, f"img_{i:03d}.jpg"))


class TestSplitListing(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        _make_tree(self.root, {
            "train": {"Cotton": 5, "Polyester": 2},
            "val": {"Cotton": 2, "Silk": 1},
        })
        # noise that must be ignored
        open(os.path.join(self.root, "val", "Cotton", "notes.txt"), "w").close()
        os.makedirs(os.path.join(self.root, "val", "Unknown"), exist_ok=True)
        noise_image((32, 32)).save(os.path.join(self.root, "val", "Unknown", "x.jpg"))

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_lists_images_with_class_indices_sorted(self):
        paths, labels = list_split(self.root, "val", CLASSES)
        self.assertEqual(len(paths), 3)
        self.assertEqual(labels.tolist(), [0, 0, 2])
        self.assertEqual(paths, sorted(paths))
        self.assertTrue(all(p.endswith(".jpg") for p in paths))

    def test_limit_takes_a_class_balanced_deterministic_subset(self):
        paths, labels = list_split(self.root, "train", CLASSES, limit_per_class=1)
        self.assertEqual(labels.tolist(), [0, 1])
        again, _ = list_split(self.root, "train", CLASSES, limit_per_class=1)
        self.assertEqual(paths, again)

    def test_counts_per_class_include_missing_classes(self):
        np.testing.assert_array_equal(count_split(self.root, "train", CLASSES), [5, 2, 0])

    def test_missing_split_raises_clear_error(self):
        with self.assertRaises(FileNotFoundError):
            list_split(self.root, "test", CLASSES)


class TestFitTemperature(unittest.TestCase):
    def _overconfident(self, n=5000, seed=0):
        """Labels sampled from softmax(true_logits) → true_logits are perfectly calibrated;
        the 'model' outputs 3x those logits, i.e. it is 3x over-confident (ideal T = 3)."""
        rng = np.random.default_rng(seed)
        true_logits = rng.normal(0, 1.5, (n, 3))
        probs = softmax(true_logits)
        labels = np.array([rng.choice(3, p=p) for p in probs])
        return true_logits * 3.0, true_logits, labels

    def test_recovers_overconfidence_factor(self):
        scaled, _, labels = self._overconfident()
        self.assertAlmostEqual(fit_temperature(scaled, labels), 3.0, delta=0.4)

    def test_reduces_negative_log_likelihood(self):
        scaled, _, labels = self._overconfident()
        t = fit_temperature(scaled, labels)

        def nll(temp):
            p = softmax(scaled / temp)
            return -np.mean(np.log(p[np.arange(len(labels)), labels] + 1e-12))

        self.assertLess(nll(t), nll(1.0))

    def test_offset_is_applied_after_scaling(self):
        scaled, _, labels = self._overconfident()
        offset = np.array([0.0, 0.0, 0.0])
        self.assertAlmostEqual(fit_temperature(scaled, labels, offset=offset), fit_temperature(scaled, labels),
                               places=4)

    def test_result_within_bounds(self):
        logits = np.zeros((10, 3))
        t = fit_temperature(logits, np.zeros(10, dtype=int), bounds=(0.5, 2.0))
        self.assertTrue(0.5 <= t <= 2.0)


class TestEvalDatasetPickles(unittest.TestCase):
    def test_dataset_is_picklable_for_spawned_workers(self):
        import pickle

        from backend.fabric_classifier.training.recalibrate import EvalDataset

        ds = pickle.loads(pickle.dumps(EvalDataset(["a.jpg", "b.jpg"])))
        self.assertEqual(len(ds), 2)


class TestLogitCache(unittest.TestCase):
    def test_round_trip(self):
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, "sub", "val.npz")
            logits = np.random.default_rng(0).normal(size=(4, 3)).astype(np.float32)
            save_logits(path, logits, np.array([0, 1, 2, 0]), ["a.jpg", "b.jpg", "c.jpg", "d.jpg"])
            got = load_logits(path)
            np.testing.assert_allclose(got["logits"], logits)
            self.assertEqual(got["labels"].tolist(), [0, 1, 2, 0])
            self.assertEqual(got["paths"], ["a.jpg", "b.jpg", "c.jpg", "d.jpg"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_cache_returns_none(self):
        self.assertIsNone(load_logits("/nonexistent/cache.npz"))


class TestReport(unittest.TestCase):
    def _m(self, top1, f1, worst, recalls, precisions):
        return {
            "top1_accuracy": top1, "top3_accuracy": top1 + 0.2, "macro_f1": f1, "worst_class_recall": worst,
            "balanced_accuracy": float(np.mean(recalls)),
            "per_class_metrics": {
                c: {"recall": r, "precision": p, "f1_score": 0.0, "support": 10}
                for c, r, p in zip(CLASSES, recalls, precisions)
            },
        }

    def test_compare_metrics_reports_deltas(self):
        before = self._m(0.40, 0.35, 0.10, [0.1, 0.5, 0.9], [0.9, 0.5, 0.1])
        after = self._m(0.55, 0.45, 0.30, [0.6, 0.5, 0.3], [0.7, 0.5, 0.4])
        rows = compare_metrics(before, after)
        top1 = next(r for r in rows if r["metric"] == "top1_accuracy")
        self.assertAlmostEqual(top1["delta"], 0.15)
        self.assertEqual({r["metric"] for r in rows} >= {"macro_f1", "worst_class_recall", "top3_accuracy"}, True)

    def test_render_report_contains_key_facts(self):
        before = self._m(0.40, 0.35, 0.10, [0.1, 0.5, 0.9], [0.9, 0.5, 0.1])
        after = self._m(0.55, 0.45, 0.30, [0.6, 0.5, 0.3], [0.7, 0.5, 0.4])
        text = render_report(
            split="val", before=before, after=after, class_names=CLASSES,
            settings={"strength": 0.8, "temperature": 1.7}, n_images=30,
        )
        for needle in ("val", "0.8", "1.7", "Cotton", "Top-1", "Macro-F1", "40.0%", "55.0%", "+15.0"):
            self.assertIn(needle, text)


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestRecalibrateEndToEnd(unittest.TestCase):
    """Runs the full CLI on a tiny synthetic dataset with an untrained model."""

    def test_cli_writes_report_cache_and_calibration(self):
        import torch

        from backend.fabric_classifier.classes import MATERIAL_CLASSES
        from backend.fabric_classifier.model import get_model
        from backend.fabric_classifier.training.recalibrate import main

        tmp = tempfile.mkdtemp()
        try:
            data = os.path.join(tmp, "imat")
            _make_tree(data, {
                "train": {c: 3 for c in MATERIAL_CLASSES},
                "val": {c: 2 for c in MATERIAL_CLASSES},
                "test": {c: 2 for c in MATERIAL_CLASSES},
            })
            weights_dir = os.path.join(tmp, "model", "weights")
            os.makedirs(weights_dir)
            weights = os.path.join(weights_dir, "best.pt")
            torch.manual_seed(0)
            torch.save({"model_state_dict": get_model(14, pretrained=False).state_dict(),
                        "present_class_names": MATERIAL_CLASSES}, weights)
            out = os.path.join(tmp, "out")

            # num-workers 2 exercises multiprocess pickling of the dataset (spawn on macOS).
            main(["--weights", weights, "--imaterialist-dir", data, "--out", out, "--device", "cpu",
                  "--num-workers", "2", "--batch-size", "4", "--report-test", "--write"])

            self.assertTrue(os.path.exists(os.path.join(out, "logits_val.npz")))
            self.assertTrue(os.path.exists(os.path.join(out, "logits_test.npz")))
            with open(os.path.join(out, "recalibration_report.md")) as f:
                report = f.read()
            self.assertIn("Top-1", report)
            with open(os.path.join(out, "recalibration_results.json")) as f:
                results = json.load(f)
            self.assertIn("val", results)
            self.assertIn("test", results)

            calib_path = os.path.join(tmp, "model", "calibration", "temperature.json")
            with open(calib_path) as f:
                calib = json.load(f)
            self.assertGreater(calib["temperature"], 0)
            self.assertEqual(len(calib["prior_correction"]["target_priors"]), 14)

            # The written calibration loads in the real inference class.
            from backend.fabric_classifier.inference import FabricClassifier

            clf = FabricClassifier(weights, device="cpu")
            self.assertEqual(clf.temperature, calib["temperature"])
            self.assertIsNotNone(clf.prior_correction)
            self.assertEqual(len(clf.predict(noise_image((300, 300)))), 3)

            # Second run reuses the cached logits (no model pass needed).
            main(["--weights", weights, "--imaterialist-dir", data, "--out", out, "--device", "cpu",
                  "--num-workers", "0"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
