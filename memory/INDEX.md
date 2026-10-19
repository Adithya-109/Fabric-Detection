# Project Memory System Index

## 1. Startup Instructions
At the start of every session or after a context reset:
1. **Read Entry Points**: Read [memory/INDEX.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/INDEX.md) and [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md).
2. **Follow Route**: Use the Conditional Routing Table below to load only the specific files required for the current task.
3. **Verify State**: Verify process state and file timestamps before acting; do not rely on unverified claims.
4. **Checkpoint**: Update records and [HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) before handing off.

---

## 2. Common Operating Rules
- **Epistemic Hygiene**: Strictly separate verified facts, user requirements, reported history, hypotheses, and decisions. Attach evidence paths and dates.
- **Single Canonical Home**: Each fact or result has one authoritative record; index tables link to it; [HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) summarizes the live state.
- **Search Before Reading**: Search file basenames, IDs, and symbols using ripgrep before reading large logs or record collections.
- **Update Sequence**: Write or update detailed records in `memory/records/` first, update the corresponding index table (`tasks.md`, `experiments.md`, `buglog.md`, `decisions.md`), then update [HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md).
- **Process Guard**: In this repository, verify whether a `train.py` background process is running before executing any training or script that accesses GPU/weights.

---

## 3. Conditional Routing Table

| Task / Situation | Files & Records to Retrieve |
|---|---|
| **Starting or Resuming Work** | [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) -> active task in [memory/tasks.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/tasks.md) -> referenced records in `memory/records/` -> active source files for next step. |
| **Planning an Experiment** | [memory/experiments.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/experiments.md) -> matching prior experiment records -> [memory/buglog.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/buglog.md) blockers -> [memory/decisions.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/decisions.md) -> read [memory/templates/experiment.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/templates/experiment.md) to draft record. |
| **Investigating or Fixing Bugs** | [memory/buglog.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/buglog.md) -> matching bug records -> related experiment records -> affected source code -> read [memory/templates/bug.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/templates/bug.md) to create/update record. |
| **Making Architecture / Scope Decisions** | [memory/PROJECT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/PROJECT.md) -> [memory/decisions.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/decisions.md) -> supporting experiment/bug records. |
| **Researching, Analyzing, or Writing** | [memory/PROJECT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/PROJECT.md) -> relevant task in [memory/tasks.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/tasks.md) -> target data manifest or analysis scripts. |
| **Switching Tasks** | Checkpoint unfinished work in current record -> update status in [memory/tasks.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/tasks.md) -> update [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) -> retrieve new task records. |
| **Completing Milestone / Handoff** | Record verification evidence in canonical record -> mark status in [memory/tasks.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/tasks.md) / index -> update [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md). |

---

## 4. Memory Registry

| File / Directory | Purpose | Read Triggers | Write Triggers |
|---|---|---|---|
| [memory/INDEX.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/INDEX.md) | Entry point, routing table, operating rules, and file registry | Startup, reset, or routing lookup | System additions, new record types |
| [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) | Current active handover, live progress, next action | Startup, reset, or checking active status | Checkpoint, task switch, handoff |
| [memory/PROJECT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/PROJECT.md) | Durable goals, fixed contracts, project map, stable facts | Onboarding, scope review, architecture check | Goal, contract, or architecture changes |
| [memory/tasks.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/tasks.md) | Authoritative task ledger, requirements, and completion criteria | Task planning, task switching, status checks | Task created, status changed, milestone met |
| [memory/experiments.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/experiments.md) | Experiment procedure and compact searchable attempt index | Before planning/running experiments | Experiment planned, status updated, run completed |
| [memory/buglog.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/buglog.md) | Debugging procedure and compact searchable bug ledger | Diagnosing failures, checking known blockers | New issue discovered, mitigated, or resolved |
| [memory/decisions.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/decisions.md) | Significant architecture, licensing, and scoping decisions | Scope queries, evaluating major trade-offs | New decision finalized or reconsidered |
| [memory/templates/](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/templates/) | Blank schemas for `experiment.md` and `bug.md` | When creating new experiment/bug records | When structural schema fields are refined |
| [memory/records/](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/) | Canonical detailed records (`EXP-*`, `BUG-*`, `DEC-*`) | When inspecting specific experiment/bug/decision details | Meaningful event, run result, or investigation step |
| [memory/archive/](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/) | Inactive historical handovers and superseded records | Deep historical audits, recovering prior context | When archiving superseded documents |
