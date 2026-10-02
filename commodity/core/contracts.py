"""Contract identity, expiry/notice rules and versioned specifications."""
from __future__ import annotations

import pandas as pd

from . import calendars as cal
from .config import market

MONTH_CODES = "FGHJKMNQUVXZ"


def contract_id(root: str, year: int, month: int) -> str:
    return f"{root}{year}{MONTH_CODES[month - 1]}"


def parse_contract_id(cid: str) -> tuple[str, int, int]:
    code = cid[-1]
    year = int(cid[-5:-1])
    return cid[:-5], year, MONTH_CODES.index(code) + 1


# ------------------------------------------------------------------ expiry rules
def _third_last_bd(c, y, m):
    return cal.month_bds(c, y, m)[-3]


def _last_bd(c, y, m):
    return cal.month_bds(c, y, m)[-1]


def _last_bd_prior_month(c, y, m):
    py, pm = (y - 1, 12) if m == 1 else (y, m - 1)
    return cal.month_bds(c, py, pm)[-1]


def _cl_rule(c, y, m):
    """NYMEX CL: trading terminates 3 bd before the 25th calendar day of the month prior to
    delivery; if the 25th is not a business day, 3 bd before the last bd preceding the 25th."""
    py, pm = (y - 1, 12) if m == 1 else (y, m - 1)
    d25 = pd.Timestamp(py, pm, 25)
    anchor = d25 if d25 in cal.business_days(c) else cal.bd_on_or_before(c, d25 - pd.Timedelta(days=1))
    return cal.bd_offset(c, anchor, -3)


def _ng_rule(c, y, m):
    """NYMEX NG: 3 bd prior to the first calendar day of the delivery month."""
    first = pd.Timestamp(y, m, 1)
    return cal.bd_offset(c, cal.bd_on_or_before(c, first - pd.Timedelta(days=1)), -2)


def _next(y, m):
    return (y + 1, 1) if m == 12 else (y, m + 1)


def _mcx_day_5(c, y, m):
    return cal.bd_on_or_before(c, pd.Timestamp(y, m, 5))


def _mcx_crude(c, y, m):
    ny, nm = _next(y, m)
    return cal.bd_offset("MCX", _cl_rule("CME", ny, nm), -1)


def _mcx_ng(c, y, m):
    ny, nm = _next(y, m)
    return cal.bd_offset("MCX", _ng_rule("CME", ny, nm), -1)


LTD_RULES = {
    "third_last_bd_of_month": _third_last_bd,
    "last_bd_of_month": _last_bd,
    "cl_rule": _cl_rule,
    "ng_rule": _ng_rule,
    "mcx_day_5": _mcx_day_5,
    "mcx_crude": _mcx_crude,
    "mcx_ng": _mcx_ng,
}


def ltd(root: str, year: int, month: int) -> pd.Timestamp:
    m = market(root)
    return LTD_RULES[m["ltd_rule"]](m["calendar"], year, month)


def fnd(root: str, year: int, month: int) -> pd.Timestamp | None:
    m = market(root)
    rule = m.get("fnd_rule", "none")
    if rule == "last_bd_of_prior_month":
        return _last_bd_prior_month(m["calendar"], year, month)
    if rule == "mcx_tender_5bd":
        return cal.bd_offset(m["calendar"], ltd(root, year, month), -5)
    return None


def delivery_risk_date(root: str, year: int, month: int) -> pd.Timestamp:
    f = fnd(root, year, month)
    t = ltd(root, year, month)
    return min(f, t) if f is not None else t


def spec(root: str, on_date) -> dict:
    """Specification version valid on a date (P&L must use this, never today's spec)."""
    versions = sorted(market(root)["spec_versions"], key=lambda v: str(v["valid_from"]))
    d = pd.Timestamp(on_date)
    chosen = versions[0]
    for v in versions:
        if pd.Timestamp(v["valid_from"]) <= d:
            chosen = v
    return chosen


def spec_frame(root: str, index) -> pd.DataFrame:
    """Vectorised spec lookup (multiplier, tick, commission) for a date index."""
    versions = sorted(market(root)["spec_versions"], key=lambda v: str(v["valid_from"]))
    starts = pd.DatetimeIndex([pd.Timestamp(v["valid_from"]) for v in versions])
    pos = (starts.searchsorted(pd.DatetimeIndex(index), side="right") - 1).clip(0)
    return pd.DataFrame([versions[i] for i in pos], index=index)[["multiplier", "tick", "commission"]]


def contract_calendar(root: str, start, end) -> pd.DataFrame:
    """Rule-based contract calendar for all listed months whose LTD falls in [start, end + horizon]."""
    m = market(root)
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    rows = []
    y, mo = start.year - 1, 1
    last = end + pd.DateOffset(months=m.get("listing_months_ahead", 12) + 1)
    while pd.Timestamp(y, mo, 1) <= last:
        if mo in m["listed_months"]:
            t = ltd(root, y, mo)
            if t >= start - pd.Timedelta(days=40):
                f = fnd(root, y, mo)
                rows.append({
                    "root": root,
                    "contract_id": contract_id(root, y, mo),
                    "contract_month": pd.Timestamp(y, mo, 1),
                    "listing_date": t - pd.DateOffset(months=m.get("listing_months_ahead", 12)),
                    "fnd": f,
                    "ltd": t,
                    "delivery_risk_date": min(f, t) if f is not None else t,
                    "settlement_type": m["settlement"],
                    "is_liquid_month": mo in m["liquid_months"],
                    "calendar_source": "RULE",
                })
        y, mo = _next(y, mo)
    return pd.DataFrame(rows)
