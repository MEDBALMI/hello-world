# 00 — Commodity Research Program: Master Index

**Objective:** build institutional-quality understanding of metals and energy futures (global + MCX), then develop and rigorously test hypotheses. **Not** a strategy search.

**Pipeline:** Knowledge → Market structure → Data → Hypotheses → Historical testing → Robustness → OOS → Paper trading → Live.
**Current stage:** Quantitative foundation complete (Phases 1–3, data architecture design). Phase 4 (data acquisition) desk research done (17); awaiting review before quotes/trials and the validation pilot. No data downloaded, no backtests, no strategies.

## Scope
| Tier | Commodities |
|---|---|
| Core (study first) | Gold, Crude Oil, Copper, Silver, Natural Gas, Aluminium |
| Secondary (later, if research justifies) | Platinum, Palladium, Zinc, Nickel, Lead |
| Out of scope | All agriculture |

Global benchmark ≠ Indian contract: every module keeps **Global** and **MCX** sections separate.

## Evidence labels (used in every file)
| Label | Meaning |
|---|---|
| [FACT] | Contractual, definitional, or officially documented |
| [THEORY] | Established economic model (may or may not hold empirically) |
| [EMPIRICAL] | Published test result — cite source; not yet replicated by us |
| [TESTED] | Replicated/tested in this program (none yet) |
| [BELIEF] | Market folklore; untested |
| [HYPOTHESIS] | Our testable proposition |
| [OPEN] | Open research question — not answerable reliably yet |
| [V-S] | Number/rule confirmed via search excerpt of the official exchange/regulator document (direct fetch blocked) |
| [V-2] | Confirmed by ≥2 secondary (broker/vendor) sources only |
| [VERIFY] | Quoted from memory; still unchecked |
| [ILLUSTRATIVE] | Worked calculation under stated assumptions; not a general rule (see 03 §8.4) |

## Research architecture
Three layers; each concept is defined **once** and cross-referenced.

1. **Foundation layer** — concepts and mechanics shared by all commodities
   - 01 Foundations (50 concepts) · 02 Market structure (equities vs commodities, curve, continuous series)
   - 10 Positioning (COT) · 11 Term structure · 12 Seasonality · 13 Options
2. **Commodity modules** — one per core commodity, each with the same template:
   drivers → mechanism → data source/frequency/history → candidate hypotheses → look-ahead/data risks → backtest design
   - 04 Gold · 05 Crude · 06 Copper · 07 Silver · 08 Natural Gas · 09 Aluminium
   - Cross-commodity relationships (Phase 11) are recorded in the module of the *dependent* commodity, summarised in 15.
3. **Implementation layer**
   - 03 Data architecture (PostgreSQL design) · 14 MCX implementation · 15 Hypotheses · 16 Roadmap
   - SOURCE_REGISTER · RESEARCH_LOG

## Research types and venues (detail: 03 §11)
| Type | Description | Status |
|---|---|---|
| A | Single-commodity time-series | Primary; tested first |
| B | Cross-commodity / relative-value | Designed; after A |
| C | Cross-sectional selection | Supported by the design; not tested yet |

Venues: **Global** = primary for discovering general effects. **MCX** = tested independently (implementation, India-specific effects, USDINR, local liquidity, structure, costs). Every hypothesis is tagged Type × Venue.

## File map
| File | Phase(s) | Status |
|---|---|---|
| [01_COMMODITY_FOUNDATIONS.md](01_COMMODITY_FOUNDATIONS.md) | 1 | v0.2 — specs checked |
| [02_COMMODITY_MARKET_STRUCTURE.md](02_COMMODITY_MARKET_STRUCTURE.md) | 2, 3 | v1.0: Phase 2 + Phase 3 complete |
| [03_COMMODITY_DATA_ARCHITECTURE.md](03_COMMODITY_DATA_ARCHITECTURE.md) | 18 | v1.0 design (no implementation) |
| 04_GOLD_RESEARCH.md | 5 (+11 gold links) | Not started |
| 05_CRUDE_OIL_RESEARCH.md | 6 | Not started |
| 06_COPPER_RESEARCH.md | 7 | Not started |
| 07_SILVER_RESEARCH.md | 8 | Not started |
| 08_NATURAL_GAS_RESEARCH.md | 9 | Not started |
| 09_ALUMINIUM_RESEARCH.md | 10 | Not started |
| 10_COMMODITY_POSITIONING.md | 13 | Not started |
| [11_COMMODITY_TERM_STRUCTURE.md](11_COMMODITY_TERM_STRUCTURE.md) | 14 | v0.1 construction/feature definitions |
| 12_COMMODITY_SEASONALITY.md | 12 | Not started |
| 13_COMMODITY_OPTIONS.md | 16 | Not started |
| 14_MCX_IMPLEMENTATION.md | 17 | Not started |
| 15_COMMODITY_HYPOTHESES.md | 19, 11, 15 | Not started |
| [16_COMMODITY_RESEARCH_ROADMAP.md](16_COMMODITY_RESEARCH_ROADMAP.md) | 20 | v0.3 |
| [17_COMMODITY_DATA_SOURCES.md](17_COMMODITY_DATA_SOURCES.md) | 4 (data acquisition) | v0.1 desk research; decision matrix |
| [SOURCE_REGISTER.md](SOURCE_REGISTER.md) | all | v0.1 |
| [RESEARCH_LOG.md](RESEARCH_LOG.md) | all | ongoing |

## Concept locator (where a concept is *defined*)
| Concept | Defined in |
|---|---|
| Spot, futures, forwards, options; contract mechanics; margin; lifecycle | 01 §A–D |
| Basis, carry, convenience yield, contango/backwardation (definitions) | 01 §E |
| Roll yield, continuous series, roll policy, research vs P&L series | 02 §B |
| Data handling rules, timestamp framework, minimum data, universe review | 03 §5, §6, §8, §9 |
| Curve features & empirical curve research | 11 |
| OI, volume, COT definitions | 01 §F; deep dive 10 |
| Inventory/supply/demand definitions | 01 §G; commodity-specific in 04–09 |
| Participants | 01 §H |
| Equities vs commodities | 02 §A |

## Open research questions register
Tracked in each file with IDs `[OPEN-<phase>.<n>]`; consolidated in 16.
