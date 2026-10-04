# AGENTS.md

Deployable dotfiles for a **herbstluftwm 0.9.5** desktop on Ubuntu 24.04 (dzen2 panel, rofi window switcher, ru/us layout toggle). Deployed from this repo to `~/.config/herbstluftwm/` via `./install.sh`; pushed to GitHub `origin` (git@github.com:zcho/herbstluftwmconfig.git, branch `master`).

## Layout
- `herbstluftwm/autostart` — full hlwm config (keybinds, theme colors, rules, panel launch). Autostart is re-run on `herbstclient reload`.
- `herbstluftwm/panel.sh` — dzen2 panel: tags, clickable window taskbar (current tag), Kbd/Bat/Net/Vol/date blocks, corner `⛧` dual button (LMB app menu / RMB window switcher).
- `herbstluftwm/{xkbget.py,xkbtoggle.py}` — layout detection/toggle via X11 ctypes (`XkbGetState`/`XkbLockGroup`).
- `herbstluftwm/textwidth.py` — panel right-side width measurement **Pango/Cairo** (`python3-gi`, `python3-cairo`), not PIL. PIL was tried and abandoned (undermeasures ~100px).
- `herbstluftwm/panel_astro.py` — sunset time (NOAA sun position) + moon illumination %, pure stdlib. Takes `LAT LON` args, prints a dzen markup line (FreeMono `^fn()` glyphs). Coordinates are `LAT`/`LON` at the top of `panel.sh`.
- `herbstluftwm/panel_batip.py` — battery tooltip spawned by left-click on the panel battery block (`^ca(1,...)` in `panel.sh`). **Line 1 is the battery runtime, line 2 is % + watts.** ETA comes from sysfs current (`charge_now / current_now * 60`), gated by `PLAUSIBLE_MIN/MAX` (2 min…36 h) because idle `current_now` yields nonsense like 81 days. Read-only, pure stdlib, closes on click, single instance via `/tmp/panel_batip.pid`.
- `herbstluftwm/apps.txt` — launcher list for the corner menu. Also lives at `~/.config/herbstluftwm/apps.txt`; keep both in sync.
- `alacritty/alacritty.yml` — terminal config with `Ctrl+Shift+C` copy + `save_to_clipboard` (deployed to `~/.config/alacritty/`).
- `bin/brave-hiddify` — Brave launcher: **always** passes `--proxy-server="http://127.0.0.1:12334"` (fail closed — never a silent direct launch) and waits up to 30 s for the mixed port first, because after a reboot Hiddify needs tens of seconds and the old plain-Brave fallback looked exactly like a working browser (symptom: "YouTube does not open"). It also warns when Brave is **already running**: Chromium is single-instance, hands the URL to the live process and silently drops `--proxy-server`, so only a full restart applies it.
- **`applications/*.tpl` must never contain a bare `Exec=/snap/bin/brave`**: every action (`New Window`, `New Incognito Window`, …) has to route through `__HIDDIFY_WRAPPER__`, otherwise that one action escapes the proxy. Verify with `grep -n '^Exec=' applications/*.tpl` — all lines should read `__HIDDIFY_WRAPPER__`.
- `bin/hiddify-gui` — Hiddify launcher, used by the `Hiddify` entry in `apps.txt` (corner `⛧` menu). Raises the existing hlwm window (`jumpto`) instead of starting a second copy. `install.sh` copies `bin/*` automatically — no install.sh change needed for new helpers.
- `applications/*.tpl` — desktop overrides; `install.sh` renders them (sed `__HIDDIFY_WRAPPER__` → `$HOME/.local/bin/brave-hiddify`). Never commit an absolute `/home/zcho` path in the `.tpl`.
- `herbstluftwm/restart_panel.sh` — restarts the panel (see gotchas).
- `install.sh` — deploys hlwm/rofi/alacritty/`bin`/desktop overrides. README.md is the setup manual (Russian).

## Gotchas (agent will miss these)
- **Two copies of config**: this repo and the live `~/.config/herbstluftwm/`. Edits usually belong in BOTH — change the live file, then `cp` into repo (or edit repo then run `install.sh`). No symlink exists. Applies to `apps.txt` too.
- **Hiddify (v2.0.5) has no TUN on Linux desktop**: the `ServiceMode` enum only carries `none`/`proxy`. Setting pref `flutter.service-mode` to `tun` breaks core startup (`No element`). Proxy mode is the only working mode; mixed inbound is `127.0.0.1:12334`.
- **HiddifyTunnelService.service dies with `./lib/libcore.so` (exit 127)** unless the unit has `WorkingDirectory=/usr/share/hiddify` in `[Service]`. It is only needed for TUN mode (currently unused).
- **Colors**: the bright active color lives in TWO separate keys that must stay in sync: `theme.active.color` (window frame) and `window_border_active_color` (panel `selbg`, read directly by `panel.sh`). The latter is not set in stock config and must be set explicitly.
- **bash `printf` `%(...)T` grabs the next argument**: the date-loop line uses THREE separate `printf` runs (`$t`, `$d`, `$astro`) because putting `%(...)T` in the same format as `%s` makes the time iterator consume the `%s` argument. Do not "simplify" back to one format string.
- **Sun/moon glyphs** (☼ U+263C, ☽ U+263D) are missing from UbuntuMono Nerd Font Mono; they render only because `panel_astro.py` wraps them in `^fn(FreeMono:size=15)`. FreeMono coverage is verified (`fc-query`): U+263C/263D/263E/2600/26E7/2193.
- **`bash` printf/dzen2 colors**: a color constant interpolated as `" %s " % DIM` prints the literal text `#909090` — dzen2 only understands `^fg(#909090)`. `panel_batip.py` wrapped the watt value in `^fg()` only after this showed up in the popup as `#90909039.8 Вт`. Never interpolate a color name bare into panel markup.
- **Battery ETA is only meaningful when current is real**: `status=Full` with an idle `current_now` (~1 mA) yields hours-to-empty in the dozens of days. Hence the plausibility gate, plus the `cap >= 100` → `Заряжена полностью` branch. Do not "simplify" by always computing `charge_now / current_now`.
- **hlwm 0.9.5 has no `activate` command** — use `jumpto <winid>` to focus a window (it also switches tag).
- **Portability**: keep paths `$HOME`/`~`-relative; never reintroduce `/home/zcho` hardcodes (verify with `grep -rn "zcho\\|/home/" herbstluftwm/ install.sh`; the `.tpl` uses `__HIDDIFY_WRAPPER__` instead).
- **`restart_panel.sh`** uses pkill patterns with `[h]erbstluftwm/panel.sh` / `[d]zen2 -w` bracket trick so it doesn't kill its own shell. On the live machine a copy may live at `/tmp/restart_panel.sh` (recreate from repo if /tmp was cleared).
- **`xkbget.py`** detects layout by the keysym of keycode 33 (`P`): `p`(0x70)→`us`, `з`(0x6da)→`ru`. Do not "simplify" it to a group-index lookup — that was the actual historical bug.
- **`XDG_DATA_DIRS` must contain `/usr/share`**: GLib only looks for GSettings schemas in `$XDG_DATA_DIRS/glib-2.0/schemas`. `/etc/X11/Xsession.d/60x11-common_xdg_path` can yield a value missing `/usr/share` → `gsettings list-schemas` says "No schemas installed" → `at-spi-dbus-bus` + `xdg-desktop-portal{,-gtk}` die with `status=5/TRAP` and every dbus activation stalls the full 120 s. Symptom: GUI windows that wait on those services take minutes to map (Hiddify: 170 s → 2 s once fixed). Fixed in two places because neither covers the other: `herbstluftwm/autostart` (hlwm-launched apps, self-healing + idempotent) and `~/.config/environment.d/10-xdg-data-dirs.conf` (systemd user services, needs next login). Diagnose with `gsettings list-schemas | head -1` — "No schemas installed" means the path is broken.
- **Hiddify (v2.0.5) is not single-instance on Linux**: a second `/usr/bin/hiddify` spawns another process and a second window. Any launcher must raise the running window (`herbstclient jumpto`) instead of exec'ing the binary. Stale `~/.local/share/hiddify/command.sock` (left by a killed instance) makes the next launch hang at `initializing [window controller]` with an unmapped 10x10 window; delete the socket when no GUI process is running.
- Right after `herbstclient reload`, attribute reads can race autostart and show stale values; re-query.

## Commands
- Apply config: `herbstclient reload`
- Restart panel: `restart_panel.sh` (from repo, or `/tmp/restart_panel.sh` on the machine)
- Validate: `bash -n` on `*.sh` (autostart/panel.sh/restart_panel.sh/install.sh); `python3 -m py_compile herbstluftwm/*.py`
- Sync live→repo: `cp ~/.config/herbstluftwm/{autostart,panel.sh,panel_astro.py,panel_batip.py,xkbglyph.py,xkbget.py,xkbtoggle.py,textwidth.py} herbstluftwm/`
- Deploy repo→live: `./install.sh`
- Commit/push only when the user asks (they do so explicitly).