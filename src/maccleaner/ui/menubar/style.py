"""QSS stylesheets for MacCleaner.

STYLESHEET_GLASS  — default frosted-glass look (Midnight Navy)
STYLESHEET_DARK   — flat opaque dark theme
9 additional glass themes generated via _glass()
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
#   brh         border hover                          sts  status bar bg
#   cbo         combo/input bg                        pop  combo popup bg
#   trk         progress / slider track               div  divider
#   tof         toggle unchecked                      bb   secondary btn bg
#   bh          secondary btn hover                   bt   secondary btn text
#   cbf         primary action btn foreground (Clean/Save)

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
    border-top-color: «brh»;
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

_ROSE = dict(
    fg="rgba(55,12,28,230)",   fg2="rgba(110,42,62,212)",  fg3="rgba(158,88,108,188)",
    fgt="rgba(38,6,18,242)",
    bg0="rgba(255,228,235,212)", bg1="rgba(248,208,220,202)", bg2="rgba(238,185,205,198)",
    hdr="rgba(252,200,215,90)", tab="rgba(255,238,244,85)",
    acc="rgba(185,35,70,238)",  ac2="rgba(225,75,105,225)",
    crd="rgba(255,212,225,138)", crh="rgba(248,192,210,170)",
    brd="rgba(218,132,160,65)", brh="rgba(192,72,102,92)",
    sts="rgba(255,243,248,120)", cbo="rgba(255,218,230,158)", pop="rgba(252,205,220,242)",
    trk="rgba(238,180,200,142)", div="rgba(215,148,170,108)", tof="rgba(225,162,182,195)",
    bb="rgba(255,212,225,142)",  bh="rgba(248,192,210,175)",  bt="rgba(185,35,70,238)",
    cbf="rgba(255,255,255,242)",
)

_SKY = dict(
    fg="rgba(8,32,72,230)",    fg2="rgba(32,72,132,212)",  fg3="rgba(72,112,172,188)",
    fgt="rgba(4,18,52,242)",
    bg0="rgba(208,232,255,212)", bg1="rgba(182,215,252,202)", bg2="rgba(155,198,250,198)",
    hdr="rgba(188,222,255,88)", tab="rgba(218,240,255,85)",
    acc="rgba(15,95,215,238)",  ac2="rgba(55,135,248,225)",
    crd="rgba(188,220,255,138)", crh="rgba(165,208,252,170)",
    brd="rgba(98,168,238,62)",  brh="rgba(28,108,222,90)",
    sts="rgba(222,240,255,118)", cbo="rgba(192,225,255,158)", pop="rgba(202,232,255,242)",
    trk="rgba(152,198,248,142)", div="rgba(115,182,242,108)", tof="rgba(138,192,245,195)",
    bb="rgba(188,220,255,142)",  bh="rgba(165,208,252,175)",  bt="rgba(15,95,215,238)",
    cbf="rgba(255,255,255,242)",
)

_MINT = dict(
    fg="rgba(5,42,25,230)",    fg2="rgba(22,85,52,212)",   fg3="rgba(58,125,85,188)",
    fgt="rgba(2,26,15,242)",
    bg0="rgba(198,245,222,212)", bg1="rgba(172,230,200,202)", bg2="rgba(145,215,178,198)",
    hdr="rgba(178,238,208,88)", tab="rgba(208,248,228,85)",
    acc="rgba(12,138,85,238)",  ac2="rgba(48,178,112,225)",
    crd="rgba(172,232,205,138)", crh="rgba(152,220,188,170)",
    brd="rgba(78,192,138,62)",  brh="rgba(22,148,92,90)",
    sts="rgba(212,248,230,118)", cbo="rgba(178,235,210,158)", pop="rgba(188,238,215,242)",
    trk="rgba(138,215,178,142)", div="rgba(98,202,152,108)", tof="rgba(118,208,165,195)",
    bb="rgba(172,232,205,142)",  bh="rgba(152,220,188,175)",  bt="rgba(12,138,85,238)",
    cbf="rgba(255,255,255,242)",
)

_PEACH = dict(
    fg="rgba(58,20,4,230)",    fg2="rgba(112,48,15,212)",  fg3="rgba(162,95,48,188)",
    fgt="rgba(42,12,2,242)",
    bg0="rgba(255,228,202,212)", bg1="rgba(252,212,175,202)", bg2="rgba(248,195,148,198)",
    hdr="rgba(255,215,182,90)", tab="rgba(255,238,218,85)",
    acc="rgba(195,82,18,238)",  ac2="rgba(232,122,38,225)",
    crd="rgba(255,212,175,138)", crh="rgba(250,198,155,172)",
    brd="rgba(228,152,78,65)",  brh="rgba(208,98,32,92)",
    sts="rgba(255,240,222,120)", cbo="rgba(255,218,180,158)", pop="rgba(255,222,188,242)",
    trk="rgba(245,192,145,142)", div="rgba(225,165,98,108)", tof="rgba(235,182,125,195)",
    bb="rgba(255,212,175,142)",  bh="rgba(250,198,155,175)",  bt="rgba(195,82,18,238)",
    cbf="rgba(255,255,255,242)",
)

_LAVENDER = dict(
    fg="rgba(35,12,65,230)",   fg2="rgba(78,38,125,212)",  fg3="rgba(122,82,172,188)",
    fgt="rgba(22,6,48,242)",
    bg0="rgba(235,222,255,212)", bg1="rgba(218,202,252,202)", bg2="rgba(200,180,248,198)",
    hdr="rgba(228,212,255,90)", tab="rgba(242,235,255,85)",
    acc="rgba(110,38,205,238)", ac2="rgba(148,78,242,225)",
    crd="rgba(218,198,252,138)", crh="rgba(202,178,248,170)",
    brd="rgba(165,122,232,65)", brh="rgba(125,62,212,92)",
    sts="rgba(240,232,255,120)", cbo="rgba(220,202,252,158)", pop="rgba(225,208,252,242)",
    trk="rgba(188,162,242,142)", div="rgba(172,135,232,108)", tof="rgba(185,152,235,195)",
    bb="rgba(218,198,252,142)",  bh="rgba(202,178,248,175)",  bt="rgba(110,38,205,238)",
    cbf="rgba(255,255,255,242)",
)

_SAGE = dict(
    fg="rgba(15,38,20,230)",   fg2="rgba(42,85,50,212)",   fg3="rgba(82,125,88,188)",
    fgt="rgba(8,24,12,242)",
    bg0="rgba(202,222,206,212)", bg1="rgba(178,205,182,202)", bg2="rgba(155,188,160,198)",
    hdr="rgba(190,215,194,88)", tab="rgba(212,230,215,85)",
    acc="rgba(45,105,58,238)",  ac2="rgba(85,148,95,225)",
    crd="rgba(178,212,184,138)", crh="rgba(158,198,165,170)",
    brd="rgba(102,162,112,62)", brh="rgba(52,118,65,90)",
    sts="rgba(215,232,218,118)", cbo="rgba(185,215,190,158)", pop="rgba(192,220,198,242)",
    trk="rgba(145,192,155,142)", div="rgba(115,168,125,108)", tof="rgba(135,182,145,195)",
    bb="rgba(178,212,184,142)",  bh="rgba(158,198,165,175)",  bt="rgba(45,105,58,238)",
    cbf="rgba(255,255,255,242)",
)

_ARCTIC = dict(
    fg="rgba(6,25,55,232)",    fg2="rgba(22,58,108,215)",  fg3="rgba(58,98,152,192)",
    fgt="rgba(2,14,38,242)",
    bg0="rgba(240,248,255,215)", bg1="rgba(225,240,255,205)", bg2="rgba(208,232,255,202)",
    hdr="rgba(232,245,255,90)", tab="rgba(245,252,255,85)",
    acc="rgba(0,78,175,242)",   ac2="rgba(28,118,222,230)",
    crd="rgba(220,240,255,145)", crh="rgba(202,232,255,175)",
    brd="rgba(98,165,228,65)",  brh="rgba(32,108,212,92)",
    sts="rgba(236,247,255,122)", cbo="rgba(222,242,255,162)", pop="rgba(228,244,255,242)",
    trk="rgba(182,225,255,148)", div="rgba(145,202,245,112)", tof="rgba(165,215,248,198)",
    bb="rgba(220,240,255,148)",  bh="rgba(202,232,255,178)",  bt="rgba(0,78,175,242)",
    cbf="rgba(255,255,255,242)",
)

_CHAMPAGNE = dict(
    fg="rgba(52,30,0,232)",    fg2="rgba(105,70,8,215)",   fg3="rgba(155,115,38,192)",
    fgt="rgba(38,20,0,242)",
    bg0="rgba(255,246,208,212)", bg1="rgba(252,236,172,202)", bg2="rgba(248,222,138,198)",
    hdr="rgba(255,242,192,90)", tab="rgba(255,250,225,85)",
    acc="rgba(162,108,0,240)",  ac2="rgba(208,148,18,228)",
    crd="rgba(252,235,165,140)", crh="rgba(248,222,140,172)",
    brd="rgba(208,172,58,65)",  brh="rgba(178,128,10,92)",
    sts="rgba(255,250,222,122)", cbo="rgba(255,240,170,160)", pop="rgba(255,244,182,242)",
    trk="rgba(245,212,118,145)", div="rgba(218,178,65,110)",  tof="rgba(230,195,85,198)",
    bb="rgba(252,235,165,145)",  bh="rgba(248,222,140,178)",  bt="rgba(162,108,0,240)",
    cbf="rgba(255,255,255,242)",
)

_NEON = dict(
    fg="rgba(198,255,238,240)", fg2="rgba(125,228,198,218)", fg3="rgba(78,172,145,192)",
    fgt="rgba(228,255,248,250)",
    bg0="rgba(8,2,22,215)",    bg1="rgba(12,4,32,208)",    bg2="rgba(5,0,18,220)",
    hdr="rgba(0,255,178,22)",   tab="rgba(4,0,12,100)",
    acc="rgba(0,238,178,248)",  ac2="rgba(195,0,252,242)",
    crd="rgba(0,28,22,155)",    crh="rgba(0,42,32,182)",
    brd="rgba(0,198,148,45)",   brh="rgba(0,238,178,72)",
    sts="rgba(2,0,10,138)",     cbo="rgba(0,22,18,178)",    pop="rgba(0,18,14,248)",
    trk="rgba(0,58,42,155)",    div="rgba(0,148,110,102)",  tof="rgba(0,52,40,208)",
    bb="rgba(0,22,18,160)",     bh="rgba(0,38,28,195)",     bt="rgba(0,238,178,242)",
    cbf="rgba(6,16,12,242)",
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

STYLESHEET_ROSE       = _glass(**_ROSE)
STYLESHEET_SKY        = _glass(**_SKY)
STYLESHEET_MINT       = _glass(**_MINT)
STYLESHEET_PEACH      = _glass(**_PEACH)
STYLESHEET_LAVENDER   = _glass(**_LAVENDER)
STYLESHEET_SAGE       = _glass(**_SAGE)
STYLESHEET_ARCTIC     = _glass(**_ARCTIC)
STYLESHEET_CHAMPAGNE  = _glass(**_CHAMPAGNE)
STYLESHEET_NEON       = _glass(**_NEON)


# ── Theme registry ─────────────────────────────────────────────────────────

# Ordered: shown in Settings combobox exactly as listed here.
# Key = Settings.theme value stored in settings.json
THEME_NAMES: dict[str, str] = {
    "glass":     "Midnight Navy",    # dark glass (default)
    "rose":      "Rose Quartz",      # light · warm pink
    "sky":       "Sky Frost",        # light · cool blue
    "mint":      "Fresh Mint",       # light · mint green
    "peach":     "Peach Glow",       # light · warm peach
    "lavender":  "Lavender Dream",   # light · soft purple
    "sage":      "Sage Breeze",      # light · earthy green
    "arctic":    "Arctic Ice",       # light · icy white
    "champagne": "Champagne Gold",   # light · warm gold
    "neon":      "Neon Edge",        # vivid · electric
    "dark":      "Flat Dark",        # opaque dark (legacy)
}

STYLESHEETS: dict[str, str] = {
    "glass":     STYLESHEET_GLASS,
    "rose":      STYLESHEET_ROSE,
    "sky":       STYLESHEET_SKY,
    "mint":      STYLESHEET_MINT,
    "peach":     STYLESHEET_PEACH,
    "lavender":  STYLESHEET_LAVENDER,
    "sage":      STYLESHEET_SAGE,
    "arctic":    STYLESHEET_ARCTIC,
    "champagne": STYLESHEET_CHAMPAGNE,
    "neon":      STYLESHEET_NEON,
    "dark":      STYLESHEET_DARK,
}


CHECKMARK_CHECKED = """
QCheckBox::indicator:checked {
    background-color: #7c3aed;
    border-color: #7c3aed;
}
"""
