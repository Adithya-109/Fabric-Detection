"""Embedding-based fabric classifier: frozen CLIP image encoder + a small linear head.

EXP-404 found this the best model so far on everyday garment photos (balanced accuracy
58.5% vs 32.5% for the EfficientNet-B0 weights). The head is a few hundred KB of NumPy
arrays; CLIP itself is downloaded from Hugging Face on first use.
"""
from __future__ import annotations

import os
import time
import warnings
from dataclasses import dataclass

import numpy as np
from PIL import Image

from .classes import MATERIAL_CLASSES
from .postprocess import format_top_k, softmax
from .training.dataset import resize_max_side

DEFAULT_HEAD_PATH = os.path.join(os.path.dirname(__file__), "weights", "clip_head.npz")
CLIP_REPO = "openai/clip-vit-base-patch16"
DEFAULT_MAX_SIDE = 512
_UNSEEN = -1e9  # intercept for classes absent from the training data → probability 0


def l2_normalize(X) -> np.ndarray:
    X = np.asarray(X, dtype=np.float64)
    norm = np.linalg.norm(X, axis=-1, keepdims=True)
    return np.divide(X, norm, out=np.zeros_like(X), where=norm > 0)


def choose_model_kind(env_value, head_exists: bool) -> str:
    """'clip_head' or 'efficientnet'. Unset/empty = clip_head when the head file exists."""
    value = (env_value or "").strip().lower()
    if not value:
        return "clip_head" if head_exists else "efficientnet"
    if value not in ("clip_head", "efficientnet"):
        raise ValueError(f"FABRIC_MODEL must be 'clip_head' or 'efficientnet', got {env_value!r}")
    return value


@dataclass
class LinearHead:
    class_names: list
    mean: np.ndarray       # (d,)   standardisation fitted on L2-normalised embeddings
    scale: np.ndarray      # (d,)
    coef: np.ndarray       # (n_classes, d)
    intercept: np.ndarray  # (n_classes,)

    @classmethod
    def fit(cls, X, y, class_names, C: float = 0.01, balanced: bool = True, seed: int = 0) -> "LinearHead":
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        Xn = l2_normalize(X)
        scaler = StandardScaler().fit(Xn)
        clf = LogisticRegression(C=C, max_iter=3000, class_weight="balanced" if balanced else None,
                                 random_state=seed)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            clf.fit(scaler.transform(Xn), np.asarray(y))
        n, d = len(class_names), Xn.shape[1]
        coef, intercept = np.zeros((n, d)), np.full(n, _UNSEEN)
        w, b = clf.coef_, clf.intercept_
        if len(clf.classes_) == 2:  # sklearn stores one row for a binary problem
            w, b = np.vstack([-w[0] / 2, w[0] / 2]), np.array([-b[0] / 2, b[0] / 2])
        coef[clf.classes_], intercept[clf.classes_] = w, b
        return cls(list(class_names), scaler.mean_, scaler.scale_, coef, intercept)

    def logits(self, embeddings) -> np.ndarray:
        E = np.atleast_2d(np.asarray(embeddings, dtype=np.float64))
        if E.shape[1] != self.mean.shape[0]:
            raise ValueError(f"embedding has {E.shape[1]} dims, head expects {self.mean.shape[0]}")
        Z = (l2_normalize(E) - self.mean) / self.scale
        return Z @ self.coef.T + self.intercept

    def probabilities(self, embeddings) -> np.ndarray:
        return softmax(self.logits(embeddings))

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        np.savez_compressed(path, class_names=np.array(self.class_names), mean=self.mean, scale=self.scale,
                            coef=self.coef.astype(np.float32), intercept=self.intercept)

    @classmethod
    def load(cls, path: str) -> "LinearHead":
        if not os.path.exists(path):
            raise FileNotFoundError(f"Head file not found at {path}")
        d = np.load(path, allow_pickle=False)
        return cls([str(n) for n in d["class_names"]], d["mean"], d["scale"],
                   d["coef"].astype(np.float64), d["intercept"])


class EmbeddingClassifier:
    """Drop-in for FabricClassifier: ``predict`` / ``predict_detailed`` with the same outputs."""

    model_name = "CLIP ViT-B/16 + linear head"

    def __init__(self, embedder, head: LinearHead, max_side=DEFAULT_MAX_SIDE, weights_file: str = "clip_head.npz"):
        self.embedder, self.head, self.max_side = embedder, head, max_side
        self.class_names = list(head.class_names)
        self.temperature = 1.0
        self.prior_correction = None
        self.weights_file = weights_file

    @classmethod
    def from_files(cls, head_path: str = DEFAULT_HEAD_PATH, device: str = "cpu", max_side=DEFAULT_MAX_SIDE):
        head = LinearHead.load(head_path)
        return cls(ClipEmbedder(device=device), head, max_side=max_side, weights_file=os.path.basename(head_path))

    def predict_detailed(self, pil_image: Image.Image, n_patches: int = 7) -> dict:
        start = time.perf_counter()
        image = resize_max_side(pil_image.convert("RGB"), self.max_side)
        view = image.resize((224, 224), Image.Resampling.BILINEAR)  # what the UI shows as the analysed crop
        prep_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        probs = self.head.probabilities(self.embedder.embed(image))[0]
        model_ms = (time.perf_counter() - start) * 1000
        return {
            "top3": format_top_k(probs, self.class_names, k=3),
            "probabilities": probs,
            "patches": [view],
            "timing": {"patch_ms": prep_ms, "model_ms": model_ms},
        }

    def predict(self, pil_image) -> list:
        if pil_image is None:
            names = [self.class_names[i % len(self.class_names)] for i in range(3)]
            return [{"name": n, "confidence": c} for n, c in zip(names, (33.34, 33.33, 33.33))]
        return self.predict_detailed(pil_image)["top3"]


class ClipEmbedder:  # pragma: no cover - needs torch + transformers + weight download
    """Projected CLIP image embedding (512-d), exactly as used in tools/backbone_probe.py."""

    def __init__(self, repo: str = CLIP_REPO, device: str = "cpu"):
        import torch
        from transformers import AutoImageProcessor, CLIPModel

        self.torch, self.device = torch, device
        self.processor = AutoImageProcessor.from_pretrained(repo)
        self.model = CLIPModel.from_pretrained(repo).eval().to(device)

    def embed(self, pil_image: Image.Image) -> np.ndarray:
        torch = self.torch
        with torch.no_grad():
            inputs = self.processor(images=pil_image.convert("RGB"), return_tensors="pt")
            pooled = self.model.vision_model(pixel_values=inputs["pixel_values"].to(self.device)).pooler_output
            return self.model.visual_projection(pooled).cpu().numpy()[0]

    def embed_texts(self, texts) -> np.ndarray:
        torch = self.torch
        if not hasattr(self, "tokenizer"):
            from transformers import AutoTokenizer

            self.tokenizer = AutoTokenizer.from_pretrained(CLIP_REPO)
        with torch.no_grad():
            tok = self.tokenizer(list(texts), padding=True, return_tensors="pt").to(self.device)
            pooled = self.model.text_model(**tok).pooler_output
            return self.model.text_projection(pooled).cpu().numpy()
