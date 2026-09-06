#!/usr/bin/env bash
# App launcher menu: curated list from apps.txt via rofi (spawned from the panel corner).
set -e

CONF="$HOME/.config/herbstluftwm"
APPS="$CONF/apps.txt"

[ -f "$APPS" ] || exit 0

choice=$(grep -v '^\s*#' "$APPS" | grep -v '^\s*$' | rofi -dmenu -i -p "Launch:") || true

# grep may exit 1 when no matches/empty file after filtering
[ -z "$choice" ] && exit 0

cmd="${choice#*	}"
[ -z "$cmd" ] && exit 0

setsid nohup bash -c "$cmd" >/dev/null 2>&1 &
disown 2>/dev/null || true
exit 0
