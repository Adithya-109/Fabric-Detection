# Experiment Record: EXP-307 — Multi-Attempt Warm Start Run (Completed)

- **ID**: EXP-307
- **Title**: Autonomous retry warm-started from Attempt 306 on 232k dataset
- **TASK IDs**: TASK-001
- **Status**: completed
- **Created**: 2026-10-12 02:40:00
- **Updated**: 2026-10-12 12:35:00

---

## 1. Objective & Hypothesis
- **Question**: Can a secondary warm-start retry push Top-1 above 35% and drive Polyester recall toward 10–20%?
- **Hypothesis**: Successive fine-tuning rounds allow the head and backbone to progressively separate the massive Cotton vs Polyester distribution.
- **Rationale**: Attempt 306 showed positive upward momentum in Polyester recall and macro-F1.
- **Related Attempts**: [EXP-306](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-306-expanded-dataset-in-flight.md)
- **Reason for Repeat**: Autonomous continuation triggered by Attempt 306 policy stop.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py`
- **Data Version**: 232,330 images
- **Environment**: PID 31100 + 8 worker processes, RTX 3050 6GB GPU, conda `myenv`
- **Inputs & Seeds**: Dynamic DataLoader workers (`NUM_WORKERS = 8`), `pin_memory = True`, batch size 32, FP16
- **Baseline**: Attempt 306 (Final Top-1: 33.69%, Top-3: 58.50%, Macro-F1: 33.17%, Worst Recall: 4.88%)
- **Planned Changes**: Warm start from Attempt 306 best weights with adjusted learning rate schedule
- **Success Criteria**: Top-1 >= 0.72, Top-3 >= 0.90, Macro-F1 >= 0.68, Worst Recall >= 0.40
- **Stopping Condition**: Autonomous policy stop (`worst_recall_below_0_20_after_min_epoch` at Epoch 20)

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```powershell
  conda activate myenv; python -u backend/fabric_classifier/training/train.py
  ```
- **Affected Files**: `backend/fabric_classifier/weights/fabric_clf_best.pt`, `backend/fabric_classifier/weights/fabric_clf_last.pt`
- **Execution State**: completed (stopped at epoch 20 by policy)

## 4. Observed Results & Evidence
- **Final Metrics Achieved**:
  - Final Test Loss: 4.2136
  - Final Top-1 Accuracy: **35.59%** (+1.90% over Attempt 306; +4.45% over Attempt 305)
  - Final Top-3 Accuracy: **61.07%** (+2.57% over Attempt 306; +5.51% over Attempt 305)
  - Final Macro-F1: **34.91%** (+1.74% over Attempt 306; +3.66% over Attempt 305)
  - Final Worst-Class Recall: **8.44%** (Polyester; peaked at **10.30%** in validation at Epoch 20!)
  - Stop Rule Trigger: `worst_recall_below_0_20_after_min_epoch` at Epoch 20 (Polyester at 10.30% < 20%)
- **Per-Class Breakdown**:
  - Corduroy: **87.5%**, Suede: **84.0%**, Linen: **82.0%**, Satin: **74.2%**, Wool: **65.2%**, Leather: **62.3%**, Silk: **56.7%** (F1: 60.3%), Velvet: **54.7%**, Nylon: **50.7%**, Fleece: **46.2%**, Knitted: **35.8%**, Denim: **30.2%**, Cotton: **15.9%**, Polyester: **8.44%** (F1: 0.1466, up from 0.0508 in Att 305)
- **Original Evidence References**:
  - Artifact / Log Path: `backend/fabric_classifier/training/training_log.json` (Attempt 307 entry)
  - Verification Date: 2026-10-12

## 5. Interpretation & Next Action
- **Interpretation**: Significant steady progression across all fabric classes. Polyester recall has tripled across attempts (2.65% in 305 -> 4.88% in 306 -> 8.44% in 307, with validation hitting 10.30%). Overall Macro-F1 reached ~35%, and Top-3 passed 61%. Auto-retry launched Attempt 308.
- **Related Records**: [EXP-306](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-306-expanded-dataset-in-flight.md), [EXP-308](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-308-expanded-dataset-in-flight.md), [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md)
