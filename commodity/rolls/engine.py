"""Roll engine: which contract is held each day, when it rolls, and the resulting tradable returns.

Rules (02 s.B.6, OPEN-3.8; roll method is a research variable, never hard-coded):
  ROLL_A  calendar      : nth business day of the delivery-risk month (capped at the deadline)
  ROLL_B  volume        : next contract's lagged volume > current for k consecutive days
  ROLL_C  open interest : next contract's lagged OI > current for k consecutive days
  ROLL_D  volume + OI   : both B and C conditions
  ROLL_E  days-before   : fixed business days before delivery_risk_date
  ROLL_F  carry-aware   : at the ROLL_E date choose, among the next 3 eligible contracts, the one
                          with the highest annualised roll-down (long-exposure convention)
All rules: only liquid months; position must be out by delivery_risk_date - buffer (forced roll);
volume/OI used with a 1-day lag (no look-ahead); roll executes at the settle of the roll date.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.config import market
from ..core.contracts import spec

RULES = ["ROLL_A", "ROLL_B", "ROLL_C", "ROLL_D", "ROLL_E", "ROLL_F"]


def _pivot(prices: pd.DataFrame, col: str) -> pd.DataFrame:
    return prices.pivot_table(index="trade_date", columns="contract_id", values=col, aggfunc="last").sort_index()


def build_schedule(prices: pd.DataFrame, ccal: pd.DataFrame, root: str, rule: str, params: dict | None = None):
    """Return (held, events): held = Series(trade_date -> contract held after the close),
    events = DataFrame of roll events. Uses only information available at each close."""
    m = market(root)
    p = dict(m["roll"])
    p.update(params or {})
    calname = m["calendar"]
    st = _pivot(prices, "settle")
    vol = _pivot(prices, "volume").reindex_like(st).shift(1)
    oi = _pivot(prices, "open_interest").reindex_like(st).shift(1)
    cc = ccal[(ccal.root == root) & ccal.is_liquid_month & ccal.contract_id.isin(st.columns)].sort_values("ltd")
    cc = cc.set_index("contract_id")
    if cc.empty:
        raise ValueError(f"no liquid contracts with data for {root}")
    deadline = {c: cal.bd_offset(calname, r, -p["buffer_bd"]) for c, r in cc.delivery_risk_date.items()}
    e_date = {c: cal.bd_offset(calname, r, -p["days_before"]) for c, r in cc.delivery_risk_date.items()}
    a_date = {}
    for c, r in cc.delivery_risk_date.items():
        bds = cal.month_bds(calname, r.year, r.month)
        a_date[c] = min(bds[min(p["calendar_bd"], len(bds)) - 1], deadline[c])
    order = list(cc.index)
    ltd = cc.ltd.to_dict()
    dates = st.index
    stv = st.values
    col = {c: i for i, c in enumerate(st.columns)}

    def has(c, i):
        return not np.isnan(stv[i, col[c]])

    def eligible(i, after=None):
        t = dates[i]
        out = []
        for c in order:
            if after is not None and ltd[c] <= ltd[after]:
                continue
            if t <= deadline[c] and has(c, i):
                out.append(c)
        return out

    held, events = [], []
    cur, streak = None, 0
    for i, t in enumerate(dates):
        if cur is None:
            el = eligible(i)
            # start in a contract that is not already inside its own roll window
            el = [c for c in el if t < e_date[c]] or el
            cur = el[0] if el else None
            if cur is None:
                held.append(None)
                continue
        nxt_list = eligible(i, after=cur)
        nxt = nxt_list[0] if nxt_list else None
        roll_to, reason = None, None
        if nxt is not None and has(cur, i):
            forced = t >= deadline[cur]
            if rule == "ROLL_A" and t >= a_date[cur]:
                roll_to, reason = nxt, "calendar"
            elif rule in ("ROLL_E", "ROLL_F") and t >= e_date[cur]:
                roll_to, reason = nxt, "days_before"
                if rule == "ROLL_F" and len(nxt_list) > 1:
                    best, best_c = -np.inf, nxt
                    prev = cur
                    for c in nxt_list[:3]:
                        dt_y = (ltd[c] - ltd[prev]).days / 365.0
                        ry = np.log(stv[i, col[prev]] / stv[i, col[c]]) / dt_y if dt_y > 0 else -np.inf
                        if ry > best:
                            best, best_c = ry, c
                        prev = c
                    roll_to, reason = best_c, "carry_aware"
            elif rule in ("ROLL_B", "ROLL_C", "ROLL_D"):
                cv, nv = vol.iat[i, col[cur]], vol.iat[i, col[nxt]]
                co, no = oi.iat[i, col[cur]], oi.iat[i, col[nxt]]
                cond_v = nv > cv if not (np.isnan(cv) or np.isnan(nv)) else False
                cond_o = no > co if not (np.isnan(co) or np.isnan(no)) else False
                cond = {"ROLL_B": cond_v, "ROLL_C": cond_o, "ROLL_D": cond_v and cond_o}[rule]
                streak = streak + 1 if cond else 0
                if streak >= p["crossover_days"]:
                    roll_to, reason = nxt, "crossover"
            if roll_to is None and forced:
                roll_to, reason = nxt, "forced_deadline"
        elif nxt is not None and not has(cur, i) and t > deadline[cur]:
            roll_to, reason = nxt, "forced_missing_data"
        if roll_to is not None:
            events.append({"rule_id": rule, "root": root, "roll_date": t, "from_contract": cur,
                           "to_contract": roll_to, "reason": reason})
            cur, streak = roll_to, 0
        held.append(cur)
    held = pd.Series(held, index=dates, name="held_contract")
    return held, pd.DataFrame(events, columns=["rule_id", "root", "roll_date", "from_contract", "to_contract", "reason"])


def tradable_returns(prices: pd.DataFrame, held: pd.Series, root: str, rule: str,
                     cost_mult: float = 1.0) -> pd.DataFrame:
    """Same-contract chained returns (02 P2): return on t uses the contract held at close t-1.
    Roll cost (one calendar-spread trade + 2 commissions) is charged on the roll date.
    Missing settle on the held contract: return 0 that day, multi-day return booked when data returns."""
    m = market(root)
    st = _pivot(prices, "settle").reindex(held.index)
    col = {c: i for i, c in enumerate(st.columns)}
    stv = st.values
    rows = []
    last_px = {}
    prev_c = None
    abs_hist = []
    for i, t in enumerate(st.index):
        c_ret = held.iloc[i - 1] if i > 0 else None
        c_now = held.iloc[i]
        sp = spec(root, t)
        r, s_prev, s_now, flag = np.nan, np.nan, np.nan, ""
        if c_ret is not None and c_ret in col:
            s_now = stv[i, col[c_ret]]
            s_prev = last_px.get(c_ret, np.nan)
            if np.isnan(s_now):
                r, flag = 0.0, "missing"
            elif not np.isnan(s_prev):
                floor = 0.05 * np.median(abs_hist[-252:]) if abs_hist else 0.0
                if abs(s_prev) < max(floor, 1e-12) or s_prev <= 0:
                    base = max(floor, abs(s_prev), 1e-9)
                    r, flag = (s_now - s_prev) / base, "notional_floor"
                else:
                    r = s_now / s_prev - 1.0
        # update last observed prices for all contracts
        for c, j in col.items():
            v = stv[i, j]
            if not np.isnan(v):
                last_px[c] = v
        rolled = c_now is not None and c_ret is not None and c_now != c_ret
        cost = 0.0
        if rolled:
            px = last_px.get(c_ret, np.nan)
            cost_ccy = cost_mult * (m["costs"]["roll_spread_ticks"] * sp["tick"] * sp["multiplier"] + 2 * sp["commission"])
            cost = cost_ccy / abs(px * sp["multiplier"]) if px and not np.isnan(px) else 0.0
        if c_ret is not None and not np.isnan(s_now):
            abs_hist.append(abs(s_now))
        rows.append((t, c_ret, c_now, s_prev, s_now, r, rolled, cost, flag, sp["multiplier"]))
        prev_c = c_now
    df = pd.DataFrame(rows, columns=["trade_date", "held_contract", "next_held", "settle_prev", "settle",
                                     "gross_return", "roll_flag", "roll_cost", "flag", "multiplier"])
    df["gross_return"] = df["gross_return"].fillna(0.0)
    df["net_return"] = df["gross_return"] - df["roll_cost"]
    df["point_change"] = (df["settle"] - df["settle_prev"]).fillna(0.0)
    df["index_level"] = 100 * (1 + df["net_return"]).cumprod()
    df["gross_index"] = 100 * (1 + df["gross_return"]).cumprod()
    df.insert(0, "root", root)
    df.insert(0, "rule_id", rule)
    return df.set_index("trade_date")


def adjusted_series(prices: pd.DataFrame, held: pd.Series, method: str) -> pd.Series:
    """Research price views (02 s.B.4): 'unadjusted', 'panama' (difference), 'ratio'.
    Generated dynamically; never used for P&L. Value on t = settle of the contract held over day t."""
    st = _pivot(prices, "settle").reindex(held.index)
    over = held.shift(1).fillna(held)
    px = pd.Series([st.at[t, c] if c in st.columns else np.nan for t, c in over.items()], index=held.index)
    if method == "unadjusted":
        return px
    adj = px.copy()
    rolls = [t for t, c_old, c_new in zip(held.index, over, held) if c_old != c_new]
    for t in rolls:
        c_old, c_new = over[t], held[t]
        old_px, new_px = st.at[t, c_old], st.at[t, c_new]
        if np.isnan(old_px) or np.isnan(new_px):
            continue
        before = adj.index <= t
        if method == "panama":
            adj[before] = adj[before] + (new_px - old_px)
        elif method == "ratio":
            adj[before] = adj[before] * (new_px / old_px)
    return adj
