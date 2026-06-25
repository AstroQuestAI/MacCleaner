"""Unused virtual environment scanner.

Finds Python venvs (directories containing bin/python or Scripts/python.exe)
inside common project roots. Reports each one as a separate entry so the user
can selectively delete.
"""
import time
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_VENV_NAMES = {".venv", "venv", "env", ".env", "virtualenv"}

_SEARCH_ROOTS = [
    "Projects", "Developer", "code", "repos", "workspace",
    "Documents", "Desktop", "Sites", "src",
]

# Consider a venv "unused" if its parent project hasn't been touched in 60 days
_UNUSED_DAYS = 60
_SECONDS_PER_DAY = 86_400


def _is_venv(path: Path) -> bool:
    """True if the directory looks like a Python virtual environment."""
    return (
        path.is_dir()
        and (
            (path / "bin" / "python").exists()
            or (path / "bin" / "python3").exists()
            or (path / "Scripts" / "python.exe").exists()
        )
    )


def _days_since_modified(path: Path) -> float:
    try:
        mtime = path.stat().st_mtime
        return (time.time() - mtime) / _SECONDS_PER_DAY
    except OSError:
        return 0.0


class VenvScanner(BaseScanner):
    category = Category.UNUSED_VENVS

    def __init__(self, home: Path | None = None, unused_days: int = _UNUSED_DAYS) -> None:
        self._home = home or Path.home()
        self._unused_days = unused_days

    def _find_paths(self) -> list[Path]:
        found: list[Path] = []

        for root_name in _SEARCH_ROOTS:
            root = self._home / root_name
            if not root.exists():
                continue

            # Search 3 levels deep: root / project / [sub] / venv_dir
            for project in root.iterdir():
                if not project.is_dir():
                    continue
                found.extend(self._scan_project(project))

        return found

    def _scan_project(self, project: Path) -> list[Path]:
        results: list[Path] = []
        try:
            for child in project.rglob("*"):
                if child.name not in _VENV_NAMES:
                    continue
                if not _is_venv(child):
                    continue
                # Only report if the project root hasn't been used recently
                if _days_since_modified(project) >= self._unused_days:
                    results.append(child)
                # Don't recurse inside a venv dir itself
                break
        except (PermissionError, OSError):
            pass
        return results
