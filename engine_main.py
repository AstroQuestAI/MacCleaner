"""Entry point for the lean maccleaner-engine binary."""
import sys, os
if getattr(sys, "frozen", False):
    sys.path.insert(0, os.path.join(sys._MEIPASS, "src"))
from maccleaner.engine_cli import main
sys.exit(main())
