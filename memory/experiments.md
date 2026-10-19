# Experiment Protocol & Index

## 1. Experiment Operating Procedure
Before starting an experiment:
1. **Prior Review**: Review related attempts in this index, unresolved issues in [memory/buglog.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/buglog.md), and decisions in [memory/decisions.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/decisions.md).
2. **Formulation**: Define clear question, testable hypothesis, technical rationale, control baseline, planned change (change ONE thing at a time), success criteria (Top-1 >= 0.72, Macro-F1 >= 0.68, Worst Recall >= 0.40), and stopping condition.
3. **De-duplication**: Check if the experiment duplicates an earlier run. Re-run only with an explicit reason (e.g., changed code, corrected data, deliberate replication).
4. **Pre-execution Record**: Initialize an experiment record in `memory/records/` using [memory/templates/experiment.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/templates/experiment.md) with status `planned` or `running` before executing.
5. **Execution & Evidence**: Record exact commands, dataset version, hardware profile, and original evidence references (log paths, run IDs).
6. **Post-execution Assessment**: Record observed metrics, distinguish execution status from hypothesis outcome (a successfully completed experiment may disprove its hypothesis), and identify next action or retry condition. Update this index and [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md).

Template reference: [memory/templates/experiment.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/templates/experiment.md).

---

## 2. Experiments Index Table

| ID | Title / Search Terms | Status | Affected Area | Last Update | Link | Outcome / Retry Condition |
|---|---|---|---|---|---|---|
| **EXP-304** | Expanded Dataset Baseline Run (232k images) | `completed` | Data / Model | 2026-10-10 | [EXP-304](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-304-expanded-dataset.md) | Top-1: 28.66%, Macro-F1: 28.83%; severe class shift; retry with longer horizon |
| **EXP-305** | 20-Epoch Training on Expanded Dataset | `completed` | Training / Workers | 2026-10-11 | [EXP-305](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-305-expanded-dataset-20ep.md) | Top-1: 31.68%, Macro-F1: 31.76%; stopped at Ep 20 by Polyester recall (2.65% < 20%) |
| **EXP-306** | Warm-Start Retry from Ep 6 Best Weights | `completed` | Training / Checkpoints | 2026-10-12 | [EXP-306](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-306-expanded-dataset-in-flight.md) | Top-1: 33.69%, Macro-F1: 33.17%; stopped at Ep 20 by Polyester recall (4.88% < 20%) |
| **EXP-307** | Warm-Start Retry from Attempt 306 | `completed` | Training / Multi-Run | 2026-10-12 | [EXP-307](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-307-expanded-dataset.md) | Top-1: 35.59%, Macro-F1: 34.91%; stopped at Ep 20 by Polyester recall (8.44% < 20%) |
| **EXP-308** | Warm-Start Retry from Attempt 307 | `completed` | Training / Multi-Run | 2026-10-13 | [EXP-308](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-308-expanded-dataset-in-flight.md) | Top-1: 38.97%, Macro-F1: 37.87%, Worst: 12.67%; 12/14 classes >= 40% recall |
| **EXP-309** | Warm-Start Retry from Attempt 308 | `completed` | Training / Multi-Run | 2026-10-14 | [EXP-309](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-309-expanded-dataset-in-flight.md) | Resumed after restart; policy stop at Ep 20 (worst 15.44% < 20%). `final_metrics_achieved`: Top-1 43.28%, Macro-F1 40.48%, worst 17.55% (split unverified); best val Macro-F1 40.37% (Ep 13) |
| **EXP-310** | Warm-Start Continuation from Attempt 309 (no change) | `interrupted` | Training | 2026-10-14 | [EXP-310](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/EXP-310-warm-start-interrupted.md) | Killed by server restart after Ep 5; val Macro-F1 34.9-37.5%, worst recall 9.6-14.0%, no gain; do not relaunch unchanged |
| **EXP-015** | Historical Best Legacy Dataset Run (~800/class) | `completed` | Training | 2026-10-09 | [Archive](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/HANDOFF_legacy_2026-10-11.md#61-summary-through-attempt-16) | Top-1: 58.2%, Macro-F1: 58.3%; hit data ceiling, prompted non-commercial expansion |
| **EXP-022** | Commercial-Safe Policy Plateau Stop | `completed` | Training / Gating | 2026-10-10 | [Archive](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/HANDOFF_legacy_2026-10-11.md#62-detailed-attempts-17-22-persisted) | Top-1: 55.37%, Macro-F1: 56.13%; triggered plateau window policy stop |
