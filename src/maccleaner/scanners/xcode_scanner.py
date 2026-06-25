"""Xcode derived data, archives, simulators, and iOS backup scanner."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_XCODE_PATHS = [
    "Library/Developer/Xcode/DerivedData",
    "Library/Developer/Xcode/Archives",
    "Library/Developer/CoreSimulator/Devices",
    "Library/Developer/Xcode/iOS Device Logs",
]

_BACKUP_PATHS = [
    "Library/Application Support/MobileSync/Backup",
]


class XcodeScanner(BaseScanner):
    category = Category.XCODE_ARTIFACTS

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []
        for rel in _XCODE_PATHS + _BACKUP_PATHS:
            p = self._home / rel
            if not p.exists():
                continue
            if rel in _BACKUP_PATHS:
                # Each subfolder is one device backup
                for backup in p.iterdir():
                    if backup.is_dir():
                        paths.append(backup)
            elif rel == "Library/Developer/CoreSimulator/Devices":
                # Each subfolder is one simulator
                for sim in p.iterdir():
                    if sim.is_dir():
                        paths.append(sim)
            else:
                paths.append(p)
        return paths
