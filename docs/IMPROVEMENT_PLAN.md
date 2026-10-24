# Fabric Classifier — Assessment & Improvement Plan

_Written 2026-10-24 on branch `feature/tests-and-accuracy-plan`, starting from `main` @ `e72c8b2`
(the fork of `Rancheology/Fabric-Classifier-7-Segment`; the fork only copied `main`, which already
contains the front-end + back-end commits)._

---

## 1. Where the project stands

| Area | State | Notes |
|---|---|---|
| Model + training pipeline | Works, **below target** | Best: Top-1 43.3%, Top-3 66.5%, Macro-F1 40.5%, worst recall 17.6% (Attempt 309). Targets: 72 / 90 / 68 / 40. |
| Inference API (`FabricClassifier.predict`) | Works | Returns top-3 contract. Uses a different patch aggregation from evaluation/calibration (see §3.6). |
| Web app (Flask + SPA) | Works | Upload, samples, 7-patch inspector, metrics. Builds the model at import time; a bad upload returns HTTP 500. |
| Calibration (TASK-002) | Not done | `temperature.json` is the default `1.0`. |
| Tests | **None** | `integration_test.py` is a script that writes a dummy weights file over the real path if missing. |
| Reproducibility | Weak | No `requirements.txt`; Windows absolute dataset paths are hard-coded in `train.py`. |

### What is left to finish the project
1. Reach the accuracy targets (the main work — §3 and §4).
2. Fit the temperature on the final weights and verify the inference contract (TASK-002).
3. Make the "general photo of clothing" use case actually work: real garment segmentation, scale-aware patches (§3.4, §3.5).
4. Automated tests + CI so changes stop silently breaking the contract (this branch starts that).
5. Packaging: `requirements.txt`, configurable dataset paths, a README with run instructions.
6. Repo hygiene: move `scratch/`, root analysis scripts and logs out of the main tree (needs your OK).

---

## 2. The key finding: the bottleneck is class priors, not features

From the per-class recall and F1 stored for Attempt 309 (precision derived as `F1·R / (2R − F1)`):

| Class | Recall | Precision | Reading |
|---|---|---|---|
| Cotton | 0.18 | **0.90** | When it says Cotton it is right — it just almost never says it |
| Polyester | 0.18 | 0.55 | Same pattern, plus real confusion with Cotton |
| Denim | 0.55 | 0.94 | Under-predicted |
| Corduroy | 0.84 | **0.04** | Massively over-predicted (517 images in the data) |
| Suede | 0.85 | 0.06 | Over-predicted (1,122 images) |
| Linen | 0.81 | 0.12 | Over-predicted (2,064 images) |
| Velvet | 0.70 | 0.21 | Over-predicted |

**Cause — the classes are balanced twice.**
1. `build_dataloaders` samples with weights `1/count`, so every class is seen equally often.
2. `run_training_attempt` *also* weights the cross-entropy loss by `1/count`.

Together the model learns an effective prior **∝ 1/count**: the rarer a class, the more likely the
model believes it is. The val/test splits keep the real distribution (Cotton ≈ 35%, Polyester ≈ 19%
of images), so at test time Cotton/Polyester images are handed to rare textured classes — exactly the
"low recall on smooth fabrics" in BUG-001. Each Corduroy image is also drawn ~150× more often than
each Cotton image, so the model memorises them.

**Consequences for the plan.**
- Focal loss / up-weighting Cotton & Polyester (the plan in BUG-001) works against the real problem; deprioritise it.
- The cheapest experiment is **post-hoc prior correction on the existing weights** — multiply the
  posteriors by `(true prior / effective training prior)^strength`. No retraining. Expected to raise
  Cotton/Polyester recall and the precision of the rare classes at the same time. Ready to run:
  `python -m backend.fabric_classifier.training.prior_sweep --report-test --write`.

---

## 3. Other issues found in the code

1. **Mixed taxonomy.** The 14 classes mix *fibres* (Cotton, Polyester, Nylon, Wool, Silk, Linen) with
   *constructions/finishes* (Denim, Knitted, Velvet, Corduroy, Fleece, Satin, Suede). A cotton knit jumper is
   legitimately both "Cotton" and "Knitted"; a polyester satin dress is both "Polyester" and "Satin".
   Labels come from different sources with different conventions, so this is label noise the model cannot
   resolve. Fibre identity (Cotton vs Polyester on a plain weave) is also close to unidentifiable from a photo.
   → **Decision needed (§5).**
2. **Possible train/test leakage.** All sources are pooled and split randomly per image. Product photo
   datasets contain near-duplicates (same product, colourways, crops), which inflates val scores and makes
   checkpoint selection noisy. → group near-duplicates before splitting.
3. **Batch size 4 with BatchNorm.** EfficientNet's BatchNorm statistics are updated from 4 images per step,
   which is too few. → freeze BN (keep ImageNet stats) or use a larger batch via smaller patches/AMP.
4. **Segmentation built for product shots.** `extract_patches` keeps "non-white, opaque" pixels. On a
   normal photo (person, room, street) that is almost the whole image, so patches land on skin, hair and
   background. This directly hurts the project goal ("general images of cloth").
5. **Fixed 160 px patch.** A 160 px patch is ~8% of a 2048 px photo but ~40% of a 400 px one, so the texture
   scale the model sees varies wildly with resolution. → patch size relative to the garment area.
6. **Train/eval/inference mismatch.** `evaluate.py` and `calibrate.py` average *logits* over patches;
   `inference.py`/`web_service.py` average *probabilities* and then apply the temperature to log-probs.
   The temperature is therefore fitted on a different quantity from the one it is applied to, and the
   checkpoint is selected on a different decision rule from the one served.
7. **Silent failure.** `FabricMemoryManager.run_inference` returns a uniform distribution on *any* exception,
   so a real bug looks like a low-confidence prediction.
8. **Warm-start chaining (304→310)** re-used the same split and data; gains came from more epochs, and
   the test set was looked at after every attempt (risk of overfitting decisions to test).

---

## 4. Accuracy plan (ordered; one change per experiment, as the project protocol requires)

Each step gets an `EXP-3xx` record before it runs. All Phase-B switches live in `HYPERPARAMS` in
`train.py`; **their defaults reproduce the legacy trainer exactly**, so nothing changes until a flag is set. Selection is done on **val**; test is read once per
phase. Always report per-class **precision and recall** and the confusion matrix, not just recall.

### Phase A — free wins on the existing weights (no training, ~1 day)
| # | Change | How | Success signal |
|---|---|---|---|
| A1 | Measure baseline with the new metrics | `compute_classification_metrics` on val: precision, recall, confusion matrix | Confirms §2 table |
| A2 | Post-hoc prior correction | `training/prior_sweep.py`: train prior = `effective_training_prior(counts, 0, True)` (∝ 1/count), target = val frequencies; sweeps strength 0–1.5 on val, picks best Macro-F1 with worst recall ≥ 0.40 if possible, writes it to `temperature.json` | Cotton/Polyester recall ↑ and rare-class precision ↑; Top-1 expected to jump substantially |
| A3 | Consistent aggregation | Use `aggregate_patch_logits(..., "mean_logits")` everywhere | Val metrics identical to served predictions |
| A4 | Fit temperature after A2/A3 | `calibrate.py` on val | ECE ↓; finishes TASK-002 |

### Phase B — fix the training signal (one retrain each, from ImageNet weights)
| # | Change | Why |
|---|---|---|
| B1 | Leakage-free grouped split (`group_near_duplicates` + `grouped_stratified_split`) | Trustworthy val numbers before tuning anything else |
| B2 | `SAMPLER_POWER=0.5`, `LOSS="logit_adjusted"` (drops the double balancing) | Keeps rare classes visible without teaching a false prior; the standard fix for long-tailed data |
| B3 | `FREEZE_BN=True` | Batch of 4 cannot estimate BN statistics |
| B4 | `PATCH_FRACTION=0.2`, `PATCH_MIN_COVERAGE=0.9` (saved in the checkpoint, read back at inference) | Consistent texture scale; no half-background patches |
| B5 | Cap the oversampling of tiny classes; collect more Corduroy/Suede/Linen (DEC-001-compliant) | 517 Corduroy images cannot support 84% recall honestly |

### Phase C — make "general photos" work (the project's actual goal)
| # | Change | Why |
|---|---|---|
| C1 | Garment segmentation (e.g. a clothes-parsing SegFormer/U²-Net model) passed in via `extract_patches(mask=...)` | Patches land on cloth, not skin/background |
| C2 | Build a small **in-the-wild test set** (200–500 own photos, labelled carefully) | The current test set is mostly product shots; this is the number that matters |
| C3 | Two-scale input: patches + a downsized full-garment view (drape/sheen cues) | Silk/Satin/Leather are recognisable from drape and highlights, not micro-texture |
| C4 | Stronger backbone if B-phase plateaus (EfficientNet-B2/ConvNeXt-T, or a frozen DINOv2/CLIP encoder + linear probe) | Self-supervised features transfer far better to material recognition; a linear probe also trains in minutes on the 3050 |

### Phase D — taxonomy (pending your decision, see §5)
Split into two heads — **fibre** (Cotton / Polyester / Wool / Silk / Linen / Nylon / Leather) and
**construction** (Woven-plain / Denim / Knitted / Velvet / Corduroy / Fleece / Satin / Suede) — with
"unknown" allowed for fibre. Expected to lift Macro-F1 the most of any single change, because it removes
contradictory labels rather than fighting them.

### Realistic expectations
Phase A alone should move Top-1 well above the current 43% because the largest classes stop being
starved. Hitting **Top-1 ≥ 72% on the current 14-way taxonomy** is unlikely while Cotton vs Polyester
on plain weaves is in it; with the two-head taxonomy the targets become reachable per head.

---

## 5. Decisions needed from you
1. **Taxonomy (Phase D):** keep 14 classes, or move to fibre + construction heads?
2. **Training runs:** the project rule is "don't start a run without asking". Phase A needs no training;
   Phase B needs the RTX 3050 machine and the `DATASETS/` folder (not in git).
3. **Garment segmenter (C1):** OK to add a ~50–100 MB segmentation model as a dependency?
4. **Repo cleanup:** OK to move `scratch/`, root one-off scripts and `*.txt` outputs into `archive/`?

---

## 6. What this branch adds (test-first)

Tests in `tests/` were written before the code. Run with `pytest` (or `python -m unittest discover tests`).
Tests that need PyTorch skip automatically when it is not installed.

| Module | New / changed functions |
|---|---|
| `training/balancing.py` | `class_counts`, `class_priors`, `tempered_sample_weights`, `effective_training_prior`, `effective_number_weights`, `logit_adjustment` |
| `training/prior_sweep.py` | `evaluate_with_prior_correction`, `sweep_prior_correction`, `best_result`, CLI for Phase A |
| `training/losses.py` | `logit_adjusted_cross_entropy`, `LogitAdjustedLoss`, `freeze_batchnorm` |
| `training/splits.py` | `average_hash`, `hamming_distance`, `group_near_duplicates`, `grouped_stratified_split` |
| `training/dataset.py` | `foreground_mask`, `compute_patch_size`; `extract_patches` gains `patch_fraction`, `mask`, `min_coverage` (defaults unchanged — same patches as before for the same seed) |
| `training/train.py` | opt-in `SAMPLER_POWER`, `LOSS`, `LOGIT_ADJUST_TAU`, `CLASS_WEIGHTED_LOSS`, `FREEZE_BN`, `PATCH_FRACTION`, `PATCH_MIN_COVERAGE`; `FABRIC_IMATERIALIST_DIR` env var; checkpoints store `patch_config` |
| `training/evaluate.py`, `calibrate.py` | use the shared metrics; calibration merges into `temperature.json` instead of overwriting |
| `training/metrics.py` | `compute_classification_metrics` (adds precision, balanced accuracy, confusion matrix) |
| `postprocess.py` | `softmax`, `aggregate_patch_logits`, `apply_temperature`, `prior_correction`, `format_top_k` |
| `inference.py` | uses the shared post-processing; `predict_detailed`; prior correction + patch config loaded from calibration/checkpoint |
| `web_service.py`, `profiles.py` | web service reuses `predict_detailed` (one code path); profiles moved to a light module |
| `memory_manager.py` | `run_inference(..., return_logits=True)`; errors are raised, not hidden |
| `backend/app.py` | lazy service creation, upload size limit, invalid image → HTTP 400 |

### How to run
```bash
pip install -r requirements.txt   # CPU torch: add --index-url https://download.pytorch.org/whl/cpu
pytest                            # or: python -m unittest discover -s tests -t .
```
CI (`.github/workflows/tests.yml`) runs the full suite, including the PyTorch tests, on every push.
