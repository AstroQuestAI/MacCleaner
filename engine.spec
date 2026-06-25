# -*- mode: python ; coding: utf-8 -*-
"""
Lean engine spec — NO PySide6, NO Qt.
Produces: dist/maccleaner-engine  (~18 MB vs 642 MB for full bundle)
Build:    .venv/bin/pyinstaller engine.spec --noconfirm --clean
"""

a = Analysis(
    ["engine_main.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        ("src/maccleaner", "maccleaner"),
        ("swift-ai/maccleaner-ai", "."),   # Apple Intelligence bridge
    ],
    hiddenimports=[
        "maccleaner.engine_cli",
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
        "send2trash",
        "psutil",
        "objc",
        "Foundation",
        "UserNotifications",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "PySide6", "PyQt6", "PyQt5", "wx", "tkinter",
        "unittest", "pytest", "pip", "setuptools",
        "rich",       # not needed in headless engine
        "Cocoa",      # keep lightweight — only UserNotifications needed
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="maccleaner-engine",
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,           # strip debug symbols → smaller binary
    upx=False,
    console=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,         # single binary, no dist/ folder
)
