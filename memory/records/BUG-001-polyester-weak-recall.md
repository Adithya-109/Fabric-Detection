# Bug Record: BUG-001 — Chronic Weak Recall on Polyester & Smooth Fabrics

- **ID**: BUG-001
- **Title**: Chronic low recall on Polyester and smooth synthetic classes triggering policy stops
- **TASK IDs**: TASK-001
- **Status**: open
- **Created**: 2026-10-10 10:00:00
- **Updated**: 2026-10-14 04:50 (+05:30)

---

## 1. Problem Description & Impact
- **Symptom**: Polyester recall (and Cotton recall) consistently fail to reach the 20% autonomous policy-stop threshold, causing `worst_recall_below_0_20_after_min_epoch` to abort training runs after epoch 20.
- **Expected Behavior**: Worst single-class recall should exceed >= 40% (0.40) to meet project done criteria; interim target is > 20% to stop triggering early abort.
- **Actual Behavior**: Strongly textured fabrics (Corduroy, Suede, Linen) dominate predictions (>70-85% recall), while smooth woven synthetics (Polyester, Cotton) are heavily confused with each other and under-predicted.
- **Affected Area**: Loss function, class balancing, feature representation in patch crops.
- **Impact & Severity**: High / Blocking. Directly prevents any training run from passing the completion criteria or running past epoch 20.

## 2. Environment & Reproduction
- **Reproduction Steps**:
  1. Train model on dataset containing 14 classes including expanded iMaterialist data (232k images).
  2. Evaluate validation recall per class at each epoch end.
  3. Observe Polyester recall and Cotton recall are the two lowest-performing classes, oscillating below 20%.
- **Inputs & Configuration**: 14-class classifier, 7 random square crops per garment, EfficientNet-B0 backbone.
- **Environment & Version**: PyTorch, EfficientNet-B0, conda `myenv`.
- **Original Evidence References**:
  - Error/Log/Source Path: `backend/fabric_classifier/training/epoch_progress.jsonl` (all attempt epochs)
  - `backend/fabric_classifier/training/training_log.json` (Attempts 305-308 final metrics)
  - Verification Date: 2026-10-13

## 3. Investigation & Attempts

### Progress Trajectory (Worst-Class Recall by Attempt):
| Attempt | Stop Epoch | Worst Recall | Class |
|---|---|---|---|
| 305 | 20 | 2.68% | Polyester |
| 306 | 20 | 7.01% | Polyester |
| 307 | 20 | 10.30% | Polyester |
| 308 | 20 | 12.67% | Polyester |
| 309 (persisted; policy stop) | 20 | 17.55% (final_metrics_achieved; split unverified); val Ep 20 15.44% | Polyester |
| 310 (interrupted, EXP-310) | killed after Ep 5 | val worst recall 9.6-14.0% (no gain) | not recorded |

> **Update 2026-10-14**: The earlier ~+5%-per-attempt improvement trend did not continue into Attempt 310 (verified in `epoch_progress.jsonl`). Further unchanged warm-start retries are unlikely to clear the 20% stop. Note also that the "Lack of training data" hypothesis is already ruled out below; an earlier chat suggestion of adding more Cotton/Polyester data should be treated as low priority until label quality is checked (unverified).

### Attempts Made & Linked Records:
- Attempt 15–22 (legacy cap): Polyester recall was 15–37% on smaller balanced sets; class was manageable with fewer Cotton images.
- Attempt 304–305: Uncapped 41k Polyester + 76k Cotton images from iMaterialist; recall dropped to 2.65% due to catastrophic class confusion between plain-weave Polyester and plain-weave Cotton.
- Attempts 306–309: Each warm-start continuation improves worst recall incrementally (~5% per attempt). Epoch 13 of Attempt 309 reached Val Macro-F1 = 40.37% and worst recall 17.14%.
- Linked records: [EXP-304](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-304-expanded-dataset.md), [EXP-305](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-305-expanded-dataset-20ep.md), [EXP-306](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-306-expanded-dataset-in-flight.md), [EXP-307](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-307-expanded-dataset.md), [EXP-308](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-308-expanded-dataset-in-flight.md), [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md).

### Ruled-Out Hypotheses & Evidence:
- **Lack of training data**: Ruled out — Polyester has 41,534 images (2nd highest in dataset), Cotton has 76,291 (largest).
- **Overall model quality**: Ruled out — 12/14 classes now exceed 40% recall; only Cotton and Polyester lag.

> **Update 2026-10-24 (root cause, evidence-based)**: Precision derived from Attempt 309's stored recall/F1 shows Cotton precision 0.90 (recall 0.18) and Corduroy precision 0.04 (recall 0.84). The model *can* recognise Cotton but almost never predicts it. Cause: double balancing in `train.py` — inverse-frequency `WeightedRandomSampler` **plus** inverse-frequency CE class weights ⇒ effective learned prior ∝ 1/count, while val/test keep the natural distribution (~35% Cotton, ~19% Polyester). This is prior shift, not missing features. **Focal loss / up-weighting would worsen it; deprioritised.** Fix path: post-hoc prior correction on existing weights (`training/prior_sweep.py`, no training), then retrain with `SAMPLER_POWER=0.5` + `LOSS="logit_adjusted"`. See `docs/IMPROVEMENT_PLAN.md` §2.

### Active Hypothesis:
- Plain-weave synthetic fabrics (Polyester, Cotton) share macro-level visual patterns (smooth texture, similar sheen) that 7-patch square crops cannot distinguish without fabric composition information (thread count, sheen gradient).
- The model's patch crops do not capture enough discriminative signal; focal loss or class-weighted cross-entropy may improve minority recall within these two classes.

### Unexplored Mitigations (prioritized for next session):
1. **Class-weighted focal loss**: Increase the effective training weight of Polyester and Cotton during loss computation to penalize their misclassification more heavily. [Priority: High]
2. **Hard negative mining**: Add a sampler that over-samples Cotton/Polyester training examples from the most confused pairs.
3. **Label smoothing adjustment**: Reduce label smoothing specifically for Cotton/Polyester to avoid confidence suppression.
4. **Patch scale variation**: Vary the patch size range to capture both micro-texture and sheen effects simultaneously.

## 4. Workaround & Next Diagnostic
- **Workaround**: Autonomous retry with warm-start is the current approach. Each attempt incrementally improves worst-class recall (~5% per 20-epoch run). At this rate, ~2-3 more attempts (310, 311) may naturally clear the 20% threshold.
- **Alternative Path**: Implement class-weighted focal loss in `train.py` before the next attempt if natural retry does not clear 20% in Attempt 310 by epoch 10.
- **Conditions for Revisiting with focal loss**: If Attempt 310 best epoch worst recall remains below 20% after 10 epochs.

## 5. Resolution & Verification
- **Resolution Summary**: Not resolved. Worst recall reached 17.14% (Ep 13 of interrupted Attempt 309) — below the 20% policy stop threshold and well below the 40% done criterion.
- **Resolution Verification**: Not yet verified.
- **Verification Evidence**: None (unmet criteria).
- **Evidence Status for Consequential Claims**:
  - Polyester/Cotton recall is primary bottleneck: **verified** (training_log.json Attempts 305-308, epoch_progress.jsonl Attempt 309)
  - Worst recall is improving ~5%/attempt via warm-start: **verified** (2.68% → 7.01% → 10.30% → 12.67% → 17.14%)
  - Smooth fabrics lack distinctive patch texture: **hypothesis** (unverified)
  - Focal loss would improve recall: **hypothesis** (not yet tried)
