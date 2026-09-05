#!/usr/bin/env bash
# Install the herbstluftwm config from this repository into ~/.config/herbstluftwm.
# Usage: ./install.sh [dest_dir]   (default: $HOME/.config/herbstluftwm)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/herbstluftwm"
DEST="${1:-$HOME/.config/herbstluftwm}"

mkdir -p "$DEST"

for f in "$SRC"/*; do
    [ -f "$f" ] || continue
    cp -v "$f" "$DEST/$(basename "$f")"
    chmod +x "$DEST/$(basename "$f")" 2>/dev/null || true
done

echo
echo "Config installed to: $DEST"
echo "Apply it now (running session): herbstclient reload"
echo "For a fresh session, just log in to herbstluftwm again."