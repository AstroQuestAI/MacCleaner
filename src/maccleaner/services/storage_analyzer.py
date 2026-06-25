"""Storage analyzer — finds the largest folders on disk using `du`."""
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

_TOP_N = 20

_EXTRA_ROOTS = [Path("/Applications")]

# Directories to never recurse into when hunting for node_modules
_SKIP_DIRS = {".Trash", "Library", ".git"}


@dataclass(frozen=True)
class FolderInfo:
    path: Path
    size: int          # bytes
    is_node_modules: bool = False


def _find_node_modules(
    home: Path,
    progress: Callable[[str], None] | None = None,
) -> list[FolderInfo]:
    """Return FolderInfo for every node_modules directory under *home*."""
    if progress:
        progress("Scanning for node_modules …")

    try:
        # Find all node_modules dirs without descending into them
        find = subprocess.run(
            ["find", str(home), "-name", "node_modules", "-type", "d", "-prune"],
            capture_output=True, text=True, timeout=60,
        )
    except Exception:
        return []

    paths = [p.strip() for p in find.stdout.splitlines() if p.strip()]
    if not paths:
        return []

    if progress:
        progress(f"Measuring {len(paths)} node_modules folder{'s' if len(paths) != 1 else ''} …")

    results: list[FolderInfo] = []
    # Measure in one du call (xargs splits if needed)
    try:
        du = subprocess.run(
            ["du", "-sk"] + paths,
            capture_output=True, text=True, timeout=120,
        )
        for line in du.stdout.splitlines():
            if "\t" not in line:
                continue
            kb_str, path_str = line.split("\t", 1)
            try:
                results.append(FolderInfo(
                    path=Path(path_str.strip()),
                    size=int(kb_str.strip()) * 1024,
                    is_node_modules=True,
                ))
            except ValueError:
                pass
    except Exception:
        pass

    return results


def scan_top_folders(
    home: Path | None = None,
    progress: Callable[[str], None] | None = None,
    top_n: int = _TOP_N,
) -> list[FolderInfo]:
    """Return up to *top_n* folders sorted by size descending.

    Includes both top-level home directories and all node_modules
    directories found anywhere under home.
    """
    home = home or Path.home()
    items: list[FolderInfo] = []
    seen: set[Path] = set()

    if progress:
        progress(f"Scanning {home} …")

    # Direct children of home
    try:
        proc = subprocess.run(
            ["du", "-d", "1", "-k", str(home)],
            capture_output=True, text=True, timeout=120,
        )
        for line in proc.stdout.splitlines():
            if "\t" not in line:
                continue
            kb_str, path_str = line.split("\t", 1)
            path = Path(path_str.strip())
            if path == home:
                continue
            try:
                info = FolderInfo(path=path, size=int(kb_str.strip()) * 1024)
                items.append(info)
                seen.add(path)
            except ValueError:
                pass
    except Exception:
        pass

    # /Applications total
    for root in _EXTRA_ROOTS:
        if not root.exists() or root in seen:
            continue
        if progress:
            progress(f"Scanning {root} …")
        try:
            proc = subprocess.run(
                ["du", "-d", "0", "-k", str(root)],
                capture_output=True, text=True, timeout=60,
            )
            line = proc.stdout.strip()
            if "\t" in line:
                kb_str, _ = line.split("\t", 1)
                items.append(FolderInfo(path=root, size=int(kb_str.strip()) * 1024))
                seen.add(root)
        except Exception:
            pass

    # ALL node_modules anywhere under home (not subject to top_n cap)
    nm_items: list[FolderInfo] = []
    for nm in _find_node_modules(home, progress):
        if nm.path not in seen:
            nm_items.append(nm)
            seen.add(nm.path)

    # Top-N of regular folders; node_modules listed separately
    items.sort(key=lambda f: f.size, reverse=True)
    nm_items.sort(key=lambda f: f.size, reverse=True)

    return nm_items + items[:top_n]
