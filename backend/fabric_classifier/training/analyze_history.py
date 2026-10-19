import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def load_jsonl(path: Path):
    rows = []
    if not path.exists():
        return rows
    try:
        with path.open("r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rows.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return rows
    return rows


def fmt_num(value):
    if isinstance(value, (int, float)):
        return f"{float(value):.4f}"
    return "N/A"


def sort_attempt_key(value):
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(out)


def get_metric(entry, key):
    metrics = entry.get("final_metrics_achieved")
    if isinstance(metrics, dict):
        return metrics.get(key)
    return None


def parse_handoff_digest(handoff_text, max_bullets=10):
    bullets = []
    for line in handoff_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped)
        if len(bullets) >= max_bullets:
            break
    return bullets


def extract_dataset_target_counts(dataset_audit):
    counts_by_dataset = defaultdict(lambda: defaultdict(int))

    for ds in dataset_audit.get("datasets", []):
        ds_name = ds.get("name", "unknown")
        rows = ds.get("per_semantic_class")
        if not isinstance(rows, list) or not rows:
            rows = ds.get("per_top_class", [])

        for row in rows:
            if not isinstance(row, dict):
                continue
            target = row.get("mapped_target_class")
            valid = row.get("images_valid", 0)
            if isinstance(target, str) and isinstance(valid, (int, float)):
                counts_by_dataset[ds_name][target] += int(valid)

    return counts_by_dataset


def main():
    repo_root = Path(__file__).resolve().parents[3]
    training_dir = repo_root / "backend" / "fabric_classifier" / "training"

    training_log_path = training_dir / "training_log.json"
    epoch_progress_path = training_dir / "epoch_progress.jsonl"
    issues_log_path = training_dir / "issues_log.json"
    handoff_path = repo_root / "HANDOFF.md"
    dataset_audit_path = training_dir / "new_dataset_audit.json"

    training_log = load_json(training_log_path, default=[])
    epoch_progress = load_jsonl(epoch_progress_path)
    issues_log = load_json(issues_log_path, default=[])
    handoff_text = handoff_path.read_text(encoding="utf-8") if handoff_path.exists() else ""
    dataset_audit = load_json(dataset_audit_path, default={"datasets": []})

    attempt_rows = []
    best_by_metric = {
        "top1_accuracy": (None, None),
        "top3_accuracy": (None, None),
        "macro_f1": (None, None),
        "worst_class_recall": (None, None),
    }

    for entry in training_log:
        attempt = entry.get("attempt")
        status = entry.get("status", "N/A")
        targets_met = entry.get("targets_met", False)

        top1 = get_metric(entry, "top1_accuracy")
        top3 = get_metric(entry, "top3_accuracy")
        macro_f1 = get_metric(entry, "macro_f1")
        worst_recall = get_metric(entry, "worst_class_recall")

        infer = entry.get("inference_metrics") if isinstance(entry.get("inference_metrics"), dict) else {}
        inf_ms = infer.get("inference_time_ms")
        vram_mb = infer.get("vram_mb")

        attempt_rows.append(
            [
                attempt,
                status,
                targets_met,
                fmt_num(top1),
                fmt_num(top3),
                fmt_num(macro_f1),
                fmt_num(worst_recall),
                fmt_num(inf_ms),
                fmt_num(vram_mb),
                str(entry.get("reason_for_retry", ""))[:180],
            ]
        )

        for metric_key, metric_value in [
            ("top1_accuracy", top1),
            ("top3_accuracy", top3),
            ("macro_f1", macro_f1),
            ("worst_class_recall", worst_recall),
        ]:
            cur_best, _ = best_by_metric[metric_key]
            if isinstance(metric_value, (int, float)) and (cur_best is None or metric_value > cur_best):
                best_by_metric[metric_key] = (float(metric_value), attempt)

    epoch_by_attempt = defaultdict(lambda: {
        "max_epoch": 0,
        "eval_rows": [],
        "policy_stop_count": 0,
    })

    for row in epoch_progress:
        attempt = row.get("attempt")
        epoch = row.get("epoch")
        if isinstance(epoch, int):
            epoch_by_attempt[attempt]["max_epoch"] = max(epoch_by_attempt[attempt]["max_epoch"], epoch)

        if isinstance(row.get("policy_stop_trigger"), dict):
            epoch_by_attempt[attempt]["policy_stop_count"] += 1

        if "val_top1_accuracy" in row:
            epoch_by_attempt[attempt]["eval_rows"].append(row)

    epoch_summary_rows = []
    for attempt in sorted(epoch_by_attempt.keys(), key=sort_attempt_key):
        payload = epoch_by_attempt[attempt]
        eval_rows = payload["eval_rows"]

        best_top1 = max((r.get("val_top1_accuracy") for r in eval_rows if isinstance(r.get("val_top1_accuracy"), (int, float))), default=None)
        best_top3 = max((r.get("val_top3_accuracy") for r in eval_rows if isinstance(r.get("val_top3_accuracy"), (int, float))), default=None)
        best_macro = max((r.get("val_macro_f1") for r in eval_rows if isinstance(r.get("val_macro_f1"), (int, float))), default=None)
        best_worst_recall = max((r.get("val_worst_class_recall") for r in eval_rows if isinstance(r.get("val_worst_class_recall"), (int, float))), default=None)

        epoch_summary_rows.append(
            [
                attempt,
                payload["max_epoch"],
                len(eval_rows),
                fmt_num(best_top1),
                fmt_num(best_top3),
                fmt_num(best_macro),
                fmt_num(best_worst_recall),
                payload["policy_stop_count"],
            ]
        )

    class_recalls = defaultdict(list)
    class_attempts_below_040 = defaultdict(int)

    for entry in training_log:
        final_metrics = entry.get("final_metrics_achieved")
        if not isinstance(final_metrics, dict):
            continue
        per_class = final_metrics.get("per_class_metrics")
        if not isinstance(per_class, dict):
            continue

        for cls, cls_payload in per_class.items():
            if not isinstance(cls_payload, dict):
                continue
            recall = cls_payload.get("recall")
            if isinstance(recall, (int, float)):
                r = float(recall)
                class_recalls[cls].append(r)
                if r < 0.40:
                    class_attempts_below_040[cls] += 1

    weakness_rows = []
    for cls, recalls in class_recalls.items():
        weakness_rows.append(
            [
                cls,
                fmt_num(sum(recalls) / len(recalls)),
                fmt_num(min(recalls)),
                fmt_num(max(recalls)),
                class_attempts_below_040.get(cls, 0),
                len(recalls),
            ]
        )

    weakness_rows.sort(key=lambda r: float(r[1]) if r[1] != "N/A" else 999.0)

    transition_rows = []
    for idx in range(1, len(training_log)):
        prev = training_log[idx - 1]
        cur = training_log[idx]

        prev_hp = prev.get("hyperparameters_used") if isinstance(prev.get("hyperparameters_used"), dict) else {}
        cur_hp = cur.get("hyperparameters_used") if isinstance(cur.get("hyperparameters_used"), dict) else {}

        changed_keys = []
        for key in sorted(set(prev_hp.keys()) | set(cur_hp.keys())):
            if prev_hp.get(key) != cur_hp.get(key):
                changed_keys.append(f"{key}: {prev_hp.get(key)} -> {cur_hp.get(key)}")

        prev_top1 = get_metric(prev, "top1_accuracy")
        cur_top1 = get_metric(cur, "top1_accuracy")
        prev_f1 = get_metric(prev, "macro_f1")
        cur_f1 = get_metric(cur, "macro_f1")
        prev_worst = get_metric(prev, "worst_class_recall")
        cur_worst = get_metric(cur, "worst_class_recall")

        d_top1 = (float(cur_top1) - float(prev_top1)) if isinstance(cur_top1, (int, float)) and isinstance(prev_top1, (int, float)) else None
        d_f1 = (float(cur_f1) - float(prev_f1)) if isinstance(cur_f1, (int, float)) and isinstance(prev_f1, (int, float)) else None
        d_worst = (float(cur_worst) - float(prev_worst)) if isinstance(cur_worst, (int, float)) and isinstance(prev_worst, (int, float)) else None

        transition_rows.append(
            [
                f"{prev.get('attempt')} -> {cur.get('attempt')}",
                "; ".join(changed_keys[:6]) + ("; ..." if len(changed_keys) > 6 else "") if changed_keys else "no changes",
                fmt_num(d_top1),
                fmt_num(d_f1),
                fmt_num(d_worst),
            ]
        )

    category_counts = Counter()
    severity_counts = Counter()
    status_counts = Counter()

    for issue in issues_log:
        if not isinstance(issue, dict):
            continue
        category_counts[str(issue.get("category", "unknown"))] += 1
        severity_counts[str(issue.get("severity", "unknown"))] += 1
        status_counts[str(issue.get("status", "unknown"))] += 1

    latest_10_issues = issues_log[-10:] if isinstance(issues_log, list) else []
    latest_10_issue_rows = []
    for issue in latest_10_issues:
        if not isinstance(issue, dict):
            continue
        latest_10_issue_rows.append([
            issue.get("timestamp_utc", "N/A"),
            issue.get("category", "N/A"),
            issue.get("severity", "N/A"),
            str(issue.get("title", ""))[:120],
            str(issue.get("action_taken", ""))[:120],
            issue.get("status", "N/A"),
        ])

    handoff_bullets = parse_handoff_digest(handoff_text, max_bullets=10)

    target_counts_by_dataset = extract_dataset_target_counts(dataset_audit)

    weakest_classes = [r[0] for r in weakness_rows[:5]]
    implication_lines = []
    implication_lines.append(
        "Weak-class pressure is concentrated in: " + (", ".join(weakest_classes) if weakest_classes else "N/A")
    )

    for ds_name, ds_counts in target_counts_by_dataset.items():
        covered = [f"{cls}:{count}" for cls, count in sorted(ds_counts.items(), key=lambda kv: kv[1], reverse=True)]
        implication_lines.append(f"{ds_name} mapped target counts -> " + (", ".join(covered) if covered else "none"))

    implication_lines.append(
        "Microscope dataset contributes texture-only views and lacks full 14-class coverage; best used as targeted augmentation for mapped classes only."
    )
    implication_lines.append(
        "iBUG dataset is research-only licensed and can be used only for experimentation; final production weights must be retrained without iBUG samples."
    )
    implication_lines.append(
        "Given weak recalls in Polyester/Velvet/Nylon family classes, limited iBUG class additions likely help short-term recall but introduce domain/licensing debt."
    )

    analysis_json = {
        "attempt_summary_rows": attempt_rows,
        "epoch_summary_rows": epoch_summary_rows,
        "weakness_rows": weakness_rows,
        "transition_rows": transition_rows,
        "issues": {
            "category_counts": dict(category_counts),
            "severity_counts": dict(severity_counts),
            "status_counts": dict(status_counts),
            "latest_10": latest_10_issue_rows,
        },
        "handoff_bullets": handoff_bullets,
        "dataset_target_counts": {
            ds_name: dict(counts) for ds_name, counts in target_counts_by_dataset.items()
        },
        "best_by_metric": {
            k: {"value": v[0], "attempt": v[1]} for k, v in best_by_metric.items()
        },
    }

    analysis_json_path = training_dir / "history_analysis.json"
    analysis_md_path = training_dir / "history_analysis.md"

    analysis_json_path.write_text(json.dumps(analysis_json, indent=2), encoding="utf-8")

    md_lines = []
    md_lines.append("# History Analysis")
    md_lines.append("")
    md_lines.append("## Attempt Summary")
    md_lines.append(md_table(
        [
            "attempt",
            "status",
            "targets_met",
            "top1",
            "top3",
            "macro_f1",
            "worst_recall",
            "inference_ms",
            "vram_mb",
            "reason_for_retry",
        ],
        attempt_rows,
    ))
    md_lines.append("")

    md_lines.append("## Epoch Progress Diagnostics")
    md_lines.append(md_table(
        [
            "attempt",
            "max_epoch",
            "eval_rows",
            "best_val_top1",
            "best_val_top3",
            "best_val_macro_f1",
            "best_val_worst_recall",
            "policy_stop_triggers",
        ],
        epoch_summary_rows,
    ))
    md_lines.append("")

    md_lines.append("## Chronic Class Weakness")
    md_lines.append(md_table(
        [
            "class",
            "mean_recall",
            "min_recall",
            "max_recall",
            "attempts_recall_lt_0_40",
            "attempts_represented",
        ],
        weakness_rows,
    ))
    md_lines.append("")

    md_lines.append("## Hyperparameter Change Impact")
    md_lines.append(md_table(
        [
            "transition",
            "major_param_changes",
            "delta_top1",
            "delta_macro_f1",
            "delta_worst_recall",
        ],
        transition_rows,
    ))
    md_lines.append("")

    md_lines.append("## Issues Log Summary")
    md_lines.append(f"- Category counts: {dict(category_counts)}")
    md_lines.append(f"- Severity counts: {dict(severity_counts)}")
    md_lines.append(f"- Status counts: {dict(status_counts)}")
    md_lines.append("")
    md_lines.append("### Latest 10 Issues")
    md_lines.append(md_table(
        ["timestamp_utc", "category", "severity", "title", "action_taken", "status"],
        latest_10_issue_rows,
    ))
    md_lines.append("")

    md_lines.append("## HANDOFF Constraints Digest")
    if handoff_bullets:
        for bullet in handoff_bullets:
            md_lines.append(f"- {bullet[2:] if bullet.startswith('- ') else bullet}")
    else:
        md_lines.append("- No bullet constraints found in HANDOFF.md")
    md_lines.append("")

    md_lines.append("## Implications For New Datasets")
    for line in implication_lines:
        md_lines.append(f"- {line}")
    md_lines.append("")

    analysis_md_path.write_text("\n".join(md_lines), encoding="utf-8")

    total_attempts = len(training_log)
    latest_attempt = training_log[-1].get("attempt") if training_log else None

    print(f"total_attempts={total_attempts}")
    print(f"latest_logged_attempt={latest_attempt}")

    for metric in ["top1_accuracy", "top3_accuracy", "macro_f1", "worst_class_recall"]:
        payload = best_by_metric[metric]
        print(f"best_{metric}={fmt_num(payload[0])} attempt={payload[1]}")

    print("top5_weakest_classes_by_mean_recall=" + ",".join(weakest_classes))
    print(f"history_analysis_md={analysis_md_path.as_posix()}")
    print(f"history_analysis_json={analysis_json_path.as_posix()}")


if __name__ == "__main__":
    main()
