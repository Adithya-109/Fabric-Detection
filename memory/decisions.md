# Architecture & Project Decisions Ledger

## 1. Decision Making Protocol
Significant architecture, licensing, data, or scope choices are recorded here.
Each entry records:
- **Scope**: Subsystems, files, and workflows governed by the decision.
- **Rationale**: Why this path was selected over alternatives.
- **Evidence**: Measured results, logs, or formal requirements supporting the choice.
- **Alternatives Considered**: Rejected alternatives and specific reasons for rejection.
- **Reconsideration Conditions**: Explicit triggers that would justify revisiting the decision.

---

## 2. Decisions Index Table

| ID | Title / Search Terms | Scope | Status | Date | Link | Summary & Evidence |
|---|---|---|---|---|---|---|
| **DEC-001** | Non-Commercial Research Classification & Dataset Use | Entire project / Licensing | `active` | 2026-10-10 | [DEC-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/DEC-001-non-commercial-data-policy.md) | Permitted iBUG and iMaterialist in final model; removed 800-image cap |
| **DEC-002** | Dynamic DataLoader Worker Scaling (NUM_WORKERS=8) | Training throughput | `active` | 2026-10-10 | [DEC-002](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/DEC-002-dynamic-resource-optimization.md) | Scaled from 0 to 8 workers + pinned memory; cut epoch time from 65m to 32m |
| **DEC-003** | Fixed Backbone & Head Architecture Contract | Model definition | `active` | 2026-10-08 | [PROJECT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/PROJECT.md#21-model-architecture) | EfficientNet-B0 + 2-layer classifier head strictly required by design |
| **DEC-004** | 7-Patch Dynamic Extraction & Inference API Contract | Inference pipeline | `active` | 2026-10-08 | [PROJECT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/PROJECT.md#23-inference-api-contract) | 7 interior crops with edge avoidance, top 3 descending confidence dicts |
| **DEC-005** | Strict Unambiguous Material Label Mapping | Data preprocessing | `active` | 2026-10-10 | [Archive](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/HANDOFF_legacy_2026-10-11.md#19-phase-2-label-mapping) | Dropped compound materials to prevent label noise; mapped explicit synonyms |
