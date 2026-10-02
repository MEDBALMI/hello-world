"""Futures-curve engine (11_COMMODITY_TERM_STRUCTURE.md): positional prices, constant-maturity
points (method CM-1: log-linear in days to LTD, no extrapolation), and term-structure features.
All values on date t use only settlements of date t (point-in-time)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.config import market

CM_TENORS = (30, 60, 90, 180, 365)


def curve_table(prices: pd.DataFrame, ccal: pd.DataFrame, root: str) -> pd.DataFrame:
    m = market(root)
    st = prices.pivot_table(index="trade_date", columns="contract_id", values="settle", aggfunc="last").sort_index()
    cc = ccal[(ccal.root == root) & ccal.contract_id.isin(st.columns)].set_index("contract_id")
    ltd = cc["ltd"]
    liquid = cc["is_liquid_month"]
    month = cc["contract_month"]
    deadline = {c: cal.bd_offset(m["calendar"], r, -m["roll"]["buffer_bd"]) for c, r in cc.delivery_risk_date.items()}
    cols = list(st.columns)
    stv = st.values
    out = []
    for i, t in enumerate(st.index):
        avail = [(ltd[c], c, stv[i, j]) for j, c in enumerate(cols)
                 if c in ltd.index and not np.isnan(stv[i, j]) and ltd[c] >= t]
        avail.sort()
        rec = {"trade_date": t}
        for k in range(3):
            rec[f"F{k + 1}"] = avail[k][2] if len(avail) > k else np.nan
            rec[f"C{k + 1}"] = avail[k][1] if len(avail) > k else None
        # eligible liquid contracts (outside delivery window) for carry
        el = [(l, c, v) for l, c, v in avail if liquid[c] and t <= deadline[c] and v > 0]
        if len(el) >= 2:
            (l1, c1, f1), (l2, c2, f2) = el[0], el[1]
            rec["carry"] = np.log(f1 / f2) * 365.0 / max((l2 - l1).days, 1)
            rec["front_second_spread"] = f1 - f2
        else:
            rec["carry"] = rec["front_second_spread"] = np.nan
        # constant maturity (positive prices only)
        pos = [(float((l - t).days), np.log(v)) for l, c, v in avail if v > 0]
        dte = np.array([d for d, _ in pos])
        lp = np.array([x for _, x in pos])
        for tau in CM_TENORS:
            val = np.nan
            if len(dte) >= 2 and dte[0] <= tau <= dte[-1]:
                val = float(np.exp(np.interp(tau, dte, lp)))
            rec[f"CM{tau}"] = val
        # seasonal-neutral carry: nearest liquid contract vs same calendar month one year later
        rec["carry_12m"] = np.nan
        if el:
            c1 = el[0][1]
            target = month[c1] + pd.DateOffset(years=1)
            partner = [v for l, c, v in avail if month[c] == target]
            if partner and partner[0] > 0:
                rec["carry_12m"] = float(np.log(el[0][2] / partner[0]))
        out.append(rec)
    df = pd.DataFrame(out).set_index("trade_date")
    df["slope_cm"] = np.log(df["CM30"] / df["CM180"]) * 365.0 / 150.0
    df["curvature_cm"] = np.log(df["CM30"]) - 2 * np.log(df["CM90"]) + np.log(df["CM180"])
    df["backwardation"] = (df["carry"] > 0).astype(float).where(df["carry"].notna())
    df["root"] = root
    return df
