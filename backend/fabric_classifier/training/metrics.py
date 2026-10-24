"""Classification metrics (NumPy / scikit-learn only).

Extends the original evaluator with per-class precision, support, balanced accuracy
and the confusion matrix. Precision is what exposes over-prediction of rare classes
(e.g. Corduroy precision ≈ 4% in Attempt 309), which recall alone hides.
"""
from __future__ import annotations

import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


def _topk_accuracy(scores: np.ndarray, y_true: np.ndarray, k: int) -> float:
    k = min(k, scores.shape[1])
    topk = np.argsort(-scores, axis=1, kind="stable")[:, :k]
    return float(np.mean(np.any(topk == y_true[:, None], axis=1)))


def compute_classification_metrics(y_true, y_pred, class_names, scores=None, top_k: int = 3) -> dict:
    y_true = np.asarray(y_true, dtype=np.int64).ravel()
    y_pred = np.asarray(y_pred, dtype=np.int64).ravel()
    if y_true.size == 0:
        raise ValueError("no samples to evaluate")
    if y_true.shape != y_pred.shape:
        raise ValueError(f"y_true has {y_true.size} items but y_pred has {y_pred.size}")

    n_classes = len(class_names)
    labels = np.arange(n_classes)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )
    present = support > 0

    per_class = {
        name: {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1_score": float(f1[i]),
            "support": int(support[i]),
        }
        for i, name in enumerate(class_names)
    }

    metrics = {
        "top1_accuracy": float(np.mean(y_true == y_pred)),
        # Macro averages over classes that appear in the ground truth.
        "macro_f1": float(f1[present].mean()),
        "macro_precision": float(precision[present].mean()),
        "balanced_accuracy": float(recall[present].mean()),
        "worst_class_recall": float(recall[present].min()),
        "class_recall": [float(r) for r in recall],
        "per_class_metrics": per_class,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        "num_samples": int(y_true.size),
    }

    if scores is not None:
        scores = np.asarray(scores, dtype=np.float64)
        if scores.shape != (y_true.size, n_classes):
            raise ValueError(f"scores must have shape {(y_true.size, n_classes)}, got {scores.shape}")
        metrics["top_k"] = int(min(top_k, n_classes))
        metrics["topk_accuracy"] = _topk_accuracy(scores, y_true, top_k)
        if top_k == 3:
            metrics["top3_accuracy"] = metrics["topk_accuracy"]

    return metrics
