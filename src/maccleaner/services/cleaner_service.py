"""CleanerService — orchestrates scan and clean lifecycle."""
import shutil
import subprocess
from pathlib import Path
from typing import Callable

import send2trash

from ..models.category import Category
from ..models.scan_result import CategoryResult, ScanReport
from ..scanners.base import BaseScanner
from ..scanners.browser_scanner import BrowserCacheScanner
from ..scanners.build_cache_scanner import BuildCacheScanner
from ..scanners.cache_scanner import UserCacheScanner
from ..scanners.docker_scanner import DOCKER_SENTINEL, DockerScanner
from ..scanners.log_scanner import LogScanner
from ..scanners.mail_scanner import MailDownloadsScanner
from ..scanners.node_scanner import NodeCacheScanner
from ..scanners.python_cache_scanner import PythonCacheScanner
from ..scanners.temp_scanner import TempScanner
from ..scanners.trash_scanner import TrashScanner
from ..scanners.homebrew_scanner import HomebrewCacheScanner
from ..scanners.node_modules_scanner import NodeModulesScanner
from ..scanners.venv_scanner import VenvScanner
from ..scanners.xcode_scanner import XcodeScanner

ProgressCallback = Callable[[Category, int, int], None]


class CleanerService:
    """Orchestrates all scanners and drives the clean operation."""

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()
        self._scanners: list[BaseScanner] = [
            UserCacheScanner(self._home),
            LogScanner(self._home),
            TempScanner(),
            BrowserCacheScanner(self._home),
            XcodeScanner(self._home),
            TrashScanner(self._home),
            MailDownloadsScanner(self._home),
            NodeCacheScanner(self._home),
            PythonCacheScanner(self._home),
            DockerScanner(),
            BuildCacheScanner(self._home),
            VenvScanner(self._home),
            HomebrewCacheScanner(self._home),
            NodeModulesScanner(self._home),
        ]

    def scan(self, on_progress: ProgressCallback | None = None) -> ScanReport:
        report = ScanReport()
        total = len(self._scanners)
        for i, scanner in enumerate(self._scanners):
            if on_progress:
                on_progress(scanner.category, i, total)
            result = scanner.scan()
            report.results.append(result)
        return report

    def clean(
        self,
        report: ScanReport,
        categories: list[Category] | None = None,
        dry_run: bool = False,
        on_progress: ProgressCallback | None = None,
    ) -> dict[Category, int]:
        freed: dict[Category, int] = {}
        selected_results = [
            r for r in report.results
            if categories is None or r.category in categories
        ]
        total = len(selected_results)

        for i, result in enumerate(selected_results):
            if on_progress:
                on_progress(result.category, i, total)
            bytes_freed = 0
            for entry in result.entries:
                # Docker sentinel — run prune instead of file deletion
                if entry.path == DOCKER_SENTINEL:
                    if not dry_run:
                        try:
                            subprocess.run(
                                ["docker", "system", "prune", "-f"],
                                capture_output=True, timeout=120,
                            )
                        except (subprocess.TimeoutExpired, FileNotFoundError):
                            pass
                    bytes_freed += entry.size
                    continue

                if not entry.path.exists():
                    continue
                size = entry.size
                if not dry_run:
                    try:
                        self._delete(entry.path, result.category)
                        bytes_freed += size
                    except (PermissionError, OSError):
                        pass
                else:
                    bytes_freed += size
            freed[result.category] = bytes_freed

        return freed

    @staticmethod
    def _delete(path: Path, category: Category) -> None:
        if category == Category.TRASH:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
        else:
            send2trash.send2trash(str(path))
