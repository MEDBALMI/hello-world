# 12 Final Commodity System Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Run tag `synthetic_carry_s7`, runtime 14.5 min.

- Hypotheses registered/tested: 27/25; parameter combinations: 48 (effective independent trials 4, mean |corr| 0.22)
- Reality-check p (best of all trials): 0.024
- Machine statuses: WEAK: H01, H02, H03, H04, H05, H09, H13, H14, H17, H20, H21, H22, H23; REJECTED: H06, H07, H10, H12, H15, H16, H18, H19, H24; ROBUST: H08, H25; PROMISING: H11; DATA-LIMITED: H26; DESIGN-LIMITED: H27
- Validation: {'PASS': 65, 'OPEN': 5}
- Paper replay (reference book, 1y): {'days': 252, 'final_equity': 9929080.0, 'n_trades': 512, 'n_alerts': 77, 'alert_types': {'ROLL_DUE': 77}}

**Machinery check:** in scenario `CARRY` the carry hypothesis (H11) should be detected. Because the planted premium depends on a persistent curve state, it also creates persistent drift, so trend rules may legitimately earn part of it; unrelated families (positioning, macro, seasonality, mean reversion) should not be accepted. Compare with the statuses above.
