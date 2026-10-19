import json
import os
import pandas as pd
from datetime import datetime

base_path = r"backend/fabric_classifier/training"
training_log_path = os.path.join(base_path, "training_log.json")
epoch_progress_path = os.path.join(base_path, "epoch_progress.jsonl")
issues_log_path = os.path.join(base_path, "issues_log.json")
handoff_path = "HANDOFF.md"

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

print("--- 1) Attempt Summary Table ---")
if training_log and "attempts" in training_log:
    rows = []
    for attempt in training_log["attempts"]:
        metrics = attempt.get("metrics", {})
        resource_usage = attempt.get("resource_usage", {})
        rows.append({
            "Attempt": attempt.get("id"),
            "Status": attempt.get("status"),
            "TargetsMet": attempt.get("targets_met"),
            "Top1": metrics.get("top1"),
            "Top3": metrics.get("top3"),
            "MacroF1": metrics.get("macro_f1"),
            "WorstRecall": metrics.get("worst_recall"),
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
        for attempt_id in df_epoch["attempt_id"].unique():
            subset = df_epoch[df_epoch["attempt_id"] == attempt_id]
            # Policy stop triggers
            triggers = subset[subset["event"].str.contains("policy_stop_trigger", na=False)] if "event" in subset.columns else []
            
            # Metrics are usually in a 'metrics' dict or flat
            # Assuming flat for this check
            stats.append({
                "Attempt": attempt_id,
                "MaxEpoch": subset["epoch"].max() if "epoch" in subset.columns else "N/A",
                "BestTop1": subset["val_top1"].max() if "val_top1" in subset.columns else "N/A",
                "BestTop3": subset["val_top3"].max() if "val_top3" in subset.columns else "N/A",
                "BestMacroF1": subset["val_macro_f1"].max() if "val_macro_f1" in subset.columns else "N/A",
                "BestWorstRec": subset["val_worst_class_recall"].max() if "val_worst_class_recall" in subset.columns else "N/A",
                "StopTriggers": len(triggers)
            })
        print(pd.DataFrame(stats).to_string(index=False))
else:
    print("Epoch progress empty.")

print("\n--- 3) Underperforming Classes ---")
if training_log and "attempts" in training_log:
    class_metrics = {}
    for attempt in training_log["attempts"]:
        per_class = attempt.get("metrics", {}).get("per_class", {})
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
        print("No underperforming classes detected or metrics missing.")

print("\n--- 4) Hyperparameter-change Effectiveness ---")
if training_log and "attempts" in training_log and len(training_log["attempts"]) > 1:
    attempts = training_log["attempts"]
    for i in range(1, len(attempts)):
        prev = attempts[i-1]
        curr = attempts[i]
        
        # Identify changes in hyperparameters
        h_prev = prev.get("hyperparameters", {})
        h_curr = curr.get("hyperparameters", {})
        changes = []
        for k in set(h_prev.keys()) | set(h_curr.keys()):
            if h_prev.get(k) != h_curr.get(k):
                changes.append(f"{k}: {h_prev.get(k)} -> {h_curr.get(k)}")
        
        m_prev = prev.get("metrics", {})
        m_curr = curr.get("metrics", {})
        d_top1 = (m_curr.get("top1", 0) or 0) - (m_prev.get("top1", 0) or 0)
        d_f1 = (m_curr.get("macro_f1", 0) or 0) - (m_prev.get("macro_f1", 0) or 0)
        
        print(f"Attempt {prev['id']} -> {curr['id']}:")
        print(f"  Changes: {', '.join(changes) if changes else 'None'}")
        print(f"  Delta Top1: {d_top1:+.4f}, Delta MacroF1: {d_f1:+.4f}")

print("\n--- 5) Issues Log Summary ---")
if issues_log:
    if isinstance(issues_log, list):
        df_issues = pd.DataFrame(issues_log)
    else:
        df_issues = pd.DataFrame(issues_log.get("issues", []))
    
    if not df_issues.empty:
        print("Counts by Category/Severity:")
        print(df_issues.groupby(["category", "severity"]).size().reset_index(name="count").to_string(index=False))
        print("\nLast 10 Issues:")
        print(df_issues.tail(10)[["timestamp", "category", "severity", "description"]].to_string(index=False))
else:
    print("Issues log empty.")

print("\n--- 6) Key Constraints from HANDOFF.md ---")
if os.path.exists(handoff_path):
    with open(handoff_path, "r") as f:
        lines = f.readlines()
    bullets = []
    for line in lines:
        if line.strip().startswith("-") or line.strip().startswith("*"):
            # Simple heuristic for "key constraints or notes"
            clean = line.strip().lstrip("-* ").strip()
            if any(kw in clean.lower() for kw in ["must", "limit", "target", "constraint", "note", "require", "fix"]):
                bullets.append(clean)
        if len(bullets) >= 8: break
    for b in bullets:
        print(f"- {b}")
else:
    print("HANDOFF.md not found.")
