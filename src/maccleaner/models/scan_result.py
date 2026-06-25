from dataclasses import dataclass, field
from pathlib import Path
from .category import Category


@dataclass
class FileEntry:
    path: Path
    size: int  # bytes

    @property
    def size_mb(self) -> float:
        return self.size / (1024 * 1024)


@dataclass
class CategoryResult:
    category: Category
    entries: list[FileEntry] = field(default_factory=list)
    error: str | None = None

    @property
    def total_size(self) -> int:
        return sum(e.size for e in self.entries)

    @property
    def total_size_mb(self) -> float:
        return self.total_size / (1024 * 1024)

    @property
    def count(self) -> int:
        return len(self.entries)


@dataclass
class ScanReport:
    results: list[CategoryResult] = field(default_factory=list)

    @property
    def total_size(self) -> int:
        return sum(r.total_size for r in self.results)

    @property
    def total_size_mb(self) -> float:
        return self.total_size / (1024 * 1024)

    @property
    def total_size_gb(self) -> float:
        return self.total_size / (1024 ** 3)

    @property
    def total_count(self) -> int:
        return sum(r.count for r in self.results)

    def result_for(self, category: Category) -> CategoryResult | None:
        return next((r for r in self.results if r.category == category), None)
