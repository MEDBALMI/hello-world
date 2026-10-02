# 17 — Commodity Data Sources & Acquisition (Phase 4)

> Status: **v0.1 (2026-10-02). Desk research only. Nothing purchased, nothing downloaded.** Facts come from web-search excerpts of provider documentation; direct fetches of exchange sites are blocked in this environment.
> Tags: `[V-S]` confirmed from a provider/official-document excerpt · `[V-2]` secondary sources only · `[VERIFY]` unconfirmed (check during a trial) · `[OPEN]` unknown.
> Architecture and requirements → 03 (§3, §5, §8). This file only covers **where the data comes from and how good it is**.

---

## 1. What "historical futures data" can mean (these are not the same thing)

| Level | What you get | Usable for our P&L series (02 §B.5)? |
|---|---|---|
| **L1 Continuous only** | One spliced series per market (front month, back-adjusted or ratio-adjusted), vendor's roll rule | **No.** Contract identity is lost, the roll is unknown or fixed, and settlement/OI are often missing |
| **L2 Active contracts only** | Currently listed contracts, with history only while listed | No for history. Useful for live updates |
| **L3 Individual contracts incl. expired, partial** | Expired contracts, but limited depth (e.g. IBKR: 2 years after expiry) or limited fields | Only for recent-period validation |
| **L4 Complete contract history** | Every listed contract since inception, with OHLC, settle, volume, OI and expiry metadata | **Yes. This is the requirement** |

Every source below is classified by this level. **A source is acceptable as primary only at L4**, and only if it gives the settlement price (or a documented close = settlement), volume and open interest.

## 2. Required fields checklist (from the phase brief)

1 expired contracts · 2 daily OHLC · 3 settlement · 4 volume · 5 open interest · 6 contract symbol · 7 contract month · 8 FND · 9 LTD · 10 multiplier · 11 tick size · 12 trading calendar · 13 spec history.

Fields 1–7 come from price sources. **Fields 8–13 are metadata and usually have to be assembled from separate sources** (§5).

## 3. Source inventory by category

### A. Official exchange

| Source | Markets | Level | Depth | Fields | Access / cost | Licensing | Limitations | Status |
|---|---|---|---|---|---|---|---|---|
| **CME DataMine — End-of-Day** | GC, SI, HG, CL, NG (all CME products) | **L4** | **From 1 Jan 1982 or contract inception** [V-S] | OHLC, settlement, volume, OI (official EOD) [V-S] | Purchase per product [V-S]; price by quote [OPEN] | Exchange licence; internal use. Redistribution restricted | Must subscribe per product; file formats changed over time; no FND/LTD metadata in the price file (from rulebook/calendars) | Benchmark source; cost unknown |
| **CME daily settlement files** (`stl`, after ~18:00 CT, T+1) [V-S] | CME products | L2 (forward only) | From subscription date | Settlement, volume, OI | Via DataMine | As above | Builds history only going forward | For live updates |
| **CME public website settlements** | CME products | L2 | Current/recent days only | Settlement | Free (browser) | Website terms; no bulk/automated use | Not a historical source | Not usable for history |
| **LME historical data — Official & Settlement Prices** | LME Aluminium (all LME metals) | Prompt-based (cash, 3M, Dec forwards from Oct 2011) [V-S] — **not monthly contracts** | **From 2000** [V-S] | Official/settlement prices per prompt; no OHLC/OI in this report | **USD 85 per contract-year for the first 5 reports, USD 55 thereafter** [V-S]; Online Licensing Portal (Excel) | LME licence; restrictive | No pre-2000; volume/OI need other LME reports [OPEN]; prompt structure ≠ CME months | Only official LME route |
| **LME Unofficial Prices** | LME metals | Prompt-based | 2000–2021 [V-S] | Unofficial (closing) prices | USD 72 / 46 per contract-year [V-S] | LME licence | Ends 2021 per document [VERIFY] | Secondary |
| **MCX Bhavcopy** | All MCX contracts | **L4 in principle** (contract-wise daily file incl. expiry) | Date-wise download on mcxindia.com [V-2]. **Earliest date not confirmed** [OPEN-3.6]; MCX started Nov 2003 | Contract-wise OHLC, close, volume, value, OI [V-2]; settlement price field [VERIFY] | Free download, no login [V-2] | MCX website terms; bulk scraping may need data-feed agreement [VERIFY] | Format/symbol changes across platform migrations [VERIFY]; must be scraped day by day; field definitions need checking | **Primary MCX candidate. Must be audited** |
| **MCX Data Feed — historical data (on request)** | MCX | Order book + trade book [V-S] | On request; **minimum one year per request** [V-S]; up to 3 months free *excluding the latest 12 months* [V-S] | Tick-level trade/order data (not EOD bhavcopy) | Charges per MCX Data Feed Products & Charges [OPEN]; datafeed@mcxindia.com | MCX Data Feed Policy v6.8 (May 2024) [V-S]; redistribution needs permission | Heavy, tick-level; EOD must be derived | Fallback for gaps or intraday |
| **MCX "Contract-wise High Low", "Reports on Historical Data"** | MCX | Summary | [OPEN] | Highs/lows per contract | Free (web) | Website terms | Summary only | Useful as cross-check |

### B. Commercial vendors

| Source | Markets | Level | Depth | Fields | Access / cost | Licensing | Limitations | Status |
|---|---|---|---|---|---|---|---|---|
| **Databento GLBX.MDP3** | CME: GC, SI, HG, CL, NG | **L4 from 6 Jun 2010** [V-S] | 2010+ (2010–May 2017 backfilled from CME DataMine legacy FIX/FAST) [V-S] | Trades, books (MBP-10 pre-2017), OHLCV bars, **statistics schema: official settlement, OI, cleared volume** [V-S]; **definitions schema: raw symbol, expiration, contract size, tick** [V-S] | API; usage-based pricing [OPEN] | Vendor licence (internal) | No history before 2010; pre-May-2017 settlement-type normalisation missing [V-S]; timestamps pre-May-2017 are SendingTime only [V-S] | **Strong for 2010+** and metadata; too short alone for ≥ 20-year research |
| **Norgate Data — Futures package** | ~100 markets, 11 exchange groups [V-S]; CME metals and energy included [VERIFY per root]; LME [VERIFY]; MCX not expected [VERIFY] | **L4: all individual contracts incl. expired** [V-S] | Back to ~1980 or market start [V-S] | Daily O, H, L, C, volume, OI [V-S]; close = settlement? [VERIFY]; expiry metadata [VERIFY] | Subscription, Windows updater + Python API [V-S]; price [OPEN] | Personal/internal use | Its continuous series use a fixed roll (day before FND / LTD) [V-S]. **Ignore them and use individual contracts.** Pit/electronic session splice conventions [VERIFY] | Candidate (trial) |
| **CSI Data — Unfair Advantage** | Very broad futures coverage; LME/MCX [VERIFY] | **L4** claimed; history "since the earliest days of trading" [V-S] | Decades (some markets pre-1950) [V-S] | OHLC, volume, OI [V-2]; expiration schedules published [V-S] | Software subscription [OPEN] | Vendor licence | Software is built around continuous series (back-, ratio-, Gann-adjusted, perpetual) [V-S], so **export raw individual contracts explicitly**. Settlement vs close [VERIFY] | Candidate (trial) |
| **Barchart OnDemand (getHistory, getFuturesExpirations)** | CME + others | Individual contracts incl. expired [V-S]; depth [OPEN] | [OPEN] | EOD/minute/tick; **FND and LTD via getFuturesExpirations** [V-S]; OI [VERIFY] | Paid API [OPEN] | Vendor licence | Depth and OI history unverified | Candidate for metadata |
| **LSEG (Refinitiv) / Datastream, Bloomberg** | All incl. LME, MCX | L4 | Deep | Full, incl. expired chains and expiry metadata (historical expiry retrieval discussed on LSEG forums [V-2]) | Institutional, expensive [OPEN] | Restrictive | Cost; export limits | Institutional setup |
| **Indian vendors (e.g. TrueData, Global Datafeeds, Tickstory)** | MCX | [OPEN] | [OPEN] | Tickstory sells MCX historical [V-2] | Paid [OPEN] | Vendor licence | Coverage of expired contracts unknown | Evaluate only if bhavcopy fails |

### C. Broker / API

| Source | Markets | Level | Depth | Fields | Limitations | Status |
|---|---|---|---|---|---|---|
| **Interactive Brokers TWS API** | CME (and others) | **L3**: expired futures available **only up to 2 years after expiry** (`includeExpired`) [V-S] | ~2 years | Bars built from trades (not official settlement) [VERIFY]; historical OI not in bars [VERIFY] | Pacing limits and throttling [V-S] | Live/recent validation only; **not a history source** |
| **Zerodha Kite Connect** | MCX | **L1/L2**: expired contracts **only through `continuous=1`, daily candles** [V-S]; instrument tokens for expired contracts not retrievable [V-S] | Depth [OPEN] | OHLCV (+OI flag) | Continuous series with an unknown roll | Cross-check only; **not acceptable as primary** |
| Other Indian broker APIs (Upstox, Dhan, Fyers, Angel) | MCX | [OPEN] | [OPEN] | [OPEN] | Likely similar to Kite | Not investigated (low priority) |

### D. Free / public

| Source | Level | Notes | Use |
|---|---|---|---|
| **EIA NYMEX futures (contracts 1–4)** | Fixed-position "contract 1–4" series (not contract-identified) | WTI, NG, products; **discontinued after 5 Apr 2024** [V-S] | Free cross-check of curve slope (energy) pre-2024 |
| **EIA spot prices** (WTI Cushing, Henry Hub) | Spot | Ongoing | Spot benchmark |
| Yahoo Finance (`GC=F`, `CL=F`), Stooq, Investing.com | **L1** front-month spliced, unknown roll | No contract identity; OI usually missing; terms restrict scraping | **Reject** for research series |
| Nasdaq Data Link CHRIS | L1 (ratio-adjusted continuous) | Deprecated; known integrity gaps [V-2] | Reject |
| Kaggle and GitHub dumps (e.g. MCX bhavcopy scrapes) | Varies | Unknown provenance, incomplete | Only to cross-check our own bhavcopy scrape |
| World Bank Pink Sheet, IMF | Monthly spot averages | Long history | Macro context only |
| LBMA Gold/Silver Price | Spot fixings | Licensed via IBA; free display has restrictions [VERIFY] | Spot reference (licence check) |
| CFTC COT | Not prices | Free | Positioning (10) |

### E. Academic / research datasets
| Source | Notes | Status |
|---|---|---|
| WRDS-hosted datasets (e.g. Datastream/LSEG futures), university Bloomberg terminals | Individual contracts and expiry chains if licensed by an institution | Available only with an academic affiliation [OPEN] |
| CRB / Pinnacle / similar "research" futures files | Often continuous (e.g. Pinnacle CLC) | Check level before use |
| Published replication data (e.g. Koijen et al. 2018 carry, Moskowitz et al. 2012) | Derived returns, not raw contracts | Use as **benchmark checks** for our own built series, not as source data |

## 4. Source-quality issues to test for

| Issue | Where it bites | Test |
|---|---|---|
| **Survivorship / missing expired contracts** | IBKR (2-year limit), Kite (continuous only), free sites | Count contracts per root per year against the exchange listing rules |
| **Adjusted prices disguised as raw** | Vendor continuous series; CSI default views | Raw contract prices must match official settlements on sample dates |
| **Vendor roll methodology** | Norgate (fixed: day before FND/LTD) [V-S], CSI (multiple), Kite (unknown) | Never ingest vendor continuous series as source data |
| **Settlement vs last trade** | IBKR (trade bars), some vendor "close" fields | Compare against DataMine/Databento statistics settlement on ≥ 50 sample dates per root |
| **Volume quality** | Pit + electronic splices pre-~2015; spreads/blocks/EFRP included or not | Check for jumps at session-migration dates; compare with exchange totals |
| **OI quality** | OI lags by one day at many sources; some vendors shift it | Check the date convention against Databento/DataMine OI |
| **Contract-symbol changes** | MCX symbols across platform changes; vendor root codes (e.g. CL vs QM vs legacy) | Symbol map with validity dates (`ref.symbol_map`) |
| **Spec changes** | MCX lot-size changes, new minis; CME micro/mini contracts are separate roots | Spec-history table from circulars |
| **Licensing** | LME, DataMine, MCX data feed, LBMA | Licence register; internal research only, no redistribution |

## 5. Contract metadata (fields 8–13): where it comes from

| Field | CME (GC, SI, HG, CL, NG) | LME Aluminium | MCX |
|---|---|---|---|
| Contract symbol / month | Price source; Databento definitions [V-S] | Prompt date (cash, 3M, Dec forwards) [V-S] | Bhavcopy symbol + expiry date [V-2] |
| **FND** | Rule from rulebook + holiday calendar; Barchart getFuturesExpirations [V-S]; Norgate [VERIFY] | n/a (prompt-date delivery) | Tender/delivery period from MCX circulars [OPEN-3.7] |
| **LTD / expiry** | Databento definitions (2010+) [V-S]; rulebook reconstruction pre-2010; vendor metadata | Prompt date | Bhavcopy expiry column [V-2] |
| Multiplier, tick | Rulebook chapters (current) [V-S]; historical changes [OPEN] | LME specs (25 t) [V-S] | MCX contract-launch circulars / spec PDFs (versioned, e.g. "…January 2026 contract onwards") [V-S] |
| Trading calendar | CME holiday calendars; open-source calendar libraries as a starting point [VERIFY] | LME calendar | MCX holiday circulars |
| Spec history | Rulebook amendments (CFTC filings) | LME notices | MCX circulars (good: spec PDFs are versioned by contract month) |

**Conclusion:** no single source provides fields 8–13 completely for the full history. Plan for a manually curated metadata layer (`ref.contract`, `ref.contract_spec_version`), validated against observed price data: the last trading date seen in the data must equal the LTD.

## 6. Market-by-market data-source matrix

Rating scale: depth / individual contracts / settlement / OI / metadata / overall.

| Market | Exchange | Best free route | Best paid route | Practical depth (individual, expired) | Settlement | Volume / OI | Metadata | Main limitation | Overall |
|---|---|---|---|---|---|---|---|---|---|
| **Gold (GC)** | COMEX | None at L4 (EIA has no metals) | DataMine EOD (1982+) or Norgate/CSI (~1980+); Databento (2010+) | 40+ years (paid) | Official (DataMine/Databento) | Yes / yes | Rulebook + vendor | Pit/electronic splice; active-month cycle | **Easy (paid)** |
| **Silver (SI)** | COMEX | None at L4 | Same | 40+ years | Official | Yes / yes | Same | Same | **Easy (paid)** |
| **Copper (HG)** | COMEX | None at L4 | Same | Long (contract changed historically; check pre-1988 grade) [VERIFY] | Official | Yes / yes | Same | Contract-grade history | **Easy–medium (paid)** |
| **WTI Crude (CL)** | NYMEX | EIA contracts 1–4 to Apr 2024 (not contract-identified) | Same | Since 1983 | Official | Yes / yes | Same | Negative price 2020 | **Easy (paid); partial free** |
| **Natural Gas (NG)** | NYMEX | EIA contracts 1–4 to Apr 2024 | Same | Since 1990 | Official | Yes / yes | Same | Seasonality in curve | **Easy (paid); partial free** |
| **Aluminium (LME)** | LME | None | LME Official/Settlement Prices (2000+, ~USD 55–85 per contract-year) [V-S]; or Bloomberg/LSEG | 2000+ official; **prompt structure, not monthly contracts** | Official settlement | Separate LME reports [OPEN] | LME specs | Licensing, structure, cost; volume/OI history unclear | **Hard** |
| **MCX Gold** | MCX | Bhavcopy (free) | MCX historical feed; Indian vendors | From bhavcopy start [OPEN] (exchange since 2003) | Field to verify | Yes / yes [V-2] | Bhavcopy expiry + circulars | Scraping, format changes, compulsory delivery and tender rules | **Medium** |
| **MCX Silver** | MCX | Bhavcopy | Same | Same | Same | Same | Same | Contract variants (Silver/Mini/Micro) are separate roots | **Medium** |
| **MCX Crude Oil** | MCX | Bhavcopy | Same | Same (launch year conflicting in sources [OPEN]) | Cash-settled on NYMEX × RBI rate [V-S] | Same | Same | Expiry mismatch with NYMEX; negative Apr 2020 | **Medium** |
| **MCX Natural Gas** | MCX | Bhavcopy | Same | Same (launch ~2006 [V-2]) | Same | Same | Same | Same | **Medium** |
| **MCX Copper** | MCX | Bhavcopy | Same | Same | Same | Same | Same | Lot/spec changes [VERIFY] | **Medium** |
| **MCX Aluminium** | MCX | Bhavcopy | Same | Same | Same | Same | Same | Lot/spec changes, mini variants [VERIFY] | **Medium** |

## 7. DATA ACQUISITION DECISION MATRIX

Scores are 1 (poor) to 5 (excellent) on the research requirement, with **cost** as a separate column. Pending trials: these are *preliminary*.

| Need | Option | Level | Depth | Settle | OI | Metadata | Cost | Licensing risk | Decision |
|---|---|---|---|---|---|---|---|---|---|
| CME 5 roots, ≥ 20 years | CME DataMine EOD | L4 | 5 | 5 (official) | 5 | 2 | **Quote needed** | Low (official) | **Reference standard.** Get a quote |
| | Norgate futures | L4 | 5 | 3–4 [VERIFY] | 4 | 3 [VERIFY] | Low–medium [OPEN] | Low | **Trial**, then validate vs official sample |
| | CSI Data | L4 | 5 | 3–4 [VERIFY] | 4 | 3 | Low–medium [OPEN] | Low | **Trial** (alternative to Norgate) |
| | Databento | L4 (2010+) | 3 | 5 | 5 | 5 | Usage-based [OPEN] | Low | **Use for validation and 2010+ metadata**; not alone |
| | IBKR | L3 | 1 | 2 | 1 | 2 | Free with account | Low | Live updates only |
| | Free (Yahoo etc.) | L1 | — | 1 | 1 | 1 | Free | Medium (ToS) | **Reject** |
| LME Aluminium | LME historical (official) | Prompt | 3 (2000+) | 5 | ? | 4 | ~USD 55–85 per contract-year [V-S] | Medium | **Defer decision** (OPEN-3.4): buy only if Al via LME is kept in scope |
| | Vendor coverage of LME (Norgate/CSI) | ? | ? | ? | ? | ? | ? | ? | **Check during trials** |
| | Bloomberg/LSEG | L4 | 5 | 5 | 5 | 5 | High | High | Institutional only |
| MCX (6 roots) | Bhavcopy scrape | L4 (if complete) | ? [OPEN-3.6] | ? [VERIFY] | 4 | 3 | Free | Low–medium (terms) | **Primary candidate → audit first** |
| | MCX historical data feed | Tick | 4 | derive | derive | 3 | Paid [OPEN] | Low | Fallback |
| | Kite continuous | L1 | ? | 2 | 3 | 1 | Free with account | Low | Cross-check only |
| Contract metadata | Rulebooks/circulars + Databento definitions + Barchart expirations | — | — | — | — | 4 combined | Low | Low | **Curate manually, validate against data** |

### Acceptance tests (any source must pass before it becomes primary)
1. **Coverage audit:** every expected contract per root per year is present (no survivorship gaps).
2. **Settlement match:** ≥ 50 random contract-days per root match the official settlement (DataMine or Databento statistics) within 0 ticks. Tolerance documented if not.
3. **OI convention:** the date alignment of OI matches the official source (T vs T+1 reporting).
4. **Expiry match:** the last date with data equals the LTD for ≥ 95% of contracts. Exceptions explained.
5. **Raw, not adjusted:** prices are verified unadjusted.
6. **Volume continuity:** no unexplained level shifts at pit-to-electronic transition dates.
7. **Licence compatibility:** internal research use permitted; storage in our database permitted.

## 8. Open questions created in this phase
- [OPEN-17.1] Exact price quotes: CME DataMine EOD (5 roots), Norgate, CSI, Databento (EOD statistics for 5 roots, 2010+).
- [OPEN-17.2] Does Norgate/CSI "close" equal the official settlement for CME futures? Does either cover LME aluminium (and in what structure)?
- [OPEN-17.3] MCX bhavcopy: earliest available date, field list by era (settlement present?), symbol/format changes, permitted bulk download.
- [OPEN-17.4] MCX contract launch dates and spec/lot-size history for the 6 roots.
- [OPEN-17.5] LME volume and OI history availability and cost.
- [OPEN-17.6] Historical CME FND/LTD for pre-2010 contracts: vendor metadata vs rulebook reconstruction.
- [OPEN-17.7] Copper contract-grade changes in early COMEX history.
