# 12 Final Commodity System Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Run tag `synthetic_null_s21`, runtime 14.2 min.

- Hypotheses registered/tested: 27/25; parameter combinations: 48 (effective independent trials 5, mean |corr| 0.20)
- Reality-check p (best of all trials): 0.684
- Machine statuses: WEAK: H01, H02, H04, H05, H11, H13, H14, H23; REJECTED: H03, H06, H07, H08, H09, H10, H12, H15, H16, H17, H18, H19, H20, H21, H22, H24, H25; DATA-LIMITED: H26; DESIGN-LIMITED: H27
- Validation: {'PASS': 65, 'OPEN': 5}
- Paper replay (reference book, 1y): {'days': 252, 'final_equity': 9814755.0, 'n_trades': 535, 'n_alerts': 76, 'alert_types': {'ROLL_DUE': 76}}

**Machinery check:** in scenario `NULL` all hypotheses should be REJECTED or WEAK (no edge exists by construction). Compare with the statuses above.
