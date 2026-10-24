# Experiment Record: EXP-401 — Recalibration of existing weights (no training)

- **ID**: EXP-401
- **Title**: Post-hoc prior correction + temperature scaling on the current best weights
- **TASK IDs**: TASK-002, TASK-003
- **Status**: planned
- **Created**: 2026-10-24 21:40
- **Updated**: 2026-10-24 21:40

---

## 1. Objective & Hypothesis
- **Question**: How much of the accuracy gap is caused by the wrong class prior the model learned, rather than by missing visual features?
- **Hypothesis**: Correcting the posteriors for the prior shift (effective training prior ∝ 1/count from double balancing; true prior = val class frequency) raises Top-1, Cotton/Polyester recall and rare-class precision without retraining. Temperature scaling lowers calibration error.
- **Rationale**: Attempt 309 per-class data: Cotton precision 0.90 / recall 0.18, Corduroy precision 0.04 / recall 0.84 (see BUG-001 update 2026-10-24).
- **Related Attempts**: Attempt 310 (source of the weights), BUG-001.
- **Reason for Repeat**: Not applicable.

## 2. Configuration & Baseline
- **Source / Version**: `backend/fabric_classifier/training/recalibrate.py` on `main` of Adithya-109/Fabric-Detection.
- **Weights**: `fabric_clf_best.pt` — **verified 2026-10-24 to be Attempt 310** (val macro-F1 0.3754). `fabric_clf_last.pt` is Attempt 310 epoch 5. Attempt 309's better weights (val macro-F1 0.4037) were overwritten and are no longer available.
- **Data Version**: iMaterialist processed folders only (`train/` counts for the training prior, `val/` for selection, `test/` read once). Fixed on-disk split → no train/eval leakage. TextileNet/microscope excluded because their legacy split depended on Windows directory order.
- **Environment**: Inference only — Mac (CPU/MPS), Colab, or the original Windows PC.
- **Baseline**: Same weights, plain argmax, T = 1 (the model as served today), measured on the same images.
- **Planned Changes**: Post-hoc only: prior-correction strength chosen on val (macro-F1, prefer worst recall ≥ 0.40), then temperature fitted on val.
- **Success Criteria**: Val and test macro-F1 and Top-1 higher than baseline; worst-class recall not lower.
- **Stopping Condition**: Single run.

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```bash
  python -m backend.fabric_classifier.training.recalibrate \
      --imaterialist-dir <path>/DATASETS/imaterialist_processed --report-test --write
  ```
- **Affected Files**: `backend/fabric_classifier/calibration/temperature.json` (with `--write`), `runs/recalibration/*`.
- **Execution State**: not yet run (waiting for data access).

## 4. Observed Results & Evidence
- Not yet run.
