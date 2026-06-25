"""Rich terminal dashboard for scan results."""
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

from ..models.category import Category
from ..models.scan_result import CategoryResult, ScanReport
from .formatting import fmt_size

console = Console()

CATEGORY_ICONS = {
    Category.USER_CACHES: "󰃨",
    Category.SYSTEM_LOGS: "",
    Category.TEMP_FILES: "󰡕",
    Category.BROWSER_CACHES: "",
    Category.XCODE_ARTIFACTS: "",
    Category.TRASH: "󰩺",
    Category.MAIL_DOWNLOADS: "",
}

CATEGORY_COLORS = {
    Category.USER_CACHES: "cyan",
    Category.SYSTEM_LOGS: "yellow",
    Category.TEMP_FILES: "magenta",
    Category.BROWSER_CACHES: "blue",
    Category.XCODE_ARTIFACTS: "bright_blue",
    Category.TRASH: "red",
    Category.MAIL_DOWNLOADS: "green",
}


def print_banner() -> None:
    console.print(Panel.fit(
        "[bold white]MacCleaner[/bold white]\n"
        "[dim]Storage cleaner for macOS — safe, fast, recoverable[/dim]",
        border_style="bright_cyan",
        padding=(1, 4),
    ))


def make_scan_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
        transient=True,
    )


def print_report(report: ScanReport) -> None:
    table = Table(
        title="[bold]Scan Results[/bold]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold bright_white",
        border_style="bright_cyan",
        expand=True,
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Category", style="bold")
    table.add_column("Files / Dirs", justify="right")
    table.add_column("Size", justify="right", style="bold")
    table.add_column("Status", justify="center")

    for i, result in enumerate(report.results, 1):
        color = CATEGORY_COLORS.get(result.category, "white")
        status = "[red]error[/red]" if result.error else (
            "[green]found[/green]" if result.count > 0 else "[dim]clean[/dim]"
        )
        table.add_row(
            str(i),
            f"[{color}]{result.category.value}[/{color}]",
            str(result.count),
            fmt_size(result.total_size),
            status,
        )

    table.add_section()
    table.add_row(
        "",
        "[bold]TOTAL[/bold]",
        f"[bold]{report.total_count}[/bold]",
        f"[bold bright_green]{fmt_size(report.total_size)}[/bold bright_green]",
        "",
    )

    console.print()
    console.print(table)
    console.print()


def print_clean_summary(freed: dict[Category, int]) -> None:
    total = sum(freed.values())
    table = Table(
        title="[bold]Cleaned[/bold]",
        box=box.SIMPLE,
        header_style="bold",
        border_style="green",
    )
    table.add_column("Category")
    table.add_column("Freed", justify="right", style="bold green")

    for cat, size in freed.items():
        color = CATEGORY_COLORS.get(cat, "white")
        table.add_row(f"[{color}]{cat.value}[/{color}]", fmt_size(size))

    table.add_section()
    table.add_row("[bold]Total freed[/bold]", f"[bold bright_green]{fmt_size(total)}[/bold bright_green]")

    console.print()
    console.print(table)
    console.print()


def prompt_category_selection(report: ScanReport) -> list[Category] | None:
    """Interactive multi-select for categories. Returns None if user selects All."""
    non_empty = [r for r in report.results if r.count > 0]
    if not non_empty:
        return []

    console.print("[bold]Select categories to clean[/bold] [dim](comma-separated numbers, or Enter for all):[/dim]")
    for i, result in enumerate(non_empty, 1):
        color = CATEGORY_COLORS.get(result.category, "white")
        console.print(
            f"  [dim]{i}.[/dim] [{color}]{result.category.value}[/{color}]"
            f"  [dim]{fmt_size(result.total_size)}[/dim]"
        )

    raw = console.input("\n[bold cyan]> [/bold cyan]").strip()
    if not raw:
        return None  # All

    selected: list[Category] = []
    for token in raw.split(","):
        token = token.strip()
        if token.isdigit():
            idx = int(token) - 1
            if 0 <= idx < len(non_empty):
                selected.append(non_empty[idx].category)
    return selected or None
