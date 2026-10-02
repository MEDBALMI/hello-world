# Research Log

Chronological record of what was done, decided, and left open. Newest first.

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
