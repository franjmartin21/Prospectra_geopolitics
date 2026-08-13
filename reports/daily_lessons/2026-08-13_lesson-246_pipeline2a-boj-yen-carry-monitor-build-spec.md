# Lesson 246: Pipeline 2-A Build Spec — BOJ Yen Carry Monitor, Complete Code
**Date:** 2026-08-13 (Thursday)
**Session Type:** Engineering Phase — Pipeline Build Sprint
**Curriculum Position:** 246 — Engineering Phase, Session 9
**Pipeline 4 Deadline:** August 15, 2026 — **2 days**
**Pipeline 2-A Deadline:** September 12, 2026 — 30 days

---

## CEO Opening Question

Pipeline 4 code has been in your hands for two days. The August 15 deadline is Saturday.

Here is today's question — and it is not about Pipeline 4:

**What would it take for the yen carry unwind to happen *before* Pipeline 2-A is live — and would you know it in time?**

The BOJ's next scheduled meeting is September 19. Pipeline 2-A's deadline is September 12 — one week before. If Pipeline 2-A goes live on schedule, you have 7 days of live signal heading into the most consequential policy meeting of the current rate normalization cycle.

If it doesn't go live on schedule, you have the same signal-gathering capacity you had in August 2024 when the Nikkei dropped 13% in 48 hours: none.

Today's lesson does not wait for Pipeline 4 confirmation. The code for Pipeline 2-A is written below. The September 12 deadline is now formally active. When you finish Pipeline 4 this weekend, you open this document next.

The build sprint is already queued. Read it, understand it, run it.

---

## Why Pipeline 2-A Is the Hardest Build in the Sequence

Pipeline 4 (Export Control Radar) was deliberately chosen as the first build because it runs on GDELT alone — no authentication, no market data APIs, no paid subscriptions. You can have it running in 60 minutes.

Pipeline 2-A is more complex for two structural reasons:

**1. It requires market data, not just news sentiment.**

The yen carry signal cannot be detected from GDELT alone. The actual warning indicators are market quantities:
- JPY/USD exchange rate (daily close and intraday moves)
- The MOVE Index (US Treasury volatility — the single best early-warning indicator of carry stress)
- BOJ policy rate (from official BOJ data releases)
- Japan 10-year JGB yield (the carry anchor)
- Nikkei 225 (equity-side carry proxy)

These require real data APIs: FRED (Federal Reserve Economic Data, free) for MOVE and macro series, and a Yahoo Finance wrapper or Alpha Vantage (free tier) for daily exchange rates and equity prices.

**2. It must distinguish signal from noise.**

JPY appreciates against the dollar regularly. Every JPY/USD move does not indicate a carry unwind. Pipeline 2-A must distinguish between:
- **Routine FX movement:** JPY/USD moves < 0.5% on no news
- **BOJ communication signal:** Hawkish language from Ueda without a rate move (pre-position signal)
- **Pre-unwind positioning:** JPY strengthening on rising MOVE + falling Nikkei (the dangerous confluence)
- **Active unwind:** JPY strengthening > 2% over 3 sessions + rising MOVE + institutional positioning shift

Only the last two warrant portfolio response. The pipeline must score them differently.

This is the hard engineering problem. The solution below handles it.

---

## Pipeline 2-A Architecture — Final Specification

```
PIPELINE 2-A: BOJ Yen Carry Unwind Early Warning Monitor
Version: 1.0

INPUTS:
  1. FRED API — MOVE Index (TMUBMUSD01Y volatility), US 10Y yield
  2. Yahoo Finance (yfinance) — JPY/USD (JPYUSD=X), Nikkei (^N225)
  3. FRED API — BOJ policy rate series (IRSTCI01JPM156N or equivalent)
  4. GDELT — BOJ / Bank of Japan / rate hike sentiment (news signal)
  5. BOJ website RSS — official rate decisions and meeting minutes

OUTPUTS:
  1. jpy_stress_score: float (1.0–5.0) — FX + equity carry stress composite
  2. move_signal: float (1.0–5.0) — US Treasury volatility component
  3. boj_communication_score: float (1.0–5.0) — BOJ guidance hawkishness
  4. p2a_composite_score: float (1.0–5.0) — GSI-ready output (Signal 1)
  5. carry_unwind_phase: string — "DORMANT" / "POSITIONING" / "EARLY_UNWIND" / "ACTIVE_UNWIND"

FREQUENCY: Daily (run at 6:00 UTC)
DESTINATION: Delta table `geopolitics.pipeline2a_scores`
ALERT THRESHOLD: p2a_composite_score >= 3.8 → immediate email to Bolo
```

The `carry_unwind_phase` is the novel categorical output that Pipeline 4 did not have. The score alone is useful; the phase label is actionable — it answers "what do I do right now?" without interpretation.

---

## The Complete Code — Notebook Cell by Cell

### Cell 1: Setup and Configuration

```python
# Pipeline 2-A: BOJ Yen Carry Unwind Early Warning Monitor
# Version 1.0 | Prospectra Geopolitics & Investment

import requests
import datetime
import json
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType, TimestampType

spark = SparkSession.builder.appName("Pipeline2A_BOJCarryMonitor").getOrCreate()

# ── Configuration ──────────────────────────────────────────────────────────────
FRED_API_KEY = dbutils.secrets.get(scope="prospectra", key="fred_api_key")
# Free FRED API key at: https://fred.stlouisfed.org/docs/api/api_key.html

ALERT_THRESHOLD = 3.8       # Alert Bolo above this level
BOJ_RATE_THRESHOLD = 0.75   # The policy rate level that triggers maximum sensitivity
LOOKBACK_DAYS_MARKET = 30   # Market data window for trend detection
LOOKBACK_DAYS_GDELT = 7     # GDELT news window

GDELT_GKG_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"
FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

print("Pipeline 2-A initialized: BOJ Yen Carry Monitor")
print(f"Alert threshold: {ALERT_THRESHOLD}/5.0")
print(f"BOJ rate sensitivity threshold: {BOJ_RATE_THRESHOLD}%")
print(f"Market lookback: {LOOKBACK_DAYS_MARKET} days")
```

---

### Cell 2: FRED Data Fetch (MOVE Index + US Rates)

```python
def fetch_fred_series(series_id, lookback_days=60):
    """
    Fetch a FRED time series and return as a pandas DataFrame.
    
    Key series IDs:
    - TMUBMUSD01Y: MOVE Index (Merrill Lynch Option Volatility Estimate) — ICE BofA 1M MOVE Index
    - DGS10: 10-Year Treasury Yield
    - DEXJPUS: JPY per USD exchange rate (inverse of JPY/USD)
    - IRSTCI01JPM156N: BOJ short-term interest rate (monthly, delayed ~4 weeks)
    """
    start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "sort_order": "desc",
        "limit": lookback_days + 10
    }
    
    try:
        r = requests.get(FRED_BASE, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        
        obs = data.get("observations", [])
        rows = []
        for o in obs:
            try:
                rows.append({
                    "date": datetime.datetime.strptime(o["date"], "%Y-%m-%d").date(),
                    "value": float(o["value"])
                })
            except (ValueError, KeyError):
                continue  # Skip "." (missing) observations
        
        df = pd.DataFrame(rows).sort_values("date", ascending=False).reset_index(drop=True)
        return df
    except Exception as e:
        print(f"FRED fetch error for {series_id}: {e}")
        return pd.DataFrame(columns=["date", "value"])


def get_market_data():
    """Fetch all required FRED series and return clean current + trend values."""
    print("Fetching FRED market data...")
    
    move_df = fetch_fred_series("TMUBMUSD01Y", lookback_days=LOOKBACK_DAYS_MARKET)
    jpy_df = fetch_fred_series("DEXJPUS", lookback_days=LOOKBACK_DAYS_MARKET)  # JPY per USD (higher = weaker JPY)
    us10y_df = fetch_fred_series("DGS10", lookback_days=LOOKBACK_DAYS_MARKET)
    boj_rate_df = fetch_fred_series("IRSTCI01JPM156N", lookback_days=90)  # Monthly — need longer window
    
    results = {}
    
    # MOVE Index current + 5-day trend
    if not move_df.empty:
        results["move_current"] = move_df["value"].iloc[0]
        results["move_5d_avg"] = move_df["value"].head(5).mean()
        results["move_20d_avg"] = move_df["value"].head(20).mean()
        results["move_trend"] = results["move_current"] / results["move_20d_avg"] - 1  # +10% = elevated
        print(f"  MOVE Index: {results['move_current']:.1f} (20d avg: {results['move_20d_avg']:.1f}, trend: {results['move_trend']:+.1%})")
    else:
        results.update({"move_current": None, "move_5d_avg": None, "move_20d_avg": None, "move_trend": 0})
    
    # JPY/USD — convert: FRED gives JPY per USD, we want USD per JPY
    # Higher DEXJPUS = weaker JPY; lower = stronger JPY (potential carry stress)
    if not jpy_df.empty:
        jpy_usd_current = 1 / jpy_df["value"].iloc[0]     # Convert to USD per JPY
        jpy_usd_5d = 1 / jpy_df["value"].head(5).mean()
        jpy_usd_20d = 1 / jpy_df["value"].head(20).mean()
        results["jpy_usd_current"] = jpy_usd_current
        results["jpy_appreciation_5d"] = (jpy_usd_current / jpy_usd_5d) - 1   # + = JPY strengthening (carry stress)
        results["jpy_appreciation_20d"] = (jpy_usd_current / jpy_usd_20d) - 1
        print(f"  JPY/USD: {jpy_usd_current:.4f} | 5d move: {results['jpy_appreciation_5d']:+.2%} | 20d: {results['jpy_appreciation_20d']:+.2%}")
    else:
        results.update({"jpy_usd_current": None, "jpy_appreciation_5d": 0, "jpy_appreciation_20d": 0})
    
    # BOJ policy rate (monthly, use most recent available)
    if not boj_rate_df.empty:
        results["boj_rate"] = boj_rate_df["value"].iloc[0]
        print(f"  BOJ Policy Rate (latest): {results['boj_rate']:.2f}%")
    else:
        results["boj_rate"] = None
    
    # US 10Y yield
    if not us10y_df.empty:
        results["us10y_current"] = us10y_df["value"].iloc[0]
        results["us10y_20d_avg"] = us10y_df["value"].head(20).mean()
        print(f"  US 10Y: {results['us10y_current']:.2f}% (20d avg: {results['us10y_20d_avg']:.2f}%)")
    else:
        results.update({"us10y_current": None, "us10y_20d_avg": None})
    
    return results


market_data = get_market_data()
```

---

### Cell 3: Nikkei and JPY from Yahoo Finance

```python
# yfinance gives us higher-frequency data than FRED
# Install: pip install yfinance (already available on Databricks ML Runtime)

import yfinance as yf

def get_yfinance_data():
    """
    Fetch Nikkei 225 and JPY/USD from Yahoo Finance.
    Complementary to FRED — yfinance gives intraday and more recent daily close.
    """
    results = {}
    
    try:
        # Nikkei 225
        nikkei = yf.Ticker("^N225")
        nikkei_hist = nikkei.history(period="30d", interval="1d")
        if not nikkei_hist.empty:
            nikkei_close = nikkei_hist["Close"].dropna()
            results["nikkei_current"] = float(nikkei_close.iloc[-1])
            results["nikkei_5d_return"] = float(nikkei_close.iloc[-1] / nikkei_close.iloc[-6] - 1)
            results["nikkei_20d_return"] = float(nikkei_close.iloc[-1] / nikkei_close.iloc[0] - 1)
            print(f"  Nikkei 225: {results['nikkei_current']:,.0f} | 5d: {results['nikkei_5d_return']:+.2%} | 20d: {results['nikkei_20d_return']:+.2%}")
        else:
            results.update({"nikkei_current": None, "nikkei_5d_return": 0, "nikkei_20d_return": 0})
    except Exception as e:
        print(f"  Nikkei fetch error: {e}")
        results.update({"nikkei_current": None, "nikkei_5d_return": 0, "nikkei_20d_return": 0})
    
    try:
        # JPY/USD from Yahoo Finance (more current than FRED)
        jpy = yf.Ticker("JPYUSD=X")
        jpy_hist = jpy.history(period="30d", interval="1d")
        if not jpy_hist.empty:
            jpy_close = jpy_hist["Close"].dropna()
            results["jpy_yf_current"] = float(jpy_close.iloc[-1])
            results["jpy_yf_5d_return"] = float(jpy_close.iloc[-1] / jpy_close.iloc[-6] - 1)  # + = JPY strengthening
            print(f"  JPY/USD (yfinance): {results['jpy_yf_current']:.4f} | 5d: {results['jpy_yf_5d_return']:+.2%}")
        else:
            results.update({"jpy_yf_current": None, "jpy_yf_5d_return": 0})
    except Exception as e:
        print(f"  JPY/USD fetch error: {e}")
        results.update({"jpy_yf_current": None, "jpy_yf_5d_return": 0})
    
    return results


yf_data = get_yfinance_data()

# Merge market data with yfinance data
# yfinance is more current; use it to overwrite FRED JPY if available
if yf_data.get("jpy_yf_current"):
    market_data["jpy_yf_5d_return"] = yf_data["jpy_yf_5d_return"]
    market_data["jpy_yf_current"] = yf_data["jpy_yf_current"]

if yf_data.get("nikkei_5d_return") is not None:
    market_data["nikkei_5d_return"] = yf_data["nikkei_5d_return"]
    market_data["nikkei_20d_return"] = yf_data["nikkei_20d_return"]
    market_data["nikkei_current"] = yf_data["nikkei_current"]
```

---

### Cell 4: BOJ Communication Signal (GDELT)

```python
# The BOJ communication signal catches hawkish language before rate moves.
# It is the earliest-possible leading indicator — often 5–10 days ahead of any market move.

BOJ_HAWKISH_KEYWORDS = {
    "rate hike": 2.0,
    "rate increase": 1.8,
    "BOJ tightening": 2.0,
    "bank of japan hike": 2.0,
    "ueda hawkish": 2.0,
    "yen carry unwind": 2.5,
    "carry trade unwind": 2.5,
    "yen appreciation": 1.5,
    "japan rate": 1.5,
    "boj normalization": 1.8,
    "hawkish boj": 2.0,
    "japan inflation target": 1.2,
    "boj governor": 1.0,
    "japan monetary tightening": 2.0,
    "boj meeting": 1.2,
    "japan yield curve control": 1.8,
    "ycc adjustment": 2.0,
}

BOJ_DOVISH_KEYWORDS = {
    "boj hold": -1.5,
    "bank of japan unchanged": -1.5,
    "japan rate cut": -1.8,
    "boj easing": -1.8,
    "yield curve control maintained": -1.5,
    "boj dovish": -1.8,
}

def query_gdelt_news(query_string, lookback_days=7, max_records=100):
    """Reuse from Pipeline 4 — identical GDELT query function."""
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=lookback_days)
    params = {
        "query": query_string,
        "mode": "artlist",
        "maxrecords": max_records,
        "startdatetime": start_date.strftime("%Y%m%d%H%M%S"),
        "enddatetime": end_date.strftime("%Y%m%d%H%M%S"),
        "format": "json",
        "sort": "DateDesc",
    }
    try:
        r = requests.get(GDELT_GKG_BASE, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("articles", [])
    except Exception as e:
        print(f"GDELT error: {e}")
        return []


def compute_boj_communication_score(lookback_days=7):
    """
    Detect BOJ hawkishness from GDELT news.
    
    Key signal: Ueda/Himino hawkish comments appear 5-10 days before a rate move.
    The media picks up hawkish signals from BOJ speeches; GDELT captures them within 24h.
    
    Returns score 1.0–5.0 where 5.0 = maximum hawkish pressure detected.
    """
    print("Computing BOJ communication score...")
    
    queries = [
        "Bank of Japan rate hike OR BOJ tightening OR Ueda hawkish",
        "yen carry trade unwind OR Japan interest rate increase 2026",
        "BOJ monetary policy normalization OR Japan yield curve adjustment"
    ]
    
    seen_urls = set()
    raw_hawkish = 0.0
    raw_dovish = 0.0
    total_articles = 0
    
    for query in queries:
        articles = query_gdelt_news(query, lookback_days=lookback_days, max_records=75)
        for article in articles:
            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            total_articles += 1
            
            headline = article.get("title", "").lower()
            for kw, weight in BOJ_HAWKISH_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_hawkish += weight
                    break
            for kw, weight in BOJ_DOVISH_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_dovish += abs(weight)
                    break
    
    net_signal = raw_hawkish - raw_dovish
    
    # Calibration: ~20 hawkish mentions/week = 3.0 (normal policy cycle chatter)
    # 60+ mentions = 4.5+ (pre-meeting surge, imminent hike signaling)
    if net_signal <= 0:
        boj_score = max(1.0, 2.0 + net_signal / 10)
    elif net_signal <= 20:
        boj_score = 2.0 + (net_signal / 20) * 1.0   # 2.0–3.0
    elif net_signal <= 50:
        boj_score = 3.0 + ((net_signal - 20) / 30) * 1.0  # 3.0–4.0
    elif net_signal <= 100:
        boj_score = 4.0 + ((net_signal - 50) / 50) * 0.8  # 4.0–4.8
    else:
        boj_score = 4.8 + min(0.2, (net_signal - 100) / 200)  # 4.8–5.0
    
    boj_score = min(5.0, max(1.0, boj_score))
    
    print(f"  Raw hawkish signal: {raw_hawkish:.1f}")
    print(f"  Raw dovish signal: {raw_dovish:.1f}")
    print(f"  Net signal: {net_signal:.1f}")
    print(f"  Total unique articles: {total_articles}")
    print(f"  BOJ COMMUNICATION SCORE: {boj_score:.2f}/5.0")
    
    return boj_score, {"raw_hawkish": raw_hawkish, "raw_dovish": raw_dovish,
                       "net_signal": net_signal, "total_articles": total_articles}


boj_score, boj_meta = compute_boj_communication_score(lookback_days=LOOKBACK_DAYS_GDELT)
```

---

### Cell 5: JPY Stress Score

```python
def compute_jpy_stress_score(market_data, yf_data):
    """
    Compute JPY/Nikkei-based carry stress score.
    
    The carry unwind signal has THREE components:
    1. JPY appreciation rate (faster = more stress)
    2. Nikkei decline (equity carry unwinding)
    3. MOVE Index elevation (systemic volatility = leveraged position stress)
    
    The dangerous confluence: JPY strengthening + Nikkei falling + MOVE rising
    All three moving together = active unwind phase.
    """
    print("Computing JPY stress score...")
    
    # Component 1: JPY appreciation
    # Use yfinance JPY/USD 5-day return if available, else FRED
    jpy_5d = yf_data.get("jpy_yf_5d_return") or market_data.get("jpy_appreciation_5d", 0)
    jpy_20d = market_data.get("jpy_appreciation_20d", 0)
    
    # Score JPY appreciation: 0% = 1.0, 1% 5-day = 2.5, 2% = 3.5, 3%+ = 5.0
    jpy_5d_pct = abs(max(0, jpy_5d))  # Only count appreciation (positive = JPY strengthening)
    if jpy_5d < 0:  # JPY weakening = no carry stress
        jpy_component = 1.0
    elif jpy_5d_pct < 0.005:
        jpy_component = 1.0 + jpy_5d_pct / 0.005 * 0.5  # 1.0–1.5
    elif jpy_5d_pct < 0.01:
        jpy_component = 1.5 + (jpy_5d_pct - 0.005) / 0.005 * 1.0  # 1.5–2.5
    elif jpy_5d_pct < 0.02:
        jpy_component = 2.5 + (jpy_5d_pct - 0.01) / 0.01 * 1.0  # 2.5–3.5
    elif jpy_5d_pct < 0.03:
        jpy_component = 3.5 + (jpy_5d_pct - 0.02) / 0.01 * 1.0  # 3.5–4.5
    else:
        jpy_component = min(5.0, 4.5 + (jpy_5d_pct - 0.03) / 0.02 * 0.5)  # 4.5–5.0
    
    # Component 2: Nikkei decline
    nikkei_5d = yf_data.get("nikkei_5d_return", 0) or 0
    nikkei_decline = abs(min(0, nikkei_5d))  # Only count declines
    
    if nikkei_decline < 0.01:
        nikkei_component = 1.0 + nikkei_decline / 0.01 * 0.5
    elif nikkei_decline < 0.03:
        nikkei_component = 1.5 + (nikkei_decline - 0.01) / 0.02 * 1.5
    elif nikkei_decline < 0.06:
        nikkei_component = 3.0 + (nikkei_decline - 0.03) / 0.03 * 1.5
    else:
        nikkei_component = min(5.0, 4.5 + (nikkei_decline - 0.06) / 0.07 * 0.5)
    
    # Component 3: MOVE Index elevation
    move_current = market_data.get("move_current")
    move_20d_avg = market_data.get("move_20d_avg")
    
    if move_current and move_20d_avg:
        move_ratio = move_current / move_20d_avg
        # MOVE historical calibration:
        # MOVE < 80 = low vol; 80-100 = normal; 100-120 = elevated; 120+ = stress; 140+ = crisis
        if move_current < 80:
            move_component = 1.0
        elif move_current < 100:
            move_component = 1.5 + (move_current - 80) / 20 * 1.0
        elif move_current < 120:
            move_component = 2.5 + (move_current - 100) / 20 * 1.0
        elif move_current < 140:
            move_component = 3.5 + (move_current - 120) / 20 * 1.0
        else:
            move_component = min(5.0, 4.5 + (move_current - 140) / 60 * 0.5)
        
        # Amplify if MOVE is rising (trend signal)
        move_trend = market_data.get("move_trend", 0)
        if move_trend > 0.10:   # MOVE up 10%+ from 20d avg
            move_component = min(5.0, move_component * 1.15)
    else:
        move_component = 2.5  # Default neutral if FRED unavailable
    
    # Confluence detector — dangerous when ALL THREE are elevated
    # Simple: multiply components vs. additive, to require co-movement
    low_threshold = 2.5
    confluence_bonus = 0.0
    if jpy_component >= low_threshold and nikkei_component >= low_threshold and move_component >= low_threshold:
        confluence_bonus = 0.5  # All three elevated simultaneously = structural signal
    
    # Weighted composite: JPY most important, then MOVE, then Nikkei
    jpy_stress = (
        jpy_component * 0.45 +
        move_component * 0.35 +
        nikkei_component * 0.20 +
        confluence_bonus
    )
    jpy_stress = min(5.0, max(1.0, jpy_stress))
    
    print(f"  JPY appreciation (5d): {jpy_5d:+.2%} → component: {jpy_component:.2f}")
    print(f"  Nikkei (5d): {nikkei_5d:+.2%} → component: {nikkei_component:.2f}")
    print(f"  MOVE Index: {move_current or 'N/A'} → component: {move_component:.2f}")
    print(f"  Confluence bonus: +{confluence_bonus:.2f}")
    print(f"  JPY STRESS SCORE: {jpy_stress:.2f}/5.0")
    
    return jpy_stress, {
        "jpy_5d_pct": jpy_5d,
        "nikkei_5d_return": nikkei_5d,
        "move_current": move_current,
        "jpy_component": jpy_component,
        "nikkei_component": nikkei_component,
        "move_component": move_component,
        "confluence_bonus": confluence_bonus
    }


jpy_stress, jpy_meta = compute_jpy_stress_score(market_data, yf_data)
```

---

### Cell 6: BOJ Rate Proximity Multiplier

```python
def compute_boj_rate_multiplier(boj_rate):
    """
    The BOJ rate proximity multiplier captures how close the current rate
    is to levels that historically trigger forced carry unwinds.
    
    The rate level matters because:
    - 0.0% to 0.50%: carry trade is comfortable — borrowing is nearly free
    - 0.50% to 0.75%: carry trade is under pressure — returns shrinking
    - 0.75% to 1.00%: carry trade is in the danger zone — significant positions close
    - 1.00%+: carry trade is structurally challenged — high unwind risk
    
    This multiplier scales UP the composite score when the rate is in the danger zone,
    because the same JPY appreciation event has much larger consequences at 1.0%
    than at 0.1% (fewer carry positions survive at 1.0%).
    """
    if boj_rate is None:
        print(f"  BOJ rate: unavailable — using neutral multiplier 1.0")
        return 1.0
    
    if boj_rate < 0.50:
        multiplier = 0.80    # Very low rates = carry is robust, less amplification
    elif boj_rate < 0.75:
        multiplier = 1.00    # Normal multiplier
    elif boj_rate < 1.00:
        multiplier = 1.15    # In the danger zone — amplify all signals
    elif boj_rate < 1.25:
        multiplier = 1.25    # High normalization — maximum amplification
    else:
        multiplier = 1.30    # Structural challenge to carry — every signal matters more
    
    print(f"  BOJ policy rate: {boj_rate:.2f}% → rate multiplier: {multiplier:.2f}x")
    return multiplier


boj_multiplier = compute_boj_rate_multiplier(market_data.get("boj_rate"))
```

---

### Cell 7: Composite Score and Phase Classification

```python
def compute_p2a_composite(jpy_stress, boj_score, boj_multiplier):
    """
    Compute the final Pipeline 2-A composite score (Signal 1 for GSI).
    
    Formula:
    - JPY stress (market signal): 60% weight
    - BOJ communication (news signal): 40% weight
    - BOJ rate multiplier: applied to final composite
    
    Phase classification maps score to actionable label.
    """
    raw_composite = (
        jpy_stress * 0.60 +
        boj_score * 0.40
    )
    
    # Apply rate multiplier — amplifies when BOJ is in the danger zone
    p2a_composite = min(5.0, max(1.0, raw_composite * boj_multiplier))
    
    # Phase classification
    if p2a_composite >= 4.5:
        phase = "ACTIVE_UNWIND"
        phase_note = "Multi-indicator confluence: forced position liquidation underway"
    elif p2a_composite >= 3.8:
        phase = "EARLY_UNWIND"
        phase_note = "Warning signals active: monitor hourly, prepare portfolio response"
    elif p2a_composite >= 3.0:
        phase = "POSITIONING"
        phase_note = "Carry trade stress building: review EWY, EM exposure"
    elif p2a_composite >= 2.0:
        phase = "WATCH"
        phase_note = "Normal monitoring: no portfolio action required"
    else:
        phase = "DORMANT"
        phase_note = "Carry trade stable: low yen carry risk"
    
    print("\n" + "="*65)
    print("PIPELINE 2-A: BOJ YEN CARRY UNWIND MONITOR")
    print("="*65)
    print(f"JPY Stress Score:         {jpy_stress:.2f}/5.0  (weight: 60%)")
    print(f"BOJ Communication Score:  {boj_score:.2f}/5.0  (weight: 40%)")
    print(f"BOJ Rate Multiplier:      {boj_multiplier:.2f}x")
    print(f"─────────────────────────────────────────────────────")
    print(f"P2-A COMPOSITE SCORE:     {p2a_composite:.2f}/5.0")
    print(f"CARRY UNWIND PHASE:       {phase}")
    print(f"                          {phase_note}")
    print("="*65)
    
    if p2a_composite >= ALERT_THRESHOLD:
        print(f"\n⚠  ALERT: Score {p2a_composite:.2f} exceeds threshold {ALERT_THRESHOLD}")
        print("   PORTFOLIO ACTION REQUIRED — see Phase response protocol below")
    
    return p2a_composite, phase, {
        "raw_composite": raw_composite,
        "boj_multiplier": boj_multiplier,
        "phase_note": phase_note
    }


p2a_composite, carry_phase, p2a_meta = compute_p2a_composite(
    jpy_stress, boj_score, boj_multiplier
)
```

---

### Cell 8: Phase Response Protocol

```python
def print_phase_response_protocol(carry_phase, p2a_composite, market_data, yf_data):
    """
    Print the specific portfolio actions keyed to the current phase.
    
    This is the "what do I do right now?" output that the CEO designed in Lesson 239.
    Each phase has a defined response — no interpretation required at execution time.
    """
    
    print("\n━━━ PHASE RESPONSE PROTOCOL ━━━")
    print(f"Current Phase: {carry_phase} | Score: {p2a_composite:.2f}/5.0")
    print()
    
    if carry_phase == "DORMANT":
        print("NO ACTION REQUIRED")
        print("  ✓ EWY / EM exposure: normal sizing acceptable")
        print("  ✓ Existing carry-sensitive positions: hold")
        print("  → Check again tomorrow (daily pipeline run)")
    
    elif carry_phase == "WATCH":
        print("HEIGHTENED AWARENESS — No immediate action")
        print("  → Review EWY position size against framework limits")
        print("  → Verify FRO/DHT tanker position is sized (Signal 2 hedge doubles as carry hedge)")
        print("  → Next threshold: if JPY appreciates another 0.5% in 3 sessions, expect POSITIONING")
        print("  → No portfolio changes yet")
    
    elif carry_phase == "POSITIONING":
        print("CARRY STRESS BUILDING — Review and trim")
        print("  ⚡ EWY: Begin systematic reduction if not already exited (CEO directive: EXIT)")
        print("  ⚡ INDA / EM broad: Review position sizes — trim to below 5% aggregate EM")
        print("  → KWEB: Hold (bifurcated signal — trade de-escalation partially offsets carry)")
        print("  → Gold: Consider 1-2% starter — gold often catches carry hedge demand")
        print("  → Energy: No change — Signal 2 (Iran) drives energy, not carry")
        print("  → Next threshold: if MOVE crosses 120, escalate to EARLY_UNWIND response")
    
    elif carry_phase == "EARLY_UNWIND":
        print("WARNING — PREPARE PORTFOLIO RESPONSE")
        print("  🔴 EWY: EXIT IMMEDIATELY if any residual position exists")
        print("  🔴 Any broad EM equity exposure: Reduce by 50% within 48 hours")
        print("  🔴 US equities: Reduce to minimum strategic allocation")
        print("  ⚡ VIX calls / UVXY: Consider 1% allocation as hedge on acceleration")
        print("  ⚡ USD/JPY short: Structural position — JPY appreciation benefits this")
        print("  → Send status to ceo@prospectra.earth within 24 hours")
        print("  → Next pipeline run: HOURLY (override daily schedule)")
    
    elif carry_phase == "ACTIVE_UNWIND":
        print("ACTIVE UNWIND — EXECUTE DEFENSIVE POSTURE IMMEDIATELY")
        print("  🚨 ALL EM equity: EXIT (Nikkei selloff will cascade to EM)")
        print("  🚨 EWY: Confirm exit executed")
        print("  🚨 Any leveraged or illiquid positions: Reduce to zero")
        print("  ✓ Hold: Gold (carry unwind = safety bid + USD pressure)")
        print("  ✓ Hold: FRO/DHT (volatility spike may create separate Iran risk spike)")
        print("  ✓ Hold: KWEB only if China diplomatic signal remains Level 2+")
        print("  → This is the August 5, 2024 scenario. Move fast.")
        print("  → CEO session: emergency review required")
    
    # Timeframe context
    boj_rate = market_data.get("boj_rate")
    if boj_rate:
        print(f"\n  BOJ Rate Context: {boj_rate:.2f}% (threshold: {BOJ_RATE_THRESHOLD}%)")
        if boj_rate >= BOJ_RATE_THRESHOLD:
            print(f"  ⚠  BOJ rate AT OR ABOVE threshold — all signals amplified")
        else:
            print(f"  → BOJ rate {BOJ_RATE_THRESHOLD - boj_rate:.2f}% below threshold — still building")
    
    print(f"\n  Next BOJ meeting: September 19, 2026 ({(datetime.date(2026, 9, 19) - datetime.date.today()).days} days)")
    print(f"  Pipeline 2-A must be live by: September 12, 2026")

print_phase_response_protocol(carry_phase, p2a_composite, market_data, yf_data)
```

---

### Cell 9: Write to Delta Table

```python
def write_p2a_to_delta(run_date, p2a_composite, carry_phase, jpy_stress, boj_score,
                        boj_multiplier, market_data, yf_data, boj_meta, jpy_meta, p2a_meta):
    """Write Pipeline 2-A output to Delta Lake table."""
    
    spark.sql("CREATE DATABASE IF NOT EXISTS geopolitics")
    spark.sql("""
        CREATE TABLE IF NOT EXISTS geopolitics.pipeline2a_scores (
            run_date DATE,
            run_timestamp TIMESTAMP,
            p2a_composite_score FLOAT,
            carry_unwind_phase STRING,
            jpy_stress_score FLOAT,
            boj_communication_score FLOAT,
            boj_rate_multiplier FLOAT,
            boj_rate_pct FLOAT,
            move_index_current FLOAT,
            jpy_5d_appreciation FLOAT,
            nikkei_5d_return FLOAT,
            boj_news_hawkish_signal FLOAT,
            boj_news_articles INT,
            confluence_bonus FLOAT,
            alert_triggered BOOLEAN,
            phase_note STRING
        )
        USING DELTA
        PARTITIONED BY (run_date)
    """)
    
    row = {
        "run_date": run_date.strftime("%Y-%m-%d"),
        "run_timestamp": datetime.datetime.utcnow().isoformat(),
        "p2a_composite_score": float(p2a_composite),
        "carry_unwind_phase": carry_phase,
        "jpy_stress_score": float(jpy_stress),
        "boj_communication_score": float(boj_score),
        "boj_rate_multiplier": float(boj_multiplier),
        "boj_rate_pct": float(market_data.get("boj_rate") or 0),
        "move_index_current": float(market_data.get("move_current") or 0),
        "jpy_5d_appreciation": float(jpy_meta.get("jpy_5d_pct") or 0),
        "nikkei_5d_return": float(jpy_meta.get("nikkei_5d_return") or 0),
        "boj_news_hawkish_signal": float(boj_meta.get("raw_hawkish") or 0),
        "boj_news_articles": int(boj_meta.get("total_articles") or 0),
        "confluence_bonus": float(jpy_meta.get("confluence_bonus") or 0),
        "alert_triggered": bool(p2a_composite >= ALERT_THRESHOLD),
        "phase_note": p2a_meta.get("phase_note", ""),
    }
    
    df = spark.createDataFrame([row])
    df.write.format("delta").mode("append").saveAsTable("geopolitics.pipeline2a_scores")
    
    print(f"\n✓ Written to Delta: geopolitics.pipeline2a_scores")
    print(f"  Date: {row['run_date']} | Phase: {carry_phase} | Score: {p2a_composite:.2f}")
    print(f"  Alert triggered: {row['alert_triggered']}")
    return row


today = datetime.date.today()
written_row = write_p2a_to_delta(
    run_date=today,
    p2a_composite=p2a_composite,
    carry_phase=carry_phase,
    jpy_stress=jpy_stress,
    boj_score=boj_score,
    boj_multiplier=boj_multiplier,
    market_data=market_data,
    yf_data=yf_data,
    boj_meta=boj_meta,
    jpy_meta=jpy_meta,
    p2a_meta=p2a_meta
)
```

---

### Cell 10: GSI v2.0 Integration

```python
# Insert Pipeline 2-A score into the GSI alongside Pipeline 4

def compute_gsi_v2_with_p2a(boj_p2a_score, iran_score, china_reset_score, p4_score):
    """
    GSI v2.0 — four-component composite.
    Now uses a live P2-A score for Signal 1.
    
    Weights:
    - Signal 1 (BOJ): 0.30
    - Signal 2 (Iran): 0.30
    - Signal 4 (Export Control): 0.25
    - Signal 3 (China reset, inverted): 0.15
    """
    china_stress = 6.0 - china_reset_score  # Invert: high de-escalation = low stress
    
    gsi = (
        boj_p2a_score   * 0.30 +
        iran_score      * 0.30 +
        p4_score        * 0.25 +
        china_stress    * 0.15
    )
    gsi = min(5.0, max(1.0, gsi))
    
    if gsi >= 4.5:
        gsi_regime = "CRITICAL — Multi-signal convergence"
    elif gsi >= 3.5:
        gsi_regime = "ELEVATED_TAIL_RISK"
    elif gsi >= 2.5:
        gsi_regime = "MODERATE — Watch mode"
    elif gsi >= 1.5:
        gsi_regime = "LOW — No structural stress"
    else:
        gsi_regime = "MINIMAL"
    
    return gsi, gsi_regime


# Use estimated scores for signals not yet live
# Replace these with Delta table reads once Pipelines 2-B and 3 are built
IRAN_SCORE_ESTIMATED = 3.5
CHINA_RESET_ESTIMATED = 3.8

# Use live Pipeline 4 score from Delta, or estimated if not available
try:
    p4_live_df = spark.sql("""
        SELECT p4_composite_score 
        FROM geopolitics.pipeline4_scores 
        ORDER BY run_timestamp DESC 
        LIMIT 1
    """)
    P4_SCORE = float(p4_live_df.collect()[0]["p4_composite_score"])
    print(f"Pipeline 4 score (LIVE from Delta): {P4_SCORE:.2f}")
except Exception as e:
    P4_SCORE = 3.9  # CEO estimated fallback
    print(f"Pipeline 4 score (ESTIMATED — run P4 to go live): {P4_SCORE:.2f}")

gsi_composite, gsi_regime = compute_gsi_v2_with_p2a(
    boj_p2a_score=p2a_composite,
    iran_score=IRAN_SCORE_ESTIMATED,
    china_reset_score=CHINA_RESET_ESTIMATED,
    p4_score=P4_SCORE
)

print("\n" + "="*65)
print("GSI v2.0 — FOUR-COMPONENT COMPOSITE (P2-A LIVE)")
print("="*65)
china_stress_val = 6.0 - CHINA_RESET_ESTIMATED
print(f"Signal 1 — BOJ (LIVE):      {p2a_composite:.2f} × 0.30 = {p2a_composite * 0.30:.2f}")
print(f"Signal 2 — Iran (est.):     {IRAN_SCORE_ESTIMATED:.2f} × 0.30 = {IRAN_SCORE_ESTIMATED * 0.30:.2f}")
print(f"Signal 4 — Export Ctrl:     {P4_SCORE:.2f} × 0.25 = {P4_SCORE * 0.25:.2f}")
print(f"Signal 3 — China reset:     {CHINA_RESET_ESTIMATED:.2f} → {china_stress_val:.2f} × 0.15 = {china_stress_val * 0.15:.2f}")
print(f"─────────────────────────────────────────────────────")
print(f"GSI v2.0 COMPOSITE:         {gsi_composite:.2f}/5.0")
print(f"PORTFOLIO REGIME:           {gsi_regime}")
print("="*65)
```

---

## What the Expected First Reading Should Show

The CEO's current judgmental estimate for Signal 1 (BOJ) is **3.8/5.0**, set in Lesson 243. When Pipeline 2-A first runs, here is what to expect:

| Market Condition (Aug 2026) | Expected Score | Interpretation |
|---|---|---|
| JPY stable, MOVE < 100, BOJ hawkish articles moderate | **3.2–3.6** | Below CEO estimate. Carry risk lower than assessed. |
| JPY appreciation < 1%, MOVE 100–115, hawkish chatter active | **3.6–4.1** | In line with CEO estimate. Calibrated. |
| JPY appreciation > 1.5%, MOVE > 115, pre-meeting surge in hawkish articles | **4.1–4.5** | Above CEO estimate. Carry stress building — BOJ hike closer than assumed. |
| JPY appreciating > 2%, MOVE > 125, Nikkei falling | **4.5+** | EARLY_UNWIND phase. Portfolio action required. |

The BOJ rate multiplier (currently 1.15–1.25 at the 1.0% rate level) means that the same JPY/MOVE combination produces higher scores now than it would have in 2024 when the rate was 0.25%. The multiplier is doing its job.

---

## Key Calibration Note — August 2026 Baseline

When Pipeline 2-A first runs, it creates the baseline. The August 2026 environment is characterized by:
- BOJ rate: approximately 1.0% (normalized, danger zone begins)
- JPY: volatile but not in active appreciation trend as of early August
- MOVE Index: moderately elevated (110–115 range) following Q1 2026 volatility
- BOJ communication: hawkish — multiple dissents in recent meeting, September meeting well-telegraphed

The expected first Pipeline 2-A reading: **3.6–4.0/5.0 | POSITIONING phase**

This is exactly the right calibration for a BOJ that is at 1.0% heading into a September meeting where another 25bps is possible.

---

## Databricks Angle — The Multi-Source Pipeline Design

Pipeline 4 was a GDELT-only pipeline. Pipeline 2-A introduces the multi-source pattern that will be standard for all future pipelines:

| Source | What It Provides | Why It's Necessary |
|---|---|---|
| FRED | MOVE Index, US 10Y yield, JPY/USD daily close | The quantitative market signal — no news-based proxy can replicate |
| Yahoo Finance (yfinance) | Nikkei daily close, intraday JPY | More current than FRED; available without API key |
| GDELT | BOJ communication sentiment | The leading indicator — catches hawkishness 5–10 days before market pricing |

**Key Databricks task after go-live:**

Create a composite monitoring dashboard notebook:
```sql
-- Compare Pipeline 2-A and Pipeline 4 scores on the same chart
SELECT 
    COALESCE(p2a.run_date, p4.run_date) AS date,
    p2a.p2a_composite_score AS signal_1_boj,
    p2a.carry_unwind_phase,
    p4.p4_composite_score AS signal_4_export,
    p4.bifurcation_index
FROM geopolitics.pipeline2a_scores p2a
FULL OUTER JOIN geopolitics.pipeline4_scores p4
    ON p2a.run_date = p4.run_date
ORDER BY date DESC
LIMIT 30;
```

This query becomes the live dashboard view for both active pipelines. When you see this query returning 30 days of dual-signal data in October 2026, the analytical platform will be producing genuinely novel signal.

**Dataset to register:** `geopolitics.pipeline2a_scores` (self-generated, begins on Pipeline 2-A go-live date)

---

## Key Concepts Summary

| Concept | Definition |
|---|---|
| **MOVE Index** | Merrill Lynch Option Volatility Estimate — implied volatility of US Treasuries. The single best early-warning indicator of global carry stress. Above 120 = systemic pressure on leveraged positions. |
| **Confluence detection** | The requirement that JPY appreciation, Nikkei decline, AND MOVE elevation occur simultaneously before declaring EARLY_UNWIND. Single-signal moves are noise; three-signal co-movement is a structural event. |
| **BOJ rate proximity multiplier** | The amplifier that makes identical JPY/MOVE movements more significant when the BOJ rate is at 1.0% than at 0.25%. Same input, bigger output, because carry positions are under more structural pressure. |
| **Phase classification** | The categorical label (DORMANT → WATCH → POSITIONING → EARLY_UNWIND → ACTIVE_UNWIND) that converts a continuous score into an actionable decision with a defined portfolio response. |
| **September 12 deadline** | One week before the September 19 BOJ meeting — the minimum lead time needed for Pipeline 2-A to produce reliable signal before the most consequential policy event of Q3 2026. |
| **Multi-source pipeline pattern** | The architecture introduced in Pipeline 2-A: FRED (quantitative) + Yahoo Finance (current pricing) + GDELT (news sentiment) feeding a weighted composite. Standard for all future pipelines. |

---

## Investment Implications

**Signal 1 and the portfolio as of August 13, 2026:**

The three portfolio actions from Lessons 241–245 remain outstanding. Signal 1 is directly relevant to all three:

**EWY (South Korea):** The POSITIONING phase trigger at 3.0 is the last warning before the CEO expects forced action. South Korea's equity market is one of the most carry-sensitive EM markets — its tech sector (Samsung, SK Hynix) is leveraged to global risk appetite, which collapses in a carry unwind. If Pipeline 2-A shows POSITIONING or above on first run, EWY must be exited regardless of any other signal.

**FRO/DHT (tanker position):** Uncorrelated to yen carry. In fact, tankers benefit from global volatility (risk premium on Hormuz route) while carry unwinds typically weaken EM currencies and reduce shipping volumes. FRO/DHT is the position that does NOT need to be re-evaluated based on Signal 1.

**KWEB (China tech):** The carry unwind complicates KWEB. Even with Signal 3 (trade normalization) at Level 2, a full carry unwind would temporarily hammer EM including Chinese equities. The KWEB starter position (1–2%) is designed for exactly this — small enough to survive a carry unwind, large enough to participate in Signal 3 Level 3 re-rating. The starter size is validated by Pipeline 2-A's output: if P2-A enters EARLY_UNWIND, KWEB starter holds but no add.

---

## Reflection Questions

**Question 1 — The MOVE Index as systemic proxy:**
The MOVE Index was designed to measure US Treasury volatility, not yen carry risk specifically. Yet it is the most reliable early warning signal for carry unwinds because leveraged carry positions unwind into safe havens (Treasuries), driving Treasury volatility up before the JPY/equity cascade is visible. Design a diagnostic test: how would you verify that MOVE is currently elevated *because of carry stress* rather than because of US-specific factors (e.g., a US debt ceiling crisis or surprise US inflation print)? What data would distinguish these two causes of elevated MOVE?

**Question 2 — Calibration without history:**
Pipeline 2-A's scoring thresholds (e.g., "JPY appreciation of 2% over 5 days = component score 3.5") were calibrated by the CEO from memory of the August 2024 carry unwind. After 30 days of live data, you will have 30 daily scores. How would you back-test the calibration? Specifically: the August 5, 2024 event should produce a score of 4.5+ (ACTIVE_UNWIND). Can you find the JPY/USD, MOVE, and Nikkei data from that period and check whether the Pipeline 2-A formula would have generated the correct phase label?

**Question 3 — Phase transition speed:**
The pipeline runs once daily at 6:00 UTC. But carry unwinds can escalate from POSITIONING to ACTIVE_UNWIND in 36 hours (as August 2024 showed — the Nikkei dropped 13% over two trading sessions). Should Pipeline 2-A switch to hourly running when the score crosses 3.5? Design the logic for an adaptive run schedule: what event or score threshold should trigger the switch from daily to hourly, and how would you implement this in Databricks Workflows?

---

## CEO Closing Note

Two deadlines are now on the board:

**August 15 (Saturday):** Pipeline 4 go-live. The code has been in your hands for 72 hours. The validation framework is in Lesson 245. There is nothing more the CEO can do to prepare you for this build — the only remaining task is to open Databricks and run it. When it runs, send the output to ceo@prospectra.earth. That single email unlocks the next phase of the engineering roadmap.

**September 12 (Friday):** Pipeline 2-A go-live. The complete code is in this document. The architecture is more complex than Pipeline 4 — it requires FRED API authentication, a yfinance install, and the multi-source merge logic in Cells 3–5. But the pattern is identical to what you just built. You have 30 days. The BOJ meets on September 19.

The sequence is clear. The code is written. The deadlines are set.

One build at a time. First Pipeline 4. Then Pipeline 2-A.

The CEO will be watching for the Pipeline 4 confirmation email.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session 246 | August 13, 2026 | Engineering Phase, Session 9*
*Pipeline 4 deadline: August 15, 2026 — 2 days*
*Pipeline 2-A deadline: September 12, 2026 — 30 days*
*Next session: Pipeline 4 confirmation review + Pipeline 2-A FRED API setup*

---

## Quick Reference: Pipeline 2-A Databricks Setup Checklist

```
PRE-BUILD (before coding):
□ Get FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html
□ Add to Databricks secrets: 
  dbutils.secrets.put(scope="prospectra", key="fred_api_key", string_value="YOUR_KEY")
□ Verify yfinance available: import yfinance as yf (installed on ML Runtime)
□ Create database: spark.sql("CREATE DATABASE IF NOT EXISTS geopolitics")

BUILD (use code above, cell by cell):
□ Cell 1 — FRED key loads, no error
□ Cell 2 — MOVE Index, JPY/USD, US10Y, BOJ rate all return values
□ Cell 3 — Nikkei and JPY/USD via yfinance (may show 0 returns if market closed)
□ Cell 4 — GDELT BOJ communication score: expect 2.5–3.5 in Aug 2026
□ Cell 5 — JPY stress score: expect 2.5–3.5 unless unwind active
□ Cell 6 — BOJ rate multiplier: expect 1.15–1.25 at current rate (~1.0%)
□ Cell 7 — P2-A composite printed, phase classified
□ Cell 8 — Phase response protocol printed (actionable)
□ Cell 9 — Delta write to geopolitics.pipeline2a_scores ✓
□ Cell 10 — GSI v2.0 with live Signal 1 printed

POST-BUILD:
□ Screenshot final output
□ Send score + phase to ceo@prospectra.earth
□ Schedule as Databricks Workflow (daily at 6:00 UTC)
□ Report Pipeline 4 confirmation and three portfolio action status in same email
```
