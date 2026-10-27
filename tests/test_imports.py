"""Import-hygiene tests: lightweight modules must not pull in PyTorch.

Keeps data-prep, metrics and the web layer usable (and testable) without loading
the model, and stops the web app from building the model at import time.
"""
import os
import subprocess
import sys
import unittest

from tests import ROOT

LIGHT_MODULES = [
    "backend.fabric_classifier.classes",
    "backend.fabric_classifier.postprocess",
    "backend.fabric_classifier.clip_head",
    "backend.fabric_classifier.training.balancing",
    "backend.fabric_classifier.training.splits",
    "backend.fabric_classifier.training.metrics",
    "backend.fabric_classifier.training.dataset",
    "backend.app",
]


class TestLightImports(unittest.TestCase):
    def test_modules_do_not_import_torch(self):
        for module in LIGHT_MODULES:
            with self.subTest(module=module):
                code = f"import sys, {module}; print('torch' in sys.modules)"
                out = subprocess.run(
                    [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True,
                    env={**os.environ, "PYTHONPATH": ROOT},
                )
                self.assertEqual(out.returncode, 0, out.stderr)
                self.assertEqual(out.stdout.strip(), "False")


if __name__ == "__main__":
    unittest.main()
