#!/usr/bin/env bash
# Compile maccleaner-ai — the Apple Intelligence bridge (no Xcode needed)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK="$(xcrun --show-sdk-path)"
OUT="$SCRIPT_DIR/maccleaner-ai"

echo "==> Compiling maccleaner-ai (FoundationModels bridge)..."
swiftc \
  -sdk "$SDK" \
  -target arm64-apple-macosx26.0 \
  -framework Foundation \
  -framework FoundationModels \
  -O \
  "$SCRIPT_DIR/maccleaner-ai.swift" \
  -o "$OUT"

codesign --force --sign - "$OUT" 2>/dev/null || true
cp "$OUT" "$SCRIPT_DIR/../dist/maccleaner-ai"

SIZE=$(du -sh "$OUT" | cut -f1)
echo "✅ maccleaner-ai built: $SIZE  →  dist/maccleaner-ai"
echo ""
echo "Test: echo '{\"cmd\":\"available\"}' | $OUT"
