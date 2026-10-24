"""Tests for class-balance utilities (training/balancing.py).

These replace the inverse-frequency sampler that taught the model a uniform prior
(see docs/IMPROVEMENT_PLAN.md §2).
"""
import unittest

import numpy as np

from tests import ROOT  # noqa: F401  (ensures repo root on sys.path)
from backend.fabric_classifier.training.balancing import (
    class_counts,
    class_priors,
    effective_number_weights,
    effective_training_prior,
    logit_adjustment,
    tempered_sample_weights,
)


class TestClassCounts(unittest.TestCase):
    def test_counts_every_class_including_empty(self):
        counts = class_counts([0, 0, 2, 2, 2], num_classes=4)
        np.testing.assert_array_equal(counts, [2, 0, 3, 0])

    def test_rejects_out_of_range_labels(self):
        with self.assertRaises(ValueError):
            class_counts([0, 5], num_classes=3)
        with self.assertRaises(ValueError):
            class_counts([0, -1], num_classes=3)


class TestClassPriors(unittest.TestCase):
    def test_priors_sum_to_one_and_match_frequency(self):
        priors = class_priors([0, 0, 0, 1], num_classes=2)
        np.testing.assert_allclose(priors, [0.75, 0.25])
        self.assertAlmostEqual(float(priors.sum()), 1.0)

    def test_smoothing_gives_empty_classes_nonzero_prior(self):
        priors = class_priors([0, 0], num_classes=3, smoothing=1.0)
        self.assertTrue(np.all(priors > 0))
        self.assertAlmostEqual(float(priors.sum()), 1.0)

    def test_empty_labels_raise(self):
        with self.assertRaises(ValueError):
            class_priors([], num_classes=3)


class TestTemperedSampleWeights(unittest.TestCase):
    labels = np.array([0] * 900 + [1] * 100)

    def _class_mass(self, weights):
        return np.array([weights[self.labels == c].sum() for c in (0, 1)])

    def test_weights_are_a_probability_distribution(self):
        w = tempered_sample_weights(self.labels, num_classes=2, power=0.5)
        self.assertEqual(w.shape, (1000,))
        self.assertTrue(np.all(w > 0))
        self.assertAlmostEqual(float(w.sum()), 1.0, places=6)

    def test_power_one_keeps_natural_distribution(self):
        mass = self._class_mass(tempered_sample_weights(self.labels, 2, power=1.0))
        np.testing.assert_allclose(mass, [0.9, 0.1], atol=1e-9)

    def test_power_zero_is_fully_balanced(self):
        mass = self._class_mass(tempered_sample_weights(self.labels, 2, power=0.0))
        np.testing.assert_allclose(mass, [0.5, 0.5], atol=1e-9)

    def test_power_half_is_sqrt_frequency(self):
        mass = self._class_mass(tempered_sample_weights(self.labels, 2, power=0.5))
        expected = np.sqrt([900, 100]) / np.sqrt([900, 100]).sum()  # 0.75 / 0.25
        np.testing.assert_allclose(mass, expected, atol=1e-9)

    def test_invalid_power_raises(self):
        with self.assertRaises(ValueError):
            tempered_sample_weights(self.labels, 2, power=-0.1)
        with self.assertRaises(ValueError):
            tempered_sample_weights(self.labels, 2, power=1.5)


class TestEffectiveNumberWeights(unittest.TestCase):
    def test_rarer_classes_get_larger_weight(self):
        w = effective_number_weights([10000, 1000, 100], beta=0.999)
        self.assertTrue(w[2] > w[1] > w[0])

    def test_weights_have_mean_one_over_present_classes(self):
        w = effective_number_weights([500, 50, 0], beta=0.99)
        self.assertEqual(w[2], 0.0)
        self.assertAlmostEqual(float(w[:2].mean()), 1.0, places=6)

    def test_beta_zero_gives_equal_weights(self):
        w = effective_number_weights([10, 1000], beta=0.0)
        np.testing.assert_allclose(w, [1.0, 1.0])

    def test_invalid_beta_raises(self):
        with self.assertRaises(ValueError):
            effective_number_weights([1, 2], beta=1.0)


class TestEffectiveTrainingPrior(unittest.TestCase):
    counts = np.array([900, 100])

    def test_natural_sampling_unweighted_loss_is_data_frequency(self):
        np.testing.assert_allclose(effective_training_prior(self.counts, 1.0, False), [0.9, 0.1])

    def test_balanced_sampler_is_uniform(self):
        np.testing.assert_allclose(effective_training_prior(self.counts, 0.0, False), [0.5, 0.5])

    def test_legacy_double_balancing_inverts_the_prior(self):
        # Balanced sampler + inverse-frequency loss weights (the legacy trainer):
        # rarer classes look MORE likely to the model.
        prior = effective_training_prior(self.counts, 0.0, True)
        np.testing.assert_allclose(prior, [0.1, 0.9])

    def test_empty_class_gets_zero_prior(self):
        prior = effective_training_prior([10, 0, 30], 1.0, False)
        self.assertEqual(prior[1], 0.0)
        self.assertAlmostEqual(float(prior.sum()), 1.0)


class TestLogitAdjustment(unittest.TestCase):
    def test_is_tau_times_log_prior(self):
        priors = np.array([0.5, 0.25, 0.25])
        np.testing.assert_allclose(logit_adjustment(priors, tau=2.0), 2.0 * np.log(priors))

    def test_uniform_priors_shift_all_logits_equally(self):
        adj = logit_adjustment(np.full(4, 0.25), tau=1.0)
        self.assertAlmostEqual(float(np.ptp(adj)), 0.0)

    def test_zero_prior_is_finite(self):
        adj = logit_adjustment(np.array([1.0, 0.0]))
        self.assertTrue(np.all(np.isfinite(adj)))


if __name__ == "__main__":
    unittest.main()
