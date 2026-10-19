# Decision Record: DEC-001 — Non-Commercial Project Policy & Dataset Ingestion

- **ID**: DEC-001
- **Title**: Project classification as non-commercial research allowing full dataset utilization
- **Scope**: Entire fabric classifier dataset pipeline, license gating, and done criteria
- **Status**: active
- **Date**: 2026-10-10

---

## 1. Context & Rationale
- **Context**: The project was originally constrained by strict commercial-only licensing rules, preventing research datasets (iBUG, iMaterialist) from being included in the final model deliverable. This created a hard ceiling (~58% top-1) due to scarce data (~800 samples/class max).
- **Decision**: Declare the project non-commercial (personal/research use only).
  - All datasets (TextileNet, Microscope MIT, iBUG, iMaterialist) may be used in the final model.
  - `research_only_data_used` remains logged as provenance, but is no longer a pass/fail blocker for `targets_met`.
  - The ~800 image per-class caps in `train.py` and `prepare_additional_datasets.py` were eliminated.
  - Backup preserved at `backend/fabric_classifier_backup/` and `backend/fabric_classifier_backup_pre_imaterialist/`.
- **Evidence**: Initial audit and integration showed >216,000 valid samples in iMaterialist, unlocking 232,330 total images.
- **Alternatives Considered**:
  - Keep commercial restriction: Ruled out because commercial data sources were insufficient to overcome plateauing accuracy.
- **Conditions for Reconsideration**: If user explicitly decides to commercialize the model, necessitating retraining exclusively on verified commercial-safe data.
