"""System and application log scanner."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner


class LogScanner(BaseScanner):
    category = Category.SYSTEM_LOGS

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []

        # ~/Library/Logs — per-app logs
        user_logs = self._home / "Library" / "Logs"
        if user_logs.exists():
            for entry in user_logs.iterdir():
                paths.append(entry)

        # /var/log — only include files we can actually delete (writable)
        system_logs = Path("/private/var/log")
        if system_logs.exists():
            for f in system_logs.glob("*.log"):
                if f.is_file():
                    try:
                        if f.stat().st_size > 0 and f.stat().st_uid == __import__("os").getuid():
                            paths.append(f)
                    except (PermissionError, OSError):
                        pass

        return paths
