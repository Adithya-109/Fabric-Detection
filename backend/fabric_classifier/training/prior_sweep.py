"""Phase A: post-hoc prior correction on existing weights (no retraining).

The legacy trainer sampled classes uniformly *and* weighted the loss by inverse
frequency, so the model's posteriors assume rare classes are the most likely ones,
while real data is ~35% Cotton / ~19% Polyester. This module sweeps
the correction strength on validation logits, picks the best setting and stores it
in ``calibration/temperature.json`` where ``FabricClassifier`` picks it up.

Usage (from the repository root, on the machine that has DATASETS/):

    python -m backend.fabric_classifier.training.prior_sweep \
        --weights backend/fabric_classifier/weights/fabric_clf_best.pt --write

The pure-NumPy functions below are unit-tested; ``main`` needs PyTorch and the data.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from ..postprocess import apply_temperature, prior_correction
from .balancing import effective_training_prior
from .metrics import compute_classification_metrics

DEFAULT_STRENGTHS = [round(x, 2) for x in np.arange(0.0, 1.55, 0.1)]


def evaluate_with_prior_correction(logits, labels, class_names, train_priors, target_priors,
                                   strength: float, temperature: float = 1.0) -> dict:
    """Metrics after ``softmax(logits / T)`` and prior correction of the given strength."""
    probs = apply_temperature(np.asarray(logits, dtype=np.float64), temperature)
    probs = prior_correction(probs, train_priors, target_priors, strength=strength)
    return compute_classification_metrics(labels, probs.argmax(axis=1), class_names, scores=probs, top_k=3)


def sweep_prior_correction(logits, labels, class_names, train_priors, target_priors,
                           strengths=None, temperature: float = 1.0) -> list[dict]:
    strengths = DEFAULT_STRENGTHS if strengths is None else list(strengths)
    return [
        {
            "strength": s,
            "metrics": evaluate_with_prior_correction(
                logits, labels, class_names, train_priors, target_priors, s, temperature
            ),
        }
        for s in strengths
    ]


def best_result(results: list[dict], metric: str = "macro_f1", min_worst_recall: float | None = None) -> dict:
    """Best sweep entry by ``metric``; prefers entries meeting the worst-recall floor if any do."""
    if not results:
        raise ValueError("no sweep results")
    candidates = results
    if min_worst_recall is not None:
        passing = [r for r in results if r["metrics"].get("worst_class_recall", 0.0) >= min_worst_recall]
        candidates = passing or results
    return max(candidates, key=lambda r: r["metrics"][metric])


def _format_row(r: dict) -> str:
    m = r["metrics"]
    return (f"  strength={r['strength']:<4} top1={m['top1_accuracy']:.4f} top3={m.get('top3_accuracy', 0):.4f} "
            f"macroF1={m['macro_f1']:.4f} worstRecall={m['worst_class_recall']:.4f}")


def collect_logits(model, dataloader, device):  # pragma: no cover - needs torch + data
    """Mean-over-patches logits for every image in a (multi-patch) eval dataloader."""
    import torch

    model.eval().to(device)
    all_logits, all_labels = [], []
    with torch.no_grad():
        for inputs, labels in dataloader:
            if inputs.numel() == 0:
                continue
            inputs = inputs.to(device=device, dtype=torch.float32)
            bs, n_patches, c, h, w = inputs.shape
            logits = model(inputs.view(-1, c, h, w)).view(bs, n_patches, -1).mean(1)
            all_logits.append(logits.float().cpu().numpy())
            all_labels.append(labels.numpy())
    return np.concatenate(all_logits), np.concatenate(all_labels)


def main(argv=None):  # pragma: no cover - needs torch + data
    import torch
    from torch.utils.data import DataLoader
    from torchvision import transforms

    from ..inference import FabricClassifier
    from . import train as trainer

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--weights", default=trainer.BEST_WEIGHTS_PATH)
    parser.add_argument("--metric", default="macro_f1", choices=["macro_f1", "top1_accuracy", "balanced_accuracy"])
    parser.add_argument("--min-worst-recall", type=float, default=0.40)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--sampler-power", type=float, default=0.0,
                        help="SAMPLER_POWER the weights were trained with (legacy: 0 = balanced sampler)")
    parser.add_argument("--unweighted-loss", action="store_true",
                        help="set if the weights were trained WITHOUT inverse-frequency loss weights")
    parser.add_argument("--write", action="store_true", help="store the chosen correction in temperature.json")
    parser.add_argument("--report-test", action="store_true", help="also report the chosen setting on test (once)")
    args = parser.parse_args(argv)

    clf = FabricClassifier(args.weights, device="cpu")
    names = clf.class_names
    (_, train_labels), (val_files, val_labels), (test_files, test_labels) = trainer.load_and_split_data(
        trainer.load_additional_data_sources()
    )
    tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    def loader(files, labels):
        ds = trainer.FabricDataset(files, labels, tf, n_patches=7, is_train=False)
        return DataLoader(ds, batch_size=args.batch_size, shuffle=False, num_workers=2,
                          collate_fn=trainer.collate_fn_filter_corrupted)

    print(f"Collecting validation logits for {len(val_files)} images...")
    val_logits, val_y = collect_logits(clf.model, loader(val_files, val_labels), args.device)

    n = len(names)
    # The prior the training setup taught the model (legacy: balanced sampler + weighted loss ⇒ ∝ 1/count).
    train_priors = effective_training_prior(
        np.bincount(train_labels, minlength=n), args.sampler_power, not args.unweighted_loss
    )
    target_priors = np.bincount(val_y, minlength=n) / len(val_y)
    print("Validation class priors:", {c: round(float(p), 4) for c, p in zip(names, target_priors)})

    results = sweep_prior_correction(val_logits, val_y, names, train_priors, target_priors,
                                     temperature=clf.temperature)
    for r in results:
        print(_format_row(r))
    best = best_result(results, args.metric, args.min_worst_recall)
    print("Chosen:\n" + _format_row(best))

    if args.report_test:
        test_logits, test_y = collect_logits(clf.model, loader(test_files, test_labels), args.device)
        m = evaluate_with_prior_correction(test_logits, test_y, names, train_priors, target_priors,
                                           best["strength"], clf.temperature)
        print("Test with chosen setting:\n" + _format_row({"strength": best["strength"], "metrics": m}))

    if args.write:
        calib_path = os.path.abspath(
            os.path.join(os.path.dirname(args.weights), "..", "calibration", "temperature.json")
        )
        calib = {}
        if os.path.exists(calib_path):
            with open(calib_path) as f:
                calib = json.load(f)
        calib["prior_correction"] = {
            "target_priors": target_priors.tolist(),
            "train_priors": train_priors.tolist(),
            "strength": best["strength"],
            "selected_on": "val",
            "metric": args.metric,
            "val_metrics": {k: best["metrics"][k] for k in
                            ("top1_accuracy", "top3_accuracy", "macro_f1", "worst_class_recall")},
        }
        os.makedirs(os.path.dirname(calib_path), exist_ok=True)
        with open(calib_path, "w") as f:
            json.dump(calib, f, indent=4)
        print(f"Wrote prior correction to {calib_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
