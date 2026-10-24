"""Tests for shared post-processing (backend/fabric_classifier/postprocess.py).

One implementation is used by inference, evaluation and calibration so the
decision rule that is served is the one that was measured (plan §3.6).
"""
import unittest

import numpy as np

from tests import ROOT  # noqa: F401
from backend.fabric_classifier.postprocess import (
    aggregate_patch_logits,
    apply_temperature,
    format_top_k,
    prior_correction,
    softmax,
)

NAMES = ["Cotton", "Polyester", "Silk", "Denim"]


class TestSoftmax(unittest.TestCase):
    def test_sums_to_one(self):
        p = softmax(np.array([1.0, 2.0, 3.0]))
        self.assertAlmostEqual(float(p.sum()), 1.0)
        self.assertTrue(p[2] > p[1] > p[0])

    def test_numerically_stable_for_large_logits(self):
        p = softmax(np.array([1000.0, 1000.0]))
        np.testing.assert_allclose(p, [0.5, 0.5])

    def test_batched_rows(self):
        p = softmax(np.array([[0.0, 0.0], [10.0, 0.0]]))
        np.testing.assert_allclose(p.sum(axis=-1), [1.0, 1.0])


class TestAggregatePatchLogits(unittest.TestCase):
    patch_logits = np.array([[4.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])

    def test_mean_logits(self):
        out = aggregate_patch_logits(self.patch_logits, method="mean_logits")
        np.testing.assert_allclose(out, self.patch_logits.mean(axis=0))

    def test_mean_probs_returns_log_of_mean_probability(self):
        out = aggregate_patch_logits(self.patch_logits, method="mean_probs")
        expected = softmax(self.patch_logits).mean(axis=0)
        np.testing.assert_allclose(softmax(out), expected, rtol=1e-6)

    def test_single_patch_vector_is_accepted(self):
        out = aggregate_patch_logits(np.array([1.0, 2.0]), method="mean_logits")
        np.testing.assert_allclose(out, [1.0, 2.0])

    def test_unknown_method_and_empty_input_raise(self):
        with self.assertRaises(ValueError):
            aggregate_patch_logits(self.patch_logits, method="max")
        with self.assertRaises(ValueError):
            aggregate_patch_logits(np.zeros((0, 4)))


class TestApplyTemperature(unittest.TestCase):
    logits = np.array([2.0, 1.0, 0.0])

    def test_temperature_one_is_plain_softmax(self):
        np.testing.assert_allclose(apply_temperature(self.logits, 1.0), softmax(self.logits))

    def test_higher_temperature_softens_but_keeps_ranking(self):
        sharp, soft = apply_temperature(self.logits, 1.0), apply_temperature(self.logits, 3.0)
        self.assertLess(soft.max(), sharp.max())
        np.testing.assert_array_equal(np.argsort(soft), np.argsort(sharp))

    def test_non_positive_temperature_raises(self):
        for t in (0.0, -1.0):
            with self.assertRaises(ValueError):
                apply_temperature(self.logits, t)


class TestPriorCorrection(unittest.TestCase):
    def test_equal_priors_leave_probs_unchanged(self):
        p = np.array([0.1, 0.2, 0.7])
        out = prior_correction(p, train_priors=np.full(3, 1 / 3), target_priors=np.full(3, 1 / 3))
        np.testing.assert_allclose(out, p)

    def test_moves_mass_towards_frequent_target_class(self):
        # Model trained on a uniform prior; in reality class 0 is 9x more common.
        p = np.array([0.4, 0.6])
        out = prior_correction(p, train_priors=[0.5, 0.5], target_priors=[0.9, 0.1])
        self.assertAlmostEqual(float(out.sum()), 1.0)
        self.assertGreater(out[0], out[1])  # decision flips to the common class

    def test_strength_zero_is_identity_and_scales_smoothly(self):
        p = np.array([0.4, 0.6])
        kwargs = dict(train_priors=[0.5, 0.5], target_priors=[0.9, 0.1])
        np.testing.assert_allclose(prior_correction(p, strength=0.0, **kwargs), p)
        half = prior_correction(p, strength=0.5, **kwargs)
        full = prior_correction(p, strength=1.0, **kwargs)
        self.assertTrue(p[0] < half[0] < full[0])

    def test_matches_bayes_rule(self):
        p = np.array([0.2, 0.3, 0.5])
        train, target = np.array([0.5, 0.25, 0.25]), np.array([0.2, 0.2, 0.6])
        expected = p * target / train
        expected /= expected.sum()
        np.testing.assert_allclose(prior_correction(p, train, target), expected)

    def test_works_on_batches(self):
        p = np.array([[0.4, 0.6], [0.7, 0.3]])
        out = prior_correction(p, [0.5, 0.5], [0.9, 0.1])
        np.testing.assert_allclose(out.sum(axis=-1), [1.0, 1.0])

    def test_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            prior_correction(np.array([0.5, 0.5]), [0.5, 0.5], [0.3, 0.3, 0.4])


class TestFormatTopK(unittest.TestCase):
    def test_contract_shape_and_order(self):
        probs = np.array([0.1, 0.5, 0.15, 0.25])
        top = format_top_k(probs, NAMES, k=3)
        self.assertEqual([t["name"] for t in top], ["Polyester", "Denim", "Silk"])
        self.assertEqual([t["confidence"] for t in top], [50.0, 25.0, 15.0])
        for item in top:
            self.assertEqual(set(item), {"name", "confidence"})
            self.assertIsInstance(item["confidence"], float)

    def test_k_larger_than_classes_is_clamped(self):
        self.assertEqual(len(format_top_k(np.array([0.6, 0.4]), NAMES[:2], k=3)), 2)

    def test_ties_resolved_by_class_order(self):
        top = format_top_k(np.full(4, 0.25), NAMES, k=3)
        self.assertEqual([t["name"] for t in top], NAMES[:3])

    def test_name_count_mismatch_raises(self):
        with self.assertRaises(ValueError):
            format_top_k(np.array([0.5, 0.5]), NAMES, k=1)


if __name__ == "__main__":
    unittest.main()
