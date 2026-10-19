import json
import os
import re
from datetime import datetime
from collections import defaultdict

def safe_get(d, keys, default=None):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def load_json(path):
    if not os.path.exists(path): return {}
    try:
        with open(path, 'r') as f: return json.load(f)
    except: return {}

def load_jsonl(path):
    data = []
    if not os.path.exists(path): return data
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip(): data.append(json.loads(line))
    except: pass
    return data

def load_file(path):
    if not os.path.exists(path): return ""
    with open(path, 'r', encoding='utf-8') as f: return f.read()

# Paths
BASE_DIR = "backend/fabric_classifier/training"
TRAINING_LOG_PATH = os.path.join(BASE_DIR, "training_log.json")
EPOCH_PROGRESS_PATH = os.path.join(BASE_DIR, "epoch_progress.jsonl")
ISSUES_LOG_PATH = os.path.join(BASE_DIR, "issues_log.json")
HANDOFF_PATH = "HANDOFF.md"
NEW_DATASET_AUDIT_PATH = os.path.join(BASE_DIR, "new_dataset_audit.json")

# 1. Parse Data
training_log = load_json(TRAINING_LOG_PATH)
epoch_progress = load_jsonl(EPOCH_PROGRESS_PATH)
issues_log = load_json(ISSUES_LOG_PATH)
handoff_content = load_file(HANDOFF_PATH)
new_dataset_audit = load_json(NEW_DATASET_AUDIT_PATH)

attempts = training_log.get("attempts", [])
epochs_by_attempt = defaultdict(list)
for ep in epoch_progress:
    attempts_id = ep.get("attempt")
    if attempts_id is not None:
        epochs_by_attempt[attempts_id].append(ep)

# 2. Process Stats
attempt_summaries = []
for a in attempts:
    mid = a.get("metrics", {})
    final = mid.get("final_test", {})
    attempt_summaries.append({
        "attempt": a.get("attempt_id"),
        "status": a.get("status"),
        "targets_met": final.get("targets_met"),
        "top1": final.get("top1"),
        "top3": final.get("top3"),
        "macro_f1": final.get("macro_f1"),
        "worst_recall": final.get("worst_recall"),
        "inference_ms": final.get("latency_ms"),
        "vram_mb": final.get("vram_usage_mb"),
        "reason_for_retry": a.get("reason_for_retry"),
        "params": a.get("hyperparameters", {})
    })

epoch_diagnostics = []
for aid, eps in epochs_by_attempt.items():
    max_epoch = max([e.get("epoch", 0) for e in eps]) if eps else 0
    completed_eval = len([e for e in eps if "val_top1" in e])
    best_top1 = max([e.get("val_top1", 0) for e in eps if "val_top1" in e], default=0)
    best_top3 = max([e.get("val_top3", 0) for e in eps if "val_top3" in e], default=0)
    best_f1 = max([e.get("val_macro_f1", 0) for e in eps if "val_macro_f1" in e], default=0)
    best_worst_recall = max([e.get("val_worst_recall", 0) for e in eps if "val_worst_recall" in e], default=0)
    policy_stops = len([e for e in eps if e.get("stop_triggered")])
    epoch_diagnostics.append({
        "attempt": aid,
        "max_epoch": max_epoch,
        "eval_count": completed_eval,
        "best_top1": best_top1,
        "best_top3": best_top3,
        "best_f1": best_f1,
        "best_worst_recall": best_worst_recall,
        "policy_stop": policy_stops
    })

# 3. Chronic Weekly Classes
class_recalls = defaultdict(list)
for a in attempts:
    recalls = safe_get(a, ["metrics", "final_test", "class_recalls"], {})
    for cls, val in recalls.items():
        class_recalls[cls].append(val)

chronic_weakness = []
for cls, vals in class_recalls.items():
    mean_r = sum(vals)/len(vals)
    chronic_weakness.append({
        "class": cls,
        "mean_recall": mean_r,
        "min_recall": min(vals),
        "max_recall": max(vals),
        "count_below_40": len([v for v in vals if v < 0.40]),
        "attempts": len(vals)
    })
chronic_weakness.sort(key=lambda x: x["mean_recall"])

# 4. Hyperparameter Change Impact
hp_impacts = []
for i in range(1, len(attempt_summaries)):
    prev = attempt_summaries[i-1]
    curr = attempt_summaries[i]
    
    diff_params = []
    p1, p2 = prev["params"], curr["params"]
    all_keys = set(p1.keys()) | set(p2.keys())
    for k in sorted(all_keys):
        if p1.get(k) != p2.get(k):
            diff_params.append(f"{k}: {p1.get(k)}->{p2.get(k)}")
    
    def delta(k):
        v1, v2 = prev.get(k), curr.get(k)
        if v1 is not None and v2 is not None: return v2 - v1
        return 0
        
    hp_impacts.append({
        "transition": f"{prev['attempt']} -> {curr['attempt']}",
        "changes": "; ".join(diff_params),
        "delta_top1": delta("top1"),
        "delta_f1": delta("macro_f1"),
        "delta_worst_recall": delta("worst_recall")
    })

# 5. Issues Log Summary
issues_list = issues_log.get("issues", [])
issue_counts = {
    "category": defaultdict(int),
    "severity": defaultdict(int),
    "status": defaultdict(int)
}
for iss in issues_list:
    issue_counts["category"][iss.get("category")] += 1
    issue_counts["severity"][iss.get("severity")] += 1
    issue_counts["status"][iss.get("status")] += 1

latest_issues = sorted(issues_list, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]

# 6. HANDOFF Constraints
handoff_bullets = re.findall(r"^- (.*)", handoff_content, re.M)
constraints = handoff_bullets[:10]

# 7. Implications
new_dataset_counts = new_dataset_audit.get("class_distribution", {})
# Merge new dataset counts with weak classes
weak_implications = []
for cw in chronic_weakness[:10]:
    cls = cw["class"]
    count = new_dataset_counts.get(cls, 0)
    weak_implications.append(f"{cls}: Mean Recall {cw['mean_recall']:.4f}, New Samples Available: {count}")

# OUTPUTS
history_analysis_json = {
    "attempt_summaries": attempt_summaries,
    "epoch_diagnostics": epoch_diagnostics,
    "chronic_weakness": chronic_weakness,
    "hp_impacts": hp_impacts,
    "issue_summary": {k: dict(v) for k, v in issue_counts.items()},
    "constraints": constraints,
    "implications": weak_implications
}

with open(os.path.join(BASE_DIR, "history_analysis.json"), 'w') as f:
    json.dump(history_analysis_json, f, indent=2)

# Generate Markdown
md = "# Training History Analysis\n\n"

md += "## 1. Attempt Summary\n"
md += "| Attempt | Status | Targets Met | Top 1 | Top 3 | Macro F1 | Worst Recall | Inference (ms) | VRAM (MB) | Reason |\n"
md += "|---|---|---|---|---|---|---|---|---|---|\n"
for a in attempt_summaries:
    md += f"| {a['attempt']} | {a['status']} | {a['targets_met']} | {a['top1'] or 0:.4f} | {a['top3'] or 0:.4f} | {a['macro_f1'] or 0:.4f} | {a['worst_recall'] or 0:.4f} | {a['inference_ms'] or 0:.2f} | {a['vram_mb'] or 0:.0f} | {a['reason_for_retry']} |\n"

md += "\n## 2. Epoch Progress Diagnostics\n"
md += "| Attempt | Max Epoch | Eval Count | Best Top 1 | Best Top 3 | Best Macro F1 | Best Worst Recall | Stop Triggers |\n"
md += "|---|---|---|---|---|---|---|---|\n"
for d in epoch_diagnostics:
    md += f"| {d['attempt']} | {d['max_epoch']} | {d['eval_count']} | {d['best_top1']:.4f} | {d['best_top3']:.4f} | {d['best_f1']:.4f} | {d['best_worst_recall']:.4f} | {d['policy_stop']} |\n"

md += "\n## 3. Chronic Class Weakness\n"
md += "| Class | Mean Recall | Min Recall | Max Recall | <0.40 Count | Attempts |\n"
md += "|---|---|---|---|---|---|\n"
for cw in chronic_weakness:
    md += f"| {cw['class']} | {cw['mean_recall']:.4f} | {cw['min_recall']:.4f} | {cw['max_recall']:.4f} | {cw['count_below_40']} | {cw['attempts']} |\n"

md += "\n## 4. Hyperparameter Change Impact\n"
md += "| Transition | Changes | Δ Top 1 | Δ Macro F1 | Δ Worst Recall |\n"
md += "|---|---|---|---|---|---|\n"
for h in hp_impacts:
    md += f"| {h['transition']} | {h['changes']} | {h['delta_top1']:.4f} | {h['delta_f1']:.4f} | {h['delta_worst_recall']:.4f} |\n"

md += "\n## 5. Issues Log Summary\n"
md += "### Counts\n"
for categ, counts in issue_counts.items():
    md += f"- **{categ.capitalize()}**: " + ", ".join([f"{k}: {v}" for k, v in counts.items()]) + "\n"

md += "\n### Latest 10 Issues\n"
md += "| Timestamp | Title | Category | Severity | Status | Action |\n"
md += "|---|---|---|---|---|---|\n"
for iss in latest_issues:
    md += f"| {iss.get('timestamp')} | {iss.get('title')} | {iss.get('category')} | {iss.get('severity')} | {iss.get('status')} | {iss.get('action_taken')} |\n"

md += "\n## 6. HANDOFF Constraints Digest\n"
for c in constraints:
    md += f"- {c}\n"

md += "\n## 7. Implications for New Datasets\n"
for imp in weak_implications:
    md += f"- {imp}\n"

with open(os.path.join(BASE_DIR, "history_analysis.md"), 'w', encoding='utf-8') as f:
    f.write(md)

# Console Output
total_attempts = len(attempts)
latest_attempt = attempts[-1].get("attempt_id") if attempts else "None"
best_top1 = max(attempt_summaries, key=lambda x: x["top1"] or 0) if attempt_summaries else {}
best_top3 = max(attempt_summaries, key=lambda x: x["top3"] or 0) if attempt_summaries else {}
best_f1 = max(attempt_summaries, key=lambda x: x["macro_f1"] or 0) if attempt_summaries else {}
best_wrc = max(attempt_summaries, key=lambda x: x["worst_recall"] or 0) if attempt_summaries else {}

print(f"Total Attempts: {total_attempts}")
print(f"Latest Logged Attempt: {latest_attempt}")
if attempt_summaries:
    print(f"Best Top1: {best_top1.get('top1'):.4f} (Attempt {best_top1.get('attempt')})")
    print(f"Best Top3: {best_top3.get('top3'):.4f} (Attempt {best_top3.get('attempt')})")
    print(f"Best Macro F1: {best_f1.get('macro_f1'):.4f} (Attempt {best_f1.get('attempt')})")
    print(f"Best Worst Recall: {best_wrc.get('worst_recall'):.4f} (Attempt {best_wrc.get('attempt')})")
print("\nTop 5 Weakest Classes (Mean Recall):")
for cw in chronic_weakness[:5]:
    print(f"- {cw['class']}: {cw['mean_recall']:.4f}")
