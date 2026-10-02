"""Performance metrics on daily return series (fully collateralised excess returns)."""
from __future__ import annotations

import numpy as np
import pandas as pd

ANN = 252


def drawdown(r: pd.Series) -> pd.Series:
    eq = (1 + r.fillna(0)).cumprod()
    return eq / eq.cummax() - 1


def trades_from_weights(r: pd.Series, held: pd.Series) -> pd.Series:
    """Trade = maximal run of constant non-zero direction; trade P&L = sum of daily returns."""
    d = np.sign(held.shift(1).fillna(0))
    run = (d != d.shift()).cumsum()
    g = pd.DataFrame({"r": r, "d": d, "run": run})
    g = g[g.d != 0]
    return g.groupby("run")["r"].sum()


def compute(r: pd.Series, held: pd.Series | None = None, gross: pd.Series | None = None,
            margin_pct: float = 0.08) -> dict:
    r = r.dropna()
    if len(r) < 20 or r.std() == 0:
        return {"n_days": len(r), "sharpe": np.nan}
    years = len(r) / ANN
    eq = (1 + r).cumprod()
    dd = drawdown(r)
    vol = r.std() * np.sqrt(ANN)
    downside = r[r < 0].std() * np.sqrt(ANN)
    cagr = eq.iloc[-1] ** (1 / years) - 1 if eq.iloc[-1] > 0 else -1.0
    out = {
        "n_days": len(r), "years": years, "cagr": cagr, "ann_vol": vol,
        "sharpe": r.mean() / r.std() * np.sqrt(ANN),
        "sortino": r.mean() * ANN / downside if downside > 0 else np.nan,
        "max_dd": dd.min(), "avg_dd": dd[dd < 0].mean() if (dd < 0).any() else 0.0,
        "calmar": cagr / abs(dd.min()) if dd.min() < 0 else np.nan,
        "skew": r.skew(), "worst_day": r.min(),
    }
    if held is not None:
        h = held.reindex(r.index).fillna(0)
        tr = trades_from_weights(r, h)
        wins, losses = tr[tr > 0], tr[tr < 0]
        streak = mx = 0
        for v in tr.values:
            streak = streak + 1 if v < 0 else 0
            mx = max(mx, streak)
        out.update({
            "n_trades": int(len(tr)), "win_rate": len(wins) / len(tr) if len(tr) else np.nan,
            "profit_factor": wins.sum() / -losses.sum() if len(losses) and losses.sum() != 0 else np.nan,
            "expectancy": tr.mean() if len(tr) else np.nan,
            "avg_winner": wins.mean() if len(wins) else np.nan, "avg_loser": losses.mean() if len(losses) else np.nan,
            "worst_trade": tr.min() if len(tr) else np.nan, "longest_losing_streak": int(mx),
            "exposure": float((h != 0).mean()), "turnover": float(h.diff().abs().sum() / years),
        })
    if gross is not None:
        g = gross.reindex(r.index).fillna(0)
        out["avg_gross_leverage"] = float(g.mean())
        out["margin_utilisation"] = float((g * margin_pct).mean())
    out["return_over_maxdd"] = out["cagr"] / abs(out["max_dd"]) if out["max_dd"] < 0 else np.nan
    return out
