# Experiment Record: EXP-310 — Warm-Start Continuation from Attempt 309 (Interrupted)

- **ID**: EXP-310
- **Title**: Attempt 310 warm-started after Attempt 309 policy stop — interrupted after Epoch 5 evaluation
- **TASK IDs**: TASK-001, TASK-003
- **Status**: interrupted
- **Created**: 2026-10-14 04:50:00
- **Updated**: 2026-10-14 04:50:00

---

## 1. Objective & Hypothesis
- **Question**: Does another unmodified warm-start continuation lift worst-class recall past 20% and Macro-F1 past Attempt 309's 40.37%?
- **Hypothesis**: Continuing the ~+5%-per-attempt worst-recall trend seen in 305–309 would clear the 20% policy stop. (Recorded retrospectively; this was the plan in `memory/experiments.md`, not a separately designed experiment.)
- **Rationale**: Autonomous retry in `train.py` after the Attempt 309 policy stop.
- **Related Attempts**: [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md), [EXP-308](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-308-expanded-dataset-in-flight.md)
- **Reason for Repeat**: Autonomous retry policy; no code or data change versus 309 (unverified: the hyperparameter dict for 310 was not persisted because the attempt was not finalized).

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py` (same as EXP-309; no edits recorded)
- **Data Version**: 232,330 images plus merged curated-manifest paths (as in EXP-309)
- **Environment**: RTX 3050 6GB, conda `myenv`, 8 DataLoader workers, FP16
- **Baseline**: Attempt 309 (epochs 19/20 val Macro-F1 37.86% / 39.51%; best 40.37% at Ep 13)
- **Planned Changes**: None (plain warm-start continuation)
- **Success Criteria**: Top-1 >= 0.72, Top-3 >= 0.90, Macro-F1 >= 0.68, Worst Recall >= 0.40
- **Stopping Condition**: Policy stop (worst recall < 0.20 after Epoch 20), early stopping, or 20 epochs

## 3. Procedure & Execution
- **Exact Commands / Procedure**: Started automatically by the trainer's retry loop after Attempt 309 stopped (launched via `conda activate myenv; python -u backend/fabric_classifier/training/train.py`, 2026-10-13 ~17:38 +05:30).
- **Affected Files**: `backend/fabric_classifier/weights/fabric_clf_best.pt` (last write 2026-10-13 20:56), `fabric_clf_last.pt` (last write 2026-10-14 00:39), `backend/fabric_classifier/training/epoch_progress.jsonl` (last write 2026-10-14 01:53)
- **Execution State**: **INTERRUPTED** by a server restart (system notice 2026-10-13T23:11Z). Epoch 6 reached step 58,000 (of 58,083) but its validation was not logged. No `train.py` process was found at 2026-10-14 04:42 and 04:46.
- **Check actual state**: `Get-CimInstance Win32_Process | ? {$_.CommandLine -match 'train.py'}` and `Get-Content backend/fabric_classifier/training/epoch_progress.jsonl -Tail 3`.

## 4. Observed Results & Evidence
- **Observed Results & Measurements** (validation, from `epoch_progress.jsonl`):

  | Epoch | Train Loss | Val Top-1 | Val Top-3 | Val Macro-F1 | Val Worst Recall |
  |---|---|---|---|---|---|
  | 1 | 0.8371 | 38.65% | 64.52% | 37.54% | 14.00% |
  | 2 | 0.8296 | 36.51% | 63.75% | 36.12% | 12.76% |
  | 3 | 0.8351 | 38.81% | 64.60% | 37.50% | 9.56% |
  | 4 | 0.9020 | 34.00% | 58.85% | 34.95% | 10.32% |
  | 5 | 0.9155 | 36.65% | 60.67% | 36.19% | 10.93% |
  | 6 | running train loss 0.9178 at step 58,000; validation NOT recorded | — | — | — | — |

  - Resource Usage: ~23 it/s observed in the console log; VRAM not recorded.
- **Hypothesis Outcome**: not supported so far (5 epochs, no gain over 309; incomplete run, so inconclusive for the full 20 epochs).
- **Original Evidence References**:
  - Artifact / Log Path: `backend/fabric_classifier/training/epoch_progress.jsonl`
  - Not in `training_log.json` (last entry is Attempt 309).
  - Verification Date: 2026-10-14
- **Evidence Status for Consequential Claims**:
  - Epoch 1–5 metrics: verified (read from jsonl 2026-10-14).
  - Train loss rose from ~0.83 to ~0.90–0.92 at Epoch 4: verified; cause NOT investigated (unverified hypothesis: head-only/unfreeze schedule change at `HEAD_ONLY_EPOCHS = 3`, as the config prints 3 head-only epochs — not checked).
  - Which checkpoint `best.pt` / `last.pt` contain: unverified.

## 5. Interpretation & Next Action
- **Interpretation**: Plain warm-start retries stopped paying off: Attempt 310's validation sits below 309's peak and worst recall (9.6–14.0%) did not improve on 309.
- **Limitations & Uncertainty**: Only 5 evaluated epochs; validation is very noisy epoch to epoch (±3–5 points Top-1); a loss spike coincides with Epoch 4.
- **Related Records**: [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md), [BUG-006 in buglog](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/buglog.md) (server restart), [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md)
- **Next Action / Retry Condition**: Do NOT relaunch unchanged. User instruction (2026-10-14): do not start anything without asking. Before any retry, change one thing (see BUG-001 mitigation list: class-weighted focal loss first) and create a new `planned` EXP record.
