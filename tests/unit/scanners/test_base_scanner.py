"""Unit tests for BaseScanner template method."""
import pytest
from pathlib import Path
from unittest.mock import patch

from maccleaner.models.category import Category
from maccleaner.models.scan_result import CategoryResult
from maccleaner.scanners.base import BaseScanner


class _ConcreteScanner(BaseScanner):
    """Test double that returns whatever paths we give it."""
    category = Category.TEMP_FILES

    def __init__(self, paths: list[Path]):
        self._paths = paths

    def _find_paths(self) -> list[Path]:
        return self._paths


class TestBaseScanner:
    def test_given_no_paths_when_scan_then_result_is_empty(self) -> None:
        scanner = _ConcreteScanner([])
        result = scanner.scan()
        assert result.count == 0
        assert result.total_size == 0
        assert result.error is None

    def test_given_existing_files_when_scan_then_entries_populated(self, tmp_path: Path) -> None:
        f = tmp_path / "junk.tmp"
        f.write_bytes(b"x" * 1024)

        scanner = _ConcreteScanner([f])
        result = scanner.scan()

        assert result.count == 1
        assert result.total_size == 1024

    def test_given_directory_when_scan_then_size_recursed(self, tmp_path: Path) -> None:
        d = tmp_path / "cache_dir"
        d.mkdir()
        (d / "a.bin").write_bytes(b"a" * 512)
        (d / "b.bin").write_bytes(b"b" * 512)

        scanner = _ConcreteScanner([d])
        result = scanner.scan()

        assert result.total_size == 1024

    def test_given_find_paths_raises_when_scan_then_error_recorded(self) -> None:
        class _ErrorScanner(BaseScanner):
            category = Category.TEMP_FILES

            def _find_paths(self):
                raise PermissionError("no access")

        result = _ErrorScanner().scan()
        assert result.error is not None
        assert "no access" in result.error
        assert result.count == 0

    def test_given_missing_file_when_size_of_then_returns_zero(self, tmp_path: Path) -> None:
        missing = tmp_path / "ghost.bin"
        size = BaseScanner._size_of(missing)
        assert size == 0
