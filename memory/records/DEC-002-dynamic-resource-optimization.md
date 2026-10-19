# Decision Record: DEC-002 — Dynamic Hardware Resource Allocation for DataLoader

- **ID**: DEC-002
- **Title**: Dynamic DataLoader worker scaling (NUM_WORKERS=8) and pinned memory for RTX 3050
- **Scope**: Data ingestion and batch throughput in `backend/fabric_classifier/training/train.py`
- **Status**: active
- **Date**: 2026-10-10

---

## 1. Context & Rationale
- **Context**: The host machine has 24 GB of physical RAM and a 12-core CPU, but legacy code hardcoded `NUM_WORKERS = 0` (or <=4) and disabled pinned memory due to an outdated 8 GB RAM specification in `.github/copilot-instructions.md`. On 232,330 images, this caused training throughput to crawl at ~13.5 it/s (~65 mins/epoch).
- **Decision**: Set dynamic DataLoader workers: `NUM_WORKERS = min(8, max(1, os.cpu_count() - 2))` (allocating 8 workers on this 12-core machine) and enable `pin_memory = True` for RTX 3050.
- **Evidence**:
  - Throughput doubled from ~13.5 it/s to ~28–30 it/s (>120 samples/sec).
  - Epoch duration cut in half from ~65 min to ~32 min.
  - Zero OOM errors and zero dropped steps observed across Attempt 305 and 306.
- **Alternatives Considered**:
  - Keep `NUM_WORKERS = 0`: Ruled out because 20 epochs would take ~22 hours instead of ~11 hours.
  - Maximize to 12 workers: Ruled out to preserve headroom for system and GPU driver stability.
- **Conditions for Reconsideration**: If running concurrently with memory-intensive external tasks causing RAM usage to exceed 85%.
