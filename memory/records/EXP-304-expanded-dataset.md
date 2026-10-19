# Experiment Record: EXP-304 — Expanded Dataset Baseline Run

- **ID**: EXP-304
- **Title**: Initial baseline training run on expanded 232,330 image dataset
- **TASK IDs**: TASK-001
- **Status**: completed
- **Created**: 2026-10-10 12:00:00
- **Updated**: 2026-10-10 20:00:00

---

## 1. Objective & Hypothesis
- **Question**: Can integrating the full iMaterialist dataset (~216k images) alongside TextileNet, Microscope, and iBUG overcome weak class bottlenecks?
- **Hypothesis**: Massive data expansion will increase generalized representation and improve macro-F1 across 14 classes.
- **Rationale**: Prior runs were capped at ~800 images per class and hit a 58% top-1 ceiling.
- **Related Attempts**: Attempt 15, Attempt 22
- **Reason for Repeat**: New expanded dataset available under non-commercial policy.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/train.py`
- **Data Version**: TextileNet + Microscope + iBUG + iMaterialist (232,330 training images)
- **Environment**: RTX 3050 6GB GPU, Windows 11, conda `myenv`, 12-core CPU
- **Inputs & Seeds**: Batch size 32, FP16, AdamW, standard learning rate schedule
- **Baseline**: Attempt 15 (Top-1: 0.582, Macro-F1: 0.583 on legacy ~800/class dataset)
- **Planned Changes**: Full integration of 216k iMaterialist parquet samples
- **Success Criteria**: Top-1 >= 0.72, Macro-F1 >= 0.68, Worst Recall >= 0.40
- **Stopping Condition**: Autonomous policy stop or 20 epochs

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```powershell
  conda activate myenv; python -u backend/fabric_classifier/training/train.py
  ```
- **Affected Files**: `backend/fabric_classifier/training/train.py`, `imaterialist_label_mapping.json`
- **Execution State**: completed (13 epochs executed before completion)

## 4. Observed Results & Evidence
- **Observed Results & Measurements**:
  - Top-1 Accuracy: 0.2866 (test)
  - Top-3 Accuracy: 0.5312 (test)
  - Macro F1: 0.2883 (test)
  - Worst Single-Class Recall: 0.0279 (test)
  - Inference Time: 6.31 ms
  - VRAM: 182.1 MB
- **Hypothesis Outcome**: disproven (Immediate naive expansion dropped top-1 accuracy to ~28.6% due to severe class distribution shift and unadapted training dynamics)
- **Original Evidence References**:
  - Artifact / Log Path: `backend/fabric_classifier/training/training_log.json`
  - Location / Run ID: Attempt 304 entry in `training_log.json`
  - Verification Date: 2026-10-10
- **Evidence Status for Consequential Claims**:
  - Raw data expansion caused severe drop in top-1 vs legacy test set: verified
  - Worst recall plummeted to 2.79%: verified

## 5. Interpretation & Next Action
- **Interpretation**: Expanded data requires longer training, worker throughput optimization, and warm-start learning rate adaptation.
- **Limitations & Uncertainty**: Legacy test set vs expanded val set differences.
- **Related Records**: [EXP-305](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-305-expanded-dataset-20ep.md), [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md)
- **Next Action / Retry Condition**: Enable dynamic DataLoader workers and continue training with Attempt 305.
