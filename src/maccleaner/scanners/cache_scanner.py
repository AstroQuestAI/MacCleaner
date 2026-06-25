"""User and application cache scanner."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_SKIP_DIRS = {"com.apple.Safari"}  # Safari has its own scanner


class UserCacheScanner(BaseScanner):
    category = Category.USER_CACHES

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        caches_dir = self._home / "Library" / "Caches"
        if not caches_dir.exists():
            return []
        paths: list[Path] = []
        for entry in caches_dir.iterdir():
            if entry.name in _SKIP_DIRS:
                continue
            # Only include directories that look like app cache bundles
            if entry.is_dir() and "." in entry.name:
                paths.append(entry)
        return paths
