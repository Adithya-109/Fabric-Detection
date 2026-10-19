import json

with open("backend/fabric_classifier/training/epoch_progress.jsonl", "r") as f:
    lines = f.readlines()

for line in lines[-1000:]:
    try:
        data = json.loads(line)
        if data.get("attempt") == 309 and "val_top1_accuracy" in data:
            print("Completed Epoch:", data.get("epoch"))
            print("Train Loss:", data.get("train_loss"))
            print("Val Loss:", data.get("val_loss"))
            print("Val Top1:", data.get("val_top1_accuracy"))
            print("Val Top3:", data.get("val_top3_accuracy"))
            print("Val Macro F1:", data.get("val_macro_f1"))
            print("Val Worst Recall:", data.get("val_worst_class_recall"))
            print("-" * 30)
    except:
        pass
