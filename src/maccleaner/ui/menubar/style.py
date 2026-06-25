"""QSS stylesheets for MacCleaner.

STYLESHEET_GLASS  — original verbatim dark-navy glass (kept for reference)
STYLESHEET_DARK   — flat opaque dark theme
10 glass themes generated via _glass() using Apple system color vocabulary
THEME_NAMES       — ordered display-name → key mapping shown in Settings
STYLESHEETS       — dict keyed by Settings.theme value
"""

# ── Parametric glass-theme engine ──────────────────────────────────────────
#
# Token legend:
#   fg/fg2/fg3  text hierarchy (primary → muted)    fgt  title / total
#   bg0/bg1/bg2 panel gradient stops (top → bottom)  hdr  header shimmer
#   tab         tab-bar background                   acc  accent (active states)
#   ac2         accent 2 (gradient pair)              crd  card row bg
#   crh         card row hover                        brd  border
#   brh         border hover                          bdt  border-top specular (glass edge)
#   sts         status bar bg                         cbo  combo/input bg
#   pop         combo popup bg                        trk  progress / slider track
#   div         divider                               tof  toggle unchecked
#   bb          secondary btn bg                      bh   secondary btn hover
#   bt          secondary btn text                    cbf  primary action btn fg

_T = """\
QWidget {
    background: transparent;
    color: «fg»;
    font-family: -apple-system, "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 13px;
}
#MainPanel {
    background: qlineargradient(x1:0, y1:0, x2:0.35, y2:1,
        stop:0 «bg0», stop:0.14 «bg1», stop:1 «bg2»);
    border-radius: 16px;
    border: 1px solid «brd»;
    border-top-color: «bdt»;
    border-left-color: «brd»;
}
#Header {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 «hdr», stop:1 rgba(0,0,0,0));
    border-bottom: 1px solid «brd»;
    border-radius: 16px;
    min-height: 48px; max-height: 48px;
}
#AppTitle  { font-size: 16px; font-weight: 700; color: «fgt»; letter-spacing: 0.3px; }
#CloseBtn  { background: transparent; border: none; color: «fg3»; font-size: 18px;
             padding: 0; min-width: 24px; min-height: 24px; border-radius: 12px; }
#CloseBtn:hover { background: «brd»; color: «fg»; }

#TabBar { background: «tab»; border-bottom: 1px solid «brd»; min-height: 36px; max-height: 36px; }
#TabBtn { background: transparent; border: none; border-bottom: 2px solid transparent;
          color: «fg3»; font-size: 12px; font-weight: 600; padding: 6px 0; border-radius: 0; }
#TabBtn:hover { color: «fg2»; background: transparent; }
#TabBtn[active="true"] { color: «acc»; border-bottom: 2px solid «acc»; background: transparent; }

#DiskLabel     { color: «fg2»; font-size: 11px; }
#DiskFreeLabel { color: «fg»;  font-size: 12px; font-weight: 600; }
QProgressBar   { background: «trk»; border-radius: 4px; border: none; height: 6px; }
QProgressBar::chunk {
    border-radius: 4px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «acc», stop:1 «ac2»);
}
QProgressBar#DiskBarDanger::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(220,38,38,215), stop:1 rgba(239,68,68,215));
}
QProgressBar#DiskBarWarning::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(217,119,6,215), stop:1 rgba(245,158,11,215));
}

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { width: 4px; background: transparent; }
QScrollBar::handle:vertical { background: «brd»; border-radius: 2px; min-height: 20px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

#CategoryScroll { border: none; background: transparent; }
#CategoryRow  { background: «crd»; border-radius: 10px; border: 1px solid «brd»; margin: 2px 0; }
#CategoryRow:hover { background: «crh»; border-color: «brh»; }
#CatIcon { font-size: 18px; min-width: 28px; }
#CatName { font-size: 13px; color: «fg»;  font-weight: 500; }
#CatDesc { font-size: 11px; color: «fg3»; }
#CatSize      { font-size: 13px; font-weight: 600; color: «acc»;
                min-width: 70px; qproperty-alignment: AlignRight; }
#CatSizeClean { font-size: 13px; color: rgba(16,185,129,220);
                min-width: 70px; qproperty-alignment: AlignRight; }

QCheckBox { spacing: 0; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 5px;
                       border: 2px solid «brh»; background: transparent; }
QCheckBox::indicator:checked          { background: «acc»; border-color: «acc»; }
QCheckBox::indicator:unchecked:hover  { border-color: «acc»; }

#Divider    { background: «div»; max-height: 1px; min-height: 1px; }
#TotalLabel { color: «fg2»; font-size: 12px; }
#TotalSize  { font-size: 22px; font-weight: 700; color: «fgt»; }

#ScanBtn {
    background: «bb»; color: «bt»; border: 1px solid «brd»; border-radius: 10px;
    padding: 10px 0; font-size: 13px; font-weight: 600; min-width: 110px;
}
#ScanBtn:hover    { background: «bh»; border-color: «brh»; color: «acc»; }
#ScanBtn:pressed  { background: «crh»; }
#ScanBtn:disabled { color: «fg3»; border-color: «brd»; }

#CleanBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «acc», stop:1 «ac2»);
    color: «cbf»; border: 1px solid «brh»; border-radius: 10px;
    padding: 10px 0; font-size: 13px; font-weight: 700; min-width: 130px;
}
#CleanBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «ac2», stop:1 «acc»);
    border-color: «brh»;
}
#CleanBtn:pressed  { background: «ac2»; }
#CleanBtn:disabled { background: «crd»; color: «fg3»; border-color: transparent; }

#StatusBar { background: «sts»; border-top: 1px solid «brd»; border-radius: 0 0 16px 16px; }
#StatusDot  { font-size: 10px; }
#StatusText { color: «fg3»; font-size: 11px; }
#StatusProgress { background: «crd»; border-radius: 3px; border: none; }
#StatusProgress::chunk {
    border-radius: 3px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «acc», stop:1 «ac2»);
}

#SectionHeader { background: transparent; }
#SectionLabel  { font-size: 11px; font-weight: 700; color: «fg3»; letter-spacing: 0.5px; }
#SelectAllBtn {
    background: «bb»; color: «bt»; border: 1px solid «brd»; border-radius: 6px;
    padding: 0 8px; font-size: 11px; font-weight: 600;
}
#SelectAllBtn:hover { background: «bh»; border-color: «brh»; color: «acc»; }

#DeleteBtn {
    background: rgba(59,17,17,175); color: rgba(248,113,113,220);
    border: 1px solid rgba(127,29,29,175); border-radius: 8px;
    padding: 0 10px; font-size: 12px; font-weight: 600;
}
#DeleteBtn:hover    { background: rgba(127,29,29,195); color: rgba(252,165,165,238);
                      border-color: rgba(239,68,68,198); }
#DeleteBtn:pressed  { background: rgba(153,27,27,215); }
#DeleteBtn:disabled { background: «crd»; color: «fg3»; border-color: transparent; }

#FolderRow  { background: «crd»; border-radius: 10px; border: 1px solid «brd»; margin: 2px 0; }
#FolderRow:hover  { background: «crh»; border-color: «brh»; }
#FolderIcon       { font-size: 16px; }
#FolderName       { font-size: 13px; font-weight: 600; color: «fg»; }
#FolderSize       { font-size: 13px; font-weight: 700; color: «acc»; }
#FolderSizeNormal { font-size: 13px; font-weight: 600; color: «ac2»; }
#FolderPath       { font-size: 10px; color: «fg3»; }

#SettingsContent { background: transparent; }
#SettingsSectionLabel { font-size: 11px; font-weight: 700; color: «fg3»;
                        letter-spacing: 0.5px; padding: 0 2px; }
#SettingsCard { background: «crd»; border-radius: 12px; border: 1px solid «brd»; }
#SettingsRow  { background: transparent; }
#SettingsRow:hover { background: «crh»; border-radius: 10px; }
#SettingsRowLabel  { color: «fg»; font-size: 13px; }
#SettingsDivider   { background: «div»; margin: 0 14px; }
#SettingsSaveRow   { background: transparent; border-top: 1px solid «div»; }

#SaveBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «acc», stop:1 «ac2»);
    color: «cbf»; border: 1px solid «brh»; border-radius: 10px;
    padding: 9px 18px; font-size: 13px; font-weight: 700;
}
#SaveBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «ac2», stop:1 «acc»);
    border-color: «brh»;
}
#SaveBtn:pressed { background: «ac2»; }
#SavedLabel { color: rgba(16,185,129,220); font-size: 12px; font-weight: 600; }

QComboBox {
    background: «cbo»; border: 1px solid «brh»; border-radius: 8px;
    padding: 4px 8px; color: «fg»; font-size: 12px; min-height: 26px;
}
QComboBox:hover { border-color: «acc»; }
QComboBox::drop-down { border: none; padding-right: 6px; width: 18px; }
QComboBox::down-arrow {
    width: 0; height: 0;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-top: 5px solid «ac2»;
}
QComboBox QAbstractItemView {
    background: «pop»; border: 1px solid «brh»; border-radius: 8px;
    selection-background-color: «acc»; color: «fg»; padding: 4px; outline: none;
}

QCheckBox#SettingsToggle { spacing: 0; }
QCheckBox#SettingsToggle::indicator { width: 36px; height: 20px; border-radius: 10px; border: none; }
QCheckBox#SettingsToggle::indicator:unchecked { background: «tof»; }
QCheckBox#SettingsToggle::indicator:checked   { background: «acc»; }

QSlider::groove:horizontal { height: 4px; background: «trk»; border-radius: 2px; margin: 0 2px; }
QSlider::handle:horizontal {
    width: 16px; height: 16px; background: «ac2»;
    border: 2px solid «acc»; border-radius: 8px; margin: -6px 0;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 «acc», stop:1 «ac2»);
    border-radius: 2px;
}
#SettingsSliderVal { color: «ac2»; font-size: 12px; font-weight: 600; }

#StorageBtn {
    background: transparent; border: 1px solid «brd»; color: «fg2»;
    font-size: 14px; padding: 0 6px; min-width: 30px; min-height: 26px; border-radius: 7px;
}
#StorageBtn:hover        { background: «crh»; border-color: «acc»; color: «acc»; }
#StorageBtn[active="true"] { background: «crh»; border-color: «acc»; color: «acc»; }
"""


def _glass(**t: str) -> str:
    s = _T
    for k, v in t.items():
        s = s.replace(f"«{k}»", v)
    return s


# ── Theme token dicts ──────────────────────────────────────────────────────
# All dark themes share: white text hierarchy (255,255,255 at 95%/67%/42%)
# Light theme (Titanium) uses black text hierarchy on Apple system backgrounds
# Each theme = one saturated Apple system accent + matching deep-tinted glass panel

# ── MIDNIGHT INDIGO — Apple Indigo #5E5CE6 on deep space glass ───────────
_MIDNIGHT_INDIGO = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(28,24,52,240)",   bg1="rgba(18,15,38,235)",    bg2="rgba(10,8,25,232)",
    hdr="rgba(94,92,230,38)",   tab="rgba(8,6,20,105)",
    bdt="rgba(255,255,255,58)", brd="rgba(255,255,255,20)",  brh="rgba(94,92,230,65)",
    acc="rgba(94,92,230,255)",  ac2="rgba(165,132,248,252)",
    crd="rgba(44,40,72,162)",   crh="rgba(58,55,88,188)",
    sts="rgba(8,6,20,145)",     cbo="rgba(38,35,65,172)",    pop="rgba(22,18,40,252)",
    trk="rgba(44,40,72,175)",   div="rgba(255,255,255,15)",  tof="rgba(38,35,65,215)",
    bb="rgba(38,35,65,165)",    bh="rgba(52,48,80,195)",     bt="rgba(165,132,248,245)",
    cbf="rgba(255,255,255,252)",
)

# ── INFRARED — Apple Pink #FF375F on deep crimson glass ────────────────────
_INFRARED = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(88,18,38,240)",   bg1="rgba(65,12,26,235)",    bg2="rgba(42,6,16,232)",
    hdr="rgba(255,55,95,35)",   tab="rgba(38,8,18,105)",
    bdt="rgba(255,185,200,62)", brd="rgba(255,100,130,20)",  brh="rgba(255,55,95,58)",
    acc="rgba(255,55,95,255)",  ac2="rgba(255,148,168,252)",
    crd="rgba(105,25,45,162)",  crh="rgba(128,35,58,188)",
    sts="rgba(28,6,14,145)",    cbo="rgba(82,18,35,172)",    pop="rgba(45,8,20,252)",
    trk="rgba(88,25,45,175)",   div="rgba(255,100,130,20)",  tof="rgba(72,15,30,215)",
    bb="rgba(82,18,35,165)",    bh="rgba(105,25,45,195)",    bt="rgba(255,148,168,245)",
    cbf="rgba(255,255,255,252)",
)

# ── PACIFIC BLUE — Apple Blue #0A84FF · iPhone 12 Pro ocean glass ─────────
_PACIFIC_BLUE = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(0,58,110,240)",   bg1="rgba(0,40,80,235)",     bg2="rgba(0,22,52,232)",
    hdr="rgba(10,132,255,35)",  tab="rgba(0,18,42,105)",
    bdt="rgba(165,215,255,62)", brd="rgba(100,180,255,20)",  brh="rgba(10,132,255,58)",
    acc="rgba(10,132,255,255)", ac2="rgba(100,210,255,252)",
    crd="rgba(0,52,100,162)",   crh="rgba(0,68,118,188)",
    sts="rgba(0,12,32,145)",    cbo="rgba(0,40,78,172)",     pop="rgba(0,18,42,252)",
    trk="rgba(0,52,100,175)",   div="rgba(100,180,255,20)",  tof="rgba(0,32,62,215)",
    bb="rgba(0,40,78,165)",     bh="rgba(0,55,98,195)",      bt="rgba(100,210,255,245)",
    cbf="rgba(255,255,255,252)",
)

# ── MIDNIGHT GREEN — Apple Green #30D158 · iPhone 11 Pro forest glass ──────
_MIDNIGHT_GREEN = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(0,58,45,240)",    bg1="rgba(0,40,30,235)",     bg2="rgba(0,22,18,232)",
    hdr="rgba(48,209,88,35)",   tab="rgba(0,18,14,105)",
    bdt="rgba(148,240,178,62)", brd="rgba(80,215,122,20)",   brh="rgba(48,209,88,58)",
    acc="rgba(48,209,88,255)",  ac2="rgba(148,240,178,252)",
    crd="rgba(0,52,40,162)",    crh="rgba(0,68,52,188)",
    sts="rgba(0,12,10,145)",    cbo="rgba(0,40,30,172)",     pop="rgba(0,18,14,252)",
    trk="rgba(0,52,40,175)",    div="rgba(80,215,122,20)",   tof="rgba(0,32,24,215)",
    bb="rgba(0,40,30,165)",     bh="rgba(0,55,42,195)",      bt="rgba(148,240,178,245)",
    cbf="rgba(255,255,255,252)",
)

# ── DESERT SUNSET — Apple Orange #FF9F0A · macOS Sequoia warm amber glass ──
_DESERT_SUNSET = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(95,38,8,240)",    bg1="rgba(72,25,4,235)",     bg2="rgba(48,15,2,232)",
    hdr="rgba(255,159,10,35)",  tab="rgba(42,18,2,105)",
    bdt="rgba(255,222,148,62)", brd="rgba(255,178,80,20)",   brh="rgba(255,159,10,58)",
    acc="rgba(255,159,10,255)", ac2="rgba(255,222,100,252)",
    crd="rgba(105,48,12,162)",  crh="rgba(128,62,16,188)",
    sts="rgba(28,12,2,145)",    cbo="rgba(78,38,8,172)",     pop="rgba(42,18,2,252)",
    trk="rgba(88,42,10,175)",   div="rgba(255,178,80,20)",   tof="rgba(62,28,5,215)",
    bb="rgba(78,38,8,165)",     bh="rgba(100,50,12,195)",    bt="rgba(255,222,100,245)",
    cbf="rgba(255,255,255,252)",
)

# ── DEEP PURPLE — Apple Purple #BF5AF2 · space violet glass ───────────────
_DEEP_PURPLE = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(52,18,80,240)",   bg1="rgba(38,12,58,235)",    bg2="rgba(24,6,40,232)",
    hdr="rgba(191,90,242,38)",  tab="rgba(22,8,38,105)",
    bdt="rgba(228,178,255,62)", brd="rgba(200,128,255,20)",  brh="rgba(191,90,242,58)",
    acc="rgba(191,90,242,255)", ac2="rgba(218,148,250,252)",
    crd="rgba(62,22,92,162)",   crh="rgba(80,30,112,188)",
    sts="rgba(15,5,26,145)",    cbo="rgba(48,18,72,172)",    pop="rgba(28,8,45,252)",
    trk="rgba(58,22,82,175)",   div="rgba(200,128,255,20)",  tof="rgba(38,12,58,215)",
    bb="rgba(48,18,72,165)",    bh="rgba(65,25,95,195)",     bt="rgba(218,148,250,245)",
    cbf="rgba(255,255,255,252)",
)

# ── OLIVE NIGHT — Apple Yellow #FFD60A · dark warm olive glass ────────────
_OLIVE_NIGHT = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(45,42,15,240)",   bg1="rgba(32,30,10,235)",    bg2="rgba(18,17,5,232)",
    hdr="rgba(255,214,10,30)",  tab="rgba(18,17,5,105)",
    bdt="rgba(255,240,130,62)", brd="rgba(200,188,60,20)",   brh="rgba(255,214,10,55)",
    acc="rgba(255,214,10,255)", ac2="rgba(255,240,130,252)",
    crd="rgba(52,50,18,162)",   crh="rgba(68,65,25,188)",
    sts="rgba(10,10,3,145)",    cbo="rgba(40,38,12,172)",    pop="rgba(22,20,6,252)",
    trk="rgba(48,45,15,175)",   div="rgba(200,188,60,20)",   tof="rgba(30,28,8,215)",
    bb="rgba(40,38,12,165)",    bh="rgba(55,52,18,195)",     bt="rgba(255,240,130,245)",
    cbf="rgba(25,20,0,252)",
)

# ── TITANIUM — Apple light system colors #F2F2F7 · only light theme ───────
_TITANIUM = dict(
    fg="rgba(0,0,0,218)",        fg2="rgba(0,0,0,142)",       fg3="rgba(0,0,0,82)",
    fgt="rgba(0,0,0,235)",
    bg0="rgba(242,242,247,242)", bg1="rgba(229,229,234,238)", bg2="rgba(216,216,221,235)",
    hdr="rgba(255,255,255,158)", tab="rgba(232,232,237,115)",
    bdt="rgba(255,255,255,245)", brd="rgba(0,0,0,20)",         brh="rgba(94,92,230,85)",
    acc="rgba(94,92,230,255)",   ac2="rgba(155,122,245,248)",
    crd="rgba(255,255,255,172)", crh="rgba(255,255,255,218)",
    sts="rgba(209,209,214,148)", cbo="rgba(255,255,255,188)",  pop="rgba(242,242,247,252)",
    trk="rgba(199,199,204,172)", div="rgba(0,0,0,15)",          tof="rgba(188,188,192,215)",
    bb="rgba(255,255,255,175)",  bh="rgba(255,255,255,225)",   bt="rgba(94,92,230,252)",
    cbf="rgba(255,255,255,252)",
)

# ── ROSE GOLD — Apple rose-gold warm bronze metallic glass ────────────────
_ROSE_GOLD = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(88,55,18,240)",   bg1="rgba(65,38,8,235)",     bg2="rgba(42,22,2,232)",
    hdr="rgba(255,188,60,32)",  tab="rgba(38,22,2,105)",
    bdt="rgba(255,232,148,62)", brd="rgba(200,155,45,20)",   brh="rgba(255,188,60,58)",
    acc="rgba(255,188,60,255)", ac2="rgba(255,228,128,252)",
    crd="rgba(100,65,20,162)",  crh="rgba(122,80,28,188)",
    sts="rgba(25,15,2,145)",    cbo="rgba(72,48,12,172)",    pop="rgba(40,25,2,252)",
    trk="rgba(82,55,15,175)",   div="rgba(200,155,45,20)",   tof="rgba(58,38,8,215)",
    bb="rgba(72,48,12,165)",    bh="rgba(95,62,18,195)",     bt="rgba(255,232,128,245)",
    cbf="rgba(255,255,255,252)",
)

# ── ECLIPSE — Apple true-dark #1C1C1E + indigo/purple · Raycast-inspired ──
_ECLIPSE = dict(
    fg="rgba(255,255,255,242)",  fg2="rgba(255,255,255,172)",  fg3="rgba(255,255,255,108)",
    fgt="rgba(255,255,255,255)",
    bg0="rgba(28,28,30,245)",   bg1="rgba(35,32,45,242)",    bg2="rgba(22,22,25,248)",
    hdr="rgba(94,92,230,28)",   tab="rgba(18,18,20,112)",
    bdt="rgba(255,255,255,35)", brd="rgba(255,255,255,15)",  brh="rgba(191,90,242,68)",
    acc="rgba(191,90,242,255)", ac2="rgba(94,92,230,252)",
    crd="rgba(44,44,46,168)",   crh="rgba(58,58,60,198)",
    sts="rgba(15,15,17,148)",   cbo="rgba(44,44,46,182)",    pop="rgba(28,28,30,252)",
    trk="rgba(58,58,60,178)",   div="rgba(255,255,255,12)",  tof="rgba(58,58,60,215)",
    bb="rgba(44,44,46,172)",    bh="rgba(58,58,60,202)",     bt="rgba(218,148,250,245)",
    cbf="rgba(255,255,255,252)",
)


# ── Original themes (preserved verbatim) ──────────────────────────────────

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
#StorageBtn[active="true"] {
    background: rgba(45, 53, 97, 148);
    border-color: rgba(124, 58, 237, 198);
    color: rgba(196, 181, 253, 238);
}
"""


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


# ── Generated themes ───────────────────────────────────────────────────────

STYLESHEET_MIDNIGHT_INDIGO = _glass(**_MIDNIGHT_INDIGO)
STYLESHEET_INFRARED        = _glass(**_INFRARED)
STYLESHEET_PACIFIC_BLUE    = _glass(**_PACIFIC_BLUE)
STYLESHEET_MIDNIGHT_GREEN  = _glass(**_MIDNIGHT_GREEN)
STYLESHEET_DESERT_SUNSET   = _glass(**_DESERT_SUNSET)
STYLESHEET_DEEP_PURPLE     = _glass(**_DEEP_PURPLE)
STYLESHEET_OLIVE_NIGHT     = _glass(**_OLIVE_NIGHT)
STYLESHEET_TITANIUM        = _glass(**_TITANIUM)
STYLESHEET_ROSE_GOLD       = _glass(**_ROSE_GOLD)
STYLESHEET_ECLIPSE         = _glass(**_ECLIPSE)


# ── Theme registry ─────────────────────────────────────────────────────────

# Ordered: shown in Settings combobox exactly as listed here.
# Key = Settings.theme value stored in settings.json
THEME_NAMES: dict[str, str] = {
    "glass":     "Midnight Indigo",   # Apple Indigo on deep space glass (default)
    "rose":      "Infrared",          # Apple Pink on deep crimson glass
    "sky":       "Pacific Blue",      # Apple Blue · iPhone 12 Pro ocean glass
    "mint":      "Midnight Green",    # Apple Green · iPhone 11 Pro forest glass
    "peach":     "Desert Sunset",     # Apple Orange · macOS Sequoia amber glass
    "lavender":  "Deep Purple",       # Apple Purple · space violet glass
    "sage":      "Olive Night",       # Apple Yellow · dark warm olive glass
    "arctic":    "Titanium",          # light · Apple system silver backgrounds
    "champagne": "Rose Gold",         # Apple rose-gold warm metallic glass
    "neon":      "Eclipse",           # Apple true-dark + indigo/purple
    "dark":      "Flat Dark",         # opaque dark (legacy)
}

STYLESHEETS: dict[str, str] = {
    "glass":     STYLESHEET_MIDNIGHT_INDIGO,
    "rose":      STYLESHEET_INFRARED,
    "sky":       STYLESHEET_PACIFIC_BLUE,
    "mint":      STYLESHEET_MIDNIGHT_GREEN,
    "peach":     STYLESHEET_DESERT_SUNSET,
    "lavender":  STYLESHEET_DEEP_PURPLE,
    "sage":      STYLESHEET_OLIVE_NIGHT,
    "arctic":    STYLESHEET_TITANIUM,
    "champagne": STYLESHEET_ROSE_GOLD,
    "neon":      STYLESHEET_ECLIPSE,
    "dark":      STYLESHEET_DARK,
}


CHECKMARK_CHECKED = """
QCheckBox::indicator:checked {
    background-color: #7c3aed;
    border-color: #7c3aed;
}
"""
