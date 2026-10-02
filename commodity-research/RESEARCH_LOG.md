# Research Log

Chronological record of what was done, decided, and left open. Newest first.

---

## 2026-10-02 — Session 5: master execution — implementation + engineering validation

**Environment finding:** every market-data host (CME, CFTC, EIA, FRED, MCX, LME, LBMA, Yahoo, Stooq) is blocked from the build container; only PyPI/GitHub are reachable. No real-market results can be produced here. Nothing has been fabricated.

**Implemented (`../commodity/`):**
- Versioned market/spec config and rule-based expiry calendars (verified CLF24, CLZ23, NGF24, GCG24 and MCX crude dates).
- PostgreSQL schema covering the user's table list, with provenance and idempotent COPY upserts.
- Ingestion adapters: MCX bhavcopy, vendor CSV, CFTC, FRED, EIA contracts 1–4 → contract identities.
- Roll engine A–F; tradable returns; Panama and ratio views.
- Curve and feature engines, with availability-aligned COT and macro joins.
- Validation T1–T14.
- 27 pre-registered hypotheses.
- Research runner, robustness, DSR / permutation / FDR / reality check.
- Portfolio construction, MCX study, paper trading, 12 reports, CLI, 25 tests.

**Engineering validation (synthetic, 1995–2025, GC/SI/HG/CL/NG + 6 MCX roots):**
- NULL seeds 7 and 21: 0 hypotheses accepted (see final report).
- CARRY seed 7: H11 detected (DSR p 0.003). Unrelated families rejected.

**Defects found and fixed by the runs:**
1. Convexity drift in the null generator.
2. Near-zero synthetic prices that T3/T9 missed (added the extreme-move / near-zero check, with a known-events whitelist for WTI 2020-04-20).
3. Unstable risk-parity solver (replaced by coordinate descent).
4. NaN in JSON persistence.
5. Circular-shift permutation is invalid for persistent signals (block sign-flip instead).
6. DSR now uses effective trials.

**Requires user approval:** paid per-contract history (DataMine / Norgate / CSI), LME licence, EIA API key (optional), and network access to data hosts.

---

## 2026-10-02 — Session 4: Phase 4 data acquisition & validation (desk research)

**Done**
- Created 17_COMMODITY_DATA_SOURCES.md:
  - Data-level taxonomy L1–L4 (continuous / active / partial expired / complete).
  - Source inventory by category: exchange, vendor, broker, free, academic.
  - Metadata sourcing, quality-issue tests, per-market matrix.
  - **Data acquisition decision matrix** and **7 acceptance tests**.
- 03: added source-level fields (data level, close = settlement flag, OI date convention, acceptance status) and the rule that only L4 + accepted sources populate clean data. §7 summary now points to 17.
- 16 step 5 updated with next actions and gate. SOURCE_REGISTER: 12 data-source entries with verified facts.

**Key findings** (web-search excerpts of provider docs; direct exchange fetches blocked)
- CME DataMine EOD goes back to 1982 (official settlement, volume, OI). Paid per product; price unknown.
- Databento CME history starts June 2010, with statistics (settlement/OI) and definitions (expiration, size). Too short alone.
- Norgate claims all individual contracts incl. expired back to ~1980. Close = settlement is not yet verified.
- IBKR: expired futures only for 2 years after expiry. Zerodha Kite: expired MCX contracts only as a continuous daily series. **Neither is a history source.**
- LME: official/settlement prices only from 2000, priced per contract-year (USD 85/55). Prompt structure, not monthly contracts.
- MCX: bhavcopy is free and contract-wise, with OI, but the earliest date and the field history are unconfirmed. The MCX historical data feed is tick-level, on request, minimum 1 year.
- No single source supplies FND/LTD/spec history for the full period → curated metadata layer is required.

**Nothing purchased, downloaded or tested. Waiting for review.**

---

## 2026-10-02 — Session 3: corrections to Phase 3 / architecture (no new research)

1. **Statistical power:** removed the "SR 0.4 needs ~25 years" claim.
   - Added the reporting standard (03 §8.4): frequency, independence, annualisation, effective n and test method must all be stated.
   - Kept the calculation only as an [ILLUSTRATIVE] example with its assumptions and failure modes. The effective-N illustration in 03 §9 now lists its assumptions too.
   - The ≥ 20-year target is now justified by regime coverage.
2. **Roll rule:** ROLL-A is marked as an initial research assumption (02 §B.6, 03 §5.3). Added a comparison plan for exchange-specific, volume, OI, calendar and carry-optimised families (OPEN-3.8). Roll-rule comparison added to the data-pilot gate.
3. **MCX:** no longer "implementation validation only". Global markets are primary for general effects; MCX is tested independently for implementation, India-specific effects, USDINR, local liquidity, contract structure and costs (03 §11.2).
4. **Research types A/B/C** added (03 §11.1, 00).
   - New support tables (03 §3.6b): point-in-time universe membership, spread definitions and values, panel view, decision calendar.
   - Type C is supported but its testing is deferred.
5. No Gold work, no empirical tests, no web verification.

---

## 2026-10-02 — Session 2: quantitative foundation (Phase 3 complete, data architecture)

**Done**
- 02 Part B rewritten as Phase 3 v1.0:
  - Contract lifecycle with `delivery_risk_date`.
  - Spot / futures / total return definitions.
  - Seven continuous-series methods, each evaluated on six criteria (A–F), with a worked numeric example.
  - **Research price series vs realistic traded P&L series** (rules R1–R4, P1–P9).
  - Default roll policy ROLL-A.
- 03 created (design only):
  - Layered PostgreSQL design (ref/meta/raw/clean/derived/fund/pos/mkt), with tables, keys and relationships.
  - Mapping from the originally proposed table list.
  - Data-handling rules for expiry, FND, rolls, illiquidity, missing data, contract changes, negative prices, limit events, abnormal observations and spec changes.
  - **Timestamp framework**: observation date, release date, release time, first tradable session.
  - Minimum data, split into essential / useful / optional.
  - Universe-sufficiency review.
- 11 created: curve feature definitions TS1–TS12, constant-maturity method CM-1, NG seasonality handling. No empirical work.
- 16 updated: data sourcing decision and a data-validation pilot are now gates before the Gold module.

**Decisions**
- P&L only from same-contract differencing with modelled roll trades. Back-adjusted series are dynamic views, never P&L.
- Stored series: clean contract data, roll schedule, held contract, tradable returns, constant-maturity curve points, features. Dynamic: unadjusted, Panama, ratio, perpetual.
- Point-in-time rule: as-of join on `available_ts`; first-release vintages; unknown release times are treated as next session.
- Universe: adequate for **time-series** research (effective breadth roughly 4–7). Not adequate for cross-sectional strategies as a primary line. **LME data access is the binding constraint for base metals.**

**Corrections**
- Refined the earlier "too few markets" statement (03 §9).
- Fixed the Panama negative-price explanation: it happens with large cumulative roll *gains* (backwardated histories), not with contango.

**No web verification this session** (as instructed). New timing values are tagged [VERIFY] for confirmation at ingestion.

---

## 2026-10-02 — Session 1b: source verification pass

**Done**
- Checked all `[VERIFY]` items in 01/02 against official documents. Direct fetches of cmegroup.com, cftc.gov and mcxindia.com are **blocked by this environment's network policy**, so facts were confirmed via web-search excerpts of official documents (`[V-S]`) or ≥2 secondary sources (`[V-2]`). New tag scheme added to 00.
- Confirmed (V-S): GC/SI/NG/CL contract sizes and ticks (GC, SI, NG), CL & NG termination rules, GC FND/LTD, NG settlement window 14:28–14:30 ET, LME 25 t lots and prompt structure, COT Tuesday→Friday 15:30 ET timing, S&P GSCI roll window, MCX crude/NG final-settlement formula (NYMEX settle × RBI reference rate).

**Corrections / material findings**
- **EIA stopped publishing NYMEX futures prices after 5 Apr 2024.** Removed EIA as an ongoing free fallback for energy curve data (02 §B.8, 16).
- **CFTC request for comment (May 2026) on COT frequency and content** → possible future schema change (OPEN-1.6).
- MCX crude also settled negative in Apr 2020 (−₹2,884/bbl) because it settles on NYMEX → added to negative-price question (OPEN-3.5).
- Nasdaq Data Link CHRIS confirmed deprecated with known integrity issues → excluded.

**Still unchecked:** CL tick ($0.01), MCX crude lot size, CL volume figure, rough volatility ranges (to be measured from data), vendor "perpetual" definitions.

**To reach full `VERIFIED` status:** allow cmegroup.com, cftc.gov, mcxindia.com, eia.gov, lme.com in the environment's network settings, or check manually.

---

## 2026-10-02 — Session 1: program setup, Phases 1–2

**Done**
- Created program structure in `commodity-research/` with master index, evidence-label convention, and three-layer architecture (foundations → commodity modules → implementation).
- Phase 1: 50 foundation concepts, each with simple/technical/example/trader relevance/quant variable/data/pitfalls (01).
- Phase 2: equities-vs-commodities comparison across 20+ dimensions, return-decomposition explanation, initial transferability assessment of equity techniques (02 Part A).
- Phase 3 (partial): continuous-futures construction methods, roll schedules, artefact checklist, preliminary data-source table (02 Part B).
- Initial roadmap (16) and source register.

**Decisions**
- Each concept defined once; other files cross-reference by `file#concept`.
- Backtest P&L to be computed from **return-chained held-contract series**; adjusted series are *views*, never stored as source data. Constant-maturity series for features only. (Provisional — confirm in 03/11.)
- Default roll rule proposal: N business days before FND (physical) / LTD (cash), liquid months only; N per commodity from lagged volume/OI crossover.
- Time-series tests preferred over cross-sectional tests given small universe.

**Caveats**
- No external sources fetched in this session; all citations are `CITED` (from prior knowledge). Contract numbers flagged [VERIFY].
- No data downloaded; no code; no backtests.

**Next session (proposed)**
1. Complete Phase 3 / Phase 14 theory → create 11_COMMODITY_TERM_STRUCTURE.md.
2. Verify CME and MCX contract specs for the core 6 against exchange pages; update [VERIFY] tags.
3. Start data-vendor evaluation (OPEN-3.1) and 03 data-architecture design.
