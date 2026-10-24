"""Training losses and helpers for long-tailed fabric data (PyTorch).

Logit-adjusted cross-entropy (Menon et al., 2021, "Long-tail learning via logit
adjustment") trains on the natural (or tempered) data distribution while still
giving rare classes a fair margin, instead of oversampling them to a uniform prior.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

_EPS = 1e-12


def logit_adjusted_cross_entropy(logits: torch.Tensor, targets: torch.Tensor, log_priors: torch.Tensor,
                                 tau: float = 1.0, label_smoothing: float = 0.0,
                                 ignore_index: int = -1) -> torch.Tensor:
    """Cross-entropy on ``logits + tau * log_priors``.

    At inference, use the raw logits: the adjustment only shapes training.
    Samples whose target equals ``ignore_index`` (the trainer's marker for
    corrupted images) are skipped.
    """
    adjusted = logits + float(tau) * log_priors.to(device=logits.device, dtype=logits.dtype)
    return F.cross_entropy(adjusted, targets, label_smoothing=label_smoothing, ignore_index=ignore_index)


class LogitAdjustedLoss(nn.Module):
    """``nn.Module`` wrapper; priors are stored as a buffer so they follow ``.to(device)``."""

    def __init__(self, priors, tau: float = 1.0, label_smoothing: float = 0.0, ignore_index: int = -1):
        super().__init__()
        priors = torch.as_tensor(priors, dtype=torch.float32)
        self.register_buffer("log_priors", torch.log(priors.clamp_min(_EPS)))
        self.tau = float(tau)
        self.label_smoothing = float(label_smoothing)
        self.ignore_index = int(ignore_index)

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        return logit_adjusted_cross_entropy(
            logits, targets, self.log_priors, self.tau, self.label_smoothing, self.ignore_index
        )


def freeze_batchnorm(model: nn.Module, freeze_affine: bool = True) -> int:
    """Put every BatchNorm layer in eval mode (keep ImageNet running stats).

    With a batch of 4 the batch statistics are too noisy to update running stats.
    ``model.train()`` resets BN to training mode, so call this after it at the start
    of every epoch. Returns the number of BN layers frozen.
    """
    count = 0
    for module in model.modules():
        if isinstance(module, nn.modules.batchnorm._BatchNorm):
            module.eval()
            if freeze_affine:
                for p in module.parameters():
                    p.requires_grad_(False)
            count += 1
    return count
