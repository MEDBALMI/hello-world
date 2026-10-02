"""Configuration loading (markets, settings, hypotheses). Single source of runtime parameters."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

PKG_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = PKG_DIR / "config"


@lru_cache(maxsize=None)
def _load(name: str) -> dict:
    with open(CONFIG_DIR / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def markets() -> dict:
    return _load("markets.yaml")["markets"]


def market(root: str) -> dict:
    cfg = dict(_load("markets.yaml")["defaults"])
    cfg.update(markets()[root])
    return cfg


def defaults() -> dict:
    return _load("markets.yaml")["defaults"]


def mcx_charges() -> dict:
    return _load("markets.yaml")["mcx_charges"]


def settings() -> dict:
    return _load("settings.yaml")


def hypotheses() -> list[dict]:
    return _load("hypotheses.yaml")["hypotheses"]


def dsn() -> str:
    return os.environ.get("COMMODITY_DSN", settings()["database"]["dsn"])


def configured_roots(venue: str | None = None) -> list[str]:
    """Roots with a full contract configuration (excludes DATA-LIMITED / NOT-CONFIGURED)."""
    out = []
    for root, cfg in markets().items():
        if cfg.get("status") in ("DATA-LIMITED", "NOT-CONFIGURED"):
            continue
        if venue and cfg.get("venue") != venue:
            continue
        out.append(root)
    return out


def path(key: str) -> Path:
    p = PKG_DIR / settings()["paths"][key]
    p.mkdir(parents=True, exist_ok=True)
    return p
