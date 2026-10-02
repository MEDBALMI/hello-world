"""Backtest engine.

Two modes sharing the same signals, roll schedule and sizing:
  * fractional (research): unit-notional weights on chained tradable returns (02 s.B.5 'unit tradable')
  * contracts  (realistic): integer lots, equity path, trade log, rolls as trades (02 P1-P9)
Timing: signal at close t -> weight held from close t+exec_lag -> earns returns from t+exec_lag+1.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core.config import market, mcx_charges
from ..core.contracts import spec, spec_frame


def apply_exits(sig: pd.Series, idx: pd.Series, atr_pct: pd.Series, stop_atr: float | None = None,
                time_stop: int | None = None) -> pd.Series:
    """Trailing ATR stop and time stop. After an exit, stay flat until the raw signal changes."""
    if not stop_atr and not time_stop:
        return sig
    out = np.zeros(len(sig))
    pos, best, age, blocked = 0.0, np.nan, 0, None
    for i, (s, p, a) in enumerate(zip(sig.fillna(0).values, idx.values, atr_pct.fillna(0.02).values)):
        if blocked is not None and np.sign(s) != blocked:
            blocked = None
        target = 0.0 if blocked is not None else s
        if np.sign(target) != np.sign(pos):
            pos, best, age = target, p, 0
        elif pos != 0:
            pos = target
            age += 1
            best = max(best, p) if pos > 0 else min(best, p)
            hit_stop = stop_atr and ((pos > 0 and p < best * (1 - stop_atr * a)) or (pos < 0 and p > best * (1 + stop_atr * a)))
            hit_time = time_stop and age >= time_stop
            if hit_stop or hit_time:
                blocked, pos = np.sign(pos), 0.0
        out[i] = pos
    return pd.Series(out, index=sig.index)


def cost_fraction(trd: pd.DataFrame, root: str, cost_mult: float = 1.0) -> pd.Series:
    """One-way transaction cost per unit notional (slippage + commission [+ MCX statutory charges])."""
    m = market(root)
    sp = spec_frame(root, trd.index)
    px = trd["settle"].abs().where(trd["settle"].abs() > 0)
    per_contract = m["costs"]["slippage_ticks"] * sp["tick"] * sp["multiplier"] + sp["commission"]
    c = (per_contract / (px * sp["multiplier"])).ffill().bfill() * cost_mult
    if m.get("venue") == "MCX":
        ch = mcx_charges()
        c = c + cost_mult * (ch["ctt_sell"] / 2 + ch["stamp_duty_buy"] / 2 +
                             ch["exchange_txn"] * (1 + ch["gst_on_fees"]) + ch["sebi_fee"])
    return c


def run_fractional(trd: pd.DataFrame, sig: pd.Series, vol: pd.Series, root: str, *, target_vol=0.10,
                   max_weight=1.0, exec_lag=1, cost_mult=1.0, fx_ret: pd.Series | None = None) -> pd.DataFrame:
    """Return frame with held weight, gross pnl, costs and net return for one root."""
    sig = sig.reindex(trd.index).fillna(0)
    v = vol.reindex(trd.index).replace(0, np.nan)
    target = (sig * target_vol / v).clip(-max_weight, max_weight).fillna(0)
    held = target.shift(exec_lag).fillna(0)
    r = trd["gross_return"] - cost_mult * trd["roll_cost"]
    if fx_ret is not None:          # convert to base currency (e.g. USD contract for an INR investor)
        f = fx_ret.reindex(trd.index).fillna(0)
        r = (1 + r) * (1 + f) - 1 - f   # only the notional exposure is FX-converted; collateral assumed in base ccy
    pnl = held.shift(1).fillna(0) * r
    turn = held.diff().abs().fillna(held.abs())
    cost = turn * cost_fraction(trd, root, cost_mult)
    return pd.DataFrame({"held": held, "pnl": pnl, "cost": cost, "ret": pnl - cost, "gross_lev": held.abs()})


def combine(results: dict, alloc: pd.DataFrame | None = None, portfolio_vol: float | None = None,
            max_leverage: float = 3.0, halflife: int = 60) -> pd.DataFrame:
    """Combine per-root results with allocation weights (default equal), optional portfolio vol
    targeting using trailing realised vol (past only) and a gross leverage cap."""
    rets = pd.DataFrame({k: v["ret"] for k, v in results.items()}).fillna(0)
    held = pd.DataFrame({k: v["held"] for k, v in results.items()}).fillna(0)
    if alloc is None:
        active = (held != 0) | held.notna()
        alloc = pd.DataFrame(1.0 / rets.shape[1], index=rets.index, columns=rets.columns)
    alloc = alloc.reindex(rets.index).ffill().fillna(0)
    port = (alloc.shift(1).fillna(0) * rets).sum(axis=1)
    scale = pd.Series(1.0, index=rets.index)
    if portfolio_vol:
        rv = np.sqrt((port ** 2).ewm(halflife=halflife, min_periods=60).mean() * 252)
        scale = (portfolio_vol / rv).clip(upper=5).shift(1).fillna(1.0)
    gross = (alloc * held.abs()).sum(axis=1) * scale
    cap = (max_leverage / gross).clip(upper=1.0).fillna(1.0)
    scale = scale * cap.shift(1).fillna(1.0)
    return pd.DataFrame({"ret": port * scale, "gross_lev": gross * cap, "scale": scale})


def simulate_contracts(prices: pd.DataFrame, trd: pd.DataFrame, weight: pd.Series, root: str,
                       capital: float = 1_000_000.0, cost_mult: float = 1.0):
    """Integer-lot simulation. weight = notional/equity target already lagged (held from close t).
    Returns (equity Series, trades DataFrame, positions DataFrame)."""
    m = market(root)
    st = prices.pivot_table(index="trade_date", columns="contract_id", values="settle", aggfunc="last")
    st = st.reindex(trd.index)
    equity, lots, cur = capital, 0, None
    eq_hist, trades, pos_hist = [], [], []
    last_px = {}
    for t, row in trd.iterrows():
        sp = spec(root, t)
        mult, tick = sp["multiplier"], sp["tick"]
        c_ret, c_next = row["held_contract"], row["next_held"]
        px_ret = st.at[t, c_ret] if c_ret in st.columns else np.nan
        if cur is not None and lots != 0 and cur in st.columns:
            px_now = st.at[t, cur]
            if not np.isnan(px_now) and cur in last_px:
                equity += lots * (px_now - last_px[cur]) * mult
        for c in st.columns:
            v = st.at[t, c]
            if not np.isnan(v):
                last_px[c] = v
        # roll existing position at today's settle
        if lots != 0 and c_next is not None and cur is not None and c_next != cur and c_next in last_px:
            cost = cost_mult * abs(lots) * (m["costs"]["roll_spread_ticks"] * tick * mult + 2 * sp["commission"])
            trades.append((t, root, cur, -lots, last_px[cur], cost / 2, "ROLL"))
            trades.append((t, root, c_next, lots, last_px[c_next], cost / 2, "ROLL"))
            equity -= cost
            cur = c_next
        if cur is None:
            cur = c_next
        if cur is None or cur not in last_px:
            eq_hist.append((t, equity))
            continue
        w = weight.get(t, 0.0)
        w = 0.0 if np.isnan(w) else w
        px = last_px[cur]
        target_lots = int(np.round(w * equity / (abs(px) * mult))) if px else 0
        delta = target_lots - lots
        if delta != 0:
            cost = cost_mult * abs(delta) * (m["costs"]["slippage_ticks"] * tick * mult + sp["commission"])
            trades.append((t, root, cur, delta, px, cost, "SIGNAL"))
            equity -= cost
            lots = target_lots
        eq_hist.append((t, equity))
        pos_hist.append((t, root, cur, lots, px))
    eq = pd.Series(dict(eq_hist), name="equity")
    tr = pd.DataFrame(trades, columns=["trade_date", "root", "contract_id", "contracts", "price", "cost", "reason"])
    pos = pd.DataFrame(pos_hist, columns=["trade_date", "root", "contract_id", "contracts", "price"])
    return eq, tr, pos


def reconstruct_pnl(prices: pd.DataFrame, positions: pd.DataFrame, trades: pd.DataFrame, root: str,
                    capital: float) -> pd.Series:
    """Independent P&L reconstruction from end-of-day positions + trade costs (validation T13)."""
    st = prices.pivot_table(index="trade_date", columns="contract_id", values="settle", aggfunc="last").ffill()
    pos = positions.set_index("trade_date")
    pnl = pd.Series(0.0, index=pos.index)
    prev = None
    for t, row in pos.iterrows():
        if prev is not None and prev["contracts"] != 0:
            c = prev["contract_id"]
            # position after yesterday's close may have been rolled today: mark old contract to today's
            # settle up to the roll, which equals marking `c` (pre-roll contract) today
            p0, p1 = st.at[prev.name, c], st.at[t, c] if t in st.index else np.nan
            if not (np.isnan(p0) or np.isnan(p1)):
                pnl[t] += prev["contracts"] * (p1 - p0) * spec(root, t)["multiplier"]
        prev = row
    costs = trades.groupby("trade_date")["cost"].sum().reindex(pnl.index).fillna(0)
    return capital + (pnl - costs).cumsum()
