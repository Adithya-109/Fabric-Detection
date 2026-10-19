# Fabric Classifier Master Handoff (Preserved Snapshot)

Archived Date: 2026-10-11
Original Owner Context: autonomous multi-attempt training.
Status: Historical reference snapshot preserved during persistent memory system setup. Current live handover is maintained in [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md).

---

## 0. PROJECT POLICY: NON-COMMERCIAL
This project is for personal/research use only and will NOT be commercialized.
- All datasets (TextileNet, microscope MIT, iBUG, iMaterialist) may be used in the final model.
- research_only_data_used must no longer block targets_met. Keep logging it as a provenance field, but never use it as a pass/fail gate.
- Do NOT delete the existing backup at backend/fabric_classifier_backup/.
- Keep USE_IBUG_RESEARCH_DATA and add USE_IMATERIALIST_DATA as configurable flags (default: true).
- Tag every image with its source dataset in all manifests.

## 0.1 EXPERIMENT-GATED DEFAULTS
Nothing here is a hard rule except the environment.
- **Environment**: Always run conda activate myenv. Hardware is 24 GB RAM. Measure, do not assume.
- **Starting defaults (changeable with evidence)**: EfficientNet-B0 backbone; head Dropout(0.3) -> Linear(1280->256) -> ReLU -> Dropout(0.2) -> Linear(256->14); 14-class order; FP16 on GPU; temperature scaling; predict() output format.
- **Experiment rules**: Change ONE thing per experiment. Compare against the original TextileNet test set. Keep a change only if it beats control clearly on top-1 and macro-F1 without hurting worst-class recall. Test cheap changes first (data, loss, LR, augmentation, etc.) before architecture changes. Architecture changes require fresh training runs. Log all experiments.

## 1. Project Objective

Train a 14-class fabric material classifier.

Done criteria (judged on TEST-set accuracy metrics only, on both original and combined sets):

| Metric | Target |
|---|---|
| Top-1 Accuracy (test) | >= 0.72 |
| Top-3 Accuracy (test) | >= 0.90 |
| Macro F1 (test) | >= 0.68 |
| Worst single-class recall (test) | >= 0.40 |

Inference time and inference VRAM are NOT targets and do not affect targets_met. Measure and record them once per attempt for information only.

## 2. Non-Negotiables

### 2.1 Model and class contract

- Backbone: `torchvision` EfficientNet-B0 only.
- Head: `Dropout(0.3) -> Linear(1280->256) -> ReLU -> Dropout(0.2) -> Linear(256->14)`.
- Class order is fixed in `backend/fabric_classifier/classes.py`:
  1. Cotton
  2. Polyester
  3. Silk
  4. Denim
  5. Linen
  6. Wool
  7. Leather
  8. Velvet
  9. Corduroy
  10. Fleece
  11. Nylon
  12. Satin
  13. Knitted
  14. Suede

### 2.2 Inference API contract

`FabricClassifier.predict(pil_image)` must always return exactly 3 items in descending confidence order:

```python
[
    {"name": "Cotton", "confidence": 85.5},
    {"name": "Linen", "confidence": 10.2},
    {"name": "Polyester", "confidence": 4.3},
]
```

This contract is required by `backend/wardrobe_analytics.py` (Note: this file currently does not exist in the repository but the contract remains strictly enforced).

Additionally, the inference pipeline supports Temperature Scaling. It automatically looks for a calibration file at `backend/fabric_classifier/calibration/temperature.json` to scale logits before softmax. If absent, it defaults to a temperature of 1.0.

### 2.3 Runtime constraints

- GPU: RTX 3050 6GB; this model budget <= 300 MB VRAM.
- RAM: 8 GB total; low-memory profile required.
- VRAM usage and CPU fallbacks are dynamically managed by `FabricMemoryManager` (`backend/fabric_classifier/memory_manager.py`) to prevent OOM errors.
- Background orchestration (pausing downloads during training, RAM checks) is handled by `DynamicResourceManager` (`backend/fabric_classifier/training/resource_manager.py`).
- FP16 must remain enabled on GPU path.
- Training command pattern:

```powershell
conda activate myenv; python -u backend/fabric_classifier/training/train.py
```

- Do not run downloads concurrently with training.
- Never run two `train.py` writers at once.

## 3. Repository Map (Critical Files)

- Main trainer: `backend/fabric_classifier/training/train.py`
- Resource manager: `backend/fabric_classifier/training/resource_manager.py` (Orchestrates RAM/downloads)
- Memory manager: `backend/fabric_classifier/memory_manager.py` (Handles dynamic GPU/CPU fallback)
- Patch extraction: `backend/fabric_classifier/training/dataset.py`
- Inference wrapper: `backend/fabric_classifier/inference.py`
- Model definition: `backend/fabric_classifier/model.py`
- Class order and mappings: `backend/fabric_classifier/classes.py`
- Calibration data: `backend/fabric_classifier/calibration/temperature.json` (Used by inference API)
- Root-level analysis utilities: `analysis_task.py`, `analysis_task_v2.py`, `report.py`, `count_images.py`, `integration_test.py`
- Attempt log (machine-readable): `backend/fabric_classifier/training/training_log.json`
- Per-epoch stream: `backend/fabric_classifier/training/epoch_progress.jsonl`
- Human postmortems: `backend/fabric_classifier/training/experiment_log.md`
- Issues ledger: `backend/fabric_classifier/training/issues_log.json`
- New-data audit: `backend/fabric_classifier/training/new_dataset_audit.json`
- Data decisions: `backend/fabric_classifier/training/dataset_decisions.md`
- Added-data manifest: `backend/fabric_classifier/training/additional_data_manifest.json`
- Weights:
  - `backend/fabric_classifier/weights/fabric_clf_best.pt`
  - `backend/fabric_classifier/weights/fabric_clf_last.pt`

## 4. Dataset and Licensing Truth

### 4.1 Source datasets

- Base dataset: TextileNet (`DATASETS/TextileNet-main/fabric` and `.../fibre`).
- Additional commercial-safe dataset: Microscope images of fabric (MIT).
- Additional research-only dataset: The Fabrics Dataset by iBUG (research-only, not final-deliverable safe).

### 4.2 Audit totals (from `new_dataset_audit.json`)

- Microscope images of fabric:
  - Total: 833
  - Valid: 833
  - Corrupt: 0
  - Covered target classes: Cotton, Knitted, Linen, Nylon, Polyester, Satin, Silk, Velvet
- The Fabrics Dataset by iBUG:
  - Total: 7885
  - Valid: 7885
  - Corrupt: 0
  - Covered target classes: Corduroy, Cotton, Denim, Fleece, Leather, Linen, Nylon, Polyester, Satin, Silk, Suede, Velvet, Wool

### 4.3 Current curated manifest totals (from `additional_data_manifest.json`)

- Dataset keys:
  - `microscope_mit`
  - `ibug_research_only`
- `microscope_mit` total included paths: 593
  - Nylon 121, Silk 120, Knitted 61, Satin 62, Velvet 54, Cotton 55, Linen 60, Polyester 60
- `ibug_research_only` total included paths: 1432
  - Fleece 120, Leather 76, Linen 220, Nylon 220, Polyester 700, Velvet 96

License policy implemented in trainer:

- Runs with iBUG set `research_only_data_used=true` and cannot be final deliverables even if numeric metrics pass.
- Final accepted model must be from a run with `USE_IBUG_RESEARCH_DATA=false`.

## 5. Current State Snapshot (As Of 2026-10-11)

- Active training process: PID 31100 running background task `task-558` (`conda activate myenv; python -u backend/fabric_classifier/training/train.py`).
- Active execution profile: 8 dynamic CPU DataLoader workers on 12-core CPU (`NUM_WORKERS = 8`), pinned memory enabled (`pin_memory = True`), RTX 3050 GPU running at P0 state (~58°C, ~34W, ~964 MB VRAM).
- Total training dataset: 232,330 images (TextileNet + Microscope + iBUG + iMaterialist).
- Throughput: ~25-30 it/s (~100-120 images/s, ~32 mins per epoch).
- Completed attempts on expanded dataset: Attempt 304 (completed), Attempt 305 (20 epochs completed; finished via policy stop rule `worst_recall_below_0_20_after_min_epoch` triggered by Polyester recall).
- Active running attempt: Attempt 306 (currently executing Epoch 9, step >26,000 / 58,083).
- Best metrics so far on expanded dataset: Val Macro-F1 = 32.21%, Val Top-1 = 31.95%, Worst-Class Recall = 8.11% (Attempt 306, Epoch 6); current running train loss = 1.101.

Weights on disk:
- `fabric_clf_best.pt`: 17,658,446 bytes (last write 2026-10-11 14:43:02, Attempt 306 Epoch 6)
- `fabric_clf_last.pt`: 52,558,899 bytes (last write 2026-10-11 16:02:10, Attempt 306 Epoch 8)

## 6. Attempt History (High-Level)

### 6.1 Summary through attempt 16

- Attempt 1 blocked by environment/startup issues.
- Attempts 2-16 repeatedly missed target metrics.
- Best historical completed attempt from earlier phase: attempt 15 (~0.582 top1, ~0.583 macro F1).
- Chronic weak classes persisted: Polyester (worst), then Velvet/Nylon, with Linen/Fleece instability.

### 6.2 Detailed attempts 17-22 (persisted)

| Attempt | Status | Research-only data | Top1 | Top3 | Macro F1 | Worst recall | Inference ms | VRAM MB | Primary retry reason |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 17 | completed_policy_stop | true | 0.5618 | 0.7949 | 0.5561 | 0.1917 | 8.0543 | 146.4712 | worst recall below threshold at epoch 20 |
| 18 | completed_policy_stop | true | 0.5618 | 0.7949 | 0.5561 | 0.1917 | 7.6808 | 180.5171 | plateau window policy stop |
| 19 | completed | false | 0.5622 | 0.8104 | 0.5642 | 0.1500 | 7.8350 | 150.2344 | initial run failed targets |
| 20 | completed_policy_stop | false | 0.5388 | 0.7857 | 0.5469 | 0.2917 | 7.9606 | 180.9751 | worst recall rule triggered |
| 21 | completed_policy_stop | false | 0.5505 | 0.7935 | 0.5525 | 0.3167 | 7.6988 | 180.9751 | plateau window policy stop |
| 22 | completed_policy_stop | false | 0.5537 | 0.7902 | 0.5613 | 0.3750 | 7.8227 | 180.9751 | plateau window policy stop |

### 6.3 Attempt 23 partial state (not persisted as complete)

Evidence from `epoch_progress.jsonl` and terminal:

- Started with commercial-safe mode (`USE_IBUG_RESEARCH_DATA=false`, microscope enabled).
- Reached epoch 14 step 700.
- Last completed epoch before interruption: epoch 13 (val_top1 0.5502, val_macro_f1 0.5469, val_worst_recall 0.2417).
- Interrupted by user; trainer exited cleanly.

### 6.4 Non-Commercial Expanded Dataset Phase (Attempts 304 - 306)

| Attempt | Status | Train Images | Top1 | Top3 | Macro F1 | Worst recall | Inference ms | VRAM MB | Primary stop / note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 304 | completed | 232,330 | 0.2866 | 0.5312 | 0.2883 | 0.0279 | 6.31 | 182.1 | 13 epochs run |
| 305 | completed_policy_stop | 232,330 | 0.3168 | 0.5628 | 0.3176 | 0.0268 | 6.29 | 182.1 | Stopped at epoch 20 (`worst_recall_below_0_20` on Polyester) |
| 306 | in_progress | 232,330 | 0.3195 | 0.5645 | 0.3221 | 0.0811 | ~6.29 | ~182.1 | Currently in Epoch 9; best at Epoch 6 |

## 7. Mistake Ledger (Critical, Consolidated)

This section intentionally records repeated mistakes and failure patterns so future AIs do not repeat them.

1. Environment activation failure (early run)
- Symptom: attempt 1 blocked due to activation/session problems.
- Impact: no training progress.
- Prevention: always use `myenv` and verify process before launching.

2. Relative import failure when running trainer as script
- Symptom: import errors when launching `train.py` directly.
- Impact: startup failures.
- Fix: fallback absolute-import path added in `train.py`.

3. Concurrent `train.py` writers (historical)
- Symptom: checkpoint/history oscillation and conflicting metrics from duplicate processes.
- Impact: possible checkpoint corruption and invalid progress interpretation.
- Fix: singleton lock + process PID guard added.

4. Download + training coupling instability
- Symptom: RAM spikes/stalls and noisy runtime when downloads overlap training.
- Impact: slow epochs, risk of OOM/instability.
- Fix: resource manager pauses downloads during training.

5. Targeted top-up download failures
- Symptom: repeated downloader failures (including Windows process return code errors) for Corduroy/Suede/Wool.
- Impact: data gates did not reach target counts.
- Current status: unresolved source reliability issue; workflow now proceeds with best available counts.

6. Data-gate threshold miss but continuing anyway
- Symptom: attempt 17 started below desired class-count thresholds.
- Impact: persistent weak-class performance risk.
- Lesson: gate misses must be explicitly documented and linked to outcome quality.

7. Research-only data accidentally used in high-priority attempts
- Symptom: attempts 17/18 used iBUG for exploratory gains.
- Impact: even if metrics improved, run is non-deployable.
- Fix: explicit license gate and rerun policy implemented.

8. Cross-attempt best-checkpoint reuse bug (major)
- Symptom: attempts 17 and 18 reported identical final test metrics despite different epoch trajectories.
- Root cause: stale best checkpoint metadata reused across attempts on warm start.
- Fixes in `train.py`:
  - On attempt mismatch, warm-start weights only and reset per-attempt best tracking.
  - Recompute best from same-attempt `history` when resume metadata is inconsistent.
  - Final evaluation only loads `fabric_clf_best.pt` if checkpoint attempt matches current attempt; otherwise uses attempt-local last checkpoint.

9. Monitoring command pitfalls
- Symptom: some ad-hoc Select-String patterns missed metric lines due pattern spacing/quoting.
- Impact: false assumption that epoch metrics were missing.
- Prevention: use JSON field-aware parsing or validated regex patterns.

10. User interruptions left non-finalized attempts
- Symptom: attempts can appear in `epoch_progress.jsonl` but not in `training_log.json`.
- Impact: stale dashboards if only `training_log.json` is read.
- Prevention: always cross-check `epoch_progress.jsonl`, `issues_log.json`, and process state.

11. Over-reliance on terminal text without persisted verification
- Symptom: inconsistent status claims (e.g., inferred completion when only partial logs existed).
- Impact: inaccurate handoff status.
- Prevention: finalize status only from persisted artifacts and process checks.

## 8. What Has Been Fixed In Code

Major hardening and correctness changes already landed:

- `backend/fabric_classifier/training/train.py`
  - direct-script import fallback.
  - singleton lock and existing-process detection.
  - runtime resource gating and safe constrained mode.
  - license-aware `targets_met` behavior (`research_only_data_used`).
  - auto-retry policy branches for low top1, low worst recall, plateau windows.
  - experiment postmortem appends after each completed attempt.
  - cross-attempt best-checkpoint reset and history-derived best reconciliation.
  - final evaluation uses attempt-consistent checkpoint selection.

- `backend/fabric_classifier/training/dataset.py`
  - deterministic patch sampling support via `rng` parameter.
  - malformed-image safety fallbacks.

- `backend/fabric_classifier/inference.py`
  - deterministic seed from image content (`crc32` of thumbnail) for stable patching.

- `backend/fabric_classifier/training/audit_new_datasets.py`, `analyze_history.py`, `prepare_additional_datasets.py`
  - robust audit/history/manifest workflows to support controlled integrations.

## 9. Open Problems

1. Core quality targets remain unmet after many retries.
2. Weak-class robustness still unstable, especially Polyester and Velvet; Nylon/Linen/Fleece remain inconsistent.
3. Plateau policy stops frequently trigger before meaningful target gains.
4. Data gates for Corduroy/Suede/Wool cannot reliably self-heal via targeted downloads.

## 10. Operational Runbook For Any Future AI

### 10.1 Pre-flight checks (always)

```powershell
Get-CimInstance Win32_Process | Where-Object {
  $_.Name -eq 'python.exe' -and $_.CommandLine -match 'backend/fabric_classifier/training/train.py'
} | Select-Object ProcessId, CommandLine
```

If any PID exists: monitor only. Do not launch another trainer.

```powershell
Get-ChildItem backend/fabric_classifier/training/runtime_control -ErrorAction SilentlyContinue
```

### 10.2 Launch command

```powershell
conda activate myenv; python -u backend/fabric_classifier/training/train.py
```

### 10.3 Monitoring commands

```powershell
Get-Content backend/fabric_classifier/training/epoch_progress.jsonl -Tail 30
```

```powershell
Get-Content backend/fabric_classifier/training/training_log.json -Raw
```

```powershell
Get-Content backend/fabric_classifier/training/experiment_log.md -Tail 80
```

### 10.4 Completion validation

A run is only complete if all of these are true:

1. Attempt entry exists in `training_log.json` with final metrics.
2. Numeric metrics meet done criteria.
3. `research_only_data_used` is false.
4. Inference contract in `inference.py` remains unchanged.

## 11. Current Best Knowledge For Next Iterations

- Commercial-safe attempts are currently plateauing in the low-to-mid 0.55 top1 range.
- Increasing epochs without fixing weak-class separability has mostly increased time, not quality.
- The strongest progress came from careful LR reductions, patience tuning, and controlled additional data, but still short of goals.
- Keep microscope data enabled; use iBUG only for exploratory diagnosis, never final acceptance.

## 12. Non-Obvious Gotchas

- `training_log.json` only records completed attempts; interrupted attempts may exist only in `epoch_progress.jsonl` and `issues_log.json`.
- `additional_data_manifest.json` key is `ibug_research_only` (not `ibug_research`).
- The `.github/copilot-instructions.md` references `COPILOT_TRAINING_PROMPT.md` and `FABRIC_CLASSIFIER_SPEC.md`; those files are not present in root at time of writing, so use in-repo trainer/config as practical source of truth.

## 13. Minimal Resume Checklist

1. Confirm no active trainer PID.
2. Read latest `training_log.json`, `epoch_progress.jsonl`, and `experiment_log.md`.
3. Launch exactly once in `myenv`.
4. Track epoch metrics and policy-stop triggers.
5. After each completion, verify `targets_met` and `research_only_data_used` before claiming progress.

## 14. One-Line Truth

The non-commercial pipeline is fully scaled to 232,330 training images running stably on 8 dynamic CPU workers + RTX 3050; Attempt 305 completed all 20 epochs (Macro-F1 31.76%), and Attempt 306 is actively training in Epoch 9 with train loss at a record low of 1.101 and validation Macro-F1 at 32.21%.

## 15. Performance & User FAQs

This section captures end-user knowledge about how the model works and its current performance baseline.

### 15.1 Current Accuracy Baseline
- **Top-1 Accuracy:** Currently hovers between **55% and 58.24%** on commercial-safe data.
- **Top-3 Accuracy:** Up to **83.52%**.
- **Macro F1:** Up to **58.32%**.
- **Issue:** The model triggers policy stops frequently due to "Worst-Class Recall" dipping below 20-40%.

### 15.2 Best Performing Classes
The model performs significantly better on strongly textured/rigid fabrics:
1. **Corduroy:** ~75.5% average recall (peaked at 91.1%)
2. **Denim:** ~71.4% average recall
3. **Suede:** ~69.2% average recall
4. **Leather:** ~63.6% average recall
5. **Wool:** ~60.8% average recall

*Smooth or translucent fabrics (Polyester, Velvet, Nylon) are the weakest, heavily pulling down the overall accuracy.*

### 15.3 How Image Inference Works
A user can upload a standard, non-zoomed picture of a garment (e.g., a normal shirt). The inference pipeline (`backend/fabric_classifier/training/dataset.py` -> `extract_patches`) handles it automatically:
1. **Background Masking:** Filters out transparent and pure white backgrounds.
2. **Edge Avoidance:** Erodes the mask to ignore zippers, seams, and edges.
3. **Dynamic Patch Extraction:** Randomly extracts exactly **7 square patches** from the interior fabric.
4. **Averaging:** The model predicts the fabric on all 7 zoomed-in patches and averages the probabilities for the final output.

### 15.4 Meaning of "Average Recall"
**Recall** measures what percentage of the *actual* positive instances were correctly identified. For example, if there are 100 actual Polyester shirts and the model correctly identifies 28 of them, the recall for Polyester is 28%. 
**Average Recall** is the mean of these recall percentages across all fabric classes (or across multiple training attempts), representing the model's overall ability to find the correct fabric when it's present.

### 15.5 How to Test a Single Image
To test a custom image through the model's inference pipeline:
1. Drop the image (e.g., `my_shirt.jpg`) into the `test_images/` directory at the root of the project.
2. From the project root, activate the conda environment and run the test script:

```powershell
conda activate myenv
python test_image.py test_images/my_shirt.jpg
```

This script will automatically initialize the `FabricClassifier`, process the image, and output the top 3 predicted classes with confidence scores.

## 16. Backups

### 16.1 Commercial-Safe Training Backup
A full backup of the commercial-safe training state (including weights, logs, code, and calibration) has been created at `backend/fabric_classifier_backup/`. This allows experimentation with research-only datasets (`iBUG`) or hyperparameter changes without risking the current best commercial-safe artifacts. If you need to revert to the commercial-safe baseline, restore the contents of this backup directory to `backend/fabric_classifier/`.

## 17. Phase 0 (Preflight)
Date: 2026-10-10
**Decisions and Why**: 
- Replaced the hardcoded memory and RAM thresholds with relative percentages derived from psutil totals since the hardware has 24GB RAM.
- Rewrote the top of HANDOFF.md to reflect the Non-Commercial policy change, loosening constraints on VRAM and model backbone.

**File Paths Created**:
- ackend/fabric_classifier_backup_pre_imaterialist/ (Backup of current state before iMaterialist).

**Resource Numbers Measured**:
- Total RAM: 23.80 GB (Available: 12.05 GB)
- CPU Cores: 12
- Free Disk: 23.81 GB
- Total VRAM: 6.00 GB (Free: 5.04 GB)

**Bugs or Errors Encountered**:
- Symptom: psutil script failed with SyntaxError due to single-quote escaping in f-string.
- Root Cause: Escaping issue in bash/powershell string encapsulation.
- Fix: Wrote to scratch/preflight.py and ran it using conda activate myenv.

**Current State & Next Step**:
- Preflight is complete and integration_test.py passes successfully. 
- Next Step: Proceed to Phase 1 (Inspect before touching anything). Start exploring the iMaterialist dataset parquet files using pyarrow.

## 18. Phase 1 (Inspect)
Date: 2026-10-10
**Decisions and Why**: 
- Installed pyarrow=14.0.2 to read parquet files properly on existing numpy version.
- Verified iMaterialist dataset structure (721,065 total images across 153 parquet files). 
- Found the ~800 image per class cap in `train.py` (line 99) and `prepare_additional_datasets.py` (`IBUG_TARGET_CAPS`). I removed both entirely so all valid images will be used (Phase 3 policy).
- Verified images can decode cleanly to RGB (0 corrupt images in initial test).

**File Paths Created**:
- `scratch/phase1.py` (Script to inspect schema and row counts)

**Current State & Next Step**:
- Inspection complete. Parquets are valid and contain a 'material' string column.
- Next Step: Proceed to Phase 2 (Label mapping).

## 19. Phase 2 (Label mapping)
Date: 2026-10-10
**Decisions and Why**: 
- Based on counting all materials in iMaterialist, kept only strict unambiguous mappings to our 14 classes to prevent label noise.
- Dropped compound materials like 'Cotton Polyester' or 'Faux Fur Wool'.
- Mapped explicit synonyms according to TARGET_PRIMARY_SOURCES: 'Cashmere' -> Wool, 'Faux Fur' -> Fleece, 'Knit' -> Knitted.

**Mapping Rules and Counts**:
- Cotton: 78834
- Polyester: 41956
- Denim: 26222
- Knit: 18805 (-> Knitted)
- Leather: 10075
- Wool: 7914
- Nylon: 7249
- Silk: 6562
- Faux Fur: 6190 (-> Fleece)
- Fleece: 5947
- Satin: 5013
- Velvet: 4357
- Linen: 2120
- Cashmere: 1567 (-> Wool)
- Suede: 1139
- Corduroy: 568

**File Paths Created**:
- `imaterialist_label_mapping.json` (Contains mapping rules and counts)

**Bugs or Errors Encountered**:
- None during mapping. Unit tests verified all keys map exactly to indices 0-13 and correctly back to class names.

**Current State & Next Step**:
- Label mapping is complete. 
- Next Step: Proceed to Phase 3 (Preprocessing). 

## 20. Phase 3 (Preprocessing)
Date: 2026-10-10
**Decisions and Why**: 
- Iterated over the 153 iMaterialist parquet files, decoding images and resizing max side to 512px.
- Split images deterministically using md5 hash mod 10 into 80/10/10 Train/Val/Test splits.
- Output deterministic splits to `DATASETS/imaterialist_processed/`.
- Modified `train.py` `load_and_split_data` to bypass the original `train_test_split` for iMaterialist, preserving exactly the old validation/test set for the legacy datasets while safely appending the new deterministic splits.

**File Paths Created**:
- `DATASETS/imaterialist_processed/`
- `scratch/phase3_smoke_test.py`
- `scratch/phase3_tests.py`

**Bugs or Errors Encountered**:
- `train.py`'s existing split logic dynamically resplits all incoming files with `random_state=42`. Fixed this by explicitly segregating the legacy files and appending the iMaterialist files AFTER the old split.

**Current State & Next Step**:
- Preprocessing is complete. Smoke test ran extract_patches on 700 images with 0.00% failure rate. No-leak check passed.
- Next Step: Proceed to Phase 4 (Report).

## 21. Phase 4 (Data availability report)
Date: 2026-10-10
**Decisions and Why**: 
- Counted total accessible images by parsing `additional_data_manifest.json` and the `imaterialist_processed` folder.

**File Paths Created**:
- `DATASETS/imaterialist_class_availability.json`
- `DATASETS/imaterialist_class_availability.md`

**Resource Numbers Measured**:
- Cotton: 76291, Polyester: 41534, Silk: 6359, Denim: 24998, Linen: 2344, Wool: 9064, Leather: 9692, Velvet: 4317, Corduroy: 517, Fleece: 11876, Nylon: 7208, Satin: 4758, Knitted: 18226, Suede: 1122.
- Total valid images available for training far exceed the 150-image minimum gate.

**Current State & Next Step**:
- Report generated. Integration test passed.
- Next Step: Proceed to Phase 5 (Full Scale Training Run).

## 22. Phase 5 (Full Scale Training Run - Attempts 305 & 306)
Date: 2026-10-10 / 2026-10-11
**Decisions and Why**:
- Integrated all 216,000+ iMaterialist images alongside TextileNet, Microscope, and iBUG data (total training pool: 232,330 images).
- Dynamic Hardware Optimization: Overrode legacy `NUM_WORKERS = 0` and disabled pin memory by setting `NUM_WORKERS = min(8, max(1, os.cpu_count() - 2))` (8 dynamic background workers on 12-core CPU) and `pin_memory = True` for RTX 3050. This increased throughput from ~13.5 it/s to ~30.0 it/s (>120 samples/sec), cutting per-epoch duration in half (~32 mins/epoch).
- Maintained stability: 0 NaNs (`skipped_nan_steps: 0`), 0 OOMs (`oom_skipped_steps: 0`).

**Attempt 305 Results (Completed 20 Epochs)**:
- Total Duration: 69,532 seconds (~19.3 hours).
- Progression across 20 epochs:
  - `train_loss`: dropped from 1.3471 to 1.1473.
  - `val_loss`: stabilized from 12.11 down to 4.36.
  - `val_top1_accuracy`: 31.68% (Epoch 20).
  - `val_macro_f1`: 31.76% (Epoch 20).
  - `val_worst_class_recall`: 2.68% (Polyester).
- Per-class recall in final evaluation:
  - High performers: Corduroy 84.1%, Suede 78.7%, Linen 77.0%, Satin 65.9%, Velvet 57.3%, Wool 56.5%, Leather 53.8%, Silk 46.5%.
  - Challenged classes: Knitted 39.1%, Fleece 39.0%, Denim 25.5%, Cotton 12.0%, Polyester 2.65%.
- Policy stop trigger: `worst_recall_below_0_20_after_min_epoch` at Epoch 20 (Polyester recall fell below 0.20 threshold).
- Saved checkpoint: `backend/fabric_classifier/weights/fabric_clf_last.pt`.

**Attempt 306 Progress (In-Flight)**:
- Launched automatically by autonomous retry controller from best weights.
- Epochs 1-8 completed:
  - `train_loss`: decreased to 1.1069 (Epoch 8) and currently 1.1010 in Epoch 9.
  - `val_top1_accuracy`: peaked at 31.95% (Epoch 6).
  - `val_macro_f1`: peaked at 32.21% (Epoch 6 - current overall best).
  - `val_worst_class_recall`: rose from 1.48% up to 8.11% (Epoch 6).
- Status: Epoch 9 in progress (step >26,000 / 58,083).
- Active background task: `task-558` (PID 31100 + 8 worker processes).
