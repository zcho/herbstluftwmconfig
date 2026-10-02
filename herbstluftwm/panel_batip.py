#!/usr/bin/env python3
# Всплывающая подсказка по батарее (dzen2-попап под панелью, запускается левым кликом
# на блок батареи в panel.sh). Заголовок — время работы от батареи, вторая строка —
# процент и мощность. Оценка времени остатка/заряда — из sysfs прямо по току:
#   разряд:   (charge_now * 60) / current_now  [мин]
#   заряд:    ((charge_full - charge_now) * 60) / current_now
# ETA отбрасывается как неправдоподобный (см. PLAUSIBLE_*): при status=Full и
# токе холостого хода current_now даёт оценку в десятки суток.
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

# Разумные границы оценки времени: всё, что вне их — мусор из sysfs, а не правда.
PLAUSIBLE_MIN = 2  # мин
PLAUSIBLE_MAX = 36 * 60  # мин


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


def eta_minutes(energy_now, current_now):
    """Оценка времени по току; None, если ток/энергия неизвестны или оценка неправдоподобна."""
    if energy_now <= 0 or current_now <= 0:
        return None
    minutes = energy_now / current_now * 60
    if not PLAUSIBLE_MIN <= minutes <= PLAUSIBLE_MAX:
        return None
    return minutes


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

    # На некоторых прошивках charge_now/charge_full не экспортируются — берём capacity.
    if charge_full <= 0:
        charge_full = 1000000
    if charge_now <= 0:
        charge_now = int(charge_full * cap / 100)

    watts = current_now * voltage_now / 1e12 if current_now and voltage_now else 0.0
    # DIM обязан быть обёрнут в ^fg(), иначе dzen2 напечатает "#909090" как текст.
    power = " · ^fg(%s)%.1f Вт" % (DIM, watts) if watts else ""

    if status == "Discharging":
        eta = eta_minutes(charge_now, current_now)
        if eta:
            line1 = "^fg(%s)Осталось ~%s" % (ACC, fmt_minutes(eta))
        else:
            line1 = "^fg(%s)Осталось неизвестно" % ACC
        line2 = "^fg(%s)%d%%%s" % (FW, cap, power)
    elif status == "Charging":
        eta = eta_minutes(charge_full - charge_now, current_now)
        if eta:
            line1 = "^fg(%s)До полного ~%s" % (ACC, fmt_minutes(eta))
        else:
            line1 = "^fg(%s)До полного неизвестно" % ACC
        line2 = "^fg(%s)%d%%%s" % (FW, cap, power)
    elif cap >= 100:
        # Полный заряд: времени работы не существует, пока батарея не разрядится.
        line1 = "^fg(%s)Заряжена полностью" % ACC
        line2 = "^fg(%s)%d%%%s" % (FW, cap, power)
    else:
        line1 = "^fg(%s)Заряд не идёт" % ACC
        line2 = "^fg(%s)%d%%%s%s" % (FW, cap, power, "" if status == "Not charging" else " · %s" % status)

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
