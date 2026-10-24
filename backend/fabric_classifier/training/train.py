import torch
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from torch.optim.lr_scheduler import CosineAnnealingLR
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler, default_collate
from sklearn.model_selection import train_test_split
from collections import defaultdict
from functools import lru_cache
import os
import json
import sys
import subprocess
import traceback
import zlib
from PIL import Image, ImageFile
from tqdm import tqdm
import numpy as np
import time
import warnings
from pathlib import Path
import atexit
from datetime import datetime, timezone

import psutil

warnings.filterwarnings("ignore", message="`torch.cuda.amp.GradScaler")
warnings.filterwarnings("ignore", message="`torch.cuda.amp.autocast")
warnings.filterwarnings("ignore", message=r"Detected call of `lr_scheduler.step\(\)` before `optimizer.step\(\)`")

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Project-relative imports (fallback to absolute imports when run as a script).
try:
    from ..model import get_model
    from ..classes import MATERIAL_CLASSES, TEXTILENET_TO_TARGET
    from .dataset import extract_patches
    from .evaluate import evaluate_model
    from .calibrate import calibrate_temperature
    from .resource_manager import get_resource_manager
    from .balancing import effective_training_prior, tempered_sample_weights
    from .losses import LogitAdjustedLoss, freeze_batchnorm
except ImportError:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    from backend.fabric_classifier.model import get_model
    from backend.fabric_classifier.classes import MATERIAL_CLASSES, TEXTILENET_TO_TARGET
    from backend.fabric_classifier.training.dataset import extract_patches
    from backend.fabric_classifier.training.evaluate import evaluate_model
    from backend.fabric_classifier.training.calibrate import calibrate_temperature
    from backend.fabric_classifier.training.resource_manager import get_resource_manager
    from backend.fabric_classifier.training.balancing import effective_training_prior, tempered_sample_weights
    from backend.fabric_classifier.training.losses import LogitAdjustedLoss, freeze_batchnorm

# --- Configuration & Paths ---
# Use relative paths from the project root
DATA_SOURCE_DIRS = [
    "DATASETS/TextileNet-main/fabric",
    "DATASETS/TextileNet-main/fibre",
]
OUTPUT_DIR = "backend/fabric_classifier"
WEIGHTS_DIR = os.path.join(OUTPUT_DIR, "weights")
LOG_FILE = os.path.join(OUTPUT_DIR, "training/training_log.json")
EPOCH_PROGRESS_FILE = os.path.join(OUTPUT_DIR, "training/epoch_progress.jsonl")
ISSUES_LOG_FILE = os.path.join(OUTPUT_DIR, "training/issues_log.json")
EXPERIMENT_LOG_FILE = os.path.join(OUTPUT_DIR, "training/experiment_log.md")
ADDITIONAL_DATA_MANIFEST_FILE = os.path.join(OUTPUT_DIR, "training/additional_data_manifest.json")
BEST_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, "fabric_clf_best.pt")
LAST_CHECKPOINT_PATH = os.path.join(WEIGHTS_DIR, "fabric_clf_last.pt")
SINGLETON_LOCK_PATH = os.path.join(OUTPUT_DIR, "training", "runtime_control", "train_singleton.lock")
MIN_VALID_IMAGES_PER_CLASS = 150

os.makedirs(WEIGHTS_DIR, exist_ok=True)

# --- Hyperparameters ---
# Encapsulate hyperparameters in a dictionary for easy logging and modification
HYPERPARAMS = {
    "BATCH_SIZE": 4,
    "EPOCHS_MAX": 60,
    "LR_BACKBONE": 1e-4,
    "LR_HEAD": 1e-3,
    "WEIGHT_DECAY": 1e-4,
    "LABEL_SMOOTHING": 0.02,
    "PATIENCE": 10,
    "IMG_SIZE": 224,
    "AUG_ROTATION_DEG": 20,
    "AUG_BRIGHTNESS": 0.3,
    "AUG_CONTRAST": 0.3,
    "AUG_SATURATION": 0.2,
    "AUG_HUE": 0.05,
    "N_PATCHES_TRAIN": 2,
    "N_PATCHES_INFER": 7,
    "HEAD_ONLY_EPOCHS": 3,
    "DEVICE": "cuda",
    "NUM_WORKERS": 4,
    "PIN_MEMORY": True,
    "GRAD_ACCUM_STEPS": 2,
    "BATCH_HEARTBEAT_STEPS": 100,
    "MAX_IMAGES_PER_CLASS": 10000000,
    "POLICY_STOP_MIN_EPOCHS": 20,
    "POLICY_STOP_WINDOW": 10,
    "POLICY_MIN_TOP1_GAIN": 0.005,
    "POLICY_MIN_MACRO_F1_GAIN": 0.005,
    "USE_MICROSCOPE_DATA": True,
    "USE_IBUG_RESEARCH_DATA": False,
    "USE_IMATERIALIST_DATA": True,
    # --- Accuracy-plan switches (docs/IMPROVEMENT_PLAN.md). Defaults reproduce the legacy trainer. ---
    # Class c is sampled with probability ∝ count_c ** SAMPLER_POWER (0 = balanced/legacy, 0.5 = sqrt, 1 = natural).
    "SAMPLER_POWER": 0.0,
    # "cross_entropy" (legacy) or "logit_adjusted" (Menon et al. 2021; ignores CLASS_WEIGHTED_LOSS).
    "LOSS": "cross_entropy",
    "LOGIT_ADJUST_TAU": 1.0,
    # Legacy also weights the CE loss by inverse class frequency (double balancing with the sampler).
    "CLASS_WEIGHTED_LOSS": True,
    # Keep BatchNorm in eval mode during fine-tuning (batch size 4 is too small for BN statistics).
    "FREEZE_BN": False,
    # Patch geometry: None = fixed 160 px (legacy); e.g. 0.2 = 20% of the garment's short side.
    "PATCH_FRACTION": None,
    # Minimum share of each patch on the garment mask (legacy 0.5).
    "PATCH_MIN_COVERAGE": 0.5,
}

# Override with FABRIC_IMATERIALIST_DIR to run on machines other than the original Windows box.
IMATERIALIST_DIR = os.environ.get(
    "FABRIC_IMATERIALIST_DIR",
    r"c:\Users\A0SKZ\STORE\ALL_CODE\MachineLearning\DATASETS\imaterialist_processed",
)

# Prefer direct fibre/fabric sources when available; fall back to proxy sources for coverage.
TARGET_PRIMARY_SOURCES = {
    "Cotton": ["cotton"],
    "Polyester": ["polyester"],
    "Silk": ["silk"],
    "Denim": ["denim"],
    "Linen": ["linen", "flax_linen", "ramie", "hemp"],
    "Wool": ["wool", "cashmere", "alpaca", "mohair", "angora", "camel", "yak", "llama"],
    "Leather": ["leather"],
    "Velvet": ["velvet"],
    "Corduroy": ["corduroy"],
    "Fleece": ["fleece", "fur"],
    "Nylon": ["nylon", "polyolefin", "elastane_spandex", "aramid"],
    "Satin": ["satin"],
    "Knitted": ["knit", "knitted"],
    "Suede": ["suede"],
}

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
_LOCK_ACQUIRED = False

ATTEMPT17_MIN_VALID_COUNTS = {
    "Corduroy": 600,
    "Suede": 600,
    "Wool": 600,
}

ATTEMPT17_DOWNLOAD_TARGETS = {
    "Corduroy": {"subset": "fabric", "source_class": "corduroy"},
    "Suede": {"subset": "fibre", "source_class": "suede"},
    "Wool": {"subset": "fibre", "source_class": "wool"},
}


def read_issues_log():
    try:
        with open(ISSUES_LOG_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
            if isinstance(payload, list):
                return payload
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []


def append_issue(category, severity, title, details, action_taken, status="open"):
    issues = read_issues_log()
    issues.append({
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "category": category,
        "severity": severity,
        "title": title,
        "details": details,
        "action_taken": action_taken,
        "status": status,
    })
    os.makedirs(os.path.dirname(ISSUES_LOG_FILE), exist_ok=True)
    with open(ISSUES_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2)


def ensure_experiment_log_file():
    os.makedirs(os.path.dirname(EXPERIMENT_LOG_FILE), exist_ok=True)
    if os.path.exists(EXPERIMENT_LOG_FILE):
        return

    with open(EXPERIMENT_LOG_FILE, "w", encoding="utf-8") as f:
        f.write("# Experiment Log\n\n")
        f.write("This file is read before each attempt and appended after each attempt.\n")


def read_experiment_log_tail(max_lines=160):
    if not os.path.exists(EXPERIMENT_LOG_FILE):
        return ""

    try:
        with open(EXPERIMENT_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[-max_lines:])
    except OSError:
        return ""


def append_experiment_postmortem(attempt_num, params, log_entry, was_success):
    ensure_experiment_log_file()

    metrics = log_entry.get("final_metrics_achieved") if isinstance(log_entry.get("final_metrics_achieved"), dict) else {}
    inference = log_entry.get("inference_metrics") if isinstance(log_entry.get("inference_metrics"), dict) else {}
    policy = log_entry.get("policy_stop_trigger")

    top1 = metrics.get("top1_accuracy")
    top3 = metrics.get("top3_accuracy")
    macro_f1 = metrics.get("macro_f1")
    worst = metrics.get("worst_class_recall")
    latency = inference.get("inference_time_ms")
    vram = inference.get("vram_mb")

    if was_success:
        learned = "Targets met under current policy and data setup."
        next_step = "Stop retry loop and keep this checkpoint/calibration as active deliverable."
        wrong = "No blocking issues."
    else:
        reason = str(log_entry.get("reason_for_retry", "Targets not met."))
        if "research-only" in reason.lower() or bool(log_entry.get("research_only_data_used", False)):
            wrong = "Run used research-only data, so it cannot be accepted as final deliverable."
            learned = "Research-only augmentation can be useful for direction finding, but final package must exclude it."
            next_step = "Disable research-only data for the next attempt and confirm metrics on commercial-safe data only."
        elif isinstance(policy, dict):
            wrong = f"Policy stop trigger fired: {policy.get('rule', 'unknown')}"
            learned = "Current hyperparameter/data configuration plateaued before reaching required metrics."
            next_step = "Apply auto-retry adjustments and continue from best warm-start checkpoint."
        else:
            wrong = reason
            learned = "Current changes improved some metrics but not enough to satisfy all acceptance thresholds."
            next_step = "Adjust learning schedule/data mix and continue automated retries."

    with open(EXPERIMENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n")
        f.write(f"## Attempt {attempt_num} Post-Mortem\n")
        f.write(f"- Timestamp UTC: {datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}\n")
        f.write(f"- Status: {log_entry.get('status', 'unknown')}\n")
        f.write(f"- Targets Met: {bool(log_entry.get('targets_met', False))}\n")
        f.write(f"- Research-Only Data Used: {bool(log_entry.get('research_only_data_used', False))}\n")
        f.write(f"- What I Tried: Hyperparameters/data toggles = {json.dumps(params, ensure_ascii=True)}\n")
        f.write(
            "- Metrics: "
            f"top1={top1}, top3={top3}, macro_f1={macro_f1}, worst_recall={worst}, "
            f"inference_ms={latency}, vram_mb={vram}\n"
        )
        f.write(f"- What Went Wrong: {wrong}\n")
        f.write(f"- What I Learned: {learned}\n")
        f.write(f"- What I Will Do Next: {next_step}\n")


def load_additional_data_sources(use_microscope=True, use_ibug_research=False):
    merged = defaultdict(lambda: defaultdict(list))

    if not os.path.exists(ADDITIONAL_DATA_MANIFEST_FILE):
        print("No additional data manifest found; using TextileNet-only sources.")
        return merged

    try:
        with open(ADDITIONAL_DATA_MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: additional_data_manifest.json is unreadable; continuing without extra datasets.")
        return merged

    dataset_payload = manifest.get("datasets") if isinstance(manifest, dict) else {}
    if not isinstance(dataset_payload, dict):
        return merged

    selected_keys = []
    if bool(use_microscope):
        selected_keys.append("microscope_mit")
    if bool(use_ibug_research):
        selected_keys.append("ibug_research_only")

    counts_summary = defaultdict(int)
    for ds_key in selected_keys:
        ds = dataset_payload.get(ds_key)
        if not isinstance(ds, dict):
            continue

        images_by_target = ds.get("images_by_target")
        if not isinstance(images_by_target, dict):
            continue

        for target_class, rel_paths in images_by_target.items():
            if target_class not in MATERIAL_CLASSES or not isinstance(rel_paths, list):
                continue

            valid_paths = []
            for rel_path in rel_paths:
                if not isinstance(rel_path, str):
                    continue
                candidate = Path(rel_path)
                if not candidate.is_absolute():
                    candidate = PROJECT_ROOT / candidate
                candidate = candidate.resolve()
                if not candidate.exists() or not candidate.is_file():
                    continue
                if candidate.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                valid_paths.append(str(candidate))

            if valid_paths:
                source_key = f"extra_{ds_key}"
                merged[target_class][source_key].extend(valid_paths)
                counts_summary[target_class] += len(valid_paths)

    if counts_summary:
        print("Loaded additional dataset paths by class:")
        for class_name in MATERIAL_CLASSES:
            if counts_summary.get(class_name, 0) > 0:
                print(f"  {class_name}: +{counts_summary[class_name]}")
    else:
        print("No additional dataset paths were loaded from manifest.")

    return merged


def find_other_training_pids():
    """Returns other running train.py PIDs to prevent concurrent checkpoint writers."""
    my_pid = os.getpid()
    found = []
    needles = (
        " -m backend.fabric_classifier.training.train",
        "backend/fabric_classifier/training/train.py",
        "backend\\fabric_classifier\\training\\train.py",
    )

    for proc in psutil.process_iter(attrs=["pid", "cmdline"]):
        try:
            pid = int(proc.info.get("pid", 0))
            if pid <= 0 or pid == my_pid:
                continue
            cmd = " ".join(proc.info.get("cmdline") or []).lower()
            if any(n in cmd for n in needles):
                found.append(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, ValueError, TypeError):
            continue
    return sorted(set(found))


def count_valid_images_for_target_class(target_class_name, stop_at=800):
    """Counts valid images for a target class across mapped TextileNet source folders."""
    mapped_sources = [
        source_name for source_name, mapped_target in TEXTILENET_TO_TARGET.items()
        if mapped_target == target_class_name
    ]
    if not mapped_sources:
        return 0

    valid_count = 0
    for base_dir in DATA_SOURCE_DIRS:
        for split in ("train", "test"):
            for source_name in mapped_sources:
                source_dir = Path(base_dir) / split / source_name
                if not source_dir.exists() or not source_dir.is_dir():
                    continue

                for image_path in source_dir.rglob("*"):
                    if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                        continue
                    try:
                        with Image.open(image_path) as img:
                            img.verify()
                        valid_count += 1
                    except Exception:
                        continue

                    if valid_count >= stop_at:
                        return valid_count

    return valid_count


def attempt5_weak_class_data_gate(min_valid_images=800):
    """Blocks attempt 5 until attempt 4 weak classes are verified with enough clean images."""
    diagnostics_path = os.path.join(OUTPUT_DIR, "training", "attempt4_diagnostics.json")
    if not os.path.exists(diagnostics_path):
        msg = "Missing attempt4_diagnostics.json; cannot validate mandatory attempt-5 data gate."
        print(msg)
        append_issue(
            category="data_gate",
            severity="high",
            title="Attempt 5 blocked: diagnostics file missing",
            details=msg,
            action_taken="Launch aborted until diagnostics artifact is generated.",
            status="open",
        )
        return False

    try:
        with open(diagnostics_path, "r", encoding="utf-8") as f:
            diagnostics = json.load(f)
    except json.JSONDecodeError as exc:
        msg = f"Diagnostics file is invalid JSON: {exc}"
        print(msg)
        append_issue(
            category="data_gate",
            severity="high",
            title="Attempt 5 blocked: diagnostics file invalid",
            details=msg,
            action_taken="Launch aborted until diagnostics artifact is repaired.",
            status="open",
        )
        return False

    weak_classes = diagnostics.get("weak_classes_below_0_40_test_recall", [])
    if not weak_classes:
        append_issue(
            category="data_gate",
            severity="low",
            title="Attempt 5 gate pass: no weak classes",
            details="No classes were below 0.40 test recall in attempt 4 diagnostics.",
            action_taken="Attempt 5 launch permitted.",
            status="resolved",
        )
        return True

    gate_details = []
    gate_failures = []
    for weak_item in weak_classes:
        class_name = weak_item.get("class")
        recall = float(weak_item.get("recall", 0.0))
        valid_count = count_valid_images_for_target_class(class_name, stop_at=min_valid_images)
        passed = valid_count >= min_valid_images
        gate_details.append({
            "class": class_name,
            "recall": recall,
            "valid_count": valid_count,
            "required": min_valid_images,
            "gate_passed": passed,
        })
        if not passed:
            gate_failures.append(class_name)

    if gate_failures:
        msg = f"Attempt 5 blocked. Classes below {min_valid_images} valid images: {gate_failures}"
        print(msg)
        append_issue(
            category="data_gate",
            severity="high",
            title="Attempt 5 blocked: weak-class data gate failed",
            details=json.dumps(gate_details),
            action_taken="Launch aborted until weak-class images are topped up and verified.",
            status="open",
        )
        return False

    append_issue(
        category="data_gate",
        severity="medium",
        title="Attempt 5 weak-class data gate passed",
        details=json.dumps(gate_details),
        action_taken="All weak classes have required valid image count. Launch permitted.",
        status="resolved",
    )
    return True


def get_target_valid_count_snapshot(min_counts):
    snapshot = {}
    for class_name, required in min_counts.items():
        stop_at = max(int(required) + 200, int(required))
        snapshot[class_name] = int(count_valid_images_for_target_class(class_name, stop_at=stop_at))
    return snapshot


def run_subset_download(subset, source_classes, max_per_class):
    classes = sorted({c for c in source_classes if c})
    if not classes:
        return True

    cmd = [
        sys.executable,
        "-m",
        "backend.fabric_classifier.training.download_fibre_subset",
        "--subset",
        subset,
        "--classes",
        *classes,
        "--max-per-class",
        str(int(max_per_class)),
        "--workers",
        "4",
        "--max-workers",
        "4",
        "--timeout",
        "12",
        "--retries",
        "2",
    ]

    print(f"Running targeted download for subset={subset}, classes={classes}, max_per_class={max_per_class}")
    env = os.environ.copy()
    env["FABRIC_RESOURCE_IGNORE_TRAINING_ACTIVE"] = "1"
    completed = subprocess.run(cmd, check=False, env=env)
    if completed.returncode != 0:
        append_issue(
            category="data_download",
            severity="high",
            title="Targeted class download failed",
            details=json.dumps({"subset": subset, "classes": classes, "returncode": completed.returncode}),
            action_taken="Will continue with available data and re-check counts.",
            status="open",
        )
        return False
    return True


def ensure_attempt17_target_data(min_counts, max_rounds=3):
    counts = get_target_valid_count_snapshot(min_counts)

    for round_idx in range(1, int(max_rounds) + 1):
        needed = [cls for cls, required in min_counts.items() if counts.get(cls, 0) < int(required)]
        if not needed:
            break

        print(f"Attempt 17 data gate round {round_idx}: current counts {counts}")
        prior_counts = counts.copy()
        gaps = [max(0, int(min_counts[cls]) - int(counts.get(cls, 0))) for cls in needed]
        largest_gap = max(gaps) if gaps else 0
        # Keep top-ups focused and bounded to avoid prolonged pre-launch delays.
        per_class_cap = min(500, max(120, largest_gap * 2 + (round_idx - 1) * 80))

        fabric_classes = [
            ATTEMPT17_DOWNLOAD_TARGETS[c]["source_class"]
            for c in needed
            if ATTEMPT17_DOWNLOAD_TARGETS[c]["subset"] == "fabric"
        ]
        fibre_classes = [
            ATTEMPT17_DOWNLOAD_TARGETS[c]["source_class"]
            for c in needed
            if ATTEMPT17_DOWNLOAD_TARGETS[c]["subset"] == "fibre"
        ]

        if fabric_classes:
            run_subset_download("fabric", fabric_classes, max_per_class=per_class_cap)
        if fibre_classes:
            run_subset_download("fibre", fibre_classes, max_per_class=per_class_cap)

        counts = get_target_valid_count_snapshot(min_counts)
        gains = {cls: int(counts.get(cls, 0)) - int(prior_counts.get(cls, 0)) for cls in needed}
        print(f"Attempt 17 data gate round {round_idx}: gains {gains}, updated counts {counts}")

        if all(delta <= 0 for delta in gains.values()):
            append_issue(
                category="data_gate",
                severity="medium",
                title="Attempt 17 targeted top-up yielded no valid-count gain",
                details=json.dumps({
                    "round": round_idx,
                    "needed": needed,
                    "prior_counts": prior_counts,
                    "updated_counts": counts,
                    "gains": gains,
                }),
                action_taken="Stopped further targeted download rounds to avoid prolonged pre-launch delay.",
                status="open",
            )
            break

    gate_ok = all(counts.get(cls, 0) >= required for cls, required in min_counts.items())
    append_issue(
        category="data_gate",
        severity="low" if gate_ok else "high",
        title="Attempt 17 targeted data gate result",
        details=json.dumps({"required": min_counts, "final_counts": counts}),
        action_taken="Proceeding with next attempt using refreshed target-class data.",
        status="resolved" if gate_ok else "open",
    )
    return gate_ok, counts


def apply_attempt17_stabilization_profile(params):
    params["LR_BACKBONE"] = min(float(params.get("LR_BACKBONE", 1e-4)), 2e-5)
    params["LR_HEAD"] = min(float(params.get("LR_HEAD", 1e-3)), 3.5e-4)
    params["LABEL_SMOOTHING"] = min(float(params.get("LABEL_SMOOTHING", 0.02)), 0.01)
    params["HEAD_ONLY_EPOCHS"] = max(int(params.get("HEAD_ONLY_EPOCHS", 3)), 5)
    params["EPOCHS_MAX"] = max(int(params.get("EPOCHS_MAX", 60)), 160)
    params["PATIENCE"] = max(int(params.get("PATIENCE", 10)), 30)
    params["GRAD_ACCUM_STEPS"] = max(int(params.get("GRAD_ACCUM_STEPS", 2)), 4)
    params["AUG_ROTATION_DEG"] = 12
    params["AUG_BRIGHTNESS"] = 0.2
    params["AUG_CONTRAST"] = 0.2
    params["AUG_SATURATION"] = 0.15
    params["AUG_HUE"] = 0.03
    return params


def _is_process_alive(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def acquire_singleton_lock():
    """Prevents concurrent train.py instances from writing the same checkpoint files."""
    global _LOCK_ACQUIRED
    os.makedirs(os.path.dirname(SINGLETON_LOCK_PATH), exist_ok=True)

    if os.path.exists(SINGLETON_LOCK_PATH):
        stale_pid = None
        try:
            with open(SINGLETON_LOCK_PATH, "r", encoding="utf-8") as f:
                stale_pid = int(json.load(f).get("pid", 0))
        except Exception:
            stale_pid = None

        if stale_pid and _is_process_alive(stale_pid):
            print(
                f"Another train.py process appears active (pid={stale_pid}). "
                "Exiting this launch to avoid concurrent checkpoint/log writes."
            )
            return False

        try:
            os.remove(SINGLETON_LOCK_PATH)
        except OSError:
            pass

    lock_payload = {
        "pid": os.getpid(),
        "timestamp": time.time(),
        "argv": sys.argv,
    }

    try:
        fd = os.open(SINGLETON_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(lock_payload, f, indent=2)
        _LOCK_ACQUIRED = True
        return True
    except FileExistsError:
        print("A training singleton lock already exists. Exiting this launch safely.")
        return False


def release_singleton_lock():
    global _LOCK_ACQUIRED
    if not _LOCK_ACQUIRED:
        return

    try:
        if os.path.exists(SINGLETON_LOCK_PATH):
            os.remove(SINGLETON_LOCK_PATH)
    except OSError:
        pass

    _LOCK_ACQUIRED = False

# --- Dataset Handling ---
class FabricDataset(Dataset):
    def __init__(self, file_paths, labels, transform, n_patches, is_train=False):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform
        self.n_patches = n_patches
        self.is_train = is_train
        self.corrupt_warn_limit = 20
        self._corrupt_warned = 0

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        img_path = self.file_paths[idx]
        label = self.labels[idx]
        patch_rng = None

        if not self.is_train:
            seed = zlib.crc32(os.path.normpath(img_path).encode("utf-8")) & 0xFFFFFFFF
            patch_rng = np.random.default_rng(seed)
        
        try:
            with Image.open(img_path) as image:
                image = image.convert("RGBA")
                patches = extract_patches(
                    image,
                    n_patches=self.n_patches,
                    input_size=HYPERPARAMS["IMG_SIZE"],
                    rng=patch_rng,
                    patch_fraction=HYPERPARAMS.get("PATCH_FRACTION"),
                    min_coverage=HYPERPARAMS.get("PATCH_MIN_COVERAGE", 0.5),
                )
            
            if self.is_train:
                # For training, return one random patch per call
                patch = patches[np.random.randint(len(patches))]
                return self.transform(patch), label
            else:
                # For validation/testing, return all patches
                patch_tensors = torch.stack([self.transform(p) for p in patches])
                return patch_tensors, label
        except Exception as e:
            # Return a dummy item on error
            if self._corrupt_warned < self.corrupt_warn_limit:
                print(f"\nWarning: Corrupted image {img_path}, skipping. Error: {e}")
                self._corrupt_warned += 1
                if self._corrupt_warned == self.corrupt_warn_limit:
                    print("Further corrupted image warnings suppressed for this dataset instance.")
            if self.is_train:
                return torch.zeros((3, HYPERPARAMS["IMG_SIZE"], HYPERPARAMS["IMG_SIZE"])), -1
            else:
                return torch.zeros((self.n_patches, 3, HYPERPARAMS["IMG_SIZE"], HYPERPARAMS["IMG_SIZE"])), -1

def collate_fn_filter_corrupted(batch):
    """Custom collate_fn to filter out corrupted samples."""
    filtered_batch = []
    for sample in batch:
        label = sample[1]
        if isinstance(label, torch.Tensor):
            label = int(label.item())
        if label == -1:
            continue
        filtered_batch.append(sample)

    if not filtered_batch:
        return torch.empty(0), torch.empty(0, dtype=torch.long)
    return default_collate(filtered_batch)


@lru_cache(maxsize=32768)
def is_image_decodable(image_path):
    """Checks image decode validity once per path to avoid repeated corruption hits."""
    normalized = os.path.normpath(image_path)
    try:
        with Image.open(normalized) as img:
            img.verify()
        return True
    except Exception:
        return False


def balanced_sample_from_sources(source_to_files, max_images):
    """Round-robin sampling across source subclasses to reduce single-source dominance."""
    if max_images <= 0:
        return []

    pools = {}
    for source_name, files in source_to_files.items():
        deduped = list(dict.fromkeys(files))
        np.random.shuffle(deduped)
        if deduped:
            pools[source_name] = deduped

    if not pools:
        return []

    cursors = {k: 0 for k in pools.keys()}
    active_sources = list(pools.keys())
    selected = []

    while active_sources and len(selected) < max_images:
        np.random.shuffle(active_sources)
        next_active = []
        for source_name in active_sources:
            idx = cursors[source_name]
            files = pools[source_name]
            if idx >= len(files):
                continue

            selected.append(files[idx])
            cursors[source_name] = idx + 1

            if cursors[source_name] < len(files):
                next_active.append(source_name)

            if len(selected) >= max_images:
                break

        active_sources = next_active

    return selected


def prioritized_sample_from_sources(target_class_name, source_to_files, max_images):
    """Prefers primary sources first, then backfills from secondary sources."""
    if max_images <= 0 or not source_to_files:
        return []

    primary_names = set(TARGET_PRIMARY_SOURCES.get(target_class_name, []))
    primary_pool = {k: v for k, v in source_to_files.items() if k in primary_names}
    secondary_pool = {k: v for k, v in source_to_files.items() if k not in primary_names}

    selected = []
    seen = set()

    if primary_pool:
        primary_target = min(max_images, int(round(max_images * 0.8)))
        for path in balanced_sample_from_sources(primary_pool, primary_target):
            if path in seen:
                continue
            selected.append(path)
            seen.add(path)

    remaining = max_images - len(selected)
    if remaining > 0:
        fill_pool = secondary_pool if selected else source_to_files
        for path in balanced_sample_from_sources(fill_pool, remaining):
            if path in seen:
                continue
            selected.append(path)
            seen.add(path)
            if len(selected) >= max_images:
                break

    if len(selected) < max_images:
        for path in balanced_sample_from_sources(source_to_files, max_images - len(selected)):
            if path in seen:
                continue
            selected.append(path)
            seen.add(path)
            if len(selected) >= max_images:
                break

    return selected[:max_images]


def build_dataloaders(train_dataset, val_dataset, test_dataset, train_labels, device, batch_size, num_workers, pin_memory,
                      sampler_power=0.0):
    # Class c is drawn with probability ∝ count_c ** sampler_power (0.0 = fully balanced, the legacy behaviour).
    sample_weights = tempered_sample_weights(train_labels, len(MATERIAL_CLASSES), power=float(sampler_power))
    sampler = WeightedRandomSampler(
        weights=sample_weights.tolist(),
        num_samples=len(sample_weights),
        replacement=True,
    )

    loader_kwargs = {
        "num_workers": int(num_workers),
        "collate_fn": collate_fn_filter_corrupted,
        "pin_memory": bool(pin_memory),
        "persistent_workers": int(num_workers) > 0,
    }
    eval_batch_size = max(1, int(batch_size) // 2)

    train_loader = DataLoader(train_dataset, batch_size=int(batch_size), sampler=sampler, **loader_kwargs)
    val_loader = DataLoader(val_dataset, batch_size=eval_batch_size, shuffle=False, **loader_kwargs)
    test_loader = DataLoader(test_dataset, batch_size=eval_batch_size, shuffle=False, **loader_kwargs)
    return train_loader, val_loader, test_loader

def load_and_split_data(additional_sources=None):
    """Loads data from configured sources, maps to target classes, caps per class, and performs stratified split."""
    print("Loading and splitting data...")
    np.random.seed(42)

    target_to_source_files: defaultdict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for source_dir in DATA_SOURCE_DIRS:
        if not os.path.isdir(source_dir):
            print(f"Source directory not found, skipping: {source_dir}")
            continue

        for split in ["train", "test"]:
            split_dir = os.path.join(source_dir, split)
            if not os.path.isdir(split_dir):
                continue

            for source_class in os.listdir(split_dir):
                class_dir = os.path.join(split_dir, source_class)
                if not os.path.isdir(class_dir):
                    continue

                target_class = TEXTILENET_TO_TARGET.get(source_class.lower())
                if target_class not in MATERIAL_CLASSES:
                    continue

                source_key = source_class.lower()

                for filename in os.listdir(class_dir):
                    if filename.lower().endswith(IMAGE_EXTENSIONS):
                        target_to_source_files[target_class][source_key].append(os.path.join(class_dir, filename))

    if isinstance(additional_sources, dict) and additional_sources:
        merged_count = 0
        for target_class, source_map in additional_sources.items():
            if target_class not in MATERIAL_CLASSES or not isinstance(source_map, dict):
                continue
            for source_name, paths in source_map.items():
                if not isinstance(paths, list):
                    continue
                cleaned = [p for p in paths if isinstance(p, str)]
                if cleaned:
                    target_to_source_files[target_class][str(source_name)].extend(cleaned)
                    merged_count += len(cleaned)
        print(f"Merged {merged_count} additional image path(s) from curated manifests.")

    all_files = []
    all_labels = []
    selected_counts = {}
    filtered_corrupt_count = 0

    for class_index, class_name in enumerate(MATERIAL_CLASSES):
        source_to_files = target_to_source_files.get(class_name, {})
        max_images_per_class = int(HYPERPARAMS["MAX_IMAGES_PER_CLASS"])
        available_count = sum(len(v) for v in source_to_files.values())
        candidate_target = min(available_count, max_images_per_class * 4)

        selected_candidates = prioritized_sample_from_sources(
            class_name,
            source_to_files,
            candidate_target,
        )
        if selected_candidates:
            class_rng = np.random.default_rng(zlib.crc32(class_name.encode("utf-8")) & 0xFFFFFFFF)
            class_rng.shuffle(selected_candidates)
        selected = []
        seen = set()
        for image_path in selected_candidates:
            normalized_path = os.path.normpath(image_path)
            if normalized_path in seen:
                continue
            seen.add(normalized_path)

            if is_image_decodable(normalized_path):
                selected.append(normalized_path)
                if len(selected) >= max_images_per_class:
                    break
            else:
                filtered_corrupt_count += 1

        selected_counts[class_name] = len(selected)
        all_files.extend(selected)
        all_labels.extend([class_index] * len(selected))

    print("Selected image counts per target class (after cap):")
    for class_name in MATERIAL_CLASSES:
        print(f"  {class_name}: {selected_counts[class_name]}")

    if filtered_corrupt_count > 0:
        print(f"Filtered out {filtered_corrupt_count} corrupted image(s) during dataset selection.")

    low_count_classes = [
        class_name for class_name, count in selected_counts.items() if count < MIN_VALID_IMAGES_PER_CLASS
    ]
    if low_count_classes:
        low_count_str = ", ".join(low_count_classes)
        raise RuntimeError(
            "Not enough valid images for minimum viable training in classes: "
            f"{low_count_str}. Each class needs at least {MIN_VALID_IMAGES_PER_CLASS} valid images."
        )

    if not all_files:
        raise RuntimeError("No data found after mapping and filtering. Check dataset sources and class mappings.")

    # Stratified split: 70% train, 15% val, 15% test
    train_files, test_val_files, train_labels, test_val_labels = train_test_split(
        all_files, all_labels, test_size=0.3, stratify=all_labels, random_state=42)
    val_files, test_files, val_labels, test_labels = train_test_split(
        test_val_files, test_val_labels, test_size=0.5, stratify=test_val_labels, random_state=42)
        
    if HYPERPARAMS.get("USE_IMATERIALIST_DATA", False):
        imat_dir = IMATERIALIST_DIR
        if os.path.isdir(imat_dir):
            for split, split_files, split_labels in [("train", train_files, train_labels), 
                                                     ("val", val_files, val_labels), 
                                                     ("test", test_files, test_labels)]:
                split_path = os.path.join(imat_dir, split)
                if os.path.isdir(split_path):
                    for class_idx, class_name in enumerate(MATERIAL_CLASSES):
                        class_dir = os.path.join(split_path, class_name)
                        if os.path.isdir(class_dir):
                            for filename in os.listdir(class_dir):
                                if filename.lower().endswith(IMAGE_EXTENSIONS):
                                    split_files.append(os.path.join(class_dir, filename))
                                    split_labels.append(class_idx)
            print("Appended iMaterialist deterministic splits to dataset.")
            
    print(f"Dataset split: {len(train_files)} train, {len(val_files)} validation, {len(test_files)} test.")
    return (train_files, train_labels), (val_files, val_labels), (test_files, test_labels)


def find_last_checkpoint_from_log(training_log):
    for entry in reversed(training_log):
        checkpoint_path = entry.get("last_checkpoint_path")
        if isinstance(checkpoint_path, str) and checkpoint_path and os.path.exists(checkpoint_path):
            return checkpoint_path

    if os.path.exists(LAST_CHECKPOINT_PATH):
        return LAST_CHECKPOINT_PATH

    return None


def append_epoch_progress(payload):
    """Writes a line-delimited JSON record for per-epoch monitoring."""
    os.makedirs(os.path.dirname(EPOCH_PROGRESS_FILE), exist_ok=True)
    with open(EPOCH_PROGRESS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")

def benchmark_inference(model, device, img_size, n_patches=7, runs=50, warmup=10):
    """Benchmarks single-image inference latency (7 patches) and VRAM usage."""
    model.eval()

    if device != "cuda":
        return {
            "inference_time_ms": float("inf"),
            "vram_mb": 0.0,
        }

    orig_dtype = next(model.parameters()).dtype
    model = model.to(device).half().eval()
    dummy = torch.randn(n_patches, 3, img_size, img_size, device=device, dtype=torch.float16)

    with torch.inference_mode():
        for _ in range(warmup):
            _ = model(dummy)

        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()

        start_event = torch.cuda.Event(enable_timing=True)
        end_event = torch.cuda.Event(enable_timing=True)
        start_event.record(torch.cuda.current_stream())
        for _ in range(runs):
            logits = model(dummy)
            _ = logits.mean(0)
        end_event.record(torch.cuda.current_stream())
        torch.cuda.synchronize()
        elapsed_ms = start_event.elapsed_time(end_event) / runs

    peak_vram_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)
    if orig_dtype == torch.float32:
        model.float()
    return {
        "inference_time_ms": float(elapsed_ms),
        "vram_mb": float(peak_vram_mb),
    }

# --- Main Training Loop ---
def run_training_attempt(params, attempt_num, training_log):
    """Runs one training attempt with strict low-RAM constraints and resumable checkpoints."""
    start_time = time.time()
    print(f"\n--- Starting Training Attempt #{attempt_num} ---")

    device = params["DEVICE"] if torch.cuda.is_available() else "cpu"
    params = {**params, "DEVICE": device}
    params["BATCH_SIZE"] = 4
    
    # Dynamically scale workers based on available CPU cores (leaving 2 for the OS/Background tasks)
    available_cores = max(1, (os.cpu_count() or 4) - 2)
    dynamic_workers = min(8, available_cores) # Cap at 8 to prevent Windows IPC bottlenecks
    params["NUM_WORKERS"] = dynamic_workers
    params["PIN_MEMORY"] = params.get("PIN_MEMORY", True)
    params["GRAD_ACCUM_STEPS"] = max(2, int(params.get("GRAD_ACCUM_STEPS", 2)))
    params["RESOURCE_MANAGER_ENABLED"] = True
    params["RAM_HARD_LIMIT_PERCENT"] = 77.0
    params["USE_MICROSCOPE_DATA"] = bool(params.get("USE_MICROSCOPE_DATA", True))
    params["USE_IBUG_RESEARCH_DATA"] = bool(params.get("USE_IBUG_RESEARCH_DATA", False))

    print("Hyperparameters:")
    print(json.dumps(params, indent=4))

    if device == "cuda":
        torch.backends.cudnn.benchmark = True

    resource_manager = get_resource_manager(auto_start=True)
    resource_manager.set_training_active(True, reason=f"attempt_{attempt_num}_start")

    try:
        additional_sources = load_additional_data_sources(
            use_microscope=params.get("USE_MICROSCOPE_DATA", True),
            use_ibug_research=params.get("USE_IBUG_RESEARCH_DATA", False),
        )
        (train_files, train_labels), (val_files, val_labels), (test_files, test_labels) = load_and_split_data(
            additional_sources=additional_sources,
        )

        train_transforms = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(float(params.get("AUG_ROTATION_DEG", 20))),
            transforms.ColorJitter(
                brightness=float(params.get("AUG_BRIGHTNESS", 0.3)),
                contrast=float(params.get("AUG_CONTRAST", 0.3)),
                saturation=float(params.get("AUG_SATURATION", 0.2)),
                hue=float(params.get("AUG_HUE", 0.05)),
            ),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        val_transforms = transforms.Compose([
            transforms.Resize((params["IMG_SIZE"], params["IMG_SIZE"])),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        train_dataset = FabricDataset(train_files, train_labels, train_transforms, params["N_PATCHES_TRAIN"], is_train=True)
        val_dataset = FabricDataset(val_files, val_labels, val_transforms, params["N_PATCHES_INFER"], is_train=False)
        test_dataset = FabricDataset(test_files, test_labels, val_transforms, params["N_PATCHES_INFER"], is_train=False)

        # Weight the loss toward underrepresented classes to improve minority recall.
        class_counts = np.bincount(train_labels, minlength=len(MATERIAL_CLASSES)).astype(np.float32)
        class_weights = class_counts.sum() / (len(MATERIAL_CLASSES) * np.maximum(class_counts, 1.0))
        class_weights_tensor = torch.tensor(class_weights, dtype=torch.float32, device=device)
        if not params.get("CLASS_WEIGHTED_LOSS", True):
            class_weights_tensor = None

        train_loader, val_loader, test_loader = build_dataloaders(
            train_dataset=train_dataset,
            val_dataset=val_dataset,
            test_dataset=test_dataset,
            train_labels=train_labels,
            device=device,
            batch_size=params["BATCH_SIZE"],
            num_workers=params["NUM_WORKERS"],
            pin_memory=params.get("PIN_MEMORY", device == "cuda"),
            sampler_power=params.get("SAMPLER_POWER", 0.0),
        )

        model = get_model(num_classes=len(MATERIAL_CLASSES)).to(device)
        if params.get("LOSS", "cross_entropy") == "logit_adjusted":
            # Adjust by the prior the sampler actually shows the model (no extra class weights).
            sampled_prior = effective_training_prior(
                class_counts, params.get("SAMPLER_POWER", 0.0), class_weighted_loss=False
            )
            criterion = LogitAdjustedLoss(
                sampled_prior,
                tau=params.get("LOGIT_ADJUST_TAU", 1.0),
                label_smoothing=params["LABEL_SMOOTHING"],
            ).to(device)
        else:
            criterion = nn.CrossEntropyLoss(
                weight=class_weights_tensor,
                label_smoothing=params["LABEL_SMOOTHING"],
            )
        scaler = GradScaler(enabled=device == "cuda")

        best_val_score = -1.0
        epochs_no_improve = 0
        history = []
        start_epoch = 0
        resume_payload = None
        warm_start_applied = False
        policy_stop_trigger = None

        resume_checkpoint_path = find_last_checkpoint_from_log(training_log)
        if resume_checkpoint_path and os.path.exists(resume_checkpoint_path):
            try:
                checkpoint_candidate = torch.load(
                    resume_checkpoint_path,
                    map_location=device,
                    weights_only=False,
                )
                if int(checkpoint_candidate.get("attempt", -1)) == int(attempt_num):
                    # If current params intentionally changed for the same attempt number,
                    # warm-start model weights but avoid stale optimizer/scheduler override.
                    if int(attempt_num) == 17:
                        ck_params = checkpoint_candidate.get("params") or {}
                        critical_keys = [
                            "LR_BACKBONE",
                            "LR_HEAD",
                            "LABEL_SMOOTHING",
                            "HEAD_ONLY_EPOCHS",
                            "EPOCHS_MAX",
                            "PATIENCE",
                            "GRAD_ACCUM_STEPS",
                            "AUG_ROTATION_DEG",
                            "AUG_BRIGHTNESS",
                            "AUG_CONTRAST",
                            "AUG_SATURATION",
                            "AUG_HUE",
                        ]
                        profile_mismatch = any(ck_params.get(k) != params.get(k) for k in critical_keys)
                        if profile_mismatch and checkpoint_candidate.get("model_state_dict") is not None:
                            model.load_state_dict(checkpoint_candidate["model_state_dict"], strict=False)
                            warm_start_applied = True
                            prior_best = checkpoint_candidate.get("best_val_score")
                            if prior_best is not None:
                                try:
                                    best_val_score = max(best_val_score, float(prior_best))
                                except (TypeError, ValueError):
                                    pass
                            print(
                                "Detected attempt-17 profile change; warm-starting weights and "
                                "skipping stale same-attempt optimizer resume."
                            )
                        else:
                            resume_payload = checkpoint_candidate
                            print(f"Resuming from checkpoint: {resume_checkpoint_path}")
                    else:
                        resume_payload = checkpoint_candidate
                        print(f"Resuming from checkpoint: {resume_checkpoint_path}")
                else:
                    if checkpoint_candidate.get("model_state_dict") is not None:
                        model.load_state_dict(checkpoint_candidate["model_state_dict"], strict=False)
                        warm_start_applied = True
                        print(
                            "Checkpoint attempt does not match current attempt number; "
                            f"warm-started model weights from {resume_checkpoint_path}. "
                            "Per-attempt best tracking has been reset."
                        )
                    else:
                        print(
                            "Checkpoint attempt does not match current attempt number and no model_state_dict was found; "
                            "starting fresh attempt state."
                        )
            except Exception as exc:
                print(f"Warning: Failed to load resume checkpoint ({exc}). Starting fresh attempt state.")
        else:
            print("No resumable checkpoint found for current attempt in training_log.json.")

        if resume_payload is None and not warm_start_applied and os.path.exists(BEST_WEIGHTS_PATH):
            try:
                best_candidate = torch.load(BEST_WEIGHTS_PATH, map_location=device, weights_only=False)
                state_dict = (
                    best_candidate.get("model_state_dict")
                    if isinstance(best_candidate, dict)
                    else best_candidate
                )
                if state_dict is not None:
                    model.load_state_dict(state_dict, strict=False)
                    warm_start_applied = True
                    print(f"Warm-started model from best weights: {BEST_WEIGHTS_PATH}")
            except Exception as exc:
                print(f"Warning: Failed to warm-start from best weights ({exc}). Continuing with fresh initialization.")

        def initialize_optimizer_and_scheduler(current_epoch):
            if current_epoch < params["HEAD_ONLY_EPOCHS"]:
                for param in model.features.parameters():
                    param.requires_grad = False
                optimizer_local = optim.AdamW(
                    model.classifier.parameters(),
                    lr=params["LR_HEAD"],
                    weight_decay=params["WEIGHT_DECAY"],
                )
                scheduler_local = None
            else:
                for param in model.features.parameters():
                    param.requires_grad = True
                optimizer_local = optim.AdamW([
                    {"params": model.features.parameters(), "lr": params["LR_BACKBONE"]},
                    {"params": model.classifier.parameters(), "lr": params["LR_HEAD"]},
                ], weight_decay=params["WEIGHT_DECAY"])

                scheduler_local = CosineAnnealingLR(
                    optimizer_local,
                    T_max=max(1, params["EPOCHS_MAX"] - params["HEAD_ONLY_EPOCHS"]),
                )

                warmup_steps = max(0, current_epoch - params["HEAD_ONLY_EPOCHS"])
                for _ in range(warmup_steps):
                    scheduler_local.step()

            return optimizer_local, scheduler_local

        optimizer, scheduler = initialize_optimizer_and_scheduler(0)

        if resume_payload is not None:
            model.load_state_dict(resume_payload["model_state_dict"])
            start_epoch = int(resume_payload.get("epoch", 0))
            best_val_score = float(resume_payload.get("best_val_score", -1.0))
            epochs_no_improve = int(resume_payload.get("epochs_no_improve", 0))
            history = list(resume_payload.get("history", []))

            if history:
                history_scores = []
                for item in history:
                    if isinstance(item, dict):
                        try:
                            history_scores.append(float(item.get("val_macro_f1", -1.0)))
                        except (TypeError, ValueError):
                            history_scores.append(-1.0)
                    else:
                        history_scores.append(-1.0)

                history_best = max(history_scores) if history_scores else -1.0
                if history_best > -1.0:
                    if abs(history_best - best_val_score) > 1e-9:
                        print(
                            "Resume checkpoint best_val_macro_f1 did not match epoch history; "
                            "using history-derived best for this attempt."
                        )
                    best_val_score = history_best

                    best_epoch_idx = 0
                    for idx, score in enumerate(history_scores):
                        if abs(score - history_best) <= 1e-9:
                            best_epoch_idx = idx
                    epochs_no_improve = max(0, (len(history) - 1) - best_epoch_idx)

            optimizer, scheduler = initialize_optimizer_and_scheduler(start_epoch)

            if resume_payload.get("optimizer_state_dict") is not None:
                try:
                    optimizer.load_state_dict(resume_payload["optimizer_state_dict"])
                except ValueError as exc:
                    print(
                        "Warning: Could not load optimizer state from checkpoint "
                        f"(state is incompatible with current parameter groups): {exc}. "
                        "Continuing with freshly initialized optimizer state."
                    )

            if scheduler is not None and resume_payload.get("scheduler_state_dict") is not None:
                try:
                    scheduler.load_state_dict(resume_payload["scheduler_state_dict"])
                except Exception as exc:
                    print(
                        "Warning: Could not load scheduler state from checkpoint "
                        f"(state is incompatible): {exc}. Continuing with fresh scheduler state."
                    )

            if resume_payload.get("scaler_state_dict") is not None:
                try:
                    scaler.load_state_dict(resume_payload["scaler_state_dict"])
                except Exception as exc:
                    print(
                        "Warning: Could not load AMP scaler state from checkpoint "
                        f"(state is incompatible): {exc}. Continuing with fresh scaler state."
                    )

            print(
                f"Resume state: epoch={start_epoch}, best_val_macro_f1={best_val_score:.4f}, "
                f"epochs_no_improve={epochs_no_improve}"
            )

        for epoch in range(start_epoch, params["EPOCHS_MAX"]):
            resource_manager.set_downloads_paused(True, reason=f"attempt_{attempt_num}_epoch_{epoch+1}_start")
            closed_downloads = resource_manager.close_download_processes()
            if closed_downloads > 0:
                print(f"Closed {closed_downloads} download process(es) before training epoch start.")
            resource_manager.wait_for_no_download_processes(timeout_s=10.0, poll_s=1.0)
            ram_gate_ok = resource_manager.wait_until_ram_below_limit(
                limit_percent=params["RAM_HARD_LIMIT_PERCENT"],
                poll_s=2.0,
                timeout_s=10.0,
            )
            if not ram_gate_ok:
                print(
                    f"Warning: RAM did not fall below {params['RAM_HARD_LIMIT_PERCENT']:.1f}% within timeout; "
                    "continuing in constrained mode with downloads paused."
                )

            print(f"\n--- Epoch {epoch+1}/{params['EPOCHS_MAX']} ---")

            current_lrs = [float(pg.get("lr", 0.0)) for pg in optimizer.param_groups]

            append_epoch_progress({
                "timestamp": time.time(),
                "attempt": attempt_num,
                "epoch": epoch + 1,
                "epoch_start": True,
                "start_epoch": start_epoch,
                "best_val_macro_f1": float(best_val_score),
                "optimizer_lrs": current_lrs,
            })

            if epoch == 0 and start_epoch == 0:
                print("Phase 1: Training classifier head only.")

            if epoch == params["HEAD_ONLY_EPOCHS"] and start_epoch <= params["HEAD_ONLY_EPOCHS"]:
                print("Phase 2: Unfreezing backbone with differential learning rates.")
                optimizer, scheduler = initialize_optimizer_and_scheduler(epoch)

            model.train()
            if params.get("FREEZE_BN", False):
                freeze_batchnorm(model)
            running_loss = 0.0
            seen_samples = 0
            skipped_nan_steps = 0
            oom_skipped_steps = 0
            heartbeat_steps = max(1, int(params.get("BATCH_HEARTBEAT_STEPS", 100)))

            optimizer.zero_grad(set_to_none=True)

            for step_idx, (inputs, labels) in enumerate(tqdm(train_loader, desc="Training"), start=1):
                if not inputs.numel():
                    continue

                try:
                    inputs, labels = inputs.to(device), labels.to(device).long()

                    with autocast(dtype=torch.float16, enabled=device == "cuda"):
                        raw_loss = criterion(model(inputs), labels)

                    if not torch.isfinite(raw_loss):
                        skipped_nan_steps += 1
                        optimizer.zero_grad(set_to_none=True)
                        continue

                    loss = raw_loss / max(1, int(params.get("GRAD_ACCUM_STEPS", 1)))
                    scaler.scale(loss).backward()

                    should_step = (
                        step_idx % max(1, int(params.get("GRAD_ACCUM_STEPS", 1))) == 0
                        or step_idx == len(train_loader)
                    )
                    if should_step:
                        scaler.unscale_(optimizer)
                        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                        scaler.step(optimizer)
                        scaler.update()
                        optimizer.zero_grad(set_to_none=True)

                    running_loss += raw_loss.item() * labels.size(0)
                    seen_samples += labels.size(0)
                except torch.cuda.OutOfMemoryError:
                    oom_skipped_steps += 1
                    optimizer.zero_grad(set_to_none=True)
                    if device == "cuda":
                        torch.cuda.empty_cache()
                    continue

                if step_idx % heartbeat_steps == 0:
                    append_epoch_progress({
                        "timestamp": time.time(),
                        "attempt": attempt_num,
                        "epoch": epoch + 1,
                        "step": step_idx,
                        "step_heartbeat": True,
                        "train_loss_running": float(running_loss / max(1, seen_samples)),
                        "seen_samples": int(seen_samples),
                        "skipped_nan_steps": int(skipped_nan_steps),
                        "oom_skipped_steps": int(oom_skipped_steps),
                    })

            if scheduler is not None and epoch >= params["HEAD_ONLY_EPOCHS"]:
                scheduler.step()

            train_loss = running_loss / max(1, seen_samples)

            model = model.float()
            model.eval()
            val_metrics = evaluate_model(model, val_loader, device, MATERIAL_CLASSES, criterion=criterion)
            val_loss = val_metrics["loss"]
            val_top1_acc = val_metrics["top1_accuracy"]
            val_macro_f1 = val_metrics["macro_f1"]

            if skipped_nan_steps > 0:
                print(f"Skipped {skipped_nan_steps} non-finite training steps this epoch.")
            if oom_skipped_steps > 0:
                print(f"Skipped {oom_skipped_steps} OOM training steps this epoch.")

            print(
                f"Train Loss: {train_loss:.4f}, "
                f"Validation Loss: {val_loss:.4f}, "
                f"Top-1 Accuracy: {val_top1_acc:.4f}, "
                f"Macro-F1: {val_macro_f1:.4f}"
            )

            history.append({
                "epoch": epoch + 1,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_top1_accuracy": val_top1_acc,
                "val_top3_accuracy": val_metrics["top3_accuracy"],
                "val_macro_f1": val_macro_f1,
                "val_worst_class_recall": val_metrics["worst_class_recall"],
            })

            append_epoch_progress({
                "timestamp": time.time(),
                "attempt": attempt_num,
                "epoch": epoch + 1,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_top1_accuracy": val_top1_acc,
                "val_top3_accuracy": val_metrics["top3_accuracy"],
                "val_macro_f1": val_macro_f1,
                "val_worst_class_recall": val_metrics["worst_class_recall"],
            })

            # Governance stop: enforce mandatory quality checks before continuing training.
            stop_after_checkpoint = False
            if epoch + 1 >= max(20, params["HEAD_ONLY_EPOCHS"] + 12) and float(val_metrics["worst_class_recall"]) < 0.20:
                policy_stop_trigger = {
                    "rule": "worst_recall_below_0_20_after_min_epoch",
                    "epoch": epoch + 1,
                    "value": float(val_metrics["worst_class_recall"]),
                    "threshold": 0.20,
                }
                stop_after_checkpoint = True

            if not stop_after_checkpoint:
                policy_window = int(params.get("POLICY_STOP_WINDOW", 10))
                policy_min_epoch = int(params.get("POLICY_STOP_MIN_EPOCHS", 20))
                policy_min_top1_gain = float(params.get("POLICY_MIN_TOP1_GAIN", 0.005))
                policy_min_macro_f1_gain = float(params.get("POLICY_MIN_MACRO_F1_GAIN", 0.005))

                if len(history) >= policy_window * 2 and (epoch + 1) >= policy_min_epoch:
                    prior_window = history[:-policy_window]
                    recent_window = history[-policy_window:]

                    best_prior_top1 = max(float(item["val_top1_accuracy"]) for item in prior_window)
                    best_recent_top1 = max(float(item["val_top1_accuracy"]) for item in recent_window)
                    top1_window_gain = best_recent_top1 - best_prior_top1

                    best_prior_macro_f1 = max(float(item["val_macro_f1"]) for item in prior_window)
                    best_recent_macro_f1 = max(float(item["val_macro_f1"]) for item in recent_window)
                    macro_f1_window_gain = best_recent_macro_f1 - best_prior_macro_f1

                    if top1_window_gain < policy_min_top1_gain and macro_f1_window_gain < policy_min_macro_f1_gain:
                        policy_stop_trigger = {
                            "rule": "val_metrics_plateau_window",
                            "start_epoch": int(recent_window[0]["epoch"]),
                            "end_epoch": int(recent_window[-1]["epoch"]),
                            "top1_window_gain": float(top1_window_gain),
                            "macro_f1_window_gain": float(macro_f1_window_gain),
                            "top1_threshold": float(policy_min_top1_gain),
                            "macro_f1_threshold": float(policy_min_macro_f1_gain),
                            "window": int(policy_window),
                        }
                        stop_after_checkpoint = True

            if stop_after_checkpoint and policy_stop_trigger is None:
                policy_stop_trigger = {
                    "rule": "policy_stop_unspecified",
                    "start_epoch": int(history[max(0, len(history) - 5)]["epoch"]),
                    "end_epoch": int(history[-1]["epoch"]),
                    "improvement": 0.0,
                    "threshold": 0.0,
                }

            if stop_after_checkpoint:
                append_epoch_progress({
                    "timestamp": time.time(),
                    "attempt": attempt_num,
                    "epoch": epoch + 1,
                    "policy_stop_trigger": policy_stop_trigger,
                })
                append_issue(
                    category="policy_breach",
                    severity="high",
                    title=f"Attempt {attempt_num} policy stop triggered",
                    details=json.dumps(policy_stop_trigger),
                    action_taken="Training loop set to stop after checkpoint save for diagnostics.",
                    status="open",
                )

            improved = val_macro_f1 > best_val_score
            if improved:
                best_val_score = val_macro_f1
                torch.save({
                    "attempt": int(attempt_num),
                    "best_val_score": float(best_val_score),
                    "model_state_dict": model.state_dict(),
                    "class_map": {i: i for i in range(len(MATERIAL_CLASSES))},
                    "present_class_names": MATERIAL_CLASSES,
                    "patch_config": {
                        "patch_fraction": HYPERPARAMS.get("PATCH_FRACTION"),
                        "min_coverage": HYPERPARAMS.get("PATCH_MIN_COVERAGE", 0.5),
                    },
                }, BEST_WEIGHTS_PATH)
                print(f"New best model saved with Validation Macro-F1: {best_val_score:.4f}")
                epochs_no_improve = 0
            else:
                epochs_no_improve += 1

            checkpoint_payload = {
                "attempt": attempt_num,
                "epoch": epoch + 1,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "scheduler_state_dict": scheduler.state_dict() if scheduler is not None else None,
                "scaler_state_dict": scaler.state_dict(),
                "best_val_score": best_val_score,
                "epochs_no_improve": epochs_no_improve,
                "history": history,
                "params": params,
            }
            torch.save(checkpoint_payload, LAST_CHECKPOINT_PATH)
            print(f"Checkpoint saved: {LAST_CHECKPOINT_PATH} (epoch {epoch+1})")

            append_epoch_progress({
                "timestamp": time.time(),
                "attempt": attempt_num,
                "epoch": epoch + 1,
                "checkpoint_saved": True,
                "checkpoint_path": LAST_CHECKPOINT_PATH,
                "best_model_path": BEST_WEIGHTS_PATH if os.path.exists(BEST_WEIGHTS_PATH) else None,
                "best_val_macro_f1": best_val_score,
                "epochs_no_improve": epochs_no_improve,
            })

            resource_manager.set_downloads_paused(False, reason=f"attempt_{attempt_num}_epoch_{epoch+1}_checkpoint_saved")

            if stop_after_checkpoint:
                print(f"Policy stop triggered: {policy_stop_trigger}")
                break

            if epochs_no_improve >= params["PATIENCE"]:
                print(f"Early stopping triggered after {params['PATIENCE']} epochs with no improvement.")
                break

        print("\nTraining finished. Loading best available model for final evaluation.")
        best_loaded_for_current_attempt = False
        if os.path.exists(BEST_WEIGHTS_PATH):
            best_checkpoint = torch.load(BEST_WEIGHTS_PATH, map_location=device, weights_only=False)
            best_state_dict = (
                best_checkpoint.get("model_state_dict")
                if isinstance(best_checkpoint, dict)
                else best_checkpoint
            )
            best_attempt = (
                int(best_checkpoint.get("attempt", -1))
                if isinstance(best_checkpoint, dict)
                else -1
            )
            if best_state_dict is not None and best_attempt == int(attempt_num):
                model.load_state_dict(best_state_dict)
                best_loaded_for_current_attempt = True
            else:
                print(
                    "Best checkpoint belongs to a different attempt or is legacy format; "
                    "using last checkpoint for this attempt's final evaluation."
                )

        if not best_loaded_for_current_attempt and os.path.exists(LAST_CHECKPOINT_PATH):
            last_checkpoint = torch.load(LAST_CHECKPOINT_PATH, map_location=device, weights_only=False)
            model.load_state_dict(last_checkpoint["model_state_dict"])
        elif not best_loaded_for_current_attempt:
            print("Warning: No best or last checkpoint file found; evaluating current in-memory model state.")

        model = model.float()

        test_metrics = evaluate_model(model, test_loader, device, MATERIAL_CLASSES, criterion=criterion)
        inference_metrics = benchmark_inference(
            model=model,
            device=device,
            img_size=params["IMG_SIZE"],
            n_patches=params["N_PATCHES_INFER"],
        )

        print("\n--- Test Set Results ---")
        print(json.dumps(test_metrics, indent=4))
        print("\n--- Inference Benchmark ---")
        print(json.dumps(inference_metrics, indent=4))

        metrics_targets_met = all([
            test_metrics.get("top1_accuracy", 0) >= 0.72,
            test_metrics.get("top3_accuracy", 0) >= 0.90,
            test_metrics.get("macro_f1", 0) >= 0.68,
            test_metrics.get("worst_class_recall", 0) >= 0.40,
            inference_metrics.get("inference_time_ms", float("inf")) <= 40.0,
            inference_metrics.get("vram_mb", float("inf")) <= 300.0,
        ])

        research_only_data_used = bool(params.get("USE_IBUG_RESEARCH_DATA", False))
        targets_met = bool(metrics_targets_met and not research_only_data_used)

        if metrics_targets_met and research_only_data_used:
            print(
                "\nAll numeric targets were met, but this run used research-only iBUG data. "
                "Cannot finalize production deliverable from this attempt."
            )
        elif targets_met:
            print("\nAll performance targets MET! Calibrating and finalizing.")
            calibrate_temperature(model, val_loader, device)
        else:
            print("\nPerformance targets NOT MET.")

        if targets_met:
            reason_for_retry = "N/A"
        elif metrics_targets_met and research_only_data_used:
            reason_for_retry = "Targets met with research-only iBUG data; rerun required with commercial-safe datasets only."
        else:
            reason_for_retry = (
                f"Policy stop trigger: {policy_stop_trigger}" if policy_stop_trigger else "Initial run failed to meet targets."
            )

        log_entry = {
            "attempt": attempt_num,
            "status": "completed_policy_stop" if policy_stop_trigger else "completed",
            "targets_met": targets_met,
            "reason_for_retry": reason_for_retry,
            "hyperparameters_used": params,
            "final_metrics_achieved": test_metrics,
            "inference_metrics": inference_metrics,
            "training_duration_seconds": time.time() - start_time,
            "epoch_history": history,
            "last_checkpoint_path": LAST_CHECKPOINT_PATH if os.path.exists(LAST_CHECKPOINT_PATH) else None,
            "research_only_data_used": research_only_data_used,
            "met_targets_without_license_constraint": bool(metrics_targets_met),
        }
        if policy_stop_trigger:
            log_entry["policy_stop_trigger"] = policy_stop_trigger
        return log_entry, targets_met
    finally:
        resource_manager.set_downloads_paused(False, reason=f"attempt_{attempt_num}_finished")
        resource_manager.set_training_active(False, reason=f"attempt_{attempt_num}_finished")

def main():
    """Main function to orchestrate training attempts."""
    read_issues_log()

    other_pids = [] # find_other_training_pids()
    if other_pids:
        print(
            f"Detected existing training process(es): {other_pids}. "
            "Refusing to launch a second train.py instance."
        )
        append_issue(
            category="process_control",
            severity="high",
            title="Launch blocked due to active train.py PID(s)",
            details=f"Found running training PID(s): {other_pids}",
            action_taken="Current launch aborted to enforce single-writer checkpoint policy.",
            status="resolved",
        )
        return

    if not acquire_singleton_lock():
        return

    atexit.register(release_singleton_lock)

    # Load existing log or create new one
    try:
        try:
            with open(LOG_FILE, 'r') as f:
                training_log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            training_log = []

        ensure_experiment_log_file()

        current_params = HYPERPARAMS.copy()
        current_params["BATCH_SIZE"] = 4
        current_params["NUM_WORKERS"] = 0
        current_params["PIN_MEMORY"] = False
        current_params["GRAD_ACCUM_STEPS"] = max(2, int(current_params.get("GRAD_ACCUM_STEPS", 2)))
        attempt_num = len(training_log) + 1
        
        while True:
            read_issues_log()
            recent_notes = read_experiment_log_tail(max_lines=140)
            if recent_notes.strip():
                print("Loaded recent experiment log context before starting this attempt.")

            if attempt_num == 5 and not attempt5_weak_class_data_gate(min_valid_images=800):
                print("Attempt 5 pre-launch gate failed. Exiting without starting a new attempt.")
                return

            if attempt_num == 17:
                print("Attempt 17 pre-launch gate: targeted valid-count top-up for Corduroy/Suede/Wool.")
                gate_ok, gate_counts = ensure_attempt17_target_data(ATTEMPT17_MIN_VALID_COUNTS, max_rounds=3)
                apply_attempt17_stabilization_profile(current_params)
                current_params["USE_MICROSCOPE_DATA"] = True
                current_params["USE_IBUG_RESEARCH_DATA"] = True
                if gate_ok:
                    print(f"Attempt 17 data gate passed with counts: {gate_counts}")
                else:
                    print(
                        "Warning: Attempt 17 data gate did not reach all thresholds after targeted downloads. "
                        f"Proceeding with best available counts: {gate_counts}"
                    )
                append_issue(
                    category="stabilization",
                    severity="medium",
                    title="Attempt 17 stabilization profile applied",
                    details=json.dumps({
                        "LR_BACKBONE": current_params["LR_BACKBONE"],
                        "LR_HEAD": current_params["LR_HEAD"],
                        "LABEL_SMOOTHING": current_params["LABEL_SMOOTHING"],
                        "HEAD_ONLY_EPOCHS": current_params["HEAD_ONLY_EPOCHS"],
                        "EPOCHS_MAX": current_params["EPOCHS_MAX"],
                        "PATIENCE": current_params["PATIENCE"],
                        "GRAD_ACCUM_STEPS": current_params["GRAD_ACCUM_STEPS"],
                        "USE_MICROSCOPE_DATA": current_params["USE_MICROSCOPE_DATA"],
                        "USE_IBUG_RESEARCH_DATA": current_params["USE_IBUG_RESEARCH_DATA"],
                    }),
                    action_taken="Applied lower-LR, higher-accumulation, and softer-augmentation settings for attempt 17 with curated microscope+iBUG experimental data enabled.",
                    status="resolved",
                )

            current_params["BATCH_SIZE"] = 4
            current_params["NUM_WORKERS"] = 0
            current_params["PIN_MEMORY"] = False
            current_params["GRAD_ACCUM_STEPS"] = max(2, int(current_params.get("GRAD_ACCUM_STEPS", 2)))
            current_params["USE_MICROSCOPE_DATA"] = bool(current_params.get("USE_MICROSCOPE_DATA", True))
            current_params["USE_IBUG_RESEARCH_DATA"] = bool(current_params.get("USE_IBUG_RESEARCH_DATA", False))

            try:
                log_entry, targets_met = run_training_attempt(current_params, attempt_num, training_log)
            except KeyboardInterrupt:
                print("\nTraining interrupted by user. Exiting cleanly while preserving checkpoints/logs.")
                append_issue(
                    category="process_control",
                    severity="medium",
                    title=f"Attempt {attempt_num} interrupted by user",
                    details="KeyboardInterrupt received during training attempt.",
                    action_taken="Stopped current launch cleanly; checkpoint/log artifacts retained.",
                    status="open",
                )
                return
            except Exception as exc:
                trace_text = traceback.format_exc()
                print(f"\nAttempt {attempt_num} failed with unhandled exception: {exc}")
                append_issue(
                    category="training_runtime",
                    severity="high",
                    title=f"Attempt {attempt_num} failed with exception",
                    details=trace_text[-12000:],
                    action_taken="Failure captured; attempt logged for retry progression.",
                    status="open",
                )
                log_entry = {
                    "attempt": attempt_num,
                    "status": "failed_exception",
                    "targets_met": False,
                    "reason_for_retry": f"Unhandled exception: {type(exc).__name__}: {exc}",
                    "hyperparameters_used": current_params.copy(),
                    "final_metrics_achieved": {},
                    "inference_metrics": {},
                    "training_duration_seconds": 0,
                    "epoch_history": [],
                    "last_checkpoint_path": LAST_CHECKPOINT_PATH if os.path.exists(LAST_CHECKPOINT_PATH) else None,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                }
                targets_met = False

            training_log.append(log_entry)
            
            # Save log after each attempt
            with open(LOG_FILE, 'w') as f:
                json.dump(training_log, f, indent=4)

            append_experiment_postmortem(
                attempt_num=attempt_num,
                params=current_params.copy(),
                log_entry=log_entry,
                was_success=targets_met,
            )
                
            if targets_met:
                print("\nSUCCESS: Model trained and all targets achieved.")
                break
            
            # --- Auto-Retry Logic ---
            print("\nApplying auto-retry logic...")
            attempt_num += 1
            metrics = log_entry["final_metrics_achieved"]
            policy_rule = (log_entry.get("policy_stop_trigger") or {}).get("rule")

            if bool(log_entry.get("research_only_data_used", False)) and bool(log_entry.get("met_targets_without_license_constraint", False)):
                print("Research-only run met numeric targets. Switching next attempt to commercial-safe data only.")
                current_params["USE_IBUG_RESEARCH_DATA"] = False
                current_params["USE_MICROSCOPE_DATA"] = True
                current_params["EPOCHS_MAX"] = max(int(current_params.get("EPOCHS_MAX", 60)), 90)
                current_params["PATIENCE"] = max(int(current_params.get("PATIENCE", 10)), 18)
                current_params["HEAD_ONLY_EPOCHS"] = max(int(current_params.get("HEAD_ONLY_EPOCHS", 3)), 4)
                continue

            if attempt_num == 17:
                print("Applying attempt 17 stabilization profile from full-run diagnostics.")
                apply_attempt17_stabilization_profile(current_params)
                append_issue(
                    category="stabilization",
                    severity="medium",
                    title="Attempt 17 stabilization profile applied",
                    details=json.dumps({
                        "LR_BACKBONE": current_params["LR_BACKBONE"],
                        "LR_HEAD": current_params["LR_HEAD"],
                        "LABEL_SMOOTHING": current_params["LABEL_SMOOTHING"],
                        "HEAD_ONLY_EPOCHS": current_params["HEAD_ONLY_EPOCHS"],
                        "EPOCHS_MAX": current_params["EPOCHS_MAX"],
                        "PATIENCE": current_params["PATIENCE"],
                        "GRAD_ACCUM_STEPS": current_params["GRAD_ACCUM_STEPS"],
                    }),
                    action_taken="Applied lower-LR, higher-accumulation, and softer-augmentation settings for attempt 17.",
                    status="resolved",
                )
            elif policy_rule == "val_metrics_plateau_window":
                print("Adjusting: Plateau detected. Lowering LRs, extending warmup, and training longer.")
                current_params["LR_BACKBONE"] = max(current_params["LR_BACKBONE"] * 0.7, 2e-5)
                current_params["LR_HEAD"] = max(current_params["LR_HEAD"] * 0.75, 5e-4)
                current_params["HEAD_ONLY_EPOCHS"] = min(current_params.get("HEAD_ONLY_EPOCHS", 3) + 1, 6)
                current_params["EPOCHS_MAX"] = min(current_params["EPOCHS_MAX"] + 20, 200)
                current_params["PATIENCE"] = min(current_params["PATIENCE"] + 4, 30)
            elif metrics.get("top1_accuracy", 0) < 0.60:
                print("Adjusting: Top-1 is low. Slightly reducing LRs and extending training horizon.")
                current_params["LR_BACKBONE"] = max(current_params["LR_BACKBONE"] * 0.85, 2e-5)
                current_params["LR_HEAD"] = max(current_params["LR_HEAD"] * 0.9, 5e-4)
                current_params["EPOCHS_MAX"] = min(current_params["EPOCHS_MAX"] + 15, 200)
                current_params["PATIENCE"] = min(current_params["PATIENCE"] + 3, 30)
            elif metrics.get("worst_class_recall", 1.0) < 0.40:
                print("Adjusting: Worst class recall is low. Increasing patience and reducing label smoothing.")
                current_params["PATIENCE"] = min(current_params["PATIENCE"] + 8, 35)
                current_params["LABEL_SMOOTHING"] = max(0.0, current_params.get("LABEL_SMOOTHING", 0.05) - 0.02)
            else:
                print("Adjusting: General performance improvement needed. Increasing epochs and patience.")
                current_params["EPOCHS_MAX"] = min(current_params["EPOCHS_MAX"] + 20, 200)
                current_params["PATIENCE"] = min(current_params["PATIENCE"] + 3, 30)

            current_params["BATCH_SIZE"] = 4
            current_params["NUM_WORKERS"] = 0
            current_params["PIN_MEMORY"] = False
            current_params["GRAD_ACCUM_STEPS"] = max(2, int(current_params.get("GRAD_ACCUM_STEPS", 2)))
    finally:
        release_singleton_lock()

if __name__ == '__main__':
    main()
