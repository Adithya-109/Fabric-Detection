import json

path = r"backend/fabric_classifier/training/epoch_progress.jsonl"

attempts = {}
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            att = data.get("attempt")
            if att is None:
                continue
            if att not in attempts:
                attempts[att] = {"evals": []}
            if "val_macro_f1" in data:
                attempts[att]["evals"].append(data)
        except Exception:
            pass

# Show last few attempts in full detail
for att in sorted(attempts.keys())[-4:]:
    evals = attempts[att]["evals"]
    print(f"\n=== Attempt {att}: {len(evals)} evaluated epochs ===")
    for e in evals:
        print(f"  Ep {e['epoch']}: train={e['train_loss']:.4f}, val_top1={e['val_top1_accuracy']:.4f}, macro_f1={e['val_macro_f1']:.4f}, worst={e['val_worst_class_recall']:.4f}")

# Show current heartbeat status
print("\n=== Last 3 heartbeat lines ===")
with open(path, "r", encoding="utf-8") as f:
    all_lines = f.readlines()
for line in all_lines[-3:]:
    try:
        d = json.loads(line)
        if "step_heartbeat" in d:
            print(f"  Attempt {d.get('attempt')} Epoch {d.get('epoch')} Step {d.get('step')}: train_loss={d.get('train_loss_running'):.4f}")
    except Exception:
        pass
