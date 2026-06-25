"""Abstract base scanner — Template Method pattern."""
from abc import ABC, abstractmethod
from pathlib import Path

from ..models.category import Category
from ..models.scan_result import CategoryResult, FileEntry


class BaseScanner(ABC):
    """Template method: scan() orchestrates; subclasses implement _find_paths()."""

    @property
    @abstractmethod
    def category(self) -> Category:
        ...

    @abstractmethod
    def _find_paths(self) -> list[Path]:
        """Return every path (file or dir) that should be considered for deletion."""
        ...

    def scan(self) -> CategoryResult:
        result = CategoryResult(category=self.category)
        try:
            paths = self._find_paths()
            for path in paths:
                size = self._size_of(path)
                if size > 0:
                    result.entries.append(FileEntry(path=path, size=size))
        except Exception as exc:
            result.error = str(exc)
        return result

    @staticmethod
    def _size_of(path: Path) -> int:
        """Return total size in bytes, recursing into directories."""
        try:
            if path.is_file() or path.is_symlink():
                return path.stat().st_size
            if path.is_dir():
                return sum(
                    f.stat().st_size
                    for f in path.rglob("*")
                    if f.is_file()
                )
        except (PermissionError, OSError):
            pass
        return 0
