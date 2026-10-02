"""Portfolio construction and position-sizing comparisons.

Allocation methods operate on per-sleeve daily returns (each sleeve = one hypothesis x root,
already vol-targeted). All weights use trailing data only and are rebalanced monthly.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..backtests import metrics
from ..core.config import market


def _monthly(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    s = pd.Series(index, index=index)
    return pd.DatetimeIndex(s.groupby([index.year, index.month]).last().values)


def _erc(cov: np.ndarray, iters: int = 500, tol: float = 1e-10) -> np.ndarray:
    """Equal risk contribution via cyclical coordinate descent (Griveau-Billion, Richard & Roncalli 2013);
    stable with negative correlations. Solves sigma_ii w_i^2 + b_i w_i - 1/n = 0 for each i."""
    n = cov.shape[0]
    w = 1 / np.sqrt(np.diag(cov))
    w = w / w.sum()
    for _ in range(iters):
        w_old = w.copy()
        for i in range(n):
            a = cov[i, i]
            b = cov[i] @ w - a * w[i]
            w[i] = (-b + np.sqrt(b * b + 4 * a / n)) / (2 * a)
        if np.max(np.abs(w - w_old)) < tol:
            break
    return w / w.sum()


def weights(rets: pd.DataFrame, method: str, lookback: int = 252, sectors: dict | None = None,
            sector_cap: float = 0.5) -> pd.DataFrame:
    rebal = _monthly(rets.index)
    out = pd.DataFrame(np.nan, index=rets.index, columns=rets.columns)
    for t in rebal:
        hist = rets[rets.index <= t].tail(lookback).dropna(axis=1, how="all").fillna(0)
        cols = [c for c in hist.columns if hist[c].std() > 0]
        if len(cols) == 0 or len(hist) < 60:
            continue
        h = hist[cols]
        vol = h.std() * np.sqrt(252)
        if method == "equal":
            w = pd.Series(1.0 / len(cols), index=cols)
        elif method == "equal_vol":
            w = (1 / vol) / (1 / vol).sum()
        elif method == "risk_parity":
            w = pd.Series(_erc(h.cov().values * 252), index=cols)
        elif method == "corr_adjusted":
            corr = h.corr().fillna(0)
            avg = (corr.sum() - 1) / max(len(cols) - 1, 1)
            raw = (1 / vol) * (1 / (1 + avg.clip(lower=0)))
            w = raw / raw.sum()
        else:
            raise ValueError(method)
        if sectors:
            w = cap_sectors(w, h, sectors, sector_cap)
        out.loc[t, cols] = w.values
        out.loc[t, [c for c in rets.columns if c not in cols]] = 0.0
    return out.ffill().fillna(0)


def cap_sectors(w: pd.Series, hist: pd.DataFrame, sectors: dict, cap: float) -> pd.Series:
    """Cap each sector's share of portfolio RISK (marginal contribution) at `cap`; redistribute."""
    cov = hist.cov().values * 252
    for _ in range(10):
        rc = w.values * (cov @ w.values)
        total = rc.sum()
        if total <= 0:
            break
        share = pd.Series(rc / total, index=w.index).groupby(lambda c: sectors.get(c, "OTHER")).sum()
        over = share[share > cap]
        if over.empty:
            break
        for sec in over.index:
            members = [c for c in w.index if sectors.get(c, "OTHER") == sec]
            w[members] *= cap / share[sec]
        w = w / w.sum()
    return w


def sleeve_sector(sleeve: str) -> str:
    root = sleeve.split("|")[-1]
    return market(root).get("sector", "OTHER")


def build_portfolios(sleeves: pd.DataFrame, port_vol: float, sector_cap: float) -> dict:
    sectors = {c: sleeve_sector(c) for c in sleeves.columns}
    out = {}
    for method in ("equal", "equal_vol", "risk_parity", "corr_adjusted"):
        for capped in (False, True):
            w = weights(sleeves, method, sectors=sectors if capped else None, sector_cap=sector_cap)
            raw = (w.shift(1) * sleeves.fillna(0)).sum(axis=1)
            rv = np.sqrt((raw ** 2).ewm(halflife=60, min_periods=60).mean() * 252)
            scale = (port_vol / rv).clip(upper=4).shift(1).fillna(1.0)
            r = raw * scale
            name = method + ("+sector_cap" if capped else "")
            m = metrics.compute(r)
            risk_share = _risk_share(sleeves, w, sectors)
            m["max_sector_risk_share"] = float(max(risk_share.values())) if risk_share else np.nan
            m["sector_risk_share"] = risk_share
            out[name] = {"returns": r, "metrics": m}
    return out


def _risk_share(sleeves, w, sectors):
    h = sleeves.tail(252).fillna(0)          # same window as the allocation/cap estimate
    wt = w.iloc[-1].reindex(h.columns).fillna(0).values
    cov = h.cov().values * 252
    rc = wt * (cov @ wt)
    if rc.sum() <= 0:
        return {}
    s = pd.Series(rc / rc.sum(), index=h.columns).groupby(lambda c: sectors.get(c, "OTHER")).sum()
    return s.round(3).to_dict()
