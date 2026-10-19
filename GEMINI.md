# Project Instructions — Fabric Classifier System

## Persistent Memory Loader
Before project work, and after a new session or context reset, read memory/INDEX.md and memory/HOT.md. Follow INDEX.md to retrieve task-relevant records and current source material. Checkpoint meaningful changes before handoff. If these files are unavailable, report that; do not claim to remember them.

## Operating Constraints & Environment
- **Environment**: Always run in conda environment `myenv` (`conda activate myenv`).
- **Hardware Profile**: 24 GB RAM, 12-core CPU, RTX 3050 6GB GPU (FP16 required, target VRAM budget <= 300MB at inference).
- **Core Memory Registry**: Refer to [memory/INDEX.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/INDEX.md) for conditional routing and [memory/HOT.md](file:///c:/Users/A0SKZ/STORE/ALL_CODE/BUISINESS/Clothes_Machine_Learning/memory/HOT.md) for current working state.
- **Process Guard**: Never run concurrent `train.py` writers; always check active processes before launching.
