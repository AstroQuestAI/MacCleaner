"""Settings panel — Appearance, Scheduler, Scan sections."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ...config import Settings
from .style import THEME_NAMES

_THEME_KEYS = {v: k for k, v in THEME_NAMES.items()}


class SettingsPanel(QWidget):
    settings_saved = Signal(object)   # emits a Settings instance

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self._build_ui()
        self._load_values()

    # ── Layout ────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content.setObjectName("SettingsContent")
        v = QVBoxLayout(content)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(6)

        # ── Appearance
        v.addWidget(self._section_label("🎨  Appearance"))
        v.addWidget(self._card([
            self._combo_row("Theme",       list(THEME_NAMES.values()),      "_theme"),
            self._combo_row("Tray shows",  ["Free space", "Disk used %"], "_tray"),
            self._slider_row("Opacity",    70, 100,                        "_opacity"),
        ]))

        v.addSpacing(6)

        # ── Scheduler
        v.addWidget(self._section_label("⏰  Scheduler"))
        v.addWidget(self._card([
            self._toggle_row("Auto-scan",             "_auto_scan"),
            self._combo_row("Interval",
                ["1 hour", "2 hours", "6 hours", "12 hours", "24 hours"],  "_interval"),
            self._combo_row("Alert when disk ≥",
                ["50%", "60%", "70%", "80%", "90%"],                       "_notify_pct"),
            self._combo_row("Min junk to notify",
                ["50 MB", "100 MB", "200 MB", "500 MB"],                   "_junk_min"),
            self._combo_row("Warn colour at",
                ["60%", "70%", "75%", "80%", "85%"],                       "_warn_pct"),
            self._combo_row("Critical colour at",
                ["80%", "85%", "90%", "95%"],                              "_crit_pct"),
        ]))

        v.addSpacing(6)

        # ── Scan
        v.addWidget(self._section_label("🔍  Scan"))
        v.addWidget(self._card([
            self._toggle_row("Scan node_modules folders", "_scan_nm"),
            self._combo_row("Startup scan delay",
                ["5 s", "15 s", "30 s", "60 s"],                          "_startup_delay"),
        ]))

        v.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

        # ── Footer
        footer = QWidget()
        footer.setObjectName("SettingsSaveRow")
        h = QHBoxLayout(footer)
        h.setContentsMargins(12, 8, 12, 12)
        h.setSpacing(10)

        self._saved_lbl = QLabel("Saved ✓")
        self._saved_lbl.setObjectName("SavedLabel")
        self._saved_lbl.hide()
        h.addWidget(self._saved_lbl)
        h.addStretch()

        save_btn = QPushButton("💾  Save Settings")
        save_btn.setObjectName("SaveBtn")
        save_btn.clicked.connect(self._on_save)
        h.addWidget(save_btn)
        outer.addWidget(footer)

    # ── Widget helpers ────────────────────────────────────────────────────

    def _section_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("SettingsSectionLabel")
        return lbl

    def _card(self, rows: list[QWidget]) -> QWidget:
        card = QWidget()
        card.setObjectName("SettingsCard")
        v = QVBoxLayout(card)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        for i, row in enumerate(rows):
            v.addWidget(row)
            if i < len(rows) - 1:
                sep = QWidget()
                sep.setObjectName("SettingsDivider")
                sep.setFixedHeight(1)
                v.addWidget(sep)
        return card

    def _row_base(self, label: str) -> tuple[QWidget, QHBoxLayout]:
        w = QWidget()
        w.setObjectName("SettingsRow")
        h = QHBoxLayout(w)
        h.setContentsMargins(14, 9, 14, 9)
        h.setSpacing(10)
        lbl = QLabel(label)
        lbl.setObjectName("SettingsRowLabel")
        h.addWidget(lbl, stretch=1)
        return w, h

    def _combo_row(self, label: str, options: list[str], attr: str) -> QWidget:
        w, h = self._row_base(label)
        combo = QComboBox()
        combo.setObjectName("SettingsCombo")
        for opt in options:
            combo.addItem(opt)
        combo.setFixedWidth(152)
        h.addWidget(combo)
        setattr(self, attr, combo)
        return w

    def _slider_row(self, label: str, lo: int, hi: int, attr: str) -> QWidget:
        w, h = self._row_base(label)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setObjectName("SettingsSlider")
        slider.setRange(lo, hi)
        slider.setFixedWidth(88)
        val_lbl = QLabel()
        val_lbl.setObjectName("SettingsSliderVal")
        val_lbl.setFixedWidth(36)
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        slider.valueChanged.connect(lambda v, lv=val_lbl: lv.setText(f"{v}%"))
        h.addWidget(slider)
        h.addWidget(val_lbl)
        setattr(self, f"{attr}_slider", slider)
        setattr(self, f"{attr}_val", val_lbl)
        return w

    def _toggle_row(self, label: str, attr: str) -> QWidget:
        w, h = self._row_base(label)
        toggle = QCheckBox()
        toggle.setObjectName("SettingsToggle")
        h.addWidget(toggle)
        setattr(self, attr, toggle)
        return w

    # ── Load / Save ───────────────────────────────────────────────────────

    def _load_values(self) -> None:
        s = self._settings
        self._theme.setCurrentText(THEME_NAMES.get(s.theme, "Midnight Navy"))
        self._tray.setCurrentIndex(0 if s.tray_label == "free" else 1)
        self._opacity_slider.setValue(s.opacity)
        self._opacity_val.setText(f"{s.opacity}%")

        self._auto_scan.setChecked(s.auto_scan)
        self._interval.setCurrentIndex(
            {1: 0, 2: 1, 6: 2, 12: 3, 24: 4}.get(s.scan_interval_h, 1))
        self._notify_pct.setCurrentIndex(
            {50: 0, 60: 1, 70: 2, 80: 3, 90: 4}.get(s.notify_above_pct, 2))
        self._junk_min.setCurrentIndex(
            {50: 0, 100: 1, 200: 2, 500: 3}.get(s.junk_min_mb, 2))
        self._warn_pct.setCurrentIndex(
            {60: 0, 70: 1, 75: 2, 80: 3, 85: 4}.get(s.warn_pct, 1))
        self._crit_pct.setCurrentIndex(
            {80: 0, 85: 1, 90: 2, 95: 3}.get(s.crit_pct, 1))

        self._scan_nm.setChecked(s.scan_node_modules)
        self._startup_delay.setCurrentIndex(
            {5: 0, 15: 1, 30: 2, 60: 3}.get(s.startup_delay_s, 1))

    def _on_save(self) -> None:
        s = self._settings
        s.theme     = _THEME_KEYS.get(self._theme.currentText(), "glass")
        s.tray_label = "free" if self._tray.currentIndex() == 0 else "pct"
        s.opacity   = self._opacity_slider.value()

        s.auto_scan       = self._auto_scan.isChecked()
        s.scan_interval_h = [1, 2, 6, 12, 24][self._interval.currentIndex()]
        s.notify_above_pct = [50, 60, 70, 80, 90][self._notify_pct.currentIndex()]
        s.junk_min_mb     = [50, 100, 200, 500][self._junk_min.currentIndex()]
        s.warn_pct        = [60, 70, 75, 80, 85][self._warn_pct.currentIndex()]
        s.crit_pct        = [80, 85, 90, 95][self._crit_pct.currentIndex()]

        s.scan_node_modules = self._scan_nm.isChecked()
        s.startup_delay_s   = [5, 15, 30, 60][self._startup_delay.currentIndex()]

        s.save()
        self.settings_saved.emit(s)
        self._flash_saved()

    def _flash_saved(self) -> None:
        self._saved_lbl.show()
        QTimer.singleShot(2000, self._saved_lbl.hide)
