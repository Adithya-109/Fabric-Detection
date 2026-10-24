# Experiment Record: EXP-404 — Frozen-backbone probe on external photos (no fine-tuning)

- **ID**: EXP-404
- **Status**: completed
- **Created**: 2026-10-25
- **Tool / workflow**: `tools/backbone_probe.py`, `.github/workflows/backbone-probe.yml`; results branch `results/backbone-probe` (run on `probe/step1-2`)

## Question
Is EfficientNet-B0 the limit, or is it the training data? Frozen embeddings + a linear head trained on the external "calib" half (1,254 photos, ≤300/class), scored on the same 483 "eval" photos (≤150/class) as EXP-402/403.

## Result (balanced accuracy; current app model 32.5%)
| Model | Method | Balanced acc | Macro-F1 | Top-3 | Cotton↔Poly AUC | Δ vs current [95% CI] |
|---|---|---|---|---|---|---|
| current_app_model | existing weights (legacy_512, prior-fixed) | 32.5% | 21.1% | 66.3% | 0.630 | – |
| clip_b16 | linear head | 58.5% | 42.6% | 86.1% | 0.808 | +26.0 pts [+18.7, +33.4] |
| clip_b16 | zero-shot prompts | 43.7% | 25.0% | 63.6% | 0.577 | +11.3 pts [+3.1, +19.8] |
| dinov2_small | linear head | 58.0% | 44.1% | 86.1% | 0.806 | +25.6 pts [+15.5, +35.9] |
| dinov2_base | linear head | 55.5% | 46.8% | 88.0% | 0.831 | +23.0 pts [+14.3, +32.0] |
| our_b0_features | linear head | 50.5% | 31.6% | 72.0% | 0.762 | +18.0 pts [+11.0, +25.2] |
| imagenet_b0 | linear head | 47.4% | 42.6% | 85.3% | 0.742 | +14.9 pts [+6.3, +23.6] |

Paired bootstrap (95% CI, pts): DINOv2-S vs ImageNet-B0 +10.7 [+4.2,+17.5]; DINOv2-S vs our-B0 features +7.6 [−4.0,+19.3]; CLIP linear vs DINOv2-S +0.5 [−8.5,+9.0]; CLIP linear vs our-B0 features +8.0 [−0.3,+16.1]; CLIP linear vs ImageNet-B0 +11.1 [+3.3,+19.3].

## Findings
1. Data dominates: even ImageNet B0 + a head trained on ~1.2k everyday photos gains +15 pts over the shipped model.
2. A stronger backbone adds ~8–11 pts on top (DINOv2-S/B, CLIP B/16 ≈ 55–58%, statistically tied with each other). Versus the shipped B0's own features the gap is ~8 pts but not significant at this sample size.
3. CLIP zero-shot (no training photos) 43.7% — beats the shipped model by +11 pts but is weaker than any trained head.
4. Weak classes remain: Cotton ~25–29%, Corduroy 0–33%, Velvet/Satin ~40–60%; Cotton↔Polyester AUC ≤ 0.83. Label noise in the external set limits the ceiling.
5. Caveat: heads were trained in-domain (same dataset), so this is an upper-ish bound for frozen features, not a like-for-like model comparison.

## Decision input
Backbone decision reopened: run a proper fine-tune comparison (B0 vs DINOv2-S/CLIP B/16) in Colab on the same data before committing. Interim option: ship a frozen-DINOv2-S + head to the app (CPU-feasible, ~58% on external photos).
