"""Exchange trading calendars (rule-based approximations).

These are APPROXIMATIONS used when no official holiday file is loaded. Validation test T2/T6
compares them with observed data dates; official calendars should replace them when available
(ref table `exchange_calendar`).
"""
from __future__ import annotations

import datetime as dt
from functools import lru_cache

import numpy as np
import pandas as pd


def _easter(year: int) -> dt.date:
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return dt.date(year, month, day + 1)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def _last_weekday(year: int, month: int, weekday: int) -> dt.date:
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else dt.date(year, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - weekday) % 7)


def _observed(d: dt.date) -> dt.date:
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def us_exchange_holidays(year: int) -> set[dt.date]:
    h = {
        _observed(dt.date(year, 1, 1)),
        _nth_weekday(year, 2, 0, 3),                # Presidents' Day
        _easter(year) - dt.timedelta(days=2),        # Good Friday
        _last_weekday(year, 5, 0),                   # Memorial Day
        _observed(dt.date(year, 7, 4)),
        _nth_weekday(year, 9, 0, 1),                 # Labor Day
        _nth_weekday(year, 11, 3, 4),                # Thanksgiving
        _observed(dt.date(year, 12, 25)),
    }
    if year >= 1998:
        h.add(_nth_weekday(year, 1, 0, 3))           # MLK Day
    if year >= 2022:
        h.add(_observed(dt.date(year, 6, 19)))       # Juneteenth
    return h


def mcx_holidays(year: int) -> set[dt.date]:
    # Fixed national holidays only (approximation; MCX evening sessions differ).
    return {d for d in (dt.date(year, 1, 26), dt.date(year, 8, 15), dt.date(year, 10, 2),
                        dt.date(year, 12, 25)) if d.weekday() < 5}


def lme_holidays(year: int) -> set[dt.date]:
    e = _easter(year)
    return {_observed(dt.date(year, 1, 1)), e - dt.timedelta(days=2), e + dt.timedelta(days=1),
            _nth_weekday(year, 5, 0, 1), _last_weekday(year, 5, 0), _last_weekday(year, 8, 0),
            _observed(dt.date(year, 12, 25)), dt.date(year, 12, 26) if dt.date(year, 12, 26).weekday() < 5
            else dt.date(year, 12, 28)}


_HOLIDAY_FUNCS = {"CME": us_exchange_holidays, "MCX": mcx_holidays, "LME": lme_holidays}


@lru_cache(maxsize=None)
def business_days(calendar: str, start: str = "1975-01-01", end: str = "2035-12-31") -> pd.DatetimeIndex:
    days = pd.bdate_range(start, end)
    hol = set()
    for y in range(days[0].year, days[-1].year + 1):
        hol |= _HOLIDAY_FUNCS[calendar](y)
    mask = np.array([d.date() not in hol for d in days])
    return days[mask]


def is_bd(calendar: str, d) -> bool:
    return pd.Timestamp(d) in set(business_days(calendar))


def bd_on_or_before(calendar: str, d) -> pd.Timestamp:
    bds = business_days(calendar)
    i = bds.searchsorted(pd.Timestamp(d), side="right") - 1
    return bds[i]


def bd_on_or_after(calendar: str, d) -> pd.Timestamp:
    bds = business_days(calendar)
    return bds[bds.searchsorted(pd.Timestamp(d), side="left")]


def bd_offset(calendar: str, d, n: int) -> pd.Timestamp:
    """Move n business days from d (d is snapped to a business day first)."""
    bds = business_days(calendar)
    base = bds.searchsorted(bd_on_or_before(calendar, d))
    return bds[base + n]


def month_bds(calendar: str, year: int, month: int) -> pd.DatetimeIndex:
    bds = business_days(calendar)
    return bds[(bds.year == year) & (bds.month == month)]
