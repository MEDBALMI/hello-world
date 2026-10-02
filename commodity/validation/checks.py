"""Automated data/engine validation T1-T14. Each test returns PASS / FAIL / OPEN with details.
OPEN = cannot be decided with the data available (e.g. no second source for cross-checks)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.config import market
from ..core.contracts import contract_calendar, spec_frame


def _res(test_id, root, result, n_checked=0, n_failed=0, **details):
    return {"test_id": test_id, "root": root, "result": result, "n_checked": int(n_checked),
            "n_failed": int(n_failed), "details": details}


def t1_completeness(px, root):
    m = market(root)
    first, last = px.trade_date.min(), px.trade_date.max()
    exp = contract_calendar(root, first, last)
    exp = exp[(exp.ltd > first + pd.Timedelta(days=400)) & (exp.ltd < last)]
    have = set(px.contract_id.unique())
    missing = sorted(set(exp.contract_id) - have)
    return _res("T1", root, "PASS" if not missing else "FAIL", len(exp), len(missing), missing=missing[:20])


def t2_date_gaps(px, root):
    calname = market(root)["calendar"]
    bds = cal.business_days(calname)
    gaps, checked = [], 0
    for c, g in px.groupby("contract_id"):
        d = pd.DatetimeIndex(g.trade_date.sort_values())
        expected = bds[(bds >= d[0]) & (bds <= d[-1])]
        miss = expected.difference(d)
        checked += len(expected)
        if len(miss):
            gaps.append((c, len(miss), str(miss[0].date())))
    extra = pd.DatetimeIndex(px.trade_date.unique()).difference(bds)
    n_fail = sum(g[1] for g in gaps)
    res = "PASS" if n_fail == 0 and len(extra) == 0 else "FAIL"
    return _res("T2", root, res, checked, n_fail, contracts_with_gaps=gaps[:10],
                rows_on_non_business_days=len(extra), note="calendar is rule-based approximation")


def t3_settlement(px, root, sources=None, max_abs_logret=0.4, near_zero_ticks=20):
    m = market(root)
    allow_neg = m.get("allows_negative", False)
    known = {pd.Timestamp(d) for d in m.get("known_events", [])}
    g = px.dropna(subset=["settle"]).sort_values(["contract_id", "trade_date"])
    has_range = g.high.notna() & g.low.notna() & (g.volume.fillna(0) > 0)
    out_rng = g[has_range & ((g.settle > g.high + 1e-9) | (g.settle < g.low - 1e-9))]
    neg = g[(g.settle <= 0)] if not allow_neg else g.iloc[0:0]
    # abnormal observations (03 s.5.9 V3): extreme same-contract moves and near-zero prices
    tick = spec_frame(root, pd.DatetimeIndex(g.trade_date))["tick"].values
    near_zero = g[(g.settle.abs().values < near_zero_ticks * tick) & ~g.trade_date.isin(known).values]
    prev = g.groupby("contract_id").settle.shift(1)
    lr = np.log(g.settle.where(g.settle > 0) / prev.where(prev > 0))
    extreme = g[(lr.abs() > max_abs_logret) & ~g.trade_date.isin(known)]
    n_fail = len(out_rng) + len(neg) + len(near_zero) + len(extreme)
    cross = "OPEN: single source - official settlement cross-check pending (17 s.7 test 2)" if not sources else "checked"
    res = "FAIL" if n_fail else ("OPEN" if not sources else "PASS")
    return _res("T3", root, res, len(g), n_fail, settle_outside_range=len(out_rng), non_positive=len(neg),
                near_zero=len(near_zero), extreme_moves=len(extreme),
                extreme_examples=[(r.contract_id, str(r.trade_date.date())) for r in extreme.head(5).itertuples()],
                cross_source=cross, note="extreme/near-zero rows are flagged for review, never deleted")


def t4_volume(px, root):
    v = px.volume
    neg = int((v < 0).sum())
    nonint = int(((v.dropna() % 1) != 0).sum())
    missing = int(v.isna().sum())
    res = "FAIL" if neg or nonint else ("OPEN" if missing == len(v) else "PASS")
    return _res("T4", root, res, len(v), neg + nonint, negative=neg, non_integer=nonint, missing=missing)


def t5_open_interest(px, root):
    g = px.sort_values(["contract_id", "trade_date"])
    neg = int((g.open_interest < 0).sum())
    d_oi = g.groupby("contract_id").open_interest.diff().abs()
    inconsistent = int((d_oi > g.volume + 1e-9).sum())     # OI cannot change by more than volume traded
    allna = g.open_interest.isna().all()
    res = "OPEN" if allna else ("FAIL" if neg or inconsistent else "PASS")
    return _res("T5", root, res, len(g), neg + inconsistent, negative=neg, change_exceeds_volume=inconsistent)


def t6_expiry(px, ccal, root):
    last = px.groupby("contract_id").trade_date.max()
    cc = ccal[ccal.root == root].set_index("contract_id")
    expired = cc[cc.ltd < px.trade_date.max()]
    mism = []
    for c, r in expired.iterrows():
        if c in last.index and last[c] != r.ltd:
            mism.append((c, str(last[c].date()), str(r.ltd.date())))
    return _res("T6", root, "PASS" if not mism else "FAIL", len(expired), len(mism), mismatches=mism[:10])


def t7_first_notice(ccal, schedules, root):
    cc = ccal[ccal.root == root]
    bad_order = cc[cc.fnd.notna() & (cc.fnd > cc.ltd)]
    m = market(root)
    held_viol = []
    risk = cc.set_index("contract_id").delivery_risk_date
    for rule, held in schedules.items():
        for t, c in held.dropna().items():
            if c in risk.index and t > cal.bd_offset(m["calendar"], risk[c], -m["roll"]["buffer_bd"]):
                held_viol.append((rule, str(t.date()), c))
    n = len(bad_order) + len(held_viol)
    return _res("T7", root, "PASS" if n == 0 else "FAIL", len(cc), n, fnd_after_ltd=len(bad_order),
                held_inside_delivery_window=held_viol[:10])


def t8_spec(px, root):
    sp = spec_frame(root, pd.DatetimeIndex(px.trade_date))
    q = px.settle.values / sp["tick"].values
    off = np.abs(q - np.round(q)) > 1e-6
    off &= ~np.isnan(q)
    return _res("T8", root, "PASS" if off.sum() == 0 else "FAIL", int((~np.isnan(q)).sum()), int(off.sum()))


def t9_unadjusted(px, root):
    allow_neg = market(root).get("allows_negative", False)
    sp = spec_frame(root, pd.DatetimeIndex(px.trade_date))
    q = px.settle.values / sp["tick"].values
    on_tick = float(np.mean(np.abs(q - np.round(q)) < 1e-6)) if len(q) else 0.0
    neg = int((px.settle <= 0).sum()) if not allow_neg else 0
    res = "PASS" if on_tick > 0.999 and neg == 0 else "FAIL"
    return _res("T9", root, res, len(px), int(neg), on_tick_share=on_tick,
                note="adjusted series are rarely on the tick grid; cross-vendor raw comparison pending")


def t10_reconstructable(px, ccal, root):
    cc = ccal[ccal.root == root].set_index("contract_id")
    data_c = set(px.contract_id.unique())
    no_meta = sorted(data_c - set(cc.index))
    g = px.groupby("contract_id").trade_date.agg(["min", "max"])
    outside = [c for c, r in g.iterrows() if c in cc.index and r["max"] > cc.at[c, "ltd"]]
    n = len(no_meta) + len(outside)
    return _res("T10", root, "PASS" if n == 0 else "FAIL", len(data_c), n, without_metadata=no_meta[:10],
                trading_after_ltd=outside[:10])


def t11_roll_reconstructable(px, ccal, root, schedules, events, rebuild):
    fails = []
    st = px.pivot_table(index="trade_date", columns="contract_id", values="settle")
    for rule, held in schedules.items():
        h2, e2 = rebuild(rule)
        if not h2.equals(held) or not e2.reset_index(drop=True).equals(events[rule].reset_index(drop=True)):
            fails.append((rule, "non-deterministic"))
        for ev in events[rule].itertuples():
            if np.isnan(st.at[ev.roll_date, ev.from_contract]) or np.isnan(st.at[ev.roll_date, ev.to_contract]):
                fails.append((rule, str(ev.roll_date.date()), "missing price on roll date"))
    n_ev = sum(len(e) for e in events.values())
    return _res("T11", root, "PASS" if not fails else "FAIL", n_ev, len(fails), failures=fails[:10])


def t12_continuous_reconstruction(ratio_series, trd, root):
    a = ratio_series.pct_change()
    b = trd["gross_return"]
    ix = a.dropna().index.intersection(b.index)[1:]
    diff = (a[ix] - b[ix]).abs()
    bad = diff[(diff > 1e-8) & (trd.loc[ix, "flag"] == "")]
    return _res("T12", root, "PASS" if len(bad) == 0 else "FAIL", len(ix), len(bad),
                max_abs_diff=float(diff.max()) if len(diff) else 0.0)


def t13_pnl_reconstruction(eq_sim, eq_rebuilt, root, tol=1.0):
    ix = eq_sim.index.intersection(eq_rebuilt.index)
    if len(ix) == 0:
        return _res("T13", root, "OPEN", 0, 0, reason="no overlapping dates")
    diff = float(abs(eq_sim[ix[-1]] - eq_rebuilt[ix[-1]]))
    return _res("T13", root, "PASS" if diff <= tol else "FAIL", len(ix), int(diff > tol), final_equity_diff=diff)


def t14_lookahead(trunc_result, cot, macro_df, root):
    issues = []
    if cot is not None and not cot.empty:
        c = cot[cot.root == root]
        early = c[pd.to_datetime(c.release_ts).dt.tz_localize(None) <= pd.to_datetime(c.as_of_date)] if len(c) else c
        if len(early):
            issues.append(f"{len(early)} COT rows released on/before observation date")
    revised_only = []
    if macro_df is not None and "vintage" in macro_df:
        revised_only = sorted(macro_df.loc[macro_df.vintage == "latest", "series_id"].unique())
    res = trunc_result["result"]
    if issues:
        res = "FAIL"
    elif res == "PASS" and revised_only:
        res = "OPEN"
    return _res("T14", root, res, trunc_result.get("n_checked", 0), len(trunc_result.get("failures", [])) + len(issues),
                truncation=trunc_result, timing_issues=issues,
                revised_only_series=revised_only,
                note="market series (yields, FX) are not revised; revisable fundamentals need first-release vintages")
