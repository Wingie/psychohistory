"""Dataset loaders with local caching. All sources are public; raw downloads
land in validate/data/ (gitignored, regenerable), curated hand-coded tables
live in validate/curated/ (committed, sources documented in
curated/README.md).

Sources
-------
- JST Macrohistory Database R6 (macrohistory.net), CC-BY-NC-SA-ish academic
  license: Jorda, Schularick, Taylor et al. 18 countries, 1870-2020, credit
  aggregates + systemic crisis flags.
- Wikipedia, "Motor vehicle fatality rate in U.S. by year" (CC BY-SA 4.0),
  which transcribes the FHWA/NHTSA series: deaths, VMT, deaths per 100M VMT.
- Our World in Data grapher: fatal airliner accidents per million commercial
  flights (CC BY; underlying data ASN/Boeing as compiled by OWID).
- World Bank Open Data API (CC BY 4.0): IS.AIR.DPRT registered carrier
  departures worldwide.
- Epoch AI, notable AI models dataset (CC BY): training compute estimates.
"""

from __future__ import annotations

import io
import json
import os
import re
import ssl
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
CURATED = HERE / "curated"

URLS = {
    "jst": "https://www.macrohistory.net/app/download/9834512469/JSTdatasetR6.dta",
    "us_roads_wiki": (
        "https://en.wikipedia.org/w/api.php?action=parse"
        "&page=Motor_vehicle_fatality_rate_in_U.S._by_year"
        "&prop=wikitext&format=json&formatversion=2"
    ),
    "owid_aviation": (
        "https://ourworldindata.org/grapher/"
        "fatal-airliner-accidents-per-million-flights.csv"
        "?useColumnShortNames=true"
    ),
    "wb_departures": (
        "https://api.worldbank.org/v2/country/WLD/indicator/IS.AIR.DPRT"
        "?format=json&per_page=200"
    ),
    "epoch_models": "https://epoch.ai/data/epochdb/notable_ai_models.csv",
}


def _ssl_context() -> ssl.SSLContext:
    """Honor the environment's CA bundle (managed egress proxies re-terminate
    TLS); fall back to system defaults."""
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        path = os.environ.get(var)
        if path and Path(path).exists():
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()


def fetch(key: str, fname: str, refresh: bool = False) -> Path:
    """Download URLS[key] into the cache (once) and return the local path."""
    DATA.mkdir(exist_ok=True)
    path = DATA / fname
    if path.exists() and not refresh:
        return path
    req = urllib.request.Request(
        URLS[key], headers={"User-Agent": "steering-envelope/0.2 (research)"})
    with urllib.request.urlopen(req, context=_ssl_context(), timeout=180) as r:
        path.write_bytes(r.read())
    return path


# ----------------------------------------------------------------------------
# domain loaders
# ----------------------------------------------------------------------------

def load_jst() -> pd.DataFrame:
    """JST Macrohistory R6: country-year panel with crisisJST, nominal loans
    (tloans), CPI, GDP, population."""
    path = fetch("jst", "JSTdatasetR6.dta")
    df = pd.read_stata(path)
    keep = ["year", "country", "iso", "crisisJST", "tloans", "cpi", "gdp",
            "pop"]
    return df[[c for c in keep if c in df.columns]].copy()


def load_us_roads() -> pd.DataFrame:
    """US road panel from the FHWA/NHTSA series as transcribed on Wikipedia:
    year, deaths, vmt (billions), rate (deaths per 100M VMT)."""
    path = fetch("us_roads_wiki", "us_roads_wiki.json")
    wt = json.loads(path.read_text())["parse"]["wikitext"]
    rows = []
    current: list = []
    for raw in wt.splitlines():
        line = raw.strip()
        if line.startswith("|-"):
            if current:
                rows.append(current)
            current = []
        elif line.startswith("|") and not line.startswith("|}"):
            current.append(line[1:].strip())
    if current:
        rows.append(current)

    def num(cell: str):
        cell = re.sub(r"<ref.*?(</ref>|/>)", "", cell)
        cell = re.sub(r"\{\{.*?\}\}", "", cell)
        cell = cell.replace(",", "").strip()
        m = re.match(r"^-?\d+(\.\d+)?$", cell)
        return float(m.group(0)) if m else np.nan

    out = []
    for r in rows:
        if len(r) < 4:
            continue
        year = num(r[0])
        if not (1899 <= (year or 0) <= 2100):
            continue
        out.append({
            "year": int(year),
            "deaths": num(r[1]),
            "vmt": num(r[2]),
            "rate": num(r[3]),
        })
    df = pd.DataFrame(out).drop_duplicates("year").sort_values("year")
    return df.reset_index(drop=True)


def load_owid_aviation() -> pd.DataFrame:
    """World fatal airliner accidents per million commercial flights
    (OWID, from ASN data), 1970-present."""
    path = fetch("owid_aviation", "owid_aviation.csv")
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    rate_col = [c for c in df.columns
                if "accident" in c or "per_million" in c][-1]
    df = df[df["entity"] == "World"][["year", rate_col]]
    return df.rename(columns={rate_col: "fatal_per_million"}).reset_index(
        drop=True)


def load_wb_departures() -> pd.DataFrame:
    """World registered carrier departures (IS.AIR.DPRT), World Bank."""
    path = fetch("wb_departures", "wb_departures.json")
    payload = json.loads(path.read_text())
    rows = [{"year": int(d["date"]), "departures": d["value"]}
            for d in payload[1] if d["value"] is not None]
    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)


def load_epoch() -> pd.DataFrame:
    """Epoch AI notable models: publication date + training compute (FLOP)."""
    path = fetch("epoch_models", "epoch_notable_ai_models.csv")
    df = pd.read_csv(path, low_memory=False)
    cols = {c.lower().strip(): c for c in df.columns}
    date_col = next(cols[c] for c in cols if "publication date" in c)
    flop_col = next(cols[c] for c in cols
                    if "training compute" in c and "flop" in c)
    out = df[[date_col, flop_col]].dropna()
    out.columns = ["date", "flop"]
    out["year"] = pd.to_datetime(out["date"], errors="coerce").dt.year
    out = out.dropna(subset=["year"])
    out["year"] = out["year"].astype(int)
    return out[["year", "flop"]].reset_index(drop=True)


# ----------------------------------------------------------------------------
# curated tables (committed; see curated/README.md for sources)
# ----------------------------------------------------------------------------

def load_curated(name: str) -> pd.DataFrame:
    return pd.read_csv(CURATED / f"{name}.csv", comment="#")


def steering_index(events: pd.DataFrame, years: np.ndarray,
                   ramp: int = 5, s0: float = 1.0) -> np.ndarray:
    """Turn a table of (year, weight) steering interventions into a smooth
    cumulative capacity index: each intervention phases in linearly over
    `ramp` years (laws take time to bind)."""
    years = np.asarray(years)
    s = np.full(len(years), s0, dtype=float)
    for _, row in events.iterrows():
        frac = np.clip((years - row["year"]) / ramp, 0.0, 1.0)
        s += row["weight"] * frac
    return s
