import json
import os
import pandas as pd

base_path = r"backend/fabric_classifier/training"
training_log_path = os.path.join(base_path, "training_log.json")
epoch_progress_path = os.path.join(base_path, "epoch_progress.jsonl")
issues_log_path = os.path.join(base_path, "issues_log.json")
handoff_paths = ["HANDOFF.md", "../../HANDOFF.md", "../HANDOFF.md"]

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def load_jsonl(path):
    data = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
    return data

training_log = load_json(training_log_path)
epoch_progress = load_jsonl(epoch_progress_path)
issues_log = load_json(issues_log_path)

handoff_content = None
for hp in handoff_paths:
    if os.path.exists(hp):
        with open(hp, "r") as f:
            handoff_content = f.read()
        break

print("--- 1) Attempt Summary Table ---")
if training_log:
    rows = []
    for attempt in training_log:
        metrics = attempt.get("final_metrics_achieved", {})
        if not isinstance(metrics, dict): metrics = {}
        resource_usage = attempt.get("resource_usage", {})
        if not isinstance(resource_usage, dict): resource_usage = {}
        rows.append({
            "Attempt": attempt.get("attempt"),
            "Status": attempt.get("status"),
            "TargetsMet": attempt.get("targets_met"),
            "Top1": metrics.get("top1_accuracy"),
            "Top3": metrics.get("top3_accuracy"),
            "MacroF1": metrics.get("macro_f1"),
            "WorstRecall": metrics.get("worst_class_recall"),
            "Inf(ms)": resource_usage.get("inference_ms"),
            "VRAM(MB)": resource_usage.get("vram_mb")
        })
    df_summary = pd.DataFrame(rows)
    print(df_summary.to_string(index=False))
else:
    print("Training log empty or missing.")

print("\n--- 2) Epoch Progress Stats ---")
if epoch_progress:
    df_epoch = pd.DataFrame(epoch_progress)
    if not df_epoch.empty:
        stats = []
        att_col = "attempt" if "attempt" in df_epoch.columns else "attempt_id"
        for attempt_id in df_epoch[att_col].unique():
            subset = df_epoch[df_epoch[att_col] == attempt_id]
            triggers = subset["event"].str.contains("policy_stop_trigger", na=False).sum() if "event" in subset.columns else 0
            stats.append({
                "Attempt": attempt_id,
                "MaxEpoch": subset["epoch"].max() if "epoch" in subset.columns else "N/A",
                "BestTop1": subset["val_top1_accuracy"].max() if "val_top1_accuracy" in subset.columns else "N/A",
                "BestTop3": subset["val_top3_accuracy"].max() if "val_top3_accuracy" in subset.columns else "N/A",
                "BestMacroF1": subset["val_macro_f1"].max() if "val_macro_f1" in subset.columns else "N/A",
                "BestWorstRec": subset["val_worst_class_recall"].max() if "val_worst_class_recall" in subset.columns else "N/A",
                "StopTriggers": triggers
            })
        print(pd.DataFrame(stats).to_string(index=False))

print("\n--- 3) Underperforming Classes ---")
if training_log:
    class_metrics = {}
    for attempt in training_log:
        metrics = attempt.get("final_metrics_achieved", {})
        if not isinstance(metrics, dict): continue
        per_class = metrics.get("per_class_metrics", {})
        for cls, m in per_class.items():
            if cls not in class_metrics: class_metrics[cls] = []
            if "recall" in m: class_metrics[cls].append(m["recall"])
    
    under_rows = []
    for cls, recalls in class_metrics.items():
        if recalls:
            under_rows.append({
                "Class": cls,
                "MinRecall": min(recalls),
                "MeanRecall": sum(recalls)/len(recalls),
                "Below0.40": sum(1 for r in recalls if r < 0.40)
            })
    df_under = pd.DataFrame(under_rows)
    if not df_under.empty:
        print(df_under[df_under["Below0.40"] > 0].to_string(index=False))
    else:
        print("No underperforming classes detected with recall < 0.40.")

print("\n--- 4) Hyperparameter-change Effectiveness ---")
if training_log and len(training_log) > 1:
    for i in range(1, len(training_log)):
        prev = training_log[i-1]
        curr = training_log[i]
        hp_p = prev.get("hyperparameters_used", {})
        hp_c = curr.get("hyperparameters_used", {})
        changes = []
        if isinstance(hp_p, dict) and isinstance(hp_c, dict):
            for k in set(hp_p.keys()) | set(hp_c.keys()):
                if hp_p.get(k) != hp_c.get(k):
                    changes.append(f"{k}: {hp_p.get(k)} -> {hp_c.get(k)}")
        else:
            changes.append(f"Hyperparams format mismatch or missing: {hp_p} vs {hp_c}")
            
        m_prev = prev.get("final_metrics_achieved", {})
        m_curr = curr.get("final_metrics_achieved", {})
        def get_top1(m): return m.get("top1_accuracy") if isinstance(m, dict) else 0
        def get_f1(m): return m.get("macro_f1") if isinstance(m, dict) else 0
        d_top1 = (get_top1(m_curr) or 0) - (get_top1(m_prev) or 0)
        d_f1 = (get_f1(m_curr) or 0) - (get_f1(m_prev) or 0)
        print(f"Attempt {prev.get('attempt')} -> {curr.get('attempt')}:")
        print(f"  Changes: {', '.join(changes) if changes else 'None'}")
        print(f"  Delta Top1: {d_top1:+.4f}, Delta MacroF1: {d_f1:+.4f}")

print("\n--- 5) Issues Log Summary ---")
if issues_log:
    df_issues = pd.DataFrame(issues_log)
    if not df_issues.empty:
        print("Counts by Category/Severity:")
        print(df_issues.groupby(["category", "severity"]).size().reset_index(name="count").to_string(index=False))
        print("\nLast 10 Issues:")
        cols = ["timestamp_utc", "category", "severity", "title"]
        print(df_issues.tail(10)[[c for c in cols if c in df_issues.columns]].to_string(index=False))

print("\n--- 6) Key Constraints from HANDOFF.md ---")
if handoff_content:
    bullets = []
    for line in handoff_content.splitlines():
        if line.strip().startswith("-") or line.strip().startswith("*"):
            clean = line.strip().lstrip("-* ").strip()
            if any(kw in clean.lower() for kw in ["must", "limit", "target", "constraint", "note", "require", "fix"]):
                bullets.append(clean)
        if len(bullets) >= 8: break
    for b in bullets:
        print(f"- {b}")
else:
    print("HANDOFF.md content not available or could not be found.")
