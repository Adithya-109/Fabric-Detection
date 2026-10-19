import json

with open("backend/fabric_classifier/training/training_log.json", "r", encoding="utf-8") as f:
    log = json.load(f)

for a in log:
    if a.get("attempt") == 308:
        print("=== Attempt 308 Final ===")
        print("Status:", a.get("status"))
        print("Policy Stop:", a.get("policy_stop_trigger"))
        print("Final Metrics:", a.get("final_metrics_achieved"))
        print("Best Checkpoint:", a.get("best_checkpoint"))
        break
