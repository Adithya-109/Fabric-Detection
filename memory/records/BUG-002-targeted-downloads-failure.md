# Bug Record: BUG-002 — Targeted Top-Up Downloader Failures for Specific Classes

- **ID**: BUG-002
- **Title**: Targeted downloader failures for Corduroy, Suede, and Wool on Windows
- **TASK IDs**: TASK-001
- **Status**: mitigated
- **Created**: 2026-10-09 14:00:00
- **Updated**: 2026-10-10 18:00:00

---

## 1. Problem Description & Impact
- **Symptom**: Targeted downloader scripts for Corduroy, Suede, and Wool repeatedly failed with Windows process return code errors and failed downloads.
- **Expected Behavior**: Download scripts should retrieve target image counts to satisfy data gates.
- **Actual Behavior**: Downloader failed to retrieve top-ups reliably.
- **Affected Area**: Data preparation / download scripts in `DATASETS/` and `backend/fabric_classifier/training/download_fibre_subset.py`.
- **Impact & Severity**: Medium. Historically prevented data gates from passing; now bypassed by integrating iMaterialist dataset.

## 2. Environment & Reproduction
- **Reproduction Steps**:
  1. Run top-up downloader scripts for Corduroy/Suede from legacy sources.
  2. Process exits with non-zero return codes on Windows.
- **Inputs & Configuration**: Windows PowerShell, python download scripts.
- **Environment & Version**: Windows 11, conda `myenv`.
- **Original Evidence References**:
  - Error/Log/Source Path: `backend/fabric_classifier/training/issues_log.json`
  - Location / Run ID: Issue entry in `issues_log.json`
  - Verification Date: 2026-10-09

## 3. Investigation & Attempts
- **Attempts Made & Linked Records**:
  - Script fixes and retry passes failed to establish reliable source connection.
- **Ruled-Out Hypotheses & Evidence**:
  - Script syntax issue: ruled out; remote endpoints were flaky or rate-limited.
- **Remaining Uncertainty**: Source endpoint availability.

## 4. Workaround & Next Diagnostic
- **Workaround**: Integrated iMaterialist parquet data directly, which provides ample images for Corduroy (517 valid), Suede (1,122 valid), and Wool (9,064 valid), far exceeding the 150-image gate without needing top-up downloads.
- **Next Diagnostic Step**: No further downloads needed under non-commercial expanded dataset policy.
- **Conditions for Revisiting**: If specific dataset source is ever required.

## 5. Resolution & Verification
- **Resolution Summary**: Mitigated by switching data source to iMaterialist parquets.
- **Resolution Verification**: verified via [DATASETS/imaterialist_class_availability.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/DATASETS/imaterialist_class_availability.json)
- **Verification Evidence**: `DATASETS/imaterialist_class_availability.json` verifies count > 150 for all classes.
- **Evidence Status for Consequential Claims**:
  - iMaterialist satisfies class count requirements: verified
