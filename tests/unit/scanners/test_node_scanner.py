from pathlib import Path
from maccleaner.scanners.node_scanner import NodeCacheScanner
from maccleaner.models.category import Category


class TestNodeCacheScanner:
    def test_given_no_npm_cache_when_scan_then_empty(self, tmp_path):
        result = NodeCacheScanner(home=tmp_path).scan()
        assert result.count == 0
        assert result.category == Category.NODE_CACHE

    def test_given_npm_cache_when_scan_then_found(self, tmp_path):
        npm = tmp_path / ".npm"
        npm.mkdir()
        (npm / "package.tgz").write_bytes(b"x" * 4096)
        result = NodeCacheScanner(home=tmp_path).scan()
        assert result.count == 1
        assert result.total_size == 4096

    def test_given_yarn_and_pnpm_when_scan_then_both_found(self, tmp_path):
        (tmp_path / ".npm").mkdir()
        (tmp_path / ".npm" / "f").write_bytes(b"n" * 100)
        yarn = tmp_path / ".yarn" / "cache"
        yarn.mkdir(parents=True)
        (yarn / "f").write_bytes(b"y" * 200)
        result = NodeCacheScanner(home=tmp_path).scan()
        assert result.count == 2
        assert result.total_size == 300
