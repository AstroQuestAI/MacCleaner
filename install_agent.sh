#!/bin/bash
# Install MacCleaner as a macOS Launch Agent that starts at login.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_SRC="$SCRIPT_DIR/com.maccleaner.agent.plist"
AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_DST="$AGENTS_DIR/com.maccleaner.agent.plist"

if [ ! -f "$PLIST_SRC" ]; then
  echo "Error: plist not found at $PLIST_SRC" >&2
  exit 1
fi

# Unload existing agent if running
if launchctl list | grep -q "com.maccleaner.agent" 2>/dev/null; then
  echo "Stopping existing MacCleaner agent..."
  launchctl bootout "gui/$(id -u)/com.maccleaner.agent" 2>/dev/null || true
fi

mkdir -p "$AGENTS_DIR"
cp "$PLIST_SRC" "$PLIST_DST"

launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
echo "MacCleaner agent installed and started."
echo "It will auto-launch at every login. Logs: /tmp/maccleaner.log"
echo ""
echo "To stop:     launchctl bootout gui/\$(id -u)/com.maccleaner.agent"
echo "To uninstall: rm $PLIST_DST && launchctl bootout gui/\$(id -u)/com.maccleaner.agent"
