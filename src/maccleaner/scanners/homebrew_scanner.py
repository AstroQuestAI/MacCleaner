from pathlib import Path

from .base import BaseScanner
from ..models.category import Category

_HOMEBREW_CACHE_PATHS = [
    "Library/Caches/Homebrew",
]

_HOMEBREW_GLOBAL_PATHS = [
    Path("/opt/homebrew/Caches"),
    Path("/usr/local/Homebrew/Cache"),
]


class HomebrewCacheScanner(BaseScanner):
    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    @property
    def category(self) -> Category:
        return Category.HOMEBREW_CACHE

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []
        for rel in _HOMEBREW_CACHE_PATHS:
            p = self._home / rel
            if p.exists():
                paths.append(p)
        for p in _HOMEBREW_GLOBAL_PATHS:
            if p.exists():
                paths.append(p)
        return paths
