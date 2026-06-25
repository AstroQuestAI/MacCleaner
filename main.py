"""PyInstaller entry point for MacCleaner .app bundle."""
import sys
import os

# Ensure src/ is on the path when running from bundle
if getattr(sys, "frozen", False):
    sys.path.insert(0, os.path.join(sys._MEIPASS, "src"))

from maccleaner.ui.menubar.app import run

sys.exit(run())
