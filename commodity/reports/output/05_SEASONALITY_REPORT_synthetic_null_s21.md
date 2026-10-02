# 05 Seasonality Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

- **GC**: Kruskal-Wallis p = 0.776; months with |t|>2: 0 (≈0.5 expected by chance)
- **SI**: Kruskal-Wallis p = 0.833; months with |t|>2: 0 (≈0.5 expected by chance)
- **HG**: Kruskal-Wallis p = 0.688; months with |t|>2: 1 (≈0.5 expected by chance)
- **CL**: Kruskal-Wallis p = 0.182; months with |t|>2: 2 (≈0.5 expected by chance)
- **NG**: Kruskal-Wallis p = 0.702; months with |t|>2: 0 (≈0.5 expected by chance)

| id | family | type | strategy | params | train | val | WF | OOS |
|---|---|---|---|---|---|---|---|---|
| H21 | P_SEASONALITY | A | seasonal | {} | -0.05 | -0.49 | -0.37 | -0.16 |
| H22 | P_SEASONALITY | A | seasonal_trend | {"n": 200} | -0.12 | -0.41 | -0.23 | 0.12 |
