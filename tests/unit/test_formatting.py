"""Unit tests for size formatting."""
import pytest

from maccleaner.ui.formatting import fmt_size


class TestFmtSize:
    @pytest.mark.parametrize("size,expected", [
        (0, "0 B"),
        (512, "512 B"),
        (1023, "1023 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (1024 * 1024, "1.0 MB"),
        (int(1.5 * 1024 * 1024), "1.5 MB"),
        (1024 ** 3, "1.00 GB"),
        (int(2.5 * 1024 ** 3), "2.50 GB"),
    ])
    def test_given_size_bytes_when_fmt_then_correct_unit(self, size: int, expected: str) -> None:
        assert fmt_size(size) == expected
