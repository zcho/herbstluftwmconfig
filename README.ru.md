# mylinux — herbstluftwm setup

[**English**](README.md) | **Русский**

Готовая конфигурация оконного менеджера [herbstluftwm](https://herbstluftwm.org/) для
**Ubuntu 24.04**, собранная в процессе настройки. Цель — разворачивать на «чистом»
Ubuntu 24 и получать тот же GUI, что и на исходной машине.

## Состав репозитория

```
mylinux/
├── README.md                  # английская версия документации
├── README.ru.md               # русская версия документации
├── install.sh                 # копирует конфиг в ~/.config/herbstluftwm
├── rofi/
│   └── config.rasi            # тема rofi (переключатель окон + меню приложений)
└── herbstluftwm/
    ├── autostart              # весь конфиг WM (клавиши, тема, правила, панель)
    ├── panel.sh               # dzen2-панель (таскбар, теги, сеть, звук, дата, угол-меню)
    ├── xkbget.py              # текущая раскладка (по keysym, а не по индексу)
    ├── xkbtoggle.py           # переключение ru/us через XkbLockGroup
    ├── textwidth.py           # замер ширины текста Pango/Cairo для выравнивания панели
    ├── apps.txt               # редактируемый список приложений для углового меню
    ├── appmenu.sh             # меню запуска (rofi) по клику в угол панели
    └── restart_panel.sh       # надёжный перезапуск панели (без зависания pkill)
```

## Установка с нуля на Ubuntu 24.04

### 1. Системные пакеты

```bash
sudo apt update
sudo apt install herbstluftwm dzen2 rofi alacritty dmenu slock brightnessctl \
  network-manager network-manager-gnome x11-xserver-utils \
  python3 python3-gi python3-cairo gir1.2-pango-1.0
```

Зависимости по назначению:

| Пакет | Для чего |
|---|---|
| `herbstluftwm` | сам оконный менеджер |
| `dzen2` | панель (таскбар/теги) |
| `rofi` | переключатель окон по Alt+Tab (список с превью) |
| `alacritty` | терминал по `$Mod-Return` |
| `dmenu` | `$Mod-Shift-p` (меню запуска) |
| `slock` | блокировка экрана `$Mod-l` |
| `brightnessctl` | клавиши/хоткеи яркости |
| `network-manager`, `network-manager-gnome` | индикатор сети в панели + иконка в трее (`nm-applet`) |
| `x11-xserver-utils` | `xsetroot` (сплошной фон рабочего стола) |
| `python3-gi`, `python3-cairo`, `gir1.2-pango-1.0` | замер ширины текста (`textwidth.py`) |

### 2. Шрифт

Панель использует **UbuntuMono Nerd Font Mono** (размер 15). Установите семейство
Nerd Fonts, например `UbuntuMono Nerd Font` из проекта
[nerdfonts.com](https://www.nerdfonts.com/) (папка `~/.local/share/fonts`), затем:

```bash
fc-cache -fv
```

Если шрифта нет — панель отрисуется системным моноширинным; при желании поменяйте
`font=` в `panel.sh`.

### 3. Развернуть конфиг

```bash
git clone <URL_этого_репо> ~/mylinux
cd ~/mylinux
./install.sh
```

Скрипт копирует файлы в `~/.config/herbstluftwm` и делает их исполняемыми.
В текущей сессии примените: `herbstclient reload` (или перезайдите в herbstluftwm).

### 4. Системные настройки (вне репозитория, нужен sudo)

Эти шаги не автоматизированы, т.к. требуют прав администратора:

**Яркость (intel_backlight)** — пользователь должен быть в группе `video`:
```bash
sudo usermod -aG video $USER   # затем перелогиниться
```

**Раскладка на уровне системы (опционально)** — `/etc/default/keyboard`:
```
XKBLAYOUT="ru,us"
XKBOPTIONS="grp:rctrl_toggle,grp_led:scroll"
```
Но помните: `autostart` и так принудительно выполняет
`setxkbmap -layout ru,us -option grp:alt_space_toggle -option grp_led:scroll`,
поэтому шаг необязателен (нужен только чтобы правый Ctrl тоже переключал при входе).

### 5. VPN / аналог V2RayTun

На исходной машине установлен **Hiddify Next** (Flutter-клиент; VLESS, Trojan,
VMess, Shadowsocks; импорт по ссылке/QR). Ставится отдельно с сайта hiddify.com.
Конфиги живут в `~/.local/share/hiddify/` — в этот репозиторий не входят.

## Что изменено относительно чистого herbstluftwm

### Клавиши (Mod = Mod4/Super)

| Комбинация | Действие |
|---|---|
| `Mod+Shift+p` | `dmenu_run` (поиск/запуск программ) |
| `Mod+Shift+Space` | переключение раскладки ru/us (`xkbtoggle.py`) |
| `Alt+Space` | переключение раскладки (через XKB) |
| `Mod+Return` | терминал `alacritty` |
| `Mod+F1` / `F2` / `F3` | mute / громкость −5% / +5% (`wpctl`) |
| `Mod+F6` / `F7`, `XF86MonBrightnessDown/Up` | яркость −/+ 5% (`brightnessctl`) |
| `Mod+l`, `Mod+Shift+l` | блокировка экрана (`slock`) |
| `Alt+Tab`, `Alt+Shift+Tab` | **список окон с превью** (`rofi -show window`) |
| `Mod+Tab`, `Mod+Shift+Tab` | быстрый цикл по окнам всех тегов (`cycle_all`) |
| `Mod+i` | перейти к urgent-окну |

Остальное (фокус `hjkl`/стрелки, перемещение `Shift+hjkl`, сплиты `Mod+u`/`Mod+o`,
ресайз `Mod+Control+hjkl`, теги 1–9, `Mod+space` — циклировать layout) — стоковое.

### Панель (`panel.sh`, dzen2)

- Шрифт `UbuntuMono Nerd Font Mono-15`, высота 22px, тёмная тема из цветов WM.
- **Кликабельные теги** (SVN dzen): клик по тегу → переход.
- **Таскбар**: кликабельный список окон текущего тега (клик → `herbstclient jumpto`,
  активное окно подсвечено). Добавлен поверх стокового одного заголовка.
- **Блоки**: `Kbd` (клик → переключение раскладки), `Bat` (батарея), `Net` (SSID/сигнал,
  клик → `nm-connection-editor`), `Vol` (ЛКМ +5%, ПКМ −5%), дата `HH:MM DD.MM.YYYY` + день недели.
- **Угол-меню**: едва заметный глиф `⛧` (перевёрнутая пентаграмма, U+26E7) у правого
  края панели — двойная кнопка: **ЛКМ** открывает меню запуска на `rofi`, **ПКМ** —
  переключатель окон (`rofi -show window`, как по Alt+Tab). Список для меню запуска
  берётся из `apps.txt` — формат `Имя<TAB>команда`, строки с `#` игнорируются. Глиф
  рисуется шрифтом FreeMono через dzen `^fn()` (в UbuntuMono Nerd Font символа нет).
- Колесо на панели → цикл по тегам.
- Выравнивание правой части через реальный замер ширины `textwidth.py`
  (Pango/Cairo), чтобы дата не уезжала за экран (правый отступ сведён к минимуму,
  так что угловое меню `⛧` кликабельно вплоть до края экрана).

### Раскладка

- Пара раскладок `ru,us`; переключение `XkbLockGroup` через `xkbtoggle.py`
  (не зависит от XKB-опций).
- `xkbget.py` определяет активный язык **по реальному keysym** клавиши `P`
  (`p`→us / `з`→ru), а не по индексу группы — бар всегда показывает правду.
- В `autostart` раскладка применяется дважды (сразу и через 2 с) — защита от
  сброса SDDM/GDM при входе.

### Остальное

- `export XDG_DATA_DIRS="$XDG_DATA_DIRS:/var/lib/snapd/desktop"` — чтобы snap-приложения
  (например, snap-VLC) находились через xdg-mime для видеоплеера.
- `xsetroot -solid '#5A8E3A'` — зелёный фон рабочего стола.
- Тема: активный фрейм `#345F0C`/`#7d9567` (мягкий sage), гап 4px, рамки, древовидный сепаратор.
- Автостарт `nm-applet` (иконка сети в трее).
- **Тема rofi** (`rofi/config.rasi`): тёмный фон `#101010`, акцент sage `#7d9567`,
  светлый текст `#efefef` — в цветах панели. Используется и в переключателе окон Alt+Tab,
  и в угловом меню приложений, и в переключателе окон по ПКМ на `⛧`.
- Служебный `restart_panel.sh` — перезапуск панели (паттерны `[h]erbstluftwm/panel.sh`,
  не убивают саму оболочку). Запуск: `~/mylinux/herbstluftwm/restart_panel.sh`.

## Примечания / известные особенности

- **Композитора нет** — `slock` показывает чёрный экран, а миниатюры окон в rofi
  могут быть пустыми/чёрными. Если миниатюры мешают — уберите `-window-thumbnail`
  из keybind'ов Alt+Tab в `autostart`.
- Для `wpctl` нужен PipeWire/WirePlumber (стоит на Ubuntu 24 по умолчанию).
- Пути в конфиге используют `$HOME`/`~` — работает при любом имени пользователя.
- `mousebind` в herbstluftwm 0.9.5 поддерживает только внутренние действия
  (`move`/`zoom`/`resize`) и не умеет запускать команды — поэтому меню запуска
  вынесено в угол панели (dzen `^ca`), а не на правый клик по рабочему столу.