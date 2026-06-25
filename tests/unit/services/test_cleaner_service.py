"""Unit tests for CleanerService."""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

from maccleaner.services.cleaner_service import CleanerService
from maccleaner.models.category import Category
from maccleaner.models.scan_result import CategoryResult, FileEntry, ScanReport


def _make_result(category: Category, sizes: list[int], tmp_path: Path) -> CategoryResult:
    result = CategoryResult(category=category)
    for i, size in enumerate(sizes):
        f = tmp_path / f"{category.name}_{i}"
        f.write_bytes(b"x" * size)
        result.entries.append(FileEntry(path=f, size=size))
    return result


class TestCleanerService:
    def test_given_scan_when_called_then_returns_report_with_all_categories(
        self, tmp_path: Path
    ) -> None:
        service = CleanerService(home=tmp_path)
        report = service.scan()
        categories = {r.category for r in report.results}
        assert Category.USER_CACHES in categories
        assert Category.TRASH in categories

    def test_given_dry_run_when_clean_then_no_files_deleted(self, tmp_path: Path) -> None:
        f = tmp_path / "junk.bin"
        f.write_bytes(b"x" * 1024)

        entry = FileEntry(path=f, size=1024)
        result = CategoryResult(category=Category.TEMP_FILES, entries=[entry])
        report = ScanReport(results=[result])

        service = CleanerService(home=tmp_path)
        freed = service.clean(report, dry_run=True)

        assert f.exists(), "dry run must not delete files"
        assert freed[Category.TEMP_FILES] == 1024

    def test_given_real_run_when_clean_caches_then_file_trashed(self, tmp_path: Path) -> None:
        f = tmp_path / "cache_junk.bin"
        f.write_bytes(b"y" * 512)

        entry = FileEntry(path=f, size=512)
        result = CategoryResult(category=Category.USER_CACHES, entries=[entry])
        report = ScanReport(results=[result])

        service = CleanerService(home=tmp_path)
        with patch("maccleaner.services.cleaner_service.send2trash") as mock_trash:
            freed = service.clean(report)

        mock_trash.send2trash.assert_called_once_with(str(f))
        assert freed[Category.USER_CACHES] == 512

    def test_given_trash_category_when_clean_then_permanently_deleted(self, tmp_path: Path) -> None:
        f = tmp_path / "trash_item.bin"
        f.write_bytes(b"z" * 256)

        entry = FileEntry(path=f, size=256)
        result = CategoryResult(category=Category.TRASH, entries=[entry])
        report = ScanReport(results=[result])

        service = CleanerService(home=tmp_path)
        freed = service.clean(report)

        assert not f.exists(), "Trash items should be permanently deleted"
        assert freed[Category.TRASH] == 256

    def test_given_category_filter_when_clean_then_only_selected_cleaned(
        self, tmp_path: Path
    ) -> None:
        cache_f = tmp_path / "cache.bin"
        cache_f.write_bytes(b"c" * 100)
        log_f = tmp_path / "log.log"
        log_f.write_bytes(b"l" * 100)

        report = ScanReport(results=[
            CategoryResult(
                category=Category.USER_CACHES,
                entries=[FileEntry(path=cache_f, size=100)],
            ),
            CategoryResult(
                category=Category.SYSTEM_LOGS,
                entries=[FileEntry(path=log_f, size=100)],
            ),
        ])

        service = CleanerService(home=tmp_path)
        with patch("maccleaner.services.cleaner_service.send2trash"):
            freed = service.clean(report, categories=[Category.USER_CACHES])

        assert Category.USER_CACHES in freed
        assert Category.SYSTEM_LOGS not in freed

    def test_given_missing_file_when_clean_then_skipped_gracefully(
        self, tmp_path: Path
    ) -> None:
        ghost = tmp_path / "ghost.bin"  # intentionally NOT created

        entry = FileEntry(path=ghost, size=999)
        result = CategoryResult(category=Category.USER_CACHES, entries=[entry])
        report = ScanReport(results=[result])

        service = CleanerService(home=tmp_path)
        with patch("maccleaner.services.cleaner_service.send2trash"):
            freed = service.clean(report)

        assert freed[Category.USER_CACHES] == 0

    def test_given_progress_callback_when_scan_then_called_per_category(
        self, tmp_path: Path
    ) -> None:
        called: list[Category] = []

        def on_progress(cat: Category, i: int, total: int) -> None:
            called.append(cat)

        service = CleanerService(home=tmp_path)
        service.scan(on_progress=on_progress)

        assert len(called) == 14  # one per scanner
