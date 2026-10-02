# 05 Seasonality Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

- **GC**: Kruskal-Wallis p = 0.723; months with |t|>2: 2 (≈0.5 expected by chance)
- **SI**: Kruskal-Wallis p = 0.608; months with |t|>2: 2 (≈0.5 expected by chance)
- **HG**: Kruskal-Wallis p = 0.839; months with |t|>2: 0 (≈0.5 expected by chance)
- **CL**: Kruskal-Wallis p = 0.665; months with |t|>2: 7 (≈0.5 expected by chance)
- **NG**: Kruskal-Wallis p = 0.686; months with |t|>2: 2 (≈0.5 expected by chance)

| id | family | type | strategy | params | train | val | WF | OOS |
|---|---|---|---|---|---|---|---|---|
| H21 | P_SEASONALITY | A | seasonal | {} | -0.28 | 0.88 | 0.48 | 0.48 |
| H22 | P_SEASONALITY | A | seasonal_trend | {"n": 200} | 0.13 | 1.09 | 0.73 | 0.41 |
