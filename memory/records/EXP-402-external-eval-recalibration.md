# Experiment Record: EXP-402 — Recalibration tested on an external garment-photo dataset

- **ID**: EXP-402
- **Title**: Current weights + post-hoc prior correction/temperature on never-seen e-commerce photos
- **TASK IDs**: TASK-002, TASK-003
- **Status**: completed (hypothesis not supported on this data)
- **Created**: 2026-10-24 22:15
- **Updated**: 2026-10-24 22:15

---

## 1. Objective & Hypothesis
- **Question**: With no access to DATASETS/, does recalibration (EXP-401 method) improve the current model on independent garment photos?
- **Hypothesis**: Prior correction raises Top-1 and macro-F1 without retraining.

## 2. Configuration
- **Weights**: `fabric_clf_best.pt` = Attempt 310 (sha1 prefix c8fa0616751bed94).
- **Data**: HF `0x-Jayveersinh-Raj/fabric_classification_dataset` (12,984 Indian e-commerce photos, models in studio). 8,166 kept with unambiguous single-material labels (blends, viscose, georgette, net etc. dropped). Near-duplicate-aware halves: calib 5,235 (settings chosen here), eval 2,931 (reported). No Knitted images; Corduroy/Suede/Velvet < 20 each.
- **Run**: GitHub Actions workflow `external-eval` (CPU), commit e7f4cdf; results on branch `results/external-eval`.
- **Variants**: A = target priors from iMaterialist counts (shippable); B = priors from calib half (smoothed, upper bound).

## 3. Results (eval half, 2,931 images)
| | Before | After A | After B |
|---|---|---|---|
| Top-1 | 1.2% | 68.9% | 68.9% |
| Top-3 | 2.9% | 94.0% | 94.8% |
| Macro-F1 | 3.1% | 6.3% | 6.3% |
| Balanced accuracy | 21.9% | 7.7% | 7.7% |

- "After" Top-1 equals the Cotton share of the eval half (68.9%): the correction makes the model predict Cotton for everything. Not a real improvement.
- Fitted temperature hit the upper bound (10) → logits carry very little information on this data.
- Diagnostics from cached logits: model predicts Corduroy for ~40% of images; true class median rank 10–12 of 14 (worse than random ≈ 7); Cotton-vs-Polyester AUC 0.57–0.58 (chance = 0.5).

## 4. Interpretation
- On these photos the existing model has almost no usable signal, so post-hoc correction cannot help. The prior inversion (∝ 1/count) is visible (Corduroy dominates predictions) but fixing it only exposes the lack of signal.
- Leading hypothesis (unverified): patch extraction treats grey studio backdrops and skin as "fabric" (only near-white is masked), so patches often miss the garment. Supports Phase 7 (garment segmentation) and retraining.
- Caveats: labels come from product listings (some noise); domain differs from training (Indian e-commerce vs iMaterialist/TextileNet); the aHash grouping produced uneven halves for Polyester (2,213 calib vs 728 eval), suggesting 8×8 hashes over-group studio photos.
- EXP-401 on iMaterialist val/test (in-domain) is still worth running when data is available; this result does not predict it.

## 5. Next
- Cheap diagnostic (no training): compare patch strategies on the eval half — legacy, whole image, centre region, clothes-segmentation mask — to test the backdrop hypothesis.
