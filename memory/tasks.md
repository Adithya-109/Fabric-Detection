# Project Tasks Ledger

## 1. Task Operating Rules
- **Authoritative Statuses**: `todo`, `in_progress`, `paused`, `blocked`, `done`, `cancelled`.
- **Single Source of Truth**: This file maintains the canonical status for all project tasks; [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) summarizes the currently active task.
- **Completion Standard**: Mark a task `done` ONLY when its completion criteria have verified supporting evidence recorded in logs or test outputs.
- **Cancellation Standard**: Cancellation requires an explicit user direction or recorded decision ([decisions.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/decisions.md)).
- **Task Switching**: Before switching tasks, checkpoint unfinished work and update status here; never drop active state silently.
- **Scope Discipline**: Only meaningful project tasks belong here; do not record trivial one-off terminal commands as tasks.

---

## 2. Tasks Index Table

| ID | Title / Search Terms | Status | Affected Area | Last Update | Link | Essential Outcome / Blocker |
|---|---|---|---|---|---|---|
| **TASK-000** | Persistent Memory System Setup & Verification | `done` | Entire repository / Memory | 2026-10-11 | [Details](#task-000) | Fully initialized and verified file-based memory system |
| **TASK-001** | Train 14-Class Classifier to Target Accuracy | `paused` | `backend/fabric_classifier/` | 2026-10-13 | [Details](#task-001) | No trainer running (server restart); Att 309 policy-stopped, Att 310 interrupted after Ep 5 with no gain; best val Macro-F1 40.37% (Att 309 Ep 13); blocked by [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md) |
| **TASK-002** | Temperature Calibration & Inference Contract Test | `todo` | `backend/fabric_classifier/calibration/` | 2026-10-11 | [Details](#task-002) | Blocked on TASK-001 final weights |
| **TASK-003** | Resolve Polyester & Smooth Fabric Recall Deficit | `in_progress` | Loss / Augmentation / Training | 2026-10-14 | [Details](#task-003) | Worst recall 15.44% val at Att 309 stop, 9.6-14.0% in Att 310; still <20%; focal loss planned, not tried; nothing running |

---

## 3. Detailed Task Specifications

### <a id="task-000"></a>TASK-000: Persistent Memory System Setup & Verification
- **Requirement / Source**: User instruction (2026-10-11).
- **Status**: `done`
- **Completion Criteria**:
  - `GEMINI.md` configured with persistent memory loader.
  - `memory/INDEX.md`, `HOT.md`, `PROJECT.md`, `tasks.md`, `experiments.md`, `buglog.md`, `decisions.md` created.
  - Reusable templates `experiment.md` and `bug.md` present.
  - Historical records, decisions, bugs, and legacy handover archived.
  - Cross-file links resolve properly.
- **Evidence of Completion**: Verified file creation on disk and tested retrieval paths.
- **Last Update**: 2026-10-11

### <a id="task-001"></a>TASK-001: Autonomous Fabric Classifier Training on Expanded Dataset
- **Requirement / Source**: Master handover Section 1; user goal.
- **Status**: `paused` — as of 2026-10-14 04:42 no trainer running. Attempt 309 completed (policy stop); Attempt 310 interrupted by a second server restart after Epoch 5 (val Macro-F1 34.9–37.5%, no gain). Do not relaunch without user approval. See memory/HOT.md.
- **Completion Criteria**:
  - Test set Top-1 Accuracy >= 0.72 (verified in `training_log.json`).
  - Test set Top-3 Accuracy >= 0.90.
  - Test set Macro F1 >= 0.68.
  - Test set Worst Single-Class Recall >= 0.40.
  - Model adheres to fixed EfficientNet-B0 backbone + 14-class head.
- **Current Progress** (verified 2026-10-14 from `epoch_progress.jsonl` / `training_log.json`):
  - Attempt 309 completed with a policy stop at Epoch 20 (worst val recall 15.44% < 20%); now persisted in `training_log.json` (309 entries). `final_metrics_achieved` (split unverified): Top-1 43.28%, Macro-F1 40.48%, worst recall 17.55%.
  - Best val Macro-F1: **40.37%** (Attempt 309 Epoch 13).
  - Attempt 310 ([EXP-310](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-310-warm-start-interrupted.md)) interrupted after Epoch 5 by a server restart; no gain (val Macro-F1 34.9–37.5%). Not in `training_log.json`.
  - Which attempt/epoch `fabric_clf_best.pt` (2026-10-13 20:56) holds is unverified.
- **Dependencies & Blockers**:
  - [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md) (Polyester/Cotton recall below the 20% policy stop; unchanged warm-start retries no longer help).
  - User instruction 2026-10-14: do not start any run without asking.
- **Next Action** (all PLANNED, none done):
  1. Verify no trainer is running: `Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'python.exe' -and $_.CommandLine -match 'train.py'}`
  2. Ask the user which change to test (suggested: class-weighted focal loss per BUG-001, one change only).
  3. Create a new `planned` EXP record before any launch; do not relaunch unchanged.
  4. Optional read-only checks: per-class image counts and a Cotton/Polyester label-quality sample.
- **Supporting Records**: [EXP-304](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-304-expanded-dataset.md), [EXP-305](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-305-expanded-dataset-20ep.md), [EXP-306](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-306-expanded-dataset-in-flight.md), [EXP-307](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-307-expanded-dataset.md), [EXP-308](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-308-expanded-dataset-in-flight.md), [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md), [EXP-310](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-310-warm-start-interrupted.md), [DEC-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/DEC-001-non-commercial-data-policy.md), [DEC-002](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/DEC-002-dynamic-resource-optimization.md).
- **Last Update**: 2026-10-14 04:50

### <a id="task-002"></a>TASK-002: Temperature Calibration & Final Inference Verification
- **Requirement / Source**: Non-Negotiables Section 2.2; `integration_test.py`.
- **Status**: `todo`
- **Completion Criteria**:
  - `calibrate.py` run on accepted final weights `fabric_clf_best.pt`.
  - Calibrated temperature written to `backend/fabric_classifier/calibration/temperature.json`.
  - `python integration_test.py` passes all contract assertions.
  - Predict output returns exactly 3 descending confidence classes.
- **Dependencies & Blockers**: Blocked on TASK-001 meeting completion criteria.
- **Next Action**: Await accepted model weights from TASK-001.
- **Last Update**: 2026-10-11 16:00

### <a id="task-003"></a>TASK-003: Resolve Polyester & Smooth Fabric Recall Deficit
- **Requirement / Source**: Mistake Ledger item 6; [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md).
- **Status**: `in_progress`
- **Completion Criteria**:
  - Polyester recall exceeds >= 0.20 in validation (interim: avoid policy stop).
  - Polyester and Cotton recall both exceed >= 0.40 in test evaluation (final target).
  - High recall on textured fabrics (>70%) is preserved without regression.
- **Current State** (verified 2026-10-14):
  - Worst val recall: 17.14% (Att 309 Ep 13), 15.44% at the Att 309 policy stop (Ep 20); Att 310 Ep 1–5: 9.6–14.0%. Below the 20% stop in all cases.
  - Focal loss, hard negative mining, label smoothing change and patch scale variation have NOT been tried (planned only).
  - The ~+5%-per-attempt trend did NOT continue; unchanged retries are not expected to help.
- **Dependencies & Blockers**: No trainer running. User asked not to start runs without approval.
- **Next Action** (planned): With user approval, implement class-weighted focal loss in `train.py` as a single isolated change and record it as a new `planned` EXP record first (spec: BUG-001 "Unexplored Mitigations").
- **Supporting Records**: [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md), [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md), [EXP-310](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-310-warm-start-interrupted.md).
- **Last Update**: 2026-10-14 04:50
