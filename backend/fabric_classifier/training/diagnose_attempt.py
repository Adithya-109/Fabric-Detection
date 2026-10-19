import argparse
import json
from pathlib import Path
import sys

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import confusion_matrix
from torchvision import transforms


REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.fabric_classifier.classes import MATERIAL_CLASSES
from backend.fabric_classifier.model import get_model
from backend.fabric_classifier.training.evaluate import evaluate_model
from backend.fabric_classifier.training.train import (
    HYPERPARAMS,
    FabricDataset,
    build_dataloaders,
    load_and_split_data,
)


def collect_preds_labels(model: torch.nn.Module, dataloader, device: str):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            if inputs.nelement() == 0:
                continue

            inputs = inputs.to(device=device, dtype=torch.float32)
            labels = labels.to(device).long()

            if inputs.dim() == 5:
                bs, n_patches, c, h, w = inputs.shape
                inputs = inputs.view(-1, c, h, w)
                patch_outputs = model(inputs)
                outputs = patch_outputs.view(bs, n_patches, -1).mean(1)
            else:
                outputs = model(inputs)

            preds = torch.argmax(outputs, dim=1)
            all_preds.append(preds.cpu().numpy())
            all_labels.append(labels.cpu().numpy())

    if not all_labels:
        return np.array([], dtype=np.int64), np.array([], dtype=np.int64)

    return np.concatenate(all_labels), np.concatenate(all_preds)


def top_confusions(cm: np.ndarray, class_names: list[str], top_k: int = 15):
    pairs = []
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if i == j:
                continue
            count = int(cm[i, j])
            if count <= 0:
                continue
            pairs.append(
                {
                    "true": class_names[i],
                    "pred": class_names[j],
                    "count": count,
                }
            )

    pairs.sort(key=lambda x: x["count"], reverse=True)
    return pairs[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Diagnose a training attempt from checkpoint.")
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("backend/fabric_classifier/weights/fabric_clf_last.pt"),
        help="Checkpoint path to diagnose.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("backend/fabric_classifier/training/attempt_diagnostics.json"),
        help="Output JSON path.",
    )
    parser.add_argument(
        "--expected-attempt",
        type=int,
        default=None,
        help="Optional expected attempt number; raises if checkpoint attempt differs.",
    )
    args = parser.parse_args()

    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    attempt = checkpoint.get("attempt")
    if args.expected_attempt is not None and int(attempt) != int(args.expected_attempt):
        raise RuntimeError(
            f"Checkpoint attempt={attempt} does not match expected={args.expected_attempt}"
        )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    (train_files, train_labels), (val_files, val_labels), (test_files, test_labels) = load_and_split_data()

    val_transforms = transforms.Compose(
        [
            transforms.Resize((HYPERPARAMS["IMG_SIZE"], HYPERPARAMS["IMG_SIZE"])),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    train_dataset = FabricDataset(train_files, train_labels, val_transforms, HYPERPARAMS["N_PATCHES_TRAIN"], is_train=True)
    val_dataset = FabricDataset(val_files, val_labels, val_transforms, HYPERPARAMS["N_PATCHES_INFER"], is_train=False)
    test_dataset = FabricDataset(test_files, test_labels, val_transforms, HYPERPARAMS["N_PATCHES_INFER"], is_train=False)

    _, val_loader, test_loader = build_dataloaders(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        test_dataset=test_dataset,
        train_labels=train_labels,
        device=device,
        batch_size=4,
        num_workers=0,
        pin_memory=False,
    )

    class_counts = np.bincount(train_labels, minlength=len(MATERIAL_CLASSES)).astype(np.float32)
    class_weights = class_counts.sum() / (len(MATERIAL_CLASSES) * np.maximum(class_counts, 1.0))
    class_weights_tensor = torch.tensor(class_weights, dtype=torch.float32, device=device)
    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor, label_smoothing=HYPERPARAMS["LABEL_SMOOTHING"])

    model = get_model(num_classes=len(MATERIAL_CLASSES)).to(device)
    model.load_state_dict(checkpoint["model_state_dict"], strict=False)
    model = model.float()

    val_metrics = evaluate_model(model, val_loader, device, MATERIAL_CLASSES, criterion=criterion)
    test_metrics = evaluate_model(model, test_loader, device, MATERIAL_CLASSES, criterion=criterion)

    val_y, val_p = collect_preds_labels(model, val_loader, device)
    test_y, test_p = collect_preds_labels(model, test_loader, device)

    val_cm = confusion_matrix(val_y, val_p, labels=np.arange(len(MATERIAL_CLASSES))) if val_y.size else np.zeros((len(MATERIAL_CLASSES), len(MATERIAL_CLASSES)), dtype=np.int64)
    test_cm = confusion_matrix(test_y, test_p, labels=np.arange(len(MATERIAL_CLASSES))) if test_y.size else np.zeros((len(MATERIAL_CLASSES), len(MATERIAL_CLASSES)), dtype=np.int64)

    weak_classes = []
    per_class_test = test_metrics.get("per_class_metrics", {})
    for class_name in MATERIAL_CLASSES:
        recall = float((per_class_test.get(class_name) or {}).get("recall", 0.0))
        if recall < 0.40:
            weak_classes.append({"class": class_name, "recall": recall})

    output = {
        "attempt": attempt,
        "checkpoint_epoch": checkpoint.get("epoch"),
        "checkpoint_best_val_score": checkpoint.get("best_val_score"),
        "val_metrics": val_metrics,
        "test_metrics": test_metrics,
        "val_confusion_matrix": val_cm.tolist(),
        "test_confusion_matrix": test_cm.tolist(),
        "val_top_confusions": top_confusions(val_cm, MATERIAL_CLASSES, top_k=15),
        "test_top_confusions": top_confusions(test_cm, MATERIAL_CLASSES, top_k=15),
        "weak_classes_below_0_40_test_recall": weak_classes,
        "class_order": MATERIAL_CLASSES,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")

    summary = {
        "attempt": output["attempt"],
        "checkpoint_epoch": output["checkpoint_epoch"],
        "val_top1": output["val_metrics"].get("top1_accuracy"),
        "val_macro_f1": output["val_metrics"].get("macro_f1"),
        "val_worst_recall": output["val_metrics"].get("worst_class_recall"),
        "test_top1": output["test_metrics"].get("top1_accuracy"),
        "test_macro_f1": output["test_metrics"].get("macro_f1"),
        "test_worst_recall": output["test_metrics"].get("worst_class_recall"),
        "weak_classes_below_0_40_test_recall": weak_classes,
        "output_file": str(args.output),
    }
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    main()
