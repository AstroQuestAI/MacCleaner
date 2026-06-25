"""Unit tests for TrashScanner."""
from pathlib import Path

from maccleaner.scanners.trash_scanner import TrashScanner
from maccleaner.models.category import Category


class TestTrashScanner:
    def test_given_no_trash_when_scan_then_empty(self, tmp_path: Path) -> None:
        scanner = TrashScanner(home=tmp_path)
        result = scanner.scan()
        assert result.count == 0

    def test_given_trash_with_files_when_scan_then_found(self, tmp_path: Path) -> None:
        trash = tmp_path / ".Trash"
        trash.mkdir()
        (trash / "old_photo.jpg").write_bytes(b"img" * 1000)
        (trash / "notes.txt").write_bytes(b"note" * 100)

        scanner = TrashScanner(home=tmp_path)
        result = scanner.scan()

        assert result.count == 2
        assert result.category == Category.TRASH

    def test_given_ds_store_in_trash_when_scan_then_skipped(self, tmp_path: Path) -> None:
        trash = tmp_path / ".Trash"
        trash.mkdir()
        (trash / ".DS_Store").write_bytes(b"ds")
        (trash / "real_file.txt").write_bytes(b"content")

        scanner = TrashScanner(home=tmp_path)
        result = scanner.scan()

        names = {e.path.name for e in result.entries}
        assert ".DS_Store" not in names
        assert "real_file.txt" in names
