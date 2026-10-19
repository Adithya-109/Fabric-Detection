# Fabric Classifier — Project Overview & Durable Knowledge

## 1. Durable Goals & User Requirements
The objective is to train a 14-class fabric material classifier for garment analysis (personal/research use under non-commercial policy [DEC-001](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/records/DEC-001-non-commercial-data-policy.md)).

### Done Criteria (Evaluated on Test Set)
Success is determined strictly by test-set metrics on both original TextileNet and combined evaluation sets:

| Metric | Target | Verification Method |
|---|---|---|
| **Top-1 Accuracy** | >= 0.72 (72%) | Final test evaluation in `training_log.json` |
| **Top-3 Accuracy** | >= 0.90 (90%) | Final test evaluation in `training_log.json` |
| **Macro F1** | >= 0.68 | Final test evaluation in `training_log.json` |
| **Worst Single-Class Recall** | >= 0.40 (40%) | Per-class breakdown in `training_log.json` |

*Note*: Inference latency (<= 40ms) and inference VRAM (<= 300MB) are monitored for informational reporting, but are not pass/fail gates.

---

## 2. Fixed Contracts & Non-Negotiables

### 2.1 Model Architecture
- **Backbone**: `torchvision` EfficientNet-B0 (Apache 2.0).
- **Head**: `Dropout(0.3) -> Linear(1280->256) -> ReLU -> Dropout(0.2) -> Linear(256->14)`.
- Defined in [backend/fabric_classifier/model.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/model.py).

### 2.2 Class Order (Exact Indices 0–13)
Canonical ordering fixed in [backend/fabric_classifier/classes.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/classes.py):
1. `Cotton` (0), 2. `Polyester` (1), 3. `Silk` (2), 4. `Denim` (3), 5. `Linen` (4), 6. `Wool` (5), 7. `Leather` (6), 8. `Velvet` (7), 9. `Corduroy` (8), 10. `Fleece` (9), 11. `Nylon` (10), 12. `Satin` (11), 13. `Knitted` (12), 14. `Suede` (13).

### 2.3 Inference API Contract
`FabricClassifier.predict(pil_image)` in [backend/fabric_classifier/inference.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/inference.py) must return exactly 3 items in descending confidence order:
```python
[
    {"name": "Cotton", "confidence": 85.5},
    {"name": "Linen", "confidence": 10.2},
    {"name": "Polyester", "confidence": 4.3},
]
```
- Temperature scaling calibration loaded from [backend/fabric_classifier/calibration/temperature.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/calibration/temperature.json) (defaults to 1.0 if absent).
- Patch extraction extracts exactly 7 square crops from segmented interior fabric (eroding edges/zippers) and averages softmax logits.

### 2.4 Environment & Operational Rules
- Conda environment: `conda activate myenv`.
- Process guard: Never run two `train.py` writers concurrently. Singleton lock and PID check enforced.
- Low-memory GPU profile: FP16 enabled on GPU path; dynamic CPU/GPU fallback managed by `FabricMemoryManager` in [backend/fabric_classifier/memory_manager.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/memory_manager.py).

---

## 3. Project Map & Core Reference Files
- **Trainer**: [backend/fabric_classifier/training/train.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/train.py)
- **Patch Pipeline**: [backend/fabric_classifier/training/dataset.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/dataset.py)
- **Inference Wrapper**: [backend/fabric_classifier/inference.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/inference.py)
- **Class Specs**: [backend/fabric_classifier/classes.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/classes.py)
- **Model Definition**: [backend/fabric_classifier/model.py](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/model.py)
- **Active Logs**:
  - Per-epoch stream: [backend/fabric_classifier/training/epoch_progress.jsonl](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/epoch_progress.jsonl)
  - Attempt ledger: [backend/fabric_classifier/training/training_log.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/training_log.json)
  - Human postmortems: [backend/fabric_classifier/training/experiment_log.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/experiment_log.md)
  - Issues ledger: [backend/fabric_classifier/training/issues_log.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/issues_log.json)
- **Data Manifests & Counts**:
  - Class availability: [DATASETS/imaterialist_class_availability.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/DATASETS/imaterialist_class_availability.json)
  - Added manifest: [backend/fabric_classifier/training/additional_data_manifest.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/backend/fabric_classifier/training/additional_data_manifest.json)
  - Label mapping: [imaterialist_label_mapping.json](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/imaterialist_label_mapping.json)
- **Best Weights**:
  - `backend/fabric_classifier/weights/fabric_clf_best.pt`
  - `backend/fabric_classifier/weights/fabric_clf_last.pt`
- **Historical Reference**: [memory/archive/HANDOFF_legacy_2026-10-11.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/archive/HANDOFF_legacy_2026-10-11.md)
