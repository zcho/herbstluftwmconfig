#!/usr/bin/env bash
# App launcher menu: curated list from apps.txt via rofi (spawned from the panel corner).
set -e

CONF="$HOME/.config/herbstluftwm"
APPS="$CONF/apps.txt"
LOG="$CONF/appmenu.log"

# GLib looks for GSettings schemas only under $XDG_DATA_DIRS/glib-2.0/schemas. A
# value without /usr/share therefore leaves every GLib app with "No GSettings
# schemas are installed on the system", and Nautilus aborts with a core dump.
# /etc/X11/Xsession.d/60x11-common_xdg_path can produce exactly such a value, and
# this menu inherits whatever environment the panel was started with - so if the
# panel came up before the healing block in autostart ran (e.g. via
# restart_panel.sh), every deb-based GUI app launched from here dies silently.
# Heal it here instead of trusting the ambient environment. Idempotent, and
# mirrors the identical block in autostart.
_xdg_add() {
    case ":${XDG_DATA_DIRS:-}:" in
        *":$1:"*) ;;
        *) XDG_DATA_DIRS="${XDG_DATA_DIRS:+$XDG_DATA_DIRS:}$1" ;;
    esac
}
_xdg_add /usr/local/share
_xdg_add /usr/share
_xdg_add /usr/share/herbstluftwm
_xdg_add /var/lib/snapd/desktop
export XDG_DATA_DIRS
unset -f _xdg_add

[ -f "$APPS" ] || exit 0

choice=$(grep -v '^\s*#' "$APPS" | grep -v '^\s*$' | rofi -dmenu -i -p "Launch:") || true

# grep may exit 1 when no matches/empty file after filtering
[ -z "$choice" ] && exit 0

cmd="${choice#*	}"
[ -z "$cmd" ] && exit 0

# Log rather than discard: a launcher that fails quietly is indistinguishable from
# one that works, which is exactly how a crashing Nautilus went unnoticed. One line
# per launch plus whatever the app itself writes to stderr.
printf '%s launch: %s\n' "$(date '+%F %T')" "$cmd" >>"$LOG"
setsid nohup bash -c "$cmd" >>"$LOG" 2>&1 &
disown 2>/dev/null || true
exit 0
