"""Trash scanner."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner


class TrashScanner(BaseScanner):
    category = Category.TRASH

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        trash = self._home / ".Trash"
        if not trash.exists():
            return []
        paths: list[Path] = []
        try:
            for entry in trash.iterdir():
                if entry.name == ".DS_Store":
                    continue
                paths.append(entry)
        except PermissionError:
            # Terminal lacks Full Disk Access; silently skip
            pass
        return paths
