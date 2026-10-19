# Debugging Protocol & Bug Log

## 1. Debugging Operating Procedure
When an issue, crash, or blocking quality bottleneck occurs:
1. **Search Before Filing**: Search this log and `memory/records/` for matching symptoms or error strings. Avoid duplicate entries.
2. **Characterize Problem**: Document symptom, expected vs. actual behavior, affected subsystem, and impact (specifically whether it blocks [memory/tasks.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/tasks.md) active tasks).
3. **Capture Original Evidence**: Record error traces, reproduction commands, environment details, and file locations with timestamps.
4. **Discriminating Investigation**: Formulate falsifiable hypotheses. If an attempt produces no new information, pivot hypotheses or collect diagnostic evidence; do not repeat identical failed attempts under unchanged conditions.
5. **Workarounds vs. Resolutions**: A workaround allows status `mitigated`, but the issue remains open if underlying cause or task requirements are unmet.
6. **Verification Standard**: Mark an issue `resolved` ONLY when verified with direct evidence (e.g., passing automated tests, confirmed metrics, or clean logs).
7. **Checkpointing**: Checkpoint the bug record, update this index and [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md).

Template reference: [memory/templates/bug.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/templates/bug.md).

---

## 2. Bug & Blocker Index Table

| ID | Title / Search Terms | Status | Affected Area | Last Update | Link | Essential Outcome / Blocker |
|---|---|---|---|---|---|---|
| **BUG-001** | Chronic Low Recall on Polyester & Cotton / Smooth Fabrics | `open` | Training / Loss / Recall | 2026-10-13 | [BUG-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-001-polyester-weak-recall.md) | Blocks TASK-001; worst recall 17.14% (Att309 Ep13); 20% threshold not yet cleared; focal loss not yet tried |
| **BUG-002** | Targeted Top-Up Downloader Failures on Windows | `mitigated` | Data Pipeline / Scripts | 2026-10-10 | [BUG-002](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-002-targeted-downloads-failure.md) | Mitigated by iMaterialist parquet integration; all classes > 150 |
| **BUG-003** | Stale Best-Checkpoint Reuse on Warm-Start | `resolved` | `train.py` / Checkpoints | 2026-10-10 | [BUG-003](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/BUG-003-cross-attempt-checkpoint-leak.md) | Fixed in `train.py`; warm-start resets per-attempt best tracking |
| **BUG-004** | Direct-Script Import Failure in `train.py` | `resolved` | `train.py` / Imports | 2026-10-09 | [Archive](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/HANDOFF_legacy_2026-10-11.md#7-mistake-ledger-critical-consolidated) | Fixed via fallback absolute-import sys.path injection |
| **BUG-005** | Concurrent `train.py` Writer Race Condition | `resolved` | Runtime / Process Guard | 2026-10-09 | [Archive](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/HANDOFF_legacy_2026-10-11.md#7-mistake-ledger-critical-consolidated) | Fixed via singleton lock file and active PID checks |
| **BUG-006** | Server Restart Killed Trainer at Attempt 309 Epoch 19 | `resolved` | Process / Infrastructure | 2026-10-13 | — | Trainer was at Ep 19 step 58,000/58,083 when system restarted. best.pt preserved from Ep 13. Resolved by re-launching in next session as Att310. |
