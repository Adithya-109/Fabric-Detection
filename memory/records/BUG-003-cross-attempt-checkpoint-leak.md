# Bug Record: BUG-003 — Cross-Attempt Best-Checkpoint Reuse on Warm Start

- **ID**: BUG-003
- **Title**: Stale best checkpoint metadata and evaluation reused across distinct attempts
- **TASK IDs**: TASK-001
- **Status**: resolved
- **Created**: 2026-10-09 18:00:00
- **Updated**: 2026-10-10 02:00:00

---

## 1. Problem Description & Impact
- **Symptom**: Attempts 17 and 18 reported identical final test metrics despite different epoch trajectories.
- **Expected Behavior**: Each attempt must track its own attempt-local best metrics and only evaluate the weights corresponding to its current attempt.
- **Actual Behavior**: On warm-start, stale best checkpoint metadata from an earlier attempt was reused, leading to invalid progress interpretation.
- **Affected Area**: `backend/fabric_classifier/training/train.py` checkpointing and final evaluation routines.
- **Impact & Severity**: High / Corruptive. Led to false reporting of attempt outcomes.

## 2. Environment & Reproduction
- **Reproduction Steps**:
  1. Complete attempt N with a best checkpoint saved.
  2. Launch attempt N+1 with warm-start.
  3. Attempt N+1 finishes and reads stale metadata from attempt N checkpoint.
- **Inputs & Configuration**: `train.py` resume logic.
- **Environment & Version**: Python trainer runtime.
- **Original Evidence References**:
  - Code Location: `backend/fabric_classifier/training/train.py`
  - Documentation: Mistake #8 in master handoff
  - Verification Date: 2026-10-10

## 3. Investigation & Attempts
- **Attempts Made & Linked Records**:
  - Analyzed `train.py` checkpoint loading logic and metadata reconciliation.
- **Ruled-Out Hypotheses & Evidence**:
  - Model convergence coincidence: ruled out by inspecting identical float bitstrings in `training_log.json`.

## 4. Workaround & Next Diagnostic
- **Workaround**: None needed; permanent code fix applied.

## 5. Resolution & Verification
- **Resolution Summary**: Hardened `train.py`:
  1. On attempt mismatch, warm-start weights only and reset per-attempt best tracking.
  2. Recompute best from same-attempt `history` when resume metadata is inconsistent.
  3. Final evaluation only loads `fabric_clf_best.pt` if checkpoint attempt matches current attempt; otherwise falls back to attempt-local last checkpoint.
- **Resolution Verification**: verified via [backend/fabric_classifier/training/train.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/train.py)
- **Verification Evidence**: Attempts 304, 305, and 306 tracked distinct attempt IDs, checkpoints, and metrics without collision.
- **Evidence Status for Consequential Claims**:
  - Cross-attempt checkpoint leak fixed in code: verified
