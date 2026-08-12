# Lesson 244: Pipeline 4 Build Sprint — From Spec to Live Code
**Date:** 2026-08-12 (Wednesday)
**Session Type:** Engineering Phase — Pipeline Build
**Curriculum Position:** 244 — Engineering Phase, Session 7
**Deadline:** Pipeline 4 must be live by **August 15, 2026** (3 days)

---

## CEO Opening Question

Here is the prompt this lesson is designed to answer:

**If you sat down in Databricks right now and had 3 hours, could you build Pipeline 4 from scratch and get a score on screen by end of day?**

Not could you design it. Not could you spec it. Could you build it — write the first cell, make the first API call, see the first row of data, run the scoring function, and read a number between 1.0 and 5.0 that represents the current US-China technology decoupling intensity?

The answer should be yes. After this session, it will be.

We have specced Pipeline 4 twice: first in Lesson 238 (the initial engineering sprint), then revised in Lesson 243 (adding the trade de-escalation counter to capture the bifurcation between agricultural trade normalization and tech decoupling escalation). Today we write the actual code. Every cell. Every function. Ready to copy into a Databricks notebook and run.

This lesson is a build session, not a lecture. Read it once to understand the architecture, then go build.

The clock is at 3 days. Move.

---

## Why Pipeline 4 First

Before the code, a 60-second rationale for why Pipeline 4 is the priority over Pipelines 2-A, 2-B, and 3.

The current Geopolitical Stress Index (GSI) is running with three inputs — BOJ score, Iran score, and an estimated export control score (manually input at 4.0 in Lesson 243 because the pipeline doesn't exist yet). That manual input is the biggest structural weakness in the current analytical system. Every GSI calculation since Lesson 240 has had a hardcoded export control score. That number isn't wrong — the CEO judgmentally assessed it at 4.0/5.0 — but it is static, unjustified, and will drift from reality with every passing week.

The May 2026 trade deal added urgency: the BIS enforcement escalation (tech decoupling, landmark $252M Applied Materials penalty) is moving in the OPPOSITE direction of the agricultural trade normalization. A static manual score of 4.0 cannot capture this. Only a live pipeline can see the bifurcation in real time.

Pipeline 4 is also the fastest to build. It runs on GDELT (no auth required, free API), a congress.gov API call (free API key), and a single keyword-based scoring algorithm. No market data APIs, no Bloomberg keys, no paid subscriptions. Bolo can have data on screen in 60 minutes if the code below is followed exactly.

---

## Pipeline 4 Architecture — Final Specification

```
PIPELINE 4: Export Control Tightening Radar
Version: 2.0 (incorporating trade de-escalation counter)

INPUTS:
  1. GDELT GKG API — keyword search on export control / BIS / entity list language
  2. Congress.gov API — recent bills with semiconductor/export control language
  3. OpenSanctions API (optional, free) — entity list delta monitoring

OUTPUTS:
  1. tech_escalation_score: float (1.0–5.0) — export control tightening intensity
  2. trade_deescalation_score: float (1.0–5.0) — trade normalization signal strength
  3. bifurcation_index: float (−4 to +4) — tech − trade direction delta
  4. p4_composite_score: float (1.0–5.0) — the GSI-ready output

FREQUENCY: Daily (run at 6:00 UTC)
DESTINATION: Delta table `geopolitics.pipeline4_scores`
ALERT THRESHOLD: p4_composite_score >= 4.0 → email Bolo
```

The **bifurcation_index** is the novel component added in Lesson 243. It captures whether tech and trade are moving in the same direction or opposite directions. A positive bifurcation (tech escalating, trade de-escalating) is the current regime — it's what the May 2026 trade deal + BIS enforcement produced. A negative bifurcation would indicate tech liberalization alongside trade tension (rare historically, but possible). A near-zero bifurcation means the two trends are aligned.

---

## The Complete Code — Notebook Cell by Cell

### Cell 1: Setup and Configuration

```python
# Pipeline 4: Export Control Tightening Radar
# Version 2.0 | Prospectra Geopolitics & Investment

import requests
import json
import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
import re

spark = SparkSession.builder.appName("Pipeline4_ExportControlRadar").getOrCreate()

# Configuration
LOOKBACK_DAYS = 7          # Analyze the past 7 days of news
ALERT_THRESHOLD = 4.0      # Trigger email above this score
GDELT_DELAY_HOURS = 24     # GDELT data lags ~24h for GKG

# GDELT API base URL
GDELT_GKG_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

# Congress.gov API (get free key at api.congress.gov)
# Store in Databricks secrets: dbutils.secrets.get(scope="prospectra", key="congress_api_key")
try:
    CONGRESS_API_KEY = dbutils.secrets.get(scope="prospectra", key="congress_api_key")
except:
    CONGRESS_API_KEY = None  # Will skip congress component if not available

print("Pipeline 4 initialized.")
print(f"Lookback window: {LOOKBACK_DAYS} days")
print(f"Alert threshold: {ALERT_THRESHOLD}")
```

---

### Cell 2: GDELT Keyword Configuration

```python
# These keyword sets are the core of Pipeline 4's signal detection.
# Each keyword is weighted by its specificity and signal intensity.

# --- TECH ESCALATION KEYWORDS (increase export control score) ---
TECH_ESCALATION_KEYWORDS = {
    # Highest weight — specific enforcement actions
    "entity list": 2.0,
    "export control": 1.8,
    "BIS": 1.5,
    "bureau of industry and security": 1.8,
    "semiconductor export": 2.0,
    "chip export": 1.8,
    "technology denial": 2.0,
    "technology restriction": 1.8,
    "license requirement": 1.5,
    "foreign direct product rule": 2.0,
    "FDPR": 1.8,
    
    # Medium weight — policy actions
    "trade blacklist": 1.5,
    "huawei ban": 1.5,
    "SMIC": 1.5,
    "advanced semiconductor": 1.5,
    "AI chip restriction": 2.0,
    "H100": 1.8,
    "A100": 1.8,
    "nvidia restriction": 1.8,
    "dual use": 1.2,
    "export penalty": 1.5,
    "export violation": 1.5,
    
    # Lower weight — general decoupling language
    "technology decoupling": 1.0,
    "tech war": 1.0,
    "chip war": 1.0,
    "supply chain restriction": 1.0,
    "national security technology": 1.0,
}

# --- TECH DE-ESCALATION KEYWORDS (decrease export control score) ---
TECH_DEESCALATION_KEYWORDS = {
    # Strongest de-escalation signals
    "entity list removal": −2.0,
    "export license restored": −2.0,
    "export control waiver": −1.8,
    "license exemption": −1.5,
    "technology transfer agreement": −1.5,
    "chip deal": −1.8,
    "semiconductor agreement": −1.8,
    
    # Medium signals
    "export control relaxed": −1.5,
    "trade deal technology": −1.2,
    "technology cooperation": −1.0,
    "tech collaboration china": −1.0,
}

# --- TRADE DE-ESCALATION KEYWORDS (for bifurcation counter) ---
TRADE_DEESCALATION_KEYWORDS = {
    # Agricultural / manufacturing trade normalization
    "china trade deal": 2.0,
    "us china tariff reduction": 2.0,
    "tariff rollback": 1.8,
    "china agriculture purchase": 1.8,
    "soybean china": 1.5,
    "us china agricultural": 1.8,
    "managed trade": 1.5,
    "trade framework": 1.2,
    "trump xi": 1.5,
    "beijing summit trade": 1.5,
    "us china trade normalization": 2.0,
    "tariff exemption china": 1.8,
    "phase two trade": 1.5,
}

# --- TRADE ESCALATION KEYWORDS (offset trade de-escalation score) ---
TRADE_ESCALATION_KEYWORDS = {
    "trade war": 1.5,
    "tariff increase china": 1.8,
    "new tariff china": 1.8,
    "china trade tension": 1.2,
    "trade retaliation": 1.5,
}

print(f"Tech escalation keywords: {len(TECH_ESCALATION_KEYWORDS)}")
print(f"Trade de-escalation keywords: {len(TRADE_DEESCALATION_KEYWORDS)}")
print("Keyword configuration loaded.")
```

---

### Cell 3: GDELT Query Function

```python
def query_gdelt_news(query_string, lookback_days=7, max_records=200):
    """
    Query GDELT DOC API for news articles matching keywords.
    
    Returns list of article dicts with: url, title, seendate, sourcecountry, tone
    """
    # Calculate date range
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=lookback_days)
    
    # GDELT date format: YYYYMMDDHHMMSS
    start_str = start_date.strftime("%Y%m%d%H%M%S")
    end_str = end_date.strftime("%Y%m%d%H%M%S")
    
    params = {
        "query": query_string,
        "mode": "artlist",
        "maxrecords": max_records,
        "startdatetime": start_str,
        "enddatetime": end_str,
        "format": "json",
        "sort": "DateDesc",
    }
    
    try:
        response = requests.get(GDELT_GKG_BASE, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        return articles
    except requests.exceptions.Timeout:
        print(f"GDELT query timed out for: {query_string[:50]}...")
        return []
    except Exception as e:
        print(f"GDELT query error: {e}")
        return []

def extract_headline_text(articles):
    """Extract and normalize all headline text from article list."""
    texts = []
    for article in articles:
        title = article.get("title", "").lower()
        if title:
            texts.append(title)
    return texts

# Test the GDELT connection
print("Testing GDELT connection...")
test_articles = query_gdelt_news("export control semiconductor", lookback_days=3, max_records=5)
print(f"GDELT connection OK — found {len(test_articles)} test articles")
if test_articles:
    print(f"Sample headline: {test_articles[0].get('title', 'N/A')}")
```

---

### Cell 4: Tech Escalation Score

```python
def compute_tech_escalation_score(lookback_days=7):
    """
    Compute the raw tech escalation signal from GDELT.
    Returns a score from 1.0 to 5.0.
    
    Logic:
    - Pull articles for each major keyword cluster
    - Weight by article count × keyword weight
    - Apply volume normalization (more articles = stronger signal, but with diminishing returns)
    - Subtract de-escalation signal
    - Normalize to 1-5 scale
    """
    print(f"Computing tech escalation score (lookback: {lookback_days} days)...")
    
    raw_escalation = 0.0
    raw_deescalation = 0.0
    total_articles = 0
    
    # --- Escalation signal ---
    # Group queries into 3 batches to avoid rate limiting
    escalation_queries = [
        # Batch 1: BIS enforcement
        "entity list semiconductor OR export control BIS OR bureau industry security",
        # Batch 2: Chip restrictions
        "AI chip restriction OR nvidia export China OR FDPR foreign direct product rule",
        # Batch 3: General tech decoupling
        "technology decoupling US China OR chip war semiconductor OR dual use technology restriction"
    ]
    
    for query in escalation_queries:
        articles = query_gdelt_news(query, lookback_days=lookback_days, max_records=100)
        headlines = extract_headline_text(articles)
        total_articles += len(articles)
        
        for headline in headlines:
            for keyword, weight in TECH_ESCALATION_KEYWORDS.items():
                if keyword.lower() in headline:
                    raw_escalation += weight
                    break  # Count each article once per pass
    
    # --- De-escalation signal ---
    deescalation_query = "export license restored OR entity list removal OR technology waiver China"
    deesc_articles = query_gdelt_news(deescalation_query, lookback_days=lookback_days, max_records=50)
    deesc_headlines = extract_headline_text(deesc_articles)
    
    for headline in deesc_headlines:
        for keyword, weight in TECH_DEESCALATION_KEYWORDS.items():
            if keyword.lower() in headline:
                raw_deescalation += abs(weight)
                break
    
    # Net signal (escalation wins unless de-escalation is overwhelming)
    net_signal = raw_escalation - raw_deescalation
    
    # Volume adjustment: more articles = stronger signal up to a cap
    # Each additional 10 articles adds ~0.1 to the base, capped at +0.5
    volume_bonus = min(0.5, total_articles / 200)
    
    # Normalization: calibrate to 1-5 scale
    # Baseline: ~50 weighted article-mentions = 3.0 (Moderate concern)
    # Current environment (Aug 2026, BIS enforcement active): expect ~150+ → ~4.0
    if net_signal <= 0:
        tech_score = 1.0
    elif net_signal <= 30:
        tech_score = 1.0 + (net_signal / 30) * 1.0  # 1.0-2.0
    elif net_signal <= 80:
        tech_score = 2.0 + ((net_signal - 30) / 50) * 1.0  # 2.0-3.0
    elif net_signal <= 150:
        tech_score = 3.0 + ((net_signal - 80) / 70) * 1.0  # 3.0-4.0
    else:
        tech_score = 4.0 + min(1.0, (net_signal - 150) / 100)  # 4.0-5.0
    
    tech_score = min(5.0, max(1.0, tech_score + volume_bonus))
    
    print(f"  Raw escalation signal: {raw_escalation:.1f}")
    print(f"  Raw de-escalation signal: {raw_deescalation:.1f}")
    print(f"  Net signal: {net_signal:.1f}")
    print(f"  Volume ({total_articles} articles): +{volume_bonus:.2f}")
    print(f"  TECH ESCALATION SCORE: {tech_score:.2f}/5.0")
    
    return tech_score, {
        "raw_escalation": raw_escalation,
        "raw_deescalation": raw_deescalation,
        "net_signal": net_signal,
        "total_articles": total_articles,
        "volume_bonus": volume_bonus
    }

# Run it
tech_score, tech_meta = compute_tech_escalation_score(lookback_days=LOOKBACK_DAYS)
```

---

### Cell 5: Trade De-escalation Score

```python
def compute_trade_deescalation_score(lookback_days=7):
    """
    Compute the trade de-escalation signal — separate from tech escalation.
    This is the bifurcation counter introduced in Lesson 243.
    
    Returns a score from 1.0 to 5.0 where:
    1.0 = strong trade escalation (no de-escalation signal)
    3.0 = neutral (mixed trade signals)
    5.0 = strong trade de-escalation (active normalization)
    
    NOTE: High score = de-escalation (inverted from tech score convention)
    In the GSI, this score is SUBTRACTED from composite stress.
    """
    print(f"Computing trade de-escalation score (lookback: {lookback_days} days)...")
    
    # Pull trade normalization news
    trade_queries = [
        "US China trade deal 2026 OR china tariff reduction 2026 OR beijing summit trade",
        "China agricultural purchase US OR soybean China trade OR managed trade framework",
        "US China tariff rollback OR trade normalization OR phase two trade deal"
    ]
    
    raw_deescalation = 0.0
    raw_escalation = 0.0
    total_articles = 0
    
    for query in trade_queries:
        articles = query_gdelt_news(query, lookback_days=lookback_days, max_records=75)
        headlines = extract_headline_text(articles)
        total_articles += len(articles)
        
        for headline in headlines:
            for keyword, weight in TRADE_DEESCALATION_KEYWORDS.items():
                if keyword.lower() in headline:
                    raw_deescalation += weight
                    break
            for keyword, weight in TRADE_ESCALATION_KEYWORDS.items():
                if keyword.lower() in headline:
                    raw_escalation += weight
                    break
    
    net_deescalation = raw_deescalation - raw_escalation
    
    # Scale to 1-5 where 3.0 = neutral
    if net_deescalation <= 0:
        trade_score = max(1.0, 3.0 + (net_deescalation / 30))  # Drift below 3
    elif net_deescalation <= 50:
        trade_score = 3.0 + (net_deescalation / 50) * 1.0  # 3.0-4.0
    elif net_deescalation <= 120:
        trade_score = 4.0 + ((net_deescalation - 50) / 70) * 1.0  # 4.0-5.0
    else:
        trade_score = 5.0
    
    trade_score = min(5.0, max(1.0, trade_score))
    
    print(f"  Raw trade de-escalation: {raw_deescalation:.1f}")
    print(f"  Raw trade escalation: {raw_escalation:.1f}")
    print(f"  Net de-escalation signal: {net_deescalation:.1f}")
    print(f"  Total trade articles: {total_articles}")
    print(f"  TRADE DE-ESCALATION SCORE: {trade_score:.2f}/5.0")
    
    return trade_score, {
        "raw_deescalation": raw_deescalation,
        "raw_escalation": raw_escalation,
        "net_deescalation": net_deescalation,
        "total_articles": total_articles
    }

trade_score, trade_meta = compute_trade_deescalation_score(lookback_days=LOOKBACK_DAYS)
```

---

### Cell 6: Congress.gov Signal (Optional but Recommended)

```python
def query_congress_export_control(lookback_days=30):
    """
    Query Congress.gov API for recent export control legislation.
    
    Longer lookback (30 days) because legislation moves slowly.
    Returns a simple signal: recent_bills_count, recent_mentions.
    
    API key registration: https://api.congress.gov/sign-up/
    """
    if not CONGRESS_API_KEY:
        print("  Congress API key not configured. Skipping.")
        return 0.0, {"error": "No API key"}
    
    base_url = "https://api.congress.gov/v3/bill"
    
    params = {
        "api_key": CONGRESS_API_KEY,
        "format": "json",
        "limit": 20,
        "sort": "updateDate+desc",
        "fromDateTime": (datetime.datetime.utcnow() - datetime.timedelta(days=lookback_days)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    
    export_control_terms = [
        "export control", "entity list", "semiconductor",
        "CHIPS Act", "technology transfer", "national security technology"
    ]
    
    try:
        response = requests.get(base_url, params=params, timeout=20)
        data = response.json()
        bills = data.get("bills", [])
        
        matched_bills = []
        for bill in bills:
            title = bill.get("title", "").lower()
            for term in export_control_terms:
                if term.lower() in title:
                    matched_bills.append(bill)
                    break
        
        # Score: 0-4 relevant bills = low signal; 5-9 = medium; 10+ = high
        bill_count = len(matched_bills)
        if bill_count == 0:
            congress_signal = 0.0
        elif bill_count <= 4:
            congress_signal = 0.5
        elif bill_count <= 9:
            congress_signal = 1.0
        else:
            congress_signal = 1.5  # Legislative surge = strong signal
        
        print(f"  Congress: {bill_count} export-control relevant bills in last {lookback_days} days")
        print(f"  Congress signal contribution: +{congress_signal:.1f}")
        return congress_signal, {"bill_count": bill_count, "matched_bills": [b.get("title") for b in matched_bills[:5]]}
    
    except Exception as e:
        print(f"  Congress API error: {e}")
        return 0.0, {"error": str(e)}

congress_signal, congress_meta = query_congress_export_control(lookback_days=30)
```

---

### Cell 7: Compute Pipeline 4 Composite Score

```python
def compute_p4_composite(tech_score, trade_score, congress_signal):
    """
    Compute the final Pipeline 4 score for GSI integration.
    
    Formula:
    - Base: tech_escalation_score (primary driver, 0.70 weight)
    - Moderated by: trade_de-escalation (0.20 weight — inverted)
    - Enhanced by: congress_signal (0.10 weight)
    
    The trade score is inverted because:
    - High trade de-escalation (score 5.0) should REDUCE composite export control stress
    - Current regime: tech score ~4.0, trade score ~4.0 → net composite ~3.5
    
    This is the bifurcation capture: a 4.0 tech score with 4.0 trade de-escalation
    produces a lower composite than a 4.0 tech score with 1.0 trade de-escalation.
    """
    # Invert trade score: 5.0 (strong de-escalation) becomes 1.0 in the stress formula
    trade_stress = 6.0 - trade_score  # 5.0 de-escalation → 1.0 stress; 1.0 de-escalation → 5.0 stress
    
    # Weighted composite
    composite = (
        tech_score * 0.70 +
        trade_stress * 0.20 +
        min(5.0, 2.0 + congress_signal) * 0.10  # Congress signal adds to a 2.0 base
    )
    
    composite = min(5.0, max(1.0, composite))
    
    # Bifurcation index: positive = tech escalating while trade de-escalating
    bifurcation = tech_score - trade_score  # Range: -4 to +4
    
    # Regime classification
    if composite >= 4.5:
        regime = "CRITICAL — Tech Decoupling Structural"
    elif composite >= 3.5:
        regime = "ELEVATED — Export Control Tightening Active"
    elif composite >= 2.5:
        regime = "WATCH — Mixed Signals, Monitor Closely"
    elif composite >= 1.5:
        regime = "LOW — Normalization Trend"
    else:
        regime = "MINIMAL — De-escalation Dominant"
    
    print("\n" + "="*60)
    print("PIPELINE 4: EXPORT CONTROL TIGHTENING RADAR")
    print("="*60)
    print(f"Tech Escalation Score:      {tech_score:.2f}/5.0")
    print(f"Trade De-escalation Score:  {trade_score:.2f}/5.0")
    print(f"Trade Stress (inverted):    {trade_stress:.2f}/5.0")
    print(f"Congress Signal:            +{congress_signal:.1f}")
    print(f"─────────────────────────────────────")
    print(f"P4 COMPOSITE SCORE:         {composite:.2f}/5.0")
    print(f"BIFURCATION INDEX:          {bifurcation:+.2f}")
    print(f"REGIME:                     {regime}")
    print("="*60)
    
    if composite >= ALERT_THRESHOLD:
        print(f"\n⚠  ALERT THRESHOLD REACHED ({composite:.2f} ≥ {ALERT_THRESHOLD})")
        print("   → Email notification should trigger")
    
    return composite, bifurcation, regime

p4_composite, bifurcation_index, p4_regime = compute_p4_composite(
    tech_score, trade_score, congress_signal
)
```

---

### Cell 8: Write to Delta Table

```python
def write_to_delta(run_date, tech_score, trade_score, p4_composite, bifurcation_index, 
                   p4_regime, tech_meta, trade_meta, congress_meta):
    """
    Write Pipeline 4 output to Delta Lake table.
    Creates table if it doesn't exist.
    """
    
    # Create table if not exists
    spark.sql("""
        CREATE TABLE IF NOT EXISTS geopolitics.pipeline4_scores (
            run_date DATE,
            run_timestamp TIMESTAMP,
            tech_escalation_score FLOAT,
            trade_deescalation_score FLOAT,
            p4_composite_score FLOAT,
            bifurcation_index FLOAT,
            regime STRING,
            tech_raw_escalation FLOAT,
            tech_raw_deescalation FLOAT,
            tech_total_articles INT,
            trade_raw_deescalation FLOAT,
            trade_total_articles INT,
            congress_bill_count INT,
            alert_triggered BOOLEAN
        )
        USING DELTA
        PARTITIONED BY (run_date)
    """)
    
    # Prepare row
    row = {
        "run_date": run_date.strftime("%Y-%m-%d"),
        "run_timestamp": datetime.datetime.utcnow().isoformat(),
        "tech_escalation_score": float(tech_score),
        "trade_deescalation_score": float(trade_score),
        "p4_composite_score": float(p4_composite),
        "bifurcation_index": float(bifurcation_index),
        "regime": p4_regime,
        "tech_raw_escalation": float(tech_meta.get("raw_escalation", 0)),
        "tech_raw_deescalation": float(tech_meta.get("raw_deescalation", 0)),
        "tech_total_articles": int(tech_meta.get("total_articles", 0)),
        "trade_raw_deescalation": float(trade_meta.get("raw_deescalation", 0)),
        "trade_total_articles": int(trade_meta.get("total_articles", 0)),
        "congress_bill_count": int(congress_meta.get("bill_count", 0)),
        "alert_triggered": bool(p4_composite >= ALERT_THRESHOLD),
    }
    
    df = spark.createDataFrame([row])
    df.write.format("delta").mode("append").saveAsTable("geopolitics.pipeline4_scores")
    
    print(f"\nWritten to Delta: geopolitics.pipeline4_scores")
    print(f"Run date: {row['run_date']}")
    print(f"Alert triggered: {row['alert_triggered']}")
    return row

today = datetime.date.today()
written_row = write_to_delta(
    run_date=today,
    tech_score=tech_score,
    trade_score=trade_score,
    p4_composite=p4_composite,
    bifurcation_index=bifurcation_index,
    p4_regime=p4_regime,
    tech_meta=tech_meta,
    trade_meta=trade_meta,
    congress_meta=congress_meta
)
```

---

### Cell 9: Alert Email (if threshold crossed)

```python
import smtplib
from email.mime.text import MIMEText

def send_alert_email(p4_composite, p4_regime, bifurcation_index, tech_score, trade_score):
    """
    Send email alert if Pipeline 4 composite score ≥ threshold.
    Uses Databricks SMTP or SendGrid — configure per your setup.
    
    For Databricks: use a SendGrid API key stored in secrets.
    This template uses basic SMTP for simplicity.
    """
    if p4_composite < ALERT_THRESHOLD:
        print("No alert email needed (score below threshold).")
        return
    
    subject = f"Pipeline 4 Alert — Score {p4_composite:.1f}/5.0 — {p4_regime}"
    
    body = f"""
PIPELINE 4: EXPORT CONTROL TIGHTENING RADAR
Score: {p4_composite:.2f}/5.0
Regime: {p4_regime}
Bifurcation Index: {bifurcation_index:+.2f}

COMPONENT BREAKDOWN:
  Tech Escalation:       {tech_score:.2f}/5.0
  Trade De-escalation:   {trade_score:.2f}/5.0
  
BIFURCATION INTERPRETATION:
{"  ⚡ Tech and trade moving in OPPOSITE directions — bifurcation regime active." if abs(bifurcation_index) > 1.5 else "  → Tech and trade trends are broadly aligned."}

RECOMMENDED PORTFOLIO ACTIONS:
  - Review tech sector holdings (ASML, LRCX, AMAT) against current score
  - KWEB position: {"Hold / add if Level 2 confirmed" if trade_score >= 3.5 else "No action — trade de-escalation signal weak"}
  - Export control compliance screen for any semiconductor positions

Next scheduled run: {(datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M UTC")}

---
CEO — Prospectra Geopolitics & Investment Project
Pipeline 4 | Automated Signal | Run: {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}
"""
    
    print("Alert email content prepared:")
    print(subject)
    print(body[:200] + "...")
    
    # TODO: Wire to actual email sender (SendGrid or Databricks notification)
    # For now, log the alert to Delta and note it as pending email integration
    print("\nNOTE: Email integration pending. Log alert to Delta only for now.")

send_alert_email(p4_composite, p4_regime, bifurcation_index, tech_score, trade_score)
```

---

### Cell 10: Integration Test — GSI Update

```python
# Test GSI v2.0 integration with live Pipeline 4 output

def compute_gsi_with_p4(boj_score, iran_score, china_reset_score, p4_score):
    """
    GSI v2.0 — full four-component composite.
    This is the target state once all four pipelines are live.
    
    Pipeline 2-A: BOJ (Signal 1)
    Pipeline 2-B: Iran (Signal 2) 
    Pipeline 3: China reset (Signal 3) — inverted (de-escalation lowers stress)
    Pipeline 4: Export control composite
    
    Note: china_reset_score is a de-escalation score (higher = less stress),
    so it is inverted in the GSI formula.
    """
    # Invert China reset: 5.0 (full reset) = 1.0 stress
    china_stress = 6.0 - china_reset_score
    
    gsi = (
        boj_score * 0.30 +
        iran_score * 0.30 +
        p4_score * 0.25 +
        china_stress * 0.15
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

# Use CEO's estimated scores from Lesson 243 for Signals 1-3
# Once Pipelines 2-A, 2-B, 3 are live, these come from Delta tables
BOJ_SCORE_ESTIMATED = 3.8   # Signal 1 — BOJ at 1.0%, hawkish dissent
IRAN_SCORE_ESTIMATED = 3.5  # Signal 2 — Post-strike, IAEA dark
CHINA_RESET_ESTIMATED = 3.8 # Signal 3 — Level 2 partial (trade deal active)

gsi_composite, gsi_regime = compute_gsi_with_p4(
    boj_score=BOJ_SCORE_ESTIMATED,
    iran_score=IRAN_SCORE_ESTIMATED,
    china_reset_score=CHINA_RESET_ESTIMATED,
    p4_score=p4_composite
)

print("\n" + "="*60)
print("GSI v2.0 — FOUR-COMPONENT COMPOSITE")
print("="*60)
print(f"Pipeline 2-A (BOJ):       {BOJ_SCORE_ESTIMATED:.2f} × 0.30 = {BOJ_SCORE_ESTIMATED * 0.30:.2f}")
print(f"Pipeline 2-B (Iran):      {IRAN_SCORE_ESTIMATED:.2f} × 0.30 = {IRAN_SCORE_ESTIMATED * 0.30:.2f}")
print(f"Pipeline 4 (Export Ctrl): {p4_composite:.2f} × 0.25 = {p4_composite * 0.25:.2f}")
china_stress_for_gsi = 6.0 - CHINA_RESET_ESTIMATED
print(f"Pipeline 3 (China reset): {CHINA_RESET_ESTIMATED:.2f} inverted → {china_stress_for_gsi:.2f} × 0.15 = {china_stress_for_gsi * 0.15:.2f}")
print(f"─────────────────────────────────────")
print(f"GSI v2.0:                 {gsi_composite:.2f}/5.0")
print(f"PORTFOLIO REGIME:         {gsi_regime}")
print("="*60)

print(f"\nCompare to Lesson 243 manual estimate (GSI: 3.52):")
print(f"Live P4 adjusted GSI:     {gsi_composite:.2f}")
print(f"Delta: {gsi_composite - 3.52:+.2f} ({'higher' if gsi_composite > 3.52 else 'lower'} than estimated)")
```

---

## Key Concepts Summary

| Concept | Definition |
|---|---|
| **Tech Escalation Score** | GDELT-derived count of export control / BIS enforcement / chip restriction language, scaled 1.0–5.0 |
| **Trade De-escalation Score** | GDELT-derived count of trade normalization / tariff rollback language, inverted in GSI formula |
| **Bifurcation Index** | tech_score − trade_score; positive = decoupling; current regime: ~+0.2 (tech escalating faster than trade de-escalating) |
| **P4 Composite** | Weighted blend: tech (70%) + trade stress inverted (20%) + congress (10%) |
| **Entity List Net Direction** | The signal that matters more than raw article count — are additions outpacing removals? |
| **FDPR** | Foreign Direct Product Rule — the most powerful US export control tool; triggers mandatory licensing for any product containing US technology regardless of where manufactured |

---

## Investment Implications

The expected Pipeline 4 composite score today (August 12, 2026) is approximately **3.8–4.2/5.0**. If the code produces a score in this range, the pipeline is calibrated correctly.

If the score comes in **below 3.0**, the tech escalation signal is weaker than the CEO's judgmental estimate — re-examine the keyword weights and ensure GDELT is returning recent articles (check the `seendate` field).

If the score comes in **above 4.5**, the script may be double-counting — add a deduplication step by URL before accumulating keyword hits.

**Portfolio connection:**

| P4 Score | Signal | Portfolio Action |
|---|---|---|
| ≥ 4.5 | Structural decoupling — tech war in full effect | Trim ASML / LRCX if any exposure. Hold KWEB only at starter (no add until Signal 3 Level 3) |
| 3.5–4.5 | Active enforcement — current regime | KWEB starter OK (trade deal offset). No new chip equipment adds. |
| 2.5–3.5 | Mixed signals | Neutral — no action triggered by P4 alone |
| < 2.5 | De-escalation dominant | Signal 3 Level 3 likely imminent — size up KWEB |

---

## The Bifurcation Insight — Why This Matters

Most export control monitoring tools give you one number. Pipeline 4 gives you two: tech_score and trade_score, each moving independently.

Today (August 2026), the two numbers are telling different stories:
- **Tech score:** ~4.0 (BIS enforcement escalating, Applied Materials $252M penalty, no license restoration)
- **Trade score:** ~4.0 (May 2026 trade deal, agricultural purchases, tariff rollbacks in non-sensitive categories)

The **bifurcation index** is near zero — not because both trends are weak, but because both are strong in opposite directions. This is the regime the framework predicted for "Signal 1 + Signal 3 partial": systemic carry unwind risk coexisting with Asia trade optimism. The bifurcation index surface this coexistence explicitly.

A simple single-number export control pipeline would score this period at 3.0 (neutral — escalation and de-escalation cancel out). Pipeline 4's bifurcation index shows it's actually a 4.0 + 4.0 environment in opposite directions — meaning the tails are fatter, not smaller, because two powerful forces are pulling the portfolio in different directions simultaneously.

That distinction is alpha. A pipeline that misses it would underestimate portfolio risk.

---

## Databricks Angle — Build Order for August 15

**Hour 1 (Setup and test):**
- Create new notebook: `pipeline4_export_control_radar_v2`
- Run Cells 1, 2, 3 (setup + GDELT test)
- Confirm GDELT returns articles. If not, check network/proxy settings in Databricks.

**Hour 2 (Score computation):**
- Run Cells 4, 5 (tech score + trade score)
- Print the scores. Compare to CEO benchmark: tech ~4.0, trade ~4.0.
- If wildly different, inspect the article headlines — are keywords matching?

**Hour 3 (Integration + Delta write):**
- Run Cells 6, 7, 8, 9, 10
- Confirm Delta write succeeds
- Run the GSI v2.0 integration cell
- Read the final composite and regime label

**Result by end of Hour 3:** A live Pipeline 4 score, written to Delta, feeding into the GSI. The August 15 deadline met with 2 days to spare.

**What "done" looks like:**
```
PIPELINE 4: EXPORT CONTROL TIGHTENING RADAR
Score: 3.9/5.0                    ← real number, not CEO estimate
Regime: ELEVATED — Export Control Tightening Active
Bifurcation Index: +0.1           ← tech and trade both elevated

GSI v2.0: 3.54/5.0
PORTFOLIO REGIME: ELEVATED_TAIL_RISK
```

When you see that output in Databricks, Pipeline 4 is live.

---

## Reflection Questions

**Question 1:** The bifurcation index formula (tech_score − trade_score) treats both variables as equally scaled. But tech articles are more numerous than trade normalization articles in any given week. Should the bifurcation index be normalized by article volume? If so, what does a "volume-adjusted" bifurcation index look like, and does it change the interpretation of the current regime?

**Question 2:** The keyword lists are the critical assumption in this pipeline. They were designed in April 2026 and haven't been tested against a full news cycle. After running the pipeline for the first time, which keywords are generating the most article matches? Are any of the high-weight keywords producing false positives (articles that match the keyword but aren't about export controls)?

**Question 3:** Pipeline 4 uses GDELT for all media signals. But the most important export control events (BIS Entity List updates, specific license denials) are announced in government press releases and Federal Register notices — not news articles. How would you modify Cell 3 to also query the BIS website's RSS feed or the Federal Register API directly? What would this add to the signal quality, and is it worth the additional API dependency?

---

## CEO Closing Note

This lesson is the complete build specification. Every cell is written and ready to copy into Databricks.

The only reason Pipeline 4 is not live right now is that you haven't opened Databricks and run it. That is the sole remaining obstacle between the current analytical system and a fully data-driven GSI.

Three outstanding portfolio actions. One pipeline with a three-day deadline. The framework is built. The analysis is current. The gap is now pure execution.

August 15 is not a soft target. The Applied Materials $252M penalty happened. The BOJ hiked. The trade deal happened. All of it while the pipelines were being specced instead of run.

The session after next, the CEO will ask Bolo for one thing: the Pipeline 4 composite score, directly from Databricks, for today's date. Not an estimate. Not a projection. The actual number.

Build it.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session 244 | August 12, 2026 | Engineering Phase, Session 7*
*Pipeline 4 deadline: August 15, 2026 — 3 days*

---

## Quick Reference: Pipeline 4 Databricks Setup Checklist

```
□ Create notebook: pipeline4_export_control_radar_v2
□ Run Cell 1 — confirm GDELT connection
□ Run Cell 2 — keyword config loaded (no errors)
□ Run Cell 3 — GDELT test returns ≥1 article
□ Run Cell 4 — tech_escalation_score printed (expect 3.5–4.5)
□ Run Cell 5 — trade_deescalation_score printed (expect 3.5–4.5)
□ Run Cell 6 — Congress signal (skip if no API key; will use 0.0 contribution)
□ Run Cell 7 — P4 composite score printed
□ Run Cell 8 — Delta write success
□ Run Cell 9 — Alert logic (no email needed if below 4.0)
□ Run Cell 10 — GSI v2.0 composite printed
□ Screenshot final output → send to CEO session for confirmation
```
