#!/usr/bin/env bash
# Install the herbstluftwm config from this repository into ~/.config/herbstluftwm.
# Usage: ./install.sh [dest_dir]   (default: $HOME/.config/herbstluftwm)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/herbstluftwm"
SRC_ROFI="$(cd "$(dirname "$0")" && pwd)/rofi"
DEST="${1:-$HOME/.config/herbstluftwm}"
DEST_ROFI="$HOME/.config/rofi"

mkdir -p "$DEST"

for f in "$SRC"/*; do
    [ -f "$f" ] || continue
    cp -v "$f" "$DEST/$(basename "$f")"
    chmod +x "$DEST/$(basename "$f")" 2>/dev/null || true
done

if [ -d "$SRC_ROFI" ]; then
    mkdir -p "$DEST_ROFI"
    cp -v "$SRC_ROFI"/* "$DEST_ROFI/"
fi

echo
echo "Config installed to: $DEST"
echo "Rofi theme installed to: $DEST_ROFI"
echo "Apply it now (running session): herbstclient reload"
echo "For a fresh session, just log in to herbstluftwm again."