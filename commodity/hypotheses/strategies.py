"""Signal library. Each strategy maps a feature frame (one root, computed at close t) to a target
direction in [-1, 1] for close t. The backtest engine applies the execution lag and sizing."""
from __future__ import annotations

import numpy as np
import pandas as pd


def _hold(trigger: pd.Series, hold: int) -> pd.Series:
    """Hold the last non-zero trigger for `hold` days."""
    out = np.zeros(len(trigger))
    cur, left = 0.0, 0
    for i, v in enumerate(trigger.fillna(0).values):
        if v != 0:
            cur, left = np.sign(v), hold
        if left > 0:
            out[i] = cur
            left -= 1
        else:
            cur = 0.0
    return pd.Series(out, index=trigger.index)


def tsmom(f, lookback=252):
    col = {252: "ret_252", 126: "ret_126", 63: "ret_63", 21: "ret_21"}[lookback]
    return np.sign(f[col])


def tsmom_12_1(f):
    return np.sign(f["tsmom_12_1"])


def ma_trend(f, n=200):
    return np.sign(f[f"dist_ma_{n}"])


def ma_cross(f, fast=50, slow=200):
    return np.sign(f[f"ma_{fast}"] - f[f"ma_{slow}"])


def donchian(f, entry=55, exit=20):
    idx, hi, lo = f["idx"], f[f"don_hi_{entry}"], f[f"don_lo_{entry}"]
    xhi, xlo = f[f"don_hi_{exit}"], f[f"don_lo_{exit}"]
    out, pos = np.zeros(len(f)), 0.0
    for i in range(len(f)):
        p = idx.iat[i]
        if np.isnan(hi.iat[i]):
            continue
        if pos == 0:
            pos = 1.0 if p > hi.iat[i] else (-1.0 if p < lo.iat[i] else 0.0)
        elif pos > 0 and p < xlo.iat[i]:
            pos = 0.0
        elif pos < 0 and p > xhi.iat[i]:
            pos = 0.0
        out[i] = pos
    return pd.Series(out, index=f.index)


def vol_breakout(f, k=1.5, hold=10):
    r1 = f["idx"].pct_change()
    trig = np.where(r1 > k * f["atr_pct"], 1, np.where(r1 < -k * f["atr_pct"], -1, 0))
    return _hold(pd.Series(trig, index=f.index), hold)


def roc(f, lookback=63):
    return np.sign(f[f"ret_{lookback}"])


def trend_template(f):
    return f["trend_template"].fillna(0)


def vcp_breakout(f, entry=55):
    """Long-only VCP proxy: recent volatility contraction + 55d breakout; exit below 50d MA."""
    recent = f["vcp_contraction"].rolling(10, min_periods=1).max()
    out, pos = np.zeros(len(f)), 0.0
    for i in range(len(f)):
        p = f["idx"].iat[i]
        if pos == 0 and recent.iat[i] > 0 and p > f[f"don_hi_{entry}"].iat[i]:
            pos = 1.0
        elif pos > 0 and p < f["ma_50"].iat[i]:
            pos = 0.0
        out[i] = pos
    return pd.Series(out, index=f.index)


def mean_reversion(f, z=2.0, hold=5):
    zz = f["z_ret_5"]
    return _hold(pd.Series(np.where(zz > z, -1, np.where(zz < -z, 1, 0)), index=f.index), hold)


def carry(f, col="carry"):
    return np.sign(f[col])


def carry_z(f, threshold=0.0):
    return np.sign(f["carry_z"]).where(f["carry_z"].abs() > threshold, 0.0)


def mom_carry(f, lookback=252):
    m, c = tsmom(f, lookback), np.sign(f["carry"])
    return m.where(m == c, 0.0)


def trend_carry_filter(f, n=200):
    t = ma_trend(f, n)
    return t.where(~((t > 0) & (f["carry"] < -0.10)) & ~((t < 0) & (f["carry"] > 0.10)), 0.0)


def cot_contrarian(f, hi=0.9, lo=0.1):
    p = f.get("mm_pct")
    if p is None:
        return pd.Series(np.nan, index=f.index)
    return pd.Series(np.where(p > hi, -1, np.where(p < lo, 1, 0)), index=f.index).where(p.notna())


def cot_momentum(f):
    c = f.get("mm_chg_4w")
    return np.sign(c) if c is not None else pd.Series(np.nan, index=f.index)


def trend_cot(f, n=200, hi=0.9):
    t = ma_trend(f, n)
    p = f.get("mm_pct")
    if p is None:
        return pd.Series(np.nan, index=f.index)
    crowded = ((t > 0) & (p > hi)) | ((t < 0) & (p < 1 - hi))
    return t.where(~crowded, 0.0)


def macro_real_yield(f):
    """Gold: long when real yields fell over the last quarter (rationale: opportunity cost)."""
    c = f.get("DFII10_chg_63")
    return -np.sign(c) if c is not None else pd.Series(np.nan, index=f.index)


def macro_usd(f):
    c = f.get("DTWEXBGS_chg_63")
    return -np.sign(c) if c is not None else pd.Series(np.nan, index=f.index)


def vol_regime_trend(f, n=200, mult=1.5):
    t = ma_trend(f, n)
    high_vol = f["vol"] > mult * f["vol"].rolling(252, min_periods=126).median()
    return t.where(~high_vol, 0.5 * t)


def seasonal(f):
    return np.sign(f["season_score"])


def seasonal_trend(f, n=200):
    s, t = seasonal(f), ma_trend(f, n)
    return s.where(s == t, 0.0)


def multi_factor(f):
    parts = [np.sign(f["ret_252"]), np.sign(f["carry"])]
    if "mm_pct" in f:
        parts.append(cot_contrarian(f).fillna(0))
    return sum(p.fillna(0) for p in parts) / len(parts)


STRATEGIES = {
    "tsmom": tsmom, "tsmom_12_1": tsmom_12_1, "ma_trend": ma_trend, "ma_cross": ma_cross,
    "donchian": donchian, "vol_breakout": vol_breakout, "roc": roc, "trend_template": trend_template,
    "vcp_breakout": vcp_breakout, "mean_reversion": mean_reversion, "carry": carry, "carry_z": carry_z,
    "mom_carry": mom_carry, "trend_carry_filter": trend_carry_filter, "cot_contrarian": cot_contrarian,
    "cot_momentum": cot_momentum, "trend_cot": trend_cot, "macro_real_yield": macro_real_yield,
    "macro_usd": macro_usd, "vol_regime_trend": vol_regime_trend, "seasonal": seasonal,
    "seasonal_trend": seasonal_trend, "multi_factor": multi_factor,
}


def signal(name: str, f: pd.DataFrame, params: dict | None = None) -> pd.Series:
    s = STRATEGIES[name](f, **(params or {}))
    return pd.Series(s, index=f.index).astype(float).clip(-1, 1)


# ---------------------------------------------------------------- multi-root strategies
def gold_silver_rv(feats: dict, z_in=2.0, z_out=0.5, window=252) -> dict:
    """Type B: mean reversion of the log gold/silver ratio (both legs vol-scaled by the engine)."""
    g, s = feats["GC"]["idx"], feats["SI"]["idx"]
    ix = g.index.intersection(s.index)
    ratio = np.log(g[ix] / s[ix])
    z = (ratio - ratio.rolling(window).mean()) / ratio.rolling(window).std()
    pos, out = 0.0, np.zeros(len(ix))
    for i, v in enumerate(z.values):
        if np.isnan(v):
            continue
        if pos == 0 and abs(v) > z_in:
            pos = -np.sign(v)            # ratio high -> short gold / long silver
        elif pos != 0 and abs(v) < z_out:
            pos = 0.0
        out[i] = pos
    sig = pd.Series(out, index=ix)
    return {"GC": sig, "SI": -sig}


def xs_momentum(feats: dict, lookback="ret_252", n_long=2, n_short=2) -> dict:
    """Type C: rank roots on trailing return; long top n, short bottom n (low breadth - see 03 s.9)."""
    df = pd.DataFrame({r: f[lookback] for r, f in feats.items()})
    ranks = df.rank(axis=1)
    n = df.notna().sum(axis=1)
    longs = ranks.gt(n - n_long, axis=0)
    shorts = ranks.le(n_short, axis=0)
    sig = longs.astype(float) - shorts.astype(float)
    sig[n < n_long + n_short + 1] = 0.0
    return {r: sig[r] for r in df.columns}


MULTI = {"gold_silver_rv": gold_silver_rv, "xs_momentum": xs_momentum}
