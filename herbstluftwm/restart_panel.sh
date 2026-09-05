#!/usr/bin/env bash
# Reliable restart of the hlwm dzen panel.
# Note: pkill patterns use [..] brackets so this script never kills its own shell.
pkill -f '[h]erbstluftwm/panel.sh' 2>/dev/null
pkill -f '[d]zen2 -w' 2>/dev/null
sleep 0.3
setsid nohup "$HOME/.config/herbstluftwm/panel.sh" 0 >/tmp/panel.log 2>&1 &