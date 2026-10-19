# Experiment Record: EXP-305 — 20-Epoch Expanded Dataset Run

- **ID**: EXP-305
- **Title**: Multi-epoch training on expanded dataset with dynamic 8-worker acceleration
- **TASK IDs**: TASK-001
- **Status**: completed
- **Created**: 2026-10-10 20:30:00
- **Updated**: 2026-10-11 15:38:00

---

## 1. Objective & Hypothesis
- **Question**: Will sustained multi-epoch training (20 epochs) with dynamic background workers allow the EfficientNet-B0 backbone to converge on the 232k image dataset?
- **Hypothesis**: Loss will steadily decrease and validation metrics will rebound from the 28% trough.
- **Rationale**: Attempt 304 stopped early at 13 epochs before loss plateaued. Dynamic CPU workers (`NUM_WORKERS = 8`) and pinned memory cut epoch time to ~32 min.
- **Related Attempts**: [EXP-304](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-304-expanded-dataset.md)
- **Reason for Repeat**: Longer horizon needed to observe loss curve and evaluate policy stop triggers.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py`
- **Data Version**: 232,330 images (TextileNet, Microscope, iBUG, iMaterialist)
- **Environment**: RTX 3050 6GB GPU (~58°C, ~34W, ~964 MB VRAM in train mode), 8 CPU workers (`pin_memory = True`)
- **Inputs & Seeds**: Batch size 32, FP16, AdamW, dynamic resource manager enabled
- **Baseline**: [EXP-304](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-304-expanded-dataset.md) (Top-1: 0.2866, Macro-F1: 0.2883)
- **Planned Changes**: 20 full epochs targeted; 8 CPU DataLoader workers enabled
- **Success Criteria**: Top-1 >= 0.72, Top-3 >= 0.90, Macro-F1 >= 0.68, Worst Recall >= 0.40
- **Stopping Condition**: Policy stop `worst_recall_below_0_20_after_min_epoch` or plateau window

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```powershell
  conda activate myenv; python -u backend/fabric_classifier/training/train.py
  ```
- **Affected Files**: `backend/fabric_classifier/training/train.py`, `backend/fabric_classifier/weights/fabric_clf_last.pt`
- **Execution State**: completed (stopped at epoch 20 by policy)

## 4. Observed Results & Evidence
- **Observed Results & Measurements**:
  - Total Duration: 69,532 seconds (~19.3 hours)
  - Train Loss: Decreased steadily from 1.3471 to 1.1473
  - Val Loss: Stabilized from 12.11 down to 4.36
  - Val Top-1 Accuracy: 31.68% (Epoch 20)
  - Val Macro F1: 31.76% (Epoch 20)
  - Val Worst-Class Recall: 2.68% (Polyester)
  - Per-Class Breakdown: Corduroy 84.1%, Suede 78.7%, Linen 77.0%, Satin 65.9%, Velvet 57.3%, Wool 56.5%, Leather 53.8%, Silk 46.5%, Knitted 39.1%, Fleece 39.0%, Denim 25.5%, Cotton 12.0%, Polyester 2.65%
  - Stop Reason: `worst_recall_below_0_20_after_min_epoch` triggered by Polyester (2.65% < 20%)
- **Hypothesis Outcome**: partially supported (Loss decreased smoothly, val macro-F1 improved from 28.8% to 31.76%, but policy stop was triggered by chronic weak recall on Polyester)
- **Original Evidence References**:
  - Artifact / Log Path: `backend/fabric_classifier/training/training_log.json`
  - Weights Path: `backend/fabric_classifier/weights/fabric_clf_last.pt` (52,558,899 bytes)
  - Verification Date: 2026-10-11
- **Evidence Status for Consequential Claims**:
  - Training completed 20 epochs without OOM or NaN: verified
  - Policy stop triggered by Polyester recall: verified

## 5. Interpretation & Next Action
- **Interpretation**: Model learns textured fabrics exceptionally well (Corduroy >84%, Suede >78%, Linen 77%), but completely confuses smooth synthetics (Polyester at 2.65%).
- **Limitations & Uncertainty**: Polyester is heavily represented in iMaterialist but lacks distinguishing macro-texture on patch crops.
- **Related Records**: [EXP-304](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-304-expanded-dataset.md), [EXP-306](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-306-expanded-dataset-in-flight.md), [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md)
- **Next Action / Retry Condition**: Auto-retry launched Attempt 306 from best weights to refine convergence.
