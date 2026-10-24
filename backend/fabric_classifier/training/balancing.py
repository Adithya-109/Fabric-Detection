"""Class-balance utilities for long-tailed training data.

The original trainer sampled with weights 1/count, so the model saw every class
equally often and learned a uniform prior, while val/test keep the real (heavily
Cotton/Polyester) distribution. These helpers support the replacements described
in docs/IMPROVEMENT_PLAN.md §4 (Phase B2): tempered sampling plus logit adjustment.
"""
from __future__ import annotations

import numpy as np

_EPS = 1e-12


def class_counts(labels, num_classes: int) -> np.ndarray:
    """Number of samples per class, including classes with zero samples."""
    labels = np.asarray(labels, dtype=np.int64).ravel()
    if labels.size and (labels.min() < 0 or labels.max() >= num_classes):
        raise ValueError(f"labels must be in [0, {num_classes}); got range [{labels.min()}, {labels.max()}]")
    return np.bincount(labels, minlength=num_classes).astype(np.int64)


def class_priors(labels, num_classes: int, smoothing: float = 0.0) -> np.ndarray:
    """Empirical class frequencies, optionally with additive (Laplace) smoothing."""
    labels = np.asarray(labels).ravel()
    if labels.size == 0:
        raise ValueError("cannot estimate priors from an empty label list")
    counts = class_counts(labels, num_classes).astype(np.float64) + float(smoothing)
    return counts / counts.sum()


def tempered_sample_weights(labels, num_classes: int, power: float = 0.5) -> np.ndarray:
    """Per-sample weights so that class c is drawn with probability ∝ count_c ** power.

    power=1 → natural distribution, power=0 → fully balanced (the old behaviour),
    power=0.5 → square-root sampling, a common middle ground for long tails.
    Returned weights sum to 1 and can be passed to ``WeightedRandomSampler``.
    """
    if not 0.0 <= power <= 1.0:
        raise ValueError("power must be in [0, 1]")
    labels = np.asarray(labels, dtype=np.int64).ravel()
    counts = class_counts(labels, num_classes).astype(np.float64)
    per_class = np.zeros(num_classes, dtype=np.float64)
    present = counts > 0
    per_class[present] = counts[present] ** (power - 1.0)
    weights = per_class[labels]
    return weights / weights.sum()


def effective_number_weights(counts, beta: float = 0.999) -> np.ndarray:
    """Class-balanced loss weights from the "effective number of samples" (Cui et al., 2019).

    w_c ∝ (1 - beta) / (1 - beta ** n_c), normalised to mean 1 over classes that have
    samples; classes with no samples get weight 0.
    """
    if not 0.0 <= beta < 1.0:
        raise ValueError("beta must be in [0, 1)")
    counts = np.asarray(counts, dtype=np.float64)
    weights = np.zeros_like(counts)
    present = counts > 0
    if beta == 0.0:
        weights[present] = 1.0
    else:
        weights[present] = (1.0 - beta) / (1.0 - np.power(beta, counts[present]))
    if present.any():
        weights[present] /= weights[present].mean()
    return weights


def effective_training_prior(counts, sampler_power: float, class_weighted_loss: bool) -> np.ndarray:
    """The class prior the model implicitly learns from the training setup.

    Sampling with ``tempered_sample_weights(power)`` shows class c with frequency
    ∝ count_c ** power; an inverse-frequency class-weighted loss multiplies that by
    1 / count_c. The legacy trainer did both (power=0 + weighted loss), giving an
    effective prior ∝ 1 / count_c — rare classes look *more* likely than common ones.
    This is the ``train_priors`` to use for post-hoc prior correction.
    """
    counts = np.asarray(counts, dtype=np.float64)
    prior = np.zeros_like(counts)
    present = counts > 0
    exponent = float(sampler_power) - (1.0 if class_weighted_loss else 0.0)
    prior[present] = counts[present] ** exponent
    return prior / prior.sum()


def logit_adjustment(priors, tau: float = 1.0) -> np.ndarray:
    """Additive logit offsets ``tau * log(prior)`` (Menon et al., 2021)."""
    priors = np.asarray(priors, dtype=np.float64)
    return float(tau) * np.log(np.clip(priors, _EPS, None))
