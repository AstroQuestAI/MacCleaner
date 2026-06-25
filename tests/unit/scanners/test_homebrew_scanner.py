from pathlib import Path
from maccleaner.scanners.homebrew_scanner import HomebrewCacheScanner
from maccleaner.models.category import Category


class TestHomebrewCacheScanner:
    def test_given_no_homebrew_cache_when_scan_then_empty(self, tmp_path: Path):
        result = HomebrewCacheScanner(home=tmp_path).scan()
        assert result.count == 0
        assert result.category == Category.HOMEBREW_CACHE

    def test_given_homebrew_downloads_when_scan_then_found(self, tmp_path: Path):
        cache = tmp_path / "Library" / "Caches" / "Homebrew"
        cache.mkdir(parents=True)
        (cache / "formula-1.0.tar.gz").write_bytes(b"b" * 8192)
        result = HomebrewCacheScanner(home=tmp_path).scan()
        assert result.count == 1
        assert result.total_size == 8192

    def test_given_homebrew_subdirs_when_scan_then_whole_dir_counted(self, tmp_path: Path):
        cache = tmp_path / "Library" / "Caches" / "Homebrew"
        downloads = cache / "downloads"
        downloads.mkdir(parents=True)
        (downloads / "pkg.tar.gz").write_bytes(b"x" * 4096)
        (cache / "api").mkdir()
        (cache / "api" / "formula.json").write_bytes(b"j" * 1024)
        result = HomebrewCacheScanner(home=tmp_path).scan()
        assert result.count == 1
        assert result.total_size == 5120  # 4096 + 1024 bytes across both subdirs
