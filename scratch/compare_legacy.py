import json

with open("backend/fabric_classifier/training/training_log.json", "r") as f:
    data = json.load(f)

print("=== COMPLETED ATTEMPTS BEFORE EXPANDED DATASET (< 304) ===")
for x in data:
    att = x.get("attempt")
    st = x.get("status")
    if st in ["completed", "completed_policy_stop"] and att < 304:
        m = x.get("final_metrics_achieved")
        if isinstance(m, dict):
            top1 = m.get("top1_accuracy", 0)
            top3 = m.get("top3_accuracy", 0)
            f1 = m.get("macro_f1", 0)
            w_rec = m.get("worst_class_recall", 0)
            print(f"Attempt {att:2d} | Status: {st:23s} | Top1: {top1:.4f} | Top3: {top3:.4f} | F1: {f1:.4f} | WorstRec: {w_rec:.4f} | Stop: {x.get('reason_for_retry', 'N/A')}")

print("\n=== COMPLETED ATTEMPTS ON EXPANDED DATASET (>= 304) ===")
for x in data:
    att = x.get("attempt")
    st = x.get("status")
    if st in ["completed", "completed_policy_stop"] and att >= 304:
        m = x.get("final_metrics_achieved")
        if isinstance(m, dict):
            top1 = m.get("top1_accuracy", 0)
            top3 = m.get("top3_accuracy", 0)
            f1 = m.get("macro_f1", 0)
            w_rec = m.get("worst_class_recall", 0)
            print(f"Attempt {att:3d} | Status: {st:23s} | Top1: {top1:.4f} | Top3: {top3:.4f} | F1: {f1:.4f} | WorstRec: {w_rec:.4f} | Stop: {x.get('reason_for_retry', 'N/A')}")
