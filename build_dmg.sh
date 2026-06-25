#!/usr/bin/env bash
# Build MacCleaner.app (Swift + Python engine) + MacCleaner.dmg locally
# Usage: ./build_dmg.sh [version]
set -euo pipefail

VERSION="${1:-2.0.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
APP="$DIST_DIR/MacCleaner.app"
DMG_NAME="MacCleaner-$VERSION.dmg"
DMG_OUT="$DIST_DIR/$DMG_NAME"

echo "==> MacCleaner build — v$VERSION"

# ── 1. Ensure venv exists for Python engine ───────────────────────────────
if [[ ! -f "$SCRIPT_DIR/.venv/bin/python" ]]; then
  echo "    creating .venv..."
  python3 -m venv "$SCRIPT_DIR/.venv"
fi

source "$SCRIPT_DIR/.venv/bin/activate"

# ── 2. Install / upgrade Python deps (engine only — no PySide6) ──────────
echo "==> Installing Python engine dependencies..."
pip install -q --upgrade pip
pip install -q \
  "pyinstaller>=6" \
  send2trash \
  psutil \
  pyobjc-framework-Cocoa

pip install -q -e "$SCRIPT_DIR"

# ── 3. Build Apple Intelligence bridge (maccleaner-ai, 131 KB) ──────────
echo "==> Building Apple Intelligence bridge..."
"$SCRIPT_DIR/swift-ai/build.sh"

# ── 4. Build lean Python engine (9 MB, no PySide6) ──────────────────────
echo "==> Building Python engine..."
cd "$SCRIPT_DIR"
pyinstaller engine.spec --noconfirm --clean

echo "   Engine: $(du -sh "$DIST_DIR/maccleaner-engine" | cut -f1)"

# ── 5. Build native Swift app (552 KB binary + 9 MB engine) ─────────────
echo "==> Building native Swift app..."
"$SCRIPT_DIR/swift-app/build.sh" --release

SWIFT_BUILD="$SCRIPT_DIR/swift-app/.build/MacCleaner.app"
rm -rf "$APP"
cp -R "$SWIFT_BUILD" "$APP"

echo "   App: $(du -sh "$APP" | cut -f1)"

# ── 6. Package into .dmg ─────────────────────────────────────────────────
echo "==> Creating DMG..."
rm -f "$DMG_OUT"

# Stage only MacCleaner.app — avoids bundling engine/old-DMGs from dist/
DMG_STAGE=$(mktemp -d)
cp -R "$APP" "$DMG_STAGE/MacCleaner.app"

create-dmg \
  --volname "MacCleaner" \
  --volicon "assets/MacCleaner.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "MacCleaner.app" 150 180 \
  --hide-extension "MacCleaner.app" \
  --app-drop-link 450 180 \
  --background "assets/dmg_background.png" \
  --no-internet-enable \
  "$DMG_OUT" \
  "$DMG_STAGE/"

rm -rf "$DMG_STAGE"

echo ""
echo "✅ Done!"
echo "   App:  $APP  ($(du -sh "$APP" | cut -f1))"
echo "   DMG:  $DMG_OUT"
echo ""
echo "To test: open \"$APP\""
