import numpy as np
import pandas as pd
import pytest

from commodity import pipeline as P
from commodity.backtests.engine import reconstruct_pnl, simulate_contracts
from commodity.core import calendars as cal
from commodity.core.contracts import contract_calendar, fnd, ltd, parse_contract_id
from commodity.features import engine as feat
from commodity.ingestion import synthetic
from commodity.ingestion.sources import parse_symbol, positional_to_contracts
from commodity.robustness import stats
from commodity.rolls.engine import RULES, adjusted_series, build_schedule, tradable_returns
from commodity.validation import checks


@pytest.fixture(scope="module")
def data():
    return synthetic.generate(start="2006-01-01", end="2013-12-31", roots=("GC", "CL"), mcx=False, seed=3)


@pytest.fixture(scope="module")
def ctx(data):
    return P.build_market(data, ["GC", "CL"])


# ---------------------------------------------------------------- contract calendar
def test_known_expiries():
    assert ltd("CL", 2024, 1) == pd.Timestamp("2023-12-19")      # CLF24
    assert ltd("CL", 2023, 12) == pd.Timestamp("2023-11-20")     # CLZ23
    assert ltd("NG", 2024, 1) == pd.Timestamp("2023-12-27")      # NGF24
    assert fnd("GC", 2024, 2) == pd.Timestamp("2024-01-31")
    assert ltd("GC", 2024, 2) == pd.Timestamp("2024-02-27")
    assert ltd("MCX_CRUDEOIL", 2024, 1) == pd.Timestamp("2024-01-19")


def test_symbols():
    assert parse_symbol("CLF24") == ("CL", "CL2024F")
    assert parse_symbol("GC-2009Z") == ("GC", "GC2009Z")
    assert parse_contract_id("NG2010H") == ("NG", 2010, 3)


def test_eia_positional_mapping():
    idx = cal.business_days("CME", "2023-11-01", "2023-12-29")
    pos = pd.DataFrame({1: 80.0, 2: 81.0}, index=idx)
    out = positional_to_contracts("CL", pos)
    day = out[out.trade_date == pd.Timestamp("2023-11-20")]
    assert set(day.contract_id) == {"CL2023Z", "CL2024F"}   # LTD day: expiring contract is still contract 1
    day2 = out[out.trade_date == pd.Timestamp("2023-11-21")]
    assert set(day2.contract_id) == {"CL2024F", "CL2024G"}


# ---------------------------------------------------------------- roll engine
@pytest.mark.parametrize("rule", RULES)
def test_never_held_in_delivery_window(ctx, rule):
    for root, c in ctx.items():
        r = checks.t7_first_notice(c["ccal"], {rule: c["schedules"][rule]}, root)
        assert r["result"] == "PASS", r


def test_same_contract_returns_and_ratio_reconstruction(ctx):
    for root, c in ctx.items():
        trd = c["tradable"]["ROLL_E"]
        st = c["prices"].pivot_table(index="trade_date", columns="contract_id", values="settle")
        sample = trd.dropna(subset=["held_contract"]).iloc[300:330]
        for t, row in sample.iterrows():
            prev = st.index[st.index.get_loc(t) - 1]
            exp = st.at[t, row.held_contract] / st.at[prev, row.held_contract] - 1
            assert abs(exp - row.gross_return) < 1e-12
        ratio = adjusted_series(c["prices"], c["schedules"]["ROLL_E"], "ratio")
        assert checks.t12_continuous_reconstruction(ratio, trd, root)["result"] == "PASS"


def test_panama_preserves_points(ctx):
    c = ctx["CL"]
    pan = adjusted_series(c["prices"], c["schedules"]["ROLL_E"], "panama")
    trd = c["tradable"]["ROLL_E"]
    d = pan.diff().iloc[1:]
    pc = trd["point_change"].iloc[1:]
    assert np.allclose(d.dropna(), pc.reindex(d.dropna().index), atol=1e-9)


def test_roll_deterministic(ctx):
    c = ctx["GC"]
    h2, e2 = build_schedule(c["prices"], c["ccal"], "GC", "ROLL_B")
    assert h2.equals(c["schedules"]["ROLL_B"])


# ---------------------------------------------------------------- validation detects defects
def test_validation_catches_injected_defects(data):
    px = data["prices"][data["prices"].root == "GC"].reset_index(drop=True)
    bad, info = synthetic.inject_defects(px, np.random.default_rng(1))
    res = {r["test_id"]: r["result"] for r in [checks.t1_completeness(bad, "GC"), checks.t2_date_gaps(bad, "GC"),
                                              checks.t3_settlement(bad, "GC"), checks.t4_volume(bad, "GC"),
                                              checks.t5_open_interest(bad, "GC"), checks.t8_spec(bad, "GC")]}
    assert res == {"T1": "FAIL", "T2": "FAIL", "T3": "FAIL", "T4": "FAIL", "T5": "FAIL", "T8": "FAIL"}
    clean = {r["test_id"]: r["result"] for r in [checks.t1_completeness(px, "GC"), checks.t4_volume(px, "GC"),
                                                checks.t5_open_interest(px, "GC"), checks.t8_spec(px, "GC")]}
    assert set(clean.values()) == {"PASS"}


# ---------------------------------------------------------------- look-ahead
def test_truncation_detects_leak(ctx):
    trd = ctx["GC"]["tradable"]["ROLL_E"]

    def clean(cut):
        r = trd["net_return"] if cut is None else trd["net_return"][:cut]
        return pd.DataFrame({"m": r.rolling(20).mean()})

    def leaky(cut):
        r = trd["net_return"] if cut is None else trd["net_return"][:cut]
        return pd.DataFrame({"m": r.rolling(20).mean().shift(-1)})
    assert feat.truncation_test(clean)["result"] == "PASS"
    assert feat.truncation_test(leaky)["result"] == "FAIL"


def test_feature_pipeline_no_lookahead(ctx, data):
    r = P.lookahead_test(ctx["CL"], "CL", data, n=4)
    assert r["result"] == "PASS", r


def test_cot_usable_after_release(data):
    cot = data["cot"]
    u = feat._usable_date(cot["release_ts"], "CME")
    assert (u > pd.to_datetime(cot["release_ts"]).dt.normalize()).all()
    assert (u.dt.weekday == 0).mean() > 0.9   # Friday release -> Monday session


# ---------------------------------------------------------------- P&L
def test_contract_pnl_reconstruction(ctx):
    c = ctx["CL"]
    trd = c["tradable"]["ROLL_E"]
    f = c["features"]()
    w = (np.sign(f["ret_63"]) * 0.1 / f["vol"]).clip(-1, 1).shift(1).fillna(0)
    eq, tr, pos = simulate_contracts(c["prices"], trd, w, "CL", capital=2_000_000)
    rebuilt = reconstruct_pnl(c["prices"], pos, tr, "CL", 2_000_000)
    assert checks.t13_pnl_reconstruction(eq, rebuilt, "CL")["result"] == "PASS"
    assert (tr.reason == "ROLL").any()


def test_negative_price_handled():
    idx = cal.business_days("CME", "2020-03-02", "2020-04-30")
    cc = contract_calendar("CL", "2020-03-01", "2020-06-30")
    rows = []
    for c in cc.itertuples():
        for i, t in enumerate(idx):
            if t <= c.ltd:
                px = 20.0 if not (c.contract_id == "CL2020K" and t == pd.Timestamp("2020-04-20")) else -37.63
                rows.append(("CL", c.contract_id, t, px, px, px, px, px, 100.0, 1000.0, "TEST"))
    prices = pd.DataFrame(rows, columns=["root", "contract_id", "trade_date", "open", "high", "low", "close", "settle",
                                         "volume", "open_interest", "source_id"])
    held, _ = build_schedule(prices, cc, "CL", "ROLL_E")
    assert "CL2020K" not in held[held.index >= pd.Timestamp("2020-04-14")].values   # rolled out before expiry week
    trd = tradable_returns(prices, held, "CL", "ROLL_E")
    assert np.isfinite(trd["net_return"]).all()


# ---------------------------------------------------------------- statistics
def test_bh_fdr():
    out = stats.bh_fdr({"a": 0.001, "b": 0.01, "c": 0.04, "d": 0.5}, q=0.10)
    assert out == {"a": True, "b": True, "c": True, "d": False}


def test_dsr_penalises_trials():
    r = pd.Series(np.random.default_rng(0).normal(0.0004, 0.01, 2500))
    few = stats.deflated_sharpe(r, 2, 0.05)["dsr"]
    many = stats.deflated_sharpe(r, 500, 0.05)["dsr"]
    assert many < few


def test_permutation_noise_not_significant():
    rng = np.random.default_rng(5)
    r = pd.Series(rng.normal(0, 0.01, 3000))
    h = pd.Series(np.sign(rng.normal(0, 1, 3000))).rolling(20).mean().fillna(0)
    assert stats.permutation_pvalue(h, r, reps=200) > 0.05


def test_erc_equalises_risk():
    from commodity.portfolio.allocation import _erc
    rng = np.random.default_rng(0)
    x = rng.normal(size=(500, 6)) @ rng.normal(size=(6, 6))
    x[:, 5] = -x[:, 0] + rng.normal(size=500) * 0.3          # strongly negatively correlated sleeve
    cov = np.cov(x.T)
    w = _erc(cov)
    rc = w * (cov @ w)
    assert np.allclose(rc / rc.sum(), 1 / 6, atol=1e-6)
