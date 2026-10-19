import json

with open("backend/fabric_classifier/training/training_log.json", "r") as f:
    data = json.load(f)

def get_att(n):
    for x in data:
        if x.get("attempt") == n:
            return x
    return None

classes = [
    "Cotton", "Polyester", "Silk", "Denim", "Linen",
    "Wool", "Leather", "Velvet", "Corduroy", "Fleece",
    "Nylon", "Satin", "Knitted", "Suede"
]

def calc_p_r_f1(att_num):
    att = get_att(att_num)
    if not att:
        return {}
    pcm = att.get("final_metrics_achieved", {}).get("per_class_metrics", {})
    res = {}
    for c in classes:
        rec = pcm.get(c, {}).get("recall", 0)
        f1 = pcm.get(c, {}).get("f1_score", 0)
        # F1 = 2 * P * R / (P + R) => 1/P = 2/F1 - 1/R => P = (F1 * R) / (2 * R - F1)
        if rec > 0 and f1 > 0 and (2 * rec - f1) > 0:
            prec = (f1 * rec) / (2 * rec - f1)
        else:
            prec = 0.0
        res[c] = {"precision": prec, "recall": rec, "f1": f1}
    return res

p308 = calc_p_r_f1(308)
p15 = calc_p_r_f1(15)

print("=== ATTEMPT 308 (CURRENT EXPANDED DATASET) ===")
print(f"{'Class':10s} | {'Precision':10s} | {'Recall':10s} | {'F1-Score':10s}")
print("-" * 46)
for c in classes:
    m = p308.get(c, {})
    print(f"{c:10s} | {m.get('precision', 0)*100:8.2f}%  | {m.get('recall', 0)*100:8.2f}%  | {m.get('f1', 0)*100:8.2f}%")

print("\n=== ATTEMPT 15 (PRE-EXPANSION BASELINE) ===")
print(f"{'Class':10s} | {'Precision':10s} | {'Recall':10s} | {'F1-Score':10s}")
print("-" * 46)
for c in classes:
    m = p15.get(c, {})
    print(f"{c:10s} | {m.get('precision', 0)*100:8.2f}%  | {m.get('recall', 0)*100:8.2f}%  | {m.get('f1', 0)*100:8.2f}%")
