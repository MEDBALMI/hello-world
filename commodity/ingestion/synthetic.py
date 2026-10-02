"""Synthetic market generator — ENGINEERING VALIDATION ONLY, never research evidence.

Purpose: exercise every pipeline stage end-to-end and measure whether the research machinery
(a) rejects strategies when there is no edge (scenario NULL) and
(b) detects a known, planted effect (scenario CARRY: expected return proportional to backwardation).

Model per root (log futures price for contract with maturity T, time to maturity tau in years):
    log F(t,T) = L_t + s_t * tau + season(month(T)) + e_T(t)
    dL = s_t * dcal/365 + sigma_t * z1 - sigma_t^2/2 + mu_t (+ soft barrier beyond x8 or /8 of start) ;  ds = sigma_s * z2 ;  e_T random walk (tiny)
which makes every individual contract a martingale (mu_t = 0) -> no strategy has an edge.
Scenario CARRY sets mu_t = lam * (-s_t) * dcal/365 (backwardation premium).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.config import market
from ..core.contracts import contract_calendar, spec

SOURCE_ID = "SYNTHETIC"

PARAMS = {
    # base price, annual vol, slope vol (per sqrt yr), initial slope, seasonal amplitude
    "GC": dict(p0=400.0, vol=0.15, svol=0.010, s0=0.03, season=0.0),
    "SI": dict(p0=5.0, vol=0.27, svol=0.012, s0=0.03, season=0.0),
    "HG": dict(p0=1.0, vol=0.24, svol=0.030, s0=0.01, season=0.0),
    "CL": dict(p0=18.0, vol=0.35, svol=0.050, s0=0.00, season=0.0),
    "NG": dict(p0=2.0, vol=0.50, svol=0.060, s0=0.05, season=0.10),
    "MCX_ALUMINIUM": dict(p0=80.0, vol=0.20, svol=0.030, s0=0.02, season=0.0),
}
# MCX roots linked to a global root: INR price = USD price * USDINR * factor * (1 + duty)
MCX_LINK = {
    "MCX_GOLD": ("GC", 10 / 31.1035, 0.06),
    "MCX_SILVER": ("SI", 32.1507, 0.06),
    "MCX_CRUDEOIL": ("CL", 1.0, 0.0),
    "MCX_NATURALGAS": ("NG", 1.0, 0.0),
    "MCX_COPPER": ("HG", 2.20462, 0.05),
}


def _round_tick(x, tick):
    return np.round(np.asarray(x) / tick) * tick


def _state(dates: pd.DatetimeIndex, p: dict, rng, scenario: str, lam: float):
    n = len(dates)
    dcal = np.r_[1, np.diff(dates.values).astype("timedelta64[D]").astype(int)]
    # GARCH(1,1)-like daily variance around the annual vol
    var0 = p["vol"] ** 2 / 252
    a, b = 0.06, 0.92
    w = var0 * (1 - a - b)
    z1 = rng.standard_normal(n)
    sig = np.empty(n)
    v = var0
    for i in range(n):
        sig[i] = np.sqrt(v)
        v = w + a * (sig[i] * z1[i]) ** 2 + b * v
    s = p["s0"] + np.cumsum(p["svol"] * np.sqrt(dcal / 365) * rng.standard_normal(n))
    s_prev = np.r_[p["s0"], s[:-1]]
    mu = lam * (-s_prev) * dcal / 365 if scenario == "CARRY" else np.zeros(n)
    base = s_prev * dcal / 365 + sig * z1 - 0.5 * sig ** 2 + mu   # -0.5 sig^2: arithmetic martingale
    # Soft barrier: pure martingale inside +-log(8) of the start level; mean reversion (2/yr) only on the
    # excess beyond the band. Keeps 30-year paths in a realistic range (no zero prices); introduces
    # predictability only in rare extreme states (documented limitation of the synthetic null).
    band, k_out, L0 = np.log(8.0), 2.0, np.log(p["p0"])
    L = np.empty(n)
    cur = L0
    for i in range(n):
        dev = cur - L0
        excess = np.sign(dev) * max(abs(dev) - band, 0.0)
        cur = cur + base[i] - k_out * excess * dcal[i] / 365
        L[i] = cur
    return L, s, sig


def _volume_oi(days_to_risk: np.ndarray, liquid: bool, rng, base_vol: float):
    w = np.exp(-((days_to_risk - 45.0) / 70.0) ** 2)
    w = np.where(days_to_risk < 0, 0.02, w)
    w = w * (1.0 if liquid else 0.05) + 0.002
    vol = rng.poisson(base_vol * w).astype(float)
    target = base_vol * 4 * np.convolve(w, np.ones(10) / 10, mode="same")
    oi = np.empty_like(vol)
    cur = 0.0
    for i in range(len(vol)):
        step = np.clip(target[i] - cur, -vol[i], vol[i])
        cur = max(cur + step, 0.0)
        oi[i] = round(cur)
    return vol, oi


def _contract_rows(root, contracts, dates, logF_fn, rng, tick, base_vol):
    out = []
    for c in contracts.itertuples():
        mask = (dates >= c.listing_date) & (dates <= c.ltd)
        d = dates[mask]
        if len(d) < 5:
            continue
        logf = logF_fn(c, d, mask)
        if logf is None:
            continue
        settle = _round_tick(np.exp(logf), tick)
        dvol = np.r_[np.nan, np.diff(logf)]
        sd = np.nanstd(dvol) if len(d) > 2 else 0.01
        prev = np.r_[settle[0], settle[:-1]]
        opn = _round_tick(prev * np.exp(rng.normal(0, 0.3 * sd, len(d))), tick)
        hi = _round_tick(np.maximum(opn, settle) * np.exp(np.abs(rng.normal(0, 0.5 * sd, len(d)))), tick)
        lo = _round_tick(np.minimum(opn, settle) * np.exp(-np.abs(rng.normal(0, 0.5 * sd, len(d)))), tick)
        dtr = np.array([(c.delivery_risk_date - x).days for x in d], dtype=float)
        vol, oi = _volume_oi(dtr, c.is_liquid_month, rng, base_vol)
        out.append(pd.DataFrame({
            "root": root, "contract_id": c.contract_id, "trade_date": d,
            "open": opn, "high": hi, "low": lo, "close": settle, "settle": settle,
            "volume": vol, "open_interest": oi,
        }))
    return out


def generate(start="1995-01-01", end="2025-12-31", scenario="NULL", lam=1.5, seed=7,
             roots=("GC", "SI", "HG", "CL", "NG"), mcx=True) -> dict:
    """Return dict with prices, contract_calendar, cot, macro, fx, rates frames."""
    rng = np.random.default_rng(seed)
    frames, cals, curve_state = [], [], {}
    for root in roots:
        m, p = market(root), PARAMS[root]
        dates = cal.business_days(m["calendar"], start, end)
        L, s, sig = _state(dates, p, rng, scenario, lam)
        curve_state[root] = (dates, L, s)
        cc = contract_calendar(root, start, end)
        cals.append(cc)
        season_amp = p["season"]
        idio_vol = 0.002

        def logF_fn(c, d, mask, L=L, s=s, season_amp=season_amp, dates=dates):
            tau = np.array([(c.ltd - x).days for x in d]) / 365.0
            season = season_amp * np.cos(2 * np.pi * (c.contract_month.month - 1) / 12)  # winter premium
            idio = np.cumsum(rng.normal(0, idio_vol, len(d)))
            return L[mask] + s[mask] * tau + season + idio

        tick = spec(root, start)["tick"]
        frames += _contract_rows(root, cc, dates, logF_fn, rng, tick, base_vol=20000)

    # FX + rates + macro (random walks; no planted relationship)
    bdays = cal.business_days("CME", start, end)
    n = len(bdays)
    usdinr = 31.0 * np.exp(np.cumsum(0.035 / 252 + 0.05 / np.sqrt(252) * rng.standard_normal(n)))
    fx = pd.DataFrame({"pair": "USDINR", "fixing": "SYNTH", "obs_date": bdays, "value": usdinr})
    rates = pd.DataFrame({"rate_id": "USD_3M_TBILL", "obs_date": bdays,
                          "value": np.clip(4 + np.cumsum(0.06 * rng.standard_normal(n)), 0, 9)})
    macro = []
    for sid, x0, step in (("DFII10", 1.5, 0.04), ("DGS10", 4.0, 0.05), ("DTWEXBGS", 100.0, 0.4)):
        macro.append(pd.DataFrame({"series_id": sid, "obs_date": bdays,
                                   "value": x0 + np.cumsum(step * rng.standard_normal(n))}))
    macro = pd.concat(macro)
    macro["available_ts"] = macro["obs_date"] + pd.Timedelta(days=1, hours=21)  # next-day evening UTC

    # MCX roots
    if mcx:
        fx_s = pd.Series(usdinr, index=bdays)
        for root, (groot, factor, duty) in MCX_LINK.items():
            if groot not in curve_state:
                continue
            m = market(root)
            dates = cal.business_days("MCX", max(pd.Timestamp(start), pd.Timestamp("2005-01-01")), end)
            gd, gL, gs = curve_state[groot]
            L = pd.Series(gL, index=gd).reindex(dates).ffill().values
            S = pd.Series(gs, index=gd).reindex(dates).ffill().values
            fxv = fx_s.reindex(dates).ffill().values
            cc = contract_calendar(root, dates[0], end)
            cals.append(cc)

            def logF_fn(c, d, mask, L=L, S=S, fxv=fxv, factor=factor, duty=duty):
                tau = np.array([(c.ltd - x).days for x in d]) / 365.0 + 0.05
                basis = np.cumsum(rng.normal(0, 0.001, len(d)))
                return L[mask] + S[mask] * tau + np.log(fxv[mask] * factor * (1 + duty)) + basis

            frames += _contract_rows(root, cc, dates, logF_fn, rng, spec(root, dates[0])["tick"], 5000)
        # standalone MCX aluminium (no global benchmark)
        root, p = "MCX_ALUMINIUM", PARAMS["MCX_ALUMINIUM"]
        dates = cal.business_days("MCX", "2005-01-01", end)
        L, s, _ = _state(dates, p, rng, scenario, lam)
        cc = contract_calendar(root, dates[0], end)
        cals.append(cc)

        def logF_fn(c, d, mask, L=L, s=s):
            tau = np.array([(c.ltd - x).days for x in d]) / 365.0
            return L[mask] + s[mask] * tau

        frames += _contract_rows(root, cc, dates, logF_fn, rng, spec(root, dates[0])["tick"], 3000)

    prices = pd.concat(frames, ignore_index=True)
    prices["source_id"] = SOURCE_ID
    ccal = pd.concat(cals, ignore_index=True)
    ccal = ccal[ccal.contract_id.isin(prices.contract_id.unique())].reset_index(drop=True)

    # COT (weekly, Tuesday as-of, Friday release) for global roots
    cot = []
    for root in roots:
        tues = pd.date_range(start, end, freq="W-TUE")
        k = len(tues)
        oi = 400000 * np.exp(np.cumsum(0.02 * rng.standard_normal(k)))
        net = np.zeros(k)
        for i in range(1, k):
            net[i] = 0.95 * net[i - 1] + 0.04 * rng.standard_normal()
        mm_long = oi * (0.20 + np.clip(net, 0, None))
        mm_short = oi * (0.20 + np.clip(-net, 0, None))
        cot.append(pd.DataFrame({
            "report_type": "disaggregated", "root": root, "as_of_date": tues,
            "release_ts": tues + pd.Timedelta(days=3, hours=19, minutes=30),  # Fri 15:30 ET ~ 19:30 UTC (EDT)
            "open_interest": oi, "mm_long": mm_long, "mm_short": mm_short,
            "pm_long": oi * 0.15, "pm_short": oi * 0.35, "sd_long": oi * 0.2, "sd_short": oi * 0.1,
        }))
    cot = pd.concat(cot, ignore_index=True)
    return {"prices": prices, "contract_calendar": ccal, "cot": cot, "macro": macro, "fx": fx,
            "rates": rates, "scenario": scenario, "data_class": "SYNTHETIC"}


def inject_defects(prices: pd.DataFrame, rng=None) -> tuple[pd.DataFrame, dict]:
    """Inject known defects (for validation self-tests)."""
    rng = rng or np.random.default_rng(0)
    p = prices.copy()
    idx = rng.choice(p.index, 6, replace=False)
    p.loc[idx[0], "volume"] = -5                       # T4
    p.loc[idx[1], "settle"] = p.loc[idx[1], "high"] * 1.05  # T3
    p.loc[idx[2], "settle"] = p.loc[idx[2], "settle"] + 0.0001234  # T8 off-tick
    p.loc[idx[3], "open_interest"] = -1               # T5
    dropped_contract = p.contract_id.iloc[len(p) // 2]
    p = p[p.contract_id != dropped_contract]          # T1 / T10
    gap_rows = p[p.contract_id == p.contract_id.iloc[100]].index[20:23]
    p = p.drop(gap_rows)                              # T2
    return p, {"dropped_contract": dropped_contract}
