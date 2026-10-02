# 11 Mcx Implementation Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

MCX returns regressed on same-day and lagged global tradable returns and USDINR (timing: MCX closes after US settlement).

| root | days | rolls_per_year | roll_cost_per_year | avg_one_way_cost | median_held_volume | avg_one_way_cost_global | dec_r2 | dec_alpha | dec_glob_same | dec_glob_lag1 | dec_usdinr | dec_residual_vol_ann |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MCX_GOLD | 5417 | 5.8615 | 0.0049 | 0.0008 | 4773.0000 | 0.0012 | 0.9353 | -0.0000 | 0.9483 | 0.0031 | 0.9767 | 0.0380 |
| MCX_SILVER | 5417 | 4.8846 | 0.0056 | 0.0009 | 4678.0000 | 0.0038 | 0.9646 | -0.0000 | 0.9769 | 0.0157 | 1.0051 | 0.0554 |
| MCX_CRUDEOIL | 5417 | 11.7231 | 0.0108 | 0.0009 | 4478.0000 | 0.0007 | 0.9790 | -0.0001 | 0.9917 | 0.0093 | 1.0298 | 0.0526 |
| MCX_NATURALGAS | 5417 | 11.7231 | 0.1237 | 0.0092 | 4476.5000 | 0.0045 | 0.9691 | 0.0001 | 0.9932 | 0.0093 | 1.0354 | 0.0868 |
| MCX_COPPER | 5417 | 11.7231 | 0.0018 | 0.0002 | 4465.0000 | 0.0003 | 0.9696 | -0.0001 | 0.9806 | 0.0099 | 1.0097 | 0.0438 |
| MCX_ALUMINIUM | 5417 | 11.7231 | 0.0067 | 0.0006 | 2677.5000 | – | – | – | – | – | – | – |

## Strategy transfer (same params, MCX contracts and costs)
| id | params | global_sharpe_full | global_oos | mcx_sharpe_full | mcx_oos | mcx_cost_x2_full | status |
|---|---|---|---|---|---|---|---|
| H08 | {} | 0.635 | 0.317 | 0.693 | 0.456 | 0.557 | – |
| H11 | {'col': 'carry_12m'} | – | – | – | – | – | DATA-LIMITED on MCX (feature not computable) |
