# 12 Final Commodity System Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Run tag `synthetic_null_s7`, runtime 14.0 min.

- Hypotheses registered/tested: 27/25; parameter combinations: 48 (effective independent trials 5, mean |corr| 0.20)
- Reality-check p (best of all trials): 0.770
- Machine statuses: REJECTED: H01, H02, H03, H04, H07, H08, H09, H12, H13, H14, H15, H16, H17, H18, H19, H20, H21, H22, H23, H24, H25; WEAK: H05, H06, H10, H11; DATA-LIMITED: H26; DESIGN-LIMITED: H27
- Validation: {'PASS': 65, 'OPEN': 5}
- Paper replay (reference book, 1y): {'days': 252, 'final_equity': 9720372.5, 'n_trades': 433, 'n_alerts': 75, 'alert_types': {'ROLL_DUE': 75}}

**Machinery check:** in scenario `NULL` all hypotheses should be REJECTED or WEAK (no edge exists by construction). Compare with the statuses above.
