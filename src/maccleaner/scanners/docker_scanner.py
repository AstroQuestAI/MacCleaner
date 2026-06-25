"""Docker scanner — dangling images, stopped containers, build cache.

Uses `docker system df` to measure reclaimable space and
`docker system prune -f` to free it (safe: no volumes touched).
"""
import re
import shutil
import subprocess
from pathlib import Path

from ..models.category import Category
from ..models.scan_result import CategoryResult, FileEntry
from .base import BaseScanner

# Sentinel path — signals CleanerService to run `docker system prune` instead
# of a regular file deletion.
DOCKER_SENTINEL = Path("__docker_prune__")

_SIZE_RE = re.compile(r"([\d.]+)\s*(B|KB|MB|GB|TB)", re.IGNORECASE)

_UNITS = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}


def _parse_size(text: str) -> int:
    m = _SIZE_RE.search(text)
    if not m:
        return 0
    value, unit = float(m.group(1)), m.group(2).upper()
    return int(value * _UNITS.get(unit, 1))


class DockerScanner(BaseScanner):
    category = Category.DOCKER

    def _find_paths(self) -> list[Path]:
        return []  # unused — scan() is overridden

    def scan(self) -> CategoryResult:
        result = CategoryResult(category=self.category)

        if not shutil.which("docker"):
            return result  # Docker not installed

        try:
            info = subprocess.run(
                ["docker", "info"],
                capture_output=True, timeout=5,
            )
            if info.returncode != 0:
                return result  # Docker daemon not running
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return result

        try:
            df = subprocess.run(
                ["docker", "system", "df"],
                capture_output=True, text=True, timeout=15,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            result.error = str(exc)
            return result

        reclaimable = 0
        for line in df.stdout.splitlines()[1:]:  # skip header
            # Each row: TYPE  TOTAL  ACTIVE  SIZE  RECLAIMABLE
            # RECLAIMABLE may be "X.XGB (N%)" or just "X.XGB"
            parts = line.split()
            if len(parts) >= 5:
                reclaimable += _parse_size(parts[4])

        if reclaimable > 0:
            result.entries.append(FileEntry(path=DOCKER_SENTINEL, size=reclaimable))

        return result
