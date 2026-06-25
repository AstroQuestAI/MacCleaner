"""Persistent user settings — stored at ~/.config/maccleaner/settings.json."""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

_PATH = Path.home() / ".config" / "maccleaner" / "settings.json"


@dataclass
class Settings:
    # ── Appearance ─────────────────────────────────────────────────────────
    theme: str = "glass"           # "glass" | "dark"
    tray_label: str = "free"       # "free" (free GB) | "pct" (disk %)
    opacity: int = 92              # 70–100 %

    # ── Scheduler ──────────────────────────────────────────────────────────
    auto_scan: bool = True
    scan_interval_h: int = 2       # 1 | 2 | 6 | 12 | 24
    notify_above_pct: int = 70     # popup only when disk ≥ this %
    junk_min_mb: int = 200         # 50 | 100 | 200 | 500
    warn_pct: int = 70             # tray turns amber at this disk %
    crit_pct: int = 85             # tray turns red at this disk %

    # ── Scan ───────────────────────────────────────────────────────────────
    scan_node_modules: bool = True
    startup_delay_s: int = 15      # 5 | 15 | 30 | 60

    def save(self) -> None:
        _PATH.parent.mkdir(parents=True, exist_ok=True)
        _PATH.write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls) -> Settings:
        try:
            raw = json.loads(_PATH.read_text())
            valid = set(cls.__dataclass_fields__)
            return cls(**{k: v for k, v in raw.items() if k in valid})
        except Exception:
            return cls()
