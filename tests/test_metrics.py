"""Tests for evaluation metrics (training/metrics.py).

Adds precision and the confusion matrix, which the old evaluator did not report and
which reveal the prior-shift problem (plan §2).
"""
import unittest

import numpy as np

from tests import ROOT  # noqa: F401
from backend.fabric_classifier.training.metrics import compute_classification_metrics

NAMES = ["A", "B", "C"]


class TestClassificationMetrics(unittest.TestCase):
    def test_perfect_predictions(self):
        y = [0, 1, 2, 2]
        m = compute_classification_metrics(y, y, NAMES)
        self.assertEqual(m["top1_accuracy"], 1.0)
        self.assertEqual(m["macro_f1"], 1.0)
        self.assertEqual(m["balanced_accuracy"], 1.0)
        self.assertEqual(m["worst_class_recall"], 1.0)

    def test_precision_recall_and_support(self):
        y_true = [0, 0, 0, 0, 1, 2]
        y_pred = [0, 1, 1, 1, 1, 2]  # class 1 over-predicted
        m = compute_classification_metrics(y_true, y_pred, NAMES)
        a, b = m["per_class_metrics"]["A"], m["per_class_metrics"]["B"]
        self.assertAlmostEqual(a["recall"], 0.25)
        self.assertAlmostEqual(a["precision"], 1.0)
        self.assertEqual(a["support"], 4)
        self.assertAlmostEqual(b["precision"], 0.25)
        self.assertAlmostEqual(b["recall"], 1.0)
        for key in ("precision", "recall", "f1_score", "support"):
            self.assertIn(key, a)

    def test_confusion_matrix_rows_are_true_labels(self):
        m = compute_classification_metrics([0, 0, 1], [0, 1, 1], NAMES)
        self.assertEqual(m["confusion_matrix"], [[1, 1, 0], [0, 1, 0], [0, 0, 0]])

    def test_worst_recall_ignores_classes_absent_from_ground_truth(self):
        # Class C never appears in y_true: it must not drag worst recall to 0.
        m = compute_classification_metrics([0, 1, 1], [0, 1, 1], NAMES)
        self.assertEqual(m["worst_class_recall"], 1.0)
        self.assertEqual(m["per_class_metrics"]["C"]["support"], 0)

    def test_top3_accuracy_from_scores(self):
        scores = np.array([[0.1, 0.5, 0.4], [0.7, 0.2, 0.1]])
        names = ["A", "B", "C"]
        m = compute_classification_metrics([2, 2], scores.argmax(axis=1), names, scores=scores, top_k=2)
        self.assertAlmostEqual(m["top1_accuracy"], 0.0)
        self.assertAlmostEqual(m["topk_accuracy"], 0.5)
        self.assertEqual(m["top_k"], 2)

    def test_backwards_compatible_keys(self):
        m = compute_classification_metrics([0, 1], [0, 1], NAMES)
        for key in ("top1_accuracy", "macro_f1", "worst_class_recall", "class_recall", "per_class_metrics"):
            self.assertIn(key, m)
        self.assertEqual(len(m["class_recall"]), 3)

    def test_length_mismatch_and_empty_raise(self):
        with self.assertRaises(ValueError):
            compute_classification_metrics([0, 1], [0], NAMES)
        with self.assertRaises(ValueError):
            compute_classification_metrics([], [], NAMES)


if __name__ == "__main__":
    unittest.main()
