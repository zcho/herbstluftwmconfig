#!/usr/bin/env bash
# Install the herbstluftwm config from this repository into ~/.config/herbstluftwm.
# Usage: ./install.sh [dest_dir]   (default: $HOME/.config/herbstluftwm)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/herbstluftwm"
SRC_ROFI="$(cd "$(dirname "$0")" && pwd)/rofi"
SRC_ALACRITTY="$(cd "$(dirname "$0")" && pwd)/alacritty"
SRC_BIN="$(cd "$(dirname "$0")" && pwd)/bin"
SRC_DESKTOP="$(cd "$(dirname "$0")" && pwd)/applications"
DEST="${1:-$HOME/.config/herbstluftwm}"
DEST_ROFI="$HOME/.config/rofi"
DEST_ALACRITTY="$HOME/.config/alacritty"
DEST_BIN="$HOME/.local/bin"
DEST_DESKTOP="$HOME/.local/share/applications"

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

if [ -d "$SRC_ALACRITTY" ]; then
    mkdir -p "$DEST_ALACRITTY"
    cp -v "$SRC_ALACRITTY"/* "$DEST_ALACRITTY/"
fi

if [ -d "$SRC_BIN" ]; then
    mkdir -p "$DEST_BIN"
    for f in "$SRC_BIN"/*; do
        [ -f "$f" ] || continue
        cp -v "$f" "$DEST_BIN/$(basename "$f")"
        chmod +x "$DEST_BIN/$(basename "$f")"
    done
fi

if [ -d "$SRC_DESKTOP" ]; then
    mkdir -p "$DEST_DESKTOP"
    for tpl in "$SRC_DESKTOP"/*.tpl; do
        [ -f "$tpl" ] || continue
        out="$DEST_DESKTOP/$(basename "$tpl" .tpl)"
        sed "s|__HIDDIFY_WRAPPER__|$DEST_BIN/brave-hiddify|g" "$tpl" > "$out"
        echo "installed: $out"
    done
fi

echo
echo "Config installed to: $DEST"
echo "Rofi theme installed to: $DEST_ROFI"
echo "Alacritty config installed to: $DEST_ALACRITTY"
echo "Helpers installed to: $DEST_BIN"
echo "Apply it now (running session): herbstclient reload"
echo "For a fresh session, just log in to herbstluftwm again."