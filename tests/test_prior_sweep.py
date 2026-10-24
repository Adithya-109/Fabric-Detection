"""Tests for the Phase-A prior-correction sweep (training/prior_sweep.py).

The sweep picks how strongly to correct for the training sampler's uniform prior,
using validation logits only — no retraining (docs/IMPROVEMENT_PLAN.md §4, A2).
"""
import unittest

import numpy as np

from tests import ROOT  # noqa: F401
from backend.fabric_classifier.training.prior_sweep import (
    best_result,
    evaluate_with_prior_correction,
    sweep_prior_correction,
)

NAMES = ["Cotton", "Corduroy"]


def _prior_shifted_problem(seed=0):
    """A model trained on a balanced sampler, evaluated where class 0 is 90% of data.

    Its logits are informative but calibrated to a 50/50 prior, so it over-predicts class 1.
    """
    rng = np.random.default_rng(seed)
    labels = np.array([0] * 900 + [1] * 100)
    signal = np.where(labels == 0, 0.6, -0.6) + rng.normal(0, 1.0, size=labels.size)
    logits = np.stack([signal, -signal], axis=1)
    return logits, labels


class TestEvaluateWithPriorCorrection(unittest.TestCase):
    def test_zero_strength_equals_plain_argmax(self):
        logits, labels = _prior_shifted_problem()
        m = evaluate_with_prior_correction(logits, labels, NAMES, [0.5, 0.5], [0.9, 0.1], strength=0.0)
        self.assertAlmostEqual(m["top1_accuracy"], float(np.mean(logits.argmax(1) == labels)))

    def test_correction_improves_accuracy_under_prior_shift(self):
        logits, labels = _prior_shifted_problem()
        base = evaluate_with_prior_correction(logits, labels, NAMES, [0.5, 0.5], [0.9, 0.1], strength=0.0)
        fixed = evaluate_with_prior_correction(logits, labels, NAMES, [0.5, 0.5], [0.9, 0.1], strength=1.0)
        self.assertGreater(fixed["top1_accuracy"], base["top1_accuracy"] + 0.05)
        self.assertGreater(
            fixed["per_class_metrics"]["Corduroy"]["precision"],
            base["per_class_metrics"]["Corduroy"]["precision"],
        )

    def test_temperature_is_applied(self):
        logits, labels = _prior_shifted_problem()
        a = evaluate_with_prior_correction(logits, labels, NAMES, [0.5, 0.5], [0.9, 0.1], 1.0, temperature=1.0)
        b = evaluate_with_prior_correction(logits, labels, NAMES, [0.5, 0.5], [0.9, 0.1], 1.0, temperature=3.0)
        self.assertNotEqual(a["top1_accuracy"], b["top1_accuracy"])


class TestSweep(unittest.TestCase):
    def test_returns_one_result_per_strength_in_order(self):
        logits, labels = _prior_shifted_problem()
        results = sweep_prior_correction(logits, labels, NAMES, [0.5, 0.5], [0.9, 0.1], strengths=[0, 0.5, 1])
        self.assertEqual([r["strength"] for r in results], [0, 0.5, 1])
        for r in results:
            self.assertIn("metrics", r)

    def test_best_result_by_metric(self):
        results = [
            {"strength": 0.0, "metrics": {"macro_f1": 0.4, "top1_accuracy": 0.5}},
            {"strength": 0.5, "metrics": {"macro_f1": 0.6, "top1_accuracy": 0.55}},
            {"strength": 1.0, "metrics": {"macro_f1": 0.5, "top1_accuracy": 0.7}},
        ]
        self.assertEqual(best_result(results, "macro_f1")["strength"], 0.5)
        self.assertEqual(best_result(results, "top1_accuracy")["strength"], 1.0)

    def test_best_result_respects_worst_recall_floor(self):
        results = [
            {"strength": 0.0, "metrics": {"macro_f1": 0.7, "worst_class_recall": 0.1}},
            {"strength": 1.0, "metrics": {"macro_f1": 0.6, "worst_class_recall": 0.45}},
        ]
        self.assertEqual(best_result(results, "macro_f1", min_worst_recall=0.4)["strength"], 1.0)

    def test_best_result_falls_back_when_nothing_meets_floor(self):
        results = [{"strength": 0.0, "metrics": {"macro_f1": 0.7, "worst_class_recall": 0.1}}]
        self.assertEqual(best_result(results, "macro_f1", min_worst_recall=0.4)["strength"], 0.0)

    def test_empty_results_raise(self):
        with self.assertRaises(ValueError):
            best_result([], "macro_f1")


if __name__ == "__main__":
    unittest.main()
