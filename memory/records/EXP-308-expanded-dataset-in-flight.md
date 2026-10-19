# Experiment Record: EXP-308 — Multi-Attempt Warm Start Run (Completed)

- **ID**: EXP-308
- **Title**: Autonomous retry warm-started from Attempt 307 on 232k dataset
- **TASK IDs**: TASK-001
- **Status**: completed
- **Created**: 2026-10-12 12:45:00
- **Updated**: 2026-10-13 00:55:00

---

## 1. Objective & Hypothesis
- **Question**: Can Attempt 308 sustain training loss reduction below 0.95 and push Top-1 past 36% while continuing to elevate Polyester recall?
- **Hypothesis**: Continued fine-tuning with warm-started weights refines decision boundaries for the most confusing classes without losing texture discrimination.
- **Rationale**: Attempt 307 achieved project-high metrics and demonstrated steady upward climb in Polyester recall (10.30%).
- **Related Attempts**: [EXP-307](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-307-expanded-dataset.md)
- **Reason for Repeat**: Autonomous continuation after Attempt 307 policy stop.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py`
- **Data Version**: 232,330 images
- **Environment**: PID 31100 + 8 worker processes, RTX 3050 6GB GPU, conda `myenv`
- **Inputs & Seeds**: Dynamic DataLoader workers (`NUM_WORKERS = 8`), `pin_memory = True`, batch size 32, FP16
- **Baseline**: Attempt 307 (Final Top-1: 35.59%, Top-3: 61.07%, Macro-F1: 34.91%, Worst Recall: 8.44%)
- **Planned Changes**: Warm start from Attempt 307 weights
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
  - Final Test Loss: **3.3810** (lowest test loss in project history)
  - Final Top-1 Accuracy: **38.97%** (+3.38% over Attempt 307; +7.83% over Attempt 305; val peaked at **39.95%** in Ep 20)
  - Final Top-3 Accuracy: **65.44%** (+4.37% over Attempt 307; +9.88% over Attempt 305; val peaked at **65.60%** in Ep 17)
  - Final Macro-F1: **37.87%** (+2.96% over Attempt 307; +6.62% over Attempt 305; val peaked at **38.19%** in Ep 17)
  - Final Worst-Class Recall: **12.67%** (Polyester; up from 8.44% in 307, 4.88% in 306, 2.65% in 305!)
  - Stop Rule Trigger: `worst_recall_below_0_20_after_min_epoch` at Epoch 20 (Polyester at 12.67% < 20%)
- **Per-Class Recall Breakdown**:
  - Corduroy: **85.2%**, Suede: **84.0%**, Linen: **78.3%**, Satin: **76.5%**, Leather: **64.3%**, Velvet: **62.7%**, Wool: **62.4%**, Nylon: **56.6%**, Fleece: **50.5%**, Silk: **44.5%**, Knitted: **43.7%**, Denim: **41.5%**, Cotton: **20.0%** (F1: 32.6%), Polyester: **12.7%** (F1: 0.2096, up from 0.0508)
  - **Milestone**: **12 out of 14 classes now exceed the 40% recall done target!** Only Cotton (20.0%) and Polyester (12.7%) remain below 40%.
- **Original Evidence References**:
  - Artifact / Log Path: `backend/fabric_classifier/training/training_log.json` (Attempt 308 entry)
  - Weights Path: `backend/fabric_classifier/weights/fabric_clf_best.pt` (saved from Epoch 17)
  - Verification Date: 2026-10-13

## 5. Interpretation & Next Action
- **Interpretation**: Attempt 308 delivered major across-the-board gains. Polyester recall nearly quintupled (2.65% -> 12.67%), and Top-1 accuracy approached 39-40%. 12 classes are now passing their recall threshold. Autonomous retry launched Attempt 309 from best weights.
- **Related Records**: [EXP-307](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-307-expanded-dataset.md), [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md), [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md)
