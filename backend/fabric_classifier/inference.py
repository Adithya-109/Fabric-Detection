import json
import os
import time
import zlib

import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

from .classes import MATERIAL_CLASSES
from .memory_manager import FabricMemoryManager
from .model import get_model
from .postprocess import (
    DEFAULT_AGGREGATION,
    aggregate_patch_logits,
    apply_temperature,
    format_top_k,
    prior_correction,
)
from .training.dataset import extract_patches


def _stable_image_seed(pil_image: Image.Image) -> int:
    thumb = pil_image.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
    return zlib.crc32(thumb.tobytes()) & 0xFFFFFFFF


_VAL_TRANSFORMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def preprocess_patches(patches: list[Image.Image]) -> torch.Tensor:
    """Applies validation transforms and stacks patches into a tensor."""
    return torch.stack([_VAL_TRANSFORMS(patch.convert("RGB")) for patch in patches])


class FabricClassifier:
    def __init__(self, weights_path: str, device: str = "cuda", aggregation: str = DEFAULT_AGGREGATION):
        """
        Initializes the fabric classifier.

        Args:
            weights_path: checkpoint (raw state dict or {"model_state_dict", "present_class_names"}).
            device: preferred device; falls back to CPU automatically.
            aggregation: how patch logits are combined. "mean_logits" matches evaluate.py
                and calibrate.py, so served predictions use the measured decision rule.
        """
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weights file not found at {weights_path}")

        checkpoint = torch.load(weights_path, map_location="cpu")
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
            saved_class_names = checkpoint.get("present_class_names")
            saved_patch_config = checkpoint.get("patch_config") or {}
        else:
            state_dict = checkpoint
            saved_class_names = None
            saved_patch_config = {}

        num_classes = state_dict["classifier.4.weight"].shape[0]
        self.model = get_model(num_classes=num_classes, pretrained=False)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        if saved_class_names and len(saved_class_names) == num_classes:
            self.class_names = list(saved_class_names)
        else:
            self.class_names = MATERIAL_CLASSES[:num_classes]

        # Patch geometry must match training; older checkpoints used the legacy defaults.
        self.patch_config = {
            "patch_fraction": saved_patch_config.get("patch_fraction"),
            "min_coverage": saved_patch_config.get("min_coverage", 0.5),
        }

        self.device = device
        self.aggregation = aggregation
        self.memory_manager = FabricMemoryManager(self.model, preferred_device=self.device)

        # Calibration: temperature (and optional prior correction) fitted on validation data.
        self.temperature = 1.0
        self.prior_correction = None
        calib_path = os.path.abspath(
            os.path.join(os.path.dirname(weights_path), "..", "calibration", "temperature.json")
        )
        if os.path.exists(calib_path):
            with open(calib_path, "r") as f:
                calib = json.load(f)
            self.temperature = float(calib.get("temperature", 1.0))
            pc = calib.get("prior_correction")
            if pc:
                self.set_prior_correction(
                    pc["target_priors"], pc.get("train_priors"), pc.get("strength", 1.0)
                )
        else:
            print(f"[FabricClassifier] Warning: Calibration file not found at {calib_path}. Using T=1.0.")

    def set_prior_correction(self, target_priors, train_priors=None, strength: float = 1.0):
        """Enable (or disable with ``None``) post-hoc correction for class-prior shift.

        ``train_priors`` defaults to uniform, which is what the balanced training
        sampler effectively taught the model. See docs/IMPROVEMENT_PLAN.md §2.
        """
        if target_priors is None:
            self.prior_correction = None
            return
        n = len(self.class_names)
        target = np.asarray(target_priors, dtype=np.float64)
        train = np.full(n, 1.0 / n) if train_priors is None else np.asarray(train_priors, dtype=np.float64)
        if target.shape != (n,) or train.shape != (n,):
            raise ValueError(f"priors must have {n} entries")
        self.prior_correction = {
            "target_priors": target / target.sum(),
            "train_priors": train / train.sum(),
            "strength": float(strength),
        }

    def _uniform_top3(self) -> list[dict]:
        if len(self.class_names) == 0:
            return []
        classes = [self.class_names[i % len(self.class_names)] for i in range(3)]
        return [
            {"name": classes[0], "confidence": 33.34},
            {"name": classes[1], "confidence": 33.33},
            {"name": classes[2], "confidence": 33.33},
        ]

    def predict_detailed(self, pil_image: Image.Image, n_patches: int = 7) -> dict:
        """Full pipeline: patches → per-patch logits → aggregate → temperature → prior correction.

        Returns {"top3", "probabilities" (np.ndarray over all classes), "patches", "timing"}.
        """
        start = time.perf_counter()
        patch_rng = np.random.default_rng(_stable_image_seed(pil_image))
        patches = extract_patches(pil_image, n_patches=n_patches, rng=patch_rng, **self.patch_config)
        patch_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        patch_logits = self.memory_manager.run_inference(preprocess_patches(patches), return_logits=True)
        logits = aggregate_patch_logits(patch_logits.numpy(), method=self.aggregation)
        probs = apply_temperature(logits, self.temperature)
        if self.prior_correction is not None:
            probs = prior_correction(probs, **self.prior_correction)
        model_ms = (time.perf_counter() - start) * 1000

        return {
            "top3": format_top_k(probs, self.class_names, k=3),
            "probabilities": probs,
            "patches": patches,
            "timing": {"patch_ms": patch_ms, "model_ms": model_ms},
        }

    def predict(self, pil_image: Image.Image) -> list[dict]:
        """
        Predicts the fabric material from a PIL image.
        Returns the top-3 classes as [{"name", "confidence"}], confidence in %, descending.
        """
        if pil_image is None:
            return self._uniform_top3()
        return self.predict_detailed(pil_image)["top3"]
