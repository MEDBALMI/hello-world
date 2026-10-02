"""Feature engine. Every feature at date t uses only information available at the close of t.

Price-based features are computed on the chained tradable index (scale-invariant transforms only,
consistent with research-series rule R3); ATR uses the held contract's own OHLC. Positioning and
macro features are joined as-of their AVAILABILITY date (03 s.6), never their observation date.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.config import market


def _held_ohlc(prices: pd.DataFrame, trd: pd.DataFrame) -> pd.DataFrame:
    p = prices.set_index(["trade_date", "contract_id"])[["high", "low"]]
    key = list(zip(trd.index, trd["held_contract"]))
    hl = p.reindex(key)
    return pd.DataFrame({"high": hl["high"].values, "low": hl["low"].values}, index=trd.index)


def technical(prices: pd.DataFrame, trd: pd.DataFrame, halflife: int = 30) -> pd.DataFrame:
    idx = trd["index_level"]
    r = trd["net_return"]
    f = pd.DataFrame(index=trd.index)
    f["idx"] = idx
    for k in (21, 63, 126, 252):
        f[f"ret_{k}"] = idx.pct_change(k)
    f["tsmom_12_1"] = idx.shift(21).pct_change(231)
    for n in (20, 50, 150, 200):
        f[f"ma_{n}"] = idx.rolling(n).mean()
        f[f"dist_ma_{n}"] = idx / f[f"ma_{n}"] - 1
    f["vol"] = np.sqrt((r ** 2).ewm(halflife=halflife, min_periods=40).mean() * 252)
    hl = _held_ohlc(prices, trd)
    sp = trd["settle_prev"]
    tr = pd.concat([(hl["high"] - hl["low"]).abs(), (hl["high"] - sp).abs(), (hl["low"] - sp).abs()], axis=1).max(axis=1)
    atr_pct = (tr / sp.abs()).where(sp.abs() > 0)
    f["atr_pct"] = atr_pct.rolling(20, min_periods=10).mean().fillna(r.abs().rolling(20).mean() * 1.25)
    for n in (20, 55, 252):
        f[f"don_hi_{n}"] = idx.rolling(n).max().shift(1)
        f[f"don_lo_{n}"] = idx.rolling(n).min().shift(1)
    hi252, lo252 = idx.rolling(252).max(), idx.rolling(252).min()
    f["trend_template"] = ((idx > f["ma_50"]) & (f["ma_50"] > f["ma_150"]) & (f["ma_150"] > f["ma_200"]) &
                           (f["ma_200"] > f["ma_200"].shift(21)) & (idx >= 1.3 * lo252) &
                           (idx >= 0.75 * hi252)).astype(float)
    # VCP proxy: three successively tighter 15-day ranges, price within 10% of the 252d high
    rng15 = (idx.rolling(15).max() / idx.rolling(15).min() - 1)
    f["vcp_contraction"] = ((rng15 < rng15.shift(15)) & (rng15.shift(15) < rng15.shift(30)) &
                            (idx >= 0.90 * hi252)).astype(float)
    f["z_ret_5"] = idx.pct_change(5) / (f["vol"] * np.sqrt(5 / 252))
    f["near_high_252"] = idx / hi252
    return f


def seasonal_score(trd: pd.DataFrame) -> pd.Series:
    """Mean return of the same calendar month in PRIOR years only (expanding, no look-ahead)."""
    r = trd["net_return"]
    monthly = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
    monthly.index.names = ["y", "m"]
    mdf = monthly.reset_index(name="ret")
    mdf["score"] = mdf.groupby("m")["ret"].transform(lambda s: s.shift(1).expanding().mean())
    lookup = mdf.set_index(["y", "m"])["score"]
    return pd.Series([lookup.get((d.year, d.month), np.nan) for d in r.index], index=r.index)


def _usable_date(ts: pd.Series, calendar: str) -> pd.Series:
    """First trading date whose close comes after the release: next business day after the
    (UTC) release date. Conservative for US-afternoon releases and for MCX evening sessions."""
    d = pd.to_datetime(ts)
    if getattr(d.dt, "tz", None) is not None:
        d = d.dt.tz_convert("UTC").dt.tz_localize(None)
    bds = cal.business_days(calendar)
    pos = bds.searchsorted(d.dt.normalize(), side="right")
    return pd.Series(bds[np.minimum(pos, len(bds) - 1)], index=ts.index)


def positioning(cot: pd.DataFrame, root: str, calendar: str, index: pd.DatetimeIndex) -> pd.DataFrame:
    c = cot[cot.root == root].sort_values("as_of_date").copy()
    if c.empty:
        return pd.DataFrame(index=index)
    c["mm_net"] = (c["mm_long"] - c["mm_short"]) / c["open_interest"]
    c["pm_net"] = (c["pm_long"] - c["pm_short"]) / c["open_interest"]
    c["mm_z"] = (c["mm_net"] - c["mm_net"].rolling(156, min_periods=52).mean()) / c["mm_net"].rolling(156, min_periods=52).std()
    c["mm_pct"] = c["mm_net"].rolling(156, min_periods=52).rank(pct=True)
    c["mm_chg_4w"] = c["mm_net"].diff(4)
    c["usable_date"] = _usable_date(c["release_ts"], calendar)
    cols = ["mm_net", "pm_net", "mm_z", "mm_pct", "mm_chg_4w"]
    out = pd.merge_asof(pd.DataFrame({"trade_date": index}), c[["usable_date"] + cols].rename(columns={"usable_date": "trade_date"}),
                        on="trade_date", direction="backward")
    return out.set_index("trade_date")


def macro(macro_df: pd.DataFrame, calendar: str, index: pd.DatetimeIndex) -> pd.DataFrame:
    out = pd.DataFrame(index=index)
    for sid, g in macro_df.groupby("series_id"):
        g = g.sort_values("obs_date").copy()
        g["usable_date"] = _usable_date(g["available_ts"], calendar)
        g = g.sort_values("usable_date").drop_duplicates("usable_date", keep="last")
        s = pd.merge_asof(pd.DataFrame({"trade_date": index}), g[["usable_date", "value"]].rename(columns={"usable_date": "trade_date"}),
                          on="trade_date", direction="backward").set_index("trade_date")["value"]
        out[sid] = s
        out[f"{sid}_chg_63"] = s.diff(63)
    return out


def build(prices, trd, curve, cot, macro_df, root: str, halflife: int = 30) -> pd.DataFrame:
    calname = market(root)["calendar"]
    f = technical(prices, trd, halflife)
    cv = curve.reindex(f.index)
    for c in ("carry", "slope_cm", "curvature_cm", "carry_12m", "backwardation", "front_second_spread"):
        f[c] = cv[c]
    f["carry_z"] = (f["carry"] - f["carry"].rolling(252, min_periods=126).mean()) / f["carry"].rolling(252, min_periods=126).std()
    f["season_score"] = seasonal_score(trd)
    if cot is not None and not cot.empty:
        f = f.join(positioning(cot, root, calname, f.index))
    if macro_df is not None and not macro_df.empty:
        f = f.join(macro(macro_df, calname, f.index))
    return f


def truncation_test(fn, n_samples: int = 12, seed: int = 0, tol: float = 1e-9) -> dict:
    """Generic look-ahead detector (T14): fn(cutoff) must return a frame computed using data up
    to `cutoff` only; values at sample dates must equal those from the full-sample run."""
    full = fn(None)
    rng = np.random.default_rng(seed)
    idx = full.dropna(how="all").index
    if len(idx) < 300:
        return {"result": "OPEN", "reason": "too few rows"}
    picks = [pd.Timestamp(x) for x in sorted(rng.choice(idx[260:], size=min(n_samples, len(idx) - 260), replace=False))]
    bad = []
    for t in picks:
        part = fn(t)
        a, b = full.loc[t], part.loc[t].reindex(a_idx := full.columns)
        num = pd.to_numeric(a, errors="coerce"), pd.to_numeric(b, errors="coerce")
        diff = (num[0] - num[1]).abs()
        both_nan = num[0].isna() & num[1].isna()
        mism = diff[(diff > tol) | (num[0].isna() != num[1].isna())]
        mism = mism[~both_nan.reindex(mism.index, fill_value=False)]
        if len(mism):
            bad.append({"date": str(t.date()), "columns": list(mism.index[:10])})
    return {"result": "PASS" if not bad else "FAIL", "n_checked": len(picks), "failures": bad}
