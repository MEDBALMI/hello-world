"""Write the 12 standard reports (Markdown + CSV) from a pipeline result bundle."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import analysis

REPORTS = ["01_DATA_HEALTH_REPORT", "02_CONTRACT_COVERAGE", "03_TERM_STRUCTURE_REPORT", "04_POSITIONING_REPORT",
           "05_SEASONALITY_REPORT", "06_COMMODITY_FEATURE_REPORT", "07_STRATEGY_RESEARCH_REPORT", "08_ROBUSTNESS_REPORT",
           "09_OOS_REPORT", "10_PORTFOLIO_REPORT", "11_MCX_IMPLEMENTATION_REPORT", "12_FINAL_COMMODITY_SYSTEM_REPORT"]


def _banner(R):
    if R["data_class"] == "SYNTHETIC":
        return (f"> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `{R['scenario']}`).** "
                "No number in this report is evidence about real commodity markets. "
                "Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).\n\n")
    return f"> Data class: REAL. Generated {pd.Timestamp.now():%Y-%m-%d %H:%M}.\n\n"


def _f(x, nd=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    if isinstance(x, (int, np.integer)):
        return str(x)
    if isinstance(x, (float, np.floating)):
        return f"{x:.{nd}f}"
    return str(x)


def _md(df: pd.DataFrame, nd=2) -> str:
    if df is None or df.empty:
        return "_(none)_\n"
    cols = list(df.columns)
    out = "| " + " | ".join(map(str, cols)) + " |\n|" + "---|" * len(cols) + "\n"
    for _, r in df.iterrows():
        out += "| " + " | ".join(_f(r[c], nd) for c in cols) + " |\n"
    return out


def write_all(R: dict, outdir: Path) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    tag = R["tag"]
    paths = []
    ctx, recs = R["ctx"], R["records"]
    b = _banner(R)

    def w(name, body):
        p = outdir / f"{name}_{tag}.md"
        p.write_text(f"# {name.replace('_', ' ').title()}\n\n{b}{body}", encoding="utf-8")
        paths.append(p)

    # 01 data health
    v = pd.DataFrame(R["validation"])
    pv = v.pivot_table(index="root", columns="test_id", values="result", aggfunc="first")
    pv = pv[sorted(pv.columns, key=lambda c: int(c[1:]))]
    v.assign(details=v["details"].map(lambda d: json.dumps(d, default=str)[:400])).to_csv(outdir / f"validation_{tag}.csv", index=False)
    counts = v.result.value_counts().to_dict()
    w(REPORTS[0], f"Tests T1–T14 per root (PASS/FAIL/OPEN). Totals: {counts}.\n\n" + _md(pv.reset_index()) +
      "\n**OPEN** items require a second source or point-in-time vintages (T3 cross-source settlement, T14 revised-only macro).\n"
      f"\nMachine-readable: `validation_{tag}.csv` (+ `data_quality` table).\n")

    # 02 coverage
    rows = []
    for root, c in ctx.items():
        p = c["prices"]
        rows.append({"root": root, "contracts": p.contract_id.nunique(), "first": str(p.trade_date.min().date()),
                     "last": str(p.trade_date.max().date()), "rows": len(p), "sources": ",".join(p.source_id.unique()),
                     "rolls/yr (ROLL_E)": len(c["events"]["ROLL_E"]) / (len(c["tradable"]["ROLL_E"]) / 252)})
    w(REPORTS[1], _md(pd.DataFrame(rows)))

    # 03 term structure + roll research
    body, rc_all = "", []
    for root, c in ctx.items():
        ts = analysis.term_structure(c)
        rc = analysis.roll_comparison(c)
        rc.insert(0, "root", root)
        rc_all.append(rc)
        body += (f"## {root}\n- Backwardation share: {_f(ts['pct_backwardation'])}; mean carry {_f(ts['mean_carry'], 3)}; "
                 f"carry autocorr(21d) {_f(ts['carry_autocorr_21d'])}\n- IC carry→fwd 21d: {_f(ts['ic_carry_fwd21']['ic'], 3)} "
                 f"(t {_f(ts['ic_carry_fwd21']['t'])}, n {ts['ic_carry_fwd21']['n']}); IC CM slope: {_f(ts['ic_slope_fwd21']['ic'], 3)}\n"
                 f"- Realised vol in backwardation {_f(ts['vol_backwardation'])} vs contango {_f(ts['vol_contango'])}\n\n")
    rcdf = pd.concat(rc_all)
    rcdf.to_csv(outdir / f"roll_rules_{tag}.csv", index=False)
    w(REPORTS[2], body + "## Roll-rule comparison (per commodity)\n" + _md(rcdf, 3))

    # 04 positioning
    rows = []
    for root, c in ctx.items():
        p = analysis.positioning(c)
        if p:
            rows.append({"root": root, "IC mm_z": p["ic_mm_z"]["ic"], "t": p["ic_mm_z"]["t"], "IC mm_chg_4w": p["ic_mm_chg_4w"]["ic"],
                         "t2": p["ic_mm_chg_4w"]["t"], "share pct>0.9": p["pct_extreme_hi"]})
    hyp = [r for r in recs if r["id"] in ("H15", "H16", "H17")]
    w(REPORTS[3], "COT aligned to release (Friday 15:30 ET → next session); weekly data as-of Tuesday.\n\n" +
      _md(pd.DataFrame(rows), 3) + "\n" + _hyp_table(hyp))

    # 05 seasonality
    body, srows = "", []
    for root, c in ctx.items():
        s = analysis.seasonality(c["tradable"]["ROLL_E"])
        t = s["table"].reset_index()
        t.insert(0, "root", root)
        srows.append(t)
        body += (f"- **{root}**: Kruskal-Wallis p = {_f(s['kruskal_p'], 3)}; months with |t|>2: {s['n_months_t_gt_2']} "
                 f"(≈{s['expected_false_t_gt_2']:.1f} expected by chance)\n")
    pd.concat(srows).to_csv(outdir / f"seasonality_{tag}.csv", index=False)
    w(REPORTS[4], body + "\n" + _hyp_table([r for r in recs if r["id"] in ("H21", "H22")]))

    # 06 features
    frows = []
    for root, c in ctx.items():
        d = analysis.feature_ic(c)
        d.insert(0, "root", root)
        frows.append(d)
    fdf = pd.concat(frows)
    fdf.to_csv(outdir / f"feature_ic_{tag}.csv", index=False)
    cross = analysis.cross_relationships(ctx, R.get("macro"))
    w(REPORTS[5], "Spearman IC vs next-21d tradable return, non-overlapping monthly samples.\n\n" + _md(fdf, 3) +
      "\n## Cross-commodity / macro relationships (monthly)\nContemporaneous ≠ predictive: the lagged column is the tradable one.\n\n" + _md(cross, 3))

    # 07 strategy research
    S = R["summary"]
    w(REPORTS[6], f"**Research breadth:** {S['n_hypotheses_registered']} hypotheses registered, {S['n_hypotheses_tested']} tested, "
      f"{S['n_parameter_combinations']} parameter combinations. White reality-check p (best of all trials) = {_f(S['reality_check_p'], 3)} "
      f"(best: {S['reality_check_best']}).\n\nMachine status counts: {S['machine_status_counts']}\n\n" + _hyp_table(recs, full=True) +
      "\n_Machine status = what the acceptance rules would assign; Status = final label (synthetic data can never produce research status)._\n")
    pd.DataFrame([{k: v for k, v in r.items() if not isinstance(v, (dict, list))} for r in recs]).to_csv(outdir / f"hypotheses_{tag}.csv", index=False)

    # 08 robustness
    rows = []
    for r in recs:
        rb = r.get("robustness")
        if not rb:
            continue
        rows.append({"id": r["id"], "param_share_pos": rb["param_share_positive"], "cost_x2": rb["cost_x2"], "cost_x3": rb["cost_x3"],
                     "lag_2": rb["lag_2"], "lag_3": rb["lag_3"], "missing_5%": rb["missing_5pct"],
                     "roll_rules_min": min(rb["roll_rules"].values()), "roll_rules_max": max(rb["roll_rules"].values()),
                     "sub1": rb["subperiods"][0], "sub2": rb["subperiods"][1], "sub3": rb["subperiods"][2],
                     "boot_lo": r["bootstrap"]["lo"], "boot_hi": r["bootstrap"]["hi"]})
    reg = []
    for r in recs:
        for k, d in (r.get("robustness", {}).get("regimes") or {}).items():
            reg.append({"id": r["id"], "regime": k, "sharpe_true": d["true"], "sharpe_false": d["false"]})
    w(REPORTS[7], "All on TRAIN+VALIDATION (OOS untouched). Sharpe values.\n\n" + _md(pd.DataFrame(rows)) +
      "\n## Regime analysis\n" + _md(pd.DataFrame(reg)))

    # 09 OOS
    rows = [{"id": r["id"], "chosen": json.dumps(r.get("chosen_params")), "train": r.get("train_sharpe"), "validation": r.get("val_sharpe"),
             "walk_forward": r.get("walk_forward_sharpe"), "OOS": r.get("oos_sharpe"),
             "OOS maxDD": (r.get("metrics_oos") or {}).get("max_dd"), "machine_status": r.get("machine_status")} for r in recs if "train_sharpe" in r]
    w(REPORTS[8], f"Splits: {S['splits']}. Parameters chosen on TRAIN only; OOS evaluated once.\n\n" + _md(pd.DataFrame(rows)))

    # 10 portfolio
    P = R["portfolio"]
    prow = [{"method": k, **{m: v["metrics"].get(m) for m in ("cagr", "ann_vol", "sharpe", "sortino", "calmar", "max_dd", "max_sector_risk_share")},
             "sector_risk": json.dumps(v["metrics"].get("sector_risk_share"))} for k, v in P.get("results", {}).items()]
    srow = [{"sizing": k, **{m: v.get(m) for m in ("cagr", "ann_vol", "sharpe", "max_dd", "max_root_vol_share")}} for k, v in R["sizing"].items()]
    w(REPORTS[9], f"Sleeves: {P.get('label')} — {P.get('sleeves')}\n\nAverage sleeve correlation: {_f(P.get('avg_sleeve_corr'))}\n\n"
      "## Allocation methods (10% portfolio vol target)\n" + _md(pd.DataFrame(prow), 3) +
      "\n## Position sizing (H01 reference)\n" + _md(pd.DataFrame(srow), 3))

    # 11 MCX
    M = R["mcx"]
    mrows = [{"root": k, **{kk: vv for kk, vv in v.items() if kk != "decomposition"},
              **{f"dec_{kk}": vv for kk, vv in (v.get("decomposition") or {}).items()}} for k, v in M.get("roots", {}).items()]
    w(REPORTS[10], "MCX returns regressed on same-day and lagged global tradable returns and USDINR (timing: MCX closes after US settlement).\n\n" +
      _md(pd.DataFrame(mrows), 4) + "\n## Strategy transfer (same params, MCX contracts and costs)\n" + _md(pd.DataFrame(M.get("strategies", [])), 3))

    # 12 final
    w(REPORTS[11], R.get("final_text", ""))
    return paths


def _hyp_table(recs, full=False):
    rows = []
    for r in recs:
        row = {"id": r["id"], "family": r.get("family"), "type": r.get("research_type"), "strategy": r.get("strategy"),
               "params": json.dumps(r.get("chosen_params")) if r.get("chosen_params") is not None else "–",
               "train": r.get("train_sharpe"), "val": r.get("val_sharpe"), "WF": r.get("walk_forward_sharpe"), "OOS": r.get("oos_sharpe")}
        if full:
            row.update({"DSR p": r.get("dsr_p"), "perm p": r.get("perm_p"), "FDR": r.get("fdr_pass"),
                        "machine_status": r.get("machine_status"), "status": r.get("status")})
        rows.append(row)
    return _md(pd.DataFrame(rows))


def render_registry(path: Path, records: list[dict] | None = None) -> None:
    """Render the pre-registered hypothesis registry (+ latest statuses) to 15_COMMODITY_HYPOTHESES.md."""
    from ..core.config import hypotheses
    st = {r["id"]: (r.get("machine_status"), r.get("status"), r.get("data_class")) for r in (records or [])}
    out = ["# 15 — Commodity Hypotheses (pre-registered)\n",
           "> Generated from `commodity/config/hypotheses.yaml` (source of truth; edit there, never here).",
           "> Grids are fixed before testing. Status columns show the latest pipeline run and its data class;",
           "> runs on SYNTHETIC data never confer research status.\n"]
    for h in hypotheses():
        ms, s, dc = st.get(h["id"], ("–", h.get("status"), "–"))
        out.append(f"## {h['id']} — {h['family']} (type {h['research_type']}, {h['venue']})\n")
        out.append(f"- **Commodities:** {', '.join(h['roots'])} · **strategy:** `{h.get('strategy')}` · **grid:** `{json.dumps(h.get('grid'))}`")
        for k in ("economic_rationale", "feature", "signal", "entry", "exit", "position_size", "expected_effect",
                  "data_required", "test_period", "oos_period", "failure_condition"):
            out.append(f"- **{k.replace('_', ' ').title()}:** {h.get(k)}")
        out.append(f"- **Status:** registry `{h.get('status')}` · last run [{dc}]: machine `{ms}`, final `{s}`\n")
    path.write_text("\n".join(out), encoding="utf-8")
