# Experiment Record: [EXP-ID] — [Descriptive Title]

- **ID**: EXP-[ID]
- **Title**: [Concise descriptive title of experiment]
- **TASK IDs**: [Linked TASK-ID, e.g., TASK-001]
- **Status**: [planned | running | completed | failed | inconclusive | interrupted]
- **Created**: [YYYY-MM-DD HH:MM:SS]
- **Updated**: [YYYY-MM-DD HH:MM:SS]

---

## 1. Objective & Hypothesis
- **Question**: [What question does this experiment test?]
- **Hypothesis**: [Testable hypothesis regarding expected impact]
- **Rationale**: [Brief technical reason for this change]
- **Related Attempts**: [Previous attempt/experiment IDs or none]
- **Reason for Repeat**: [Not applicable | Explicit reason such as changed data, code fix, or replication]

## 2. Configuration & Baseline
- **Source / Version**: [Commit hash, branch, or script version]
- **Data Version**: [Dataset paths/manifests used, sample counts]
- **Environment**: [Hardware, OS, conda env `myenv`, worker counts]
- **Inputs & Seeds**: [Random seeds, hyperparameter dictionary]
- **Baseline**: [Reference baseline run or control metrics]
- **Planned Changes**: [Single isolated change vs baseline]
- **Success Criteria**: [Target metrics: top-1, macro-F1, worst-class recall]
- **Stopping Condition**: [Epoch limit, plateau window, or policy stop rule]

## 3. Procedure & Execution
- **Exact Commands / Procedure**:
  ```powershell
  [Exact commands executed]
  ```
- **Affected Files**: [File paths modified or created]
- **Execution State**: [not yet run | running | completed | interrupted | aborted]

## 4. Observed Results & Evidence
- **Observed Results & Measurements**:
  - Top-1 Accuracy: [Value or not yet run]
  - Top-3 Accuracy: [Value or not yet run]
  - Macro F1: [Value or not yet run]
  - Worst Single-Class Recall: [Value or not yet run]
  - Resource Usage: [VRAM MB, training time, throughput it/s]
- **Hypothesis Outcome**: [supported | disproven | inconclusive | not evaluated] *(Separated from execution status)*
- **Original Evidence References**:
  - Artifact / Log Path: [Path to log, jsonl, or weights file]
  - Run ID / PID: [Identifier or run record]
  - Verification Date: [YYYY-MM-DD]
- **Evidence Status for Consequential Claims**:
  - [Claim 1]: [verified | reported | hypothesis | unverified | superseded]

## 5. Interpretation & Next Action
- **Interpretation**: [What the observed results indicate]
- **Limitations & Uncertainty**: [Known caveats or confounding factors]
- **Related Records**: [BUG IDs, DEC IDs, or subsequent EXP IDs]
- **Next Action / Retry Condition**: [Next step or condition for re-running]
