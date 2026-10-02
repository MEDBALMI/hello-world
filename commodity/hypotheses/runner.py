"""Hypothesis engine: pre-registered grid -> TRAIN selection -> VALIDATION -> walk-forward ->
single OOS evaluation -> robustness battery -> multiple-testing controls -> status.

OOS data never influences parameter selection: selection uses TRAIN only (and walk-forward
windows use only data before each window)."""
from __future__ import annotations

import itertools
import json

import numpy as np
import pandas as pd

from ..backtests import metrics
from ..backtests.engine import run_fractional
from ..robustness import stats
from .strategies import MULTI, signal


def grid_points(grid: dict) -> list[dict]:
    if not grid:
        return [{}]
    keys = list(grid)
    pts = [dict(zip(keys, v)) for v in itertools.product(*[grid[k] for k in keys])]
    # drop invalid Donchian combos (exit must be shorter than entry)
    return [p for p in pts if not ("entry" in p and "exit" in p and p["exit"] >= p["entry"])]


def pkey(p: dict) -> str:
    return json.dumps(p, sort_keys=True)


class Research:
    def __init__(self, ctx: dict, cfg: dict, data_class: str, rule: str = "ROLL_E"):
        self.ctx, self.cfg, self.data_class, self.rule = ctx, cfg, data_class, rule
        idx = sorted(set().union(*[set(c["tradable"][rule].index) for c in ctx.values()]))
        idx = pd.DatetimeIndex(idx)
        n = len(idx)
        self.start, self.end = idx[0], idx[-1]
        self.train_end = idx[int(n * cfg["train_frac"])]
        self.val_end = idx[int(n * (cfg["train_frac"] + cfg["validation_frac"]))]
        self.cache: dict = {}
        self.trials: list = []          # (hyp_id, pkey, trainval sharpe, trainval returns)
        self.hyps: dict = {}

    # ------------------------------------------------------------------ core evaluation
    def roots_for(self, hyp):
        return [r for r in hyp["roots"] if r in self.ctx]

    def run(self, hyp, params, rule=None, cost_mult=1.0, lag=None, drop_frac=0.0, sizing="vol"):
        rule = rule or self.rule
        key = (hyp["id"], pkey(params), rule, cost_mult, lag, drop_frac, sizing)
        if key in self.cache:
            return self.cache[key]
        lag = self.cfg["exec_lag"] if lag is None else lag
        roots = self.roots_for(hyp)
        feats = {r: self.ctx[r]["features"](rule) for r in roots}
        if hyp.get("multi"):
            sigs = MULTI[hyp["strategy"]](feats, **params)
        else:
            sigs = {r: signal(hyp["strategy"], feats[r], params) for r in roots}
        per_root = {}
        rng = np.random.default_rng(1)
        for r in roots:
            s = sigs.get(r)
            if s is None or s.dropna().empty:
                continue
            trd = self.ctx[r]["tradable"][rule]
            if drop_frac:
                trd = trd.copy()
                kill = rng.random(len(trd)) < drop_frac
                trd.loc[kill, "gross_return"] = 0.0
            vol = feats[r]["vol"]
            if sizing == "equal_notional":
                vol = pd.Series(self.cfg["target_vol"], index=vol.index)
            elif sizing == "atr":
                vol = feats[r]["atr_pct"] * np.sqrt(252)
            per_root[r] = run_fractional(trd, s, vol, r, target_vol=self.cfg["target_vol"],
                                         max_weight=self.cfg["max_weight"], exec_lag=lag, cost_mult=cost_mult)
        if not per_root:   # e.g. feature not computable on this venue (short MCX curves) -> DATA-LIMITED
            self.cache[key] = (pd.Series(dtype=float, index=pd.DatetimeIndex([])), {})
            return self.cache[key]
        rets = pd.DataFrame({r: v["ret"] for r, v in per_root.items()})
        port = rets.mean(axis=1, skipna=True)      # equal risk budget across roots (each vol-targeted)
        self.cache[key] = (port, per_root)
        return self.cache[key]

    def split(self, s: pd.Series, part: str) -> pd.Series:
        if part == "TRAIN":
            return s[s.index < self.train_end]
        if part == "VALIDATION":
            return s[(s.index >= self.train_end) & (s.index < self.val_end)]
        if part == "TRAINVAL":
            return s[s.index < self.val_end]
        if part == "OOS":
            return s[s.index >= self.val_end]
        return s

    def sharpe(self, hyp, params, part, **kw):
        return stats.sharpe(self.split(self.run(hyp, params, **kw)[0], part))

    # ------------------------------------------------------------------ walk-forward
    def walk_forward(self, hyp, points):
        wf = self.cfg["walk_forward"]
        port0 = self.run(hyp, points[0])[0]
        if port0.empty:
            return pd.Series(dtype=float), []
        first = port0.index[0] + pd.DateOffset(years=wf["min_train_years"])
        bounds = list(pd.date_range(first, self.val_end, freq=pd.DateOffset(years=wf["step_years"])))
        if not bounds or bounds[-1] < self.val_end:
            bounds.append(self.val_end)
        pieces, chosen = [], []
        for a, b in zip(bounds[:-1], bounds[1:]):
            best = max(points, key=lambda p: np.nan_to_num(stats.sharpe(self.run(hyp, p)[0][lambda s: s.index < a]), nan=-9))
            seg = self.run(hyp, best)[0]
            pieces.append(seg[(seg.index >= a) & (seg.index < b)])
            chosen.append((str(a.date()), best))
        return (pd.concat(pieces) if pieces else pd.Series(dtype=float)), chosen

    # ------------------------------------------------------------------ full evaluation
    def evaluate(self, hyp) -> dict:
        rec = {k: hyp.get(k) for k in ("id", "family", "research_type", "venue", "strategy", "roots",
                                       "economic_rationale", "failure_condition")}
        rec["data_class"] = self.data_class
        if not hyp.get("strategy") or hyp.get("status") in ("DATA-LIMITED", "DESIGN-LIMITED"):
            rec["status"] = hyp.get("status", "DATA-LIMITED")
            return rec
        roots = self.roots_for(hyp)
        if not roots:
            rec["status"] = "DATA-LIMITED"
            return rec
        points = grid_points(hyp.get("grid") or {})
        train_s = {pkey(p): self.sharpe(hyp, p, "TRAIN") for p in points}
        for p in points:
            tv = self.sharpe(hyp, p, "TRAINVAL")
            self.trials.append((hyp["id"], pkey(p), tv, self.split(self.run(hyp, p)[0], "TRAINVAL")))
        if all(np.isnan(v) for v in train_s.values()):
            rec["status"] = "DATA-LIMITED"
            return rec
        best = max(points, key=lambda p: np.nan_to_num(train_s[pkey(p)], nan=-9))
        port, per_root = self.run(hyp, best)
        held = pd.DataFrame({r: v["held"] for r, v in per_root.items()})
        gross = pd.DataFrame({r: v["gross_lev"] for r, v in per_root.items()}).mean(axis=1)
        rec.update({
            "n_params": len(points), "chosen_params": best, "train_sharpe": train_s[pkey(best)],
            "val_sharpe": self.sharpe(hyp, best, "VALIDATION"),
            "trainval_sharpe": self.sharpe(hyp, best, "TRAINVAL"),
            "oos_sharpe": self.sharpe(hyp, best, "OOS"),
            "years": len(port) / 252,
            "metrics_full": metrics.compute(port, held.mean(axis=1), gross),
            "metrics_oos": metrics.compute(self.split(port, "OOS")),
            "per_root_trainval": {r: stats.sharpe(self.split(v["ret"], "TRAINVAL")) for r, v in per_root.items()},
            "per_root_oos": {r: stats.sharpe(self.split(v["ret"], "OOS")) for r, v in per_root.items()},
        })
        wf, chosen = self.walk_forward(hyp, points)
        rec["walk_forward_sharpe"] = stats.sharpe(wf)
        rec["walk_forward_choices"] = chosen
        # ---------------- robustness (TRAIN+VALIDATION only; OOS stays untouched)
        tv = lambda **kw: self.sharpe(hyp, best, "TRAINVAL", **kw)
        rob = {
            "param_share_positive": float(np.mean([self.sharpe(hyp, p, "TRAINVAL") > 0 for p in points])),
            "cost_x2": tv(cost_mult=2.0), "cost_x3": tv(cost_mult=3.0),
            "lag_2": tv(lag=2), "lag_3": tv(lag=3), "missing_5pct": tv(drop_frac=0.05),
            "roll_rules": {r: tv(rule=r) for r in self.ctx[roots[0]]["tradable"]},
        }
        tvs = self.split(port, "TRAINVAL")
        thirds = np.array_split(tvs, 3)
        rob["subperiods"] = [stats.sharpe(x) for x in thirds]
        rob["regimes"] = self.regimes(hyp, best, per_root)
        rec["robustness"] = rob
        rec["bootstrap"] = stats.block_bootstrap_sharpe(tvs, self.cfg["bootstrap_reps"], self.cfg["block_len"])
        rec["perm_p"] = self.permutation(per_root)
        return rec

    def permutation(self, per_root, reps=200):
        rets = {r: self.split(v["pnl"], "TRAINVAL") for r, v in per_root.items()}
        held = {r: v["held"].reindex(rets[r].index).fillna(0) for r, v in per_root.items()}
        trd_r = {r: self.split(self.ctx[r]["tradable"][self.rule]["gross_return"], "TRAINVAL") for r in per_root}
        def pooled(shift):
            parts = [pd.Series(np.roll(held[r].values, shift), index=held[r].index).shift(1).fillna(0) * trd_r[r].reindex(held[r].index).fillna(0) for r in per_root]
            return stats.sharpe(pd.concat(parts, axis=1).mean(axis=1))
        n = min(len(h) for h in held.values()) if held else 0
        if n < 600:
            return np.nan
        actual = pooled(0)
        rng = np.random.default_rng(0)
        sims = [pooled(int(s)) for s in rng.integers(252, n - 252, reps)]
        return float((np.sum(np.array(sims) >= actual) + 1) / (reps + 1))

    def regimes(self, hyp, params, per_root):
        out = {}
        for r, v in per_root.items():
            f = self.ctx[r]["features"](self.rule)
            ret = self.split(v["ret"], "TRAINVAL")
            fx = f.reindex(ret.index)
            labels = {
                "vol_high": fx["vol"] > fx["vol"].rolling(756, min_periods=252).median(),
                "backwardation": fx["carry"] > 0,
                "uptrend": fx["dist_ma_200"] > 0,
            }
            if "DFII10_chg_63" in fx:
                labels["real_yield_rising"] = fx["DFII10_chg_63"] > 0
            if "DTWEXBGS_chg_63" in fx:
                labels["usd_rising"] = fx["DTWEXBGS_chg_63"] > 0
            for name, lab in labels.items():
                lab = lab.fillna(False)
                out.setdefault(name, {"true": [], "false": []})
                out[name]["true"].append(stats.sharpe(ret[lab]))
                out[name]["false"].append(stats.sharpe(ret[~lab]))
        return {k: {kk: float(np.nanmean(vv)) if len(vv) else np.nan for kk, vv in d.items()} for k, d in out.items()}


def assign_status(rec: dict, acc: dict) -> str:
    if rec.get("status") in ("DATA-LIMITED", "DESIGN-LIMITED"):
        return rec["status"]
    oos, tv = rec.get("oos_sharpe"), rec.get("trainval_sharpe")
    if oos is None or np.isnan(oos) or tv is None or np.isnan(tv):
        return "DATA-LIMITED"
    rob = rec["robustness"]
    sig = (rec.get("dsr_p", 1) <= acc["max_dsr_pvalue"]) and rec.get("fdr_pass", False)
    pos_sub = sum(1 for x in rob["subperiods"] if x > 0)
    rolls_pos = np.mean([v > 0 for v in rob["roll_rules"].values()])
    stable = rob["param_share_positive"] >= acc["min_param_stability"] and pos_sub >= 2 and rolls_pos >= 0.67
    cost_ok = rob["cost_x2"] > acc["min_cost_stress_sharpe"] and rob["lag_2"] > 0
    if oos <= 0 or tv <= 0:
        return "REJECTED"
    if not sig:
        return "WEAK"
    if oos >= acc["min_oos_sharpe"] and stable and cost_ok and rec["years"] >= acc["min_years"]:
        return "ROBUST"
    if oos >= acc["min_oos_sharpe"]:
        return "PROMISING"
    return "WEAK"


def finalize(research: Research, records: list[dict], cfg: dict, acc: dict) -> dict:
    """Multiple-testing layer across ALL trials, then statuses."""
    tv_sharpes = np.array([t[2] for t in research.trials if not np.isnan(t[2])])
    n_trials = len(research.trials)
    var = float(np.var(tv_sharpes)) if len(tv_sharpes) > 1 else 0.0
    tested = [r for r in records if "trainval_sharpe" in r]
    for r in tested:
        port = research.run(research.hyps[r["id"]], r["chosen_params"])[0]
        d = stats.deflated_sharpe(research.split(port, "TRAINVAL"), n_trials, var)
        r["dsr"], r["dsr_p"], r["sr0_ann"] = d["dsr"], d["p"], d["sr0_ann"]
    fdr = stats.bh_fdr({r["id"]: r.get("perm_p", np.nan) for r in tested}, cfg["fdr_q"])
    for r in tested:
        r["fdr_pass"] = bool(fdr.get(r["id"], False))
    mat = pd.DataFrame({f"{t[0]}|{t[1]}": t[3] for t in research.trials}).fillna(0)
    rc = stats.reality_check(mat, reps=cfg["bootstrap_reps"], block=cfg["block_len"])
    for r in records:
        r["machine_status"] = assign_status(r, acc)
        # Synthetic data can validate the machinery but is never research evidence.
        r["status"] = r["machine_status"] if research.data_class == "REAL" else "NOT-RESEARCH (SYNTHETIC)"
    summary = {
        "n_hypotheses_registered": len(records), "n_hypotheses_tested": len(tested),
        "n_parameter_combinations": n_trials, "trial_sharpe_variance": var,
        "reality_check_p": rc["p"], "reality_check_best": rc["best"],
        "machine_status_counts": pd.Series([r["machine_status"] for r in records]).value_counts().to_dict(),
        "splits": {"start": str(research.start.date()), "train_end": str(research.train_end.date()),
                   "val_end": str(research.val_end.date()), "end": str(research.end.date())},
    }
    return summary

