"""Headless JSON engine — called by the Swift shell via subprocess.

Protocol (stdin/stdout JSON lines):
  scan    → {"cmd": "scan",  "categories": ["User Caches", ...] | null}
  clean   → {"cmd": "clean", "paths": ["/path/a", ...]}
  storage → {"cmd": "storage"}
  quit    → {"cmd": "quit"}

Response (always one JSON line to stdout):
  {"status": "ok", "data": {...}}
  {"status": "error", "message": "..."}
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def _run_scan(categories: list[str] | None) -> dict:
    from .services.cleaner_service import CleanerService
    from .models.category import Category

    service = CleanerService()
    report  = service.scan()

    results = []
    for r in report.results:
        if categories and r.category.value not in categories:
            continue
        results.append({
            "category": r.category.value,
            "count":    r.count,
            "size_mb":  round(r.total_size_mb, 2),
            "paths":    [str(e.path) for e in r.entries],
        })

    return {
        "total_size_gb": round(report.total_size_gb, 3),
        "total_count":   report.total_count,
        "results":       results,
    }


def _run_clean(paths: list[str]) -> dict:
    import send2trash
    moved, errors = [], []
    for p in paths:
        try:
            send2trash.send2trash(p)
            moved.append(p)
        except Exception as exc:
            errors.append({"path": p, "error": str(exc)})
    return {"moved_count": len(moved), "errors": errors}


def _run_storage() -> dict:
    usage = shutil.disk_usage(Path.home())
    return {
        "total_gb": round(usage.total / 1e9, 2),
        "used_gb":  round(usage.used  / 1e9, 2),
        "free_gb":  round(usage.free  / 1e9, 2),
        "used_pct": round(usage.used  / usage.total * 100, 1),
    }


def _ok(data: dict) -> None:
    print(json.dumps({"status": "ok", "data": data}), flush=True)


def _err(msg: str) -> None:
    print(json.dumps({"status": "error", "message": msg}), flush=True)


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            _err(f"invalid JSON: {exc}")
            continue

        cmd = req.get("cmd", "")
        try:
            if cmd == "scan":
                _ok(_run_scan(req.get("categories")))
            elif cmd == "clean":
                _ok(_run_clean(req.get("paths", [])))
            elif cmd == "storage":
                _ok(_run_storage())
            elif cmd == "quit":
                break
            else:
                _err(f"unknown command: {cmd!r}")
        except Exception as exc:
            _err(str(exc))


if __name__ == "__main__":
    main()
