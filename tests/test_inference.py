"""Inference contract tests for FabricClassifier and FabricMemoryManager.

Uses an untrained EfficientNet-B0 (no download) saved to a temp file, so the
tests check the contract, not accuracy. Need PyTorch; skipped otherwise.
"""
import json
import os
import shutil
import tempfile
import unittest

import numpy as np
from PIL import Image

from tests import ROOT  # noqa: F401
from tests.helpers import HAS_TORCH, TORCH_SKIP_REASON, noise_image

if HAS_TORCH:
    import torch

    from backend.fabric_classifier.classes import MATERIAL_CLASSES
    from backend.fabric_classifier.inference import FabricClassifier
    from backend.fabric_classifier.memory_manager import FabricMemoryManager
    from backend.fabric_classifier.model import get_model


def _write_weights(root, temperature=None, extra_calibration=None, patch_config=None):
    weights_dir = os.path.join(root, "weights")
    os.makedirs(weights_dir)
    torch.manual_seed(0)
    model = get_model(num_classes=len(MATERIAL_CLASSES), pretrained=False)
    path = os.path.join(weights_dir, "clf.pt")
    payload = {"model_state_dict": model.state_dict(), "present_class_names": MATERIAL_CLASSES}
    if patch_config is not None:
        payload["patch_config"] = patch_config
    torch.save(payload, path)
    if temperature is not None or extra_calibration:
        calib_dir = os.path.join(root, "calibration")
        os.makedirs(calib_dir)
        payload = {"temperature": temperature or 1.0, **(extra_calibration or {})}
        with open(os.path.join(calib_dir, "temperature.json"), "w") as f:
            json.dump(payload, f)
    return path


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestFabricClassifierContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.weights = _write_weights(cls.tmp)
        cls.clf = FabricClassifier(cls.weights, device="cpu")
        cls.image = noise_image((400, 500), seed=11)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_missing_weights_raise(self):
        with self.assertRaises(FileNotFoundError):
            FabricClassifier(os.path.join(self.tmp, "nope.pt"), device="cpu")

    def test_predict_returns_three_sorted_known_classes(self):
        result = self.clf.predict(self.image)
        self.assertEqual(len(result), 3)
        self.assertEqual(len({r["name"] for r in result}), 3)
        for r in result:
            self.assertEqual(set(r), {"name", "confidence"})
            self.assertIn(r["name"], MATERIAL_CLASSES)
            self.assertTrue(0.0 <= r["confidence"] <= 100.0)
        confs = [r["confidence"] for r in result]
        self.assertEqual(confs, sorted(confs, reverse=True))
        self.assertLessEqual(sum(confs), 100.0 + 1e-6)

    def test_predict_is_deterministic(self):
        self.assertEqual(self.clf.predict(self.image), self.clf.predict(self.image))

    def test_none_image_returns_uniform_contract(self):
        result = self.clf.predict(None)
        self.assertEqual(len(result), 3)

    def test_predict_detailed_agrees_with_predict(self):
        detailed = self.clf.predict_detailed(self.image)
        self.assertEqual(detailed["top3"], self.clf.predict(self.image))
        probs = np.asarray(detailed["probabilities"])
        self.assertEqual(probs.shape, (len(MATERIAL_CLASSES),))
        self.assertAlmostEqual(float(probs.sum()), 1.0, places=5)
        self.assertEqual(len(detailed["patches"]), 7)
        self.assertIn("patch_ms", detailed["timing"])
        self.assertIn("model_ms", detailed["timing"])

    def test_aggregation_matches_evaluation_rule(self):
        # Served probabilities must equal softmax(mean patch logits / T) — the rule used in evaluate/calibrate.
        from backend.fabric_classifier.inference import preprocess_patches

        detailed = self.clf.predict_detailed(self.image)
        tensor = preprocess_patches(detailed["patches"])
        with torch.no_grad():
            logits = self.clf.model.float().to("cpu")(tensor).mean(dim=0)
        expected = torch.softmax(logits / self.clf.temperature, dim=-1).numpy()
        np.testing.assert_allclose(detailed["probabilities"], expected, atol=1e-5)

    def test_prior_correction_shifts_prediction(self):
        clf = FabricClassifier(self.weights, device="cpu")
        baseline = clf.predict_detailed(self.image)["probabilities"]
        target = np.full(len(MATERIAL_CLASSES), 1e-3)
        target[5] = 1.0
        clf.set_prior_correction(target_priors=target)
        corrected = clf.predict_detailed(self.image)
        self.assertEqual(corrected["top3"][0]["name"], MATERIAL_CLASSES[5])
        self.assertFalse(np.allclose(baseline, corrected["probabilities"]))
        clf.set_prior_correction(None)
        np.testing.assert_allclose(clf.predict_detailed(self.image)["probabilities"], baseline, atol=1e-6)


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestCalibrationLoading(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_temperature_defaults_to_one(self):
        clf = FabricClassifier(_write_weights(self.tmp), device="cpu")
        self.assertEqual(clf.temperature, 1.0)

    def test_temperature_and_priors_loaded_from_calibration_file(self):
        priors = [1.0 / len(MATERIAL_CLASSES)] * len(MATERIAL_CLASSES)
        path = _write_weights(
            self.tmp,
            temperature=2.5,
            extra_calibration={"prior_correction": {"target_priors": priors, "strength": 0.5}},
        )
        clf = FabricClassifier(path, device="cpu")
        self.assertEqual(clf.temperature, 2.5)
        self.assertIsNotNone(clf.prior_correction)
        self.assertEqual(clf.prior_correction["strength"], 0.5)

    def test_patch_config_defaults_to_legacy(self):
        clf = FabricClassifier(_write_weights(self.tmp), device="cpu")
        self.assertEqual(clf.patch_config, {"patch_fraction": None, "min_coverage": 0.5})

    def test_inputs_resized_to_512_by_default(self):
        # EXP-403: the model only sees the zoom level it was trained on when photos are ≤ 512 px.
        clf = FabricClassifier(_write_weights(self.tmp), device="cpu")
        self.assertEqual(clf.max_side, 512)
        big = noise_image((1600, 1200), seed=4)
        small = big.resize((512, 384), Image.Resampling.BILINEAR)
        a, b = clf.predict_detailed(big), clf.predict_detailed(small)
        np.testing.assert_allclose(a["probabilities"], b["probabilities"], atol=1e-5)

    def test_resize_can_be_disabled(self):
        clf = FabricClassifier(_write_weights(self.tmp), device="cpu", max_side=None)
        big = noise_image((1600, 1200), seed=4)
        small = big.resize((512, 384), Image.Resampling.BILINEAR)
        a, b = clf.predict_detailed(big), clf.predict_detailed(small)
        self.assertFalse(np.allclose(a["probabilities"], b["probabilities"], atol=1e-5))

    def test_patch_config_read_from_checkpoint_and_used(self):
        cfg = {"patch_fraction": 0.2, "min_coverage": 0.9}
        clf = FabricClassifier(_write_weights(self.tmp, patch_config=cfg), device="cpu")
        self.assertEqual(clf.patch_config, cfg)
        self.assertEqual(len(clf.predict_detailed(noise_image((800, 600)))["patches"]), 7)

    def test_higher_temperature_lowers_top_confidence_but_keeps_ranking(self):
        clf = FabricClassifier(_write_weights(self.tmp), device="cpu")
        img = noise_image(seed=2)
        cold = clf.predict(img)
        clf.temperature = 5.0
        hot = clf.predict(img)
        self.assertLessEqual(hot[0]["confidence"], cold[0]["confidence"])
        self.assertEqual([r["name"] for r in hot], [r["name"] for r in cold])


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(12, 4))
        self.mm = FabricMemoryManager(self.model, preferred_device="cpu")
        self.batch = torch.randn(7, 3, 2, 2)

    def test_returns_averaged_probabilities_by_default(self):
        out = self.mm.run_inference(self.batch)
        self.assertEqual(tuple(out.shape), (4,))
        self.assertAlmostEqual(out.sum().item(), 1.0, places=5)

    def test_return_logits_gives_per_patch_logits(self):
        out = self.mm.run_inference(self.batch, return_logits=True)
        self.assertEqual(tuple(out.shape), (7, 4))
        expected = self.model(self.batch).detach()
        self.assertTrue(torch.allclose(out, expected, atol=1e-5))

    def test_unexpected_errors_are_raised_not_hidden(self):
        with self.assertRaises(RuntimeError):
            self.mm.run_inference(torch.randn(7, 3, 5, 5))  # wrong feature size for Linear(12, 4)


if __name__ == "__main__":
    unittest.main()
