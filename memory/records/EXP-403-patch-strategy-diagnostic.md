# Experiment Record: EXP-403 — Patch-placement strategies on external garment photos (no training)

- **ID**: EXP-403
- **Title**: Where should the 7 patches come from? Legacy vs 512-px resize vs centre vs garment segmentation vs whole image
- **TASK IDs**: TASK-003
- **Status**: completed
- **Created**: 2026-10-24 23:10
- **Updated**: 2026-10-24 23:10

---

## 1. Question & Hypothesis
- **Question**: EXP-402 showed almost no signal on external photos. Is that because patches miss the garment (grey studio backdrops/skin count as "fabric")?
- **Hypothesis**: Patches restricted to the garment (clothes segmentation) score clearly higher with the same weights.

## 2. Configuration
- **Weights**: `fabric_clf_best.pt` (Attempt 310).
- **Data**: eval half of the external HF dataset (see EXP-402), capped at 150 images/class → 483 images, 13 classes (no Knitted; Corduroy 3, Suede 2, Leather/Velvet 5, Denim/Satin 7).
- **Variants**: legacy_orig (current app), legacy_512 (resize to max side 512 first), centre_512, garment_512 (`mattmdjaga/segformer_b2_clothes`, largest clothing class, min coverage 0.9, shrink-to-fit), whole image.
- **Metrics**: after undoing the training-prior inversion (train prior ∝ 1/count → uniform; no tuning on this data). Stratified bootstrap (2,000×) for differences.
- **Runs**: GitHub Actions `patch-diagnostic`; run 1 (commit on `diag/patches-1`) had a garment-variant bug (narrow garments fell back to the whole photo); fixed with `relax_if_needed` and rerun on `diag/patches-2`. Results on branch `results/patch-diagnostic`.

## 3. Results (run 2)
| Variant | Balanced acc. | Macro-F1 | Top-3 | Cotton-vs-Poly AUC |
|---|---|---|---|---|
| legacy_orig (today) | 21.6% | 13.0% | 54.9% | 0.606 |
| **legacy_512** | **32.5%** | **21.1%** | **66.3%** | 0.630 |
| centre_512 | 25.3% | 17.5% | 57.1% | 0.614 |
| garment_512 | 29.7% | 18.8% | 61.7% | 0.595 |
| whole | 25.9% | 17.1% | 60.5% | 0.661 |

Chance ≈ 7.7%. Bootstrap differences in balanced accuracy:
- legacy_512 − legacy_orig: **+10.6 pts (95% CI +2.6 to +18.8)** → real.
- garment_512 − legacy_orig: +8.2 (−1.9 to +18.7) → not conclusive.
- legacy_512 − garment_512: +2.7 (−3.8 to +9.0) → no detectable difference.

Visual check (`patch_examples.jpg`): legacy_orig patches mostly land on backdrop/skin (hypothesis confirmed visually); segmentation masks are accurate; after the fix, garment patches sit on the garment.

## 4. Interpretation
- **Image scale is the biggest single factor.** Training images were ≤ 512 px (iMaterialist preprocessing), so a fixed 160-px patch on a large photo shows a zoom level the model never saw. Resizing to 512 before patching fixes most of it — no retraining needed.
- **Putting patches on the garment did not help this model on its own.** Likely because the model was trained on legacy patches (up to 50% background, mixed context); clean garment-only patches are themselves a distribution shift. Segmentation should be judged after training with it (Phase 7), not by swapping it in at inference.
- Even the best variant is weak (≈ 1 in 3 correct; Cotton recall 13–29%). Retraining remains necessary. Label noise is visible in the samples (e.g. a leather jacket labelled Fleece).

## 5. Next
- Candidate immediate app change: resize inputs to max side 512 before patch extraction (needs user decision; no-op for iMaterialist-sized images, effect on close-up photos untested).
- Keep segmentation for Phase 7 as a *training-time* change.
