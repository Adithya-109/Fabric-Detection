import json

with open("backend/fabric_classifier/training/training_log.json", "r", encoding="utf-8") as f:
    log = json.load(f)

for a in log[-3:]:
    att = a.get("attempt")
    print(f"\n================ ATTEMPT {att} ================")
    print("Keys:", list(a.keys()))
    print("Status:", a.get("status"))
    print("Policy Stop Trigger:", a.get("policy_stop_trigger"))
    print("Final Metrics Achieved:", a.get("final_metrics_achieved"))
    print("Best Checkpoint:", a.get("best_checkpoint"))
    params = a.get("hyperparameters", {})
    print("Learning Rates:", params.get("LR_BACKBONE"), params.get("LR_HEAD"), "Patience:", params.get("PATIENCE"))
