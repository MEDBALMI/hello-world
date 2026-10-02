# 05 Seasonality Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

- **GC**: Kruskal-Wallis p = 0.706; months with |t|>2: 0 (≈0.5 expected by chance)
- **SI**: Kruskal-Wallis p = 0.717; months with |t|>2: 0 (≈0.5 expected by chance)
- **HG**: Kruskal-Wallis p = 0.847; months with |t|>2: 0 (≈0.5 expected by chance)
- **CL**: Kruskal-Wallis p = 0.650; months with |t|>2: 2 (≈0.5 expected by chance)
- **NG**: Kruskal-Wallis p = 0.651; months with |t|>2: 0 (≈0.5 expected by chance)

| id | family | type | strategy | params | train | val | WF | OOS |
|---|---|---|---|---|---|---|---|---|
| H21 | P_SEASONALITY | A | seasonal | {} | -0.53 | -0.01 | -0.23 | 0.14 |
| H22 | P_SEASONALITY | A | seasonal_trend | {"n": 200} | -0.58 | 0.11 | -0.42 | -0.18 |
