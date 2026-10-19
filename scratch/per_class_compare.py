import json

with open("backend/fabric_classifier/training/training_log.json", "r") as f:
    data = json.load(f)

def get_att(n):
    for x in data:
        if x.get("attempt") == n:
            return x
    return None

a15 = get_att(15)
a22 = get_att(22)
a308 = get_att(308)

classes = [
    "Cotton", "Polyester", "Silk", "Denim", "Linen",
    "Wool", "Leather", "Velvet", "Corduroy", "Fleece",
    "Nylon", "Satin", "Knitted", "Suede"
]

print(f"{'Class':10s} | {'Att 15 Recall':13s} {'Att 15 F1':10s} | {'Att 22 Recall':13s} {'Att 22 F1':10s} | {'Att 308 Recall':14s} {'Att 308 F1':10s}")
print("-" * 85)

pcm15 = a15.get("final_metrics_achieved", {}).get("per_class_metrics", {})
pcm22 = a22.get("final_metrics_achieved", {}).get("per_class_metrics", {})
pcm308 = a308.get("final_metrics_achieved", {}).get("per_class_metrics", {})

for c in classes:
    r15 = pcm15.get(c, {}).get("recall", 0)
    f15 = pcm15.get(c, {}).get("f1_score", 0)
    r22 = pcm22.get(c, {}).get("recall", 0)
    f22 = pcm22.get(c, {}).get("f1_score", 0)
    r308 = pcm308.get(c, {}).get("recall", 0)
    f308 = pcm308.get(c, {}).get("f1_score", 0)
    print(f"{c:10s} | {r15*100:10.1f}%   {f15*100:6.1f}%   | {r22*100:10.1f}%   {f22*100:6.1f}%   | {r308*100:11.1f}%   {f308*100:6.1f}%")
