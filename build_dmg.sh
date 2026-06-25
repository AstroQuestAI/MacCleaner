#!/usr/bin/env bash
# Build MacCleaner.app (pure native Swift) + MacCleaner.dmg
# No Python. No pip. No PyInstaller.
# Usage: ./build_dmg.sh [version]
set -euo pipefail

VERSION="${1:-2.0.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
APP="$DIST_DIR/MacCleaner.app"
DMG_NAME="MacCleaner-$VERSION.dmg"
DMG_OUT="$DIST_DIR/$DMG_NAME"

mkdir -p "$DIST_DIR"

echo "==> MacCleaner build — v$VERSION (fully native Swift)"

# ── 1. Build native Swift app ─────────────────────────────────────────────
echo "==> Building native Swift app..."
"$SCRIPT_DIR/swift-app/build.sh" --release

SWIFT_BUILD="$SCRIPT_DIR/swift-app/.build/MacCleaner.app"
rm -rf "$APP"
cp -R "$SWIFT_BUILD" "$APP"

echo "   App: $(du -sh "$APP" | cut -f1)"

# ── 2. Package into .dmg ──────────────────────────────────────────────────
echo "==> Creating DMG..."
rm -f "$DMG_OUT"

# Stage only MacCleaner.app — avoids bundling stale files from dist/
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
