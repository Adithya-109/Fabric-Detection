import json

with open("backend/fabric_classifier/training/training_log.json", "r", encoding="utf-8") as f:
    log = json.load(f)

for a in log:
    if a.get("attempt", 0) >= 304:
        att = a.get("attempt")
        status = a.get("status")
        history = a.get("history", [])
        n_epochs = len(history)
        if history:
            final_loss = history[-1].get("train_loss", 0.0)
            best_top1 = max(h.get("val_top1_accuracy", 0.0) for h in history) * 100
            best_top3 = max(h.get("val_top3_accuracy", 0.0) for h in history) * 100
            best_f1 = max(h.get("val_macro_f1", 0.0) for h in history) * 100
            best_worst = max(h.get("val_worst_class_recall", 0.0) for h in history) * 100
            stop = a.get("policy_stop_trigger", {}).get("rule", "none")
            print(f"Attempt {att}: Status={status}, Epochs={n_epochs}, FinalLoss={final_loss:.4f}, BestTop1={best_top1:.2f}%, BestTop3={best_top3:.2f}%, BestMacroF1={best_f1:.2f}%, BestWorstRecall={best_worst:.2f}%, StopRule={stop}")
