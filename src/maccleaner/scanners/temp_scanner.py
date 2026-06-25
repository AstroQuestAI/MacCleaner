"""Temporary file scanner."""
import os
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner


class TempScanner(BaseScanner):
    category = Category.TEMP_FILES

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []

        # macOS user temp dir
        tmp_dir = Path(os.environ.get("TMPDIR", "/private/var/folders"))
        if tmp_dir.exists() and tmp_dir.is_dir():
            # TMPDIR is something like /var/folders/xx/yyyy/T/
            for f in tmp_dir.glob("**/*"):
                if f.is_file():
                    try:
                        size = f.stat().st_size
                        # Skip tiny files — noise
                        if size > 1024:
                            paths.append(f)
                    except (PermissionError, OSError):
                        pass
                if len(paths) > 500:  # cap to avoid huge listings
                    break

        # /private/tmp
        private_tmp = Path("/private/tmp")
        if private_tmp.exists():
            for f in private_tmp.iterdir():
                if f.is_file():
                    try:
                        paths.append(f)
                    except (PermissionError, OSError):
                        pass

        return paths
