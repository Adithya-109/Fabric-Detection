#!/usr/bin/env python3
"""
Convenience launcher for Fabric Classifier Web App.
Runs on Mac Apple Silicon (CPU / MPS) without CUDA requirements.
"""

import os
import sys
import socket

# Ensure root directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app import app


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def find_free_port(preferred_port: int = 5050) -> int:
    for port in [preferred_port, 5001, 8000, 8080, 8888]:
        if not is_port_in_use(port):
            return port
    return preferred_port


if __name__ == "__main__":
    port = int(os.environ.get("PORT", find_free_port(5050)))
    print("=" * 65)
    print("  TEXCLASSIFIER AI — FABRIC MATERIAL VISION SYSTEM")
    print("=" * 65)
    print(f"  • Platform: Apple Silicon / macOS")
    print(f"  • Model: EfficientNet-B0 (14-Class Garment Fabric Classifier)")
    print(f"  • Mode: Multi-Patch (7 interior texture crops)")
    print(f"  • Server URL: http://127.0.0.1:{port}")
    print("=" * 65)
    
    app.run(host="127.0.0.1", port=port, debug=False)
