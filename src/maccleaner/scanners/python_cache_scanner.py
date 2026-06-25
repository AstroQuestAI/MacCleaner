"""Python cache scanner — pip, poetry, uv, __pycache__."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_PYTHON_CACHE_PATHS = [
    ".cache/pip",                             # pip HTTP + wheel cache
    ".cache/pypoetry/cache",                  # Poetry cache
    ".cache/uv",                              # uv package manager cache
    "Library/Caches/pip",                     # pip on macOS (alt)
    ".cache/hatch",                           # Hatch cache
    ".cache/pdm",                             # PDM cache
]

# Directories to search for __pycache__ (shallow scan to keep it fast)
_PYCACHE_SEARCH_ROOTS = [
    "Projects", "Developer", "code", "repos", "workspace",
    "Documents", "Desktop", "Sites",
]


class PythonCacheScanner(BaseScanner):
    category = Category.PYTHON_CACHE

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []

        # Named cache directories
        for rel in _PYTHON_CACHE_PATHS:
            p = self._home / rel
            if p.exists():
                paths.append(p)

        # __pycache__ dirs inside common project roots (2 levels deep)
        for root_name in _PYCACHE_SEARCH_ROOTS:
            root = self._home / root_name
            if not root.exists():
                continue
            for project in root.iterdir():
                if not project.is_dir():
                    continue
                pycache = project / "__pycache__"
                if pycache.exists():
                    paths.append(pycache)
                # One level deeper
                for sub in project.iterdir():
                    if sub.is_dir():
                        pc2 = sub / "__pycache__"
                        if pc2.exists():
                            paths.append(pc2)

        return paths
