# Copilot Persistent Instructions — Fabric Classifier Project

This file is always in context. If you are mid-task on the fabric classifier training
job, re-read these constraints before every action. They do not change.

---

## Active Task

You are autonomously building and training a fabric material classifier.
Full task specification is in: `COPILOT_TRAINING_PROMPT.md`
Full architecture spec is in: `FABRIC_CLASSIFIER_SPEC.md`

Do not stop until ALL done criteria below are met.
Do not ask the user questions — make all decisions yourself.

---

## Hardware Limits (Never Exceed)

- GPU: RTX 3050 **6GB VRAM** — budget **≤ 300MB** for this model (3 other models share the GPU)
- RAM: **8GB total** — keep DataLoader workers ≤ 4, batch size ≤ 32
- CPU: i5-13420H, 8 cores, Windows 11
- Use **FP16 on GPU** at all times for this model

---

## Output Location (Never Change This)

All deliverable files go inside:
```
backend/fabric_classifier/
```
Training scripts go inside `backend/fabric_classifier/training/`
Weights file: `backend/fabric_classifier/weights/fabric_clf_best.pt`
Temperature file: `backend/fabric_classifier/calibration/temperature.json`

---

## Model (Non-Negotiable)

- EfficientNet-B0 from `torchvision` (Apache 2.0)
- No other backbone
- Custom head: Dropout(0.3) → Linear(1280→256) → ReLU → Dropout(0.2) → Linear(256→14)

---

## The 14 Classes (Exact Order — Index Matters)

```python
MATERIAL_CLASSES = [
    "Cotton",    # 0
    "Polyester", # 1
    "Silk",      # 2
    "Denim",     # 3
    "Linen",     # 4
    "Wool",      # 5
    "Leather",   # 6
    "Velvet",    # 7
    "Corduroy",  # 8
    "Fleece",    # 9
    "Nylon",     # 10
    "Satin",     # 11
    "Knitted",   # 12
    "Suede",     # 13
]
```

---

## Done Criteria (All Must Be Met Before Stopping)

| Metric | Target |
|---|---|
| Top-1 Accuracy (test set) | ≥ 72% |
| Top-3 Accuracy (test set) | ≥ 90% |
| Macro F1 (test set) | ≥ 0.68 |
| Worst single-class Recall | ≥ 40% |
| Inference time (7 patches, GPU) | ≤ 40ms |
| VRAM at inference | ≤ 300MB |

If any target is missed after a full training run, apply the auto-retry adjustments
defined in `COPILOT_TRAINING_PROMPT.md` and retrain. Never declare done early.

---

## Integration Contract (The API Must Match Exactly)

`FabricClassifier.predict(pil_image)` must return:
```python
[
    {"name": "Cotton",    "confidence": 85.5},
    {"name": "Linen",     "confidence": 10.2},
    {"name": "Polyester", "confidence": 4.3},
]
```
- Exactly 3 items
- Descending confidence order
- `name` must be from MATERIAL_CLASSES exactly
- `confidence` is 0–100 float

This return format cannot change — it plugs directly into `backend/wardrobe_analytics.py`.

---

## Dataset Location

TextileNet repo already extracted at:
`C:\Users\A0SKZ\STORE\ALL_CODE\BUISINESS\Clothes_Machine_Learning\DATASETS\TextileNet-main`

Images must be downloaded using the scripts inside that folder.
Limit to **800 images per class maximum** to control data usage.

---

## If You Are Resuming Mid-Task

Check `backend/fabric_classifier/training/training_log.json` to see what has already
been attempted. Do not repeat completed steps. Continue from where the log shows
the last completed action.
