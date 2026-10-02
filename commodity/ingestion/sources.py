"""Real-data ingestion adapters (Tier 1 official / Tier 2 vendor files).

Network access to these hosts is blocked in the development environment; the adapters are
written against documented formats and must be smoke-tested on first real run (fields marked
VERIFY). Every adapter returns the standard frames used by the pipeline:

prices: root, contract_id, trade_date, open, high, low, close, settle, volume, open_interest, source_id
"""
from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from ..core import calendars as cal
from ..core.contracts import MONTH_CODES, contract_calendar, contract_id

PRICE_COLS = ["root", "contract_id", "trade_date", "open", "high", "low", "close", "settle",
              "volume", "open_interest", "source_id"]


def _http_get(url: str, **kw) -> bytes:
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 commodity-research"}, **kw)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


# ------------------------------------------------------------------ vendor / DataMine CSV exports
_SYM = re.compile(r"^(?P<root>[A-Z]+?)[-_ ]?(?P<code>[FGHJKMNQUVXZ])(?P<yy>\d{2}|\d{4})$")
_SYM2 = re.compile(r"^(?P<root>[A-Z]+?)[-_ ]?(?P<yyyy>\d{4})(?P<code>[FGHJKMNQUVXZ])$")


def parse_symbol(sym: str, root_map: dict | None = None) -> tuple[str, str] | None:
    """Parse vendor symbols like CLF24, CL-2024F, CLF2024 -> (root, contract_id)."""
    s = sym.strip().upper()
    m = _SYM.match(s) or _SYM2.match(s)
    if not m:
        return None
    g = m.groupdict()
    year = int(g.get("yyyy") or g["yy"])
    if year < 100:
        year += 2000 if year < 70 else 1900
    root = (root_map or {}).get(g["root"], g["root"])
    return root, contract_id(root, year, MONTH_CODES.index(g["code"]) + 1)


def load_vendor_csv(path: str | Path, mapping: dict, source_id: str, root_map: dict | None = None) -> pd.DataFrame:
    """mapping: our column -> vendor column, must include 'symbol' and 'trade_date'.
    Use for CME DataMine EOD, Norgate/CSI exports. Close is NOT assumed to equal settle unless
    the source registry says close_is_settlement."""
    raw = pd.read_csv(path)
    df = pd.DataFrame({k: raw[v] for k, v in mapping.items() if v in raw.columns})
    parsed = df["symbol"].map(lambda s: parse_symbol(str(s), root_map))
    df = df[parsed.notna()].copy()
    df["root"] = parsed.dropna().map(lambda t: t[0])
    df["contract_id"] = parsed.dropna().map(lambda t: t[1])
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    for c in PRICE_COLS:
        if c not in df:
            df[c] = np.nan
    df["source_id"] = source_id
    return df[PRICE_COLS]


# ------------------------------------------------------------------ MCX bhavcopy
MCX_ROOTS = {"GOLD": "MCX_GOLD", "SILVER": "MCX_SILVER", "CRUDEOIL": "MCX_CRUDEOIL",
             "NATURALGAS": "MCX_NATURALGAS", "COPPER": "MCX_COPPER", "ALUMINIUM": "MCX_ALUMINIUM"}
MCX_URL = "https://www.mcxindia.com/backpage.aspx/GetDateWiseBhavCopy"  # VERIFY endpoint/payload


def fetch_mcx_bhavcopy(day) -> pd.DataFrame:
    """Download one day's bhavcopy (JSON endpoint used by the MCX website; VERIFY on first run)."""
    import json
    import urllib.request

    payload = json.dumps({"Date": pd.Timestamp(day).strftime("%Y%m%d"), "InstrumentName": "ALL"}).encode()
    req = urllib.request.Request(MCX_URL, data=payload, headers={
        "Content-Type": "application/json", "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.mcxindia.com/market-data/bhavcopy"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return pd.DataFrame(data.get("d", {}).get("Data", []))


def parse_mcx_bhavcopy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Map bhavcopy rows (FUTCOM only) to standard prices + per-contract expiry calendar.
    Column names vary by era (VERIFY); this accepts the common variants."""
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    g = lambda *names: next((df[cols[n]] for n in names if n in cols), pd.Series(np.nan, index=df.index))
    inst = g("instrumentname", "instrument").astype(str).str.upper()
    sym = g("symbol").astype(str).str.upper().str.strip()
    keep = inst.str.contains("FUTCOM") & sym.isin(MCX_ROOTS)
    d = df[keep]
    expiry = pd.to_datetime(g("expirydate", "expiry")[keep], dayfirst=True, errors="coerce")
    root = sym[keep].map(MCX_ROOTS)
    out = pd.DataFrame({
        "root": root,
        "contract_id": [contract_id(r, e.year, e.month) for r, e in zip(root, expiry)],
        "trade_date": pd.to_datetime(g("date", "tradedate")[keep], dayfirst=True, errors="coerce"),
        "open": pd.to_numeric(g("open")[keep], errors="coerce"),
        "high": pd.to_numeric(g("high")[keep], errors="coerce"),
        "low": pd.to_numeric(g("low")[keep], errors="coerce"),
        "close": pd.to_numeric(g("close")[keep], errors="coerce"),
        "settle": pd.to_numeric(g("settlementprice", "close")[keep], errors="coerce"),  # VERIFY field
        "volume": pd.to_numeric(g("volume", "volume(lots)")[keep], errors="coerce"),
        "open_interest": pd.to_numeric(g("openinterest", "openinterest(lots)")[keep], errors="coerce"),
        "source_id": "MCX_BHAVCOPY",
    })
    expcal = pd.DataFrame({"root": root.values, "contract_id": out.contract_id.values,
                           "ltd": expiry.values}).drop_duplicates("contract_id")
    return out, expcal


def load_mcx_folder(folder: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse manually downloaded bhavcopy CSV files."""
    frames = [pd.read_csv(p) for p in sorted(Path(folder).glob("*.csv"))]
    return parse_mcx_bhavcopy(pd.concat(frames, ignore_index=True)) if frames else (pd.DataFrame(), pd.DataFrame())


# ------------------------------------------------------------------ CFTC COT (disaggregated)
CFTC_URL = "https://www.cftc.gov/files/dea/history/fut_disagg_txt_{year}.zip"
CFTC_HIST = "https://www.cftc.gov/files/dea/history/fut_disagg_txt_hist_2006_2016.zip"
COT_COLS = {  # disaggregated column names (VERIFY on first run)
    "open_interest": "Open_Interest_All",
    "mm_long": "M_Money_Positions_Long_All", "mm_short": "M_Money_Positions_Short_All",
    "pm_long": "Prod_Merc_Positions_Long_All", "pm_short": "Prod_Merc_Positions_Short_All",
    "sd_long": "Swap_Positions_Long_All", "sd_short": "Swap__Positions_Short_All",
}


def cot_release_ts(as_of: pd.Series) -> pd.Series:
    """Friday 15:30 America/New_York after the Tuesday as-of date, in UTC. Holiday-delayed
    releases must be corrected from the CFTC release schedule (OPEN-6.1)."""
    fri = pd.to_datetime(as_of) + pd.Timedelta(days=3, hours=15, minutes=30)
    return fri.dt.tz_localize("America/New_York").dt.tz_convert("UTC")


def parse_cot(df: pd.DataFrame, code_map: dict) -> pd.DataFrame:
    code = df["CFTC_Contract_Market_Code"].astype(str).str.strip()
    d = df[code.isin(code_map)].copy()
    out = pd.DataFrame({"report_type": "disaggregated",
                        "root": code[code.isin(code_map)].map(code_map),
                        "as_of_date": pd.to_datetime(d["Report_Date_as_YYYY-MM-DD"])})
    for k, v in COT_COLS.items():
        out[k] = pd.to_numeric(d.get(v), errors="coerce")
    out["release_ts"] = cot_release_ts(out["as_of_date"])
    out["source_id"] = "CFTC"
    return out


def fetch_cot(years: list[int], code_map: dict) -> pd.DataFrame:
    frames = []
    for y in years:
        z = zipfile.ZipFile(io.BytesIO(_http_get(CFTC_URL.format(year=y))))
        frames.append(pd.read_csv(z.open(z.namelist()[0]), low_memory=False))
    return parse_cot(pd.concat(frames, ignore_index=True), code_map)


# ------------------------------------------------------------------ FRED (market rates; latest vintage)
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"


def fetch_fred(series: list[str]) -> pd.DataFrame:
    frames = []
    for sid in series:
        df = pd.read_csv(io.BytesIO(_http_get(FRED_URL.format(sid=sid))))
        df.columns = ["obs_date", "value"]
        df["obs_date"] = pd.to_datetime(df["obs_date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["series_id"] = sid
        # conservative availability: next business day 21:00 UTC (H.15 publishes next day)
        df["available_ts"] = (df["obs_date"] + pd.offsets.BDay(1) + pd.Timedelta(hours=21)).dt.tz_localize("UTC")
        df["vintage"] = "latest"
        df["source_id"] = "FRED"
        frames.append(df.dropna(subset=["value"]))
    return pd.concat(frames, ignore_index=True)


# ------------------------------------------------------------------ EIA positional futures (to 2024-04-05)
EIA_XLS = "https://www.eia.gov/dnav/{grp}/hist_xls/{sid}d.xls"
EIA_SERIES = {"CL": ("pet", ["RCLC1", "RCLC2", "RCLC3", "RCLC4"]),
              "NG": ("ng", ["RNGC1", "RNGC2", "RNGC3", "RNGC4"])}


def positional_to_contracts(root: str, pos: pd.DataFrame) -> pd.DataFrame:
    """Map EIA 'contract k' daily settlements to contract identities using the LTD rule:
    contract k on date t = k-th listed contract with LTD >= t. Result is L4-like for the first
    4 contracts (settle only; no OHLC/volume/OI) -> DATA-LIMITED source."""
    cc = contract_calendar(root, pos.index.min(), pos.index.max()).sort_values("ltd")
    ltds = cc["ltd"].values
    rows = []
    for t, row in pos.iterrows():
        i0 = np.searchsorted(ltds, np.datetime64(t), side="left")
        for k, v in enumerate(row.values):
            if pd.notna(v) and i0 + k < len(cc):
                rows.append((root, cc.contract_id.iloc[i0 + k], t, v))
    df = pd.DataFrame(rows, columns=["root", "contract_id", "trade_date", "settle"])
    for c in ("open", "high", "low", "volume", "open_interest"):
        df[c] = np.nan
    df["close"] = df["settle"]
    df["source_id"] = "EIA_FUT"
    return df[PRICE_COLS]


def fetch_eia_positional(root: str) -> pd.DataFrame:
    grp, sids = EIA_SERIES[root]
    cols = {}
    for k, sid in enumerate(sids, 1):
        x = pd.read_excel(io.BytesIO(_http_get(EIA_XLS.format(grp=grp, sid=sid))), sheet_name="Data 1", skiprows=2)
        x.columns = ["date", "value"]
        cols[k] = x.set_index(pd.to_datetime(x["date"]))["value"]
    return positional_to_contracts(root, pd.DataFrame(cols))
