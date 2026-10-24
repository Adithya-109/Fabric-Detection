# Frozen-backbone probe (EXP-404)

1254 training photos (calib half, ≤300/class), 483 test photos (eval half, ≤150/class). Backbones are frozen; only a linear head is trained.

**Balanced accuracy** (mean recall over classes) is the headline number; chance ≈ 7%.

| Model | Method | Balanced acc | Macro-F1 | Top-3 | Cotton↔Poly AUC | Δ vs current [95% CI] |
|---|---|---|---|---|---|---|
| current_app_model | existing weights (legacy_512, prior-fixed) | 32.5% | 21.1% | 66.3% | 0.630 | – |
| clip_b16 | linear head | 58.5% | 42.6% | 86.1% | 0.808 | +26.0 pts [+18.7, +33.4] |
| clip_b16 | zero-shot prompts | 43.7% | 25.0% | 63.6% | 0.577 | +11.3 pts [+3.1, +19.8] |
| dinov2_small | linear head | 58.0% | 44.1% | 86.1% | 0.806 | +25.6 pts [+15.5, +35.9] |
| dinov2_base | linear head | 55.5% | 46.8% | 88.0% | 0.831 | +23.0 pts [+14.3, +32.0] |
| our_b0_features | linear head | 50.5% | 31.6% | 72.0% | 0.762 | +18.0 pts [+11.0, +25.2] |
| imagenet_b0 | linear head | 47.4% | 42.6% | 85.3% | 0.742 | +14.9 pts [+6.3, +23.6] |

## Data efficiency (balanced accuracy vs training photos per class)

| Model | 10 | 50 | 150 |
|---|---|---|---|
| clip_b16 | 45.6% | 56.6% | 59.0% |
| dinov2_small | 45.7% | 59.2% | 59.8% |
| dinov2_base | 49.4% | 59.5% | 55.9% |
| our_b0_features | 45.5% | 46.9% | 49.7% |
| imagenet_b0 | 49.7% | 48.9% | 46.9% |

## Per-class recall — best linear head (clip_b16)

| Class | Recall |
|---|---|
| Cotton | 25.3% |
| Polyester | 49.3% |
| Silk | 81.4% |
| Denim | 71.4% |
| Linen | 60.0% |
| Wool | 63.0% |
| Leather | 60.0% |
| Velvet | 60.0% |
| Corduroy | 0.0% |
| Fleece | 73.9% |
| Nylon | 73.2% |
| Satin | 42.9% |
| Suede | 100.0% |
