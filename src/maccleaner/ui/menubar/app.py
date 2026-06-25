"""MacCleaner — pure background agent.

Runs silently as a macOS Launch Agent. No Dock icon. Status bar shows
free disk space, a junk-found indicator after auto-scans, and a storage
warning when the disk reaches the configured thresholds.
"""
import shutil
import sys

from PySide6.QtCore import QRect, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QFontMetrics, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from ...config import Settings
from ...models.scan_result import ScanReport
from ...services.cleaner_service import CleanerService
from .main_window import MainWindow
from .style import STYLESHEETS
from .workers import CleanWorker, ScanWorker, StorageScanWorker, StorageDeleteWorker

_ICON_H       = 22
_DISK_POLL_MS = 60_000
_JUNK_REVERT_MS = 30_000

_AMBER = QColor(251, 191, 36)
_RED   = QColor(239,  68,  68)
_WHITE = QColor(255, 255, 255)


# ── Helpers ────────────────────────────────────────────────────────────────

def _hide_dock_icon() -> None:
    """Remove the app from the Dock and menu-bar app menu.
    Must be called AFTER QApplication() — Qt resets the policy on init.
    """
    try:
        from AppKit import NSApplication, NSApplicationActivationPolicyAccessory
        NSApplication.sharedApplication().setActivationPolicy_(
            NSApplicationActivationPolicyAccessory
        )
        return
    except Exception:
        pass
    try:
        import ctypes, ctypes.util
        objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library("objc"))
        objc.objc_getClass.restype = ctypes.c_void_p
        objc.sel_registerName.restype = ctypes.c_void_p
        objc.objc_msgSend.restype = ctypes.c_void_p
        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_long]
        NSApp = objc.objc_msgSend(
            objc.objc_getClass(b"NSApplication"),
            objc.sel_registerName(b"sharedApplication"),
            0,
        )
        objc.objc_msgSend(NSApp, objc.sel_registerName(b"setActivationPolicy:"), 1)
    except Exception:
        pass


def _disk_usage() -> tuple[float, int]:
    try:
        u = shutil.disk_usage("/")
        return (u.total - u.free) / u.total * 100, u.free
    except Exception:
        return 0.0, 0


def _fmt_size(n: int) -> str:
    if n >= 1024 ** 3:
        return f"{n / 1024**3:.1f} GB"
    if n >= 1024 ** 2:
        return f"{n / 1024**2:.0f} MB"
    return f"{n / 1024:.0f} KB"


def _make_status_icon(text: str, color: QColor = _WHITE) -> QIcon:
    font = QFont()
    font.setPixelSize(12)
    font.setBold(True)
    fm = QFontMetrics(font)
    w = fm.horizontalAdvance(text) + 8
    px = QPixmap(w, _ICON_H)
    px.fill(QColor(0, 0, 0, 0))
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setFont(font)
    p.setPen(color)
    p.drawText(QRect(0, 0, w, _ICON_H), Qt.AlignmentFlag.AlignCenter, text)
    p.end()
    return QIcon(px)


# ── App ────────────────────────────────────────────────────────────────────

class MacCleanerApp:
    """Background agent: monitors disk, auto-scans, single tabbed panel on click."""

    def __init__(self, app: QApplication) -> None:
        self._app = app
        self._service = CleanerService()
        self._scan_worker: ScanWorker | None = None
        self._clean_worker: CleanWorker | None = None
        self._storage_worker: StorageScanWorker | None = None
        self._delete_worker: StorageDeleteWorker | None = None
        self._last_warned_pct: int = 0
        self._panel_target_visible = False

        # Load persisted settings and apply stylesheet immediately
        self._settings = Settings.load()
        app.setStyleSheet(STYLESHEETS.get(self._settings.theme, STYLESHEETS["glass"]))

        # Derive live threshold values from settings
        self._warn_pct         = self._settings.warn_pct
        self._crit_pct         = self._settings.crit_pct
        self._notify_above_pct = self._settings.notify_above_pct
        self._junk_min_bytes   = self._settings.junk_min_mb * 1024 * 1024

        self._junk_revert = QTimer()
        self._junk_revert.setSingleShot(True)
        self._junk_revert.timeout.connect(self._refresh_disk_status)

        self._ns_window = None

        self._window = MainWindow(self._settings)
        self._window.scan_requested.connect(self._start_manual_scan)
        self._window.clean_requested.connect(self._start_clean)
        self._window.quit_requested.connect(app.quit)
        self._window.panel_close_requested.connect(self._hide_panel)
        self._window.panel_hidden.connect(self._on_panel_hidden)
        self._window.storage_scan_requested.connect(self._start_storage_scan)
        self._window.storage_delete_requested.connect(self._start_storage_delete)
        self._window.settings_saved.connect(self._on_settings_saved)

        # macOS hides NSPanels on deactivation; poll NSWindow.isVisible() and
        # call orderFrontRegardless() to keep the panel on screen.
        self._keepalive = QTimer()
        self._keepalive.timeout.connect(self._panel_keepalive)
        self._keepalive.start(150)

        _, free = _disk_usage()
        self._tray = QSystemTrayIcon(_make_status_icon(f"{free / 1024**3:.0f} GB"), app)
        self._tray.activated.connect(self._on_tray_activated)
        self._tray.show()

        self._disk_timer = QTimer()
        self._disk_timer.timeout.connect(self._refresh_disk_status)
        self._disk_timer.start(_DISK_POLL_MS)
        QTimer.singleShot(0, self._refresh_disk_status)

        delay_ms = self._settings.startup_delay_s * 1000
        QTimer.singleShot(delay_ms, self._auto_scan)
        self._scan_timer = QTimer()
        self._scan_timer.timeout.connect(self._auto_scan)
        if self._settings.auto_scan:
            self._scan_timer.start(self._settings.scan_interval_h * 3600 * 1000)

    # ── Settings ───────────────────────────────────────────────────────────

    def _on_settings_saved(self, s: Settings) -> None:
        self._settings = s
        self._warn_pct         = s.warn_pct
        self._crit_pct         = s.crit_pct
        self._notify_above_pct = s.notify_above_pct
        self._junk_min_bytes   = s.junk_min_mb * 1024 * 1024

        self._app.setStyleSheet(STYLESHEETS.get(s.theme, STYLESHEETS["glass"]))

        if s.auto_scan:
            self._scan_timer.start(s.scan_interval_h * 3600 * 1000)
        else:
            self._scan_timer.stop()

        self._last_warned_pct = 0   # re-arm threshold alerts after settings change
        self._refresh_disk_status()

    # ── Disk monitoring ────────────────────────────────────────────────────

    def _refresh_disk_status(self) -> None:
        self._junk_revert.stop()
        pct, free = _disk_usage()
        if pct >= self._crit_pct:
            text, color = f"{pct:.0f}%!", _RED
            tip = f"MacCleaner — disk {pct:.0f}% full, click to clean NOW"
        elif pct >= self._warn_pct:
            text, color = f"{pct:.0f}%", _AMBER
            tip = f"MacCleaner — disk {pct:.0f}% full, click to clean"
        elif self._settings.tray_label == "pct":
            text, color = f"{pct:.0f}%", _WHITE
            tip = "MacCleaner — click to open"
        else:
            text, color = f"{free / 1024**3:.0f} GB", _WHITE
            tip = "MacCleaner — click to open"
        self._tray.setIcon(_make_status_icon(text, color))
        self._tray.setToolTip(tip)
        self._check_disk_alert(pct)

    def _check_disk_alert(self, pct: float) -> None:
        if pct < self._warn_pct:
            self._last_warned_pct = 0
            return
        if pct >= self._crit_pct and self._last_warned_pct < self._crit_pct:
            self._last_warned_pct = self._crit_pct
            self._tray.showMessage(
                "MacCleaner — Disk Almost Full",
                f"Your disk is {pct:.0f}% full. Click to scan and clean up now.",
                QSystemTrayIcon.MessageIcon.Critical, 8000,
            )
        elif self._warn_pct <= pct < self._crit_pct and self._last_warned_pct < self._warn_pct:
            self._last_warned_pct = self._warn_pct
            self._tray.showMessage(
                "MacCleaner — Storage Warning",
                f"Your disk is {pct:.0f}% full. Click to scan and free up space.",
                QSystemTrayIcon.MessageIcon.Warning, 6000,
            )

    # ── Junk overlay ───────────────────────────────────────────────────────

    def _show_junk_overlay(self, junk_bytes: int) -> None:
        pct, _ = _disk_usage()
        if pct >= self._warn_pct:
            return   # disk warning already showing on tray; don't overwrite it
        self._tray.setIcon(_make_status_icon(f"↓ {_fmt_size(junk_bytes)}", _AMBER))
        self._tray.setToolTip(f"MacCleaner — {_fmt_size(junk_bytes)} to clean, click to review")
        self._junk_revert.start(_JUNK_REVERT_MS)

    # ── Auto-scan ─────────────────────────────────────────────────────────

    def _auto_scan(self) -> None:
        if self._scan_worker and self._scan_worker.isRunning():
            return
        self._scan_worker = ScanWorker(self._service)
        self._scan_worker.finished.connect(self._on_auto_scan_done)
        self._scan_worker.start()

    def _on_auto_scan_done(self, report: ScanReport) -> None:
        self._window.on_scan_finished(report)
        self._handle_scan_result(report, notify=True)

    def _handle_scan_result(self, report: ScanReport, *, notify: bool) -> None:
        junk = report.total_size
        pct, _ = _disk_usage()
        # Only alert when storage is running low AND there is meaningful junk.
        if junk >= self._junk_min_bytes and pct >= self._notify_above_pct:
            self._show_junk_overlay(junk)
            if notify:
                self._tray.showMessage(
                    "MacCleaner",
                    f"Found {_fmt_size(junk)} to clean — click to review",
                    QSystemTrayIcon.MessageIcon.Information, 6000,
                )
        else:
            self._refresh_disk_status()

    # ── Manual scan ───────────────────────────────────────────────────────

    def _start_manual_scan(self) -> None:
        if self._scan_worker and self._scan_worker.isRunning():
            return
        self._window.on_scan_started()
        self._scan_worker = ScanWorker(self._service)
        self._scan_worker.progress.connect(self._window.on_scan_progress)
        self._scan_worker.finished.connect(self._window.on_scan_finished)
        self._scan_worker.finished.connect(
            lambda r: self._handle_scan_result(r, notify=False)
        )
        self._scan_worker.error.connect(self._window.on_scan_error)
        self._scan_worker.start()

    # ── Storage scan ──────────────────────────────────────────────────────

    def _start_storage_scan(self) -> None:
        if self._storage_worker and self._storage_worker.isRunning():
            return
        self._window.on_storage_scan_started()
        self._storage_worker = StorageScanWorker()
        self._storage_worker.progress.connect(self._window.on_storage_scan_progress)
        self._storage_worker.finished.connect(self._window.on_storage_scan_finished)
        self._storage_worker.start()

    # ── Storage delete ────────────────────────────────────────────────────

    def _start_storage_delete(self, paths: list) -> None:
        if self._delete_worker and self._delete_worker.isRunning():
            return
        self._window.on_storage_delete_started()
        self._delete_worker = StorageDeleteWorker(paths)
        self._delete_worker.progress.connect(self._window.on_storage_delete_progress)
        self._delete_worker.finished.connect(self._window.on_storage_delete_finished)
        self._delete_worker.finished.connect(lambda _: self._start_storage_scan())
        self._delete_worker.finished.connect(lambda _: self._refresh_disk_status())
        self._delete_worker.start()

    # ── Clean ─────────────────────────────────────────────────────────────

    def _start_clean(self, categories: list) -> None:
        if self._clean_worker and self._clean_worker.isRunning():
            return
        if self._window._report is None:
            return
        cat_list = categories if categories else None
        self._window.on_clean_started()
        self._clean_worker = CleanWorker(self._service, self._window._report, cat_list)
        self._clean_worker.progress.connect(self._window.on_clean_progress)
        self._clean_worker.finished.connect(self._window.on_clean_finished)
        self._clean_worker.finished.connect(lambda _: self._refresh_disk_status())
        self._clean_worker.error.connect(self._window.on_clean_error)
        self._clean_worker.start()

    # ── Tray ──────────────────────────────────────────────────────────────

    def _hide_panel(self) -> None:
        self._panel_target_visible = False
        self._window.hide()

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if self._panel_target_visible:
            self._panel_target_visible = False
            self._window.hide()
        else:
            self._panel_target_visible = True
            self._position_window()
            self._window.show()
            self._window.raise_()
            QTimer.singleShot(150, self._window.activateWindow)

    def _on_panel_hidden(self) -> None:
        if self._panel_target_visible:
            QTimer.singleShot(50, self._restore_panel)

    def _restore_panel(self) -> None:
        if self._panel_target_visible:
            self._window.show()
            self._window.raise_()

    def _panel_keepalive(self) -> None:
        """Keep the panel on screen while the user wants it visible."""
        if not self._panel_target_visible:
            return
        wid = int(self._window.winId())
        qt_visible = self._window.isVisible()
        try:
            import objc
            from ctypes import c_void_p
            if wid:
                view = objc.objc_object(c_void_p=wid)
                win = view.window()
                ns_visible = bool(win.isVisible())
            else:
                ns_visible = False
            if not ns_visible or not qt_visible:
                if wid and not ns_visible:
                    win.orderFrontRegardless()
                if not qt_visible:
                    self._window.show()
                    self._window.raise_()
        except Exception:
            if not qt_visible:
                self._window.show()
                self._window.raise_()

    def _position_window(self) -> None:
        screen = self._app.primaryScreen()
        if screen is None:
            return
        geo = screen.availableGeometry()
        w = self._window.width()
        tray_geo: QRect = self._tray.geometry()
        if tray_geo.isValid() and tray_geo.width() > 0:
            x = tray_geo.x() + tray_geo.width() // 2 - w // 2
            y = tray_geo.bottom() + 4
        else:
            x = geo.right() - w - 8
            y = geo.top() + 4
        x = max(geo.left(), min(x, geo.right() - w))
        self._window.move(x, y)


def run() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    _hide_dock_icon()
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("MacCleaner")
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("Error: system tray not available.")
        return 1
    _inst = MacCleanerApp(app)  # applies stylesheet from Settings inside __init__
    return app.exec()
