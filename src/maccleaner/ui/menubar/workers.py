"""Background QThread workers for scan, clean, and storage analysis."""
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from ...models.category import Category
from ...models.scan_result import ScanReport
from ...services.cleaner_service import CleanerService
from ...services.storage_analyzer import FolderInfo, scan_top_folders


class ScanWorker(QThread):
    progress = Signal(str, int, int)   # (category_name, done, total)
    finished = Signal(object)           # ScanReport
    error = Signal(str)

    def __init__(self, service: CleanerService) -> None:
        super().__init__()
        self._service = service

    def run(self) -> None:
        try:
            def on_progress(cat: Category, i: int, total: int) -> None:
                self.progress.emit(cat.value, i + 1, total)

            report = self._service.scan(on_progress=on_progress)
            self.finished.emit(report)
        except Exception as exc:
            self.error.emit(str(exc))


class CleanWorker(QThread):
    progress = Signal(str, int, int)           # (category_name, done, total)
    finished = Signal(dict)                     # {Category: bytes_freed}
    error = Signal(str)

    def __init__(
        self,
        service: CleanerService,
        report: ScanReport,
        categories: list[Category] | None,
    ) -> None:
        super().__init__()
        self._service = service
        self._report = report
        self._categories = categories

    def run(self) -> None:
        try:
            def on_progress(cat: Category, i: int, total: int) -> None:
                self.progress.emit(cat.value, i + 1, total)

            freed = self._service.clean(
                self._report,
                categories=self._categories,
                on_progress=on_progress,
            )
            self.finished.emit(freed)
        except Exception as exc:
            self.error.emit(str(exc))


class StorageScanWorker(QThread):
    progress = Signal(str)      # folder name currently being measured
    finished = Signal(list)     # list[FolderInfo]

    def run(self) -> None:
        results = scan_top_folders(progress=lambda msg: self.progress.emit(msg))
        self.finished.emit(results)


class StorageDeleteWorker(QThread):
    progress = Signal(str)   # name of folder being trashed
    finished = Signal(int)   # number of folders moved to trash

    def __init__(self, paths: list[Path]) -> None:
        super().__init__()
        self._paths = paths

    def run(self) -> None:
        import send2trash
        count = 0
        for path in self._paths:
            self.progress.emit(f"Trashing {path.name}…")
            try:
                send2trash.send2trash(str(path))
                count += 1
            except Exception:
                pass
        self.finished.emit(count)
