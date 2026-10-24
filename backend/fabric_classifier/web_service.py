import os
import io
import base64
import time
import psutil
import torch
from PIL import Image

from .classes import MATERIAL_CLASSES
from .inference import FabricClassifier
from .profiles import FABRIC_PROFILES  # re-exported for backwards compatibility


def _image_to_base64_jpeg(pil_img: Image.Image, quality: int = 85) -> str:
    """Converts a PIL Image to a base64 encoded data URI."""
    buf = io.BytesIO()
    rgb_img = pil_img.convert("RGB")
    rgb_img.save(buf, format="JPEG", quality=quality)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


class FabricWebService:
    """
    High-performance web inference service that wraps FabricClassifier,
    extracts visual patches, measures detailed latencies, and provides
    complete metrics and textile profiles.
    """
    def __init__(self, weights_path: str = None, device: str = "cpu"):
        if weights_path is None:
            weights_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "fabric_classifier",
                "weights",
                "fabric_clf_best.pt"
            )
        
        self.weights_path = os.path.abspath(weights_path)
        self.device = device
        print(f"[FabricWebService] Initializing with weights: {self.weights_path}")
        
        self.classifier = FabricClassifier(self.weights_path, device=self.device)
        self.class_names = self.classifier.class_names
        self.temperature = self.classifier.temperature
        
        # Determine actual execution device
        self.active_device_str = "Apple Silicon (CPU - EfficientNet-B0)"
        if torch.backends.mps.is_available() and self.device == "mps":
            self.active_device_str = "Apple Silicon Metal (MPS)"
            
        print(f"[FabricWebService] Service ready on {self.active_device_str}. Classes: {len(self.class_names)}")

    def get_system_metrics(self) -> dict:
        """Collects current hardware and memory diagnostics."""
        mem = psutil.virtual_memory()
        return {
            "device": self.active_device_str,
            "architecture": "ARM64 (Apple Silicon)",
            "ram_total_gb": round(mem.total / (1024 ** 3), 2),
            "ram_used_percent": round(mem.percent, 1),
            "ram_available_gb": round(mem.available / (1024 ** 3), 2),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "model_backbone": "EfficientNet-B0",
            "classifier_head": "Dropout(0.3) -> Linear(1280->256) -> ReLU -> Dropout(0.2) -> Linear(256->14)",
            "weights_file": os.path.basename(self.weights_path),
            "num_classes": len(self.class_names),
            "temperature_calibration": self.classifier.temperature,
            "prior_correction": self.classifier.prior_correction is not None
        }

    def predict_image(self, pil_image: Image.Image, n_patches: int = 7) -> dict:
        """
        Executes full multi-patch fabric classification pipeline,
        returning predictions, visual patches, and comprehensive performance metrics.
        """
        start_total = time.perf_counter()
        
        # 1. Image metadata
        img_w, img_h = pil_image.size
        img_format = pil_image.format or "JPEG"
        img_mode = pil_image.mode
        
        # Thumbnail of original image for preview
        thumb_img = pil_image.copy()
        thumb_img.thumbnail((600, 600), Image.Resampling.LANCZOS)
        preview_data_uri = _image_to_base64_jpeg(thumb_img, quality=80)
        
        # 2-3. Patch extraction + forward pass, via the same code path as FabricClassifier.predict
        detailed = self.classifier.predict_detailed(pil_image, n_patches=n_patches)
        patches = detailed["patches"]
        calibrated_probs = detailed["probabilities"]
        patch_time_ms = round(detailed["timing"]["patch_ms"], 2)
        model_time_ms = round(detailed["timing"]["model_ms"], 2)

        # Convert patches to base64 for frontend inspection
        patch_thumbnails = []
        for i, p in enumerate(patches):
            d_uri = _image_to_base64_jpeg(p, quality=85)
            raw_b64 = d_uri.split(",", 1)[1] if "," in d_uri else d_uri
            patch_thumbnails.append({
                "patch_index": i + 1,
                "data_uri": d_uri,
                "image_url": d_uri,
                "image_base64": raw_b64,
                "width": p.width,
                "height": p.height
            })

        # 4. Construct complete 14-class probability list
        all_classes_list = []
        for idx, class_name in enumerate(self.class_names):
            prob = float(calibrated_probs[idx])
            all_classes_list.append({
                "name": class_name,
                "class_name": class_name,
                "confidence": round(prob * 100, 2),
                "probability": round(prob, 4),
                "index": idx
            })
            
        # Sort descending by confidence
        all_classes_list.sort(key=lambda x: x["confidence"], reverse=True)
        for rank, item in enumerate(all_classes_list, 1):
            item["rank"] = rank
            
        # Top-1 and Top-3
        top_1 = all_classes_list[0]
        top_3 = all_classes_list[:3]
        
        # Fabric profile for winner
        winner_name = top_1["name"]
        fabric_profile = FABRIC_PROFILES.get(winner_name, {
            "category": "Textile Fabric",
            "tagline": "Quality apparel fabric",
            "description": f"Predicted {winner_name} fabric classification.",
            "properties": {"breathability": "Medium", "durability": "Medium", "stretch": "Medium", "texture": "Woven"},
            "care": {"washing": "Wash with care", "drying": "Air dry", "ironing": "Medium iron"},
            "uses": ["Apparel", "Garments"]
        })
        
        total_time_ms = round((time.perf_counter() - start_total) * 1000, 2)
        
        # System metrics snapshot
        sys_metrics = self.get_system_metrics()

        pred_obj = {
            "name": winner_name,
            "class_name": winner_name,
            "confidence": top_1["confidence"],
            "rank": 1,
            "category": fabric_profile["category"],
            "tagline": fabric_profile["tagline"],
            "profile": fabric_profile,
            "properties": fabric_profile.get("properties", {})
        }
        
        return {
            "prediction": pred_obj,
            "top_class": pred_obj,
            "top_3": top_3,
            "top3": top_3,
            "all_classes": all_classes_list,
            "metrics": {
                "total_latency_ms": total_time_ms,
                "patch_extraction_ms": patch_time_ms,
                "model_inference_ms": model_time_ms,
                "patches_analyzed": len(patches),
                "device": sys_metrics["device"],
                "ram_used_percent": sys_metrics["ram_used_percent"],
                "cpu_percent": sys_metrics["cpu_percent"],
                "model_backbone": sys_metrics["model_backbone"],
                "weights_checkpoint": sys_metrics["weights_file"],
                "temperature": sys_metrics["temperature_calibration"]
            },
            "timing": {
                "total_ms": total_time_ms,
                "patch_ms": patch_time_ms,
                "model_ms": model_time_ms
            },
            "system": {
                "device": sys_metrics["device"],
                "arch": sys_metrics["architecture"],
                "cpu_percent": sys_metrics["cpu_percent"],
                "ram_percent": sys_metrics["ram_used_percent"],
                "model": sys_metrics["model_backbone"]
            },
            "image_info": {
                "width": img_w,
                "height": img_h,
                "aspect_ratio": f"{round(img_w / max(1, img_h), 2)}:1",
                "format": img_format,
                "mode": img_mode,
                "preview_uri": preview_data_uri
            },
            "patches": patch_thumbnails
        }
