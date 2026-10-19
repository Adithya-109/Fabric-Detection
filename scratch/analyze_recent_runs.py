import json

path = r"backend/fabric_classifier/training/epoch_progress.jsonl"
attempts = {}
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            att = data.get("attempt")
            if att not in attempts:
                attempts[att] = {"eval_epochs": []}
            if "val_macro_f1" in data:
                attempts[att]["eval_epochs"].append({
                    "epoch": data.get("epoch"),
                    "train_loss": data.get("train_loss"),
                    "val_loss": data.get("val_loss"),
                    "val_top1": data.get("val_top1_accuracy"),
                    "val_macro_f1": data.get("val_macro_f1"),
                    "worst_recall": data.get("val_worst_class_recall")
                })
        except Exception:
            pass

for att in sorted(attempts.keys()):
    evals = attempts[att]["eval_epochs"]
    print(f"=== Attempt {att} (Total Evaluated Epochs: {len(evals)}) ===")
    for e in evals[-5:]:
        print(f"  Epoch {e['epoch']}: train_loss={e['train_loss']:.4f}, val_loss={e['val_loss']:.4f}, val_top1={e['val_top1']:.4f}, val_macro_f1={e['val_macro_f1']:.4f}, worst_recall={e['worst_recall']:.4f}")

# Also check training_log.json
try:
    with open(r"backend/fabric_classifier/training/training_log.json", "r", encoding="utf-8") as f:
        log = json.load(f)
    print("\n=== training_log.json Attempts ===")
    for entry in log[-5:]:
        print(f"  Attempt {entry.get('attempt')}: status={entry.get('status')}, top1={entry.get('test_top1_accuracy')}, macro_f1={entry.get('test_macro_f1')}, worst_recall={entry.get('test_worst_class_recall')}, reason={entry.get('reason')}")
except Exception as ex:
    print(f"Error reading training_log.json: {ex}")
