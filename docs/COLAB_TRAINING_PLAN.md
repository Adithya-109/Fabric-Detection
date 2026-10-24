# Colab Training Plan — Fabric Detection

_Written 2026-10-24. Companion to `docs/IMPROVEMENT_PLAN.md` (the *what to change*); this document is
the *how to run it on Google Colab*. Repo: `Adithya-109/Fabric-Detection`._

---

## 0. The setup in one picture

```
 ┌──────────── Mac (daily driver) ────────────┐        ┌──────── GitHub: Fabric-Detection ───────┐
 │ edit code · run tests (pytest, CPU)        │──push──▶ code, configs, tests, docs, EXP records  │
 │ run web app with downloaded weights        │        │ CI runs the test suite on every push     │
 └───────────────▲────────────────────────────┘        └───────────────┬─────────────────────────┘
                 │ download best weights + calibration                  │ clone pinned commit
 ┌───────────────┴──────────── Google Drive (persistent) ───────────────▼─────────────────────────┐
 │ /FabricDetection/data/shards/*.tar   manifest.csv.gz   /runs/<run_id>/{ckpt, logs, metrics}    │
 └───────────────▲─────────────────────────────────────────────────────┬─────────────────────────┘
                 │ checkpoints every ~15 min + each epoch              │ copy shards → local SSD
 ┌───────────────┴────────────── Colab runtime (disposable) ───────────▼─────────────────────────┐
 │ T4/L4 GPU · data extracted to /content/data · `python -m … train_v2 --config configs/X.yaml`   │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Rules that follow from this picture**
1. **GitHub is the only home for code.** Notebooks are thin launchers (≈10 cells); no logic lives in them.
2. **Drive is the only home for data and results.** The Colab VM can vanish at any moment — design for it.
3. **Every run is reproducible from three things:** git commit SHA + config file + manifest hash. The
   trainer writes all three into the run folder and the checkpoint.
4. **The Mac never trains.** It edits, tests, reviews results, and serves the web app (CPU/MPS inference
   of EfficientNet-B0 is fast enough).

---

## 1. Colab constraints we have to design around

| Constraint | Free tier | Colab Pro (~US$10/mo, 100 compute units) | Design response |
|---|---|---|---|
| GPU | Usually a T4 (16 GB), not guaranteed | T4 / L4 / A100 as available | Config picks AMP dtype per GPU (fp16 on T4, bf16 on L4/A100) |
| Session length | ≤ ~12 h, can end early | Longer, still interruptible (24 h continuous only on Pro+) | **Resumable training**: checkpoint every ~15 min, resume mid-epoch |
| Idle disconnect | ~90 min without interaction (varies) | Same idea | Keep the tab open; never depend on a run finishing in one session |
| Usage quota | Dynamic, unpublished | Compute units: T4 ≈ 1.8 CU/h, A100 ≈ 15 CU/h | Default to T4/L4; A100 is wasted on EfficientNet-B0 |
| CPU | ~2 vCPU | More with High-RAM | **Data loading is the bottleneck, not the GPU** → pre-resized images, cheap per-sample work, benchmark first |
| Disk | Local SSD (tens of GB), wiped each session | Same | Copy tar shards from Drive and extract locally each session (~minutes) |
| Drive FUSE | Very slow for 200k small files | Same | **Never train from Drive folders.** Only big `.tar` shards + one manifest |

Budget guide (estimates to confirm in Phase 0): if an epoch on a T4 takes ~15–20 min, a 15-epoch full
run is ~4–5 h ≈ 8–9 CU — about 10 full runs per month on Colab Pro, or slower progress on the free tier.
Most experiments should be cheaper **proxy runs** (§5.2).

---

## 2. Data: getting ~232k images onto Colab (the critical path)

### 2.1 What exists
| Source | Images (used) | Notes |
|---|---|---|
| iMaterialist (from 153 parquet files, `material` column) | ~216k | Already resized to max side 512; 80/10/10 split by md5; compound materials dropped |
| TextileNet `fabric/` and `fibre/` | ~15k | Close-up textures; **already separates fibre vs fabric taxonomies** (relevant to §5, Phase 6) |
| Microscope (MIT) | ~800 | Very high-res microscope textures |
| iBUG Fabrics (research-only) | ~7.9k | 400×400 patches; off by default |

All of it currently lives in `DATASETS/` on the original Windows machine — **not in git, not on Drive**.

### 2.2 Plan
1. **Locate & transfer (needs your friend / you).** Upload the *processed* folders
   (`imaterialist_processed/`, `TextileNet-main/`, microscope) once, as zip/tar files, to a Drive folder
   `FabricDetection/raw/`. Expected size roughly 8–15 GB (measure it). Free Drive is 15 GB shared with
   Gmail/Photos → **a 100 GB Google One plan is likely needed**.
   _Fallback:_ rebuild in Colab from the original sources (iMaterialist parquets, TextileNet download
   scripts) — slower, but fully reproducible. We need the exact iMaterialist parquet source name for this.
2. **Build the manifest (Colab CPU, once).** `tools/build_manifest.py` scans the raw data and writes one row
   per image: `path, label, source, source_label, sha1, ahash, width, height, group_id, split`.
   - decode check (drop corrupt/tiny images)
   - exact duplicates (sha1) and near-duplicates (`average_hash` + `group_near_duplicates`)
   - **cross-label duplicates** (same picture with two different labels) are reported — direct evidence of label noise
   - **leakage-free split** with `grouped_stratified_split` (70/15/15), per source
3. **Pack into shards.** `tools/pack_shards.py` writes ~1–2 GB uncompressed `.tar` files (JPEGs are already
   compressed) + `manifest.csv.gz` to `FabricDetection/data/`. The manifest's hash is the dataset version
   (`data_v1`, …), recorded in every run.
4. **Session start** (in the notebook): copy shards Drive → `/content/data`, extract, verify the count
   against the manifest. Target: under ~10 min.
5. **Label audit (1–2 h of your time, high value).** A notebook shows random 48-image grids per class;
   you mark obviously wrong labels. Gives a per-class noise estimate — especially Cotton vs Polyester, where
   the label comes from a product listing, not the pixels.
6. **Independent real-world test set.** FTAG (ASOS product photos; labels from the product's fibre
   composition, structure and fabric family). Different source from the training data, so it measures
   generalisation. Map composition to our classes only when one fibre dominates (e.g. ≥ 80%); drop blends.
   Never trained on. Covers dresses only, so per-class support will be uneven — report it.

> The new split changes the test set, so Attempt 309's 43% is **not comparable** to new numbers.
> First job on the new split: re-evaluate the existing `fabric_clf_best.pt` → that is the new baseline.

---

## 3. Code to build before any training (test-first, as before)

| Module | Purpose | Key tests |
|---|---|---|
| `tools/build_manifest.py` | scan → manifest rows, dedupe, grouped split | stable output for same input; no group spans splits; corrupt files excluded |
| `tools/pack_shards.py` / `unpack_shards.py` | manifest → tar shards and back | round-trip gives identical bytes; shard size limit respected |
| `training/data.py` | `ManifestDataset` (train: 1 random patch; eval: 7 patches), mask/patch config | labels/indices match manifest; deterministic eval patches |
| `training/checkpointing.py` | atomic save (tmp → rename), resume incl. optimizer, scheduler, AMP scaler, RNG, sampler position | save → load → identical state; resume mid-epoch continues at the right step |
| `training/config.py` | load YAML config, validate, merge CLI overrides, hash | unknown keys rejected; hash stable |
| `training/train_v2.py` | lean trainer reusing tested modules: AMP, cosine + warmup, time-based checkpoints, JSONL logs | 2-batch smoke run on CPU in CI with a tiny fake dataset |
| `training/report.py` | per-run report: metrics JSON, confusion matrix PNG, per-class precision/recall | runs on saved logits |
| `notebooks/colab_train.ipynb` | thin launcher (mount, clone, unpack, run, sync) | manual smoke run |
| `configs/*.yaml` | one file per experiment | — |

**Why a new trainer instead of porting `train.py`:** the legacy trainer (1,870 lines) is built around one
Windows box — process locks, psutil resource governors, auto-retry loops, download gates, absolute paths.
None of that helps on Colab, and its retry loop fights preemption-safe resuming. `train.py` stays in the
repo as reference; the new trainer reuses the already-tested pieces (`postprocess`, `balancing`, `losses`,
`metrics`, `splits`, `dataset`). The checkpoint format stays compatible with `FabricClassifier`, so the web
app keeps working.

**Private repo from Colab:** create a fine-grained GitHub token (read-only, this repo only) and store it in
**Colab Secrets** (key icon) — never paste it in a cell. Notebook clones `--branch <branch>` and logs the SHA.

---

## 4. Phase 0 — infrastructure shakedown (no science yet)

Exit criteria, all on Colab:
- [ ] Data unpacked from Drive and verified against manifest in < ~10 min
- [ ] Smoke run: 1% of data, 1 epoch, end to end, writes run folder + checkpoint to Drive
- [ ] **Kill test:** disconnect the runtime mid-epoch, reconnect, resume → step count and loss curve continue
- [ ] Throughput benchmark: images/s for (a) decode only, (b) decode + patch extraction, (c) full train step,
      at 2 and 4 workers → tells us whether CPU or GPU is the bottleneck and the real epoch time
- [ ] Batch-size probe: largest batch that fits on T4 with AMP (expect ≥ 64 vs 4 on the 3050)

If CPU-bound (likely): pre-compute garment masks/bounding boxes once into the manifest, decode JPEGs on
GPU (`torchvision.io.decode_jpeg(device="cuda")`), and validate on a fixed subset per epoch with the
full val set only at the end.

---

## 5. Experiment roadmap

### 5.1 Protocol (unchanged project rules, adapted to Colab)
- One change per experiment; an `EXP-4xx` record in `memory/records/` **before** launching.
- Select on **val**; read **test** once per phase; report three test numbers: iMaterialist-test
  (garment photos), TextileNet-test (close-ups), in-the-wild (your photos).
- Always report per-class precision **and** recall + confusion matrix, not just top-1.

### 5.2 Proxy runs vs full runs
Rank ideas with **proxy runs**: fixed stratified 25% of train, full val, ~8 epochs (~1 h on T4).
Promote only winners to **full runs** (all data, ~15 epochs). Check once that proxy ranking agrees with
full-run ranking (baseline vs best) — if it doesn't, proxies are dropped.

### 5.3 Phases

| Phase | Runs | What | Decision gate |
|---|---|---|---|
| **1. Baselines, no training** | ~1 h GPU | Re-evaluate existing `best.pt` on the new split; prior-correction sweep (`prior_sweep.py`); fit temperature | Ship corrected model to the Mac web app immediately |
| **2. New-hardware control** | 1 full | Legacy recipe (double balancing kept) but batch 64 + AMP + new split. Isolates the hardware/batch effect | This is the control every later run is compared to |
| **3. Fix imbalance** | 3 proxy + 1 full | (a) natural sampling + logit-adjusted loss, (b) √-sampling + logit-adjusted loss, (c) √-sampling + plain CE | Pick by val macro-F1 with worst-recall ≥ 0.40 as tie-breaker |
| **4. Input pipeline** | 3 proxy + 1 full | (a) `PATCH_FRACTION=0.2` + `PATCH_MIN_COVERAGE=0.9`; (b) training patches per image; (c) augmentation: RandomResizedCrop scale, light colour jitter only (colour is informative: denim) | Keep only what helps val |
| **5. Ceiling diagnostic** | ~2 h total | Frozen self-supervised encoder (DINOv2-S) → cache embeddings once → train linear/MLP heads in minutes | If a linear probe ≈ fine-tuned B0 → the limit is **labels/taxonomy**, not the network. If much higher → consider a backbone change (needs your OK: B0 is a project contract) |
| **6. Taxonomy** (if you approve) | 1–2 full | Two heads: fibre & construction. TextileNet already ships `fibre/` and `fabric/` separately; iMaterialist `material` strings map to one or both | Measure each head against its own targets |
| **7. General photos** | 1 offline job + 1 full | Run a clothes-segmentation model over the dataset once (store masks); train + infer with `extract_patches(mask=…)`; measure on in-the-wild set | Ship only if in-the-wild improves |
| **8. Final** | 1 full | Winning recipe; temperature + prior calibration on val; test once; export | Weights + `temperature.json` + `patch_config` → Mac web app; EXP records; HOT.md |

**Expected effort:** Phase 0 ≈ 1–2 sessions; Phases 1–4 ≈ 1–2 weeks part-time; 5–8 depend on decisions.
Roughly 8–12 full-run equivalents in total → fits in about one month of Colab Pro, or longer on free tier.

---

## 6. Run hygiene (what every run writes to Drive)

```
runs/2026-11-02_exp402_sqrt_la/
  config.yaml            # exact config used
  run_meta.json          # git SHA, branch, manifest hash, GPU type, torch version, start/end time
  epoch_log.jsonl        # one line per epoch: losses, val metrics, lr, throughput
  checkpoints/last.pt    # resumable (atomic writes)
  checkpoints/best.pt    # FabricClassifier-compatible (state dict + class names + patch_config)
  val_logits.npz         # for prior sweep / calibration / reports without re-running the model
  report/                # metrics.json, confusion_matrix.png, per_class.csv
```
Optional: Weights & Biases (free personal tier) to watch curves from the Mac; JSONL on Drive remains the
source of truth.

---

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Can't get `DATASETS/` off the Windows machine | Medium | Rebuild from source (need iMaterialist parquet source); start with TextileNet + microscope meanwhile |
| Drive storage too small | High on free 15 GB | Google One 100 GB; or re-encode images at lower JPEG quality |
| Colab disconnects mid-run | Certain, eventually | Time-based checkpoints + resume (tested kill test in Phase 0) |
| Data loading starves the GPU | High (2 vCPU) | Benchmark first; precomputed masks; GPU JPEG decode; subset validation |
| iMaterialist labels too noisy (blends, listing errors) | Medium–High | Label audit; cross-label duplicate report; noise-robust options if needed (label smoothing, small-loss filtering) |
| Proxy runs mislead | Low–Medium | One proxy-vs-full agreement check |
| Overfitting decisions to test | Medium | Test read once per phase; in-the-wild set never used for selection |
| Results unreproducible | Low with this design | SHA + config + manifest hash in every run |

---

## 8. Decisions (2026-10-24)

| Question | Decision |
|---|---|
| Storage | 5 TB Google Drive available → store raw data, shards and all runs on Drive; no compression trade-offs needed |
| Compute | Free Colab for Phases 0–1; reconsider Colab Pro when full runs start |
| Backbone | **Stay on EfficientNet-B0.** Phase 5 measures the gap with a cheap frozen-encoder probe; switch only if a stronger backbone beats B0 by a clear margin (proposed: ≥ 5 points val macro-F1) |
| Real-world test set | Use a **public dataset from a different source** instead of 300 own photos: FTAG (ASOS garment photos with fibre composition, structure and fabric-family labels; research-only, gated, images downloaded from product URLs). Optional small own-photo sanity set (~50) later |
| Branch | `feature/tests-and-accuracy-plan` merged into `main` |
| Still open | Location/size of `DATASETS/`; taxonomy (14 classes vs fibre + construction) |

## 9. What I build next (once data location is known)
1. `tools/build_manifest.py`, `pack_shards.py` (+ tests)
2. `training/config.py`, `checkpointing.py`, `data.py`, `train_v2.py` (+ tests, CPU smoke run in CI)
3. `notebooks/colab_train.ipynb`, `notebooks/label_audit.ipynb`
4. `configs/` for Phases 1–3
