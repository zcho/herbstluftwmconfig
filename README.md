# mylinux — herbstluftwm setup

**English** | [**Русский**](README.ru.md)

A ready-made window manager configuration for [herbstluftwm](https://herbstluftwm.org/)
on **Ubuntu 24.04**, assembled during an ongoing setup. Goal: deploy it on a clean
Ubuntu 24 and get the same GUI as on the original machine.

## Repository layout

```
mylinux/
├── README.md                  # documentation (English)
├── README.ru.md               # documentation (Russian)
├── install.sh                 # copies the config into ~/.config/herbstluftwm
├── rofi/
│   └── config.rasi            # rofi theme (window switcher + app menu)
└── herbstluftwm/
    ├── autostart              # full WM config (keybinds, theme, rules, panel launch)
    ├── panel.sh               # dzen2 panel (taskbar, tags, network, sound, date, app corner)
    ├── xkbget.py              # current keyboard layout (by keysym, not by index)
    ├── xkbtoggle.py           # ru/us layout toggle via XkbLockGroup
    ├── textwidth.py           # Pango/Cairo text-width measurement for panel alignment
    ├── apps.txt               # editable app list for the corner launcher menu
    ├── appmenu.sh             # launcher menu (rofi) opened from the panel corner
    └── restart_panel.sh       # reliable panel restart (never hangs on pkill)
```

## Fresh install on Ubuntu 24.04

### 1. System packages

```bash
sudo apt update
sudo apt install herbstluftwm dzen2 rofi alacritty dmenu slock brightnessctl \
  network-manager network-manager-gnome x11-xserver-utils \
  python3 python3-gi python3-cairo gir1.2-pango-1.0
```

What each dependency is for:

| Package | Purpose |
|---|---|
| `herbstluftwm` | the window manager itself |
| `dzen2` | panel (taskbar/tags) |
| `rofi` | Alt+Tab window switcher (list with previews) |
| `alacritty` | terminal on `$Mod-Return` |
| `dmenu` | `$Mod-Shift-p` (application launcher) |
| `slock` | screen lock on `$Mod-l` |
| `brightnessctl` | brightness keybinds/hotkeys |
| `network-manager`, `network-manager-gnome` | network indicator in panel + tray icon (`nm-applet`) |
| `x11-xserver-utils` | `xsetroot` (solid desktop background) |
| `python3-gi`, `python3-cairo`, `gir1.2-pango-1.0` | text-width measurement (`textwidth.py`) |

### 2. Font

The panel uses **UbuntuMono Nerd Font Mono** (size 15). Install a Nerd Font family,
e.g. `UbuntuMono Nerd Font` from [nerdfonts.com](https://www.nerdfonts.com/)
(into `~/.local/share/fonts`), then:

```bash
fc-cache -fv
```

Without the font the panel falls back to a system monospace font; if you prefer,
change `font=` in `panel.sh`.

### 3. Deploy the config

```bash
git clone <repo_URL> ~/mylinux
cd ~/mylinux
./install.sh
```

The script copies the files into `~/.config/herbstluftwm` and makes them executable.
In a running session apply with `herbstclient reload` (or just log back into herbstluftwm).

### 4. System settings (outside the repo, needs sudo)

These steps are not automated because they require admin rights:

**Brightness (intel_backlight)** — the user must be in the `video` group:
```bash
sudo usermod -aG video $USER   # then log back in
```

**System-wide keyboard layout (optional)** — `/etc/default/keyboard`:
```
XKBLAYOUT="ru,us"
XKBOPTIONS="grp:rctrl_toggle,grp_led:scroll"
```
Note: `autostart` already forces
`setxkbmap -layout ru,us -option grp:alt_space_toggle -option grp_led:scroll`,
so this step is optional (only needed if you also want Right Ctrl to toggle at login).

### 5. VPN / V2RayTun equivalent

On the original machine **Hiddify Next** is installed (Flutter client; VLESS, Trojan,
VMess, Shadowsocks; import via link/QR). Install it separately from hiddify.com.
Its configs live in `~/.local/share/hiddify/` and are not part of this repo.

## What changed vs. stock herbstluftwm

### Keybinds (Mod = Mod4/Super)

| Combination | Action |
|---|---|
| `Mod+Shift+p` | `dmenu_run` (search/launch apps) |
| `Mod+Shift+Space` | toggle ru/us layout (`xkbtoggle.py`) |
| `Alt+Space` | toggle layout (via XKB) |
| `Mod+Return` | terminal `alacritty` |
| `Mod+F1` / `F2` / `F3` | mute / volume −5% / +5% (`wpctl`) |
| `Mod+F6` / `F7`, `XF86MonBrightnessDown/Up` | brightness −/+ 5% (`brightnessctl`) |
| `Mod+l`, `Mod+Shift+l` | lock screen (`slock`) |
| `Alt+Tab`, `Alt+Shift+Tab` | **window list with previews** (`rofi -show window`) |
| `Mod+Tab`, `Mod+Shift+Tab` | quick cycle over windows on all tags (`cycle_all`) |
| `Mod+i` | jump to urgent window |

The rest (focus `hjkl`/arrows, move `Shift+hjkl`, splits `Mod+u`/`Mod+o`,
resize `Mod+Control+hjkl`, tags 1–9, `Mod+space` cycles layouts) is stock.

### Panel (`panel.sh`, dzen2)

- Font `UbuntuMono Nerd Font Mono-15`, height 22px, dark theme matching the WM colors.
- **Clickable tags** (SVN dzen): click a tag to switch to it.
- **Taskbar**: clickable list of windows on the current tag (click → `herbstclient jumpto`,
  active window highlighted). Replaces the stock single window title.
- **Blocks**: `Kbd` (click → layout toggle), `Bat` (battery), `Net` (SSID/signal,
  click → `nm-connection-editor`), `Vol` (LMB +5%, RMB −5%), date `HH:MM DD.MM.YYYY`
  + shortened weekday.
- **App menu in the right corner**: the subtle inverted-pentagram glyph `⛧` at the
  right edge of the panel is a dual-action button — **left-click** opens a
  `rofi`-based launcher menu, **right-click** opens the window switcher
  (`rofi -show window`, same as Alt+Tab). The launcher list is read from
  `apps.txt` — format `Display name<tab>command`; lines starting with `#` are
  ignored. The glyph is drawn with FreeMono via dzen `^fn()` (UbuntuMono
  Nerd Font lacks U+26E7).
- Mouse wheel on the panel cycles tags.
- Right side aligned using real text-width measurement via `textwidth.py`
  (Pango/Cairo), so the date never overflows off-screen (right margin kept minimal,
  so the corner `⛧` launcher is reachable right at the screen edge).

### Keyboard layout

- Layout pair `ru,us`; toggling via `XkbLockGroup` in `xkbtoggle.py`
  (independent of XKB options).
- `xkbget.py` detects the active language **by the real keysym** of the `P` key
  (`p`→us / `з`→ru), not by group index — the bar always reports the truth.
- `autostart` applies the layout twice (immediately and after 2 s) — protection
  against SDDM/GDM resetting it during login.

### Everything else

- `export XDG_DATA_DIRS="$XDG_DATA_DIRS:/var/lib/snapd/desktop"` — lets snap apps
  (e.g. snap-VLC) be found via xdg-mime for the video player.
- `xsetroot -solid '#5A8E3A'` — green desktop background.
- Theme: active frame `#345F0C`/`#7d9567` (soft sage), 4px gap, borders, tree separator.
- `nm-applet` autostarted (network tray icon).
- **Rofi theme** (`rofi/config.rasi`): dark background `#101010`, sage accent `#7d9567`,
  light text `#efefef` — matches the panel colors. Used by the Alt+Tab window switcher,
  the corner app menu, and the corner `⛧` right-click window switcher.
- Helper `restart_panel.sh` — reliable panel restart (patterns `[h]erbstluftwm/panel.sh`,
  so it never kills its own shell). Run: `~/mylinux/herbstluftwm/restart_panel.sh`.

## Notes / known quirks

- **No compositor** — `slock` shows a black screen, and rofi window thumbnails may be
  empty/black. If thumbnails bother you, remove `-window-thumbnail` from the Alt+Tab
  keybinds in `autostart`.
- `wpctl` requires PipeWire/WirePlumber (default on Ubuntu 24).
- Config paths use `$HOME`/`~` — works with any username.
- `mousebind` in herbstluftwm 0.9.5 supports only internal actions (`move`/`zoom`/
  `resize`), it cannot run arbitrary commands — which is why the app launcher lives
  in the panel corner (dzen `^ca`) instead of a desktop right-click binding.