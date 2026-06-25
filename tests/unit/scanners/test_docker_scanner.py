from unittest.mock import patch, MagicMock
from maccleaner.scanners.docker_scanner import DockerScanner, DOCKER_SENTINEL, _parse_size
from maccleaner.models.category import Category


class TestParseSize:
    def test_bytes(self):     assert _parse_size("512B")   == 512
    def test_kb(self):        assert _parse_size("2KB")    == 2048
    def test_mb(self):        assert _parse_size("1.5MB")  == int(1.5 * 1024**2)
    def test_gb(self):        assert _parse_size("2.5GB")  == int(2.5 * 1024**3)
    def test_with_pct(self):  assert _parse_size("3.2GB (72%)") == int(3.2 * 1024**3)
    def test_no_match(self):  assert _parse_size("N/A") == 0


class TestDockerScanner:
    def test_given_docker_not_installed_when_scan_then_empty(self):
        with patch("shutil.which", return_value=None):
            result = DockerScanner().scan()
        assert result.count == 0
        assert result.category == Category.DOCKER

    def test_given_docker_daemon_not_running_when_scan_then_empty(self):
        with patch("shutil.which", return_value="/usr/bin/docker"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1)
                result = DockerScanner().scan()
        assert result.count == 0

    def test_given_docker_running_with_reclaimable_when_scan_then_found(self):
        df_output = (
            "TYPE            TOTAL  ACTIVE  SIZE      RECLAIMABLE\n"
            "Images          10     3       5.2GB     3.1GB (59%)\n"
            "Containers      5      1       200MB     180MB (90%)\n"
            "Local Volumes   8      3       12GB      0B\n"
            "Build Cache     45     0       2.3GB     2.3GB\n"
        )
        with patch("shutil.which", return_value="/usr/bin/docker"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0),               # docker info
                    MagicMock(returncode=0, stdout=df_output),  # docker system df
                ]
                result = DockerScanner().scan()

        assert result.count == 1
        assert result.entries[0].path == DOCKER_SENTINEL
        assert result.total_size > 0

    def test_given_no_reclaimable_space_when_scan_then_empty(self):
        df_output = (
            "TYPE            TOTAL  ACTIVE  SIZE   RECLAIMABLE\n"
            "Images          0      0       0B     0B\n"
        )
        with patch("shutil.which", return_value="/usr/bin/docker"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0),
                    MagicMock(returncode=0, stdout=df_output),
                ]
                result = DockerScanner().scan()
        assert result.count == 0
