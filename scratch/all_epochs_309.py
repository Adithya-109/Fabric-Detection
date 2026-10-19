import json

with open("backend/fabric_classifier/training/epoch_progress.jsonl", "r") as f:
    lines = f.readlines()

print("=== ALL COMPLETED EPOCHS FOR ATTEMPT 309 ===")
for line in lines:
    try:
        data = json.loads(line)
        if data.get("attempt") == 309 and "val_top1_accuracy" in data:
            ep = data.get("epoch")
            t1 = data.get("val_top1_accuracy", 0) * 100
            t3 = data.get("val_top3_accuracy", 0) * 100
            f1 = data.get("val_macro_f1", 0) * 100
            wr = data.get("val_worst_class_recall", 0) * 100
            tl = data.get("train_loss", 0)
            print(f"Ep {ep:2d} | Top-1: {t1:5.2f}% | Top-3: {t3:5.2f}% | Macro-F1: {f1:5.2f}% | WorstRec: {wr:5.2f}% | TrainLoss: {tl:.4f}")
    except:
        pass
