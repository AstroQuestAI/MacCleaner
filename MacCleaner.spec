# -*- mode: python ; coding: utf-8 -*-
"""
MacCleaner.app — trimmed PySide6 (only 3 Qt modules used).
Target size: ~120 MB (vs 642 MB with collect_all).
Build: .venv/bin/pyinstaller MacCleaner.spec --noconfirm --clean
"""
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# ── Collect ONLY the Qt modules actually used ──────────────────────────────
# QtCore, QtGui, QtWidgets — that's it. No Network, SQL, Multimedia, WebEngine.
_QT_MODULES = ["QtCore", "QtGui", "QtWidgets"]

qt_datas    = []
qt_binaries = []
for mod in _QT_MODULES:
    qt_datas    += collect_data_files(f"PySide6.{mod}", include_py_files=False)
    qt_binaries += collect_dynamic_libs(f"PySide6.{mod}")

# PySide6 plugin data files needed by QtWidgets
qt_datas += collect_data_files("PySide6", subdir="plugins/platforms",   include_py_files=False)
qt_datas += collect_data_files("PySide6", subdir="plugins/styles",      include_py_files=False)
qt_datas += collect_data_files("PySide6", subdir="plugins/imageformats", include_py_files=False)

# Qt framework dylibs (shared across modules)
qt_binaries += collect_dynamic_libs("PySide6")

a = Analysis(
    ["main.py"],
    pathex=["src"],
    binaries=qt_binaries,
    datas=[
        ("src/maccleaner", "maccleaner"),
        *qt_datas,
    ],
    hiddenimports=[
        # PySide6 — only what's imported in source
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "shiboken6",
        # App modules
        "maccleaner",
        "maccleaner.config",
        "maccleaner.models",
        "maccleaner.models.category",
        "maccleaner.models.scan_result",
        "maccleaner.scanners",
        "maccleaner.scanners.base",
        "maccleaner.scanners.browser_scanner",
        "maccleaner.scanners.build_cache_scanner",
        "maccleaner.scanners.cache_scanner",
        "maccleaner.scanners.docker_scanner",
        "maccleaner.scanners.homebrew_scanner",
        "maccleaner.scanners.log_scanner",
        "maccleaner.scanners.mail_scanner",
        "maccleaner.scanners.node_modules_scanner",
        "maccleaner.scanners.node_scanner",
        "maccleaner.scanners.python_cache_scanner",
        "maccleaner.scanners.temp_scanner",
        "maccleaner.scanners.trash_scanner",
        "maccleaner.scanners.venv_scanner",
        "maccleaner.scanners.xcode_scanner",
        "maccleaner.scanners.duplicate_scanner",
        "maccleaner.services",
        "maccleaner.services.cleaner_service",
        "maccleaner.services.storage_analyzer",
        "maccleaner.services.notification_service",
        "maccleaner.ui",
        "maccleaner.ui.cli",
        "maccleaner.ui.dashboard",
        "maccleaner.ui.formatting",
        "maccleaner.ui.menubar",
        "maccleaner.ui.menubar.app",
        "maccleaner.ui.menubar.main_window",
        "maccleaner.ui.menubar.settings_panel",
        "maccleaner.ui.menubar.storage_panel",
        "maccleaner.ui.menubar.style",
        "maccleaner.ui.menubar.workers",
        # Runtime deps
        "rich",
        "rich.console",
        "rich.table",
        "rich.progress",
        "send2trash",
        "psutil",
        "objc",
        "Foundation",
        "AppKit",
        "UserNotifications",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        # Unused Qt modules — major size savers
        "PySide6.QtNetwork",
        "PySide6.QtSql",
        "PySide6.QtXml",
        "PySide6.QtMultimedia",
        "PySide6.QtMultimediaWidgets",
        "PySide6.QtOpenGL",
        "PySide6.QtOpenGLWidgets",
        "PySide6.QtPdf",
        "PySide6.QtPdfWidgets",
        "PySide6.QtPrintSupport",
        "PySide6.QtWebEngine",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebChannel",
        "PySide6.QtBluetooth",
        "PySide6.QtSensors",
        "PySide6.QtLocation",
        "PySide6.QtPositioning",
        "PySide6.QtNfc",
        "PySide6.QtSerialPort",
        "PySide6.QtTest",
        "PySide6.QtConcurrent",
        "PySide6.Qt3DCore",
        "PySide6.Qt3DRender",
        "PySide6.Qt3DInput",
        "PySide6.Qt3DAnimation",
        "PySide6.Qt3DExtras",
        "PySide6.QtDataVisualization",
        "PySide6.QtCharts",
        "PySide6.QtQuick",
        "PySide6.QtQml",
        # Dev tools
        "tkinter", "unittest", "pytest", "pip", "setuptools",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MacCleaner",
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/MacCleaner.icns",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=False,
    upx_exclude=[],
    name="MacCleaner",
)

app = BUNDLE(
    coll,
    name="MacCleaner.app",
    icon="assets/MacCleaner.icns",
    bundle_identifier="com.astroquestai.maccleaner",
    version="1.0.0",
    info_plist={
        "CFBundleName": "MacCleaner",
        "CFBundleDisplayName": "MacCleaner",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSUIElement": True,
        "NSHumanReadableCopyright": "© 2025 AstroQuestAI",
        "NSPrincipalClass": "NSApplication",
        "LSMinimumSystemVersion": "13.0",
    },
)
