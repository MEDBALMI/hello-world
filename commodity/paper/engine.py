"""Paper-trading engine (simulated execution only - never connects to a broker).

Daily cycle at the close of day t (same code path intended for production):
  1. mark positions to today's settlement
  2. fill orders decided at t-1 at today's settlement +/- slippage (exec lag 1, as in backtests)
  3. roll positions whose contract the roll schedule replaces today
  4. compute signals -> vol-targeted weights -> target lots -> orders for t+1
  5. risk checks + alerts (missing data, roll due, drawdown, leverage), audit log
State (positions, pending orders, equity) is JSON-serialisable and persisted to the database.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.config import market
from ..core.contracts import spec
from ..hypotheses.strategies import signal


@dataclass
class BookState:
    equity: float
    peak: float
    positions: dict = field(default_factory=dict)   # root -> {"contract": str, "lots": int, "px": float}
    pending: dict = field(default_factory=dict)     # root -> target lots for next fill
    last_date: str | None = None

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, s: str) -> "BookState":
        return cls(**json.loads(s))


class PaperBook:
    def __init__(self, name: str, cfg: dict, ctx: dict, state: BookState | None = None):
        self.name, self.cfg, self.ctx = name, cfg, ctx
        self.state = state or BookState(equity=cfg["capital"], peak=cfg["capital"])
        self.trades, self.equity_log, self.alerts, self.pos_log = [], [], [], []
        self.rule = cfg["roll_rule"]
        self.roots = [r for r in cfg["roots"] if r in ctx]

    def _px(self, root, contract, t):
        if not hasattr(self, "_pv"):
            self._pv = {r: self.ctx[r]["prices"].pivot_table(index="trade_date", columns="contract_id",
                                                             values="settle", aggfunc="last") for r in self.roots}
        pv = self._pv[root]
        try:
            return float(pv.at[t, contract])
        except KeyError:
            return np.nan

    def _target_weight(self, root, t) -> float:
        f = self.ctx[root]["features"](self.rule)
        if t not in f.index:
            return 0.0
        sigs = []
        for s in self.cfg["strategies"]:
            from ..core.config import hypotheses
            h = next(x for x in hypotheses() if x["id"] == s["id"])
            v = signal(h["strategy"], f.loc[:t], s.get("params")).iloc[-1]
            sigs.append(0.0 if np.isnan(v) else v)
        vol = f.at[t, "vol"]
        if not vol or np.isnan(vol):
            return 0.0
        w = np.mean(sigs) * self.cfg["target_vol"] / vol / len(self.roots)
        return float(np.clip(w, -1, 1))

    def step(self, t: pd.Timestamp) -> None:
        st, ts = self.state, str(t.date())
        pnl = 0.0
        for root in self.roots:
            m = market(root)
            sp = spec(root, t)
            pos = st.positions.get(root)
            held_sched = self.ctx[root]["schedules"][self.rule]
            if t not in held_sched.index:
                continue
            # 1. mark to market
            if pos and pos["lots"]:
                px = self._px(root, pos["contract"], t)
                if np.isnan(px):
                    self.alerts.append((ts, root, "MISSING_PRICE", pos["contract"]))
                else:
                    pnl += pos["lots"] * (px - pos["px"]) * sp["multiplier"]
                    pos["px"] = px
            # 2. fill pending orders at today's settle
            if root in st.pending:
                tgt = st.pending.pop(root)
                if pos is None:
                    pos = {"contract": held_sched.shift(1).get(t) or held_sched[t], "lots": 0, "px": np.nan}
                px = self._px(root, pos["contract"], t)
                delta = tgt - pos["lots"]
                if delta and not np.isnan(px):
                    cost = abs(delta) * (m["costs"]["slippage_ticks"] * sp["tick"] * sp["multiplier"] + sp["commission"])
                    self.trades.append((ts, root, pos["contract"], delta, px, cost, "SIGNAL"))
                    pnl -= cost
                    pos["lots"], pos["px"] = tgt, px
                st.positions[root] = pos
            # 3. roll if schedule switches contract at today's close
            pos = st.positions.get(root)
            new_c = held_sched[t]
            if pos and pos["lots"] and new_c and new_c != pos["contract"]:
                px_old, px_new = self._px(root, pos["contract"], t), self._px(root, new_c, t)
                if not (np.isnan(px_old) or np.isnan(px_new)):
                    cost = abs(pos["lots"]) * (m["costs"]["roll_spread_ticks"] * sp["tick"] * sp["multiplier"] + 2 * sp["commission"])
                    self.trades.append((ts, root, pos["contract"], -pos["lots"], px_old, cost / 2, "ROLL"))
                    self.trades.append((ts, root, new_c, pos["lots"], px_new, cost / 2, "ROLL"))
                    pnl -= cost
                    pos.update(contract=new_c, px=px_new)
            elif pos and not pos["lots"]:
                pos["contract"], pos["px"] = new_c, self._px(root, new_c, t)
            # roll-due alert
            if pos and pos["lots"]:
                cc = self.ctx[root]["ccal"].set_index("contract_id")
                if pos["contract"] in cc.index:
                    risk = cc.at[pos["contract"], "delivery_risk_date"]
                    bds = cal.business_days(m["calendar"])
                    left = bds.searchsorted(risk) - bds.searchsorted(t)
                    if left <= self.cfg["roll_alert_bd"] + m["roll"]["days_before"]:
                        self.alerts.append((ts, root, "ROLL_DUE", f"{pos['contract']} delivery risk in {left} bd"))
        st.equity += pnl
        st.peak = max(st.peak, st.equity)
        # 4. new targets for tomorrow
        gross = 0.0
        for root in self.roots:
            pos = st.positions.get(root) or {"contract": self.ctx[root]["schedules"][self.rule].get(t), "lots": 0, "px": np.nan}
            st.positions[root] = pos
            c = pos["contract"]
            if c is None:
                continue
            px = self._px(root, c, t)
            if np.isnan(px) or px == 0:
                continue
            mult = spec(root, t)["multiplier"]
            w = self._target_weight(root, t)
            st.pending[root] = int(np.round(w * st.equity / (abs(px) * mult)))
            gross += abs(pos["lots"]) * abs(px) * mult / st.equity
            self.pos_log.append((ts, root, c, pos["lots"], px))
        dd = st.equity / st.peak - 1
        if dd < -self.cfg["drawdown_alert"]:
            self.alerts.append((ts, "BOOK", "DRAWDOWN", f"{dd:.1%}"))
        if gross > self.cfg["max_leverage"]:
            self.alerts.append((ts, "BOOK", "LEVERAGE", f"{gross:.2f}x"))
        self.equity_log.append((ts, st.equity, pnl, gross, dd))
        st.last_date = ts

    def run(self, start, end) -> pd.DataFrame:
        dates = sorted(set().union(*[set(self.ctx[r]["schedules"][self.rule].index) for r in self.roots]))
        for t in [d for d in dates if pd.Timestamp(start) <= d <= pd.Timestamp(end)]:
            self.step(pd.Timestamp(t))
        return pd.DataFrame(self.equity_log, columns=["as_of_date", "equity", "pnl", "gross_leverage", "drawdown"])

    def persist(self) -> None:
        from ..database import db
        eq = pd.DataFrame(self.equity_log, columns=["as_of_date", "equity", "pnl", "gross_leverage", "drawdown"])
        eq["book"] = self.name
        db.bulk_upsert("paper_equity", eq, ["book", "as_of_date"])
        if self.trades:
            tr = pd.DataFrame(self.trades, columns=["trade_ts", "root", "contract_id", "contracts", "price", "cost", "reason"])
            tr["book"] = self.name
            tr["trade_ts"] = pd.to_datetime(tr["trade_ts"]).dt.tz_localize("UTC") + pd.to_timedelta(tr.groupby("trade_ts").cumcount(), unit="us")
            db.bulk_upsert("paper_trades", tr, ["book", "trade_ts", "root", "contract_id"])
        if self.pos_log:
            pos = pd.DataFrame(self.pos_log, columns=["as_of_date", "root", "contract_id", "contracts", "avg_price"])
            pos["book"] = self.name
            db.bulk_upsert("paper_positions", pos.drop_duplicates(["book", "root", "as_of_date"], keep="last"),
                           ["book", "root", "as_of_date"])
        for a in self.alerts[-200:]:
            db.audit(f"paper:{self.name}", "ALERT", f"{a[2]} {a[1]}", {"date": a[0], "detail": a[3]})

    def save_state(self, path: Path) -> None:
        path.write_text(self.state.to_json())
