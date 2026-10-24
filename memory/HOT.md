# Current Working State & Live Handover

- **Timestamp**: 2026-10-21 01:25 (+05:30) — Project shutdown complete. All background servers terminated; port 5050 closed; no training or background processes active; git working tree clean and synchronized with origin/main.
- **Active Tasks**: [TASK-004](file:///Users/adithyabinojnair/Fabric-Classifier/memory/tasks.md#task-004) (`done`), [TASK-001](file:///Users/adithyabinojnair/Fabric-Classifier/memory/tasks.md#task-001) (`paused`), [TASK-003](file:///Users/adithyabinojnair/Fabric-Classifier/memory/tasks.md#task-003) (`in_progress`, nothing running); TASK-002 `todo`, blocked on TASK-001
- **Authoritative Tasks Index**: [memory/tasks.md](file:///Users/adithyabinojnair/Fabric-Classifier/memory/tasks.md)

---

## 1. Objective & Completion Criteria
- **Objective**: Train a 14-class fabric classifier on 232,330 images (EfficientNet-B0, [PROJECT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/PROJECT.md)).
- **Done Criteria (Test Set)**: Top-1 >= 0.72, Top-3 >= 0.90, Macro F1 >= 0.68, Worst-class recall >= 0.40.

---

## 2. Current Execution State (verified 2026-10-14 04:46)
- **No `train.py` process is running** (checked twice via `Get-CimInstance Win32_Process`). Two server restarts killed earlier runs. Re-check before any action: `Get-CimInstance Win32_Process | ? {$_.CommandLine -match 'train.py'}`.
- **Attempt 309: completed** (policy stop at Ep 20, worst val recall 15.44% < 20%); persisted in `training_log.json` (309 entries). `final_metrics_achieved` (split unverified): Top-1 43.28%, Top-3 66.50%, Macro-F1 40.48%, worst recall 17.55% (Polyester; Cotton 17.95%). Best val Macro-F1 40.37% (Ep 13). Record: [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md).
- **Attempt 310: interrupted** after Epoch 5 evaluation (Epoch 6 reached step 58,000/58,083, validation not logged); not in `training_log.json`. Val Macro-F1 34.95–37.54%, worst recall 9.56–14.0%, train loss jumped from ~0.83 to ~0.90–0.92 at Ep 4 (cause not investigated). No gain over 309. Record: [EXP-310](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-310-warm-start-interrupted.md). Check state in `backend/fabric_classifier/training/epoch_progress.jsonl` (last write 2026-10-14 01:53).
- **Weights**: `fabric_clf_best.pt` (last write 2026-10-13 20:56) and `fabric_clf_last.pt` (2026-10-14 00:39) exist; which attempt/epoch each holds is **unverified**.
- **Unverified / not done**: reason for Att 310 loss spike; whether `final_metrics_achieved` is val or test; `HANDOFF.md` was not re-synced this session.

---

## 3. Persistent Blocker & Target Gap
- [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md) (open): Cotton/Polyester recall under the 20% stop and the 40% target. The ~+5%/attempt trend ended with Attempt 310. "Lack of data" was previously ruled out in BUG-001, so a data top-up is low priority until label quality is checked (unverified).
- [BUG-003](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-003-cross-attempt-checkpoint-leak.md) is `resolved` (read this session); resume behaviour observed: trainer resumed Attempt 309 at Epoch 19 from step 0.
- Large gap to targets (Top-1 ~43% vs 72%, Macro-F1 ~40% vs 68%).

---

## 3b. Update 2026-10-24 — test suite + accuracy plan (branch `feature/tests-and-accuracy-plan`)
- Root cause of BUG-001 identified as prior shift from double balancing (sampler + loss weights); see `docs/IMPROVEMENT_PLAN.md` §2 and BUG-001 update.
- Added `tests/` (unittest/pytest), shared post-processing, metrics with precision + confusion matrix, leakage-free splits, opt-in trainer flags (defaults = legacy behaviour), Phase-A `prior_sweep.py`. No training was run.
- **Next concrete action (needs user OK, no training)**: on the RTX machine run `python -m backend.fabric_classifier.training.prior_sweep --report-test --write` and record as a new EXP.

## 4. Constraints, Working Files, Next Action
- **Constraints**: conda `myenv`; never run concurrent `train.py` writers; FP16, RTX 3050 6GB; **user instruction 2026-10-14: do not start anything without asking**; data must satisfy [DEC-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/DEC-001-non-commercial-data-policy.md).
- **Working files**: `backend/fabric_classifier/training/train.py`, `epoch_progress.jsonl`, `training_log.json`, `backend/fabric_classifier/weights/`, scratch scripts in `scratch/`.
- **Next Concrete Action (PLANNED, not done)**: (1) verify no trainer is running; (2) ask the user whether to test class-weighted focal loss (one isolated change, per BUG-001) or do read-only per-class counts and a Cotton/Polyester label sample first; (3) create a new `planned` EXP record before any launch. Do NOT relaunch unchanged.
- **Open user decision**: whether to delete or keep the root `HANDOFF.md` stub (the old content is already in `memory/archive/HANDOFF_legacy_2026-10-11.md`). I only corrected its stale "Attempt 306 running" lines (2026-10-17); nothing was deleted. `scratch/` cleanup also pending the user's choice; no files removed.
- **Repository Version Control**: Clean repository created on branch `main` and pushed to remote [Fabric-Classifier-7-Segment](https://github.com/Rancheology/Fabric-Classifier-7-Segment.git). Datasets (`DATASETS/`), virtualenv (`.venv/`), and duplicate backups are ignored via [.gitignore](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/.gitignore). All source code, trained weights, training logs, scratch scripts, and persistent memory records are committed and synced. Working tree is clean; `.git` directory size reduced from 11.1 GB to ~63 MB.
