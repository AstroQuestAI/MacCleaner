"""QSS stylesheets for MacCleaner.

STYLESHEET_GLASS  — default frosted-glass look (semi-transparent dark navy)
STYLESHEET_DARK   — flat opaque dark theme (original)
STYLESHEETS       — dict keyed by Settings.theme value
"""

# ── Glass theme ────────────────────────────────────────────────────────────

STYLESHEET_GLASS = """
/* ── Global ──────────────────────────────────────────────────────── */
QWidget {
    background: transparent;
    color: rgba(226, 232, 240, 240);
    font-family: -apple-system, "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 13px;
}

/* ── Main panel — frosted glass surface ──────────────────────────── */
#MainPanel {
    background: qlineargradient(x1:0, y1:0, x2:0.35, y2:1,
        stop:0    rgba(42, 56, 118, 220),
        stop:0.14 rgba(17, 25, 60,  214),
        stop:1    rgba(9,  15, 42,  228)
    );
    border-radius: 16px;
    border: 1px solid rgba(110, 140, 230, 68);
    border-top-color: rgba(190, 210, 255, 95);
    border-left-color: rgba(120, 152, 240, 55);
}

/* ── Header — light-catch shimmer at top ────────────────────────── */
#Header {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(65, 85, 175, 85),
        stop:1 rgba(17, 25, 60,  0)
    );
    border-bottom: 1px solid rgba(110, 140, 230, 42);
    border-radius: 16px;
    min-height: 48px;
    max-height: 48px;
}

#AppTitle {
    font-size: 16px;
    font-weight: 700;
    color: rgba(255, 255, 255, 245);
    letter-spacing: 0.3px;
}

#CloseBtn {
    background: transparent;
    border: none;
    color: rgba(100, 116, 139, 200);
    font-size: 18px;
    padding: 0;
    min-width: 24px;
    min-height: 24px;
    border-radius: 12px;
}
#CloseBtn:hover {
    background: rgba(110, 140, 230, 38);
    color: rgba(226, 232, 240, 230);
}

/* ── Tab bar ─────────────────────────────────────────────────────── */
#TabBar {
    background: rgba(8, 12, 32, 95);
    border-bottom: 1px solid rgba(110, 140, 230, 38);
    min-height: 36px;
    max-height: 36px;
}
#TabBtn {
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: rgba(71, 85, 105, 220);
    font-size: 12px;
    font-weight: 600;
    padding: 6px 0;
    border-radius: 0;
}
#TabBtn:hover {
    color: rgba(148, 163, 184, 220);
    background: transparent;
}
#TabBtn[active="true"] {
    color: rgba(165, 180, 252, 245);
    border-bottom: 2px solid rgba(129, 140, 248, 255);
    background: transparent;
}

/* ── Disk usage bar ──────────────────────────────────────────────── */
#DiskLabel {
    color: rgba(148, 163, 184, 200);
    font-size: 11px;
}
#DiskFreeLabel {
    color: rgba(226, 232, 240, 220);
    font-size: 12px;
    font-weight: 600;
}

QProgressBar {
    background: rgba(45, 53, 97, 145);
    border-radius: 4px;
    border: none;
    height: 6px;
}
QProgressBar::chunk {
    border-radius: 4px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 70, 229, 215), stop:1 rgba(124, 58, 237, 215));
}
QProgressBar#DiskBarDanger::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(220, 38, 38, 215), stop:1 rgba(239, 68, 68, 215));
}
QProgressBar#DiskBarWarning::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(217, 119, 6, 215), stop:1 rgba(245, 158, 11, 215));
}

/* ── Scrollbar ───────────────────────────────────────────────────── */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    width: 4px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: rgba(45, 53, 97, 155);
    border-radius: 2px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ── Category rows ───────────────────────────────────────────────── */
#CategoryScroll {
    border: none;
    background: transparent;
}

#CategoryRow {
    background: rgba(24, 38, 88, 148);
    border-radius: 10px;
    border: 1px solid rgba(80, 110, 200, 42);
    margin: 2px 0;
}
#CategoryRow:hover {
    background: rgba(34, 50, 105, 175);
    border-color: rgba(110, 140, 230, 68);
}

#CatIcon   { font-size: 18px; min-width: 28px; }
#CatName   { font-size: 13px; color: rgba(226, 232, 240, 230); font-weight: 500; }
#CatDesc   { font-size: 11px; color: rgba(100, 116, 139, 200); }
#CatSize {
    font-size: 13px; font-weight: 600;
    color: rgba(129, 140, 248, 255);
    min-width: 70px;
    qproperty-alignment: AlignRight;
}
#CatSizeClean {
    font-size: 13px;
    color: rgba(16, 185, 129, 220);
    min-width: 70px;
    qproperty-alignment: AlignRight;
}

/* ── Checkboxes ──────────────────────────────────────────────────── */
QCheckBox { spacing: 0; }
QCheckBox::indicator {
    width: 18px; height: 18px;
    border-radius: 5px;
    border: 2px solid rgba(61, 79, 124, 195);
    background: transparent;
}
QCheckBox::indicator:checked {
    background: rgba(124, 58, 237, 240);
    border-color: rgba(124, 58, 237, 240);
}
QCheckBox::indicator:unchecked:hover {
    border-color: rgba(124, 58, 237, 200);
}

/* ── Divider ─────────────────────────────────────────────────────── */
#Divider {
    background: rgba(45, 53, 97, 145);
    max-height: 1px;
    min-height: 1px;
}

/* ── Total row ───────────────────────────────────────────────────── */
#TotalLabel { color: rgba(148, 163, 184, 200); font-size: 12px; }
#TotalSize  { font-size: 22px; font-weight: 700; color: rgba(255, 255, 255, 250); }

/* ── Action buttons ──────────────────────────────────────────────── */
#ScanBtn {
    background: rgba(24, 36, 80, 155);
    color: rgba(165, 180, 252, 230);
    border: 1px solid rgba(61, 79, 124, 165);
    border-radius: 10px;
    padding: 10px 0;
    font-size: 13px;
    font-weight: 600;
    min-width: 110px;
}
#ScanBtn:hover {
    background: rgba(34, 50, 100, 195);
    border-color: rgba(124, 58, 237, 195);
    color: rgba(196, 181, 253, 240);
}
#ScanBtn:pressed  { background: rgba(45, 53, 97, 210); }
#ScanBtn:disabled { color: rgba(55, 65, 81, 200); border-color: rgba(31, 41, 55, 200); }

#CleanBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 70, 229, 205), stop:1 rgba(124, 58, 237, 205));
    color: rgba(255, 255, 255, 245);
    border: 1px solid rgba(129, 140, 248, 78);
    border-radius: 10px;
    padding: 10px 0;
    font-size: 13px;
    font-weight: 700;
    min-width: 130px;
}
#CleanBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(67, 56, 202, 228), stop:1 rgba(109, 40, 217, 228));
    border-color: rgba(165, 180, 252, 118);
}
#CleanBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(55, 48, 163, 238), stop:1 rgba(91, 33, 182, 238));
}
#CleanBtn:disabled {
    background: rgba(45, 53, 97, 148);
    color: rgba(75, 85, 99, 200);
    border-color: transparent;
}

/* ── Status bar ──────────────────────────────────────────────────── */
#StatusBar {
    background: rgba(6, 10, 26, 128);
    border-top: 1px solid rgba(45, 53, 97, 148);
    border-radius: 0 0 16px 16px;
}
#StatusDot   { font-size: 10px; }
#StatusText  { color: rgba(100, 116, 139, 200); font-size: 11px; }
#StatusProgress {
    background: rgba(28, 40, 68, 175);
    border-radius: 3px; border: none;
}
#StatusProgress::chunk {
    border-radius: 3px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 70, 229, 218), stop:1 rgba(124, 58, 237, 218));
}

/* ── Section headers (storage tab) ──────────────────────────────── */
#SectionHeader { background: transparent; }
#SectionLabel {
    font-size: 11px; font-weight: 700;
    color: rgba(100, 116, 139, 200);
    letter-spacing: 0.5px;
}
#SelectAllBtn {
    background: rgba(24, 36, 80, 155);
    color: rgba(165, 180, 252, 230);
    border: 1px solid rgba(61, 79, 124, 148);
    border-radius: 6px; padding: 0 8px;
    font-size: 11px; font-weight: 600;
}
#SelectAllBtn:hover {
    background: rgba(45, 53, 97, 195);
    border-color: rgba(124, 58, 237, 195);
    color: rgba(196, 181, 253, 240);
}

/* ── Delete button ───────────────────────────────────────────────── */
#DeleteBtn {
    background: rgba(59, 17, 17, 175);
    color: rgba(248, 113, 113, 220);
    border: 1px solid rgba(127, 29, 29, 175);
    border-radius: 8px; padding: 0 10px;
    font-size: 12px; font-weight: 600;
}
#DeleteBtn:hover {
    background: rgba(127, 29, 29, 195);
    color: rgba(252, 165, 165, 238);
    border-color: rgba(239, 68, 68, 198);
}
#DeleteBtn:pressed { background: rgba(153, 27, 27, 215); }
#DeleteBtn:disabled {
    background: rgba(24, 36, 80, 118);
    color: rgba(55, 65, 81, 178);
    border-color: transparent;
}

/* ── Storage folder rows ─────────────────────────────────────────── */
#FolderRow {
    background: rgba(24, 38, 88, 148);
    border-radius: 10px;
    border: 1px solid rgba(80, 110, 200, 38);
    margin: 2px 0;
}
#FolderRow:hover {
    background: rgba(34, 50, 105, 175);
    border-color: rgba(110, 140, 230, 62);
}
#FolderIcon { font-size: 16px; }
#FolderName { font-size: 13px; font-weight: 600; color: rgba(226, 232, 240, 228); }
#FolderSize { font-size: 13px; font-weight: 700; color: rgba(129, 140, 248, 255); }
#FolderSizeNormal { font-size: 13px; font-weight: 600; color: rgba(165, 180, 252, 228); }
#FolderPath { font-size: 10px; color: rgba(71, 85, 105, 198); }

/* ── Settings panel ──────────────────────────────────────────────── */
#SettingsContent { background: transparent; }

#SettingsSectionLabel {
    font-size: 11px; font-weight: 700;
    color: rgba(100, 116, 139, 195);
    letter-spacing: 0.5px;
    padding: 0 2px;
}

#SettingsCard {
    background: rgba(20, 30, 70, 138);
    border-radius: 12px;
    border: 1px solid rgba(80, 110, 200, 48);
}

#SettingsRow    { background: transparent; }
#SettingsRow:hover {
    background: rgba(34, 50, 100, 75);
    border-radius: 10px;
}
#SettingsRowLabel {
    color: rgba(226, 232, 240, 212);
    font-size: 13px;
}

#SettingsDivider {
    background: rgba(45, 53, 97, 95);
    margin: 0 14px;
}

#SettingsSaveRow {
    background: transparent;
    border-top: 1px solid rgba(45, 53, 97, 148);
}

#SaveBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 70, 229, 198), stop:1 rgba(124, 58, 237, 198));
    color: rgba(255, 255, 255, 240);
    border: 1px solid rgba(129, 140, 248, 75);
    border-radius: 10px; padding: 9px 18px;
    font-size: 13px; font-weight: 700;
}
#SaveBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(67, 56, 202, 218), stop:1 rgba(109, 40, 217, 218));
    border-color: rgba(165, 180, 252, 115);
}
#SaveBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(55, 48, 163, 238), stop:1 rgba(91, 33, 182, 238));
}

#SavedLabel {
    color: rgba(16, 185, 129, 220);
    font-size: 12px; font-weight: 600;
}

/* ── QComboBox ───────────────────────────────────────────────────── */
QComboBox {
    background: rgba(20, 30, 70, 168);
    border: 1px solid rgba(80, 110, 200, 98);
    border-radius: 8px;
    padding: 4px 8px;
    color: rgba(226, 232, 240, 218);
    font-size: 12px;
    min-height: 26px;
}
QComboBox:hover { border-color: rgba(124, 58, 237, 175); }
QComboBox::drop-down { border: none; padding-right: 6px; width: 18px; }
QComboBox::down-arrow {
    width: 0; height: 0;
    border-left:  4px solid transparent;
    border-right: 4px solid transparent;
    border-top:   5px solid rgba(165, 180, 252, 198);
}
QComboBox QAbstractItemView {
    background: rgba(14, 22, 56, 245);
    border: 1px solid rgba(80, 110, 200, 118);
    border-radius: 8px;
    selection-background-color: rgba(124, 58, 237, 178);
    color: rgba(226, 232, 240, 218);
    padding: 4px;
    outline: none;
}

/* ── Toggle switch ───────────────────────────────────────────────── */
QCheckBox#SettingsToggle { spacing: 0; }
QCheckBox#SettingsToggle::indicator {
    width: 36px; height: 20px;
    border-radius: 10px; border: none;
}
QCheckBox#SettingsToggle::indicator:unchecked {
    background: rgba(45, 53, 97, 198);
}
QCheckBox#SettingsToggle::indicator:checked {
    background: rgba(124, 58, 237, 228);
}

/* ── QSlider ─────────────────────────────────────────────────────── */
QSlider::groove:horizontal {
    height: 4px;
    background: rgba(45, 53, 97, 175);
    border-radius: 2px;
    margin: 0 2px;
}
QSlider::handle:horizontal {
    width: 16px; height: 16px;
    background: rgba(129, 140, 248, 240);
    border: 2px solid rgba(165, 180, 252, 195);
    border-radius: 8px;
    margin: -6px 0;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 70, 229, 198), stop:1 rgba(124, 58, 237, 198));
    border-radius: 2px;
}
#SettingsSliderVal {
    color: rgba(165, 180, 252, 228);
    font-size: 12px; font-weight: 600;
}

/* ── Storage toggle button ───────────────────────────────────────── */
#StorageBtn {
    background: transparent;
    border: 1px solid rgba(61, 79, 124, 148);
    color: rgba(148, 163, 184, 198);
    font-size: 14px; padding: 0 6px;
    min-width: 30px; min-height: 26px;
    border-radius: 7px;
}
#StorageBtn:hover {
    background: rgba(45, 53, 97, 148);
    border-color: rgba(124, 58, 237, 198);
    color: rgba(196, 181, 253, 238);
}
"""


# ── Dark theme (original) ──────────────────────────────────────────────────

STYLESHEET_DARK = """
/* ── Global ─────────────────────────────────────────────────────── */
QWidget {
    background-color: #1a1a2e;
    color: #e2e8f0;
    font-family: -apple-system, "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 13px;
}

/* ── Main panel ──────────────────────────────────────────────────── */
#MainPanel {
    background-color: #16213e;
    border-radius: 14px;
    border: 1px solid #2d3561;
}

/* ── Header ──────────────────────────────────────────────────────── */
#Header {
    background-color: #1a1a2e;
    border-bottom: 1px solid #2d3561;
    border-radius: 14px;
    min-height: 48px;
    max-height: 48px;
}
#AppTitle {
    font-size: 16px; font-weight: 700;
    color: #ffffff; letter-spacing: 0.3px;
}
#CloseBtn {
    background: transparent; border: none;
    color: #64748b; font-size: 18px; padding: 0;
    min-width: 24px; min-height: 24px; border-radius: 12px;
}
#CloseBtn:hover { background-color: #2d3561; color: #e2e8f0; }

/* ── Tab bar ─────────────────────────────────────────────────────── */
#TabBar {
    background-color: #1a1a2e;
    border-bottom: 1px solid #2d3561;
    min-height: 36px; max-height: 36px;
}
#TabBtn {
    background: transparent; border: none;
    border-bottom: 2px solid transparent;
    color: #475569; font-size: 12px; font-weight: 600;
    padding: 6px 0; border-radius: 0;
}
#TabBtn:hover { color: #94a3b8; background: transparent; }
#TabBtn[active="true"] {
    color: #a5b4fc;
    border-bottom: 2px solid #7c3aed;
    background: transparent;
}

/* ── Disk bar ────────────────────────────────────────────────────── */
#DiskLabel    { color: #94a3b8; font-size: 11px; }
#DiskFreeLabel { color: #e2e8f0; font-size: 12px; font-weight: 600; }

QProgressBar {
    background-color: #2d3561; border-radius: 4px;
    border: none; height: 6px; text-align: center;
}
QProgressBar::chunk {
    border-radius: 4px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #7c3aed);
}
QProgressBar#DiskBarDanger::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #ef4444);
}
QProgressBar#DiskBarWarning::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #d97706, stop:1 #f59e0b);
}

/* ── Scrollbar ───────────────────────────────────────────────────── */
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { width: 4px; background: transparent; }
QScrollBar::handle:vertical {
    background: #2d3561; border-radius: 2px; min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Category rows ───────────────────────────────────────────────── */
#CategoryScroll { border: none; background: transparent; }
#CategoryRow {
    background-color: #1e2a45; border-radius: 10px; margin: 2px 0;
}
#CategoryRow:hover { background-color: #243151; }
#CatIcon   { font-size: 18px; min-width: 28px; }
#CatName   { font-size: 13px; color: #e2e8f0; font-weight: 500; }
#CatDesc   { font-size: 11px; color: #64748b; }
#CatSize {
    font-size: 13px; font-weight: 600; color: #7c3aed;
    min-width: 70px; qproperty-alignment: AlignRight;
}
#CatSizeClean {
    font-size: 13px; color: #10b981;
    min-width: 70px; qproperty-alignment: AlignRight;
}

/* ── Checkbox ────────────────────────────────────────────────────── */
QCheckBox { spacing: 0; }
QCheckBox::indicator {
    width: 18px; height: 18px;
    border-radius: 5px; border: 2px solid #3d4f7c;
    background: transparent;
}
QCheckBox::indicator:checked { background-color: #7c3aed; border-color: #7c3aed; }
QCheckBox::indicator:unchecked:hover { border-color: #7c3aed; }

/* ── Divider ─────────────────────────────────────────────────────── */
#Divider { background-color: #2d3561; max-height: 1px; min-height: 1px; }

/* ── Total row ───────────────────────────────────────────────────── */
#TotalLabel { color: #94a3b8; font-size: 12px; }
#TotalSize  { font-size: 22px; font-weight: 700; color: #ffffff; }

/* ── Buttons ─────────────────────────────────────────────────────── */
#ScanBtn {
    background-color: #1e2a45; color: #a5b4fc;
    border: 1px solid #3d4f7c; border-radius: 10px;
    padding: 10px 0; font-size: 13px; font-weight: 600; min-width: 110px;
}
#ScanBtn:hover { background-color: #243151; border-color: #7c3aed; color: #c4b5fd; }
#ScanBtn:pressed { background-color: #2d3561; }
#ScanBtn:disabled { color: #374151; border-color: #1f2937; }

#CleanBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #7c3aed);
    color: #ffffff; border: none; border-radius: 10px;
    padding: 10px 0; font-size: 13px; font-weight: 700; min-width: 130px;
}
#CleanBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4338ca, stop:1 #6d28d9);
}
#CleanBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3730a3, stop:1 #5b21b6);
}
#CleanBtn:disabled { background: #2d3561; color: #4b5563; }

/* ── Status bar ──────────────────────────────────────────────────── */
#StatusBar {
    background-color: #0f172a;
    border-top: 1px solid #2d3561;
    border-radius: 0 0 14px 14px;
}
#StatusDot  { font-size: 10px; }
#StatusText { color: #64748b; font-size: 11px; }
#StatusProgress {
    background-color: #1e2a45; border-radius: 3px; border: none;
}
#StatusProgress::chunk {
    border-radius: 3px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #7c3aed);
}

/* ── Section headers ─────────────────────────────────────────────── */
#SectionHeader { background: transparent; }
#SectionLabel  { font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.5px; }
#SelectAllBtn {
    background-color: #1e2a45; color: #a5b4fc;
    border: 1px solid #3d4f7c; border-radius: 6px;
    padding: 0 8px; font-size: 11px; font-weight: 600;
}
#SelectAllBtn:hover { background-color: #2d3561; border-color: #7c3aed; color: #c4b5fd; }

/* ── Delete button ───────────────────────────────────────────────── */
#DeleteBtn {
    background-color: #3b1111; color: #f87171;
    border: 1px solid #7f1d1d; border-radius: 8px;
    padding: 0 10px; font-size: 12px; font-weight: 600;
}
#DeleteBtn:hover { background-color: #7f1d1d; color: #fca5a5; border-color: #ef4444; }
#DeleteBtn:pressed { background-color: #991b1b; }
#DeleteBtn:disabled { background-color: #1e2a45; color: #374151; border-color: #1f2937; }

/* ── Storage rows ────────────────────────────────────────────────── */
#FolderRow { background-color: #1e2a45; border-radius: 10px; margin: 2px 0; }
#FolderRow:hover { background-color: #243151; }
#FolderIcon { font-size: 16px; }
#FolderName { font-size: 13px; font-weight: 600; color: #e2e8f0; }
#FolderSize { font-size: 13px; font-weight: 700; color: #7c3aed; }
#FolderSizeNormal { font-size: 13px; font-weight: 600; color: #a5b4fc; }
#FolderPath { font-size: 10px; color: #475569; }

/* ── Settings panel ──────────────────────────────────────────────── */
#SettingsContent { background: transparent; }
#SettingsSectionLabel {
    font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: 0.5px; padding: 0 2px;
}
#SettingsCard {
    background-color: #1e2a45; border-radius: 12px; border: 1px solid #2d3561;
}
#SettingsRow { background: transparent; }
#SettingsRow:hover { background-color: #243151; border-radius: 10px; }
#SettingsRowLabel { color: #e2e8f0; font-size: 13px; }
#SettingsDivider { background-color: #2d3561; margin: 0 14px; }
#SettingsSaveRow { background: transparent; border-top: 1px solid #2d3561; }
#SaveBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #7c3aed);
    color: #ffffff; border: none; border-radius: 10px;
    padding: 9px 18px; font-size: 13px; font-weight: 700;
}
#SaveBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4338ca, stop:1 #6d28d9);
}
#SaveBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3730a3, stop:1 #5b21b6);
}
#SavedLabel { color: #10b981; font-size: 12px; font-weight: 600; }

/* ── QComboBox ───────────────────────────────────────────────────── */
QComboBox {
    background-color: #1e2a45; border: 1px solid #3d4f7c;
    border-radius: 8px; padding: 4px 8px;
    color: #e2e8f0; font-size: 12px; min-height: 26px;
}
QComboBox:hover { border-color: #7c3aed; }
QComboBox::drop-down { border: none; padding-right: 6px; width: 18px; }
QComboBox::down-arrow {
    width: 0; height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #a5b4fc;
}
QComboBox QAbstractItemView {
    background-color: #16213e; border: 1px solid #3d4f7c;
    border-radius: 8px; selection-background-color: #7c3aed;
    color: #e2e8f0; padding: 4px; outline: none;
}

/* ── Toggle switch ───────────────────────────────────────────────── */
QCheckBox#SettingsToggle { spacing: 0; }
QCheckBox#SettingsToggle::indicator {
    width: 36px; height: 20px; border-radius: 10px; border: none;
}
QCheckBox#SettingsToggle::indicator:unchecked { background-color: #2d3561; }
QCheckBox#SettingsToggle::indicator:checked   { background-color: #7c3aed; }

/* ── QSlider ─────────────────────────────────────────────────────── */
QSlider::groove:horizontal {
    height: 4px; background: #2d3561; border-radius: 2px; margin: 0 2px;
}
QSlider::handle:horizontal {
    width: 16px; height: 16px; background: #a5b4fc;
    border: 2px solid #7c3aed; border-radius: 8px; margin: -6px 0;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #7c3aed);
    border-radius: 2px;
}
#SettingsSliderVal { color: #a5b4fc; font-size: 12px; font-weight: 600; }

/* ── Storage toggle button ───────────────────────────────────────── */
#StorageBtn {
    background: transparent; border: 1px solid #3d4f7c;
    color: #94a3b8; font-size: 14px; padding: 0 6px;
    min-width: 30px; min-height: 26px; border-radius: 7px;
}
#StorageBtn:hover {
    background-color: #2d3561; border-color: #7c3aed; color: #c4b5fd;
}
#StorageBtn[active="true"] {
    background-color: #2d3561; border-color: #7c3aed; color: #c4b5fd;
}
"""


STYLESHEETS: dict[str, str] = {
    "glass": STYLESHEET_GLASS,
    "dark":  STYLESHEET_DARK,
}

CHECKMARK_CHECKED = """
QCheckBox::indicator:checked {
    background-color: #7c3aed;
    border-color: #7c3aed;
}
"""
