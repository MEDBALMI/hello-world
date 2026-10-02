# Local setup progress (Windows PC)

> Handover note so the next session can continue without re-auditing. Last updated 2026-10-02.

## Where the code lives
- **Local folder:** `C:\Users\ADMIN\commodity-local`, a fresh clone separate from the existing `C:\Users\ADMIN\hello-world` and the trading setup.
- **Code:** branch `claude/vigilant-hamilton-neq4f0` (cloud implementation, `4235cc9`) plus one fix on `claude/zen-thompson-mqxfyy` (`81ae85d`).
- **Python:** private venv `.venv` inside the folder, built from Python 3.14. The system Python 3.14 and the Store Python 3.10 are untouched.
- **Commands:** always call `.\.venv\Scripts\python.exe` directly; the venv is never activated.

## Done
| Step | Result |
|---|---|
| Clone cloud branch | Commit `4235cc9` confirmed |
| Venv + packages | pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, psycopg 3.3.6, pytest 9.1.1 |
| Test suite | 25 passed (47 s) |
| Full synthetic run (`run --source synthetic --scenario NULL --seed 7`, no DB) | Validation 65 PASS / 5 OPEN / 0 FAIL; hypothesis results match the cloud (e.g. H01 OOS Sharpe -0.26) |
| Windows crash at report writing (`UnicodeEncodeError`, cp1252) | Worked around with `$env:PYTHONUTF8 = "1"`; fixed permanently in `81ae85d` (all text I/O uses UTF-8, plus a guard test, 26 tests) |

### Differences from the cloud outputs
Only 4 of about 45 output files differ:
- `12_FINAL_COMMODITY_SYSTEM_REPORT_synthetic_null_s7.md` (1 line, probably runtime)
- `roll_rules_synthetic_null_s7.csv`
- `feature_ic_synthetic_null_s7.csv`
- `15_COMMODITY_HYPOTHESES.md`

The suspected cause is small numeric differences from newer pandas/numpy. Not yet confirmed.

## Next steps
1. In `C:\Users\ADMIN\commodity-local`, get and test the fix:
   - `git pull origin claude/zen-thompson-mqxfyy`
   - `.\.venv\Scripts\python.exe -m pytest`, expecting 26 passed.
2. Confirm the 4 diffs with `git diff --word-diff`.
3. Read-only PostgreSQL check, to protect the existing trading databases:
   - services and data directories (`Get-CimInstance Win32_Service`)
   - listening ports 5432/5433/5434
4. Create a **new, separate** `commodity` database on the chosen instance (needs approval).
   - Set `COMMODITY_DSN` for the session only. The default DSN in `config/settings.yaml` is a Unix socket and does not work on Windows.
5. Run `init-db`, then load real **MCX Gold** data first:
   - Use `ingest-mcx` or `ingest-mcx-folder`. The MCX endpoint is marked VERIFY, so the first download may need fixes.
   - Then load the gold drivers: FRED (real yields, USD) and CFTC COT.
6. Run `run --source db --persist` and review the 12 reports. Gold only, since only gold data is loaded.
7. Afterwards, other commodities one at a time. COMEX GC per-contract history needs a paid vendor.

## Safety rules agreed
- No changes to the system Python, existing PostgreSQL instances or trading databases.
- No global environment variables.
- Every database change needs explicit approval.
