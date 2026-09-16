# AGENTS.md

Deployable dotfiles for a **herbstluftwm 0.9.5** desktop on Ubuntu 24.04 (dzen2 panel, rofi window switcher, ru/us layout toggle). Deployed from this repo to `~/.config/herbstluftwm/` via `./install.sh`; pushed to GitHub `origin` (git@github.com:zcho/herbstluftwmconfig.git, branch `master`).

## Layout
- `herbstluftwm/autostart` — full hlwm config (keybinds, theme colors, rules, panel launch). Autostart is re-run on `herbstclient reload`.
- `herbstluftwm/panel.sh` — dzen2 panel: tags, clickable window taskbar (current tag), Kbd/Bat/Net/Vol/date blocks, corner `⛧` dual button (LMB app menu / RMB window switcher).
- `herbstluftwm/{xkbget.py,xkbtoggle.py}` — layout detection/toggle via X11 ctypes (`XkbGetState`/`XkbLockGroup`).
- `herbstluftwm/textwidth.py` — panel right-side width measurement **Pango/Cairo** (`python3-gi`, `python3-cairo`), not PIL. PIL was tried and abandoned (undermeasures ~100px).
- `herbstluftwm/apps.txt` — launcher list for the corner menu. Also lives at `~/.config/herbstluftwm/apps.txt`; keep both in sync.
- `alacritty/alacritty.yml` — terminal config with `Ctrl+Shift+C` copy + `save_to_clipboard` (deployed to `~/.config/alacritty/`).
- `bin/brave-hiddify` — Brave launcher: adds `--proxy-server="http://127.0.0.1:12334"` only while Hiddify's mixed port 12334 listens; otherwise plain Brave (`ss -ltn | grep 127.0.0.1:12334` decides).
- `applications/*.tpl` — desktop overrides; `install.sh` renders them (sed `__HIDDIFY_WRAPPER__` → `$HOME/.local/bin/brave-hiddify`). Never commit an absolute `/home/zcho` path in the `.tpl`.
- `herbstluftwm/restart_panel.sh` — restarts the panel (see gotchas).
- `install.sh` — deploys hlwm/rofi/alacritty/`bin`/desktop overrides. README.md is the setup manual (Russian).

## Gotchas (agent will miss these)
- **Two copies of config**: this repo and the live `~/.config/herbstluftwm/`. Edits usually belong in BOTH — change the live file, then `cp` into repo (or edit repo then run `install.sh`). No symlink exists. Applies to `apps.txt` too.
- **Hiddify (v2.0.5) has no TUN on Linux desktop**: the `ServiceMode` enum only carries `none`/`proxy`. Setting pref `flutter.service-mode` to `tun` breaks core startup (`No element`). Proxy mode is the only working mode; mixed inbound is `127.0.0.1:12334`.
- **HiddifyTunnelService.service dies with `./lib/libcore.so` (exit 127)** unless the unit has `WorkingDirectory=/usr/share/hiddify` in `[Service]`. It is only needed for TUN mode (currently unused).
- **Colors**: the bright active color lives in TWO separate keys that must stay in sync: `theme.active.color` (window frame) and `window_border_active_color` (panel `selbg`, read directly by `panel.sh`). The latter is not set in stock config and must be set explicitly.
- **hlwm 0.9.5 has no `activate` command** — use `jumpto <winid>` to focus a window (it also switches tag).
- **Portability**: keep paths `$HOME`/`~`-relative; never reintroduce `/home/zcho` hardcodes (verify with `grep -rn "zcho\\|/home/" herbstluftwm/ install.sh`; the `.tpl` uses `__HIDDIFY_WRAPPER__` instead).
- **`restart_panel.sh`** uses pkill patterns with `[h]erbstluftwm/panel.sh` / `[d]zen2 -w` bracket trick so it doesn't kill its own shell. On the live machine a copy may live at `/tmp/restart_panel.sh` (recreate from repo if /tmp was cleared).
- **`xkbget.py`** detects layout by the keysym of keycode 33 (`P`): `p`(0x70)→`us`, `з`(0x6da)→`ru`. Do not "simplify" it to a group-index lookup — that was the actual historical bug.
- Right after `herbstclient reload`, attribute reads can race autostart and show stale values; re-query.

## Commands
- Apply config: `herbstclient reload`
- Restart panel: `restart_panel.sh` (from repo, or `/tmp/restart_panel.sh` on the machine)
- Validate: `bash -n` on `*.sh` (autostart/panel.sh/restart_panel.sh/install.sh); `python3 -m py_compile herbstluftwm/*.py`
- Sync live→repo: `cp ~/.config/herbstluftwm/{autostart,panel.sh,xkbget.py,xkbtoggle.py,textwidth.py} herbstluftwm/`
- Deploy repo→live: `./install.sh`
- Commit/push only when the user asks (they do so explicitly).