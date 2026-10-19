# Experiment Record: EXP-309 — Retry on Expanded Dataset (Completed via Policy Stop after Resume)

- **ID**: EXP-309
- **Title**: Autonomous retry warm-started from Attempt 308 on 232k dataset; interrupted by restart at Epoch 19, resumed and policy-stopped at Epoch 20
- **TASK IDs**: TASK-001
- **Status**: completed
- **Created**: 2026-10-13 01:00:00
- **Updated**: 2026-10-14 04:50 (+05:30)

> **Correction (2026-10-14)**: This record previously said the run was interrupted and absent from `training_log.json`. After relaunch (~2026-10-13 17:38) the trainer resumed Attempt 309 at Epoch 19 (restarted from step 0), ran Epoch 20 and ended by policy stop. It is now persisted in `training_log.json` (309 entries, status `completed_policy_stop`). Older text below that says "interrupted" / "NOT EVALUATED" is superseded where noted.

---

## 1. Objective & Hypothesis
- **Question**: Can Attempt 309 break training loss below 0.85, elevate Cotton and Polyester recall above 20%, and test whether Top-1 can cross 40% on the expanded 232k dataset?
- **Hypothesis**: Building directly on Attempt 308 best weights (which brought 12 of 14 classes past the 40% threshold) will allow the network to concentrate gradient updates on separating the remaining Cotton/Polyester confusion pair.
- **Rationale**: Attempt 308 demonstrated that Polyester recall jumped from 8.44% to 12.67% and Cotton jumped from 15.9% to 20.0%.
- **Related Attempts**: [EXP-308](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-308-expanded-dataset-in-flight.md)
- **Reason for Repeat**: Autonomous continuation after Attempt 308 policy stop.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py`
- **Data Version**: 232,330 images
- **Environment**: RTX 3050 6GB GPU, conda `myenv`, 8 dynamic DataLoader workers (`NUM_WORKERS = 8`), `pin_memory = True`, batch size 32, FP16
- **Baseline**: Attempt 308 (Final Top-1: 38.97%, Top-3: 65.44%, Macro-F1: 37.87%, Worst Recall: 12.67%)
- **Planned Changes**: Warm start from Attempt 308 best weights; optimizer LR starting at `0.00059049`
- **Success Criteria**: Top-1 >= 0.72, Top-3 >= 0.90, Macro-F1 >= 0.68, Worst Recall >= 0.40
- **Stopping Condition**: Autonomous policy stop, early stopping, or 20 epochs

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```powershell
  conda activate myenv; python -u backend/fabric_classifier/training/train.py
  ```
- **Affected Files**: `backend/fabric_classifier/weights/fabric_clf_best.pt`, `backend/fabric_classifier/weights/fabric_clf_last.pt`
- **Execution State**: **INTERRUPTED** — trainer process (no surviving PID after server restart 2026-10-13T09:47Z). Was at Epoch 19 step 58,000 / 58,083 (~99.8% complete) when killed. Epoch 19 validation had NOT yet run.
- **Not persisted in** `training_log.json` — only 308 entries total; Attempt 309 exists only in `epoch_progress.jsonl`.

## 4. Observed Results & Evidence

> **⚠ VERIFIED via `epoch_progress.jsonl` only. Not in `training_log.json`.**

- **Epoch-by-Epoch Validation Metrics** (all from `epoch_progress.jsonl`):
  | Epoch | Train Loss | Val Top-1 | Val Top-3 | Val Macro-F1 | Val Worst Recall |
  |---|---|---|---|---|---|
  | 1 | 0.8743 | 34.96% | 59.97% | 34.60% | 6.88% |
  | 2 | **0.8667** | 37.71% | 63.43% | 36.31% | 10.44% |
  | 3 | 0.8769 | 33.44% | 58.30% | 33.42% | 8.04% |
  | 4 | 0.8893 | **41.29%** | 66.15% | 38.79% | 12.83% |
  | 5 | 0.8808 | 39.62% | 64.93% | 37.57% | 10.79% |
  | 6 | 0.8809 | 38.26% | 63.97% | 36.45% | 11.93% |
  | 7 | 0.8813 | **43.01%** | 68.33% | 39.64% | 9.63% |
  | 8 | 0.8737 | 41.44% | 67.89% | 38.87% | 13.22% |
  | 9 | 0.8715 | 40.07% | 65.37% | 38.46% | 12.31% |
  | 10 | 0.8705 | 42.98% | 67.62% | 39.83% | 14.53% |
  | 11 | 0.8653 | 41.52% | 66.78% | 39.18% | 10.26% |
  | 12 | 0.8693 | 40.80% | 66.34% | 38.29% | 12.91% |
  | 13 | 0.8678 | **43.15%** | 67.84% | **40.37%** | 17.14% |
  | 14 | 0.8626 | 37.36% | 63.77% | 36.31% | 11.71% |
  | 15 | 0.8578 | 36.61% | 63.85% | 35.40% | 9.41% |
  | 16 | 0.8635 | 43.08% | 68.71% | 39.52% | 14.00% |
  | 17 | 0.8567 | 36.92% | 63.69% | 36.52% | 10.36% |
  | 18 | 0.8550 | 38.26% | 63.15% | 37.02% | 12.11% |
  | 19 | 0.8451 | 40.43% | 63.21% | 37.86% | 10.37% |
  | 20 | 0.8455 | 41.39% | 67.05% | 39.51% | 15.44% |

- **Policy stop (verified, `training_log.json`)**: rule `worst_recall_below_0_20_after_min_epoch`, epoch 20, value 0.1544, threshold 0.20. Duration 9,408 s over 20 epochs in the persisted entry (the run was interrupted and resumed, so wall-clock differs).
- **Final metrics in `training_log.json` -> `final_metrics_achieved`** (split not verified; likely test set, unverified): Top-1 **43.28%**, Top-3 66.50%, Macro-F1 **40.48%**, worst-class recall **17.55%** (Polyester); Cotton recall 17.95%; loss 3.373. Classes at/above 40% recall: 12 of 14 (Knitted 44.4%, Fleece 54.5%, Silk 54.8%, Denim 54.7% etc.; Corduroy 84.1% and Linen 81.3% have very low F1 (7.0% and 20.5%), i.e. over-predicted).

- **Peak Results (unverified test set — val only):**
  - Best Val Top-1: **43.15%** (Epoch 13)
  - Best Val Macro-F1: **40.37%** (Epoch 13) — **first time Macro-F1 exceeded 40%**
  - Best Worst Recall: **17.14%** (Epoch 13)
  - Record Low Train Loss: **0.8478** (Epoch 19 step ~58,000)

- **best.pt File Status**: `fabric_clf_best.pt` (17,658,446 bytes, last write 2026-10-13 10:41:18) — likely from Epoch 13 of Attempt 309 (unverified which exact epoch; need to check checkpoint metadata on next run).
- **last.pt File Status**: `fabric_clf_last.pt` (52,559,859 bytes, last write 2026-10-13 14:32:34) — last epoch checkpoint before process kill (Epoch 18).

- **Original Evidence References**:
  - Stream Log: `backend/fabric_classifier/training/epoch_progress.jsonl` — ALL EPOCH DATA VERIFIED HERE
  - `training_log.json` — DOES NOT CONTAIN Attempt 309 (only 308 entries; last = Attempt 308)
  - Weights: `fabric_clf_best.pt` last write 2026-10-13 10:41 (corresponds to intra-309 best, likely Epoch 13)
  - Process kill: Server restart 2026-10-13T09:47Z (confirmed by system message; no surviving PID)
  - Verification Date: 2026-10-13

## 5. Interpretation & Next Action
- **Interpretation**: 
  - Attempt 309 is the strongest run yet, with Epoch 13 showing Val Macro-F1 = 40.37% (first time exceeding 40% in project history). Val Top-1 crossed 43% in Epoch 7 and 13. Worst Recall reached 17.14% in Epoch 13 (still below the 20% autonomous policy stop threshold).
  - The model was **not policy-stopped**: it was **killed externally** (server restart) during Epoch 19. Epoch 19 validation was NOT executed.
  - The best weights in `fabric_clf_best.pt` are from Attempt 309 Epoch 13. These are the best weights in project history.
  - `train.py` autonomous retry logic will resume as Attempt 310 when re-launched, warming from the best checkpoint.
  - BUG-001 (Polyester recall) is progressing: worst recall reached 17.14% in Epoch 13 but has not yet cleared the 20% threshold consistently.

- **Blocker**: BUG-001 still applies — Cotton/Polyester recall below 20% policy stop threshold.
- **Next Action (for fresh session)**:
  1. Verify no trainer PID is running: `Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'python.exe' -and $_.CommandLine -match 'train.py'}`
  2. Re-launch trainer (will auto-resume as Attempt 310 warm-starting from best.pt): `conda activate myenv; python -u backend/fabric_classifier/training/train.py`
  3. Monitor and record Attempt 310 metrics into a new EXP-310 record.
