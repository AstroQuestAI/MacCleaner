"""Unit tests for UserCacheScanner."""
import pytest
from pathlib import Path

from maccleaner.scanners.cache_scanner import UserCacheScanner
from maccleaner.models.category import Category


class TestUserCacheScanner:
    def test_given_caches_dir_missing_when_scan_then_empty(self, tmp_path: Path) -> None:
        scanner = UserCacheScanner(home=tmp_path)
        result = scanner.scan()
        assert result.count == 0
        assert result.category == Category.USER_CACHES

    def test_given_app_cache_dirs_when_scan_then_each_found(self, tmp_path: Path) -> None:
        caches = tmp_path / "Library" / "Caches"
        app1 = caches / "com.example.App"
        app2 = caches / "com.another.App"
        app1.mkdir(parents=True)
        app2.mkdir(parents=True)
        (app1 / "file.bin").write_bytes(b"x" * 2048)
        (app2 / "file.bin").write_bytes(b"y" * 1024)

        scanner = UserCacheScanner(home=tmp_path)
        result = scanner.scan()

        found_names = {e.path.name for e in result.entries}
        assert "com.example.App" in found_names
        assert "com.another.App" in found_names
        assert result.total_size == 3072

    def test_given_safari_cache_when_scan_then_skipped(self, tmp_path: Path) -> None:
        caches = tmp_path / "Library" / "Caches"
        safari = caches / "com.apple.Safari"
        safari.mkdir(parents=True)
        (safari / "stuff").write_bytes(b"s" * 512)

        scanner = UserCacheScanner(home=tmp_path)
        result = scanner.scan()

        assert all(e.path.name != "com.apple.Safari" for e in result.entries)

    def test_given_dir_without_dot_when_scan_then_excluded(self, tmp_path: Path) -> None:
        caches = tmp_path / "Library" / "Caches"
        plain_dir = caches / "nodothere"
        plain_dir.mkdir(parents=True)
        (plain_dir / "f").write_bytes(b"x")

        scanner = UserCacheScanner(home=tmp_path)
        result = scanner.scan()

        assert all(e.path.name != "nodothere" for e in result.entries)
