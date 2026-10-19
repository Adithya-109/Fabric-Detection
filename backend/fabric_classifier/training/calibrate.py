import torch
import torch.nn as nn
import numpy as np
from scipy.optimize import minimize_scalar
import json
import os

class ECE(nn.Module):
    """
    Calculates the Expected Calibration Error of a model.
    """
    def __init__(self, n_bins=15):
        super(ECE, self).__init__()
        bin_boundaries = torch.linspace(0, 1, n_bins + 1)
        self.bin_lowers = bin_boundaries[:-1]
        self.bin_uppers = bin_boundaries[1:]

    def forward(self, logits, labels):
        softmaxes = torch.softmax(logits, dim=1)
        confidences, predictions = torch.max(softmaxes, 1)
        accuracies = predictions.eq(labels)

        ece = torch.zeros(1, device=logits.device)
        for bin_lower, bin_upper in zip(self.bin_lowers, self.bin_uppers):
            in_bin = confidences.gt(bin_lower.item()) * confidences.le(bin_upper.item())
            prop_in_bin = in_bin.float().mean()
            if prop_in_bin.item() > 0:
                accuracy_in_bin = accuracies[in_bin].float().mean()
                avg_confidence_in_bin = confidences[in_bin].mean()
                ece += torch.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
        return ece.item()

def calibrate_temperature(model, dataloader, device):
    """
    Finds the optimal temperature for temperature scaling.
    """
    model.eval()
    logits_list = []
    labels_list = []
    model_dtype = next(model.parameters()).dtype
    with torch.no_grad():
        for inputs, labels in dataloader:
            if inputs.nelement() == 0:
                continue

            inputs = inputs.to(device=device, dtype=model_dtype)
            labels = labels.to(device=device).long()

            if inputs.dim() == 5:  # (batch, n_patches, c, h, w)
                bs, n_patches, c, h, w = inputs.shape
                inputs = inputs.view(-1, c, h, w)
                patch_logits = model(inputs)
                logits = patch_logits.view(bs, n_patches, -1).mean(1)
            else:
                logits = model(inputs)

            logits_list.append(logits.float().cpu())
            labels_list.append(labels.cpu())

    if not logits_list:
        print("No validation logits available for temperature calibration. Using T=1.0.")
        return 1.0
    
    logits_all = torch.cat(logits_list)
    labels_all = torch.cat(labels_list)

    ece_criterion = ECE()
    nll_criterion = nn.CrossEntropyLoss()

    ece_before = ece_criterion(logits_all, labels_all)
    print(f"ECE before calibration: {ece_before:.4f}")

    def nll_for_temp(temp):
        return nll_criterion(logits_all / temp, labels_all).item()

    res = minimize_scalar(nll_for_temp, bounds=(0.1, 5.0), method='bounded')
    best_temp = float(getattr(res, "x", 1.0))
    
    ece_after = ece_criterion(logits_all / best_temp, labels_all)
    print(f"Optimal temperature: {best_temp:.4f}")
    print(f"ECE after calibration: {ece_after:.4f}")

    # Save the temperature
    calib_dir = 'backend/fabric_classifier/calibration'
    os.makedirs(calib_dir, exist_ok=True)
    calib_path = os.path.join(calib_dir, 'temperature.json')
    
    calib_data = {
        "temperature": float(best_temp),
        "ece_before": ece_before,
        "ece_after": ece_after
    }
    with open(calib_path, 'w') as f:
        json.dump(calib_data, f, indent=4)
    
    print(f"Temperature saved to {calib_path}")
    return best_temp
