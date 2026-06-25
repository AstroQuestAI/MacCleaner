"""Unit tests for BrowserCacheScanner."""
from pathlib import Path

from maccleaner.scanners.browser_scanner import BrowserCacheScanner
from maccleaner.models.category import Category


class TestBrowserCacheScanner:
    def test_given_no_browser_caches_when_scan_then_empty(self, tmp_path: Path) -> None:
        scanner = BrowserCacheScanner(home=tmp_path)
        result = scanner.scan()
        assert result.count == 0
        assert result.category == Category.BROWSER_CACHES

    def test_given_chrome_cache_when_scan_then_found(self, tmp_path: Path) -> None:
        cache_dir = tmp_path / "Library" / "Caches" / "Google" / "Chrome" / "Default" / "Cache"
        cache_dir.mkdir(parents=True)
        (cache_dir / "data_0").write_bytes(b"c" * 4096)

        scanner = BrowserCacheScanner(home=tmp_path)
        result = scanner.scan()

        assert result.count == 1
        assert result.total_size == 4096

    def test_given_multiple_browsers_when_scan_then_all_found(self, tmp_path: Path) -> None:
        chrome = tmp_path / "Library" / "Caches" / "Google" / "Chrome" / "Default" / "Cache"
        brave = tmp_path / "Library" / "Caches" / "BraveSoftware" / "Brave-Browser" / "Default" / "Cache"
        chrome.mkdir(parents=True)
        brave.mkdir(parents=True)
        (chrome / "c1").write_bytes(b"x" * 100)
        (brave / "b1").write_bytes(b"y" * 200)

        scanner = BrowserCacheScanner(home=tmp_path)
        result = scanner.scan()

        assert result.count == 2
