"""Mail downloads / attachments scanner."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_MAIL_PATHS = [
    "Library/Mail Downloads",
    "Library/Containers/com.apple.mail/Data/Library/Mail Downloads",
]


class MailDownloadsScanner(BaseScanner):
    category = Category.MAIL_DOWNLOADS

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []
        for rel in _MAIL_PATHS:
            p = self._home / rel
            if p.exists() and p.is_dir():
                for f in p.rglob("*"):
                    if f.is_file():
                        paths.append(f)
        return paths
