import json

# Get per-class breakdown for Attempt 309 from training_log.json
with open(r"backend/fabric_classifier/training/training_log.json", "r", encoding="utf-8") as f:
    log = json.load(f)

for entry in log:
    if entry.get("attempt") == 309:
        print(f"Attempt 309 status: {entry.get('status')}")
        metrics = entry.get("final_metrics", {})
        test = metrics.get("test", {})
        print(f"Test Top-1: {test.get('accuracy')}")
        print(f"Test Macro-F1: {test.get('macro_avg', {}).get('f1-score')}")
        per_class = test.get("per_class", {})
        for cls, v in per_class.items():
            print(f"  {cls}: recall={v.get('recall'):.4f}, f1={v.get('f1_score'):.4f}")
        policy = entry.get("policy_stop_trigger")
        print(f"Stop rule: {policy}")
        print(f"Epoch history count: {len(entry.get('epoch_history', []))}")

print("Done")
