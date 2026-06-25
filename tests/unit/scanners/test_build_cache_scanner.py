from pathlib import Path
from maccleaner.scanners.build_cache_scanner import BuildCacheScanner
from maccleaner.models.category import Category


class TestBuildCacheScanner:
    def test_given_no_build_caches_when_scan_then_empty(self, tmp_path):
        result = BuildCacheScanner(home=tmp_path).scan()
        assert result.count == 0
        assert result.category == Category.BUILD_CACHE

    def test_given_gradle_cache_when_scan_then_found(self, tmp_path):
        gradle = tmp_path / ".gradle" / "caches"
        gradle.mkdir(parents=True)
        (gradle / "modules.bin").write_bytes(b"g" * 8192)
        result = BuildCacheScanner(home=tmp_path).scan()
        names = {e.path.name for e in result.entries}
        assert "caches" in names
        assert result.total_size == 8192

    def test_given_cargo_and_go_caches_when_scan_then_both_found(self, tmp_path):
        cargo = tmp_path / ".cargo" / "registry" / "cache"
        cargo.mkdir(parents=True)
        (cargo / "crate.tar.gz").write_bytes(b"r" * 1024)
        go_build = tmp_path / ".cache" / "go-build"
        go_build.mkdir(parents=True)
        (go_build / "pkg.a").write_bytes(b"g" * 2048)
        result = BuildCacheScanner(home=tmp_path).scan()
        assert result.count == 2
        assert result.total_size == 3072
