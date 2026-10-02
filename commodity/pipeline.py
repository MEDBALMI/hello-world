"""End-to-end orchestration. Every stage is rerunnable; DB writes are idempotent upserts.

Stages: ingest -> persist -> build market (metadata, rolls, curves, features) -> validate ->
research (hypotheses, robustness, OOS, multiple testing) -> sizing -> portfolio -> MCX -> reports.
"""
from __future__ import annotations

import datetime as dt
import json
import time
from functools import lru_cache

import numpy as np
import pandas as pd

from .backtests import metrics
from .backtests.engine import cost_fraction, reconstruct_pnl, run_fractional, simulate_contracts
from .core import config
from .core.config import market
from .curves.curve import curve_table
from .features import engine as feat
from .hypotheses import runner
from .portfolio.allocation import build_portfolios
from .robustness import stats
from .rolls.engine import RULES, adjusted_series, build_schedule, tradable_returns
from .validation import checks

DEFAULT_RULE = "ROLL_E"


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# ------------------------------------------------------------------ data loading / persistence
def load(source: str = "synthetic", scenario: str = "NULL", seed: int = 7, **kw) -> dict:
    if source == "synthetic":
        from .ingestion import synthetic
        return synthetic.generate(scenario=scenario, seed=seed, **kw)
    if source == "db":
        return load_db()
    raise ValueError(f"unknown source {source}")


def load_db() -> dict:
    from .database import db
    px = db.read("""SELECT c.root, p.contract_id, p.trade_date, p.open, p.high, p.low, p.close, p.settle,
                           v.volume, v.open_interest, p.source_id
                    FROM daily_contract_prices p JOIN contracts c USING (contract_id)
                    LEFT JOIN daily_contract_volume_oi v USING (contract_id, trade_date)""")
    for c in ("open", "high", "low", "close", "settle", "volume", "open_interest"):
        px[c] = pd.to_numeric(px[c], errors="coerce")
    px["trade_date"] = pd.to_datetime(px["trade_date"])
    cc = db.read("""SELECT c.root, k.contract_id, c.contract_month, k.listing_date, k.fnd, k.ltd,
                           k.delivery_risk_date, k.settlement_type, c.is_liquid_month, k.calendar_source
                    FROM contract_calendar k JOIN contracts c USING (contract_id)""")
    for c in ("contract_month", "listing_date", "fnd", "ltd", "delivery_risk_date"):
        cc[c] = pd.to_datetime(cc[c])
    cot = db.read("SELECT * FROM positioning_data")
    macro = db.read("SELECT series_id, obs_date, value, available_ts, vintage FROM macro_data")
    if not macro.empty:
        macro["obs_date"] = pd.to_datetime(macro["obs_date"])
    if not cot.empty:
        cot["as_of_date"] = pd.to_datetime(cot["as_of_date"])
    srcs = db.read("SELECT source_id, tier FROM source_registry")
    data_class = "SYNTHETIC" if set(px.source_id.unique()) <= {"SYNTHETIC"} else "REAL"
    return {"prices": px, "contract_calendar": cc, "cot": cot, "macro": macro, "fx": pd.DataFrame(),
            "rates": pd.DataFrame(), "data_class": data_class, "scenario": "DB"}


def persist_inputs(data: dict) -> None:
    from .database import db
    now = pd.Timestamp.now(tz="UTC")
    syn = data["data_class"] == "SYNTHETIC"
    db.upsert("source_registry", pd.DataFrame([
        {"source_id": "SYNTHETIC", "name": "Synthetic generator (engineering validation only)", "tier": 9,
         "data_level": "L4", "close_is_settlement": True, "oi_date_convention": "T", "acceptance_status": "synthetic"},
        {"source_id": "CFTC", "name": "CFTC Commitments of Traders", "tier": 1, "data_level": "N/A", "acceptance_status": "untested"},
        {"source_id": "FRED", "name": "FRED (latest vintage)", "tier": 1, "data_level": "N/A", "acceptance_status": "untested"},
        {"source_id": "MCX_BHAVCOPY", "name": "MCX bhavcopy", "tier": 1, "data_level": "L4", "acceptance_status": "untested"},
        {"source_id": "EIA_FUT", "name": "EIA NYMEX contracts 1-4 (to 2024-04-05)", "tier": 1, "data_level": "L3",
         "close_is_settlement": True, "acceptance_status": "untested"},
    ]), ["source_id"])
    rows = []
    for root, m in config.markets().items():
        rows.append({"root": root, "name": m["name"], "venue": m["venue"], "exchange": m["exchange"],
                     "sector": m["sector"], "tier": m["tier"], "currency": m.get("currency"),
                     "settlement_type": m.get("settlement"), "global_root": m.get("global_root"),
                     "status": m.get("status", "ACTIVE")})
    db.upsert("commodities", pd.DataFrame(rows), ["root"])
    specs = []
    for root in config.configured_roots():
        for v in market(root)["spec_versions"]:
            specs.append({"root": root, "valid_from": pd.Timestamp(v["valid_from"]), "multiplier": v["multiplier"],
                          "tick_size": v["tick"], "commission": v["commission"], "source_ref": "config/markets.yaml"})
    db.upsert("contract_specs", pd.DataFrame(specs), ["root", "valid_from"])
    cc = data["contract_calendar"]
    db.bulk_upsert("contracts", cc[["contract_id", "root", "contract_month", "is_liquid_month"]], ["contract_id"])
    db.bulk_upsert("contract_calendar", cc[["contract_id", "listing_date", "fnd", "ltd", "delivery_risk_date",
                                            "settlement_type", "calendar_source"]], ["contract_id"])
    px = data["prices"]
    p = px[["contract_id", "trade_date", "open", "high", "low", "close", "settle", "source_id"]].copy()
    p["download_ts"], p["processed_ts"] = now, now
    p["quality_status"] = "unchecked"
    db.bulk_upsert("daily_contract_prices", p, ["contract_id", "trade_date"])
    v = px[["contract_id", "trade_date", "volume", "open_interest", "source_id"]].copy()
    db.bulk_upsert("daily_contract_volume_oi", v, ["contract_id", "trade_date"])
    if data.get("cot") is not None and not data["cot"].empty:
        c = data["cot"].copy()
        c["source_id"] = "SYNTHETIC" if syn else c.get("source_id", "CFTC")
        cols = [k for k in ("report_type", "root", "as_of_date", "release_ts", "open_interest", "mm_long", "mm_short",
                            "pm_long", "pm_short", "sd_long", "sd_short", "source_id") if k in c]
        db.bulk_upsert("positioning_data", c[cols], ["report_type", "root", "as_of_date"])
    if data.get("macro") is not None and not data["macro"].empty:
        mm = data["macro"].copy()
        mm["source_id"] = "SYNTHETIC" if syn else mm.get("source_id", "FRED")
        mm["vintage"] = mm.get("vintage", "synthetic" if syn else "latest")
        db.bulk_upsert("macro_data", mm[["series_id", "obs_date", "value", "available_ts", "vintage", "source_id"]],
                       ["series_id", "obs_date", "vintage"])
    if data.get("fx") is not None and not data["fx"].empty:
        f = data["fx"].copy()
        f["source_id"] = "SYNTHETIC" if syn else "RBI"
        db.bulk_upsert("fx_data", f[["pair", "fixing", "obs_date", "value", "source_id"]], ["pair", "fixing", "obs_date"])
    if data.get("rates") is not None and not data["rates"].empty:
        r = data["rates"].copy()
        r["source_id"] = "SYNTHETIC" if syn else "FRED"
        db.bulk_upsert("interest_rates", r[["rate_id", "obs_date", "value", "source_id"]], ["rate_id", "obs_date"])
    db.audit("ingest", "INFO", "inputs persisted", {"rows": len(px), "data_class": data["data_class"]})


# ------------------------------------------------------------------ market build
def build_market(data: dict, roots: list[str], rules=RULES) -> dict:
    s = config.settings()["research"]
    ctx = {}
    for root in roots:
        px = data["prices"][data["prices"].root == root]
        if px.empty:
            continue
        cc = data["contract_calendar"][data["contract_calendar"].root == root]
        sched, events, trad = {}, {}, {}
        for rule in rules:
            held, ev = build_schedule(px, cc, root, rule)
            sched[rule], events[rule] = held, ev
            trad[rule] = tradable_returns(px, held, root, rule)
        curve = curve_table(px, cc, root)
        cot, macro = data.get("cot"), data.get("macro")

        def make_features(px=px, trad=trad, curve=curve, cot=cot, macro=macro, root=root):
            @lru_cache(maxsize=None)
            def features(rule=DEFAULT_RULE):
                return feat.build(px, trad[rule], curve, cot, macro, root, s["vol_halflife"])
            return features

        ctx[root] = {"prices": px, "ccal": cc, "schedules": sched, "events": events, "tradable": trad,
                     "curve": curve, "features": make_features()}
        log(f"built {root}: {px.contract_id.nunique()} contracts, {len(trad[DEFAULT_RULE])} days, "
            f"{len(events[DEFAULT_RULE])} rolls ({DEFAULT_RULE})")
    return ctx


def persist_market(ctx: dict) -> None:
    from .database import db
    db.upsert("roll_rules", pd.DataFrame([{"rule_id": r, "family": r, "params": json.dumps(market("GC")["roll"]),
                                           "description": "see rolls/engine.py"} for r in RULES]), ["rule_id"])
    for root, c in ctx.items():
        ev = pd.concat(c["events"].values(), ignore_index=True)
        db.bulk_upsert("roll_events", ev, ["rule_id", "root", "roll_date"])
        trd = pd.concat([t.reset_index() for t in c["tradable"].values()], ignore_index=True)
        trd = trd[trd.held_contract.notna()]
        db.bulk_upsert("tradable_series", trd[["rule_id", "root", "trade_date", "held_contract", "settle_prev", "settle",
                                               "gross_return", "roll_flag", "roll_cost", "net_return", "index_level"]],
                       ["rule_id", "root", "trade_date"])
        cv = c["curve"].reset_index()
        long = cv.melt(id_vars=["trade_date", "root"], value_vars=["F1", "F2", "F3", "CM30", "CM60", "CM90", "CM180", "CM365"],
                       var_name="tenor", value_name="price").dropna(subset=["price"])
        db.bulk_upsert("curve_data", long[["root", "trade_date", "tenor", "price"]], ["root", "trade_date", "tenor"])
        cf = cv.melt(id_vars=["trade_date", "root"], value_vars=["carry", "slope_cm", "curvature_cm", "carry_12m",
                                                                  "front_second_spread"],
                     var_name="feature", value_name="value").dropna(subset=["value"])
        db.bulk_upsert("curve_features", cf[["root", "trade_date", "feature", "value"]], ["root", "trade_date", "feature"])
        series = []
        for name, col in (("FRONT", "F1"), ("SECOND", "F2"), ("THIRD", "F3"), ("CM30", "CM30"), ("CM60", "CM60"),
                          ("CM90", "CM90"), ("CM180", "CM180"), ("CM365", "CM365")):
            x = cv[["trade_date", col]].dropna().rename(columns={col: "value"})
            x["series_type"], x["root"], x["method_version"] = name, root, "v1"
            series.append(x)
        ratio = adjusted_series(c["prices"], c["schedules"][DEFAULT_RULE], "ratio").dropna()
        series.append(pd.DataFrame({"trade_date": ratio.index, "value": ratio.values, "series_type": "RATIO_ADJ_" + DEFAULT_RULE,
                                    "root": root, "method_version": "v1"}))
        db.bulk_upsert("research_series", pd.concat(series)[["series_type", "root", "trade_date", "value", "method_version"]],
                       ["series_type", "root", "trade_date", "method_version"])


# ------------------------------------------------------------------ validation
def validate(ctx: dict, data: dict) -> list[dict]:
    res = []
    for root, c in ctx.items():
        px, cc = c["prices"], c["ccal"]
        res += [checks.t1_completeness(px, root), checks.t2_date_gaps(px, root),
                checks.t3_settlement(px, root), checks.t4_volume(px, root), checks.t5_open_interest(px, root),
                checks.t6_expiry(px, cc, root), checks.t7_first_notice(cc, c["schedules"], root),
                checks.t8_spec(px, root), checks.t9_unadjusted(px, root), checks.t10_reconstructable(px, cc, root)]
        res.append(checks.t11_roll_reconstructable(px, cc, root, c["schedules"], c["events"],
                                                   lambda rule, px=px, cc=cc, root=root: build_schedule(px, cc, root, rule)))
        ratio = adjusted_series(px, c["schedules"][DEFAULT_RULE], "ratio")
        res.append(checks.t12_continuous_reconstruction(ratio, c["tradable"][DEFAULT_RULE], root))
        trd = c["tradable"][DEFAULT_RULE]
        f = c["features"]()
        w = (np.sign(f["ret_252"]) * 0.10 / f["vol"]).clip(-1, 1).shift(1).fillna(0)
        eq, tr, pos = simulate_contracts(px, trd, w, root, capital=5_000_000)
        rebuilt = reconstruct_pnl(px, pos, tr, root, 5_000_000)
        res.append(checks.t13_pnl_reconstruction(eq, rebuilt, root))
        res.append(checks.t14_lookahead(lookahead_test(c, root, data), data.get("cot"), data.get("macro"), root))
    return res


def lookahead_test(c: dict, root: str, data: dict, n: int = 6) -> dict:
    px, cc = c["prices"], c["ccal"]
    s = config.settings()["research"]
    cols = ["ret_252", "dist_ma_200", "vol", "atr_pct", "carry", "carry_z", "season_score", "trend_template", "mm_pct"]

    def fn(cutoff):
        p = px if cutoff is None else px[px.trade_date <= cutoff]
        held, _ = build_schedule(p, cc, root, DEFAULT_RULE)
        trd = tradable_returns(p, held, root, DEFAULT_RULE)
        cv = curve_table(p, cc, root)
        cot = data.get("cot")
        if cot is not None and cutoff is not None and not cot.empty:
            cot = cot[pd.to_datetime(cot.release_ts).dt.tz_localize(None) <= cutoff + pd.Timedelta(days=1)]
        f = feat.build(p, trd, cv, cot, data.get("macro"), root, s["vol_halflife"])
        return f[[x for x in cols if x in f]]
    return feat.truncation_test(fn, n_samples=n)


def persist_validation(results: list[dict], run_id: str) -> None:
    from .database import db
    df = pd.DataFrame(results)
    df["run_id"] = run_id
    df["details"] = df["details"].map(db.dumps)
    db.upsert("data_quality", df[["run_id", "test_id", "root", "result", "n_checked", "n_failed", "details"]],
              ["run_id", "test_id", "root"])


# ------------------------------------------------------------------ research
def research(ctx: dict, data: dict) -> tuple[list[dict], dict, runner.Research]:
    s = config.settings()
    rs = runner.Research(ctx, s["research"], data["data_class"], DEFAULT_RULE)
    hyps = config.hypotheses()
    rs.hyps = {h["id"]: h for h in hyps}
    records = []
    for h in hyps:
        t0 = time.time()
        rec = rs.evaluate(h)
        records.append(rec)
        log(f"{h['id']} {h.get('strategy')}: OOS Sharpe {rec.get('oos_sharpe', np.nan):.2f} "
            f"(train {rec.get('train_sharpe', np.nan):.2f}) [{time.time() - t0:.0f}s]")
    summary = runner.finalize(rs, records, s["research"], s["acceptance"])
    return records, summary, rs


def sizing_study(rs: runner.Research, hyp_id: str = "H01") -> dict:
    hyp = rs.hyps[hyp_id]
    params = runner.grid_points(hyp.get("grid") or {})[-1]
    out = {}
    for sizing in ("equal_notional", "vol", "atr"):
        port, per_root = rs.run(hyp, params, sizing=sizing)
        rets = pd.DataFrame({r: v["ret"] for r, v in per_root.items()})
        conc = (rets.std() / rets.std().sum()).max() if len(rets.columns) else np.nan
        m = metrics.compute(port)
        m["max_root_vol_share"] = float(conc)
        out[sizing] = m
    return out


def portfolio_study(rs: runner.Research, records: list[dict]) -> dict:
    """Sleeves = hypotheses with machine status >= PROMISING (else a fixed reference set, labelled)."""
    good = [r for r in records if r.get("machine_status") in ("PROMISING", "ROBUST", "PRODUCTION-CANDIDATE")]
    label = "surviving hypotheses"
    if not good:
        good = [r for r in records if r["id"] in ("H01", "H11", "H03") and "chosen_params" in r]
        label = "REFERENCE SET (no hypothesis survived) - engineering demonstration only"
    sleeves = {}
    for r in good:
        _, per_root = rs.run(rs.hyps[r["id"]], r["chosen_params"])
        for root, v in per_root.items():
            sleeves[f"{r['id']}|{root}"] = v["ret"]
    if not sleeves:
        return {"label": "none", "results": {}}
    df = pd.DataFrame(sleeves)
    s = config.settings()["research"]
    res = build_portfolios(df, s["portfolio_vol"], s["sector_cap"])
    corr = df.corr()
    return {"label": label, "sleeves": list(df.columns), "results": res,
            "avg_sleeve_corr": float((corr.values.sum() - len(corr)) / max(len(corr) ** 2 - len(corr), 1))}


def mcx_study(data: dict, gctx: dict, rs: runner.Research, records: list[dict]) -> dict:
    mroots = [r for r in config.configured_roots("MCX") if (data["prices"].root == r).any()]
    mctx = build_market(data, mroots, rules=[DEFAULT_RULE])
    fx = data.get("fx")
    fxr = None
    if fx is not None and not fx.empty:
        fxs = fx[fx.pair == "USDINR"].set_index("obs_date")["value"].sort_index()
        fxr = np.log(fxs).diff()
    out = {"roots": {}, "strategies": []}
    for mroot, c in mctx.items():
        trd = c["tradable"][DEFAULT_RULE]
        g = market(mroot).get("global_root")
        info = {"days": len(trd), "rolls_per_year": len(c["events"][DEFAULT_RULE]) / max(len(trd) / 252, 1e-9),
                "roll_cost_per_year": float(trd["roll_cost"].sum() / max(len(trd) / 252, 1e-9)),
                "avg_one_way_cost": float(cost_fraction(trd, mroot).mean())}
        held_vol = c["prices"].set_index(["trade_date", "contract_id"])["volume"].reindex(list(zip(trd.index, trd.held_contract)))
        info["median_held_volume"] = float(np.nanmedian(held_vol.values))
        if g and g in gctx:
            gr = gctx[g]["tradable"][DEFAULT_RULE]["gross_return"]
            info["avg_one_way_cost_global"] = float(cost_fraction(gctx[g]["tradable"][DEFAULT_RULE], g).mean())
            X = pd.DataFrame({"mcx": np.log1p(trd["gross_return"]), "glob_same": np.log1p(gr), "glob_lag1": np.log1p(gr).shift(1)})
            if fxr is not None:
                X["usdinr"] = fxr
            X = X.dropna()
            if len(X) > 250:
                A = np.column_stack([np.ones(len(X))] + [X[k] for k in X.columns if k != "mcx"])
                beta, *_ = np.linalg.lstsq(A, X["mcx"].values, rcond=None)
                fitted = A @ beta
                r2 = 1 - np.var(X["mcx"] - fitted) / np.var(X["mcx"])
                info["decomposition"] = {"r2": float(r2), **{k: float(b) for k, b in zip(["alpha"] + [k for k in X.columns if k != "mcx"], beta)},
                                         "residual_vol_ann": float(np.std(X["mcx"] - fitted) * np.sqrt(252))}
        out["roots"][mroot] = info
    # strategy transfer: same hypothesis + chosen params run on MCX contracts (MCX costs)
    test = [r for r in records if r.get("machine_status") in ("PROMISING", "ROBUST")] or \
           [r for r in records if r["id"] in ("H01", "H11") and "chosen_params" in r]
    mrs = runner.Research(mctx, config.settings()["research"], data["data_class"], DEFAULT_RULE)
    for r in test:
        hyp = dict(rs.hyps[r["id"]])
        if hyp.get("multi"):
            continue
        gmap = {market(m).get("global_root"): m for m in mctx}
        hyp["roots"] = [gmap[x] for x in hyp["roots"] if x in gmap]
        if not hyp["roots"]:
            continue
        port, _ = mrs.run(hyp, r["chosen_params"])
        out["strategies"].append({"id": r["id"], "params": r["chosen_params"], "global_sharpe_full": r["metrics_full"]["sharpe"],
                                  "global_oos": r["oos_sharpe"], "mcx_sharpe_full": stats.sharpe(port),
                                  "mcx_oos": stats.sharpe(mrs.split(port, "OOS")), "mcx_cost_x2_full":
                                  stats.sharpe(mrs.run(hyp, r["chosen_params"], cost_mult=2.0)[0])})
    return out


def persist_research(records: list[dict], data_class: str) -> None:
    from .database import db
    defs, runs, mets = [], [], []
    for r in records:
        defs.append({"hypothesis_id": r["id"], "family": r.get("family") or "", "research_type": r.get("research_type") or "A",
                     "venue": r.get("venue") or "GLOBAL", "definition": db.dumps(r),
                     "status": r.get("status")})
        if "metrics_full" in r:
            run_id = f"{r['id']}_{data_class}_{DEFAULT_RULE}"
            runs.append({"run_id": run_id, "hypothesis_id": r["id"], "data_class": data_class, "roll_rule": DEFAULT_RULE,
                         "params": json.dumps(r["chosen_params"]), "split": "FULL"})
            for k, v in {**r["metrics_full"], "oos_sharpe": r["oos_sharpe"], "val_sharpe": r["val_sharpe"],
                         "train_sharpe": r["train_sharpe"], "dsr_p": r.get("dsr_p"), "perm_p": r.get("perm_p")}.items():
                if isinstance(v, (int, float, np.floating)) and v is not None and not np.isnan(v):
                    mets.append({"run_id": run_id, "metric": k, "value": float(v)})
    db.upsert("strategy_definitions", pd.DataFrame(defs), ["hypothesis_id"])
    db.upsert("backtest_runs", pd.DataFrame(runs), ["run_id"])
    db.upsert("backtest_metrics", pd.DataFrame(mets), ["run_id", "metric"])
