"""Fabric classifier package.

`FabricClassifier` is imported lazily so that light modules (classes, data prep,
metrics, the web layer) can be used without loading PyTorch.
"""

__all__ = ["FabricClassifier"]


def __getattr__(name):
    if name == "FabricClassifier":
        from .inference import FabricClassifier

        return FabricClassifier
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
