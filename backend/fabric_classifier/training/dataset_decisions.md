# Dataset Integration Decisions

## Scope and Ordering
This document is written before any new data integration or retraining actions for attempt 17.

## Evidence Base
I used two evidence sources:
1. `new_dataset_audit.json` and `new_dataset_audit.md` for class coverage, corruption checks, and image characteristics.
2. `history_analysis.json` and `history_analysis.md` for full attempt history trends and chronic class weakness.

## What The Audit Shows

### Dataset 1: Microscope images of fabric (MIT)
- Total images: 833
- Valid images: 833
- Corrupt images: 0
- Characteristics: high-resolution (1920x1440), bright microscope texture captures.
- Mapped semantic classes cover: Cotton, Polyester, Linen, Nylon, Silk, Satin, Velvet, Knitted.
- Contains ambiguous blend folders (cotton-linen and cotton-silk blends) that are label-noisy for a single-label classifier.

### Dataset 2: The Fabrics Dataset by iBUG (Research only)
- Total images: 7885
- Valid images: 7885
- Corrupt images: 0
- Characteristics: standardized 400x400 material patches, moderate lighting, high class-count variance.
- Strong mapped class volume for Polyester, Denim, Cotton, Wool, Nylon; sparse for Suede/Leather/Velvet.
- License restriction: research-only; not acceptable for final commercial packaged weights.

## What The Training History Shows
- Best completed test results (attempt 15): top1=0.5824, top3=0.8352, macro_f1=0.5832, worst_recall=0.3250.
- Chronic weakness across attempts is concentrated in:
  - Polyester (mean recall ~0.287)
  - Velvet (mean recall ~0.393)
  - Nylon (mean recall ~0.457)
  - Secondary weakness: Linen/Fleece variability.
- Attempt 17 reached higher validation (val macro_f1 ~0.6231) but was interrupted and not finalized.
- Data bottleneck is no longer mainly Suede/Corduroy count; it is class-separable texture robustness for Polyester/Velvet/Nylon under varied appearance.

## Decisions

### A) Microscope dataset inclusion (Approved)
Include a curated subset from microscope data into the training pool because:
- License is compatible (MIT).
- Data is clean (0 corruption).
- Domain adds fine-grained weave texture signal for classes where history shows confusion.

Include only class folders with confident one-label mapping:
- Include: Contrado-Crepe, Contrado-Jersey, Contrado-Nylon, Contrado-Satin, Contrado-Silk, Contrado-Velvet, Contrado-Lycra, Cotton, Linen, Polyester.
- Exclude: Cotton Sateen, Cotton-Linen-Blend1, Cotton-Linen-Blend2, Cotton-Silk-Blend (ambiguous/blended labels).

Rationale for extraction strategy:
- Use original microscope images directly and let the existing `extract_patches` pipeline generate sub-patches dynamically.
- Do not pre-bake fixed patches to avoid overfitting to static crop positions.

### B) iBUG dataset use (Controlled research-only experiments)
Use iBUG only in explicit experimental runs for shortlisting useful hyperparameter/data balancing behavior, not for final packaged model.

Include only targeted weak-class support initially:
- Include mappings for: Polyester, Velvet (and Chenille), Nylon, Linen, Fleece (and Artificial_fur), optionally Leather support.
- Exclude high-volume ambiguous classes and unmapped folders (Blended, Unclassified, Utilities, Lut, Terrycloth, Acrylic) from supervised training labels.

Sampling policy:
- Class-cap iBUG contribution per target class to avoid overwhelming TextileNet distribution.
- Deterministic train/test split for reproducibility.

### C) License-safe finalization policy
- Any run that uses iBUG is marked `research_only_data_used=true` and cannot be treated as final deliverable success.
- If a research-only run meets metrics, run a clean follow-up attempt with iBUG disabled and only commercially-safe data (TextileNet + MIT microscope) to produce final packaged weights.
- Final packaged weights must be generated with `research_only_data_used=false`.

## Integration Plan
1. Build processed dataset folders for microscope (commercial-safe) and iBUG (research-only experimental).
2. Update training data source selection to toggle:
   - `USE_MICROSCOPE_DATA=true`
   - `USE_IBUG_RESEARCH_DATA=false` by default
3. Add experiment logging discipline:
   - Read `experiment_log.md` at start of each attempt.
   - Append detailed post-mortem after each attempt.
4. Resume attempt 17 with processed data and monitoring checks (single process, RAM, checkpoints, metric trend).

## Risk Controls
- Keep class mapping conservative to avoid label noise from blends/ambiguous folders.
- Keep iBUG path physically separated and explicitly gated by parameter.
- Enforce single active train process before every launch.
- Keep reproducible split logic and manifests for data provenance.
