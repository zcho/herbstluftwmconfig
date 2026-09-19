#!/usr/bin/env python3
# Всплывающая подсказка по батарее (dzen2-попап под панелью, запускается левым кликом
# на блок батареи в panel.sh). Оценка времени остатка/заряда — из sysfs прямо по току:
#   разряд:   (charge_now * 60) / current_now  [мин]
#   заряд:    ((charge_full - charge_now) * 60) / current_now
# Чистый stdlib, зависимости не нужны. Закрывается кликом (button1/button3).
import os
import subprocess
import sys

BAT = "/sys/class/power_supply/BAT0"
LOCK = "/tmp/panel_batip.pid"
DZEN = "/usr/bin/dzen2"

FW = "#efefef"
DIM = "#909090"
ACC = "#7d9567"
BG = "#101010"


def read_int(entry):
    try:
        with open(os.path.join(BAT, entry)) as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return 0


def read_str(entry):
    try:
        with open(os.path.join(BAT, entry)) as fh:
            return fh.read().strip()
    except OSError:
        return ""


def fmt_minutes(minutes):
    minutes = int(round(minutes))
    h, m = divmod(minutes, 60)
    if h and m:
        return "%d ч %02d мин" % (h, m)
    if h:
        return "%d ч" % h
    return "%d мин" % minutes


def kill_previous():
    try:
        with open(LOCK) as fh:
            pid = int(fh.read().strip())
        os.kill(pid, 15)
    except (OSError, ValueError, ProcessLookupError):
        pass


def monitor_geom():
    try:
        out = subprocess.check_output(
            ["herbstclient", "monitor_rect", "-1"], stderr=subprocess.DEVNULL
        ).decode().split()
        if len(out) >= 4:
            return int(out[2]), int(out[3])
    except (OSError, subprocess.CalledProcessError, ValueError):
        pass
    return 1920, 1080


def main():
    status = read_str("status")
    cap = read_int("capacity")
    charge_now = read_int("charge_now")
    charge_full = read_int("charge_full")
    current_now = abs(read_int("current_now"))
    voltage_now = abs(read_int("voltage_now"))

    line1 = "^fg(%s)Батарея %d%%" % (FW, cap)

    if current_now == 0 or charge_full == 0:
        power = ""
    else:
        power = " · %s %.1f Вт" % (DIM, current_now * voltage_now / 1e12)

    if status == "Charging":
        rem = charge_full - charge_now
        if rem > 0 and current_now > 0:
            eta = rem / current_now * 60
            line2 = "^fg(%s)до полного ~%s%s" % (ACC, fmt_minutes(eta), power)
        else:
            line2 = "^fg(%s)заряжена%s" % (ACC, power)
    elif status == "Discharging":
        if charge_now > 0 and current_now > 0:
            eta = charge_now / current_now * 60
            line2 = "^fg(%s)хватит на ~%s%s" % (ACC, fmt_minutes(eta), power)
        else:
            line2 = "^fg(%s)ток неизвестен%s" % (ACC, power)
    else:
        line2 = "^fg(%s)состояние: %s" % (ACC, status)

    w, h = monitor_geom()
    pop_w = 340
    x = w - pop_w - 8
    y = 24
    pop_h = 38

    kill_previous()

    text = "%s\n%s\n" % (line1, line2)
    proc = subprocess.Popen(
        [
            DZEN,
            "-p",
            "-x", str(x),
            "-y", str(y),
            "-w", str(pop_w),
            "-h", str(pop_h),
            "-l", "2",
            "-fn", "UbuntuMono Nerd Font Mono-12",
            "-bg", BG,
            "-fg", FW,
            "-e", "button1=exit;button3=exit",
        ],
        stdin=subprocess.PIPE,
    )
    try:
        proc.stdin.write(text.encode("utf-8"))
        proc.stdin.close()
    except BrokenPipeError:
        pass
    with open(LOCK, "w") as fh:
        fh.write(str(proc.pid))
    sys.exit(0)


if __name__ == "__main__":
    main()
