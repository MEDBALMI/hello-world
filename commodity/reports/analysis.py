"""Descriptive/inferential analyses feeding the reports. All forward-return tests use
non-overlapping monthly sampling (21 trading days) to avoid inflated t-statistics."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as st

from ..backtests import metrics
from ..robustness.stats import sharpe


def fwd(r: pd.Series, h: int = 21) -> pd.Series:
    lr = np.log1p(r)
    return lr[::-1].rolling(h).sum()[::-1].shift(-1)


def ic(feature: pd.Series, r: pd.Series, h: int = 21) -> dict:
    df = pd.DataFrame({"x": feature, "y": fwd(r, h)}).dropna().iloc[::h]
    if len(df) < 24:
        return {"ic": np.nan, "t": np.nan, "n": len(df)}
    rho, p = st.spearmanr(df.x, df.y)
    return {"ic": float(rho), "t": float(rho * np.sqrt((len(df) - 2) / max(1 - rho ** 2, 1e-12))), "p": float(p), "n": len(df)}


def roll_comparison(c: dict) -> pd.DataFrame:
    rows = []
    cm = c["curve"]["CM30"]
    price_ret = np.log(cm).diff()
    for rule, trd in c["tradable"].items():
        r = trd["net_return"]
        lr = np.log1p(r)
        m = metrics.compute(r)
        yrs = len(r) / 252
        total = lr.sum() / yrs
        price = price_ret.reindex(r.index).sum() / yrs
        rows.append({"rule": rule, "total_return_ann": total, "price_return_ann(CM30)": price,
                     "roll_return_ann": total - price, "roll_cost_ann": trd["roll_cost"].sum() / yrs,
                     "rolls_per_year": int(trd["roll_flag"].sum()) / yrs,
                     "sharpe": m["sharpe"], "sortino": m["sortino"], "calmar": m["calmar"], "max_dd": m["max_dd"]})
    return pd.DataFrame(rows)


def term_structure(c: dict) -> dict:
    cv, trd = c["curve"], c["tradable"]["ROLL_E"]
    carry = cv["carry"].reindex(trd.index)
    out = {"pct_backwardation": float((carry > 0).mean()), "mean_carry": float(carry.mean()),
           "carry_autocorr_21d": float(carry.autocorr(21)) if carry.notna().sum() > 50 else np.nan,
           "ic_carry_fwd21": ic(carry, trd["net_return"]), "ic_slope_fwd21": ic(cv["slope_cm"].reindex(trd.index), trd["net_return"])}
    vol = trd["net_return"].rolling(21).std() * np.sqrt(252)
    out["vol_backwardation"] = float(vol[carry > 0].mean())
    out["vol_contango"] = float(vol[carry <= 0].mean())
    return out


def seasonality(trd: pd.DataFrame) -> dict:
    r = trd["net_return"]
    mr = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
    mr.index.names = ["y", "m"]
    df = mr.reset_index(name="ret")
    tab = df.groupby("m")["ret"].agg(["mean", "std", "count"])
    tab["t"] = tab["mean"] / (tab["std"] / np.sqrt(tab["count"]))
    groups = [g.ret.values for _, g in df.groupby("m")]
    kw = st.kruskal(*groups) if all(len(g) > 2 for g in groups) else None
    return {"table": tab, "kruskal_p": float(kw.pvalue) if kw else np.nan,
            "n_months_t_gt_2": int((tab["t"].abs() > 2).sum()),
            "expected_false_t_gt_2": 12 * 0.0455}


def positioning(c: dict) -> dict:
    f, trd = c["features"](), c["tradable"]["ROLL_E"]
    if "mm_z" not in f:
        return {}
    return {"ic_mm_z": ic(f["mm_z"], trd["net_return"]), "ic_mm_chg_4w": ic(f["mm_chg_4w"], trd["net_return"]),
            "mean_mm_net": float(f["mm_net"].mean()), "pct_extreme_hi": float((f["mm_pct"] > 0.9).mean())}


FEATURES_IC = ["ret_63", "ret_252", "tsmom_12_1", "dist_ma_200", "carry", "carry_z", "slope_cm", "carry_12m",
               "z_ret_5", "trend_template", "vcp_contraction", "season_score", "mm_z", "DFII10_chg_63", "DTWEXBGS_chg_63"]


def feature_ic(c: dict) -> pd.DataFrame:
    f, trd = c["features"](), c["tradable"]["ROLL_E"]
    rows = []
    for k in FEATURES_IC:
        if k in f:
            rows.append({"feature": k, **ic(f[k], trd["net_return"])})
    return pd.DataFrame(rows)


def cross_relationships(ctx: dict, macro: pd.DataFrame | None) -> pd.DataFrame:
    """Contemporaneous vs lagged (monthly, non-overlapping) relationships; split-half stability."""
    rows = []
    rets = {r: np.log1p(c["tradable"]["ROLL_E"]["net_return"]) for r, c in ctx.items()}
    m = {}
    if macro is not None and not macro.empty:
        for sid, g in macro.groupby("series_id"):
            m[sid] = g.set_index("obs_date")["value"].sort_index()
    pairs = [("GC", "SI"), ("GC", "HG"), ("HG", "CL"), ("CL", "NG")]
    def monthly(s):
        return s.resample("ME").sum()
    for a, b in pairs:
        if a in rets and b in rets:
            x, y = monthly(rets[a]), monthly(rets[b])
            rows.append(_rel(f"{a} vs {b}", x, y))
    for sid, roots in (("DFII10", ["GC", "SI"]), ("DTWEXBGS", ["GC", "HG", "CL"])):
        if sid in m:
            mx = m[sid].resample("ME").last().diff()
            for r in roots:
                if r in rets:
                    rows.append(_rel(f"{r} vs d{sid}", monthly(rets[r]), mx))
    return pd.DataFrame(rows)


def _rel(name, y, x):
    df = pd.DataFrame({"y": y, "x": x, "x_lag": x.shift(1)}).dropna()
    if len(df) < 36:
        return {"relationship": name, "n": len(df)}
    half = len(df) // 2
    c0 = st.pearsonr(df.x, df.y)
    c1 = st.pearsonr(df.x_lag, df.y)
    return {"relationship": name, "n": len(df), "contemp_corr": c0[0], "contemp_p": c0[1],
            "lagged_corr (predictive)": c1[0], "lagged_p": c1[1],
            "contemp_corr_first_half": st.pearsonr(df.x[:half], df.y[:half])[0],
            "contemp_corr_second_half": st.pearsonr(df.x[half:], df.y[half:])[0]}
