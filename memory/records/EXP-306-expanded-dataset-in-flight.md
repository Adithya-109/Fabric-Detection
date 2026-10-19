# Experiment Record: EXP-306 — Warm-Start Expanded Dataset Run (Completed)

- **ID**: EXP-306
- **Title**: Autonomous retry warm-started from Attempt 305 best weights on 232k dataset
- **TASK IDs**: TASK-001
- **Status**: completed
- **Created**: 2026-10-11 15:40:00
- **Updated**: 2026-10-12 02:30:00

---

## 1. Objective & Hypothesis
- **Question**: Can fine-tuning / continuing training from Attempt 305 best weights drive training loss below 1.10 and elevate worst-class recall above 8% towards the 20% policy threshold?
- **Hypothesis**: Warm-starting allows faster feature discrimination for lagging classes without destabilizing high-performing textured fabrics.
- **Rationale**: Attempt 305 reached epoch 20 with steady downward loss gradient; auto-retry controller initiated Attempt 306.
- **Related Attempts**: [EXP-305](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-305-expanded-dataset-20ep.md)
- **Reason for Repeat**: Autonomous continuation after policy stop.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py`
- **Data Version**: 232,330 images
- **Environment**: PID 31100 + 8 worker processes, RTX 3050 6GB GPU, conda `myenv`
- **Inputs & Seeds**: Dynamic DataLoader workers (`NUM_WORKERS = 8`), `pin_memory = True`, batch size 32, FP16
- **Baseline**: Attempt 305 (Best Val Top-1: 31.68%, Macro-F1: 31.76%, Worst Recall: 2.68%)
- **Planned Changes**: Warm start from best checkpoint `fabric_clf_best.pt`
- **Success Criteria**: Top-1 >= 0.72, Top-3 >= 0.90, Macro-F1 >= 0.68, Worst Recall >= 0.40
- **Stopping Condition**: Autonomous policy stop, early stopping (`PATIENCE = 10`), or epoch ceiling (`EPOCHS_MAX = 60`)

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```powershell
  conda activate myenv; python -u backend/fabric_classifier/training/train.py
  ```
- **Affected Files**: `backend/fabric_classifier/weights/fabric_clf_best.pt`, `backend/fabric_classifier/weights/fabric_clf_last.pt`, `backend/fabric_classifier/training/epoch_progress.jsonl`
- **Execution State**: completed (stopped at epoch 20 by policy)

## 4. Observed Results & Evidence
- **Final Metrics Achieved**:
  - Final Test Loss: 4.1946
  - Final Top-1 Accuracy: **33.69%** (vs 31.14% in Attempt 305)
  - Final Top-3 Accuracy: **58.50%** (vs 55.56% in Attempt 305)
  - Final Macro-F1: **33.17%** (vs 31.25% in Attempt 305)
  - Final Worst-Class Recall: **4.88%** (Polyester; peaked at 8.11% in Epoch 6, 7.01% in Epoch 20)
  - Stop Rule Trigger: `worst_recall_below_0_20_after_min_epoch` at Epoch 20
- **Per-Class Breakdown**:
  - Corduroy: 85.2%, Suede: 80.0%, Linen: 77.0%, Wool: 65.4%, Satin: 65.7%, Velvet: 58.8%, Leather: 57.0%, Nylon: 52.5%, Fleece: 45.0%, Silk: 41.9%, Denim: 40.8%, Knitted: 34.9%, Cotton: 12.2%, Polyester: 4.88%
- **Original Evidence References**:
  - Artifact / Log Path: `backend/fabric_classifier/training/training_log.json` (Attempt 306 entry)
  - Verification Date: 2026-10-12

## 5. Interpretation & Next Action
- **Interpretation**: Attempt 306 made solid progress across all metrics (+2.55% Top-1, +1.92% Macro-F1, Polyester recall doubled from 2.65% to 4.88%), but remained below the 20% threshold, triggering auto-retry into Attempt 307.
- **Related Records**: [EXP-307](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-307-expanded-dataset.md), [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md)
