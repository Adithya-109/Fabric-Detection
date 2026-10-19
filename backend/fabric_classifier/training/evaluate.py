import torch
from sklearn.metrics import accuracy_score, f1_score, recall_score
import numpy as np

def top_k_accuracy(output: torch.Tensor, target: torch.Tensor, k=3):
    """Computes the top-k accuracy for the given predictions and targets."""
    with torch.no_grad():
        if target.numel() == 0:
            return 0.0
        k = min(k, output.size(1))
        _, pred = output.topk(k, 1, True, True)
        correct = pred.eq(target.view(-1, 1)).any(dim=1)
        return correct.float().mean().item()

def evaluate_model(model, dataloader, device, class_names, criterion=None):
    """Evaluates the model on a given dataset."""
    model.eval()
    all_outputs = []
    all_labels = []
    total_loss = 0.0
    total_samples = 0
    
    with torch.no_grad():
        for inputs, labels in dataloader:
            # Filter out corrupted samples that were not caught by collate_fn
            if inputs.nelement() == 0:
                continue
            inputs = inputs.to(device=device, dtype=torch.float32)
            labels = labels.to(device).long()
            
            # Handle multiple patches for validation/test
            if inputs.dim() == 5: # (batch, n_patches, channels, h, w)
                bs, n_patches, c, h, w = inputs.shape
                inputs = inputs.view(-1, c, h, w)
                
                patch_outputs = model(inputs)
                
                # Average predictions across patches
                outputs = patch_outputs.view(bs, n_patches, -1).mean(1)
            else:
                outputs = model(inputs)

            if criterion is not None:
                batch_loss = criterion(outputs, labels)
                total_loss += batch_loss.item() * labels.size(0)
                total_samples += labels.size(0)

            all_outputs.append(outputs.cpu())
            all_labels.append(labels.cpu())

    if not all_labels:
        return {
            "loss": float("inf") if criterion is not None else 0.0,
            "top1_accuracy": 0,
            "top3_accuracy": 0,
            "macro_f1": 0,
            "worst_class_recall": 0,
            "class_recall": [],
            "per_class_metrics": {}
        }

    all_outputs = torch.cat(all_outputs)
    all_labels = torch.cat(all_labels)
    loss_value = (total_loss / total_samples) if total_samples > 0 else (0.0 if criterion is None else float("inf"))
    
    _, all_preds = torch.max(all_outputs, 1)

    # Calculate metrics
    accuracy = accuracy_score(all_labels.numpy(), all_preds.numpy())
    top3_acc = top_k_accuracy(all_outputs, all_labels, k=3)
    macro_f1 = f1_score(all_labels.numpy(), all_preds.numpy(), average='macro', zero_division=0)
    
    # Detailed per-class metrics
    recall_per_class = np.atleast_1d(
        recall_score(
            all_labels.numpy(),
            all_preds.numpy(),
            average=None,
            zero_division=0,
            labels=np.arange(len(class_names)),
        )
    ).astype(np.float32)
    f1_per_class = np.atleast_1d(
        f1_score(
            all_labels.numpy(),
            all_preds.numpy(),
            average=None,
            zero_division=0,
            labels=np.arange(len(class_names)),
        )
    ).astype(np.float32)

    worst_class_recall = float(np.min(recall_per_class)) if recall_per_class.size > 0 else 0.0

    per_class_metrics = {}
    for i, class_name in enumerate(class_names):
        recall_i = float(recall_per_class[i]) if i < recall_per_class.size else 0.0
        f1_i = float(f1_per_class[i]) if i < f1_per_class.size else 0.0
        per_class_metrics[class_name] = {
            "recall": recall_i,
            "f1_score": f1_i,
        }

    class_recall_list = [float(x) for x in recall_per_class.tolist()]
    
    return {
        "loss": loss_value,
        "top1_accuracy": accuracy,
        "top3_accuracy": top3_acc,
        "macro_f1": macro_f1,
        "worst_class_recall": worst_class_recall,
        "class_recall": class_recall_list,
        "per_class_metrics": per_class_metrics
    }
