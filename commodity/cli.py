"""Command-line entry point.  python -m commodity.cli <command> [options]

  init-db                         create/upgrade the PostgreSQL schema (idempotent)
  run      --source synthetic|db  full pipeline: build -> validate -> research -> portfolio -> MCX -> paper -> reports
  ingest-mcx --start --end         download MCX bhavcopy (network) -> DB
  ingest-mcx-folder --folder       parse manually downloaded bhavcopy CSVs -> DB
  ingest-vendor --file --source-id --map symbol=SYM,trade_date=DATE,...   (DataMine/Norgate/CSI exports) -> DB
  ingest-eia --root CL|NG          EIA contracts 1-4 (history to 2024-04-05) -> DB  [DATA-LIMITED]
  ingest-cot --years 2010 2026     CFTC disaggregated COT -> DB
  ingest-fred                      FRED market series (DFII10, DGS10, DTWEXBGS, DTB3) -> DB
  paper    --book reference --source synthetic|db --days 250   replay paper book over recent days
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np
import pandas as pd

from . import pipeline as P
from .core import config
from .core.contracts import contract_calendar, fnd as rule_fnd


def _persist_real(prices: pd.DataFrame, source_id: str, expcal: pd.DataFrame | None = None) -> None:
    """Register contracts (rule calendar, overridden by exchange-published expiries) and load prices."""
    from .database import db
    db.init_schema()
    cals = []
    for root, g in prices.groupby("root"):
        cc = contract_calendar(root, g.trade_date.min(), g.trade_date.max())
        if expcal is not None and not expcal.empty:
            e = expcal[expcal.root == root].set_index("contract_id")["ltd"]
            hit = cc.contract_id.isin(e.index)
            cc.loc[hit, "ltd"] = cc.loc[hit, "contract_id"].map(e)
            cc.loc[hit, "calendar_source"] = "BHAVCOPY"
            cc["delivery_risk_date"] = [min(f, l) if pd.notna(f) else l for f, l in zip(cc["fnd"], cc["ltd"])]
        cals.append(cc[cc.contract_id.isin(g.contract_id.unique())])
    data = {"prices": prices, "contract_calendar": pd.concat(cals), "cot": None, "macro": None, "fx": None,
            "rates": None, "data_class": "REAL"}
    P.persist_inputs(data)
    db.execute("UPDATE source_registry SET acceptance_status='trial' WHERE source_id=%s AND acceptance_status='untested'", (source_id,))


def cmd_run(a) -> dict:
    t0 = time.time()
    s = config.settings()
    data = P.load(a.source, scenario=a.scenario, seed=a.seed)
    tag = f"{data['data_class'].lower()}_{data['scenario'].lower()}"
    P.log(f"loaded {len(data['prices'])} contract-days ({data['data_class']}, {data['scenario']})")
    use_db = a.persist and _db_ok()
    if use_db and a.source != "db":
        from .database import db
        db.init_schema()
        P.persist_inputs(data)
        P.log("inputs persisted to PostgreSQL")
    groots = [r for r in config.configured_roots("GLOBAL") if (data["prices"].root == r).any()]
    ctx = P.build_market(data, groots)
    if use_db:
        P.persist_market(ctx)
    val = P.validate(ctx, data)
    P.log("validation: " + json.dumps(pd.Series([v["result"] for v in val]).value_counts().to_dict()))
    if use_db:
        P.persist_validation(val, f"run_{tag}")
    records, summary, rs = P.research(ctx, data)
    sizing = P.sizing_study(rs)
    port = P.portfolio_study(rs, records)
    mcx = P.mcx_study(data, ctx, rs, records)
    from .paper.engine import PaperBook
    import yaml
    book_cfg = yaml.safe_load((config.CONFIG_DIR / "paper.yaml").read_text())["books"]["reference"]
    book = PaperBook("reference_" + tag, book_cfg, ctx)
    end = max(c["tradable"]["ROLL_E"].index[-1] for c in ctx.values())
    eq = book.run(end - pd.Timedelta(days=365), end)
    paper = {"days": len(eq), "final_equity": float(eq.equity.iloc[-1]) if len(eq) else None,
             "n_trades": len(book.trades), "n_alerts": len(book.alerts),
             "alert_types": pd.Series([x[2] for x in book.alerts]).value_counts().to_dict()}
    if use_db:
        P.persist_research(records, data["data_class"])
        book.persist()
    R = {"tag": tag, "data_class": data["data_class"], "scenario": data["scenario"], "ctx": ctx, "records": records,
         "summary": summary, "validation": val, "sizing": sizing, "portfolio": port, "mcx": mcx, "paper": paper,
         "macro": data.get("macro")}
    R["final_text"] = final_text(R, time.time() - t0)
    from .reports.generate import render_registry, write_all
    paths = write_all(R, config.path("reports"))
    render_registry(config.PKG_DIR.parent / "commodity-research" / "15_COMMODITY_HYPOTHESES.md", records)
    P.log(f"reports written: {len(paths)} -> {config.path('reports')}")
    out = {"tag": tag, "summary": summary, "paper": paper,
           "statuses": {r["id"]: [r.get("machine_status"), r.get("status")] for r in records},
           "validation": pd.Series([v["result"] for v in val]).value_counts().to_dict()}
    (config.path("reports") / f"run_summary_{tag}.json").write_text(json.dumps(out, indent=2, default=str))
    return out


def final_text(R: dict, secs: float) -> str:
    S, recs = R["summary"], R["records"]
    by = {}
    for r in recs:
        by.setdefault(r.get("machine_status"), []).append(r["id"])
    lines = [f"Run tag `{R['tag']}`, runtime {secs / 60:.1f} min.\n",
             f"- Hypotheses registered/tested: {S['n_hypotheses_registered']}/{S['n_hypotheses_tested']}; parameter combinations: {S['n_parameter_combinations']}",
             f"- Reality-check p (best of all trials): {S['reality_check_p']:.3f}",
             f"- Machine statuses: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in by.items()),
             f"- Validation: {pd.Series([v['result'] for v in R['validation']]).value_counts().to_dict()}",
             f"- Paper replay (reference book, 1y): {R['paper']}"]
    if R["data_class"] == "SYNTHETIC":
        exp = ("all hypotheses should be REJECTED or WEAK (no edge exists by construction)" if R["scenario"] == "NULL"
               else "carry-family hypotheses (H11/H12/H13) should be detected; unrelated families should not")
        lines.append(f"\n**Machinery check:** in scenario `{R['scenario']}` {exp}. Compare with the statuses above.")
    return "\n".join(lines) + "\n"


def _db_ok() -> bool:
    from .database import db
    ok = db.available()
    if not ok:
        P.log("PostgreSQL not reachable (COMMODITY_DSN) - running without persistence")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(prog="commodity")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init-db")
    r = sub.add_parser("run")
    r.add_argument("--source", default="synthetic", choices=["synthetic", "db"])
    r.add_argument("--scenario", default="NULL", choices=["NULL", "CARRY"])
    r.add_argument("--seed", type=int, default=7)
    r.add_argument("--persist", action="store_true")
    m = sub.add_parser("ingest-mcx"); m.add_argument("--start", required=True); m.add_argument("--end", required=True)
    mf = sub.add_parser("ingest-mcx-folder"); mf.add_argument("--folder", required=True)
    v = sub.add_parser("ingest-vendor"); v.add_argument("--file", required=True); v.add_argument("--source-id", required=True)
    v.add_argument("--map", required=True, help="our=theirs pairs, e.g. symbol=Symbol,trade_date=Date,settle=Settle,...")
    e = sub.add_parser("ingest-eia"); e.add_argument("--root", required=True, choices=["CL", "NG"])
    c = sub.add_parser("ingest-cot"); c.add_argument("--years", nargs=2, type=int, required=True)
    sub.add_parser("ingest-fred")
    a = ap.parse_args(argv)

    if a.cmd == "init-db":
        from .database import db
        db.init_schema(); print("schema ready")
    elif a.cmd == "run":
        print(json.dumps(cmd_run(a), indent=2, default=str))
    elif a.cmd == "ingest-mcx":
        from .ingestion import sources
        frames, cals = [], []
        for d in pd.bdate_range(a.start, a.end):
            try:
                pxs, ec = sources.parse_mcx_bhavcopy(sources.fetch_mcx_bhavcopy(d))
                frames.append(pxs); cals.append(ec)
            except Exception as ex:   # record and continue; gaps are reported by validation T2
                print(f"{d.date()}: {ex}", file=sys.stderr)
        if frames:
            _persist_real(pd.concat(frames), "MCX_BHAVCOPY", pd.concat(cals))
    elif a.cmd == "ingest-mcx-folder":
        from .ingestion import sources
        pxs, ec = sources.load_mcx_folder(a.folder)
        _persist_real(pxs, "MCX_BHAVCOPY", ec)
    elif a.cmd == "ingest-vendor":
        from .ingestion import sources
        mapping = dict(kv.split("=", 1) for kv in a.map.split(","))
        _persist_real(sources.load_vendor_csv(a.file, mapping, a.source_id), a.source_id)
    elif a.cmd == "ingest-eia":
        from .ingestion import sources
        _persist_real(sources.fetch_eia_positional(a.root), "EIA_FUT")
    elif a.cmd == "ingest-cot":
        from .database import db
        from .ingestion import sources
        cmap = {m["cftc_code"]: r for r, m in config.markets().items() if m.get("cftc_code")}
        cot = sources.fetch_cot(list(range(a.years[0], a.years[1] + 1)), cmap)
        db.bulk_upsert("positioning_data", cot, ["report_type", "root", "as_of_date"])
    elif a.cmd == "ingest-fred":
        from .database import db
        from .ingestion import sources
        mm = sources.fetch_fred(["DFII10", "DGS10", "DTWEXBGS", "DTB3"])
        db.bulk_upsert("macro_data", mm[["series_id", "obs_date", "value", "available_ts", "vintage", "source_id"]],
                       ["series_id", "obs_date", "vintage"])


if __name__ == "__main__":
    main()
