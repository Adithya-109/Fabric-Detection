import torch
import json
from PIL import Image
import torchvision.transforms as transforms
import os
import zlib
import numpy as np

from .classes import MATERIAL_CLASSES
from .model import get_model
from .memory_manager import FabricMemoryManager
from .training.dataset import extract_patches


def _stable_image_seed(pil_image: Image.Image) -> int:
    thumb = pil_image.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
    return zlib.crc32(thumb.tobytes()) & 0xFFFFFFFF

def preprocess_patches(patches: list[Image.Image]) -> torch.Tensor:
    """Applies validation transforms and stacks patches into a tensor."""
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    tensors = []
    for patch in patches:
        tensor = val_transforms(patch)
        if not isinstance(tensor, torch.Tensor):
            tensor = transforms.ToTensor()(patch)
        tensors.append(tensor)
    return torch.stack(tensors)

class FabricClassifier:
    def __init__(self, weights_path: str, device: str = "cuda"):
        """
        Initializes the fabric classifier.
        """
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weights file not found at {weights_path}")

        checkpoint = torch.load(weights_path, map_location="cpu")
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
            saved_class_names = checkpoint.get("present_class_names")
        else:
            state_dict = checkpoint
            saved_class_names = None

        num_classes = state_dict["classifier.4.weight"].shape[0]
        self.model = get_model(num_classes=num_classes, pretrained=False)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        if saved_class_names and len(saved_class_names) == num_classes:
            self.class_names = saved_class_names
        else:
            self.class_names = MATERIAL_CLASSES[:num_classes]

        self.device = device
        self.memory_manager = FabricMemoryManager(self.model, preferred_device=self.device)
        
        # Load temperature for calibration
        calib_path = os.path.abspath(
            os.path.join(os.path.dirname(weights_path), "..", "calibration", "temperature.json")
        )
        self.temperature = 1.0 # Default
        if os.path.exists(calib_path):
            with open(calib_path, 'r') as f:
                self.temperature = json.load(f).get("temperature", 1.0)
        else:
            print(f"[FabricClassifier] Warning: Calibration file not found at {calib_path}. Using T=1.0.")

    def _uniform_top3(self) -> list[dict]:
        if len(self.class_names) == 0:
            return []
        classes = [self.class_names[i % len(self.class_names)] for i in range(3)]
        return [
            {"name": classes[0], "confidence": 33.34},
            {"name": classes[1], "confidence": 33.33},
            {"name": classes[2], "confidence": 33.33},
        ]

    def predict(self, pil_image: Image.Image) -> list[dict]:
        """
        Predicts the fabric material from a PIL image.
        """
        if pil_image is None:
            return self._uniform_top3()
            
        # Use 7 patches for inference as per spec
        patch_rng = np.random.default_rng(_stable_image_seed(pil_image))
        patches = extract_patches(pil_image, n_patches=7, rng=patch_rng)
        if not patches:
            return self._uniform_top3()

        tensor = preprocess_patches(patches)
        
        # Get averaged probabilities from the memory manager
        avg_probs = self.memory_manager.run_inference(tensor)
        avg_probs = avg_probs.cpu()

        if avg_probs.dim() > 1:
            avg_probs = avg_probs.mean(dim=0)
        if avg_probs.numel() != len(self.class_names):
            return self._uniform_top3()

        # Apply temperature scaling
        calibrated_logits = torch.log(avg_probs + 1e-9) / self.temperature
        calibrated_probs = torch.softmax(calibrated_logits, dim=-1)

        # Get top-3 results
        k = min(3, calibrated_probs.numel())
        top3_probs, top3_idxs = torch.topk(calibrated_probs, k)

        results = []
        for i in range(top3_probs.size(0)):
            class_idx = int(top3_idxs[i].item())
            confidence = top3_probs[i].item()
            results.append({
                "name": self.class_names[class_idx],
                "confidence": round(confidence * 100, 2)
            })
            
        return results
