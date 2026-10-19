import json

with open("backend/fabric_classifier/training/training_log.json", "r") as f:
    data = json.load(f)

for x in data:
    if x.get("attempt") == 308:
        print("Keys:", x.keys())
        m = x.get("final_metrics_achieved", {})
        print("Metrics keys:", m.keys())
        pcm = m.get("per_class_metrics", {})
        for k in ["Cotton", "Polyester"]:
            print(k, pcm.get(k))
