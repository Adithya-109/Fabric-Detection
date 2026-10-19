import json

log = json.load(open(r'backend/fabric_classifier/training/training_log.json'))
print(f"Total entries in training_log.json: {len(log)}")
for e in log[-4:]:
    att = e["attempt"]
    status = e.get("status","?")
    policy = e.get("policy_stop_trigger")
    hist = e.get("epoch_history",[])
    dur = e.get("training_duration_seconds", 0)
    print(f"\nAttempt {att}: status={status}")
    if policy:
        print(f"  Stop: {policy}")
    print(f"  Epoch count: {len(hist)}, Duration: {dur:.0f}s ({dur/3600:.1f}h)")
    if hist:
        last = hist[-1]
        print(f"  Last Epoch ({last['epoch']}): train={last['train_loss']:.4f}, top1={last['val_top1_accuracy']:.4f}, macro_f1={last['val_macro_f1']:.4f}")
    # Per-class if available
    fm = e.get("final_metrics", {})
    test = fm.get("test", {})
    if test:
        pc = test.get("per_class", {})
        print("  Per-class recall:")
        for cls, v in pc.items():
            print(f"    {cls}: recall={v.get('recall',0):.4f}")
