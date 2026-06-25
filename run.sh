#!/usr/bin/env bash
# MacCleaner launcher
# Usage:
#   ./run.sh              — menubar GUI app
#   ./run.sh --cli        — terminal CLI
#   ./run.sh --cli --dry-run  — CLI dry run
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

if [[ ! -d "$VENV" ]]; then
  echo "Setting up virtual environment…"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -e "$SCRIPT_DIR/[dev]" -q
fi

if [[ "${1:-}" == "--cli" ]]; then
  shift
  exec "$VENV/bin/maccleaner" "$@"
else
  exec "$VENV/bin/maccleaner-gui" "$@"
fi
