"""Build-tool cache scanner — Gradle, Maven, Cargo, Go, CocoaPods, Composer."""
from pathlib import Path

from ..models.category import Category
from .base import BaseScanner

_BUILD_CACHE_PATHS = [
    # Java / Android
    ".gradle/caches",
    ".gradle/wrapper/dists",
    ".m2/repository",
    # Rust
    ".cargo/registry/cache",
    ".cargo/registry/src",
    ".cargo/git/db",
    # Go
    ".cache/go-build",
    "go/pkg/mod/cache",
    # CocoaPods
    "Library/Caches/CocoaPods",
    # Ruby / Bundler
    ".gem/cache",
    ".bundle/cache",
    # PHP Composer
    ".composer/cache",
    # .NET NuGet
    ".nuget/packages",
    # SonarQube scanner
    ".sonar/cache",
    # Dart / Flutter
    ".pub-cache/hosted",
    # SwiftPM
    "Library/Developer/Xcode/DerivedData",  # already in xcode_scanner but also a build artifact
    ".swiftpm",
]


class BuildCacheScanner(BaseScanner):
    category = Category.BUILD_CACHE

    def __init__(self, home: Path | None = None) -> None:
        self._home = home or Path.home()

    def _find_paths(self) -> list[Path]:
        paths: list[Path] = []
        for rel in _BUILD_CACHE_PATHS:
            p = self._home / rel
            if p.exists():
                paths.append(p)
        return paths
