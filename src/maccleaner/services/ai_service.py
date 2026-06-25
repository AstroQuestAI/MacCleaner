"""Apple Intelligence bridge — calls maccleaner-ai (Swift/FoundationModels).

All calls are on-device, private, and free. The binary is a 131 KB Swift
executable that wraps FoundationModels.framework (macOS 26+).
"""
from __future__ import annotations

import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

from ..models.scan_result import ScanReport

# ── Locate the binary ──────────────────────────────────────────────────────

def _find_binary() -> Path | None:
    """Find maccleaner-ai — frozen bundle, dist/, or dev swift-ai/."""
    candidates = [
        # PyInstaller frozen bundle: binary is next to the executable
        Path(sys.executable).parent / "maccleaner-ai",
        # PyInstaller _MEIPASS (onefile mode)
        Path(getattr(sys, "_MEIPASS", "")) / "maccleaner-ai",
        # Development: dist/ directory  (parents[3] = project root)
        Path(__file__).parents[3] / "dist"     / "maccleaner-ai",
        # Development: swift-ai/ directory
        Path(__file__).parents[3] / "swift-ai" / "maccleaner-ai",
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None

# ── Low-level call ─────────────────────────────────────────────────────────

def _call(payload: dict, timeout: int = 30) -> dict:
    """Send one JSON line to the binary, return the parsed response."""
    binary = _find_binary()
    if binary is None:
        return {"status": "unavailable", "reason": "binaryNotFound"}

    line = json.dumps(payload) + "\n"
    try:
        result = subprocess.run(
            [str(binary)],
            input=line,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        first_line = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "{}"
        return json.loads(first_line)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, IndexError, OSError):
        return {"status": "error", "message": "AI binary failed"}

# ── Public API ─────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def is_available() -> bool:
    """Returns True if Apple Intelligence is available on this device."""
    resp = _call({"cmd": "available"}, timeout=5)
    return resp.get("status") == "ok"


def summarize_scan(report: ScanReport) -> str | None:
    """Generate a 2-sentence plain-English scan summary via Apple Intelligence."""
    if not report.results:
        return None

    # Build a compact context string — never send raw file paths to keep it tight
    lines = []
    for r in sorted(report.results, key=lambda x: x.total_size, reverse=True):
        if r.total_size > 0:
            lines.append(f"- {r.category.value}: {r.count} files, {r.total_size_mb:.0f} MB")

    context = f"Total junk: {report.total_size_gb:.2f} GB across {report.total_count} files\n" + "\n".join(lines)
    resp = _call({"cmd": "summarize", "context": context})
    return resp.get("text") if resp.get("status") == "ok" else None


def explain_category(category_name: str, size_mb: float, count: int) -> str | None:
    """Get a one-sentence AI explanation of a scan category."""
    resp = _call({
        "cmd":      "explain",
        "category": category_name,
        "size_mb":  round(size_mb, 1),
        "count":    count,
    })
    return resp.get("text") if resp.get("status") == "ok" else None


def advise_before_clean(category_names: list[str], total_gb: float) -> str | None:
    """Get AI safety advice before deleting the selected categories."""
    if not category_names:
        return None
    resp = _call({
        "cmd":        "advise",
        "categories": category_names,
        "total_gb":   round(total_gb, 2),
    })
    return resp.get("text") if resp.get("status") == "ok" else None


def generate_notification_text(report: ScanReport) -> str | None:
    """Generate a personalised notification body for a background scan result."""
    if not report.results or report.total_size_gb < 0.1:
        return None

    top = max(report.results, key=lambda r: r.total_size)
    resp = _call({
        "cmd":          "notify",
        "total_gb":     round(report.total_size_gb, 2),
        "top_category": top.category.value,
        "top_gb":       round(top.total_size_mb / 1024, 2),
    })
    return resp.get("text") if resp.get("status") == "ok" else None
