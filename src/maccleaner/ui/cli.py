"""CLI entry point."""
import argparse
import shutil
import sys

import psutil
from rich.console import Console

from ..models.category import Category
from ..services.cleaner_service import CleanerService
from .dashboard import (
    console,
    make_scan_progress,
    print_banner,
    print_clean_summary,
    print_report,
    prompt_category_selection,
)
from .formatting import fmt_size


def _disk_free() -> int:
    return shutil.disk_usage("/").free


def _print_disk_usage() -> None:
    usage = shutil.disk_usage("/")
    pct = usage.used / usage.total * 100
    color = "red" if pct > 85 else ("yellow" if pct > 70 else "green")
    console.print(
        f"  Disk: [{color}]{fmt_size(usage.used)} used[/{color}] of {fmt_size(usage.total)}"
        f"  •  [bold]{fmt_size(usage.free)} free[/bold]"
    )
    console.print()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="maccleaner",
        description="macOS storage cleaner — removes clutter, frees space",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="scan only; show what would be deleted without deleting anything",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="skip confirmation prompts",
    )
    parser.add_argument(
        "--category", "-c",
        choices=[c.value for c in Category],
        action="append",
        dest="categories",
        metavar="CATEGORY",
        help="clean only the specified categories (repeatable)",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    service = CleanerService()

    print_banner()
    _print_disk_usage()

    # --- Scan phase ---
    report = None
    with make_scan_progress() as progress:
        task = progress.add_task("Scanning…", total=7)

        def on_scan_progress(cat: Category, i: int, total: int) -> None:
            progress.update(task, description=f"Scanning [cyan]{cat.value}[/cyan]…", completed=i + 1)

        report = service.scan(on_progress=on_scan_progress)

    print_report(report)

    if report.total_size == 0:
        console.print("[bold green]Your Mac is already clean![/bold green]")
        return 0

    # --- Category selection ---
    if args.categories:
        cat_map = {c.value: c for c in Category}
        selected_cats = [cat_map[v] for v in args.categories if v in cat_map]
    elif args.yes:
        selected_cats = None  # all
    else:
        selected_cats = prompt_category_selection(report)

    if selected_cats is not None and len(selected_cats) == 0:
        console.print("[dim]Nothing selected. Exiting.[/dim]")
        return 0

    # --- Confirmation ---
    if args.dry_run:
        console.print("[bold yellow]Dry run — no files will be deleted.[/bold yellow]")
    elif not args.yes:
        confirmed = console.input(
            "[bold red]Delete selected files? Files go to Trash (recoverable). [Y/n]: [/bold red]"
        ).strip().lower()
        if confirmed not in ("", "y", "yes"):
            console.print("[dim]Aborted.[/dim]")
            return 0

    # --- Clean phase ---
    free_before = _disk_free()

    with make_scan_progress() as progress:
        task = progress.add_task("Cleaning…", total=7)

        def on_clean_progress(cat: Category, i: int, total: int) -> None:
            progress.update(task, description=f"Cleaning [cyan]{cat.value}[/cyan]…", completed=i + 1)

        freed = service.clean(
            report,
            categories=selected_cats,
            dry_run=args.dry_run,
            on_progress=on_clean_progress,
        )

    print_clean_summary(freed)

    if not args.dry_run:
        free_after = _disk_free()
        actual = max(0, free_after - free_before)
        console.print(
            f"[bold green]Done![/bold green]  "
            f"Disk space freed: [bold bright_green]{fmt_size(actual)}[/bold bright_green]\n"
        )
    else:
        console.print(
            f"[bold yellow]Dry run complete.[/bold yellow]  "
            f"Would free approximately [bold]{fmt_size(sum(freed.values()))}[/bold]\n"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
