"""Thin PostgreSQL layer: schema migration, idempotent upserts, reads, audit log."""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd

from ..core.config import dsn, settings

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


@contextmanager
def connect():
    import psycopg

    with psycopg.connect(dsn(), autocommit=False) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SET search_path TO {settings()['database']['schema']}")
        yield conn


def available() -> bool:
    try:
        with connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False


def init_schema() -> None:
    with connect() as conn:
        conn.execute(SCHEMA_FILE.read_text(encoding="utf-8"))
        conn.commit()


def jsonable(o):
    """Recursively convert to strict JSON (NaN/inf -> null, numpy/pandas scalars -> python)."""
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp,)):
        return str(o)
    if isinstance(o, (pd.Series, pd.DataFrame)):
        return None
    return o


def dumps(o) -> str:
    return json.dumps(jsonable(o), default=str, allow_nan=False)


def _clean(v):
    if v is None:
        return None
    if isinstance(v, float) and np.isnan(v):
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return None if np.isnan(v) else float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, pd.Timestamp):
        return None if pd.isna(v) else v.to_pydatetime()
    if isinstance(v, (dict, list)):
        return dumps(v)
    if v is pd.NaT:
        return None
    return v


def upsert(table: str, df: pd.DataFrame, keys: list[str], update: bool = True, chunk: int = 5000) -> int:
    """Idempotent insert: ON CONFLICT (keys) DO UPDATE (or DO NOTHING). Re-running never duplicates."""
    if df is None or df.empty:
        return 0
    cols = list(df.columns)
    placeholders = ",".join(["%s"] * len(cols))
    non_keys = [c for c in cols if c not in keys]
    if update and non_keys:
        action = "DO UPDATE SET " + ",".join(f"{c}=EXCLUDED.{c}" for c in non_keys)
    else:
        action = "DO NOTHING"
    sql = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders}) ON CONFLICT ({','.join(keys)}) {action}"
    rows = [tuple(_clean(v) for v in r) for r in df.itertuples(index=False, name=None)]
    with connect() as conn:
        with conn.cursor() as cur:
            for i in range(0, len(rows), chunk):
                cur.executemany(sql, rows[i:i + chunk])
        conn.commit()
    return len(rows)


def bulk_upsert(table: str, df: pd.DataFrame, keys: list[str], update: bool = True) -> int:
    """Fast idempotent load: COPY into a temp table, then INSERT .. ON CONFLICT."""
    if df is None or df.empty:
        return 0
    cols = list(df.columns)
    non_keys = [c for c in cols if c not in keys]
    action = ("DO UPDATE SET " + ",".join(f"{c}=EXCLUDED.{c}" for c in non_keys)) if update and non_keys else "DO NOTHING"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE TEMP TABLE _stage (LIKE {table} INCLUDING DEFAULTS) ON COMMIT DROP")
            with cur.copy(f"COPY _stage ({','.join(cols)}) FROM STDIN") as cp:
                for row in df.itertuples(index=False, name=None):
                    cp.write_row(tuple(_clean(v) for v in row))
            cur.execute(f"INSERT INTO {table} ({','.join(cols)}) SELECT {','.join(cols)} FROM _stage "
                        f"ON CONFLICT ({','.join(keys)}) {action}")
        conn.commit()
    return len(df)


def read(sql: str, params: tuple | None = None) -> pd.DataFrame:
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            cols = [d.name for d in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=cols)


def execute(sql: str, params: tuple | None = None) -> None:
    with connect() as conn:
        conn.execute(sql, params)
        conn.commit()


def audit(job: str, level: str, message: str, payload: dict | None = None) -> None:
    try:
        execute("INSERT INTO audit_log (job, level, message, payload) VALUES (%s,%s,%s,%s)",
                (job, level, message, dumps(payload or {})))
    except Exception:
        pass  # audit must never break a job
