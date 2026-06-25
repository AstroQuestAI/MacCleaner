import time
from pathlib import Path
from unittest.mock import patch
from maccleaner.scanners.venv_scanner import VenvScanner, _is_venv
from maccleaner.models.category import Category


def _make_venv(path: Path) -> None:
    """Create a minimal fake venv directory."""
    (path / "bin").mkdir(parents=True)
    (path / "bin" / "python3").write_bytes(b"#!/usr/bin/python3")
    (path / "lib").mkdir()


class TestIsVenv:
    def test_given_real_venv_structure_when_checked_then_true(self, tmp_path):
        _make_venv(tmp_path)
        assert _is_venv(tmp_path) is True

    def test_given_random_dir_when_checked_then_false(self, tmp_path):
        (tmp_path / "src").mkdir()
        assert _is_venv(tmp_path) is False


class TestVenvScanner:
    def test_given_no_project_roots_when_scan_then_empty(self, tmp_path):
        result = VenvScanner(home=tmp_path, unused_days=0).scan()
        assert result.count == 0
        assert result.category == Category.UNUSED_VENVS

    def test_given_old_project_with_venv_when_scan_then_found(self, tmp_path):
        projects = tmp_path / "Projects"
        project = projects / "old_project"
        venv = project / ".venv"
        _make_venv(venv)
        (venv / "lib" / "site.py").write_bytes(b"x" * 1024)

        # Backdate the project directory mtime to 90 days ago
        old_time = time.time() - 90 * 86_400
        import os
        os.utime(project, (old_time, old_time))

        result = VenvScanner(home=tmp_path, unused_days=60).scan()
        assert result.count == 1

    def test_given_recent_project_with_venv_when_scan_then_excluded(self, tmp_path):
        projects = tmp_path / "Projects"
        project = projects / "active_project"
        venv = project / ".venv"
        _make_venv(venv)
        # Project mtime is NOW — not old enough

        result = VenvScanner(home=tmp_path, unused_days=60).scan()
        assert result.count == 0
