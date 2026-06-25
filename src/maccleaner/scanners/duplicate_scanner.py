"""Duplicate file scanner — finds exact duplicates by SHA-256 hash.

Groups files by (size, hash). Only computes hash for files sharing the same
size, so large unique files are skipped cheaply.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from collections import defaultdict

from .base import BaseScanner
from ..models.category import Category
from ..models.scan_result import CategoryResult, FileEntry

# Scan these directories for duplicates
_SCAN_ROOTS = [
    Path.home() / "Downloads",
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Movies",
]

# Only flag files above this size — avoids flagging tiny .gitkeep etc.
_MIN_SIZE_BYTES = 512 * 1024  # 512 KB

_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".gif", ".bmp", ".tiff", ".webp"}
_VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}
_DOC_EXTS   = {".pdf", ".docx", ".xlsx", ".pptx", ".zip", ".dmg", ".pkg"}

_SCAN_EXTS = _IMAGE_EXTS | _VIDEO_EXTS | _DOC_EXTS


def _sha256(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            while chunk := f.read(131_072):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


class DuplicateScanner(BaseScanner):
    """Find duplicate files in common user folders."""

    @property
    def category(self) -> Category:
        return Category.DUPLICATES

    def _find_paths(self) -> list[Path]:
        # Step 1: collect files, group by size
        by_size: dict[int, list[Path]] = defaultdict(list)
        for root in _SCAN_ROOTS:
            if not root.exists():
                continue
            try:
                for p in root.rglob("*"):
                    if not p.is_file():
                        continue
                    if p.suffix.lower() not in _SCAN_EXTS:
                        continue
                    try:
                        sz = p.stat().st_size
                    except OSError:
                        continue
                    if sz >= _MIN_SIZE_BYTES:
                        by_size[sz].append(p)
            except PermissionError:
                continue

        # Step 2: hash only groups with >1 file of same size
        duplicates: list[Path] = []
        for size, paths in by_size.items():
            if len(paths) < 2:
                continue
            by_hash: dict[str, list[Path]] = defaultdict(list)
            for p in paths:
                h = _sha256(p)
                if h:
                    by_hash[h].append(p)
            for group in by_hash.values():
                if len(group) >= 2:
                    # Keep the first (oldest by path sort), mark rest as duplicates
                    for dup in sorted(group)[1:]:
                        duplicates.append(dup)

        return duplicates
