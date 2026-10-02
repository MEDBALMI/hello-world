-- Commodity research database (PostgreSQL >= 13). Idempotent: safe to re-run.
-- Design: commodity-research/03_COMMODITY_DATA_ARCHITECTURE.md. Individual contracts are the
-- source of truth; continuous/tradable series are derived and versioned by roll rule.
-- Provenance on every dataset: source_id, download_ts, source_version, data_ts, processed_ts, quality_status.

CREATE SCHEMA IF NOT EXISTS commodity;
SET search_path TO commodity;

-- ---------------------------------------------------------------- registry / reference
CREATE TABLE IF NOT EXISTS source_registry (
    source_id        text PRIMARY KEY,
    name             text NOT NULL,
    tier             smallint NOT NULL CHECK (tier IN (1,2,3,9)),   -- 1 official, 2 vendor, 3 secondary, 9 synthetic
    data_level       text CHECK (data_level IN ('L1','L2','L3','L4','N/A')),
    close_is_settlement boolean,
    oi_date_convention text,                                        -- 'T' or 'T+1'
    licence_terms    text,
    acceptance_status text NOT NULL DEFAULT 'untested',            -- untested/trial/accepted/rejected/synthetic
    url              text,
    notes            text
);

CREATE TABLE IF NOT EXISTS commodities (
    root             text PRIMARY KEY,
    name             text NOT NULL,
    venue            text NOT NULL CHECK (venue IN ('GLOBAL','MCX')),
    exchange         text NOT NULL,
    sector           text NOT NULL,
    tier             text NOT NULL,
    currency         text,
    settlement_type  text,
    global_root      text,
    status           text NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS contract_specs (
    root             text REFERENCES commodities(root),
    valid_from       date NOT NULL,
    valid_to         date,
    multiplier       numeric NOT NULL,
    tick_size        numeric NOT NULL,
    tick_value       numeric GENERATED ALWAYS AS (multiplier * tick_size) STORED,
    commission       numeric,
    source_ref       text,
    PRIMARY KEY (root, valid_from)
);

CREATE TABLE IF NOT EXISTS contracts (
    contract_id      text PRIMARY KEY,                -- e.g. CL2024F
    root             text NOT NULL REFERENCES commodities(root),
    contract_month   date NOT NULL,
    exchange_symbol  text,
    is_liquid_month  boolean NOT NULL,
    UNIQUE (root, contract_month)
);

CREATE TABLE IF NOT EXISTS contract_calendar (
    contract_id      text PRIMARY KEY REFERENCES contracts(contract_id),
    listing_date     date,
    first_trade_date date,
    fnd              date,
    ltd              date NOT NULL,
    delivery_risk_date date NOT NULL,
    final_settlement_date date,
    settlement_type  text NOT NULL,
    calendar_source  text NOT NULL,                   -- RULE / EXCHANGE / BHAVCOPY / VENDOR
    validated        boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS exchange_calendar (
    calendar         text,
    trade_date       date,
    is_trading_day   boolean NOT NULL,
    settlement_ts    timestamptz,
    source           text NOT NULL DEFAULT 'RULE',
    PRIMARY KEY (calendar, trade_date)
);

-- ---------------------------------------------------------------- raw + clean prices
CREATE TABLE IF NOT EXISTS raw_contract_prices (
    source_id        text NOT NULL REFERENCES source_registry(source_id),
    batch_id         text NOT NULL,
    contract_id      text NOT NULL,
    trade_date       date NOT NULL,
    open numeric, high numeric, low numeric, close numeric, settle numeric,
    volume numeric, open_interest numeric,
    download_ts      timestamptz NOT NULL,
    source_version   text,
    PRIMARY KEY (source_id, batch_id, contract_id, trade_date)
);

CREATE TABLE IF NOT EXISTS daily_contract_prices (
    contract_id      text NOT NULL REFERENCES contracts(contract_id),
    trade_date       date NOT NULL,
    open numeric, high numeric, low numeric, close numeric,
    settle           numeric,
    source_id        text NOT NULL REFERENCES source_registry(source_id),
    download_ts      timestamptz,
    source_version   text,
    data_ts          timestamptz,                     -- when the value became public (settlement time)
    processed_ts     timestamptz NOT NULL DEFAULT now(),
    quality_status   text NOT NULL DEFAULT 'unchecked',
    PRIMARY KEY (contract_id, trade_date)
);
CREATE INDEX IF NOT EXISTS ix_dcp_date ON daily_contract_prices (trade_date);

CREATE TABLE IF NOT EXISTS daily_contract_volume_oi (
    contract_id      text NOT NULL REFERENCES contracts(contract_id),
    trade_date       date NOT NULL,
    volume           numeric,
    open_interest    numeric,
    oi_asof_date     date,
    source_id        text NOT NULL REFERENCES source_registry(source_id),
    data_ts          timestamptz,                     -- OI typically public T+1
    processed_ts     timestamptz NOT NULL DEFAULT now(),
    quality_status   text NOT NULL DEFAULT 'unchecked',
    PRIMARY KEY (contract_id, trade_date)
);

CREATE TABLE IF NOT EXISTS data_quality (
    run_id           text NOT NULL,
    test_id          text NOT NULL,
    root             text NOT NULL,
    result           text NOT NULL CHECK (result IN ('PASS','FAIL','OPEN')),
    n_checked        integer,
    n_failed         integer,
    details          jsonb,
    run_ts           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, test_id, root)
);

-- ---------------------------------------------------------------- rolls / series / curves
CREATE TABLE IF NOT EXISTS roll_rules (
    rule_id          text PRIMARY KEY,                -- ROLL_A..ROLL_F (+ version)
    family           text NOT NULL,
    params           jsonb NOT NULL,
    description      text
);

CREATE TABLE IF NOT EXISTS roll_events (
    rule_id          text REFERENCES roll_rules(rule_id),
    root             text REFERENCES commodities(root),
    roll_date        date NOT NULL,
    from_contract    text NOT NULL,
    to_contract      text NOT NULL,
    reason           text,
    PRIMARY KEY (rule_id, root, roll_date)
);

CREATE TABLE IF NOT EXISTS research_series (
    series_type      text NOT NULL,                   -- FRONT, SECOND, ACTIVE, CM30.., RATIO_ADJ
    root             text NOT NULL REFERENCES commodities(root),
    trade_date       date NOT NULL,
    value            double precision,
    contract_ids     text,
    method_version   text NOT NULL,
    processed_ts     timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (series_type, root, trade_date, method_version)
);

CREATE TABLE IF NOT EXISTS tradable_series (
    rule_id          text NOT NULL,
    root             text NOT NULL REFERENCES commodities(root),
    trade_date       date NOT NULL,
    held_contract    text NOT NULL,
    settle_prev      double precision,
    settle           double precision,
    gross_return     double precision,
    roll_flag        boolean NOT NULL,
    roll_cost        double precision,
    net_return       double precision,
    index_level      double precision,
    processed_ts     timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (rule_id, root, trade_date)
);

CREATE TABLE IF NOT EXISTS curve_data (
    root             text NOT NULL REFERENCES commodities(root),
    trade_date       date NOT NULL,
    tenor            text NOT NULL,                   -- F1, F2, F3, CM30, CM60, ...
    price            double precision,
    contract_lo      text,
    contract_hi      text,
    days_to_expiry   double precision,
    PRIMARY KEY (root, trade_date, tenor)
);

CREATE TABLE IF NOT EXISTS curve_features (
    root             text NOT NULL REFERENCES commodities(root),
    trade_date       date NOT NULL,
    feature          text NOT NULL,
    value            double precision,
    available_ts     timestamptz,
    PRIMARY KEY (root, trade_date, feature)
);

-- ---------------------------------------------------------------- fundamentals / positioning / macro
CREATE TABLE IF NOT EXISTS fundamental_data (
    series_id        text NOT NULL,
    period_end       date NOT NULL,
    vintage_ts       timestamptz NOT NULL,            -- release timestamp (point-in-time)
    value            double precision,
    root             text,
    is_first_release boolean,
    release_ts_quality text,                          -- exact / typical / assumed
    source_id        text REFERENCES source_registry(source_id),
    download_ts      timestamptz,
    PRIMARY KEY (series_id, period_end, vintage_ts)
);

CREATE TABLE IF NOT EXISTS positioning_data (
    report_type      text NOT NULL,                   -- disaggregated / legacy
    root             text NOT NULL,
    as_of_date       date NOT NULL,                   -- Tuesday
    release_ts       timestamptz NOT NULL,            -- Friday 15:30 ET (holiday shifts)
    open_interest    double precision,
    mm_long double precision, mm_short double precision,
    pm_long double precision, pm_short double precision,
    sd_long double precision, sd_short double precision,
    nc_long double precision, nc_short double precision,
    comm_long double precision, comm_short double precision,
    source_id        text REFERENCES source_registry(source_id),
    download_ts      timestamptz,
    PRIMARY KEY (report_type, root, as_of_date)
);

CREATE TABLE IF NOT EXISTS macro_data (
    series_id        text NOT NULL,                   -- e.g. DFII10, DGS10, DTWEXBGS
    obs_date         date NOT NULL,
    value            double precision,
    available_ts     timestamptz NOT NULL,
    vintage          text NOT NULL DEFAULT 'latest',  -- 'latest' => revised_only flag in T14
    source_id        text REFERENCES source_registry(source_id),
    PRIMARY KEY (series_id, obs_date, vintage)
);

CREATE TABLE IF NOT EXISTS fx_data (
    pair             text NOT NULL,                   -- USDINR
    fixing           text NOT NULL,                   -- RBI_REF / FBIL / CLOSE
    obs_date         date NOT NULL,
    value            double precision NOT NULL,
    available_ts     timestamptz,
    source_id        text REFERENCES source_registry(source_id),
    PRIMARY KEY (pair, fixing, obs_date)
);

CREATE TABLE IF NOT EXISTS interest_rates (
    rate_id          text NOT NULL,                   -- USD_3M_TBILL, INR_91D_TBILL
    obs_date         date NOT NULL,
    value            double precision NOT NULL,
    available_ts     timestamptz,
    source_id        text REFERENCES source_registry(source_id),
    PRIMARY KEY (rate_id, obs_date)
);

-- ---------------------------------------------------------------- strategies / backtests
CREATE TABLE IF NOT EXISTS strategy_definitions (
    hypothesis_id    text PRIMARY KEY,
    family           text NOT NULL,
    research_type    char(1) NOT NULL CHECK (research_type IN ('A','B','C')),
    venue            text NOT NULL,
    definition       jsonb NOT NULL,                  -- full pre-registered hypothesis record
    registered_ts    timestamptz NOT NULL DEFAULT now(),
    status           text NOT NULL DEFAULT 'REGISTERED'
);

CREATE TABLE IF NOT EXISTS strategy_signals (
    hypothesis_id    text NOT NULL,
    root             text NOT NULL,
    trade_date       date NOT NULL,
    signal           double precision,
    params           text NOT NULL,
    PRIMARY KEY (hypothesis_id, root, trade_date, params)
);

CREATE TABLE IF NOT EXISTS backtest_runs (
    run_id           text PRIMARY KEY,
    hypothesis_id    text,
    data_class       text NOT NULL CHECK (data_class IN ('REAL','SYNTHETIC')),
    roll_rule        text,
    params           jsonb,
    split            text,                            -- TRAIN / VALIDATION / OOS / WALKFORWARD / FULL
    start_date date, end_date date,
    code_version     text,
    run_ts           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS backtest_trades (
    run_id           text REFERENCES backtest_runs(run_id),
    trade_no         integer,
    root             text,
    contract_id      text,
    trade_date       date,
    side             smallint,
    contracts        double precision,
    price            double precision,
    cost             double precision,
    reason           text,                            -- SIGNAL / ROLL / STOP / TIME_STOP
    PRIMARY KEY (run_id, trade_no)
);

CREATE TABLE IF NOT EXISTS backtest_metrics (
    run_id           text REFERENCES backtest_runs(run_id),
    metric           text,
    value            double precision,
    PRIMARY KEY (run_id, metric)
);

-- ---------------------------------------------------------------- paper trading
CREATE TABLE IF NOT EXISTS paper_positions (
    book             text NOT NULL,
    root             text NOT NULL,
    contract_id      text NOT NULL,
    as_of_date       date NOT NULL,
    contracts        double precision NOT NULL,
    avg_price        double precision,
    PRIMARY KEY (book, root, as_of_date)
);

CREATE TABLE IF NOT EXISTS paper_trades (
    book             text NOT NULL,
    trade_ts         timestamptz NOT NULL,
    root             text NOT NULL,
    contract_id      text NOT NULL,
    contracts        double precision NOT NULL,
    price            double precision NOT NULL,
    cost             double precision NOT NULL,
    reason           text,
    PRIMARY KEY (book, trade_ts, root, contract_id)
);

CREATE TABLE IF NOT EXISTS paper_equity (
    book             text NOT NULL,
    as_of_date       date NOT NULL,
    equity           double precision NOT NULL,
    pnl              double precision,
    gross_leverage   double precision,
    drawdown         double precision,
    PRIMARY KEY (book, as_of_date)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id               bigserial PRIMARY KEY,
    ts               timestamptz NOT NULL DEFAULT now(),
    job              text NOT NULL,
    level            text NOT NULL,
    message          text NOT NULL,
    payload          jsonb
);
