"""Statistical controls against data mining.

  block_bootstrap_sharpe : stationary-block bootstrap CI of the annualised Sharpe
  permutation_pvalue     : circular-shift test (keeps autocorrelation of signal and returns)
  deflated_sharpe        : Bailey & Lopez de Prado (2014) - adjusts for number/variance of trials
  bh_fdr                 : Benjamini-Hochberg false discovery rate across hypotheses
  reality_check          : White (2000)-style bootstrap of the best strategy among all tried
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

EULER = 0.5772156649


def sharpe(r: pd.Series | np.ndarray, ann: int = 252) -> float:
    r = np.asarray(pd.Series(r).dropna())
    return float(r.mean() / r.std() * np.sqrt(ann)) if len(r) > 2 and r.std() > 0 else np.nan


def _block_indices(n: int, block: int, rng) -> np.ndarray:
    idx = np.empty(n, dtype=int)
    i = 0
    while i < n:
        start = rng.integers(0, n)
        length = rng.geometric(1 / block)
        for k in range(min(length, n - i)):
            idx[i + k] = (start + k) % n
        i += length
    return idx


def block_bootstrap_sharpe(r: pd.Series, reps: int = 500, block: int = 20, seed: int = 0) -> dict:
    x = np.asarray(r.dropna())
    if len(x) < 100:
        return {"lo": np.nan, "hi": np.nan, "p_le_0": np.nan}
    rng = np.random.default_rng(seed)
    sims = np.array([sharpe(x[_block_indices(len(x), block, rng)]) for _ in range(reps)])
    return {"lo": float(np.nanpercentile(sims, 5)), "hi": float(np.nanpercentile(sims, 95)),
            "p_le_0": float(np.mean(sims <= 0))}


def permutation_pvalue(held: pd.Series, ret: pd.Series, reps: int = 300, seed: int = 0, min_shift: int = 252) -> float:
    """Circularly shift the position series against returns; p = share of shifted Sharpes >= actual."""
    h = held.reindex(ret.index).fillna(0).values
    r = ret.fillna(0).values
    n = len(r)
    if n < 2 * min_shift or np.all(h == 0):
        return np.nan
    actual = sharpe(np.roll(h, 1)[1:] * r[1:])
    rng = np.random.default_rng(seed)
    shifts = rng.integers(min_shift, n - min_shift, reps)
    sims = np.array([sharpe(np.roll(h, s + 1)[1:] * r[1:]) for s in shifts])
    return float((np.sum(sims >= actual) + 1) / (reps + 1))


def deflated_sharpe(r: pd.Series, n_trials: int, trial_sharpes_var: float) -> dict:
    """Probability that the true Sharpe exceeds the expected maximum of n_trials unskilled trials.
    Sharpe values here are per-period (daily); trial_sharpes_var is the variance of ANNUALISED
    trial Sharpes and is converted."""
    x = np.asarray(r.dropna())
    T = len(x)
    if T < 100 or x.std() == 0:
        return {"dsr": np.nan, "p": np.nan, "sr0_ann": np.nan}
    sr = x.mean() / x.std()
    var_daily = max(trial_sharpes_var, 1e-12) / 252.0
    N = max(int(n_trials), 2)
    sr0 = np.sqrt(var_daily) * ((1 - EULER) * stats.norm.ppf(1 - 1 / N) + EULER * stats.norm.ppf(1 - 1 / (N * np.e)))
    sk, ku = stats.skew(x), stats.kurtosis(x, fisher=False)
    denom = np.sqrt(max(1 - sk * sr + (ku - 1) / 4 * sr ** 2, 1e-12))
    dsr = stats.norm.cdf((sr - sr0) * np.sqrt(T - 1) / denom)
    return {"dsr": float(dsr), "p": float(1 - dsr), "sr0_ann": float(sr0 * np.sqrt(252))}


def bh_fdr(pvals: dict, q: float = 0.10) -> dict:
    items = [(k, v) for k, v in pvals.items() if v is not None and not np.isnan(v)]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    cutoff = 0
    for i, (_, p) in enumerate(items, 1):
        if p <= q * i / m:
            cutoff = i
    passed = {k for k, _ in items[:cutoff]}
    return {k: (k in passed) for k in pvals}


def reality_check(returns: pd.DataFrame, reps: int = 500, block: int = 20, seed: int = 0) -> dict:
    """White's reality check on mean daily returns of all strategies tried (columns)."""
    R = returns.fillna(0).values
    if R.shape[0] < 100 or R.shape[1] == 0:
        return {"p": np.nan, "best": None}
    n = R.shape[0]
    means = R.mean(axis=0)
    stat = np.sqrt(n) * means.max()
    centered = R - means
    rng = np.random.default_rng(seed)
    sims = np.empty(reps)
    for b in range(reps):
        idx = _block_indices(n, block, rng)
        sims[b] = np.sqrt(n) * centered[idx].mean(axis=0).max()
    return {"p": float(np.mean(sims >= stat)), "best": returns.columns[int(means.argmax())]}
