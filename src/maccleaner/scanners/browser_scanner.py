"""Browser cache scanner — Safari, Chrome, Firefox, Brave."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_BROWSER_CACHE_PATHS = [
    # Safari
    "Library/Caches/com.apple.Safari",
    # Chrome
    "Library/Caches/Google/Chrome/Default/Cache",
    "Library/Application Support/Google/Chrome/Default/Code Cache",
    # Brave
    "Library/Caches/BraveSoftware/Brave-Browser/Default/Cache",
    # Firefox — find first profile
    "Library/Caches/Firefox",
    # Edge
    "Library/Caches/Microsoft Edge/Default/Cache",
]


class BrowserCacheScanner(BaseScanner):
    category = Category.BROWSER_CACHES

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []
        for rel in _BROWSER_CACHE_PATHS:
            p = self._home / rel
            if p.exists():
                paths.append(p)
        return paths
