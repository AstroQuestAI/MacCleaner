"""Node.js / npm ecosystem cache scanner."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_NODE_CACHE_PATHS = [
    ".npm",                          # npm cache
    ".yarn/cache",                   # Yarn v1
    ".cache/yarn",                   # Yarn v1 (alt)
    ".pnpm-store",                   # pnpm
    ".local/share/pnpm/store",       # pnpm (XDG)
    ".bun/install/cache",            # Bun
    ".cache/node-gyp",               # node-gyp build cache
    "Library/Caches/node-gyp",       # node-gyp on macOS
]


class NodeCacheScanner(BaseScanner):
    category = Category.NODE_CACHE

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []
        for rel in _NODE_CACHE_PATHS:
            p = self._home / rel
            if p.exists():
                paths.append(p)
        return paths
