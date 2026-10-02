# 11 Mcx Implementation Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

MCX returns regressed on same-day and lagged global tradable returns and USDINR (timing: MCX closes after US settlement).

| root | days | rolls_per_year | roll_cost_per_year | avg_one_way_cost | median_held_volume | avg_one_way_cost_global | dec_r2 | dec_alpha | dec_glob_same | dec_glob_lag1 | dec_usdinr | dec_residual_vol_ann |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MCX_GOLD | 5417 | 5.8615 | 0.0009 | 0.0002 | 4774.0000 | 0.0003 | 0.9451 | -0.0000 | 0.9579 | 0.0096 | 1.0036 | 0.0375 |
| MCX_SILVER | 5417 | 4.8846 | 0.0048 | 0.0008 | 4681.0000 | 0.0044 | 0.9604 | 0.0001 | 0.9656 | 0.0181 | 1.0032 | 0.0542 |
| MCX_CRUDEOIL | 5417 | 11.7231 | 0.0017 | 0.0002 | 4474.0000 | 0.0002 | 0.9786 | 0.0001 | 0.9885 | 0.0119 | 0.9994 | 0.0505 |
| MCX_NATURALGAS | 5417 | 11.7231 | 0.1053 | 0.0081 | 4480.0000 | 0.0052 | 0.9678 | -0.0001 | 0.9893 | 0.0131 | 0.9660 | 0.0891 |
| MCX_COPPER | 5417 | 11.7231 | 0.0277 | 0.0022 | 4465.0000 | 0.0023 | 0.9643 | -0.0000 | 0.9725 | 0.0112 | 0.9921 | 0.0469 |
| MCX_ALUMINIUM | 5417 | 11.7231 | 0.0318 | 0.0026 | 2679.0000 | – | – | – | – | – | – | – |

## Strategy transfer (same params, MCX contracts and costs)
| id | params | global_sharpe_full | global_oos | mcx_sharpe_full | mcx_oos | mcx_cost_x2_full |
|---|---|---|---|---|---|---|
| H01 | {'lookback': 252} | 0.189 | 0.518 | 0.530 | 0.404 | 0.290 |
| H11 | {'col': 'carry'} | 0.194 | 0.072 | 0.105 | 0.224 | -0.291 |
