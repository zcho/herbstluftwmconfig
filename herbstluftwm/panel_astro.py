#!/usr/bin/env python3
"""Sunset time (local tz) and moon illumination % for the dzen2 panel.

Pure-Python stdlib implementation:
- sunset: NOAA sun-position approximation (upper limb, zenith 90.833 deg);
- moon:   phase fraction from days since a known new moon (2000-01-06 18:14 UT),
          illumination ~ (1 - cos(2*pi*frac)) / 2.

Outputs a panel-ready line, e.g.:
    ^fn(FreeMono:size=15)☼^fn() 18:45  ^fn(FreeMono:size=15)☽^fn() 72%

Usage: panel_astro.py LAT LON
"""
import math
import sys
from datetime import date, datetime

NEW_MOON_JDN = 2451550.26   # 2000-01-06 18:14 UT
SYNODIC_MONTH = 29.53058867


def to_jdn(d):
    return d.toordinal() + 1721425.0


def snap(x):
    return x - math.floor(x / 360.0) * 360.0


def sunset_ut_minutes(day_of_year, lat, lon):
    """NOAA approx. sunset as minutes past UTC; None if the sun never sets."""
    lng_hour = lon / 15.0
    t = day_of_year + (18.0 - lng_hour) / 24.0
    m = 0.9856 * t - 3.289
    l = snap(m + 1.916 * math.sin(math.radians(m))
             + 0.020 * math.sin(math.radians(2 * m)) + 282.634)
    ra = math.degrees(math.atan(0.91764 * math.tan(math.radians(l))))
    lq = math.floor(l / 90.0) * 90.0
    rq = math.floor(ra / 90.0) * 90.0
    ra_deg = ra + (lq - rq)
    sin_dec = 0.39782 * math.sin(math.radians(l))
    dec = math.asin(sin_dec)
    cos_h = (math.cos(math.radians(90.833))
             - sin_dec * math.sin(math.radians(lat))
             ) / (math.cos(dec) * math.cos(math.radians(lat)))
    if cos_h > 1.0:
        return None  # polar day: the sun does not set
    if cos_h < -1.0:  # polar night
        return None
    h = math.degrees(math.acos(cos_h))          # sunset hour angle
    t_hours = h / 15.0 + ra_deg / 15.0 - 0.06571 * t - 6.622
    ut_hours = t_hours - lng_hour
    return ut_hours * 60.0


def format_local(ut_minutes, tz_minutes):
    if ut_minutes is None:
        return "-"
    total = int(round(ut_minutes)) + tz_minutes
    total %= 1440
    return "%02d:%02d" % (total // 60, total % 60)


def moon_illum(jdn):
    frac = ((jdn - NEW_MOON_JDN) % SYNODIC_MONTH) / SYNODIC_MONTH
    return (1.0 - math.cos(2 * math.pi * frac)) / 2.0 * 100.0


def main():
    lat, lon = float(sys.argv[1]), float(sys.argv[2])
    today = date.today()
    now = datetime.now().astimezone()
    off = now.utcoffset()
    tz_min = int(off.total_seconds() // 60) if off else 0

    sunset = format_local(sunset_ut_minutes(today.timetuple().tm_yday, lat, lon), tz_min)
    illum = int(round(moon_illum(to_jdn(today))))

    sun = "^fn(FreeMono:size=15)\u263c^fn()"   # ☼
    moon = "^fn(FreeMono:size=15)\u263d^fn()"  # ☽
    print(f"{sun} {sunset}  {moon} {illum}%")


if __name__ == "__main__":
    main()