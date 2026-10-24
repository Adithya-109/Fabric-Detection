"""Post-processing shared by inference, evaluation and calibration (NumPy only).

Keeping one implementation guarantees that the decision rule served by the API is
the same one used to select checkpoints and fit the temperature.
"""
from __future__ import annotations

import numpy as np

_EPS = 1e-12
AGGREGATION_METHODS = ("mean_logits", "mean_probs")
DEFAULT_AGGREGATION = "mean_logits"


def softmax(x, axis: int = -1) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    shifted = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(shifted)
    return e / np.sum(e, axis=axis, keepdims=True)


def aggregate_patch_logits(patch_logits, method: str = DEFAULT_AGGREGATION) -> np.ndarray:
    """Combine per-patch logits (n_patches × C) into one logit vector (C,).

    ``mean_logits`` averages logits (what evaluate.py/calibrate.py always did).
    ``mean_probs`` averages softmax probabilities and returns their log, so that
    ``softmax(result)`` equals the averaged probabilities.
    """
    if method not in AGGREGATION_METHODS:
        raise ValueError(f"unknown aggregation method {method!r}; expected one of {AGGREGATION_METHODS}")
    arr = np.asarray(patch_logits, dtype=np.float64)
    if arr.ndim == 1:
        arr = arr[None, :]
    if arr.ndim != 2 or arr.shape[0] == 0 or arr.shape[1] == 0:
        raise ValueError(f"expected a non-empty (n_patches, n_classes) array, got shape {arr.shape}")
    if method == "mean_logits":
        return arr.mean(axis=0)
    return np.log(softmax(arr, axis=-1).mean(axis=0) + _EPS)


def apply_temperature(logits, temperature: float) -> np.ndarray:
    """Calibrated probabilities ``softmax(logits / T)``."""
    if temperature is None or float(temperature) <= 0:
        raise ValueError("temperature must be positive")
    return softmax(np.asarray(logits, dtype=np.float64) / float(temperature))


def prior_correction(probs, train_priors, target_priors, strength: float = 1.0) -> np.ndarray:
    """Re-weight posteriors for a change in class priors (Bayes rule).

    p'(c|x) ∝ p(c|x) · (target_c / train_c) ** strength

    With a model trained on a balanced sampler, ``train_priors`` is uniform and
    ``target_priors`` is the class frequency expected at deployment (e.g. from val).
    ``strength`` in [0, 1+] interpolates from no correction to full correction.
    """
    p = np.asarray(probs, dtype=np.float64)
    train = np.asarray(train_priors, dtype=np.float64).ravel()
    target = np.asarray(target_priors, dtype=np.float64).ravel()
    if train.shape != target.shape or p.shape[-1] != train.shape[0]:
        raise ValueError(
            f"shape mismatch: probs {p.shape}, train_priors {train.shape}, target_priors {target.shape}"
        )
    ratio = np.clip(target, _EPS, None) / np.clip(train, _EPS, None)
    adjusted = p * np.power(ratio, float(strength))
    return adjusted / np.clip(adjusted.sum(axis=-1, keepdims=True), _EPS, None)


def format_top_k(probs, class_names, k: int = 3) -> list[dict]:
    """The inference contract: top-k ``{"name", "confidence"}`` dicts, confidence in %, descending.

    Ties are broken by class index so output is deterministic.
    """
    p = np.asarray(probs, dtype=np.float64).ravel()
    if p.shape[0] != len(class_names):
        raise ValueError(f"{p.shape[0]} probabilities for {len(class_names)} class names")
    k = min(int(k), p.shape[0])
    order = np.lexsort((np.arange(p.shape[0]), -p))[:k]
    return [{"name": class_names[i], "confidence": round(float(p[i]) * 100.0, 2)} for i in order]
