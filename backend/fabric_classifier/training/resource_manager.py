import json
import os
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import psutil
import torch


LOG_PATH = Path("backend/fabric_classifier/training/resource_manager.log")
CONTROL_DIR = Path("backend/fabric_classifier/training/runtime_control")
DOWNLOAD_FORCE_PAUSE_FILE = CONTROL_DIR / "downloads_paused.flag"
TRAINING_ACTIVE_FILE = CONTROL_DIR / "training_active.flag"

RAM_HARD_LIMIT_PERCENT = 85.0
RAM_DOWNLOAD_PAUSE_PERCENT = 90.0
MAX_DOWNLOAD_WORKERS = 4

TRAINING_PROCESS_TOKENS = [
    " -m backend.fabric_classifier.training.train",
    "backend/fabric_classifier/training/train.py",
    "backend\\fabric_classifier\\training\\train.py",
]

IGNORE_TRAINING_ACTIVE_ENV = "FABRIC_RESOURCE_IGNORE_TRAINING_ACTIVE"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ResourceSnapshot:
    timestamp: str
    cpu_percent: float
    ram_percent: float
    vram_free_mb: float
    network_mbps: float
    total_cpu_cores: int
    free_cpu_cores: int
    download_workers: int
    dataloader_workers: int
    batch_size: int
    download_paused: bool
    training_ram_critical: bool
    forced_download_pause: bool


class DynamicResourceManager:
    def __init__(
        self,
        scan_interval_s: int = 30,
        max_download_workers: int = MAX_DOWNLOAD_WORKERS,
        max_dataloader_workers: int = 6,
        min_batch_size: int = 8,
        max_batch_size: int = 32,
        log_path: Path = LOG_PATH,
    ):
        self.scan_interval_s = int(scan_interval_s)
        self.max_download_workers = int(max_download_workers)
        self.max_dataloader_workers = int(max_dataloader_workers)
        self.min_batch_size = int(min_batch_size)
        self.max_batch_size = int(max_batch_size)
        self.log_path = Path(log_path)
        self.control_dir = CONTROL_DIR
        self.control_dir.mkdir(parents=True, exist_ok=True)

        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

        self._net_prev_bytes: int | None = None
        self._net_prev_time: float | None = None

        self._snapshot = ResourceSnapshot(
            timestamp=utc_now_iso(),
            cpu_percent=0.0,
            ram_percent=0.0,
            vram_free_mb=0.0,
            network_mbps=0.0,
            total_cpu_cores=max(1, psutil.cpu_count(logical=True) or 1),
            free_cpu_cores=0,
            download_workers=MAX_DOWNLOAD_WORKERS,
            dataloader_workers=0,
            batch_size=8,
            download_paused=False,
            training_ram_critical=False,
            forced_download_pause=False,
        )

    def start(self) -> None:
        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                return
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True, name="fabric-resource-manager")
            self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=2.0)

    def get_snapshot(self) -> ResourceSnapshot:
        with self._lock:
            return self._snapshot

    def get_download_workers(self) -> int:
        return int(self.get_snapshot().download_workers)

    def get_dataloader_workers(self) -> int:
        return int(self.get_snapshot().dataloader_workers)

    def get_batch_size(self) -> int:
        return int(self.get_snapshot().batch_size)

    def is_download_paused(self) -> bool:
        return bool(self.get_snapshot().download_paused)

    def is_training_ram_critical(self) -> bool:
        return bool(self.get_snapshot().training_ram_critical)

    def clamp_download_workers(self, requested_workers: int) -> int:
        return max(1, min(int(requested_workers), MAX_DOWNLOAD_WORKERS))

    def set_downloads_paused(self, paused: bool, reason: str = "manual") -> None:
        if paused:
            payload = {
                "timestamp": utc_now_iso(),
                "reason": reason,
            }
            self._write_json_atomic(DOWNLOAD_FORCE_PAUSE_FILE, payload)
        else:
            DOWNLOAD_FORCE_PAUSE_FILE.unlink(missing_ok=True)

    def is_downloads_force_paused(self) -> bool:
        return DOWNLOAD_FORCE_PAUSE_FILE.exists()

    def set_training_active(self, active: bool, reason: str = "training") -> None:
        if active:
            payload = {
                "timestamp": utc_now_iso(),
                "reason": reason,
                "pid": os.getpid(),
            }
            self._write_json_atomic(TRAINING_ACTIVE_FILE, payload)
        else:
            TRAINING_ACTIVE_FILE.unlink(missing_ok=True)

    def is_any_training_process_active(self) -> bool:
        if TRAINING_ACTIVE_FILE.exists():
            try:
                payload = json.loads(TRAINING_ACTIVE_FILE.read_text(encoding="utf-8"))
                pid = int(payload.get("pid", 0))
                if pid > 0 and self._pid_matches_tokens(pid, TRAINING_PROCESS_TOKENS):
                    return True
                # Stale flag from a dead process should not block orchestration decisions.
                TRAINING_ACTIVE_FILE.unlink(missing_ok=True)
            except Exception:
                TRAINING_ACTIVE_FILE.unlink(missing_ok=True)

        pids = self._find_processes(TRAINING_PROCESS_TOKENS)
        return len(pids) > 0

    def close_download_processes(self, timeout_s: float = 20.0) -> int:
        pids = self._find_processes([
            "backend.fabric_classifier.training.download_fibre_subset",
            "backend/fabric_classifier/training/download_fibre_subset.py",
        ])

        closed = 0
        for pid in pids:
            if pid == os.getpid():
                continue
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                closed += 1
            except Exception:
                continue

        deadline = time.time() + max(1.0, float(timeout_s))
        while time.time() < deadline:
            remaining = [pid for pid in self._find_processes([
                "backend.fabric_classifier.training.download_fibre_subset",
                "backend/fabric_classifier/training/download_fibre_subset.py",
            ]) if pid != os.getpid()]
            if not remaining:
                break
            time.sleep(0.25)

        for pid in self._find_processes([
            "backend.fabric_classifier.training.download_fibre_subset",
            "backend/fabric_classifier/training/download_fibre_subset.py",
        ]):
            if pid == os.getpid():
                continue
            try:
                psutil.Process(pid).kill()
            except Exception:
                pass

        return closed

    def wait_for_no_download_processes(self, timeout_s: float = 180.0, poll_s: float = 1.0) -> bool:
        deadline = time.time() + max(1.0, float(timeout_s))
        while time.time() < deadline:
            pids = [
                pid
                for pid in self._find_processes([
                    "backend.fabric_classifier.training.download_fibre_subset",
                    "backend/fabric_classifier/training/download_fibre_subset.py",
                ])
                if pid != os.getpid()
            ]
            if not pids:
                return True
            time.sleep(max(0.2, float(poll_s)))
        return False

    def wait_until_ram_below_limit(
        self,
        limit_percent: float = RAM_HARD_LIMIT_PERCENT,
        poll_s: float = 2.0,
        timeout_s: float | None = None,
    ) -> bool:
        limit = float(limit_percent)
        deadline = None
        if timeout_s is not None:
            deadline = time.time() + max(0.5, float(timeout_s))

        while not self._stop_event.is_set():
            ram_percent = float(psutil.virtual_memory().percent)
            if ram_percent < limit:
                return True
            if deadline is not None and time.time() >= deadline:
                return False
            self._stop_event.wait(timeout=max(0.5, float(poll_s)))

        return False

    def wait_until_download_allowed(self, poll_s: float = 1.0) -> None:
        while not self._stop_event.is_set():
            training_active = False if self._ignore_training_active() else self.is_any_training_process_active()
            if not self.is_download_paused() and not self.is_downloads_force_paused() and not training_active:
                return
            self._stop_event.wait(timeout=max(0.1, float(poll_s)))

    def _ignore_training_active(self) -> bool:
        return str(os.environ.get(IGNORE_TRAINING_ACTIVE_ENV, "")).strip() == "1"

    def _write_json_atomic(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp_path.replace(path)

    def _find_processes(self, tokens: list[str]) -> list[int]:
        token_set = [t.lower() for t in tokens]
        pids = []
        for proc in psutil.process_iter(["pid", "cmdline"]):
            try:
                cmdline = " ".join(proc.info.get("cmdline") or []).lower()
            except Exception:
                continue
            if not cmdline:
                continue
            if any(token in cmdline for token in token_set):
                pids.append(int(proc.info["pid"]))
        return pids

    def _pid_matches_tokens(self, pid: int, tokens: list[str]) -> bool:
        token_set = [t.lower() for t in tokens]
        try:
            proc = psutil.Process(int(pid))
            cmdline = " ".join(proc.cmdline()).lower()
        except Exception:
            return False
        return bool(cmdline) and any(token in cmdline for token in token_set)

    def _monitor_loop(self) -> None:
        # Prime counters for non-zero network delta on subsequent iterations.
        _ = self._collect_metrics()
        while not self._stop_event.is_set():
            metrics = self._collect_metrics()
            self._apply_rules_and_update(metrics)
            self._stop_event.wait(timeout=self.scan_interval_s)

    def _collect_metrics(self) -> dict[str, float | int]:
        cpu_percent = float(psutil.cpu_percent(interval=None))
        vm = psutil.virtual_memory()
        ram_percent = float(vm.percent)

        total_cpu_cores = max(1, int(psutil.cpu_count(logical=True) or 1))
        free_cpu_cores = max(0, int(round(total_cpu_cores * (1.0 - (cpu_percent / 100.0)))))

        net = psutil.net_io_counters()
        now = time.time()
        total_bytes = int(net.bytes_sent + net.bytes_recv)
        network_mbps = 0.0
        if self._net_prev_bytes is not None and self._net_prev_time is not None:
            dt = max(now - self._net_prev_time, 1e-6)
            byte_delta = max(0, total_bytes - self._net_prev_bytes)
            network_mbps = float((byte_delta * 8.0) / (dt * 1_000_000.0))
        self._net_prev_bytes = total_bytes
        self._net_prev_time = now

        vram_free_mb = 0.0
        if torch.cuda.is_available():
            try:
                free_bytes, _ = torch.cuda.mem_get_info(0)
                vram_free_mb = float(free_bytes / (1024 ** 2))
            except Exception:
                vram_free_mb = 0.0

        return {
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "vram_free_mb": vram_free_mb,
            "network_mbps": network_mbps,
            "total_cpu_cores": total_cpu_cores,
            "free_cpu_cores": free_cpu_cores,
        }

    def _bandwidth_to_download_workers(self, network_mbps: float) -> int:
        _ = network_mbps
        return self.clamp_download_workers(self.max_download_workers)

    def _free_cores_to_dataloader_workers(self, free_cpu_cores: int) -> int:
        return min(4, max(0, free_cpu_cores - 2))

    def _ram_to_batch_size(self, ram_percent: float) -> int:
        total_ram_gb = psutil.virtual_memory().total / (1024**3)
        if total_ram_gb >= 20.0 and ram_percent < 75.0:
            return 32
        elif total_ram_gb >= 16.0 and ram_percent < 80.0:
            return 16
        return 8

    def _apply_rules_and_update(self, metrics: dict[str, float | int]) -> None:
        cpu_percent = float(metrics["cpu_percent"])
        ram_percent = float(metrics["ram_percent"])
        network_mbps = float(metrics["network_mbps"])
        total_cpu_cores = int(metrics["total_cpu_cores"])
        free_cpu_cores = int(metrics["free_cpu_cores"])
        vram_free_mb = float(metrics["vram_free_mb"])

        with self._lock:
            prev = self._snapshot

            trigger_reasons: list[str] = []
            training_active = False if self._ignore_training_active() else self.is_any_training_process_active()

            download_workers = self._bandwidth_to_download_workers(network_mbps)
            dataloader_workers = self._free_cores_to_dataloader_workers(free_cpu_cores)
            batch_size = self._ram_to_batch_size(ram_percent)
            forced_download_pause = self.is_downloads_force_paused()

            # Clear stale forced pause immediately when no training process is actually alive.
            if forced_download_pause and not training_active:
                DOWNLOAD_FORCE_PAUSE_FILE.unlink(missing_ok=True)
                forced_download_pause = False
                trigger_reasons.append("cleared_stale_forced_pause_no_training")

            if training_active:
                trigger_reasons.append("training_active_pause_downloads")

            if forced_download_pause:
                trigger_reasons.append("forced_download_pause")

            # Policy: downloads pause only while training is active.
            download_paused = bool(training_active)

            training_ram_critical = training_active and ram_percent >= 90.0
            if training_ram_critical:
                trigger_reasons.append("ram>=90_training_critical")

            effective_download_workers = 0 if download_paused else download_workers

            next_snapshot = ResourceSnapshot(
                timestamp=utc_now_iso(),
                cpu_percent=cpu_percent,
                ram_percent=ram_percent,
                vram_free_mb=vram_free_mb,
                network_mbps=network_mbps,
                total_cpu_cores=total_cpu_cores,
                free_cpu_cores=free_cpu_cores,
                download_workers=int(effective_download_workers),
                dataloader_workers=int(dataloader_workers),
                batch_size=int(batch_size),
                download_paused=bool(download_paused),
                training_ram_critical=bool(training_ram_critical),
                forced_download_pause=bool(forced_download_pause),
            )

            changed = []
            for field_name in [
                "download_workers",
                "dataloader_workers",
                "batch_size",
                "download_paused",
                "training_ram_critical",
                "forced_download_pause",
            ]:
                if getattr(prev, field_name) != getattr(next_snapshot, field_name):
                    changed.append(field_name)

            self._snapshot = next_snapshot

        if changed:
            reason = trigger_reasons if trigger_reasons else ["adaptive_scaling"]
            self._log_decision(reason=reason, changed=changed, snapshot=next_snapshot)

    def _log_decision(self, reason: list[str], changed: list[str], snapshot: ResourceSnapshot) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        log_entry = {
            "timestamp": snapshot.timestamp,
            "reason": reason,
            "changed": changed,
            "resource_levels": {
                "cpu_percent": round(snapshot.cpu_percent, 2),
                "ram_percent": round(snapshot.ram_percent, 2),
                "vram_free_mb": round(snapshot.vram_free_mb, 2),
                "network_mbps": round(snapshot.network_mbps, 3),
            },
            "applied": {
                "download_workers": snapshot.download_workers,
                "download_paused": snapshot.download_paused,
                "dataloader_workers": snapshot.dataloader_workers,
                "batch_size": snapshot.batch_size,
                "training_ram_critical": snapshot.training_ram_critical,
                "forced_download_pause": snapshot.forced_download_pause,
            },
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=True) + "\n")


_GLOBAL_MANAGER: DynamicResourceManager | None = None
_GLOBAL_MANAGER_LOCK = threading.Lock()


def get_resource_manager(auto_start: bool = True) -> DynamicResourceManager:
    global _GLOBAL_MANAGER
    with _GLOBAL_MANAGER_LOCK:
        if _GLOBAL_MANAGER is None:
            _GLOBAL_MANAGER = DynamicResourceManager()
        manager = _GLOBAL_MANAGER
    if auto_start:
        manager.start()
    return manager
