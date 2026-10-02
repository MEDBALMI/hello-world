# Source Register

Priority: 1 Exchange · 2 Government agency · 3 Regulator · 4 Official statistics · 5 Academic · 6 Institutional research · 7 Reputable financial media.

**Status codes:** `CITED` = referenced from prior knowledge, not yet re-read · `V-S` = specific facts confirmed via web-search excerpt of the official document (direct fetch blocked) · `V-2` = confirmed by ≥2 secondary sources only · `VERIFIED` = full document read · `USED` = data actually pulled.

**Access note (2026-10-02):** this research environment's network policy blocks direct fetches of cmegroup.com, cftc.gov and mcxindia.com. Full `VERIFIED` status requires allowing those domains or a manual check.

## 1. Exchanges
| ID | Source | Use | Status |
|---|---|---|---|
| EX-CME | CME Group — contract specs, rulebook chapters, settlement methodology, margins, delivery notices, warehouse stocks (cmegroup.com) | GC, SI, HG, PL, PA, CL, NG, ALI specs; FND/LTD rules | V-S (items below) |
| EX-CME-200 | NYMEX Rulebook Ch. 200 Light Sweet Crude Oil — https://www.cmegroup.com/rulebook/NYMEX/2/200.pdf | CL size, delivery, termination rule | V-S 2026-10-02 |
| EX-CME-220 | NYMEX Rulebook Ch. 220 Henry Hub Natural Gas — https://www.cmegroup.com/rulebook/NYMEX/2/220.pdf | NG size, tick, termination | V-S 2026-10-02 |
| EX-CME-113 | COMEX Rulebook Ch. 113 Gold — https://www.cmegroup.com/rulebook/COMEX/1a/113.pdf ; gold fact card | GC size, tick, LTD, 995 fineness | V-S 2026-10-02 |
| EX-CME-112 | COMEX Rulebook Ch. 112 Silver — https://www.cmegroup.com/rulebook/COMEX/1a/112.pdf | SI size, tick | V-S 2026-10-02 |
| EX-CME-NGSET | NYMEX Energy Futures Daily Settlement Procedure — https://www.cmegroup.com/trading/energy/files/NYMEX_Energy_Futures_Daily_Settlement_Procedure.pdf | NG 14:28–14:30 ET VWAP | V-S 2026-10-02 |
| EX-CME-GCFAQ | CME Gold FAQ (FND = last business day of prior month) | GC FND | V-S 2026-10-02 |
| EX-CMEDM | CME DataMine (datamine.cmegroup.com) | Paid per-contract history | CITED |
| EX-ICE | ICE Futures Europe — Brent spec, ICE Brent Index (ice.com) | Brent | CITED |
| EX-IBA | ICE Benchmark Administration — LBMA Gold/Silver Price | Spot reference | CITED |
| EX-LME | London Metal Exchange — contract specs (https://www.lme.com/en/metals/non-ferrous/lme-copper/contract-specifications), prompt-date structure, stocks, cancelled warrants, COTR | 25 t lots; prompts daily to 3M, weekly 3–6M, monthly 7–123M | V-S 2026-10-02 (specs) |
| EX-LBMA | LBMA — market structure, vault holdings (lbma.org.uk) | Gold, silver, PGMs | CITED |
| EX-MCX | Multi Commodity Exchange of India — contract specifications, circulars, bhavcopy (mcxindia.com) | MCX contracts | Partial: crude & NG Due Date Rate rule V-S (MCX spec PDFs, e.g. crude-oil-january-2026-contract-onwards.pdf; natural-gas-mini-leaflet.pdf); Gold 1 kg / ₹ per 10 g / ₹1 tick / compulsory delivery / expiry 5th, NG 1,250 MMBtu / ₹0.10 tick, bhavcopy access = V-2 (broker sources); crude lot size VERIFY |
| EX-SPGSCI | S&P GSCI Methodology (S&P Dow Jones Indices, 2026) — https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-gsci.pdf | Roll window 5th–9th business day, 20%/day | V-S 2026-10-02 |
| EX-SHFE | Shanghai Futures Exchange — warehouse stocks | Copper/aluminium inventories | CITED |

## 2–4. Government, regulators, official statistics
| ID | Source | Use | Status |
|---|---|---|---|
| GOV-EIA | US Energy Information Administration — Weekly Petroleum Status Report, Weekly Natural Gas Storage Report, spot prices, STEO (eia.gov) | Crude, products, NG | CITED; **NYMEX futures price series discontinued after 5 Apr 2024** (https://www.eia.gov/dnav/pet/pet_pri_fut_s1_d.htm) — V-S |
| GOV-CFTC | CFTC Commitments of Traders — Legacy, Disaggregated, historical files, explanatory notes (cftc.gov) | Positioning; Tuesday data, Friday 15:30 ET release | V-S 2026-10-02 (timing) |
| GOV-CFTC-RFC | CFTC, *Review of the Commitments of Traders Reporting Program*, request for comment, 91 FR 24207 (5 May 2026), comments closed 4 Jun 2026 — https://www.federalregister.gov/documents/2026/05/05/2026-08743/review-of-the-commitments-of-traders-reporting-program | Possible COT frequency/content changes | V-S 2026-10-02 |
| GOV-FRED | Federal Reserve Bank of St. Louis FRED — T-bills, TIPS real yields, breakevens, USD indices (fred.stlouisfed.org) | Rates/FX/macro | CITED |
| GOV-FED | Federal Reserve Board — H.15 rates, broad dollar index | Rates/FX | CITED |
| GOV-UST | US Treasury — yield curves, real yield curve | Rates | CITED |
| GOV-USGS | US Geological Survey — Mineral Commodity Summaries | Metals supply | CITED |
| REG-SEBI | Securities and Exchange Board of India — commodity derivatives framework, margin rules | MCX | CITED |
| GOV-RBI | Reserve Bank of India — FBIL/RBI reference rate USDINR, T-bill yields | MCX conversion | CITED |
| GOV-IND | India Ministry of Commerce (DGCI&S) — imports/exports; CBIC — import duty notifications | Gold/silver imports, duties | CITED |
| INT-WB | World Bank Commodity Price Data ("Pink Sheet") | Long monthly price history | CITED |
| INT-IMF | IMF Primary Commodity Prices | Long monthly history | CITED |
| INT-BIS | BIS — research on commodity financialisation, USD | Context | CITED |

## 6. Industry bodies (institutional)
| ID | Source | Use | Status |
|---|---|---|---|
| IND-WGC | World Gold Council — Gold Demand Trends, ETF flows, central-bank holdings | Gold | CITED |
| IND-SI | The Silver Institute — World Silver Survey | Silver | CITED |
| IND-ICSG | International Copper Study Group | Copper balance | CITED |
| IND-IAI | International Aluminium Institute — production statistics | Aluminium | CITED |
| IND-OPEC | OPEC Monthly Oil Market Report | Crude | CITED |
| IND-IEA | IEA Oil Market Report (largely paid) | Crude | CITED |

## 5. Academic literature (to be read/verified before relying on conclusions)
| ID | Reference | Relevance |
|---|---|---|
| AC-01 | Keynes, J.M. (1930). *A Treatise on Money* — normal backwardation | Hedging-pressure premium |
| AC-02 | Kaldor, N. (1939). Speculation and economic stability. *RES* | Theory of storage / convenience yield |
| AC-03 | Working, H. (1949). The theory of price of storage. *AER* | Theory of storage |
| AC-04 | Brennan, M. (1958). The supply of storage. *AER* | Theory of storage |
| AC-05 | Fama, E. & French, K. (1987). Commodity futures prices: some evidence on forecast power, premiums, and the theory of storage. *J. Business* | Basis, storage, premiums |
| AC-06 | de Roon, F., Nijman, T. & Veld, C. (2000). Hedging pressure effects in futures markets. *J. Finance* | Hedging pressure |
| AC-07 | Erb, C. & Harvey, C. (2006). The strategic and tactical value of commodity futures. *FAJ* | Return decomposition, roll yield, near-zero individual premia |
| AC-08 | Gorton, G. & Rouwenhorst, K.G. (2006). Facts and fantasies about commodity futures. *FAJ* | Long-run commodity premium |
| AC-09 | Miffre, J. & Rallis, G. (2007). Momentum strategies in commodity futures markets. *JBF* | Cross-sectional momentum |
| AC-10 | Kilian, L. (2009). Not all oil price shocks are alike. *AER* | Oil supply/demand shock decomposition |
| AC-11 | Mou, Y. (2010). Limits to arbitrage and commodity index investment: front-running the Goldman roll. Working paper (copy hosted by CFTC: https://www.cftc.gov/sites/default/files/idc/groups/public/@swaps/documents/file/plstudy_33_yu.pdf) | Index roll predictability |
| AC-12 | Moskowitz, T., Ooi, Y.H. & Pedersen, L.H. (2012). Time series momentum. *JFE* | Trend |
| AC-13 | Hong, H. & Yogo, M. (2012). What does futures market interest tell us about the macroeconomy and asset prices? *JFE* | Open interest |
| AC-14 | Tang, K. & Xiong, W. (2012). Index investment and the financialization of commodities. *FAJ* | Regime change |
| AC-15 | Gorton, G., Hayashi, F. & Rouwenhorst, K.G. (2013). The fundamentals of commodity futures returns. *Review of Finance* | Inventory ↔ curve ↔ returns |
| AC-16 | Erb, C. & Harvey, C. (2013). The golden dilemma. *FAJ* | Gold valuation, real rates |
| AC-17 | Szymanowska, M., de Roon, F., Nijman, T. & van den Goorbergh, R. (2014). An anatomy of commodity futures risk premia. *J. Finance* | Spot vs term premia |
| AC-18 | Hurst, B., Ooi, Y.H. & Pedersen, L.H. (2017). A century of evidence on trend-following investing. *JPM* | Trend, long history |
| AC-19 | Koijen, R., Moskowitz, T., Pedersen, L.H. & Vrugt, E. (2018). Carry. *JFE* | Carry across asset classes |
| AC-20 | Bakshi, G., Gao, X. & Rossi, A. (2019). Understanding the sources of risk underlying the cross section of commodity returns. *Management Science* | Factor structure |

## Candidate data vendors (to evaluate — OPEN-3.1)
Norgate Data, CSI Data, Barchart, Databento, LSEG/Refinitiv, Bloomberg. (Nasdaq Data Link CHRIS: deprecated, excluded.) Evaluation criteria: per-contract history incl. expired contracts, depth, FND/LTD metadata, settlement vs close, cost, licence terms.
