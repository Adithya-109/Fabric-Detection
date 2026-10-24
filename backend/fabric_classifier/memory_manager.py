import gc
import torch
import psutil

class FabricMemoryManager:
    @property
    def VRAM_SAFE_MB(self) -> float:
        return self._get_total_vram_mb() * 0.15

    @property
    def VRAM_TIGHT_MB(self) -> float:
        return self._get_total_vram_mb() * 0.10

    @property
    def VRAM_CRITICAL_MB(self) -> float:
        return self._get_total_vram_mb() * 0.05
        
    def _get_total_vram_mb(self) -> float:
        if not torch.cuda.is_available():
            return 2000.0
        _, total_bytes = torch.cuda.mem_get_info(0)
        return total_bytes / (1024 ** 2)

    def __init__(self, model, preferred_device: str = "cuda"):
        self.model = model
        self.preferred_device = preferred_device
        self._current_device = None

    @property
    def num_classes(self) -> int:
        if hasattr(self.model, "classifier") and len(self.model.classifier) > 0:
            head = self.model.classifier[-1]
            if hasattr(head, "out_features"):
                return int(head.out_features)
        return 14

    @property
    def vram_free_mb(self) -> float:
        if not torch.cuda.is_available():
            return 0.0
        # Use CUDA runtime free-memory query for a more accurate free-VRAM estimate.
        free_bytes, _ = torch.cuda.mem_get_info(0)
        return free_bytes / (1024 ** 2)

    @property
    def ram_used_percent(self) -> float:
        return psutil.virtual_memory().percent

    def get_inference_device(self) -> str:
        if not torch.cuda.is_available() or self.preferred_device == "cpu":
            return "cpu"
        
        free_vram = self.vram_free_mb
        if free_vram >= self.VRAM_TIGHT_MB:
            return "cuda"
        else:
            print(f"[FabricMemoryManager] Low VRAM ({free_vram:.0f}MB free). Using CPU to be safe.")
            return "cpu"

    def _forward(self, patches_tensor: torch.Tensor, device: str) -> torch.Tensor:
        if self.model.training:
            self.model.eval()
        with torch.no_grad():
            if device == "cuda":
                self.model = self.model.half()
                inp = patches_tensor.to(device).half()
            else:
                self.model = self.model.float()
                inp = patches_tensor.to(device).float()
            return self.model(inp).float()

    def run_inference(self, patches_tensor: torch.Tensor, return_logits: bool = False) -> torch.Tensor:
        """
        Batched forward pass with automatic device selection and GPU-OOM recovery.

        Returns per-patch logits of shape (n_patches, n_classes) on CPU when
        ``return_logits`` is True, otherwise the mean softmax probability over
        patches (legacy behaviour). Errors other than GPU OOM are raised: a silent
        uniform fallback made real bugs look like low-confidence predictions.
        """
        device = self.get_inference_device()

        if self._current_device != device:
            try:
                self.model = self.model.to(device)
                self._current_device = device
                print(f"[FabricMemoryManager] Model moved to {device}.")
            except Exception as e:
                print(f"[FabricMemoryManager] Failed to move model to {device}: {e}. Falling back to CPU.")
                self.model = self.model.to("cpu")
                self._current_device = "cpu"
                device = "cpu"

        try:
            logits = self._forward(patches_tensor, device)
        except torch.cuda.OutOfMemoryError:
            print("[FabricMemoryManager] OOM on GPU — falling back to CPU for this batch.")
            torch.cuda.empty_cache()
            gc.collect()
            self.model = self.model.to("cpu").float()
            self._current_device = "cpu"
            logits = self._forward(patches_tensor, "cpu")

        logits = logits.cpu()
        if return_logits:
            return logits
        return torch.softmax(logits, dim=-1).mean(dim=0)

    def free_cache(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        print("[FabricMemoryManager] Caches freed.")
