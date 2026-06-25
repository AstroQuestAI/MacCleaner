"""Integration test: scan against a real (controlled) temp tree."""
import pytest
from pathlib import Path

from maccleaner.scanners.cache_scanner import UserCacheScanner
from maccleaner.scanners.trash_scanner import TrashScanner
from maccleaner.services.cleaner_service import CleanerService
from maccleaner.models.category import Category


class TestScanRealFileSystem:
    def test_given_fake_home_with_caches_when_scan_then_sizes_accurate(
        self, tmp_path: Path
    ) -> None:
        # Build a realistic home layout
        caches = tmp_path / "Library" / "Caches"
        (caches / "com.test.App").mkdir(parents=True)
        (caches / "com.test.App" / "data.bin").write_bytes(b"a" * 8192)

        trash = tmp_path / ".Trash"
        trash.mkdir()
        (trash / "old.pdf").write_bytes(b"p" * 4096)

        service = CleanerService(home=tmp_path)
        report = service.scan()

        cache_result = report.result_for(Category.USER_CACHES)
        trash_result = report.result_for(Category.TRASH)

        assert cache_result is not None
        assert cache_result.total_size == 8192

        assert trash_result is not None
        assert trash_result.total_size == 4096

        assert report.total_size >= 12288

    def test_given_dry_run_when_clean_then_all_files_survive(
        self, tmp_path: Path
    ) -> None:
        caches = tmp_path / "Library" / "Caches"
        app_dir = caches / "com.dry.Test"
        app_dir.mkdir(parents=True)
        f = app_dir / "big.bin"
        f.write_bytes(b"x" * 2048)

        service = CleanerService(home=tmp_path)
        report = service.scan()
        service.clean(report, dry_run=True)

        assert f.exists(), "dry run must not touch any files"

    def test_given_trash_cleanup_when_clean_then_trash_items_deleted(
        self, tmp_path: Path
    ) -> None:
        trash = tmp_path / ".Trash"
        trash.mkdir()
        f = trash / "unwanted.doc"
        f.write_bytes(b"d" * 1024)

        service = CleanerService(home=tmp_path)
        report = service.scan()
        service.clean(report, categories=[Category.TRASH])

        assert not f.exists()
