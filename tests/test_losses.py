"""Tests for training losses (training/losses.py). Need PyTorch; skipped otherwise."""
import math
import unittest

from tests import ROOT  # noqa: F401
from tests.helpers import HAS_TORCH, TORCH_SKIP_REASON

if HAS_TORCH:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    from backend.fabric_classifier.training.losses import (
        LogitAdjustedLoss,
        freeze_batchnorm,
        logit_adjusted_cross_entropy,
    )


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestLogitAdjustedCrossEntropy(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)
        self.logits = torch.randn(16, 5)
        self.targets = torch.randint(0, 5, (16,))

    def test_uniform_priors_equal_plain_cross_entropy(self):
        log_priors = torch.log(torch.full((5,), 0.2))
        ours = logit_adjusted_cross_entropy(self.logits, self.targets, log_priors, tau=1.0)
        self.assertAlmostEqual(ours.item(), F.cross_entropy(self.logits, self.targets).item(), places=5)

    def test_tau_zero_equals_plain_cross_entropy(self):
        log_priors = torch.log(torch.tensor([0.6, 0.1, 0.1, 0.1, 0.1]))
        ours = logit_adjusted_cross_entropy(self.logits, self.targets, log_priors, tau=0.0)
        self.assertAlmostEqual(ours.item(), F.cross_entropy(self.logits, self.targets).item(), places=5)

    def test_matches_definition(self):
        log_priors = torch.log(torch.tensor([0.6, 0.1, 0.1, 0.1, 0.1]))
        expected = F.cross_entropy(self.logits + 0.5 * log_priors, self.targets)
        ours = logit_adjusted_cross_entropy(self.logits, self.targets, log_priors, tau=0.5)
        self.assertAlmostEqual(ours.item(), expected.item(), places=5)

    def test_rare_true_class_costs_more(self):
        logits = torch.zeros(1, 2)
        log_priors = torch.log(torch.tensor([0.99, 0.01]))
        rare = logit_adjusted_cross_entropy(logits, torch.tensor([1]), log_priors)
        common = logit_adjusted_cross_entropy(logits, torch.tensor([0]), log_priors)
        self.assertGreater(rare.item(), common.item())

    def test_ignore_index_skips_corrupted_samples(self):
        log_priors = torch.zeros(5)
        targets = self.targets.clone()
        targets[0] = -1
        ours = logit_adjusted_cross_entropy(self.logits, targets, log_priors, ignore_index=-1)
        expected = F.cross_entropy(self.logits[1:], self.targets[1:])
        self.assertAlmostEqual(ours.item(), expected.item(), places=5)

    def test_gradients_flow(self):
        logits = self.logits.clone().requires_grad_(True)
        logit_adjusted_cross_entropy(logits, self.targets, torch.zeros(5)).backward()
        self.assertIsNotNone(logits.grad)
        self.assertTrue(torch.isfinite(logits.grad).all())


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestLogitAdjustedLossModule(unittest.TestCase):
    def test_module_from_priors(self):
        loss = LogitAdjustedLoss([0.5, 0.25, 0.25], tau=1.0, label_smoothing=0.0)
        logits, targets = torch.randn(4, 3), torch.tensor([0, 1, 2, 0])
        expected = logit_adjusted_cross_entropy(logits, targets, torch.log(torch.tensor([0.5, 0.25, 0.25])))
        self.assertAlmostEqual(loss(logits, targets).item(), expected.item(), places=5)

    def test_priors_move_with_module(self):
        loss = LogitAdjustedLoss([0.5, 0.5])
        self.assertIn("log_priors", dict(loss.named_buffers()))

    def test_zero_prior_does_not_produce_nan(self):
        loss = LogitAdjustedLoss([1.0, 0.0])
        value = loss(torch.zeros(2, 2), torch.tensor([0, 1]))
        self.assertFalse(math.isnan(value.item()))


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestFreezeBatchNorm(unittest.TestCase):
    def test_bn_layers_frozen_and_stats_unchanged(self):
        model = nn.Sequential(nn.Conv2d(3, 4, 3), nn.BatchNorm2d(4), nn.ReLU())
        model.train()
        n = freeze_batchnorm(model)
        self.assertEqual(n, 1)
        bn = model[1]
        self.assertFalse(bn.training)
        self.assertFalse(bn.weight.requires_grad)
        self.assertTrue(model[0].training)  # other layers still train
        before = bn.running_mean.clone()
        model(torch.randn(2, 3, 8, 8) * 10 + 5)
        self.assertTrue(torch.equal(before, bn.running_mean))

    def test_affine_can_stay_trainable(self):
        model = nn.Sequential(nn.BatchNorm2d(2))
        freeze_batchnorm(model, freeze_affine=False)
        self.assertTrue(model[0].weight.requires_grad)
        self.assertFalse(model[0].training)


if __name__ == "__main__":
    unittest.main()
