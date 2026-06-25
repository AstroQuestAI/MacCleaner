"""Main MacCleaner panel — tabbed: Clean | Storage | Settings."""
import shutil

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath, QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ...config import Settings
from ...models.category import Category
from ...models.scan_result import CategoryResult, ScanReport
from ..formatting import fmt_size
from .settings_panel import SettingsPanel
from .storage_panel import StorageView

CATEGORY_ICONS = {
    Category.USER_CACHES:         ("🗂️",  "App data caches"),
    Category.SYSTEM_LOGS:         ("📋",  "System & app logs"),
    Category.TEMP_FILES:          ("🌡️",  "Temporary files"),
    Category.BROWSER_CACHES:      ("🌐",  "Browser caches"),
    Category.XCODE_ARTIFACTS:     ("🔨",  "DerivedData & archives"),
    Category.TRASH:               ("🗑️",  "Trash contents"),
    Category.MAIL_DOWNLOADS:      ("📩",  "Mail attachments"),
    Category.NODE_CACHE:          ("📦",  "npm / yarn / pnpm / bun"),
    Category.PYTHON_CACHE:        ("🐍",  "pip / poetry / uv / __pycache__"),
    Category.DOCKER:              ("🐳",  "Dangling images & build cache"),
    Category.BUILD_CACHE:         ("⚙️",  "Gradle / Maven / Cargo / Go"),
    Category.UNUSED_VENVS:        ("🔬",  "Unused virtual environments"),
    Category.HOMEBREW_CACHE:      ("🍺",  "Homebrew downloads & bottles"),
    Category.UNUSED_NODE_MODULES: ("📁",  "node_modules not used in 30+ days"),
}


# ── Category row ───────────────────────────────────────────────────────────

class CategoryRowWidget(QWidget):
    checked_changed = Signal()

    def __init__(self, category: Category, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.category = category
        self.setObjectName("CategoryRow")
        self._result: CategoryResult | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        self._checkbox = QCheckBox()
        self._checkbox.setChecked(False)
        self._checkbox.setEnabled(False)
        self._checkbox.stateChanged.connect(lambda _: self.checked_changed.emit())
        layout.addWidget(self._checkbox)

        icon_label = QLabel(CATEGORY_ICONS[self.category][0])
        icon_label.setObjectName("CatIcon")
        icon_label.setFixedWidth(28)
        layout.addWidget(icon_label)

        text_col = QVBoxLayout()
        text_col.setSpacing(1)
        name = QLabel(self.category.value)
        name.setObjectName("CatName")
        desc = QLabel(CATEGORY_ICONS[self.category][1])
        desc.setObjectName("CatDesc")
        text_col.addWidget(name)
        text_col.addWidget(desc)
        layout.addLayout(text_col, stretch=1)

        self._size_label = QLabel("—")
        self._size_label.setObjectName("CatSizeClean")
        layout.addWidget(self._size_label)

    def apply_result(self, result: CategoryResult) -> None:
        self._result = result
        has_files = result.count > 0
        self._checkbox.setEnabled(has_files)
        self._checkbox.setChecked(has_files)
        if has_files:
            self._size_label.setObjectName("CatSize")
            self._size_label.setText(fmt_size(result.total_size))
        else:
            self._size_label.setObjectName("CatSizeClean")
            self._size_label.setText("Clean ✓" if result.error is None else "—")
        self._size_label.style().unpolish(self._size_label)
        self._size_label.style().polish(self._size_label)

    def mark_cleaned(self) -> None:
        self._checkbox.setChecked(False)
        self._checkbox.setEnabled(False)
        self._size_label.setObjectName("CatSizeClean")
        self._size_label.setText("Cleaned ✓")
        self._size_label.style().unpolish(self._size_label)
        self._size_label.style().polish(self._size_label)

    @property
    def is_checked(self) -> bool:
        return self._checkbox.isChecked()

    @property
    def selected_category(self) -> Category | None:
        return self.category if self.is_checked else None


# ── Disk bar ───────────────────────────────────────────────────────────────

class DiskBar(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 8)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        label = QLabel("Storage")
        label.setObjectName("DiskLabel")
        self._free_label = QLabel("Scanning…")
        self._free_label.setObjectName("DiskFreeLabel")
        top_row.addWidget(label)
        top_row.addStretch()
        top_row.addWidget(self._free_label)
        layout.addLayout(top_row)

        self._bar = QProgressBar()
        self._bar.setObjectName("DiskBar")
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        self._bar.setFixedHeight(6)
        layout.addWidget(self._bar)
        self.refresh()

    def refresh(self) -> None:
        try:
            usage = shutil.disk_usage("/")
            pct = int(usage.used / usage.total * 100)
            self._free_label.setText(f"{fmt_size(usage.free)} free of {fmt_size(usage.total)}")
            self._bar.setValue(pct)
            name = "DiskBarDanger" if pct > 85 else ("DiskBarWarning" if pct > 70 else "DiskBar")
            self._bar.setObjectName(name)
            self._bar.style().unpolish(self._bar)
            self._bar.style().polish(self._bar)
        except Exception:
            self._free_label.setText("—")


# ── Main window ────────────────────────────────────────────────────────────

class MainWindow(QWidget):
    scan_requested = Signal()
    clean_requested = Signal(list)
    quit_requested = Signal()
    panel_close_requested = Signal()          # user clicked ✕ — hide panel
    panel_hidden = Signal()                   # window was hidden for any reason
    storage_scan_requested = Signal()         # storage tab needs a scan
    storage_delete_requested = Signal(list)   # list[Path] to move to trash
    settings_saved = Signal(object)           # Settings instance after save

    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(360)

        self._settings = settings or Settings()
        self._report: ScanReport | None = None
        self._row_widgets: dict[Category, CategoryRowWidget] = {}
        self._storage_ever_scanned = False
        self._build_ui()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # NSPanel (Qt Tool window) hides when the app deactivates by default.
        # Disable that so the panel stays visible when another app takes focus.
        QTimer.singleShot(50, self._fix_panel_hide)

    def hideEvent(self, event) -> None:
        super().hideEvent(event)
        # Notify app.py so it can re-show the panel if the hide wasn't user-requested.
        self.panel_hidden.emit()

    def _fix_panel_hide(self) -> None:
        try:
            import objc
            from ctypes import c_void_p
            from AppKit import NSFloatingWindowLevel
            view = objc.objc_object(c_void_p=int(self.winId()))
            win = view.window()
            win.setHidesOnDeactivate_(False)
            win.setLevel_(NSFloatingWindowLevel)
            win.orderFrontRegardless()
        except Exception:
            pass

    # ── Build ──────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        panel = QWidget()
        panel.setObjectName("MainPanel")
        outer.addWidget(panel)

        root = QVBoxLayout(panel)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())
        root.addWidget(self._build_tab_bar())

        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_clean_page())    # index 0
        self._stack.addWidget(self._build_storage_page())  # index 1
        self._stack.addWidget(self._build_settings_page()) # index 2
        root.addWidget(self._stack)

    def _build_header(self) -> QWidget:
        w = QWidget()
        w.setObjectName("Header")
        w.setFixedHeight(48)
        h = QHBoxLayout(w)
        h.setContentsMargins(16, 0, 12, 0)

        icon = QLabel("🧹")
        icon.setFixedWidth(24)
        h.addWidget(icon)

        title = QLabel("MacCleaner")
        title.setObjectName("AppTitle")
        h.addWidget(title)
        h.addStretch()

        quit_btn = QPushButton("⏻")
        quit_btn.setObjectName("CloseBtn")
        quit_btn.setFixedSize(28, 28)
        quit_btn.setToolTip("Quit MacCleaner")
        quit_btn.clicked.connect(self.quit_requested)
        h.addWidget(quit_btn)

        close_btn = QPushButton("✕")
        close_btn.setObjectName("CloseBtn")
        close_btn.setFixedSize(28, 28)
        close_btn.setToolTip("Hide panel")
        close_btn.clicked.connect(self.panel_close_requested)
        h.addWidget(close_btn)
        return w

    def _build_tab_bar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("TabBar")
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        self._tab_clean = QPushButton("🧹  Clean")
        self._tab_clean.setObjectName("TabBtn")
        self._tab_clean.clicked.connect(lambda: self._switch_tab(0))
        h.addWidget(self._tab_clean, stretch=1)

        self._tab_storage = QPushButton("📊  Storage")
        self._tab_storage.setObjectName("TabBtn")
        self._tab_storage.clicked.connect(lambda: self._switch_tab(1))
        h.addWidget(self._tab_storage, stretch=1)

        self._tab_settings = QPushButton("⚙️")
        self._tab_settings.setObjectName("TabBtn")
        self._tab_settings.setFixedWidth(44)
        self._tab_settings.setToolTip("Settings")
        self._tab_settings.clicked.connect(lambda: self._switch_tab(2))
        h.addWidget(self._tab_settings)

        self._set_tab_active(0)
        return w

    def _switch_tab(self, index: int) -> None:
        self._stack.setCurrentIndex(index)
        self._set_tab_active(index)
        if index == 1 and not self._storage_ever_scanned:
            self._storage_ever_scanned = True
            self.storage_scan_requested.emit()

    def _set_tab_active(self, index: int) -> None:
        for i, btn in enumerate([self._tab_clean, self._tab_storage, self._tab_settings]):
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ── Clean page ─────────────────────────────────────────────────────────

    def _build_clean_page(self) -> QWidget:
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        v.addWidget(self._build_disk_bar_widget())
        v.addWidget(self._build_divider())
        v.addWidget(self._build_category_scroll())
        v.addWidget(self._build_divider())
        v.addWidget(self._build_total_row())
        v.addWidget(self._build_button_row())
        v.addWidget(self._build_status_bar())
        return page

    def _build_disk_bar_widget(self) -> QWidget:
        self._disk_bar = DiskBar()
        return self._disk_bar

    def _build_divider(self) -> QWidget:
        d = QWidget()
        d.setObjectName("Divider")
        d.setFixedHeight(1)
        return d

    def _build_category_scroll(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setObjectName("CategoryScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container.setObjectName("CategoryScroll")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        for cat in Category:
            row = CategoryRowWidget(cat)
            row.checked_changed.connect(self._update_total)
            self._row_widgets[cat] = row
            layout.addWidget(row)

        scroll.setWidget(container)
        scroll.setFixedHeight(340)
        return scroll

    def _build_total_row(self) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(16, 10, 16, 4)
        lbl = QLabel("Selected to clean")
        lbl.setObjectName("TotalLabel")
        h.addWidget(lbl)
        h.addStretch()
        self._total_label = QLabel("—")
        self._total_label.setObjectName("TotalSize")
        h.addWidget(self._total_label)
        return w

    def _build_button_row(self) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(16, 6, 16, 10)
        h.setSpacing(10)
        self._scan_btn = QPushButton("🔍  Scan")
        self._scan_btn.setObjectName("ScanBtn")
        self._scan_btn.clicked.connect(self._on_scan_clicked)
        h.addWidget(self._scan_btn)
        self._clean_btn = QPushButton("✨  Clean Selected")
        self._clean_btn.setObjectName("CleanBtn")
        self._clean_btn.setEnabled(False)
        self._clean_btn.clicked.connect(self._on_clean_clicked)
        h.addWidget(self._clean_btn)
        return w

    def _build_status_bar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("StatusBar")
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 6, 16, 10)
        v.setSpacing(4)
        row = QHBoxLayout()
        self._status_dot = QLabel("●")
        self._status_dot.setObjectName("StatusDot")
        self._status_dot.setStyleSheet("color: #10b981;")
        self._status_text = QLabel("Ready — click Scan to start")
        self._status_text.setObjectName("StatusText")
        row.addWidget(self._status_dot)
        row.addSpacing(4)
        row.addWidget(self._status_text)
        row.addStretch()
        v.addLayout(row)
        self._status_progress = QProgressBar()
        self._status_progress.setObjectName("StatusProgress")
        self._status_progress.setRange(0, 100)
        self._status_progress.setValue(0)
        self._status_progress.setFixedHeight(4)
        self._status_progress.setTextVisible(False)
        self._status_progress.hide()
        v.addWidget(self._status_progress)
        return w

    # ── Storage page ───────────────────────────────────────────────────────

    def _build_storage_page(self) -> QWidget:
        self._storage_view = StorageView()
        self._storage_view.rescan_requested.connect(self.storage_scan_requested)
        self._storage_view.delete_requested.connect(self.storage_delete_requested)
        return self._storage_view

    # ── Settings page ──────────────────────────────────────────────────────

    def _build_settings_page(self) -> QWidget:
        self._settings_panel = SettingsPanel(self._settings)
        self._settings_panel.settings_saved.connect(self.settings_saved)
        return self._settings_panel

    # ── Slots ──────────────────────────────────────────────────────────────

    def _on_scan_clicked(self) -> None:
        self._disk_bar.refresh()
        self.scan_requested.emit()

    def _on_clean_clicked(self) -> None:
        selected = [cat for cat, row in self._row_widgets.items() if row.is_checked]
        self.clean_requested.emit(selected or [])

    def _update_total(self) -> None:
        if self._report is None:
            return
        total = 0
        any_checked = False
        for cat, row in self._row_widgets.items():
            if row.is_checked:
                any_checked = True
                result = self._report.result_for(cat)
                if result:
                    total += result.total_size
        self._total_label.setText(fmt_size(total) if any_checked else "—")
        self._clean_btn.setEnabled(any_checked)

    # ── Public API (clean tab) ─────────────────────────────────────────────

    def on_scan_started(self) -> None:
        self._scan_btn.setEnabled(False)
        self._clean_btn.setEnabled(False)
        self._total_label.setText("—")
        self._status_dot.setStyleSheet("color: #f59e0b;")
        self._status_text.setText("Scanning…")
        self._status_progress.setRange(0, 0)
        self._status_progress.show()

    def on_scan_progress(self, category_name: str, done: int, total: int) -> None:
        self._status_text.setText(f"Scanning {category_name}…")
        self._status_progress.setRange(0, total)
        self._status_progress.setValue(done)

    def on_scan_finished(self, report: ScanReport) -> None:
        self._report = report
        for cat, row in self._row_widgets.items():
            result = report.result_for(cat)
            if result:
                row.apply_result(result)
        self._scan_btn.setEnabled(True)
        self._update_total()
        self._status_dot.setStyleSheet("color: #7c3aed;")
        self._status_text.setText(f"Found {fmt_size(report.total_size)} to clean")
        self._status_progress.hide()

    def on_scan_error(self, msg: str) -> None:
        self._scan_btn.setEnabled(True)
        self._status_dot.setStyleSheet("color: #ef4444;")
        self._status_text.setText(f"Scan error: {msg}")
        self._status_progress.hide()

    def on_clean_started(self) -> None:
        self._scan_btn.setEnabled(False)
        self._clean_btn.setEnabled(False)
        self._status_dot.setStyleSheet("color: #f59e0b;")
        self._status_text.setText("Cleaning…")
        self._status_progress.setRange(0, 0)
        self._status_progress.show()

    def on_clean_progress(self, category_name: str, done: int, total: int) -> None:
        self._status_text.setText(f"Cleaning {category_name}…")
        self._status_progress.setRange(0, total)
        self._status_progress.setValue(done)

    def on_clean_finished(self, freed: dict) -> None:
        total_freed = sum(freed.values())
        for cat in freed:
            if cat in self._row_widgets:
                self._row_widgets[cat].mark_cleaned()
        self._scan_btn.setEnabled(True)
        self._clean_btn.setEnabled(False)
        self._total_label.setText("—")
        self._status_dot.setStyleSheet("color: #10b981;")
        self._status_text.setText(f"Freed {fmt_size(total_freed)} — your Mac is clean!")
        self._status_progress.hide()
        self._disk_bar.refresh()
        self._report = None

    def on_clean_error(self, msg: str) -> None:
        self._scan_btn.setEnabled(True)
        self._status_dot.setStyleSheet("color: #ef4444;")
        self._status_text.setText(f"Clean error: {msg}")
        self._status_progress.hide()

    # ── Public API (storage tab) ───────────────────────────────────────────

    def on_storage_scan_started(self) -> None:
        self._storage_view.show_scanning()

    def on_storage_scan_progress(self, msg: str) -> None:
        self._storage_view.show_progress(msg)

    def on_storage_scan_finished(self, folders: list) -> None:
        self._storage_view.show_results(folders)

    def on_storage_delete_started(self) -> None:
        self._storage_view.show_deleting()

    def on_storage_delete_progress(self, msg: str) -> None:
        self._storage_view.show_progress(msg)

    def on_storage_delete_finished(self, count: int) -> None:
        self._storage_view.show_progress(f"Moved {count} folder{'s' if count != 1 else ''} to Trash — rescanning…")
        # Caller (app.py) triggers the rescan after this

