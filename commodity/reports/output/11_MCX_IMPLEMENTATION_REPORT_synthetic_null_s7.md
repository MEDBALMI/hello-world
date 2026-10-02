# 11 Mcx Implementation Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

MCX returns regressed on same-day and lagged global tradable returns and USDINR (timing: MCX closes after US settlement).

| root | days | rolls_per_year | roll_cost_per_year | avg_one_way_cost | median_held_volume | avg_one_way_cost_global | dec_r2 | dec_alpha | dec_glob_same | dec_glob_lag1 | dec_usdinr | dec_residual_vol_ann |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MCX_GOLD | 5417 | 5.8615 | 0.0013 | 0.0003 | 4773.0000 | 0.0004 | 0.9384 | 0.0000 | 0.9522 | 0.0005 | 0.9759 | 0.0371 |
| MCX_SILVER | 5417 | 4.8846 | 0.0014 | 0.0003 | 4678.0000 | 0.0010 | 0.9765 | -0.0000 | 0.9879 | 0.0087 | 1.0130 | 0.0452 |
| MCX_CRUDEOIL | 5417 | 11.7231 | 0.1852 | 0.0139 | 4478.0000 | 0.0061 | 0.9285 | -0.0001 | 0.9811 | 0.0172 | 0.9994 | 0.0994 |
| MCX_NATURALGAS | 5417 | 11.7231 | 0.0451 | 0.0035 | 4476.5000 | 0.0019 | 0.9787 | 0.0001 | 0.9938 | 0.0097 | 1.0102 | 0.0716 |
| MCX_COPPER | 5417 | 11.7231 | 0.0036 | 0.0004 | 4465.0000 | 0.0004 | 0.9694 | -0.0001 | 0.9805 | 0.0099 | 1.0091 | 0.0439 |
| MCX_ALUMINIUM | 5417 | 11.7231 | 0.0317 | 0.0026 | 2677.5000 | – | – | – | – | – | – | – |

## Strategy transfer (same params, MCX contracts and costs)
| id | params | global_sharpe_full | global_oos | mcx_sharpe_full | mcx_oos | mcx_cost_x2_full | status |
|---|---|---|---|---|---|---|---|
| H01 | {'lookback': 126} | -0.192 | -0.258 | -0.328 | -0.202 | -0.911 | – |
| H11 | {'col': 'carry_12m'} | – | – | – | – | – | DATA-LIMITED on MCX (feature not computable) |
