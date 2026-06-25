"""StorageView — embeddable widget showing top disk-space consumers with delete support."""
import shutil
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ...services.storage_analyzer import FolderInfo
from ..formatting import fmt_size

_FOLDER_ICONS: dict[str, str] = {
    "Applications": "📱",
    "Desktop":      "🖥",
    "Documents":    "📄",
    "Downloads":    "⬇️",
    "Library":      "📚",
    "Movies":       "🎬",
    "Music":        "🎵",
    "Pictures":     "📷",
    "Developer":    "💻",
    "Projects":     "🗂",
    "Public":       "📤",
    "Sites":        "🌐",
    "Repositories": "📦",
    "Code":         "💻",
    "workspace":    "🗂",
    "repos":         "📦",
    "node_modules":  "📦",
}


def _icon(name: str) -> str:
    return _FOLDER_ICONS.get(name, "📁")


# ── Bar widget ─────────────────────────────────────────────────────────────

class _SizeBar(QWidget):
    def __init__(self, fraction: float, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._fraction = max(0.0, min(1.0, fraction))
        self.setFixedHeight(5)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        track = QPainterPath()
        track.addRoundedRect(0, 0, w, h, 2, 2)
        p.fillPath(track, QColor("#2d3561"))
        fill_w = int(w * self._fraction)
        if fill_w > 3:
            fill = QPainterPath()
            fill.addRoundedRect(0, 0, fill_w, h, 2, 2)
            grad = QLinearGradient(0, 0, fill_w, 0)
            grad.setColorAt(0, QColor("#7c3aed"))
            grad.setColorAt(1, QColor("#4f46e5"))
            p.fillPath(fill, grad)
        p.end()


# ── Folder row ─────────────────────────────────────────────────────────────

class _FolderRow(QWidget):
    checked_changed = Signal()

    def __init__(self, info: FolderInfo, max_size: int, rank: int) -> None:
        super().__init__()
        self.setObjectName("FolderRow")
        self._info = info

        v = QVBoxLayout(self)
        v.setContentsMargins(10, 7, 12, 7)
        v.setSpacing(4)

        top = QHBoxLayout()
        top.setSpacing(8)

        self._cb = QCheckBox()
        self._cb.stateChanged.connect(lambda _: self.checked_changed.emit())
        top.addWidget(self._cb)

        icon = QLabel(_icon(info.path.name))
        icon.setObjectName("FolderIcon")
        icon.setFixedWidth(20)
        top.addWidget(icon)

        name = QLabel(info.path.name)
        name.setObjectName("FolderName")
        top.addWidget(name, stretch=1)

        size_obj = "FolderSize" if rank <= 3 else "FolderSizeNormal"
        size_lbl = QLabel(fmt_size(info.size))
        size_lbl.setObjectName(size_obj)
        size_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        size_lbl.setFixedWidth(68)
        top.addWidget(size_lbl)
        v.addLayout(top)

        fraction = info.size / max_size if max_size else 0
        bar_row = QHBoxLayout()
        bar_row.setContentsMargins(28, 0, 0, 0)   # indent to align with name
        bar_row.addWidget(_SizeBar(fraction))
        v.addLayout(bar_row)

        from PySide6.QtGui import QFontMetrics
        path_lbl = QLabel()
        path_lbl.setObjectName("FolderPath")
        fm = QFontMetrics(path_lbl.font())
        path_lbl.setText(fm.elidedText(str(info.path), Qt.TextElideMode.ElideLeft, 300))
        path_row = QHBoxLayout()
        path_row.setContentsMargins(28, 0, 0, 0)
        path_row.addWidget(path_lbl)
        v.addLayout(path_row)

    @property
    def is_checked(self) -> bool:
        return self._cb.isChecked()

    @property
    def path(self) -> Path:
        return self._info.path


# ── StorageView ────────────────────────────────────────────────────────────

class StorageView(QWidget):
    rescan_requested = Signal()
    delete_requested = Signal(list)   # list[Path]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._folder_rows: list[_FolderRow] = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_disk_row())
        root.addWidget(self._build_divider())

        self._scroll = QScrollArea()
        self._scroll.setObjectName("CategoryScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        root.addWidget(self._scroll, stretch=1)

        root.addWidget(self._build_footer())
        self._show_placeholder("Click  ↺ Rescan  to analyse storage")

    def _build_disk_row(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 10, 16, 8)
        v.setSpacing(4)
        top = QHBoxLayout()
        lbl = QLabel("Disk usage")
        lbl.setObjectName("DiskLabel")
        self._disk_lbl = QLabel("—")
        self._disk_lbl.setObjectName("DiskFreeLabel")
        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(self._disk_lbl)
        v.addLayout(top)
        self._disk_bar = QProgressBar()
        self._disk_bar.setObjectName("DiskBar")
        self._disk_bar.setRange(0, 100)
        self._disk_bar.setValue(0)
        self._disk_bar.setTextVisible(False)
        self._disk_bar.setFixedHeight(6)
        v.addWidget(self._disk_bar)
        return w

    def _build_divider(self) -> QWidget:
        d = QWidget()
        d.setObjectName("Divider")
        d.setFixedHeight(1)
        return d

    def _build_footer(self) -> QWidget:
        w = QWidget()
        w.setObjectName("StatusBar")
        h = QHBoxLayout(w)
        h.setContentsMargins(16, 6, 16, 10)
        h.setSpacing(8)

        self._status_lbl = QLabel("Ready")
        self._status_lbl.setObjectName("StatusText")
        h.addWidget(self._status_lbl, stretch=1)

        self._delete_btn = QPushButton("🗑  Move to Trash")
        self._delete_btn.setObjectName("DeleteBtn")
        self._delete_btn.setFixedHeight(26)
        self._delete_btn.clicked.connect(self._on_delete_clicked)
        self._delete_btn.hide()
        h.addWidget(self._delete_btn)

        rescan_btn = QPushButton("↺  Rescan")
        rescan_btn.setObjectName("ScanBtn")
        rescan_btn.setFixedHeight(26)
        rescan_btn.clicked.connect(self.rescan_requested)
        h.addWidget(rescan_btn)

        return w

    # ── Helpers ────────────────────────────────────────────────────────────

    def _show_placeholder(self, text: str) -> None:
        self._folder_rows = []
        container = QWidget()
        container.setObjectName("CategoryScroll")
        v = QVBoxLayout(container)
        v.addStretch()
        lbl = QLabel(text)
        lbl.setObjectName("StatusText")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(lbl)
        v.addStretch()
        self._scroll.setWidget(container)

    def _refresh_disk(self) -> None:
        try:
            u = shutil.disk_usage("/")
            pct = int(u.used / u.total * 100)
            self._disk_lbl.setText(
                f"{fmt_size(u.free)} free of {fmt_size(u.total)}  ({pct}%)"
            )
            self._disk_bar.setValue(pct)
            obj = "DiskBarDanger" if pct > 85 else ("DiskBarWarning" if pct > 70 else "DiskBar")
            self._disk_bar.setObjectName(obj)
            self._disk_bar.style().unpolish(self._disk_bar)
            self._disk_bar.style().polish(self._disk_bar)
        except Exception:
            self._disk_lbl.setText("—")

    def _update_delete_btn(self) -> None:
        count = sum(1 for r in self._folder_rows if r.is_checked)
        if count:
            self._delete_btn.setText(f"🗑  Move to Trash ({count})")
            self._delete_btn.show()
        else:
            self._delete_btn.hide()

    def _on_delete_clicked(self) -> None:
        selected = [r.path for r in self._folder_rows if r.is_checked]
        if not selected:
            return

        names = "\n".join(f"  • {p.name}  ({p})" for p in selected[:8])
        if len(selected) > 8:
            names += f"\n  … and {len(selected) - 8} more"

        box = QMessageBox(self)
        box.setWindowTitle("Move to Trash")
        box.setText(f"Move {len(selected)} folder{'s' if len(selected) > 1 else ''} to Trash?")
        box.setInformativeText(
            f"{names}\n\nYou can restore them from Finder's Trash."
        )
        box.setIcon(QMessageBox.Icon.Warning)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        box.setDefaultButton(QMessageBox.StandardButton.Cancel)
        box.button(QMessageBox.StandardButton.Yes).setText("Move to Trash")

        if box.exec() == QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(selected)

    # ── Public API ─────────────────────────────────────────────────────────

    def show_scanning(self) -> None:
        self._delete_btn.hide()
        self._status_lbl.setText("Scanning…")
        self._show_placeholder("Scanning your storage…")

    def show_progress(self, msg: str) -> None:
        self._status_lbl.setText(msg)

    def show_results(self, folders: list[FolderInfo]) -> None:
        self._refresh_disk()
        self._delete_btn.hide()

        if not folders:
            self._show_placeholder("No folders found")
            self._status_lbl.setText("Done")
            return

        nm = [f for f in folders if f.is_node_modules]
        reg = [f for f in folders if not f.is_node_modules]
        max_size = max(f.size for f in folders)
        self._folder_rows = []

        container = QWidget()
        container.setObjectName("CategoryScroll")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        if nm:
            nm_total = sum(f.size for f in nm)
            hdr = QWidget()
            hdr.setObjectName("SectionHeader")
            hh = QHBoxLayout(hdr)
            hh.setContentsMargins(10, 8, 12, 4)
            lbl = QLabel(f"📦  node_modules  —  {fmt_size(nm_total)}")
            lbl.setObjectName("SectionLabel")
            hh.addWidget(lbl, stretch=1)
            sel_btn = QPushButton("Select All")
            sel_btn.setObjectName("SelectAllBtn")
            sel_btn.setFixedHeight(22)
            hh.addWidget(sel_btn)
            layout.addWidget(hdr)

            nm_rows: list[_FolderRow] = []
            for rank, info in enumerate(nm, start=1):
                row = _FolderRow(info, max_size, rank)
                row.checked_changed.connect(self._update_delete_btn)
                self._folder_rows.append(row)
                nm_rows.append(row)
                layout.addWidget(row)

            sel_btn.clicked.connect(lambda: [r._cb.setChecked(True) for r in nm_rows])

        if reg:
            if nm:
                div = QWidget()
                div.setObjectName("Divider")
                div.setFixedHeight(1)
                layout.addWidget(div)

            hdr2 = QWidget()
            hdr2.setObjectName("SectionHeader")
            hh2 = QHBoxLayout(hdr2)
            hh2.setContentsMargins(10, 8, 12, 4)
            lbl2 = QLabel("📁  Large Folders")
            lbl2.setObjectName("SectionLabel")
            hh2.addWidget(lbl2)
            layout.addWidget(hdr2)

            for rank, info in enumerate(reg, start=1):
                row = _FolderRow(info, max_size, rank)
                row.checked_changed.connect(self._update_delete_btn)
                self._folder_rows.append(row)
                layout.addWidget(row)

        layout.addStretch()
        self._scroll.setWidget(container)

        nm_part = f"{len(nm)} node_modules · " if nm else ""
        total = sum(f.size for f in folders)
        self._status_lbl.setText(f"{nm_part}{len(reg)} folders · {fmt_size(total)} shown")

    def show_deleting(self) -> None:
        self._delete_btn.setEnabled(False)
        self._delete_btn.setText("Moving to Trash…")
        self._status_lbl.setText("Moving to Trash…")
