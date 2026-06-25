#!/usr/bin/env bash
# Build the Swift MacCleaner.app shell using swiftc (no full Xcode needed)
# Embeds the lean Python engine binary (dist/maccleaner-engine)
#
# Usage: ./build.sh [--release]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."
RELEASE="${1:-}"

APP_NAME="MacCleaner"
BUILD_DIR="$SCRIPT_DIR/.build"
APP_BUNDLE="$BUILD_DIR/$APP_NAME.app"
CONTENTS="$APP_BUNDLE/Contents"
MACOS="$CONTENTS/MacOS"
RESOURCES="$CONTENTS/Resources"
ENGINE_BINARY="$ROOT/dist/maccleaner-engine"
SWIFT_BIN="$MACOS/MacCleanerApp"

# Prefer Xcode toolchain over CLT (needed for SwiftUI macros + FoundationModels)
XCODE_DEV="/Applications/Xcode.app/Contents/Developer"
if [[ -d "$XCODE_DEV" ]]; then
    SWIFTC="$XCODE_DEV/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc"
    SDK="$XCODE_DEV/Platforms/MacOSX.platform/Developer/SDKs/MacOSX26.sdk"
else
    SWIFTC="$(xcrun --find swiftc)"
    SDK="$(xcrun --show-sdk-path)"
fi

ARCH="arm64"
TARGET="arm64-apple-macosx26.0"   # FoundationModels requires macOS 26
OPT_FLAG="-Onone -g"
[[ "$RELEASE" == "--release" ]] && OPT_FLAG="-O -whole-module-optimization"

SWIFT_SOURCES=("$SCRIPT_DIR/Sources/MacCleanerApp/"*.swift)

FRAMEWORKS=(
    SwiftUI
    AppKit
    Foundation
    UserNotifications
    AppIntents
    FoundationModels
)

FRAMEWORK_FLAGS=()
for f in "${FRAMEWORKS[@]}"; do
    FRAMEWORK_FLAGS+=(-framework "$f")
done

echo "==> Assembling .app bundle..."
rm -rf "$APP_BUNDLE"
mkdir -p "$MACOS" "$RESOURCES"

cp "$SCRIPT_DIR/Info.plist"        "$CONTENTS/Info.plist"
cp "$ROOT/assets/MacCleaner.icns"  "$RESOURCES/$APP_NAME.icns"

echo "==> Compiling Swift sources ($("$SWIFTC" --version 2>&1 | head -1))..."
"$SWIFTC" \
    -sdk "$SDK" \
    -target "$TARGET" \
    $OPT_FLAG \
    -parse-as-library \
    -module-name MacCleanerApp \
    "${FRAMEWORK_FLAGS[@]}" \
    "${SWIFT_SOURCES[@]}" \
    -o "$SWIFT_BIN"

echo "   ✓ Swift binary: $(du -sh "$SWIFT_BIN" | cut -f1)"

# Embed the Python engine
if [[ -f "$ENGINE_BINARY" ]]; then
    cp "$ENGINE_BINARY" "$MACOS/maccleaner-engine"
    echo "   ✓ Python engine: $(du -sh "$MACOS/maccleaner-engine" | cut -f1)"
else
    echo "   ⚠️  maccleaner-engine not found — run from project root:"
    echo "      .venv/bin/pyinstaller engine.spec --noconfirm --clean"
fi

echo "==> Signing (ad-hoc)..."
# Use dev entitlements for ad-hoc signing (no Siri — that requires a real Developer ID cert)
DEV_ENTITLEMENTS="$SCRIPT_DIR/MacCleaner-dev.entitlements"
if [[ -f "$MACOS/maccleaner-engine" ]]; then
    codesign --force --sign - "$MACOS/maccleaner-engine" 2>/dev/null || true
fi
codesign --force --sign - \
    --entitlements "$DEV_ENTITLEMENTS" \
    "$APP_BUNDLE"

echo ""
echo "✅ Done: $APP_BUNDLE"
APP_MB=$(du -sh "$APP_BUNDLE" | cut -f1)
echo "   Total bundle size: $APP_MB  (engine + Swift binary)"
echo ""
echo "To run: open \"$APP_BUNDLE\""
