#!/usr/bin/env bash
# Reliable restart of the hlwm dzen panel.
# Note: pkill patterns use [..] brackets so this script never kills its own shell.
#
# The panel is spawned from whatever shell runs this script, and hlwm never
# re-exports its environment into it. If that shell carries a broken
# XDG_DATA_DIRS (no /usr/share, see appmenu.sh), the new panel inherits it and
# every app launched from the corner menu dies with "No GSettings schemas are
# installed" - the restart would silently undo the healing that autostart does.
# Heal it here too, idempotently.
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

pkill -f '[h]erbstluftwm/panel.sh' 2>/dev/null
pkill -f '[d]zen2 -w' 2>/dev/null
sleep 0.3
setsid nohup "$HOME/.config/herbstluftwm/panel.sh" 0 >/tmp/panel.log 2>&1 &
