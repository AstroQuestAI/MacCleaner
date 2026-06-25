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

# ── ROSE QUARTZ — rich warm berry glass, cherry accents ───────────────────
_ROSE = dict(
    fg="rgba(28,4,12,245)",    fg2="rgba(75,22,40,228)",   fg3="rgba(128,68,88,205)",
    fgt="rgba(15,0,6,252)",
    bg0="rgba(242,162,198,240)", bg1="rgba(225,132,172,236)", bg2="rgba(208,105,150,232)",
    hdr="rgba(255,198,228,125)", tab="rgba(248,178,215,100)",
    bdt="rgba(255,255,255,215)", brd="rgba(205,108,148,75)", brh="rgba(175,55,95,118)",
    acc="rgba(158,18,55,252)",  ac2="rgba(208,48,88,242)",
    crd="rgba(255,210,232,162)", crh="rgba(255,192,220,195)",
    sts="rgba(248,228,240,145)", cbo="rgba(252,208,228,182)", pop="rgba(255,220,238,250)",
    trk="rgba(228,155,188,162)", div="rgba(210,128,162,130)", tof="rgba(218,145,178,220)",
    bb="rgba(252,208,228,165)",  bh="rgba(245,188,215,200)",  bt="rgba(158,18,55,252)",
    cbf="rgba(255,255,255,252)",
)

# ── SKY FROST — deep cerulean glass, cobalt accents ───────────────────────
_SKY = dict(
    fg="rgba(4,18,52,245)",    fg2="rgba(18,52,112,228)",  fg3="rgba(55,95,158,205)",
    fgt="rgba(0,8,35,252)",
    bg0="rgba(128,188,248,240)", bg1="rgba(95,162,242,236)", bg2="rgba(65,138,235,232)",
    hdr="rgba(175,218,255,125)", tab="rgba(148,202,252,100)",
    bdt="rgba(235,248,255,218)", brd="rgba(68,140,225,75)",  brh="rgba(22,95,208,118)",
    acc="rgba(0,72,195,252)",   ac2="rgba(30,115,245,242)",
    crd="rgba(185,222,255,162)", crh="rgba(165,210,255,195)",
    sts="rgba(212,238,255,145)", cbo="rgba(175,218,255,182)", pop="rgba(198,230,255,250)",
    trk="rgba(118,178,245,162)", div="rgba(88,155,232,130)",  tof="rgba(105,168,238,220)",
    bb="rgba(175,218,255,165)",  bh="rgba(155,205,252,200)",  bt="rgba(0,72,195,252)",
    cbf="rgba(255,255,255,252)",
)

# ── FRESH MINT — jade glass, emerald accents ──────────────────────────────
_MINT = dict(
    fg="rgba(2,30,15,245)",    fg2="rgba(12,68,38,228)",   fg3="rgba(42,108,68,205)",
    fgt="rgba(0,18,8,252)",
    bg0="rgba(95,198,155,240)", bg1="rgba(68,178,128,236)", bg2="rgba(42,158,105,232)",
    hdr="rgba(148,225,188,125)", tab="rgba(115,212,168,100)",
    bdt="rgba(218,255,238,215)", brd="rgba(48,158,105,75)",  brh="rgba(15,118,72,118)",
    acc="rgba(0,108,62,252)",   ac2="rgba(28,155,95,242)",
    crd="rgba(178,238,208,162)", crh="rgba(158,228,195,195)",
    sts="rgba(205,245,225,145)", cbo="rgba(165,232,202,182)", pop="rgba(185,242,215,250)",
    trk="rgba(85,182,138,162)", div="rgba(58,158,112,130)",   tof="rgba(72,172,128,220)",
    bb="rgba(165,232,202,165)",  bh="rgba(145,222,188,200)",  bt="rgba(0,108,62,252)",
    cbf="rgba(255,255,255,252)",
)

# ── PEACH GLOW — warm amber glass, burnt-orange accents ──────────────────
_PEACH = dict(
    fg="rgba(35,10,0,245)",    fg2="rgba(88,35,5,228)",    fg3="rgba(145,82,35,205)",
    fgt="rgba(20,4,0,252)",
    bg0="rgba(248,175,108,240)", bg1="rgba(240,152,78,236)", bg2="rgba(232,128,52,232)",
    hdr="rgba(255,210,155,125)", tab="rgba(252,192,128,100)",
    bdt="rgba(255,248,228,215)", brd="rgba(222,138,65,75)",  brh="rgba(195,95,22,118)",
    acc="rgba(168,55,0,252)",   ac2="rgba(218,88,18,242)",
    crd="rgba(255,215,172,162)", crh="rgba(255,200,148,195)",
    sts="rgba(255,238,215,145)", cbo="rgba(255,210,165,182)", pop="rgba(255,225,185,250)",
    trk="rgba(235,165,88,162)", div="rgba(215,138,58,130)",  tof="rgba(228,155,75,220)",
    bb="rgba(255,210,165,165)",  bh="rgba(252,195,142,200)",  bt="rgba(168,55,0,252)",
    cbf="rgba(255,255,255,242)",
)

# ── LAVENDER DREAM — deep violet glass, vivid purple accents ─────────────
_LAVENDER = dict(
    fg="rgba(18,4,42,245)",    fg2="rgba(55,22,108,228)",  fg3="rgba(102,62,162,205)",
    fgt="rgba(8,0,28,252)",
    bg0="rgba(178,128,242,240)", bg1="rgba(155,102,232,236)", bg2="rgba(132,78,222,232)",
    hdr="rgba(215,178,255,125)", tab="rgba(195,152,248,100)",
    bdt="rgba(245,228,255,218)", brd="rgba(148,88,225,78)",  brh="rgba(112,45,205,118)",
    acc="rgba(88,18,198,252)",  ac2="rgba(138,58,242,242)",
    crd="rgba(215,188,255,162)", crh="rgba(200,168,252,195)",
    sts="rgba(232,215,255,145)", cbo="rgba(208,182,252,182)", pop="rgba(222,200,255,250)",
    trk="rgba(162,118,238,162)", div="rgba(138,92,222,130)",  tof="rgba(148,105,228,220)",
    bb="rgba(208,182,252,165)",  bh="rgba(192,162,248,200)",  bt="rgba(88,18,198,252)",
    cbf="rgba(255,255,255,252)",
)

# ── SAGE BREEZE — deep eucalyptus glass, forest accents ──────────────────
_SAGE = dict(
    fg="rgba(4,22,8,245)",     fg2="rgba(18,62,28,228)",   fg3="rgba(52,102,62,205)",
    fgt="rgba(0,12,4,252)",
    bg0="rgba(88,158,105,240)", bg1="rgba(65,138,82,236)",  bg2="rgba(45,118,62,232)",
    hdr="rgba(128,195,148,125)", tab="rgba(105,178,125,100)",
    bdt="rgba(208,242,218,215)", brd="rgba(48,118,65,78)",   brh="rgba(18,88,38,118)",
    acc="rgba(12,88,35,252)",   ac2="rgba(40,132,65,242)",
    crd="rgba(165,222,182,162)", crh="rgba(145,210,165,195)",
    sts="rgba(195,235,205,145)", cbo="rgba(155,215,172,182)", pop="rgba(175,228,190,250)",
    trk="rgba(72,148,92,162)",  div="rgba(48,118,68,130)",   tof="rgba(60,132,78,220)",
    bb="rgba(155,215,172,165)",  bh="rgba(138,205,158,200)",  bt="rgba(12,88,35,252)",
    cbf="rgba(255,255,255,252)",
)

# ── ARCTIC ICE — luminous white-blue glass, deep-navy accents ────────────
_ARCTIC = dict(
    fg="rgba(2,14,42,245)",    fg2="rgba(12,42,92,228)",   fg3="rgba(42,82,138,205)",
    fgt="rgba(0,6,28,252)",
    bg0="rgba(198,228,255,242)", bg1="rgba(178,215,252,238)", bg2="rgba(158,202,250,235)",
    hdr="rgba(235,248,255,130)", tab="rgba(218,240,255,108)",
    bdt="rgba(255,255,255,235)", brd="rgba(88,158,232,80)",   brh="rgba(18,98,215,120)",
    acc="rgba(0,60,182,252)",   ac2="rgba(22,105,238,242)",
    crd="rgba(228,244,255,168)", crh="rgba(210,235,255,200)",
    sts="rgba(240,250,255,150)", cbo="rgba(222,242,255,188)", pop="rgba(232,246,255,252)",
    trk="rgba(155,208,252,168)", div="rgba(118,188,245,135)",  tof="rgba(138,198,248,225)",
    bb="rgba(222,242,255,170)",  bh="rgba(205,232,252,205)",  bt="rgba(0,60,182,252)",
    cbf="rgba(255,255,255,252)",
)

# ── CHAMPAGNE GOLD — warm cognac glass, burnished-bronze accents ──────────
_CHAMPAGNE = dict(
    fg="rgba(25,12,0,245)",    fg2="rgba(72,42,5,228)",    fg3="rgba(128,88,28,205)",
    fgt="rgba(12,5,0,252)",
    bg0="rgba(232,195,108,240)", bg1="rgba(218,172,78,236)", bg2="rgba(205,150,50,232)",
    hdr="rgba(255,228,145,125)", tab="rgba(245,210,118,100)",
    bdt="rgba(255,252,228,218)", brd="rgba(198,158,48,78)",   brh="rgba(162,118,8,118)",
    acc="rgba(128,78,0,252)",   ac2="rgba(188,128,12,242)",
    crd="rgba(255,232,155,165)", crh="rgba(252,218,128,198)",
    sts="rgba(252,242,208,148)", cbo="rgba(248,228,148,185)", pop="rgba(255,238,168,252)",
    trk="rgba(218,178,72,165)", div="rgba(195,152,42,132)",   tof="rgba(208,165,58,222)",
    bb="rgba(248,228,148,168)",  bh="rgba(242,215,125,202)",  bt="rgba(128,78,0,252)",
    cbf="rgba(255,255,255,252)",
)

# ── NEON EDGE — obsidian glass, electric cyan × vivid magenta ────────────
_NEON = dict(
    fg="rgba(185,255,232,245)", fg2="rgba(108,225,188,225)", fg3="rgba(62,165,132,200)",
    fgt="rgba(220,255,245,255)",
    bg0="rgba(6,2,18,232)",    bg1="rgba(10,3,28,228)",    bg2="rgba(4,0,14,235)",
    hdr="rgba(0,255,178,30)",   tab="rgba(3,0,10,108)",
    bdt="rgba(0,255,195,88)",   brd="rgba(0,188,142,52)",   brh="rgba(0,245,182,82)",
    acc="rgba(0,242,182,255)",  ac2="rgba(180,0,255,252)",
    crd="rgba(0,22,16,172)",    crh="rgba(0,35,26,205)",
    sts="rgba(2,0,8,148)",      cbo="rgba(0,18,14,188)",    pop="rgba(0,15,11,252)",
    trk="rgba(0,48,36,165)",    div="rgba(0,135,102,112)",  tof="rgba(0,42,32,218)",
    bb="rgba(0,18,14,175)",     bh="rgba(0,32,24,208)",     bt="rgba(0,242,182,252)",
    cbf="rgba(4,14,10,252)",
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
