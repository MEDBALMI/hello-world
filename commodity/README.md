# Commodity research & systematic trading framework

Implementation of the program documented in `../commodity-research/` (design: 02, 03, 11, 17).
Individual futures contracts are the source of truth; continuous and tradable series are derived;
research price series and realistic P&L are kept separate; every stage is rerunnable and idempotent.

```
commodity/
  config/        markets.yaml (contract rules, versioned specs, costs) · settings.yaml (splits, risk) ·
                 hypotheses.yaml (pre-registered hypotheses + fixed grids) · paper.yaml (paper books)
  core/          calendars (rule-based, approximate) · contracts (LTD/FND rules, spec versions) · config
  database/      schema.sql (PostgreSQL, provenance on every table) · db.py (idempotent upserts, COPY)
  ingestion/     sources.py (MCX bhavcopy, vendor/DataMine CSV, CFTC COT, FRED, EIA contracts 1-4) ·
                 synthetic.py (ENGINEERING VALIDATION ONLY)
  rolls/         roll engine: ROLL_A calendar, B volume, C OI, D volume+OI, E days-before, F carry-aware;
                 held-contract schedule, same-contract tradable returns, Panama/ratio views
  curves/        F1-F3, constant maturity 30/60/90/180/365d, carry, slope, curvature, 12m seasonal carry
  features/      technical (MA, Donchian, ATR, trend template, VCP proxy), curve, COT (release-aligned),
                 macro (availability-aligned), seasonality (prior years only), truncation look-ahead test
  hypotheses/    strategy library (23 single-root + gold/silver RV + cross-sectional momentum) and the
                 research runner (TRAIN select -> VALIDATION -> walk-forward -> single OOS -> robustness ->
                 DSR / permutation / BH-FDR / reality check -> status)
  backtests/     fractional (research) and integer-contract (realistic) engines, metrics, P&L reconstruction
  robustness/    bootstrap, permutation, deflated Sharpe, FDR, reality check
  portfolio/     equal / equal-vol / risk-parity / correlation-adjusted, sector risk caps, vol targeting
  validation/    T1-T14 automated tests (PASS / FAIL / OPEN, machine-readable)
  paper/         paper-trading engine (simulated fills, rolls, risk alerts, audit log; no broker)
  reports/       analyses + 12 standard reports -> reports/output/
  tests/         pytest suite (21 tests)
```

## Run

```bash
pip install pandas numpy scipy pyyaml "psycopg[binary]" openpyxl pytest
export COMMODITY_DSN="postgresql://user@host/commodity"     # optional; default in config/settings.yaml
python -m commodity.cli init-db                              # create schema (idempotent)
python -m pytest                                             # 21 tests

# Engineering validation on synthetic data (no edge / planted carry edge)
python -m commodity.cli run --source synthetic --scenario NULL  --persist
python -m commodity.cli run --source synthetic --scenario CARRY --persist

# Real data (needs network access to the sources; nothing here is purchased)
python -m commodity.cli ingest-mcx --start 2005-01-01 --end 2026-09-30     # MCX bhavcopy (free)
python -m commodity.cli ingest-mcx-folder --folder data/raw/mcx           # or manually downloaded CSVs
python -m commodity.cli ingest-eia --root CL ; python -m commodity.cli ingest-eia --root NG   # to 2024-04-05
python -m commodity.cli ingest-cot --years 2010 2026
python -m commodity.cli ingest-fred
python -m commodity.cli ingest-vendor --file gc.csv --source-id NORGATE \
       --map symbol=Symbol,trade_date=Date,open=Open,high=High,low=Low,close=Close,settle=Close,volume=Volume,open_interest=OpenInterest
python -m commodity.cli run --source db --persist                         # full research on real data
```

## Rules enforced in code
- Signals at close t trade at close t+1 (`exec_lag`), returns accrue from t+2.
- Positions never held inside `delivery_risk_date - buffer` (test T7).
- Volume/OI used with a 1-day lag in roll decisions; COT usable the session after its Friday release.
- Parameters chosen on TRAIN only; OOS evaluated once; every trial counted for DSR/FDR/reality check.
- Synthetic results can never receive a research status (`NOT-RESEARCH (SYNTHETIC)`).
- No broker connectivity exists anywhere in the code base.
