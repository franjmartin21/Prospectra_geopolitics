# Lesson 247: Pipeline 2-B Build Spec — Iran Nuclear Threshold Monitor, Complete Code
**Date:** 2026-08-13 (Thursday)
**Session Type:** Engineering Phase — Pipeline Build Sprint
**Curriculum Position:** 247 — Engineering Phase, Session 10
**Pipeline 4 Deadline:** August 15, 2026 — **2 days**
**Pipeline 2-A Deadline:** September 12, 2026 — 30 days
**Pipeline 2-B Deadline:** October 3, 2026 — 51 days

---

## CEO Opening Question

Pipeline 4 is two days from its deadline. Pipeline 2-A's complete code was delivered this morning.

Here is today's question — and it is not about either of those pipelines:

**If Iran crosses the nuclear threshold while Pipeline 2-B is still unbuilt, what will you actually see in your portfolio — and will you know why it's happening?**

The May 2026 Trump-Xi trade deal reduced one tail risk. The Iran nuclear escalation has not reduced. The IAEA's access to key Iranian facilities remains restricted. Enrichment to 60% HEU — two steps from weapons-grade — has not been rolled back. The BOJ carry unwind (Signal 1) is the financial-system risk. Iran going nuclear (Signal 2) is the geopolitical risk that could reprice crude, tankers, and regional equities overnight.

Pipeline 2-B cannot wait until October 3 to be *understood*. The code must be ready when Pipeline 2-A goes live — so that the moment Bolo finishes the September 12 Pipeline 2-A build, the next notebook to open is already written.

Today's lesson delivers the complete code for Pipeline 2-B. The build is 51 days away. The preparation starts now.

---

## Why Pipeline 2-B Is Structurally Different from Pipeline 2-A

Pipeline 2-A tracked a **market phenomenon** (the yen carry trade) using market data as its primary signal (JPY/USD, MOVE Index, Nikkei). News sentiment (BOJ communication via GDELT) was the leading indicator but not the core quantitative signal.

Pipeline 2-B monitors a **geopolitical threshold event** — the crossing of a technical nuclear milestone that has no price series attached to it. There is no "Iran nuclear enrichment futures contract." The signal must be reconstructed from:

1. **News sentiment** (GDELT) — the primary real-time signal, not the secondary one
2. **Crude oil price behavior** (FRED/Yahoo Finance) — the market's proxy for Hormuz risk
3. **Tanker rate proxies** (Yahoo Finance: FRO, DHT) — the shipping market's forward pricing of Hormuz disruption
4. **Regional defense equity signals** (RTX, LMT, Israel proxy) — the market's pricing of military response probability

This inverts the Pipeline 2-A architecture: news-first, market-confirmation. The distinction matters because:

- A BOJ rate hike is announced with scheduled meeting dates. There is time to position.
- An Iran nuclear crossing event has no calendar. It is detected in news, then priced.

**Pipeline 2-B must detect the news signal before the market prices it.** That is the alpha proposition.

The challenge: Iran nuclear news is noisy. Every month produces hundreds of articles about Iran's nuclear program. The pipeline must distinguish between:
- **Background noise:** Routine diplomatic commentary, expert op-eds, annual IAEA reports
- **Escalation signal:** IAEA access denial, specific centrifuge count disclosures, enrichment level updates
- **Threshold approach:** 90% HEU enrichment reports, IAEA emergency session convening, US-Israel military coordination
- **Trigger event:** Nuclear test detonation, official weapons capability declaration

Only the last two require immediate portfolio response. The first two are daily noise. The pipeline must separate them.

---

## Pipeline 2-B Architecture — Final Specification

```
PIPELINE 2-B: Iran Nuclear Threshold Monitor
Version: 1.0

INPUTS:
  1. GDELT — Iran nuclear / IAEA / enrichment / Hormuz news (primary signal)
  2. FRED API — Brent crude price (DCOILBRENTEU), 5-year break-even inflation
  3. Yahoo Finance (yfinance) — Brent futures (BZ=F), FRO (Frontline), DHT Holdings
  4. GDELT — US-Israel military coordination / Gulf security articles (threat context)
  5. GDELT — Iran diplomatic / JCPOA / de-escalation articles (counter-signal)

OUTPUTS:
  1. nuclear_threshold_score: float (1.0–5.0) — GDELT-derived technical escalation
  2. oil_stress_score: float (1.0–5.0) — crude/tanker market's Hormuz pricing
  3. military_signal_score: float (1.0–5.0) — US-Israel military posture indicator
  4. p2b_composite_score: float (1.0–5.0) — GSI-ready output (Signal 2)
  5. iran_risk_phase: string — "COLD" / "ESCALATING" / "THRESHOLD_APPROACH" / "CRISIS"

FREQUENCY: Daily (run at 6:30 UTC — 30 minutes after Pipeline 2-A)
DESTINATION: Delta table `geopolitics.pipeline2b_scores`
ALERT THRESHOLD: p2b_composite_score >= 4.0 → immediate email to Bolo
```

The `iran_risk_phase` label is the human-facing output. A score of 3.7 is an analyst's number; "THRESHOLD_APPROACH" is an operator's instruction. The phase classification removes the interpretation burden from the user at the moment it matters most.

---

## The Complete Code — Notebook Cell by Cell

### Cell 1: Setup and Configuration

```python
# Pipeline 2-B: Iran Nuclear Threshold Monitor
# Version 1.0 | Prospectra Geopolitics & Investment

import requests
import datetime
import json
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType, TimestampType

spark = SparkSession.builder.appName("Pipeline2B_IranNuclearMonitor").getOrCreate()

# ── Configuration ──────────────────────────────────────────────────────────────
FRED_API_KEY = dbutils.secrets.get(scope="prospectra", key="fred_api_key")
# Same API key as Pipeline 2-A — no new credentials needed

ALERT_THRESHOLD = 4.0        # Alert Bolo above this level (higher than P2-A — Iran events are rarer)
LOOKBACK_DAYS_GDELT = 7      # GDELT news window
LOOKBACK_DAYS_MARKET = 30    # Market data window for Brent trend

# Brent crude price thresholds (Hormuz premium proxy)
BRENT_BASELINE_USD = 78.0    # CEO-estimated Q3 2026 fundamental value (strip price)
BRENT_STRESS_THRESHOLD = 90  # Above this = Hormuz risk premium becoming significant
BRENT_CRISIS_THRESHOLD = 105 # Above this = market pricing significant disruption

GDELT_GKG_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"
FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

print("Pipeline 2-B initialized: Iran Nuclear Threshold Monitor")
print(f"Alert threshold: {ALERT_THRESHOLD}/5.0")
print(f"Brent baseline: ${BRENT_BASELINE_USD} | Stress: ${BRENT_STRESS_THRESHOLD} | Crisis: ${BRENT_CRISIS_THRESHOLD}")
print(f"GDELT lookback: {LOOKBACK_DAYS_GDELT} days | Market lookback: {LOOKBACK_DAYS_MARKET} days")
```

---

### Cell 2: Keyword Libraries — The Core of the Pipeline

```python
# ── Nuclear Escalation Keywords ────────────────────────────────────────────────
# Weighted by specificity and escalation significance
# Higher weight = rarer, more significant event

NUCLEAR_ESCALATION_KEYWORDS = {
    # Enrichment-specific (highest specificity — direct threshold indicators)
    "90% enriched": 3.0,
    "weapons-grade uranium": 3.0,
    "nuclear weapons capability": 3.0,
    "nuclear threshold": 2.8,
    "60% enriched": 2.5,
    "60 percent enriched": 2.5,
    "highly enriched uranium": 2.5,
    "heu production": 2.5,
    "breakout capacity": 2.5,
    "nuclear breakout": 2.8,
    "uranium enrichment level": 2.0,
    "advanced centrifuge": 2.0,
    "IR-6 centrifuge": 2.5,
    "IR-8 centrifuge": 2.5,
    "natanz enrichment": 2.2,
    "fordow enrichment": 2.2,
    
    # IAEA access (access denial = active concealment)
    "iaea access denied": 2.8,
    "iaea inspectors blocked": 2.8,
    "iaea monitoring lapse": 2.5,
    "iaea emergency session": 3.0,
    "iaea censure": 2.5,
    "iaea board of governors": 2.0,
    "nuclear non-proliferation treaty": 1.5,
    "npt withdrawal": 3.0,
    "safeguards agreement": 1.8,
    
    # Military / deterrence
    "iran nuclear strike": 3.0,
    "israel iran military": 2.5,
    "preemptive strike iran": 3.0,
    "military option iran": 2.5,
    "us iran military": 2.2,
    "fifth fleet iran": 2.5,
    "carrier strike group iran": 2.5,
    "hormuz blockade": 2.8,
    "hormuz closure": 3.0,
    "strait of hormuz threat": 2.5,
    
    # Sanctions / diplomatic breakdown
    "snapback sanctions iran": 2.0,
    "jcpoa collapse": 2.5,
    "nuclear talks breakdown": 2.0,
    "iran nuclear deal failed": 2.0,
    "iran nuclear deadline": 2.0,
    "iran nuclear ultimatum": 2.5,
}

# ── Nuclear De-Escalation Keywords ────────────────────────────────────────────
NUCLEAR_DEESCALATION_KEYWORDS = {
    "iran nuclear deal": -1.5,
    "jcpoa agreement": -1.8,
    "iran nuclear talks progress": -1.8,
    "iran nuclear agreement": -2.0,
    "iaea access restored": -2.5,
    "iran enrichment freeze": -2.5,
    "iran nuclear moratorium": -2.5,
    "iran nuclear concession": -1.8,
    "iran us talks nuclear": -1.5,
    "iran nuclear diplomacy": -1.2,
    "nuclear negotiations iran": -1.2,
}

# ── Hormuz / Gulf Security Keywords ───────────────────────────────────────────
# Secondary signal — captures physical risk to oil supply chain

HORMUZ_ESCALATION_KEYWORDS = {
    "hormuz closure": 3.0,
    "hormuz blockade": 2.8,
    "hormuz mine": 2.8,
    "tanker seizure iran": 2.5,
    "tanker attack": 2.2,
    "oil tanker iran": 1.8,
    "persian gulf military": 2.0,
    "gulf oil shipping": 1.5,
    "oil supply disruption iran": 2.0,
    "iran oil sanctions": 1.5,
    "iran oil embargo": 2.0,
}

print("Keyword libraries loaded:")
print(f"  Nuclear escalation: {len(NUCLEAR_ESCALATION_KEYWORDS)} keywords")
print(f"  Nuclear de-escalation: {len(NUCLEAR_DEESCALATION_KEYWORDS)} keywords")
print(f"  Hormuz/Gulf: {len(HORMUZ_ESCALATION_KEYWORDS)} keywords")
```

---

### Cell 3: GDELT Nuclear Threshold Score

```python
def query_gdelt_news(query_string, lookback_days=7, max_records=100):
    """Fetch articles from GDELT API — identical to Pipeline 2-A and 4."""
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


def compute_nuclear_threshold_score(lookback_days=7):
    """
    Detect Iran nuclear escalation from GDELT news.
    
    The Iran nuclear signal requires three GDELT query angles:
    1. Enrichment-specific (the hard technical signal)
    2. IAEA inspection/access (the institutional signal)
    3. Military/deterrence (the response probability signal)
    
    All three must be queried separately to capture different reporting patterns.
    URL deduplication prevents double-counting.
    
    Returns score 1.0–5.0 where:
    1.0–2.0 = COLD (background noise only)
    2.0–3.0 = LOW_ESCALATION (heightened diplomatic activity)
    3.0–3.8 = ESCALATING (technical indicators moving)
    3.8–4.5 = THRESHOLD_APPROACH (imminent milestone crossing)
    4.5–5.0 = CRISIS (threshold crossed / military action begun)
    """
    print("Computing nuclear threshold score (GDELT)...")
    
    # Three distinct query angles — maximizes coverage, URL dedup prevents inflation
    queries = [
        # Angle 1: Technical enrichment signal
        "Iran nuclear enrichment OR uranium enrichment level OR IAEA Iran OR centrifuge Iran",
        # Angle 2: IAEA access and institutional signal  
        "IAEA inspectors Iran OR Iran nuclear safeguards OR Iran JCPOA OR Iran nuclear breakout",
        # Angle 3: Military/deterrence and Hormuz
        "Iran nuclear strike OR hormuz blockade OR Iran Israel military OR Iran nuclear threshold",
    ]
    
    seen_urls = set()
    raw_escalation = 0.0
    raw_deescalation = 0.0
    raw_hormuz = 0.0
    total_articles = 0
    matched_high_weight = []  # Track high-significance matches for logging
    
    for query in queries:
        articles = query_gdelt_news(query, lookback_days=lookback_days, max_records=100)
        for article in articles:
            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            total_articles += 1
            
            headline = (article.get("title") or "").lower()
            
            # Score against escalation keywords
            for kw, weight in NUCLEAR_ESCALATION_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_escalation += weight
                    if weight >= 2.5:
                        matched_high_weight.append((kw, weight, article.get("title", "")))
                    break  # One match per article against escalation dict
            
            # Score against de-escalation keywords (separate pass)
            for kw, weight in NUCLEAR_DEESCALATION_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_deescalation += abs(weight)  # Store as positive, subtract later
                    break
            
            # Hormuz-specific (separate from nuclear count — different risk dimension)
            for kw, weight in HORMUZ_ESCALATION_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_hormuz += weight
                    break
    
    net_nuclear = raw_escalation - raw_deescalation
    
    # Calibration rationale:
    # Background Iran nuclear noise: ~15-30 weighted mentions/week = COLD baseline
    # Active negotiation phase: 30-60 mentions = LOW_ESCALATION (lots of diplomatic coverage)
    # Technical escalation (enrichment news): 60-120 mentions = ESCALATING
    # IAEA crisis / military coordination: 120-200 mentions = THRESHOLD_APPROACH
    # Active military strike / blockade declared: 200+ mentions = CRISIS
    
    if net_nuclear <= 10:
        nuke_base = max(1.0, 1.5 + net_nuclear / 20)         # 1.0–2.0
    elif net_nuclear <= 30:
        nuke_base = 2.0 + (net_nuclear - 10) / 20 * 1.0      # 2.0–3.0
    elif net_nuclear <= 80:
        nuke_base = 3.0 + (net_nuclear - 30) / 50 * 0.8      # 3.0–3.8
    elif net_nuclear <= 150:
        nuke_base = 3.8 + (net_nuclear - 80) / 70 * 0.7      # 3.8–4.5
    else:
        nuke_base = 4.5 + min(0.5, (net_nuclear - 150) / 200) # 4.5–5.0
    
    nuke_base = min(5.0, max(1.0, nuke_base))
    
    print(f"  Raw escalation signal: {raw_escalation:.1f}")
    print(f"  Raw de-escalation signal: {raw_deescalation:.1f}")
    print(f"  Net nuclear signal: {net_nuclear:.1f}")
    print(f"  Hormuz/Gulf signal: {raw_hormuz:.1f}")
    print(f"  Total unique articles: {total_articles}")
    print(f"  NUCLEAR THRESHOLD SCORE: {nuke_base:.2f}/5.0")
    
    if matched_high_weight:
        print(f"\n  HIGH-SIGNIFICANCE MATCHES ({len(matched_high_weight)}):")
        for kw, weight, title in matched_high_weight[:5]:
            print(f"    [{weight:.1f}] '{kw}' → {title[:80]}")
    
    return nuke_base, {
        "raw_escalation": raw_escalation,
        "raw_deescalation": raw_deescalation,
        "net_nuclear": net_nuclear,
        "raw_hormuz": raw_hormuz,
        "total_articles": total_articles,
        "high_significance_matches": len(matched_high_weight),
    }


nuclear_score, nuclear_meta = compute_nuclear_threshold_score(lookback_days=LOOKBACK_DAYS_GDELT)
```

---

### Cell 4: Oil Stress Score (Brent + Tanker Proxies)

```python
import yfinance as yf

def fetch_fred_series(series_id, lookback_days=60):
    """Fetch FRED time series — identical to Pipeline 2-A Cell 2."""
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
                continue
        return pd.DataFrame(rows).sort_values("date", ascending=False).reset_index(drop=True)
    except Exception as e:
        print(f"FRED fetch error for {series_id}: {e}")
        return pd.DataFrame(columns=["date", "value"])


def compute_oil_stress_score():
    """
    Compute oil market stress score as a proxy for Hormuz risk premium.
    
    Logic: Hormuz disruption risk is already being priced in crude oil futures.
    When the market anticipates disruption, Brent rises *relative to* its
    fundamental level (supply/demand driven baseline). We detect this premium.
    
    Three components:
    1. Brent price level vs. CEO-estimated baseline ($78 in Q3 2026)
    2. Brent 5-day trend (directional momentum — crisis events move fast)
    3. Tanker stock behavior (FRO/DHT rising = physical Hormuz risk being priced)
    
    Returns score 1.0–5.0 where 5.0 = maximum oil market Hormuz stress.
    """
    print("Computing oil stress score...")
    
    results = {}
    
    # Brent crude from FRED (daily data, 1-2 day lag)
    brent_df = fetch_fred_series("DCOILBRENTEU", lookback_days=LOOKBACK_DAYS_MARKET)
    
    if not brent_df.empty:
        brent_current = brent_df["value"].iloc[0]
        brent_5d_avg = brent_df["value"].head(5).mean()
        brent_20d_avg = brent_df["value"].head(20).mean()
        brent_5d_change = (brent_current / brent_5d_avg) - 1
        brent_baseline_premium = (brent_current / BRENT_BASELINE_USD) - 1
        results.update({
            "brent_current": brent_current,
            "brent_5d_avg": brent_5d_avg,
            "brent_5d_change": brent_5d_change,
            "brent_baseline_premium": brent_baseline_premium,
        })
        print(f"  Brent crude: ${brent_current:.2f} (5d avg: ${brent_5d_avg:.2f}, 5d change: {brent_5d_change:+.2%})")
        print(f"  Brent vs baseline (${BRENT_BASELINE_USD}): {brent_baseline_premium:+.2%}")
    else:
        results.update({
            "brent_current": BRENT_BASELINE_USD,
            "brent_5d_change": 0.0,
            "brent_baseline_premium": 0.0,
        })
    
    # Tanker stocks from Yahoo Finance (FRO = Frontline, DHT = DHT Holdings)
    tanker_signals = {}
    for ticker, name in [("FRO", "Frontline"), ("DHT", "DHT Holdings")]:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="30d", interval="1d")
            if not hist.empty:
                close = hist["Close"].dropna()
                tanker_signals[ticker] = {
                    "current": float(close.iloc[-1]),
                    "5d_return": float(close.iloc[-1] / close.iloc[-6] - 1),
                    "20d_return": float(close.iloc[-1] / close.iloc[0] - 1),
                }
                print(f"  {name} ({ticker}): ${tanker_signals[ticker]['current']:.2f} | 5d: {tanker_signals[ticker]['5d_return']:+.2%} | 20d: {tanker_signals[ticker]['20d_return']:+.2%}")
        except Exception as e:
            print(f"  {name} ({ticker}) fetch error: {e}")
            tanker_signals[ticker] = {"5d_return": 0.0, "20d_return": 0.0}
    
    # Component 1: Brent level vs. baseline
    brent_premium = results.get("brent_baseline_premium", 0)
    if brent_premium < 0:
        brent_component = max(1.0, 1.5 + brent_premium * 5)  # Discount if below baseline
    elif brent_premium < 0.05:
        brent_component = 1.5 + brent_premium / 0.05 * 0.5    # 1.5–2.0
    elif brent_premium < 0.10:
        brent_component = 2.0 + (brent_premium - 0.05) / 0.05 * 1.0  # 2.0–3.0
    elif brent_premium < 0.20:
        brent_component = 3.0 + (brent_premium - 0.10) / 0.10 * 1.0  # 3.0–4.0
    elif brent_premium < 0.35:
        brent_component = 4.0 + (brent_premium - 0.20) / 0.15 * 0.7  # 4.0–4.7
    else:
        brent_component = min(5.0, 4.7 + (brent_premium - 0.35) / 0.30 * 0.3)  # 4.7–5.0
    
    # Component 2: Brent 5-day trend (directional signal — fast-moving crisis proxy)
    brent_5d = results.get("brent_5d_change", 0)
    if brent_5d < 0:
        brent_trend_component = max(1.0, 1.5 + brent_5d * 10)
    elif brent_5d < 0.02:
        brent_trend_component = 1.5 + brent_5d / 0.02 * 0.5
    elif brent_5d < 0.05:
        brent_trend_component = 2.0 + (brent_5d - 0.02) / 0.03 * 1.0
    elif brent_5d < 0.10:
        brent_trend_component = 3.0 + (brent_5d - 0.05) / 0.05 * 1.0
    elif brent_5d < 0.15:
        brent_trend_component = 4.0 + (brent_5d - 0.10) / 0.05 * 0.8
    else:
        brent_trend_component = min(5.0, 4.8 + (brent_5d - 0.15) / 0.20 * 0.2)
    
    # Component 3: Tanker proxy signal
    # FRO/DHT rising RELATIVE to broader market = Hormuz risk being priced specifically
    fro_5d = tanker_signals.get("FRO", {}).get("5d_return", 0)
    dht_5d = tanker_signals.get("DHT", {}).get("5d_return", 0)
    avg_tanker_5d = (fro_5d + dht_5d) / 2
    
    if avg_tanker_5d < 0:
        tanker_component = max(1.0, 1.5 + avg_tanker_5d * 5)
    elif avg_tanker_5d < 0.02:
        tanker_component = 1.5 + avg_tanker_5d / 0.02 * 0.5
    elif avg_tanker_5d < 0.05:
        tanker_component = 2.0 + (avg_tanker_5d - 0.02) / 0.03 * 1.0
    elif avg_tanker_5d < 0.10:
        tanker_component = 3.0 + (avg_tanker_5d - 0.05) / 0.05 * 1.2
    elif avg_tanker_5d < 0.20:
        tanker_component = 4.2 + (avg_tanker_5d - 0.10) / 0.10 * 0.6
    else:
        tanker_component = min(5.0, 4.8 + (avg_tanker_5d - 0.20) / 0.30 * 0.2)
    
    # Confluence bonus: when Brent AND tankers both surge, that is specifically Hormuz
    # (vs. a generalized commodity spike from EM demand, which would hit Brent but not tankers selectively)
    confluence_bonus = 0.0
    if brent_component >= 3.0 and tanker_component >= 3.0:
        confluence_bonus = 0.4  # Brent + tanker co-move = Hormuz-specific pricing
    
    oil_stress = (
        brent_component        * 0.45 +
        brent_trend_component  * 0.30 +
        tanker_component       * 0.25 +
        confluence_bonus
    )
    oil_stress = min(5.0, max(1.0, oil_stress))
    
    print(f"\n  Brent level component: {brent_component:.2f}")
    print(f"  Brent trend component: {brent_trend_component:.2f}")
    print(f"  Tanker proxy component: {tanker_component:.2f} (FRO 5d: {fro_5d:+.2%}, DHT 5d: {dht_5d:+.2%})")
    print(f"  Confluence bonus: +{confluence_bonus:.2f}")
    print(f"  OIL STRESS SCORE: {oil_stress:.2f}/5.0")
    
    return oil_stress, {
        "brent_current": results.get("brent_current"),
        "brent_baseline_premium": brent_premium,
        "brent_5d_change": brent_5d,
        "brent_component": brent_component,
        "brent_trend_component": brent_trend_component,
        "tanker_component": tanker_component,
        "avg_tanker_5d": avg_tanker_5d,
        "confluence_bonus": confluence_bonus,
        "fro_5d": fro_5d,
        "dht_5d": dht_5d,
    }


oil_stress, oil_meta = compute_oil_stress_score()
```

---

### Cell 5: Military Signal Score (US-Israel Coordination)

```python
MILITARY_ESCALATION_KEYWORDS = {
    # Direct military posture signals
    "us carrier iran": 2.5,
    "b-52 iran": 3.0,
    "fifth fleet deployment": 2.5,
    "us military gulf": 2.0,
    "israel air force iran": 3.0,
    "idf iran strike": 3.0,
    "israel iran attack": 3.0,
    "us israel iran coordination": 2.8,
    "iran military threat": 2.0,
    "us iran confrontation": 2.5,
    "patriot missile iran": 2.5,
    "iron dome iran": 2.2,
    "us troops middle east": 1.8,
    "special operations iran": 2.0,
    "cyber attack iran": 2.0,  # Stuxnet-type operations
    
    # CENTCOM / Pentagon language
    "centcom iran": 2.5,
    "pentagon iran": 2.2,
    "secretary defense iran": 2.0,
    "military option iran": 2.5,
    "preventive strike": 2.8,
    
    # Regional proxy escalation
    "hezbollah iran missile": 2.2,
    "houthi attack oil": 2.0,
    "houthi shipping": 1.8,
    "red sea tanker": 1.8,
    "iran proxy attack": 2.2,
}

MILITARY_DEESCALATION_KEYWORDS = {
    "us iran talks": -1.5,
    "us iran diplomatic": -1.5,
    "iran nuclear negotiations": -1.5,
    "iran cease fire": -2.0,
    "iran truce": -1.8,
    "us iran prisoner swap": -1.2,  # Goodwill gesture
}

def compute_military_signal_score(lookback_days=7):
    """
    Detect US-Israel military coordination / posture toward Iran from GDELT.
    
    This score measures the *response probability* dimension of Iran nuclear risk.
    A nuclear-capable Iran is dangerous; a nuclear-capable Iran that has already
    drawn a declared military response is a crisis.
    
    The military signal is the last early-warning before the market prices the 
    strike probability. At 4.0+, options markets price tail risk; equities gap down.
    At 4.5+, the event is in process.
    
    Returns score 1.0–5.0 where 5.0 = active military operation confirmed.
    """
    print("Computing military signal score (GDELT)...")
    
    queries = [
        "US Israel Iran military coordination OR Pentagon Iran OR CENTCOM Iran",
        "Israel Iran attack OR IDF Iran OR preemptive strike nuclear",
        "Houthi tanker attack OR red sea shipping attack OR Iran proxy Gulf",
    ]
    
    seen_urls = set()
    raw_military = 0.0
    raw_deescalation = 0.0
    total_articles = 0
    
    for query in queries:
        articles = query_gdelt_news(query, lookback_days=lookback_days, max_records=75)
        for article in articles:
            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            total_articles += 1
            
            headline = (article.get("title") or "").lower()
            for kw, weight in MILITARY_ESCALATION_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_military += weight
                    break
            for kw, weight in MILITARY_DEESCALATION_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_deescalation += abs(weight)
                    break
    
    net_military = raw_military - raw_deescalation
    
    # Calibration: US always maintains some military posture in the Gulf
    # Background military news: 10-25 weighted mentions/week = baseline (~1.5)
    # Elevated exercises/deployments: 25-60 = moderate (2.0–3.0)
    # Specific strike warnings / carrier surge: 60-120 = high (3.0–4.0)
    # Active operation news: 120+ = crisis (4.0–5.0)
    
    if net_military <= 5:
        mil_score = max(1.0, 1.2 + net_military / 10)
    elif net_military <= 25:
        mil_score = 1.5 + (net_military - 5) / 20 * 1.0       # 1.5–2.5
    elif net_military <= 60:
        mil_score = 2.5 + (net_military - 25) / 35 * 1.0      # 2.5–3.5
    elif net_military <= 120:
        mil_score = 3.5 + (net_military - 60) / 60 * 0.8      # 3.5–4.3
    else:
        mil_score = 4.3 + min(0.7, (net_military - 120) / 80) # 4.3–5.0
    
    mil_score = min(5.0, max(1.0, mil_score))
    
    print(f"  Raw military signal: {raw_military:.1f}")
    print(f"  Raw de-escalation: {raw_deescalation:.1f}")
    print(f"  Net military signal: {net_military:.1f}")
    print(f"  Total unique articles: {total_articles}")
    print(f"  MILITARY SIGNAL SCORE: {mil_score:.2f}/5.0")
    
    return mil_score, {
        "raw_military": raw_military,
        "raw_deescalation": raw_deescalation,
        "net_military": net_military,
        "total_articles": total_articles,
    }


military_score, military_meta = compute_military_signal_score(lookback_days=LOOKBACK_DAYS_GDELT)
```

---

### Cell 6: Composite Score and Phase Classification

```python
def compute_p2b_composite(nuclear_score, oil_stress, military_score):
    """
    Compute the final Pipeline 2-B composite score (Signal 2 for GSI).
    
    Formula:
    - Nuclear threshold score (GDELT technical): 50% weight — the primary signal
    - Oil stress score (Brent + tankers): 30% weight — market confirmation
    - Military signal score (US-Israel posture): 20% weight — response probability
    
    The nuclear score dominates because it is the early-warning indicator.
    Oil and military move later (they are confirming signals, not leading).
    
    Phase classification:
    COLD:               1.0–2.0 — Iran nuclear risk is background noise
    ESCALATING:         2.0–3.0 — Diplomatic or technical escalation underway
    THRESHOLD_APPROACH: 3.0–4.0 — Technical milestone crossing plausible within 90 days
    CRISIS:             4.0–5.0 — Threshold crossed or military operation active
    """
    raw_composite = (
        nuclear_score  * 0.50 +
        oil_stress     * 0.30 +
        military_score * 0.20
    )
    
    p2b_composite = min(5.0, max(1.0, raw_composite))
    
    # Phase classification
    if p2b_composite >= 4.0:
        phase = "CRISIS"
        phase_note = "Iran nuclear threshold crossed or military operation active — immediate portfolio response"
    elif p2b_composite >= 3.0:
        phase = "THRESHOLD_APPROACH"
        phase_note = "Technical escalation building: FRO/DHT hedge validates, Brent target $95+"
    elif p2b_composite >= 2.0:
        phase = "ESCALATING"
        phase_note = "Elevated Iran risk: existing FRO/DHT position justified, no action required"
    else:
        phase = "COLD"
        phase_note = "Iran nuclear risk dormant: baseline monitoring only"
    
    print("\n" + "="*65)
    print("PIPELINE 2-B: IRAN NUCLEAR THRESHOLD MONITOR")
    print("="*65)
    print(f"Nuclear Threshold Score:  {nuclear_score:.2f}/5.0  (weight: 50%)")
    print(f"Oil Stress Score:         {oil_stress:.2f}/5.0  (weight: 30%)")
    print(f"Military Signal Score:    {military_score:.2f}/5.0  (weight: 20%)")
    print(f"─────────────────────────────────────────────────────")
    print(f"P2-B COMPOSITE SCORE:     {p2b_composite:.2f}/5.0")
    print(f"IRAN RISK PHASE:          {phase}")
    print(f"                          {phase_note}")
    print("="*65)
    
    if p2b_composite >= ALERT_THRESHOLD:
        print(f"\n⚠  ALERT: Score {p2b_composite:.2f} exceeds threshold {ALERT_THRESHOLD}")
        print("   PORTFOLIO ACTION REQUIRED — see Phase response protocol below")
    
    return p2b_composite, phase, {
        "raw_composite": raw_composite,
        "phase_note": phase_note,
    }


p2b_composite, iran_phase, p2b_meta = compute_p2b_composite(
    nuclear_score, oil_stress, military_score
)
```

---

### Cell 7: Phase Response Protocol

```python
def print_iran_phase_protocol(iran_phase, p2b_composite, oil_meta):
    """
    Print specific portfolio actions keyed to the current Iran risk phase.
    
    Portfolio positions that interact with Signal 2:
    - FRO/DHT (tanker position): Signal 2 is the primary thesis for this position
    - EWY (South Korea): Unrelated to Iran but mentioned for holistic view
    - Gold: Iran CRISIS phase creates dual safety bid (nuclear + oil shock)
    - Brent/oil: Long crude is the most direct Iran hedge, but we are equity-focused
    """
    
    brent_current = oil_meta.get("brent_current", BRENT_BASELINE_USD)
    
    print("\n━━━ PHASE RESPONSE PROTOCOL ━━━")
    print(f"Current Phase: {iran_phase} | Score: {p2b_composite:.2f}/5.0")
    print(f"Brent Crude: ${brent_current:.2f}")
    print()
    
    if iran_phase == "COLD":
        print("NO ACTION REQUIRED")
        print("  ✓ FRO/DHT: Not yet warranted on Signal 2 alone")
        print("    (If carried from prior directive, starter size is acceptable)")
        print("  ✓ Gold: No Iran-specific bid expected")
        print("  → Check again tomorrow (daily pipeline run)")
    
    elif iran_phase == "ESCALATING":
        print("ELEVATED AWARENESS — FRO/DHT starter validated")
        print("  ✓ FRO/DHT: Maintain starter position (1–2%) — thesis intact")
        print("    Pipeline confirms: Hormuz risk premium is live but not extreme")
        print("  ✓ Gold: No add — oil shock phase not triggered")
        print("  → Watch nuclear score specifically: if nuclear_score > 3.5, expect THRESHOLD_APPROACH next")
        print("  → No new position actions required this phase")
    
    elif iran_phase == "THRESHOLD_APPROACH":
        print("THRESHOLD APPROACH — Size up Iran hedge, add Brent proxy")
        print("  ⚡ FRO/DHT: Size up to 3–4% aggregate if currently at 1–2%")
        print("    (Tanker VLCC rates will spike before Brent fully reprices Hormuz)")
        print("  ⚡ Gold: Add 1–2% — dual function as nuclear tail hedge and oil-shock hedge")
        print(f"  ⚡ Brent proxy: If Brent < $90 and threshold phase holds, oil ETF starter (1%)")
        print("  → EWY: Confirm exit (unrelated, but carry unwind and Iran can co-occur)")
        print("  → KWEB: Hold starter — China-related, not Iran-related")
        print("  → Next threshold: military_score > 3.8 triggers CRISIS protocol review")
    
    elif iran_phase == "CRISIS":
        print("CRISIS — EXECUTE DEFENSIVE POSTURE AND MAXIMUM IRAN HEDGE")
        print("  🚨 FRO/DHT: Size to maximum allocation (4–6%) — VLCC rates will 3–5x")
        print(f"     Brent at ${brent_current:.0f}. In Hormuz disruption scenario: $110–130 target.")
        print("  🚨 Gold: 4–6% allocation — nuclear shock + safe haven bid + USD pressure")
        print("  🚨 ALL risk assets: Reduce to strategic minimum")
        print("  ✓ KWEB: Reduce — even trade normalization can't survive a Gulf war")
        print("  → CEO emergency session required immediately")
        print("  → EWY: Confirm exited (critical — Korea is a secondary casualty of Gulf crisis)")
        print("  → This is the August 5, 2024 scenario mapped onto Iran. Move fast.")
    
    # Context note
    print(f"\n  CEO-estimated baseline nuclear score: 3.5/5.0 (set Lesson 241)")
    print(f"  Current pipeline-derived nuclear score: {nuclear_score:.2f}/5.0")
    if nuclear_score > 3.5:
        print(f"  ⚠  Pipeline score ABOVE CEO estimate — Iran risk more elevated than previously assessed")
    elif nuclear_score < 3.0:
        print(f"  ↓  Pipeline score BELOW CEO estimate — recalibrate or verify keyword matching")
    else:
        print(f"  ✓  Pipeline score in line with CEO estimate — calibration confirmed")


print_iran_phase_protocol(iran_phase, p2b_composite, oil_meta)
```

---

### Cell 8: Write to Delta Table

```python
def write_p2b_to_delta(run_date, p2b_composite, iran_phase, nuclear_score,
                        oil_stress, military_score, oil_meta, nuclear_meta,
                        military_meta, p2b_meta):
    """Write Pipeline 2-B output to Delta Lake table."""
    
    spark.sql("CREATE DATABASE IF NOT EXISTS geopolitics")
    spark.sql("""
        CREATE TABLE IF NOT EXISTS geopolitics.pipeline2b_scores (
            run_date DATE,
            run_timestamp TIMESTAMP,
            p2b_composite_score FLOAT,
            iran_risk_phase STRING,
            nuclear_threshold_score FLOAT,
            oil_stress_score FLOAT,
            military_signal_score FLOAT,
            brent_current_usd FLOAT,
            brent_5d_change FLOAT,
            brent_baseline_premium FLOAT,
            tanker_proxy_5d_avg FLOAT,
            fro_5d_return FLOAT,
            dht_5d_return FLOAT,
            nuclear_raw_escalation FLOAT,
            nuclear_net_signal FLOAT,
            nuclear_high_significance_matches INT,
            military_net_signal FLOAT,
            hormuz_raw_signal FLOAT,
            alert_triggered BOOLEAN,
            phase_note STRING
        )
        USING DELTA
        PARTITIONED BY (run_date)
    """)
    
    row = {
        "run_date": run_date.strftime("%Y-%m-%d"),
        "run_timestamp": datetime.datetime.utcnow().isoformat(),
        "p2b_composite_score": float(p2b_composite),
        "iran_risk_phase": iran_phase,
        "nuclear_threshold_score": float(nuclear_score),
        "oil_stress_score": float(oil_stress),
        "military_signal_score": float(military_score),
        "brent_current_usd": float(oil_meta.get("brent_current") or BRENT_BASELINE_USD),
        "brent_5d_change": float(oil_meta.get("brent_5d_change") or 0),
        "brent_baseline_premium": float(oil_meta.get("brent_baseline_premium") or 0),
        "tanker_proxy_5d_avg": float(oil_meta.get("avg_tanker_5d") or 0),
        "fro_5d_return": float(oil_meta.get("fro_5d") or 0),
        "dht_5d_return": float(oil_meta.get("dht_5d") or 0),
        "nuclear_raw_escalation": float(nuclear_meta.get("raw_escalation") or 0),
        "nuclear_net_signal": float(nuclear_meta.get("net_nuclear") or 0),
        "nuclear_high_significance_matches": int(nuclear_meta.get("high_significance_matches") or 0),
        "military_net_signal": float(military_meta.get("net_military") or 0),
        "hormuz_raw_signal": float(nuclear_meta.get("raw_hormuz") or 0),
        "alert_triggered": bool(p2b_composite >= ALERT_THRESHOLD),
        "phase_note": p2b_meta.get("phase_note", ""),
    }
    
    df = spark.createDataFrame([row])
    df.write.format("delta").mode("append").saveAsTable("geopolitics.pipeline2b_scores")
    
    print(f"\n✓ Written to Delta: geopolitics.pipeline2b_scores")
    print(f"  Date: {row['run_date']} | Phase: {iran_phase} | Score: {p2b_composite:.2f}")
    print(f"  Alert triggered: {row['alert_triggered']}")
    return row


today = datetime.date.today()
written_row = write_p2b_to_delta(
    run_date=today,
    p2b_composite=p2b_composite,
    iran_phase=iran_phase,
    nuclear_score=nuclear_score,
    oil_stress=oil_stress,
    military_score=military_score,
    oil_meta=oil_meta,
    nuclear_meta=nuclear_meta,
    military_meta=military_meta,
    p2b_meta=p2b_meta
)
```

---

### Cell 9: GSI v2.1 Integration (Signal 2 Live)

```python
def compute_gsi_v21_with_p2b(boj_score_input, iran_p2b_score, china_reset_score, p4_score):
    """
    GSI v2.1 — four-component composite with live Signal 2.
    
    When Pipeline 2-B goes live, Signal 2 transitions from CEO estimate to data.
    Version bumped from v2.0 (P2-A live) to v2.1 (P2-B live).
    
    Weights unchanged from v2.0:
    - Signal 1 (BOJ): 0.30
    - Signal 2 (Iran): 0.30
    - Signal 4 (Export Control): 0.25
    - Signal 3 (China reset, inverted): 0.15
    """
    china_stress = 6.0 - china_reset_score  # Invert: high de-escalation = low stress
    
    gsi = (
        boj_score_input  * 0.30 +
        iran_p2b_score   * 0.30 +
        p4_score         * 0.25 +
        china_stress     * 0.15
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


# Read live pipeline scores from Delta where available
# Replace estimated scores once pipelines go live

try:
    p2a_df = spark.sql("""
        SELECT p2a_composite_score 
        FROM geopolitics.pipeline2a_scores 
        ORDER BY run_timestamp DESC LIMIT 1
    """)
    BOJ_SCORE = float(p2a_df.collect()[0]["p2a_composite_score"])
    print(f"Signal 1 — BOJ (LIVE from P2-A): {BOJ_SCORE:.2f}")
except Exception:
    BOJ_SCORE = 3.8  # CEO estimate fallback
    print(f"Signal 1 — BOJ (ESTIMATED): {BOJ_SCORE:.2f}")

try:
    p4_df = spark.sql("""
        SELECT p4_composite_score 
        FROM geopolitics.pipeline4_scores 
        ORDER BY run_timestamp DESC LIMIT 1
    """)
    P4_SCORE = float(p4_df.collect()[0]["p4_composite_score"])
    print(f"Signal 4 — Export Control (LIVE from P4): {P4_SCORE:.2f}")
except Exception:
    P4_SCORE = 3.9  # CEO estimate fallback
    print(f"Signal 4 — Export Control (ESTIMATED): {P4_SCORE:.2f}")

CHINA_RESET_ESTIMATED = 3.8  # Pipeline 3 not yet live (October 31 deadline)

gsi_composite, gsi_regime = compute_gsi_v21_with_p2b(
    boj_score_input=BOJ_SCORE,
    iran_p2b_score=p2b_composite,
    china_reset_score=CHINA_RESET_ESTIMATED,
    p4_score=P4_SCORE
)

china_stress_val = 6.0 - CHINA_RESET_ESTIMATED
print("\n" + "="*65)
print("GSI v2.1 — FOUR-COMPONENT COMPOSITE (P2-B LIVE)")
print("="*65)
print(f"Signal 1 — BOJ:             {BOJ_SCORE:.2f} × 0.30 = {BOJ_SCORE * 0.30:.2f}")
print(f"Signal 2 — Iran (LIVE):     {p2b_composite:.2f} × 0.30 = {p2b_composite * 0.30:.2f}")
print(f"Signal 4 — Export Ctrl:     {P4_SCORE:.2f} × 0.25 = {P4_SCORE * 0.25:.2f}")
print(f"Signal 3 — China reset:     {CHINA_RESET_ESTIMATED:.2f} → {china_stress_val:.2f} × 0.15 = {china_stress_val * 0.15:.2f}")
print(f"─────────────────────────────────────────────────────")
print(f"GSI v2.1 COMPOSITE:         {gsi_composite:.2f}/5.0")
print(f"PORTFOLIO REGIME:           {gsi_regime}")
print("="*65)
```

---

### Cell 10: Cross-Pipeline Monitoring Dashboard Query

```python
# When all four pipelines are live, this SQL becomes the daily monitoring view.
# Currently: P4 live (August 15), P2-A live (September 12), P2-B live (October 3).
# Run this after Pipeline 2-B goes live to see the three-signal time series.

DASHBOARD_QUERY = """
SELECT 
    COALESCE(p2a.run_date, p2b.run_date, p4.run_date) AS date,
    
    -- Signal 1: BOJ (Pipeline 2-A)
    p2a.p2a_composite_score AS signal_1_boj,
    p2a.carry_unwind_phase  AS boj_phase,
    
    -- Signal 2: Iran (Pipeline 2-B)
    p2b.p2b_composite_score AS signal_2_iran,
    p2b.iran_risk_phase     AS iran_phase,
    p2b.brent_current_usd   AS brent_usd,
    
    -- Signal 4: Export Control (Pipeline 4)
    p4.p4_composite_score   AS signal_4_export,
    p4.bifurcation_index    AS export_bifurcation,
    
    -- Portfolio regime (estimated until GSI v3.0 with P3 live)
    ROUND(
        COALESCE(p2a.p2a_composite_score, 3.8) * 0.30 +
        COALESCE(p2b.p2b_composite_score, 3.5) * 0.30 +
        COALESCE(p4.p4_composite_score,   3.9) * 0.25 +
        (6.0 - 3.8) * 0.15,  -- Signal 3 estimated
    2) AS gsi_composite

FROM geopolitics.pipeline2a_scores p2a
FULL OUTER JOIN geopolitics.pipeline2b_scores p2b
    ON p2a.run_date = p2b.run_date
FULL OUTER JOIN geopolitics.pipeline4_scores p4
    ON COALESCE(p2a.run_date, p2b.run_date) = p4.run_date
ORDER BY date DESC
LIMIT 30;
"""

print("Three-pipeline monitoring query ready.")
print("Run this after October 3 when Pipeline 2-B goes live:")
print()
print(DASHBOARD_QUERY)
```

---

## What the Expected First Reading Should Show

The CEO's current judgmental estimate for Signal 2 (Iran) is **3.5/5.0**, set in Lesson 241. The environment as of August 2026:

| Market Condition (Aug 2026) | Expected Score | Interpretation |
|---|---|---|
| GDELT nuclear chatter moderate, Brent near baseline, no military surge | **2.8–3.4** | Below CEO estimate. Iran risk lower than assessed. Recalibrate. |
| Nuclear articles active, Brent at $82–88, IAEA friction visible | **3.3–3.8** | In line with CEO estimate. ESCALATING / low THRESHOLD_APPROACH. |
| IAEA access restriction news, Brent $88–95, tankers surging | **3.8–4.2** | Above CEO estimate. THRESHOLD_APPROACH. FRO/DHT sizing up warranted. |
| Enrichment-level announcement, Brent > $95, military coordination confirmed | **4.2–4.8** | CRISIS phase. Immediate portfolio action. |

**CEO expected first Pipeline 2-B reading: 3.3–3.8 | ESCALATING to THRESHOLD_APPROACH**

This range is consistent with the August 2026 environment: the IAEA is operating with restricted access, enrichment has not been rolled back from 60%, and the BOJ carry risk context means a simultaneous Iran trigger would produce an especially disorderly market response.

---

## Signal Independence — Why Both Pipelines Matter Simultaneously

The most important architectural principle of the GSI is that **Signal 1 (BOJ) and Signal 2 (Iran) are independent risk factors** that can co-occur.

The August 2024 carry unwind produced a 13% Nikkei drawdown and a 5% US equity drawdown — driven entirely by financial mechanics, with no geopolitical trigger. That event resolved in 7 trading days.

An Iran nuclear threshold crossing combined with an active carry unwind would produce:
- JPY appreciation (carry unwind) → EM equity selloff (Signal 1 cascade)
- Brent spike to $100+ (Hormuz risk premium) → energy inflation resurgence (Signal 2 cascade)
- US equity drawdown from BOTH directions: financial risk (carry) AND energy shock (Iran)
- Timeline: 30–90 days of sustained pressure, not a 7-day resolution

**Portfolio note for a dual-signal event:**

| Position | Single Signal 1 | Single Signal 2 | Both Simultaneously |
|---|---|---|---|
| EWY | Exit (Signal 1 directive) | No change | Exit urgently |
| FRO/DHT | Hold (uncorrelated) | Size up | Size up aggressively — both signals bullish |
| KWEB | Hold starter | Hold starter | Reduce — EM cannot survive dual shock |
| Gold | No add | Add 1–2% | Add 4–6% — dual safe haven demand |
| Brent proxy | No add | Add small | Add — $100+ becomes credible |

This is not a scenario the CEO is forecasting as the base case. But the GSI architecture is designed specifically to detect its approach. When Pipeline 2-A score > 3.8 AND Pipeline 2-B score > 3.8 simultaneously — that is the scenario the analytical system was built to catch.

---

## Databricks Angle — The Tanker Proxy Pattern

Pipeline 2-B introduces a data pattern not present in Pipeline 2-A: **using equity prices as geopolitical proxies**.

FRO and DHT are not tracked because the CEO wants to monitor the portfolio positions in real-time. They are tracked because tanker VLCC rates are highly correlated with Hormuz disruption risk — and VLCC rate data requires a paid Bloomberg subscription, while FRO/DHT stock prices are free via yfinance.

This is a **proxy construction principle** applicable across the entire Databricks project:

| Expensive/inaccessible data | Free equity proxy |
|---|---|
| VLCC tanker spot rates | FRO, DHT stock price |
| Baltic Dry Index daily | BDRY ETF (Breakwave Dry Bulk Shipping) |
| Copper physical LME spot | COPX (copper miners ETF) |
| Iron ore futures | BHP, RIO ADR prices |
| EM credit spreads | EMB vs. IEF spread |

**Databricks task after Pipeline 2-B goes live:**

Extend the pipeline to track COPX and BHP/RIO as China demand proxies for Signal 3 (US-China reset). When Signal 3 shows de-escalation (trade normalization), copper miners should be the first equities to re-rate. The correlation between GDELT US-China trade sentiment and COPX forward returns is a testable hypothesis the platform can run with 90 days of data.

```python
# Add to Pipeline 3 (US-China Diplomatic Reset Monitor):
china_proxies = {
    "COPX": "Global X Copper Miners ETF",    # China construction demand proxy
    "MCHI": "iShares MSCI China ETF",         # Direct China equity proxy  
    "KWEB": "KraneShares CSI China Internet", # Already in portfolio
    "BHP":  "BHP Group ADR",                  # Iron ore demand proxy
}
# Correlation: weekly GDELT US-China diplomatic sentiment → COPX forward 5-day return
# H0: trade normalization news → COPX outperforms within 5 days
```

**Dataset to register:** `geopolitics.pipeline2b_scores` (self-generated, begins on go-live date)

---

## Key Concepts Summary

| Concept | Definition |
|---|---|
| **Nuclear threshold** | The technical crossing of a weapons-grade capability milestone — 90% HEU enrichment, functional warhead design, or delivery system operability. A one-way event: no threshold crossing has ever been reversed without regime change or military action. |
| **News-first architecture** | Pipeline 2-B inverts Pipeline 2-A's logic: GDELT (news) is the primary signal; market data (oil, tankers) is the confirming signal. Nuclear events have no market series; they manifest first in news, then in prices. |
| **High-significance match** | A keyword match with weight ≥ 2.5 in the nuclear escalation dictionary. These trigger a logged record because they are rare enough that every instance deserves review (e.g., "90% enriched uranium" appearing in GDELT is a material news event, not background noise). |
| **Hormuz confluence bonus** | The amplifier applied when Brent level AND tanker prices both surge simultaneously. This distinguishes Hormuz-specific risk pricing (both move) from a generalized commodity cycle (Brent moves, tankers don't). |
| **Dual-signal event** | The scenario where P2-A (BOJ) and P2-B (Iran) both enter elevated phases simultaneously. The portfolio impact is multiplicative, not additive — the GSI architecture is designed to detect this convergence before the market prices it. |
| **Proxy construction** | The use of freely available equity data (FRO/DHT, COPX, BHP) to approximate expensive or inaccessible primary market data (VLCC rates, physical copper, iron ore). A standard data engineering pattern across all Prospectra pipelines. |

---

## Investment Implications

**Signal 2 and the portfolio as of August 13, 2026:**

The three outstanding portfolio actions (EWY exit, FRO/DHT starter, KWEB starter) are now connected to two independent signal pipelines. Signal 1 (BOJ) validates EWY exit and KWEB sizing. Signal 2 (Iran) validates FRO/DHT sizing independently of Signal 1.

This is the key insight: **FRO/DHT does not require Signal 1 to be bullish to be a correct position.** It is a pure Signal 2 hedge. When Pipeline 2-B goes live and confirms the ESCALATING or THRESHOLD_APPROACH phase, the FRO/DHT starter is validated by data — not by CEO judgment.

The KWEB starter also interacts with Signal 2 asymmetrically. A Signal 3 (China trade normalization) Level 3 outcome would be muted or reversed by a simultaneous CRISIS phase in Signal 2 — because a Gulf war would slow Chinese manufacturing demand and redirect US diplomatic attention away from the bilateral normalization track. This is why KWEB remains a 1–2% starter only: it requires Signal 2 COLD or ESCALATING to add to full size.

---

## Reflection Questions

**Question 1 — The false-positive problem:**
Iran nuclear news is inherently noisy. The GDELT keyword "highly enriched uranium" will appear in both a crisis-level enrichment announcement AND in a Congressional hearing where a senator mentions Iran's past program. The pipeline scores both equally. Design a recency-weighting scheme: should articles from the past 48 hours receive higher weight than articles from 5–7 days ago? If a single high-significance headline appears today, should it produce a score spike followed by decay? Write the mathematical function that would implement article recency weighting in the `compute_nuclear_threshold_score()` function.

**Question 2 — The oil signal as leading or lagging:**
The CEO designed the oil stress score as a *confirming* signal, weighting it at 30% and the nuclear score at 50%. This assumes GDELT catches Iran nuclear news before oil markets price it. Test this assumption: in the three most significant Iran nuclear escalation events of the past decade (2019 Fordow restart, 2021 enrichment acceleration, 2024 IAEA camera removal), did GDELT news volume spike before or after Brent crude futures moved? If oil consistently leads news volume, the weighting logic should be inverted. How would you design a backtest using GDELT historical data and FRED Brent prices to answer this question?

**Question 3 — Threshold asymmetry:**
The pipeline treats nuclear escalation and de-escalation symmetrically — net signal = escalation minus de-escalation. But the real world is asymmetric: it takes months to build enrichment capacity, but a single IAEA announcement can signal a breakthrough. Should de-escalation keywords receive a longer decay window than escalation keywords? If Iran announces a freeze today, nuclear risk does not drop to zero — the capability exists and can be restarted. Design an asymmetric scoring rule that allows escalation signals to build quickly but de-escalation signals to decay slowly. What are the second-order effects of this rule on the pipeline's long-run average score?

---

## CEO Closing Note

Three deadlines are now in view:

**August 15 (Saturday — 2 days):** Pipeline 4 go-live. The CEO has nothing more to prepare for this. The code has been in Bolo's hands for 72+ hours. Open Databricks. Run the notebook. Send the confirmation email to ceo@prospectra.earth.

**September 12 (Friday — 30 days):** Pipeline 2-A go-live. The complete code was delivered this morning in Lesson 246. When Pipeline 4 is confirmed live on Saturday, this notebook opens next. The FRED API key is the only new credential required.

**October 3 (Friday — 51 days):** Pipeline 2-B go-live. The complete code is in this lesson. After Pipeline 2-A is live on September 12, this is the notebook that opens next. No new credentials — FRED is already configured, yfinance is already installed.

The engineering roadmap through October 3 is now fully specified. Every cell of every pipeline is written. The build sequence is unambiguous:

```
August 15:   Pipeline 4 live → send output to CEO
September 12: Pipeline 2-A live → GSI v2.0 becomes fully data-driven on Signal 1
October 3:   Pipeline 2-B live → GSI v2.1 becomes fully data-driven on Signals 1 + 2
October 31:  Pipeline 3 live  → GSI v3.0 fully live (Pipeline 3 spec to follow)
```

When October 31 arrives and all four pipelines are live, the Geopolitical Signal Index will be generating a four-component composite score derived entirely from data — no CEO judgmental estimates. The analytical system the CEO described in April 2026 will exist.

The only variable is execution pace. The clock is running. Pipeline 4 is the bottleneck. Everything else is queued and ready.

Send the Pipeline 4 output to ceo@prospectra.earth on Saturday.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session 247 | August 13, 2026 | Engineering Phase, Session 10*
*Pipeline 4 deadline: August 15, 2026 — 2 days*
*Pipeline 2-A deadline: September 12, 2026 — 30 days*
*Pipeline 2-B deadline: October 3, 2026 — 51 days*
*Next session: Pipeline 4 confirmation review + Pipeline 3 architecture preview*

---

## Quick Reference: Pipeline 2-B Databricks Setup Checklist

```
PRE-BUILD (only new requirement):
□ Verify FRED API key is already in secrets from Pipeline 2-A: 
  dbutils.secrets.get(scope="prospectra", key="fred_api_key")
□ Verify yfinance is available (installed on ML Runtime — no action needed)
□ Verify geopolitics database exists: spark.sql("CREATE DATABASE IF NOT EXISTS geopolitics")

BUILD (cell by cell):
□ Cell 1  — Configuration loads, no error
□ Cell 2  — Keyword dictionaries printed (escalation / de-escalation / Hormuz counts)
□ Cell 3  — GDELT nuclear score computed; expect 2.5–3.8 in Aug 2026
□ Cell 4  — Brent crude from FRED + FRO/DHT from yfinance; oil stress score computed
□ Cell 5  — Military signal score; expect 1.8–2.8 in Aug 2026 (no active operations)
□ Cell 6  — P2-B composite + phase classification printed
□ Cell 7  — Phase response protocol printed (check phase vs. current portfolio)
□ Cell 8  — Delta write to geopolitics.pipeline2b_scores ✓
□ Cell 9  — GSI v2.1 printed (pulls live P2-A + P4 scores from Delta)
□ Cell 10 — Cross-pipeline query printed (confirm syntax is valid)

POST-BUILD:
□ Screenshot final composite score and phase label
□ Send score, phase, and Brent level to ceo@prospectra.earth
□ Schedule as Databricks Workflow (daily at 6:30 UTC — after Pipeline 2-A at 6:00 UTC)
□ Report Pipeline 4 confirmation in same email (if sending after August 15)
□ Confirm FRO/DHT position entry in same email (CEO has requested this 4 times)
```
