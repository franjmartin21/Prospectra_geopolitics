# Lesson 249: Pipeline 3 Complete Code — US-China Diplomatic Reset Monitor
**Date:** 2026-08-14 (Friday)
**Session Type:** Engineering Phase — Pipeline Build Sprint
**Curriculum Position:** 249 — Engineering Phase, Session 12
**Pipeline 4 Deadline:** August 15, 2026 — **TOMORROW**
**Pipeline 2-A Deadline:** September 12, 2026 — 29 days
**Pipeline 2-B Deadline:** October 3, 2026 — 50 days
**Pipeline 3 Deadline:** October 31, 2026 — 78 days

---

## CEO Opening Question

Lesson 248 established the architecture. One unresolved question before you open the code:

**COPX rallied 12% from April to June 2026. Was that the market pricing the May summit — or China's infrastructure investment cycle repricing copper demand regardless of diplomatic normalization?**

The distinction is not academic. If Pipeline 3's equity proxy layer cannot separate "China economy recovering" from "US-China reset happening," it will generate false-positive normalization signals every time Beijing announces a stimulus package. A pipeline that cannot distinguish its primary variable from a correlated confound is not an intelligence tool — it is a copper price tracker with a diplomatic label.

The answer is in Cell 6. Read the confluence logic before running the cell.

---

## Complete Pipeline 3 Code — 10 Cells

---

### Cell 1: Setup and Configuration

```python
# Pipeline 3: US-China Diplomatic Reset Monitor
# Version 1.0 | Prospectra Geopolitics & Investment
# Build date: October 31, 2026 (scheduled go-live)
# Code delivered: August 14, 2026 (Lesson 249)

import requests
import datetime
import json
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp
from pyspark.sql.types import (StructType, StructField, StringType,
                                FloatType, DateType, TimestampType,
                                BooleanType, IntegerType)

spark = SparkSession.builder.appName("Pipeline3_USChinaResetMonitor").getOrCreate()

# ── Window Configuration ───────────────────────────────────────────────────────
# Pipeline 3 uses LONGER lookback windows than Pipelines 2-A/2-B/4.
# Rationale: US-China relations change slowly; a 7-day blip is noise.
LOOKBACK_DAYS_DIPLOMATIC = 14    # Diplomatic engagement layer
LOOKBACK_DAYS_TRADE      = 14    # Trade normalization layer
LOOKBACK_DAYS_TAIWAN     =  3    # Taiwan counter: FAST window (escalation moves in 72h)
LOOKBACK_DAYS_EQUITY_FETCH = 30  # yfinance fetch window (compute 14d return from this)
LOOKBACK_DAYS_EQUITY_RETURN = 14 # Return calculation window

# ── Alert Thresholds ────────────────────────────────────────────────────────────
ALERT_THRESHOLD_DROP   = 0.5  # Alert if china_reset_score drops 0.5+ vs 14-day max
ALERT_THRESHOLD_TAIWAN = 1.5  # Alert if taiwan_counter >= 1.5 (acute Taiwan tension)

# ── CEO Baseline (set post-May 2026 Trump-Xi summit) ──────────────────────────
CEO_ESTIMATE_CHINA_RESET = 3.8  # MANAGED_PAUSE / NORMALIZATION boundary

GDELT_API_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"

print("=" * 60)
print("Pipeline 3: US-China Diplomatic Reset Monitor")
print("=" * 60)
print(f"Diplomatic window:  {LOOKBACK_DAYS_DIPLOMATIC} days")
print(f"Trade window:       {LOOKBACK_DAYS_TRADE} days")
print(f"Taiwan window:      {LOOKBACK_DAYS_TAIWAN} days  ← short by design")
print(f"Equity return:      {LOOKBACK_DAYS_EQUITY_RETURN} days")
print(f"CEO baseline:       {CEO_ESTIMATE_CHINA_RESET}/5.0 (MANAGED_PAUSE)")
print(f"Alert drop:         {ALERT_THRESHOLD_DROP} pts in 14-day window")
print(f"Alert Taiwan:       {ALERT_THRESHOLD_TAIWAN}+ counter-score")
```

---

### Cell 2: Keyword Libraries

```python
# ── Layer 1: Diplomatic Engagement Keywords ────────────────────────────────────
# Weighted by specificity and diplomatic significance
# Higher weight = rarer event = stronger normalization signal

DIPLOMATIC_ENGAGEMENT_KEYWORDS = {
    # Presidential / Head of State (highest signal value)
    "xi trump meeting":                  3.5,
    "us china summit":                   3.5,
    "presidential call china":           3.0,
    "trump xi":                          2.8,
    "us china leaders":                  2.8,

    # Institutional mechanisms (durable signal — more important than one-off meetings)
    "us china working group":            2.5,
    "us china trade commission":         2.5,
    "us china strategic dialogue":       3.0,
    "board of trade us china":           3.0,   # May 2026 bilateral trade board mechanism
    "us china economic dialogue":        2.5,
    "us china military hotline":         3.0,   # Military-to-military = high trust signal
    "us china military communication":   2.5,
    "us china commander call":           2.8,

    # Specific normalization acts
    "us china tariff reduction":         3.0,
    "us china tariff rollback":          3.0,
    "us china sanctions relief":         2.8,
    "us china visa agreement":           2.0,
    "us china scientific cooperation":   2.0,
    "us china climate agreement":        2.2,
    "us china fentanyl cooperation":     2.2,

    # Diplomatic language
    "constructive relationship us china": 2.5,
    "strategic stability us china":       2.5,
    "managing competition us china":      2.0,
    "guardrails us china":                2.0,
    "candid discussions us china":        1.5,
    "positive trajectory us china":       2.0,
}

DIPLOMATIC_DETERIORATION_KEYWORDS = {
    "us china sanctions":               -2.0,
    "us china decoupling":              -2.5,
    "china entity list":                -2.0,
    "us china expulsion":               -3.0,
    "us china ambassador recalled":     -3.5,
    "us china diplomatic downgrade":    -3.5,
    "us china trade war resumed":       -3.0,
    "us china tariff increase":         -2.5,
    "us china new tariffs":             -2.5,
    "china retaliation us":             -2.0,
    "us chip ban china":                -2.0,
    "us china tech war":                -2.2,
    "us china espionage":               -2.0,
}

# ── Layer 2: Trade Normalization Keywords ──────────────────────────────────────
TRADE_NORMALIZATION_KEYWORDS = {
    # Agricultural purchases (core May 2026 deal mechanism)
    "china us agricultural purchase":   2.5,
    "china soybean purchase us":        2.0,
    "china us farm goods":              2.0,
    "china agricultural import us":     2.0,
    "china us grain":                   1.8,

    # Technology / manufacturing re-linkage
    "us china supply chain":            1.8,
    "apple china production":           1.5,
    "us china investment":              1.8,
    "us china joint venture":           2.0,

    # Trade volume signals
    "us china exports increase":        2.0,
    "us china trade deal":              2.5,
    "us china trade agreement":         2.5,

    # Critical minerals (specific May 2026 deal element)
    "china critical minerals us":       2.5,
    "china rare earth us supply":       2.5,
    "china minerals agreement":         3.0,
    "china graphite us":                2.0,
}

TRADE_DETERIORATION_KEYWORDS = {
    "china export ban":                 -2.5,
    "china rare earth ban":             -3.0,   # #1 crisis trigger — see rare_earth_alert
    "china gallium ban":                -2.8,
    "china germanium ban":              -2.8,
    "china graphite ban":               -2.5,
    "us import ban china":              -2.0,
    "china dumping us":                 -1.8,
    "china overcapacity us":            -1.8,
    "us anti-dumping china":            -1.5,
    "us china steel tariffs":           -1.8,
    "us china ev tariffs":              -1.8,
}

# ── Layer 3: Taiwan Risk Keywords ─────────────────────────────────────────────
TAIWAN_RISK_KEYWORDS = {
    # Military activity
    "pla taiwan strait exercise":       2.5,
    "china military taiwan":            2.0,
    "taiwan strait tension":            2.0,
    "china taiwan military drill":      2.5,
    "pla carrier taiwan":               3.0,
    "china taiwan blockade":            4.0,
    "taiwan invasion china":            4.0,
    "china taiwan war":                 4.0,
    "china taiwan live fire":           3.0,
    "pla taiwan exercise":              2.5,

    # Political escalation
    "us taiwan arms sales":             1.8,
    "taiwan independence declaration":  3.5,
    "china taiwan sanctions":           2.0,
    "china taiwan threat":              1.5,
    "taiwan strait incident":           2.5,
    "china taiwan crisis":              2.5,

    # Diplomatic crisis
    "us taiwan visit china protest":    1.5,
    "china suspend talks taiwan":       2.5,
    "china taiwan emergency":           3.0,
}

# ── Layer 4: Equity Proxies ────────────────────────────────────────────────────
US_CHINA_EQUITY_PROXIES = {
    "COPX": {"name": "Global X Copper Miners ETF",    "weight": 0.30,
             "signal": "China ~50% of world copper demand; normalization → demand acceleration"},
    "MCHI": {"name": "iShares MSCI China ETF",         "weight": 0.35,
             "signal": "Broadest China equity proxy; normalization compresses country risk premium"},
    "KWEB": {"name": "KraneShares CSI China Internet", "weight": 0.15,
             "signal": "China tech sentiment; cross-references active portfolio position"},
    "BHP":  {"name": "BHP Group ADR",                  "weight": 0.20,
             "signal": "Iron ore; Australia-China trade most direct US-China détente beneficiary"},
}

print("Keyword libraries loaded:")
print(f"  Diplomatic engagement:    {len(DIPLOMATIC_ENGAGEMENT_KEYWORDS)} keywords")
print(f"  Diplomatic deterioration: {len(DIPLOMATIC_DETERIORATION_KEYWORDS)} keywords")
print(f"  Trade normalization:      {len(TRADE_NORMALIZATION_KEYWORDS)} keywords")
print(f"  Trade deterioration:      {len(TRADE_DETERIORATION_KEYWORDS)} keywords")
print(f"  Taiwan risk:              {len(TAIWAN_RISK_KEYWORDS)} keywords")
print(f"  Equity proxies:           {len(US_CHINA_EQUITY_PROXIES)} tickers")
```

---

### Cell 3: GDELT Query Function + Layer 1 Diplomatic Tone Score

```python
def query_gdelt_news(query_string, lookback_days=14, max_records=100):
    """Fetch articles from GDELT API — identical interface to P2-A, P2-B, P4."""
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=lookback_days)
    params = {
        "query":         query_string,
        "mode":          "artlist",
        "maxrecords":    max_records,
        "startdatetime": start_date.strftime("%Y%m%d%H%M%S"),
        "enddatetime":   end_date.strftime("%Y%m%d%H%M%S"),
        "format":        "json",
        "sort":          "DateDesc",
    }
    try:
        r = requests.get(GDELT_API_BASE, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("articles", [])
    except Exception as e:
        print(f"  GDELT error for '{query_string[:45]}...': {e}")
        return []


def compute_diplomatic_tone_score(lookback_days=14):
    """
    Layer 1: GDELT Diplomatic Tone Score (14-day window)
    
    Three query angles:
    1. High-level engagement: summits, working groups, official meetings
    2. Normalization acts: tariff cuts, agreements, sanctions relief
    3. Diplomatic language: constructive signals, stability framing
    
    URL deduplication prevents double-counting across query angles.
    
    Returns score 1.0–5.0.
    Calibration:
      1.5–2.0 = Background noise, Cold Peace baseline
      2.0–3.0 = Routine diplomatic activity
      3.0–3.8 = Active engagement: MANAGED_PAUSE / NORMALIZATION
      3.8–5.0 = Major breakthrough or sustained institutional build-out
    """
    print("Layer 1: Computing diplomatic tone score (GDELT)...")

    queries = [
        "US China summit OR US China working group OR Xi Trump meeting OR US China strategic dialogue",
        "US China tariff reduction OR US China trade agreement OR US China normalization agreement",
        "constructive US China OR strategic stability US China OR guardrails US China",
    ]

    seen_urls       = set()
    raw_engagement  = 0.0
    raw_deterioration = 0.0
    total_articles  = 0
    high_value      = []

    for query in queries:
        for article in query_gdelt_news(query, lookback_days=lookback_days, max_records=100):
            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            total_articles += 1
            headline = (article.get("title") or "").lower()

            matched = False
            for kw, weight in DIPLOMATIC_ENGAGEMENT_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_engagement += weight
                    if weight >= 3.0:
                        high_value.append((kw, weight, article.get("title", "")))
                    matched = True
                    break

            if not matched:
                for kw, weight in DIPLOMATIC_DETERIORATION_KEYWORDS.items():
                    if kw.lower() in headline:
                        raw_deterioration += abs(weight)
                        break

    net_diplomatic = raw_engagement - raw_deterioration

    if net_diplomatic <= 0:
        score = max(1.0, 1.5 + net_diplomatic / 20)
    elif net_diplomatic <= 20:
        score = 1.5 + net_diplomatic / 20 * 0.5
    elif net_diplomatic <= 60:
        score = 2.0 + (net_diplomatic - 20) / 40 * 1.0
    elif net_diplomatic <= 100:
        score = 3.0 + (net_diplomatic - 60) / 40 * 0.8
    elif net_diplomatic <= 150:
        score = 3.8 + (net_diplomatic - 100) / 50 * 0.5
    else:
        score = 4.3 + min(0.7, (net_diplomatic - 150) / 200)

    score = min(5.0, max(1.0, score))

    print(f"  Raw engagement:    {raw_engagement:.1f}")
    print(f"  Raw deterioration: {raw_deterioration:.1f}")
    print(f"  Net diplomatic:    {net_diplomatic:.1f}")
    print(f"  Articles scanned:  {total_articles}")
    if high_value:
        print(f"  HIGH-VALUE MATCHES ({len(high_value)}):")
        for kw, w, title in high_value[:3]:
            print(f"    [{w:.1f}] '{kw}' → {title[:70]}")
    print(f"  DIPLOMATIC TONE SCORE: {score:.2f}/5.0")

    return score, {
        "raw_engagement":    raw_engagement,
        "raw_deterioration": raw_deterioration,
        "net_diplomatic":    net_diplomatic,
        "total_articles":    total_articles,
        "high_value_matches": len(high_value),
    }


diplomatic_score, diplomatic_meta = compute_diplomatic_tone_score(
    lookback_days=LOOKBACK_DAYS_DIPLOMATIC
)
```

---

### Cell 4: Layer 2 Trade Normalization Score

```python
def compute_trade_normalization_score(lookback_days=14):
    """
    Layer 2: GDELT Trade Normalization Score (14-day window)
    
    Diplomatic words without economic follow-through are noise.
    This layer measures whether trade is actually normalizing.
    
    RARE EARTH ALERT: If China rare earth / gallium / germanium ban keywords
    are detected, trade_score is floored at 1.0 regardless of other signals.
    This is the single most dangerous trade-layer event — it immediately
    falsifies the managed pause thesis.
    
    Returns score 1.0–5.0.
    """
    print("Layer 2: Computing trade normalization score (GDELT)...")

    queries = [
        "China US agricultural purchase OR China soybean US OR US China trade deal implementation",
        "China critical minerals US OR China rare earth supply OR US China minerals agreement",
        "US China tariff cut OR US China trade normalization OR US China supply chain reintegration",
    ]

    seen_urls         = set()
    raw_normalization = 0.0
    raw_deterioration = 0.0
    total_articles    = 0
    rare_earth_alert  = False

    RARE_EARTH_CRISIS_PHRASES = [
        "rare earth ban", "gallium ban", "germanium ban",
        "graphite ban", "china mineral export ban", "china export control minerals"
    ]

    for query in queries:
        for article in query_gdelt_news(query, lookback_days=lookback_days, max_records=100):
            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            total_articles += 1
            headline = (article.get("title") or "").lower()

            # Rare earth crisis check — highest priority
            if any(phrase in headline for phrase in RARE_EARTH_CRISIS_PHRASES):
                rare_earth_alert = True
                print(f"  ⚠  RARE EARTH ALERT: {article.get('title', '')[:80]}")

            matched = False
            for kw, weight in TRADE_NORMALIZATION_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_normalization += weight
                    matched = True
                    break

            if not matched:
                for kw, weight in TRADE_DETERIORATION_KEYWORDS.items():
                    if kw.lower() in headline:
                        raw_deterioration += abs(weight)
                        break

    if rare_earth_alert:
        # Crisis override — floor score regardless of normalization volume
        trade_score = 1.0
        print("  ⚠  RARE EARTH BAN CONFIRMED — trade score floored at 1.0")
        print("  ⚠  Portfolio action: EXIT KWEB, cross-reference Pipeline 4")
    else:
        net_trade = raw_normalization - raw_deterioration

        if net_trade <= 0:
            trade_score = max(1.0, 1.5 + net_trade / 20)
        elif net_trade <= 20:
            trade_score = 1.5 + net_trade / 20 * 0.5
        elif net_trade <= 40:
            trade_score = 2.0 + (net_trade - 20) / 20 * 0.5
        elif net_trade <= 80:
            trade_score = 2.5 + (net_trade - 40) / 40 * 1.0
        elif net_trade <= 120:
            trade_score = 3.5 + (net_trade - 80) / 40 * 0.8
        else:
            trade_score = 4.3 + min(0.7, (net_trade - 120) / 80)

        trade_score = min(5.0, max(1.0, trade_score))

    print(f"  Raw normalization: {raw_normalization:.1f}")
    print(f"  Raw deterioration: {raw_deterioration:.1f}")
    print(f"  Articles scanned:  {total_articles}")
    print(f"  Rare earth alert:  {rare_earth_alert}")
    print(f"  TRADE NORMALIZATION SCORE: {trade_score:.2f}/5.0")

    return trade_score, {
        "raw_normalization": raw_normalization,
        "raw_deterioration": raw_deterioration,
        "total_articles":    total_articles,
        "rare_earth_alert":  rare_earth_alert,
    }


trade_score, trade_meta = compute_trade_normalization_score(
    lookback_days=LOOKBACK_DAYS_TRADE
)
```

---

### Cell 5: Layer 3 Taiwan Counter-Signal

```python
def compute_taiwan_counter_score(lookback_days=3):
    """
    Layer 3: Taiwan Counter-Signal (3-day window — FAST by design)
    
    The termination condition for the US-China reset.
    
    Output: 0.0–2.0 (subtracted from the reset composite, not added)
    
    Why 3-day window: The May 2026 trade deal took 6 months to negotiate.
    A Taiwan Strait incident can terminate the reset conversation in 72 hours.
    The Taiwan layer must react faster than the reset layer.
    
    Asymmetry: there is no Taiwan de-escalation counter. A PLA exercise
    does not 'un-happen' in the same window it occurred. The counter-score
    decays naturally as events age out of the 3-day window.
    """
    print(f"Layer 3: Computing Taiwan counter-signal (GDELT, {lookback_days}-day window)...")

    queries = [
        "PLA Taiwan strait exercise OR China Taiwan military OR Taiwan strait tension",
        "China Taiwan invasion OR China Taiwan blockade OR China Taiwan war",
        "US Taiwan arms OR Taiwan independence OR China Taiwan crisis",
    ]

    seen_urls    = set()
    raw_taiwan   = 0.0
    total_articles = 0
    high_severity = []

    for query in queries:
        for article in query_gdelt_news(query, lookback_days=lookback_days, max_records=75):
            url = article.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            total_articles += 1
            headline = (article.get("title") or "").lower()

            for kw, weight in TAIWAN_RISK_KEYWORDS.items():
                if kw.lower() in headline:
                    raw_taiwan += weight
                    if weight >= 3.0:
                        high_severity.append((kw, weight, article.get("title", "")))
                    break

    # Map raw signal → counter-score (0.0–2.0)
    # Formula from Lesson 248 architecture spec
    if raw_taiwan <= 5:
        taiwan_counter = 0.0
    elif raw_taiwan <= 20:
        taiwan_counter = 0.3 + (raw_taiwan - 5) / 15 * 0.5
    elif raw_taiwan <= 60:
        taiwan_counter = 0.8 + (raw_taiwan - 20) / 40 * 0.7
    elif raw_taiwan <= 120:
        taiwan_counter = 1.5 + (raw_taiwan - 60) / 60 * 0.4
    else:
        taiwan_counter = 2.0  # Conflict-level cap

    if taiwan_counter < 0.3:
        tw_label = "QUIET"
    elif taiwan_counter < 0.8:
        tw_label = "BACKGROUND_FRICTION"
    elif taiwan_counter < 1.5:
        tw_label = "ELEVATED"
    elif taiwan_counter < 2.0:
        tw_label = "ACUTE"
    else:
        tw_label = "CONFLICT_LEVEL"

    print(f"  Raw Taiwan signal: {raw_taiwan:.1f}")
    print(f"  Articles scanned:  {total_articles}")
    print(f"  TAIWAN COUNTER-SCORE: {taiwan_counter:.2f} ({tw_label})")
    print(f"  Effect: reset score will be reduced by {taiwan_counter:.2f} pts")

    if taiwan_counter >= ALERT_THRESHOLD_TAIWAN:
        print(f"  ⚠  TAIWAN ALERT: {taiwan_counter:.2f} >= threshold {ALERT_THRESHOLD_TAIWAN}")
        print("  ⚠  Taiwan escalation is overriding the diplomatic reset signal")

    if high_severity:
        print(f"  HIGH-SEVERITY MATCHES ({len(high_severity)}):")
        for kw, w, title in high_severity[:3]:
            print(f"    [{w:.1f}] '{kw}' → {title[:70]}")

    return taiwan_counter, {
        "raw_taiwan":            raw_taiwan,
        "total_articles":        total_articles,
        "taiwan_label":          tw_label,
        "high_severity_matches": len(high_severity),
    }


taiwan_counter, taiwan_meta = compute_taiwan_counter_score(
    lookback_days=LOOKBACK_DAYS_TAIWAN
)
```

---

### Cell 6: Layer 4 Equity Proxy Score

```python
import yfinance as yf

# ── COPX Disambiguation Logic ──────────────────────────────────────────────────
#
# COPX moves on three independent drivers — only one is US-China reset:
#   (a) Supply disruption: Chile/Peru mining strikes → COPX up (not China-related)
#   (b) USD weakness: DXY falls → copper priced up in USD (not China-related)
#   (c) China demand recovery: stimulus, infrastructure → China-related but NOT reset
#   (d) US-China diplomatic normalization → China equity AND commodity repricing together
#
# The ensemble answers this: if ONLY COPX rallies while MCHI is flat or down,
# the driver is (a), (b), or generalized commodity. That still pushes the score up,
# but COPX is only 30% of the composite — not enough to breach 3.0 alone.
# If MCHI leads and BHP follows, the driver is Chinese demand / reset — correct signal.
# The confluence_note field documents which pattern is occurring.

def compute_equity_proxy_score():
    """
    Layer 4: Equity Proxy Score — do markets confirm the diplomatic reset?
    
    Uses 14-day returns (matching GDELT diplomatic window).
    Weights: MCHI 35% + COPX 30% + BHP 20% + KWEB 15%
    
    Returns score 1.0–5.0.
    """
    print("Layer 4: Computing equity proxy score...")

    proxy_returns   = {}
    weighted_return = 0.0

    for ticker, meta in US_CHINA_EQUITY_PROXIES.items():
        try:
            hist  = yf.Ticker(ticker).history(
                period=f"{LOOKBACK_DAYS_EQUITY_FETCH}d", interval="1d"
            )
            if not hist.empty:
                close = hist["Close"].dropna()
                n     = min(len(close), LOOKBACK_DAYS_EQUITY_RETURN)
                if n >= 5:
                    ret = float(close.iloc[-1] / close.iloc[-n] - 1)
                else:
                    ret = float(close.iloc[-1] / close.iloc[0] - 1)
                proxy_returns[ticker] = ret
                weighted_return += ret * meta["weight"]
                print(f"  {meta['name']} ({ticker}): {ret:+.2%} ({n}d)")
            else:
                proxy_returns[ticker] = 0.0
                print(f"  {ticker}: no data")
        except Exception as e:
            proxy_returns[ticker] = 0.0
            print(f"  {ticker} error: {e}")

    # Map weighted composite return → equity proxy score
    wr = weighted_return
    if wr < -0.05:
        equity_score = max(1.0, 1.5 + wr * 10)
    elif wr < 0:
        equity_score = 1.5 + (wr / 0.05) * 0.5
    elif wr < 0.02:
        equity_score = 2.0 + (wr / 0.02) * 0.5
    elif wr < 0.05:
        equity_score = 2.5 + ((wr - 0.02) / 0.03) * 1.0
    elif wr < 0.08:
        equity_score = 3.5 + ((wr - 0.05) / 0.03) * 0.8
    elif wr < 0.12:
        equity_score = 4.3 + ((wr - 0.08) / 0.04) * 0.5
    else:
        equity_score = min(5.0, 4.8 + ((wr - 0.12) / 0.08) * 0.2)

    equity_score = min(5.0, max(1.0, equity_score))

    # Confluence check: is MCHI leading COPX? (reset-specific vs. supply/USD-driven)
    mchi_ret = proxy_returns.get("MCHI", 0.0)
    copx_ret = proxy_returns.get("COPX", 0.0)
    bhp_ret  = proxy_returns.get("BHP",  0.0)
    kweb_ret = proxy_returns.get("KWEB", 0.0)

    if mchi_ret > copx_ret and mchi_ret > 0.01:
        confluence_note = "MCHI leading COPX — China equity re-rating. RESET SIGNAL IS REAL."
    elif copx_ret > mchi_ret + 0.02 and mchi_ret < 0.01:
        confluence_note = "COPX leading MCHI — likely supply disruption / USD move, NOT reset. Score may OVERSTATE normalization."
    elif mchi_ret < -0.01 and copx_ret < -0.01:
        confluence_note = "Both declining — market skeptical of reset. Diplomatic words are noise."
    else:
        confluence_note = "Mixed signals — equity proxies not definitively reset-driven."

    print(f"\n  Weighted 14d composite: {wr:+.2%}")
    print(f"  MCHI: {mchi_ret:+.2%} | COPX: {copx_ret:+.2%} | BHP: {bhp_ret:+.2%} | KWEB: {kweb_ret:+.2%}")
    print(f"  Confluence: {confluence_note}")
    print(f"  EQUITY PROXY SCORE: {equity_score:.2f}/5.0")

    return equity_score, {
        "weighted_return":  wr,
        "mchi_return":      mchi_ret,
        "copx_return":      copx_ret,
        "bhp_return":       bhp_ret,
        "kweb_return":      kweb_ret,
        "confluence_note":  confluence_note,
        "proxy_returns":    proxy_returns,
    }


equity_score, equity_meta = compute_equity_proxy_score()
```

---

### Cell 7: Composite Score and Regime Classification

```python
def compute_china_reset_score(diplomatic_score, trade_score,
                               taiwan_counter, equity_score):
    """
    Composite: weighted sum of three signal layers, minus Taiwan counter.
    
    Weights:
      Diplomatic tone (GDELT):     35%   leading signal
      Trade normalization (GDELT): 25%   confirms words with actions
      Equity proxy (market):       40%   markets integrate all information (dominant weight)
    
    Then subtract taiwan_counter (0.0–2.0). Floor at 1.0.
    
    GSI input: china_stress = 6.0 - china_reset_score
    (High reset → low stress → GSI pulled down)
    """
    raw_reset = (
        diplomatic_score * 0.35 +
        trade_score      * 0.25 +
        equity_score     * 0.40
    )

    adjusted = raw_reset - taiwan_counter
    china_reset = min(5.0, max(1.0, adjusted))

    # Regime classification
    if china_reset >= 4.5:
        regime = "RESET_ACHIEVED"
        regime_note = "Strategic competition receding — bilateral institutions durable"
    elif china_reset >= 3.8:
        regime = "NORMALIZATION"
        regime_note = "Genuine cooperation emerging — structural issues being addressed"
    elif china_reset >= 3.0:
        regime = "MANAGED_PAUSE"
        regime_note = "Tactical truce — unresolved structural issues, reset not secure"
    elif china_reset >= 2.0:
        regime = "COLD_PEACE"
        regime_note = "No cooperation — strategic competition at full intensity"
    else:
        regime = "DETERIORATING"
        regime_note = "Active coercion or tariff escalation — GSI stress elevated"

    china_stress = 6.0 - china_reset
    delta        = china_reset - CEO_ESTIMATE_CHINA_RESET

    print("\n" + "=" * 65)
    print("PIPELINE 3: US-CHINA DIPLOMATIC RESET MONITOR")
    print("=" * 65)
    print(f"Layer 1 — Diplomatic Tone:     {diplomatic_score:.2f}/5.0  (×0.35 = {diplomatic_score*0.35:.2f})")
    print(f"Layer 2 — Trade Normalization: {trade_score:.2f}/5.0  (×0.25 = {trade_score*0.25:.2f})")
    print(f"Layer 4 — Equity Proxy:        {equity_score:.2f}/5.0  (×0.40 = {equity_score*0.40:.2f})")
    print(f"  Raw weighted reset:          {raw_reset:.2f}")
    print(f"Layer 3 — Taiwan Counter:     -{taiwan_counter:.2f}  (subtracted)")
    print(f"─" * 65)
    print(f"CHINA RESET SCORE:             {china_reset:.2f}/5.0")
    print(f"REGIME:                        {regime}")
    print(f"                               {regime_note}")
    print("=" * 65)

    ceo_label = "in line with" if abs(delta) < 0.3 else ("ABOVE" if delta > 0 else "BELOW")
    print(f"CEO estimate: {CEO_ESTIMATE_CHINA_RESET:.1f} | Pipeline: {china_reset:.2f} | delta: {delta:+.2f} ({ceo_label} estimate)")
    print(f"GSI Signal 3: china_stress = 6.0 − {china_reset:.2f} = {china_stress:.2f}")
    print(f"GSI contribution (×0.15): {china_stress * 0.15:.3f}")

    return china_reset, regime, {
        "raw_reset":   raw_reset,
        "china_stress": china_stress,
        "regime_note": regime_note,
        "delta_vs_ceo": delta,
    }


china_reset_score, china_regime, china_meta = compute_china_reset_score(
    diplomatic_score=diplomatic_score,
    trade_score=trade_score,
    taiwan_counter=taiwan_counter,
    equity_score=equity_score,
)
```

---

### Cell 8: Portfolio Protocol

```python
def print_china_reset_protocol(regime, china_reset_score, taiwan_counter, equity_meta):
    """
    Portfolio protocol: specific actions by regime.
    
    KWEB is the primary Signal 3 bellwether — the only position that requires
    Pipeline 3 to stay MANAGED_PAUSE or better to hold conviction.
    """
    print("\n━━━ PIPELINE 3 PORTFOLIO PROTOCOL ━━━")
    print(f"Regime: {regime} | Score: {china_reset_score:.2f}/5.0")
    print(f"Taiwan Counter: {taiwan_counter:.2f} | {equity_meta.get('confluence_note','')[:55]}")
    print()

    if regime == "DETERIORATING":
        print("DETERIORATING — EXIT ALL CHINA EXPOSURE")
        print("  🚨 KWEB: EXIT — thesis invalidated")
        print("  🚨 MCHI: Do not hold — country risk premium expanding")
        print("  ✓  COPX: Retain (copper supply thesis independent of China reset)")
        print("  → Cross-reference Pipeline 4: tech decoupling accelerating in parallel?")
        print("  → NEXT THRESHOLD: reset > 2.0 → place on re-entry watchlist")

    elif regime == "COLD_PEACE":
        print("COLD PEACE — NO CHINA ADDS; KWEB EXIT")
        print("  ✓ KWEB: Reduce to 0%. No conviction for China tech at this score.")
        print("  ✓ COPX: Hold global copper thesis — China demand bid uncertain")
        print("  ✓ MCHI: No position warranted")
        print("  → Strategic competition at full intensity — avoid China-specific adds")
        print("  → NEXT THRESHOLD: reset > 3.0 → MANAGED_PAUSE watch")

    elif regime == "MANAGED_PAUSE":
        print("MANAGED PAUSE — MAINTAIN STARTERS, NO ADDS")
        print("  ✓ KWEB: Hold 1–2% starter — thesis intact, reset confirmed by data")
        print("  ✓ COPX: Hold existing allocation — reset provides copper demand floor bid")
        print("  ✓ MCHI: No new entry (starter fine if held)")
        print("  → Watch: does trade board produce concrete tariff cuts? → NORMALIZATION")
        print("  → Watch: Taiwan counter trend over next 14 days")
        print("  → NEXT THRESHOLD: reset > 3.8 → size up KWEB")

    elif regime == "NORMALIZATION":
        print("NORMALIZATION — SIZE UP CHINA POSITIONS")
        print("  ⚡ KWEB: Size to 3–4% — genuine cooperation confirmed by pipeline")
        print("  ⚡ COPX: Add 1–2% — China construction demand bid strengthening")
        print("  ⚡ MCHI: Consider 1–2% starter — country risk premium compressing")
        print("  → Confirm: is MCHI leading COPX? (if yes: reset-driven, add with conviction)")
        print("  → Monitor Taiwan counter: any reading > 0.8 → pause sizing")
        print("  → NEXT THRESHOLD: reset > 4.5 → RESET_ACHIEVED full sizing")

    elif regime == "RESET_ACHIEVED":
        print("RESET ACHIEVED — FULL CHINA ALLOCATION")
        print("  ⚡ KWEB: 4–6% — China tech discount structurally eliminated")
        print("  ⚡ COPX: Full allocation — China copper demand on structural trend")
        print("  ⚡ MCHI: 2–4% — historical P/E multiple re-rating underway")
        print("  ⚡ BHP: Consider increase — iron ore demand signal confirms")
        print("  → CEO emergency session required: review full portfolio thesis")
        print("  → Confirm taiwan_counter is at 0.0 before applying full sizing")

    # Taiwan override
    if taiwan_counter >= 1.5:
        print()
        print("  ⚠  TAIWAN OVERRIDE ACTIVE")
        print(f"  Counter-score {taiwan_counter:.2f} overrides the reset regime label.")
        print("  Apply the protocol ONE LEVEL LOWER than the label above.")
        print("  Example: NORMALIZATION label → apply MANAGED_PAUSE actions.")


print_china_reset_protocol(
    regime=china_regime,
    china_reset_score=china_reset_score,
    taiwan_counter=taiwan_counter,
    equity_meta=equity_meta,
)
```

---

### Cell 9: Write to Delta Table

```python
def write_p3_to_delta(run_date, china_reset_score, china_regime,
                       diplomatic_score, trade_score, taiwan_counter, equity_score,
                       diplomatic_meta, trade_meta, taiwan_meta, equity_meta, china_meta):
    """
    Write Pipeline 3 output to Delta Lake.
    
    Alert logic:
    1. Score drop >= 0.5 vs 14-day max → alert_drop_triggered
    2. taiwan_counter >= 1.5            → alert_taiwan_triggered
    3. rare_earth_alert confirmed        → alert_rare_earth_triggered
    """
    spark.sql("CREATE DATABASE IF NOT EXISTS geopolitics")
    spark.sql("""
        CREATE TABLE IF NOT EXISTS geopolitics.pipeline3_scores (
            run_date                    DATE,
            run_timestamp               TIMESTAMP,
            china_reset_score           FLOAT,
            us_china_regime             STRING,
            diplomatic_tone_score       FLOAT,
            trade_normalization_score   FLOAT,
            taiwan_counter_score        FLOAT,
            equity_proxy_score          FLOAT,
            china_stress_for_gsi        FLOAT,
            raw_reset_before_taiwan     FLOAT,
            delta_vs_ceo_estimate       FLOAT,
            diplomatic_net_signal       FLOAT,
            diplomatic_high_value_matches INT,
            trade_raw_normalization     FLOAT,
            rare_earth_alert            BOOLEAN,
            taiwan_raw_signal           FLOAT,
            taiwan_label                STRING,
            taiwan_high_severity_matches INT,
            equity_weighted_return      FLOAT,
            mchi_14d_return             FLOAT,
            copx_14d_return             FLOAT,
            bhp_14d_return              FLOAT,
            kweb_14d_return             FLOAT,
            confluence_note             STRING,
            alert_drop_triggered        BOOLEAN,
            alert_taiwan_triggered      BOOLEAN,
            alert_rare_earth_triggered  BOOLEAN,
            regime_note                 STRING
        )
        USING DELTA
        PARTITIONED BY (run_date)
    """)

    # Score-drop alert: compare to 14-day historical max
    alert_drop = False
    try:
        prev = spark.sql("""
            SELECT china_reset_score FROM geopolitics.pipeline3_scores
            ORDER BY run_timestamp DESC LIMIT 14
        """).collect()
        if prev:
            max_prev = max(r["china_reset_score"] for r in prev)
            if max_prev - china_reset_score >= ALERT_THRESHOLD_DROP:
                alert_drop = True
                drop = max_prev - china_reset_score
                print(f"⚠  SCORE-DROP ALERT: {max_prev:.2f} → {china_reset_score:.2f} (drop: {drop:.2f})")
    except Exception:
        pass  # No history yet on first run

    alert_taiwan     = taiwan_counter >= ALERT_THRESHOLD_TAIWAN
    alert_rare_earth = bool(trade_meta.get("rare_earth_alert", False))

    row = {
        "run_date":                     run_date.strftime("%Y-%m-%d"),
        "run_timestamp":                datetime.datetime.utcnow().isoformat(),
        "china_reset_score":            float(china_reset_score),
        "us_china_regime":              china_regime,
        "diplomatic_tone_score":        float(diplomatic_score),
        "trade_normalization_score":    float(trade_score),
        "taiwan_counter_score":         float(taiwan_counter),
        "equity_proxy_score":           float(equity_score),
        "china_stress_for_gsi":         float(china_meta.get("china_stress", 6.0 - china_reset_score)),
        "raw_reset_before_taiwan":      float(china_meta.get("raw_reset", 0.0)),
        "delta_vs_ceo_estimate":        float(china_meta.get("delta_vs_ceo", 0.0)),
        "diplomatic_net_signal":        float(diplomatic_meta.get("net_diplomatic", 0.0)),
        "diplomatic_high_value_matches": int(diplomatic_meta.get("high_value_matches", 0)),
        "trade_raw_normalization":      float(trade_meta.get("raw_normalization", 0.0)),
        "rare_earth_alert":             alert_rare_earth,
        "taiwan_raw_signal":            float(taiwan_meta.get("raw_taiwan", 0.0)),
        "taiwan_label":                 taiwan_meta.get("taiwan_label", "QUIET"),
        "taiwan_high_severity_matches": int(taiwan_meta.get("high_severity_matches", 0)),
        "equity_weighted_return":       float(equity_meta.get("weighted_return", 0.0)),
        "mchi_14d_return":              float(equity_meta.get("mchi_return", 0.0)),
        "copx_14d_return":              float(equity_meta.get("copx_return", 0.0)),
        "bhp_14d_return":               float(equity_meta.get("bhp_return", 0.0)),
        "kweb_14d_return":              float(equity_meta.get("kweb_return", 0.0)),
        "confluence_note":              equity_meta.get("confluence_note", ""),
        "alert_drop_triggered":         alert_drop,
        "alert_taiwan_triggered":       alert_taiwan,
        "alert_rare_earth_triggered":   alert_rare_earth,
        "regime_note":                  china_meta.get("regime_note", ""),
    }

    df = spark.createDataFrame([row])
    df.write.format("delta").mode("append").saveAsTable("geopolitics.pipeline3_scores")

    print(f"\n✓ Written to geopolitics.pipeline3_scores")
    print(f"  Date: {row['run_date']} | Regime: {china_regime} | Score: {china_reset_score:.2f}")
    print(f"  Alerts → drop: {alert_drop} | taiwan: {alert_taiwan} | rare_earth: {alert_rare_earth}")
    return row


today       = datetime.date.today()
written_row = write_p3_to_delta(
    run_date=today,
    china_reset_score=china_reset_score,
    china_regime=china_regime,
    diplomatic_score=diplomatic_score,
    trade_score=trade_score,
    taiwan_counter=taiwan_counter,
    equity_score=equity_score,
    diplomatic_meta=diplomatic_meta,
    trade_meta=trade_meta,
    taiwan_meta=taiwan_meta,
    equity_meta=equity_meta,
    china_meta=china_meta,
)
```

---

### Cell 10: GSI v3.0 Integration and Cross-Pipeline Dashboard

```python
def compute_gsi_v30(boj_score, iran_score, export_control_score, china_reset_score):
    """
    GSI v3.0 — All four signals data-driven. Active: October 31, 2026.
    
    Weights (unchanged from v1.0 design):
      Signal 1 — BOJ carry unwind:        30%
      Signal 2 — Iran nuclear threshold:  30%
      Signal 4 — Export control:          25%
      Signal 3 — China reset (inverted):  15%
    
    china_stress = 6.0 − china_reset_score
    (15% weight reflects slow-moving variable — background modifier, not dominant driver)
    """
    china_stress = 6.0 - china_reset_score

    gsi = (
        boj_score            * 0.30 +
        iran_score           * 0.30 +
        export_control_score * 0.25 +
        china_stress         * 0.15
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

    return gsi, gsi_regime, china_stress


# ── Pull live pipeline scores from Delta (fall back to CEO estimates) ──────────
print("GSI v3.0: Reading live pipeline scores...")

try:
    BOJ_SCORE = float(spark.sql(
        "SELECT p2a_composite_score FROM geopolitics.pipeline2a_scores "
        "ORDER BY run_timestamp DESC LIMIT 1"
    ).collect()[0]["p2a_composite_score"])
    print(f"  Signal 1 — BOJ (LIVE P2-A): {BOJ_SCORE:.2f}")
except Exception:
    BOJ_SCORE = 3.8
    print(f"  Signal 1 — BOJ (estimated): {BOJ_SCORE:.2f} [P2-A live: September 12]")

try:
    IRAN_SCORE = float(spark.sql(
        "SELECT p2b_composite_score FROM geopolitics.pipeline2b_scores "
        "ORDER BY run_timestamp DESC LIMIT 1"
    ).collect()[0]["p2b_composite_score"])
    print(f"  Signal 2 — Iran (LIVE P2-B): {IRAN_SCORE:.2f}")
except Exception:
    IRAN_SCORE = 3.5
    print(f"  Signal 2 — Iran (estimated): {IRAN_SCORE:.2f} [P2-B live: October 3]")

try:
    P4_SCORE = float(spark.sql(
        "SELECT p4_composite_score FROM geopolitics.pipeline4_scores "
        "ORDER BY run_timestamp DESC LIMIT 1"
    ).collect()[0]["p4_composite_score"])
    print(f"  Signal 4 — Export Control (LIVE P4): {P4_SCORE:.2f}")
except Exception:
    P4_SCORE = 3.9
    print(f"  Signal 4 — Export Control (estimated): {P4_SCORE:.2f} [P4 deadline: August 15 — TOMORROW]")

gsi_v30, gsi_regime_v30, china_stress_val = compute_gsi_v30(
    boj_score=BOJ_SCORE,
    iran_score=IRAN_SCORE,
    export_control_score=P4_SCORE,
    china_reset_score=china_reset_score,
)

print("\n" + "=" * 65)
print("GSI v3.0 — FULLY DATA-DRIVEN COMPOSITE")
print("(Forward guidance — officially active October 31, 2026)")
print("=" * 65)
print(f"Signal 1 — BOJ:          {BOJ_SCORE:.2f}  × 0.30 = {BOJ_SCORE*0.30:.2f}")
print(f"Signal 2 — Iran:         {IRAN_SCORE:.2f}  × 0.30 = {IRAN_SCORE*0.30:.2f}")
print(f"Signal 4 — Export Ctrl:  {P4_SCORE:.2f}  × 0.25 = {P4_SCORE*0.25:.2f}")
print(f"Signal 3 — China reset:  {china_reset_score:.2f} → {china_stress_val:.2f} × 0.15 = {china_stress_val*0.15:.2f}")
print(f"─" * 65)
print(f"GSI v3.0 COMPOSITE:      {gsi_v30:.2f}/5.0")
print(f"PORTFOLIO REGIME:        {gsi_regime_v30}")
print("=" * 65)

# ── Four-Pipeline Dashboard Query ─────────────────────────────────────────────
# Run this SQL after October 31 to see all signals in one view.

DASHBOARD_QUERY = """
SELECT
    COALESCE(p2a.run_date, p2b.run_date, p3.run_date, p4.run_date) AS date,

    -- Signal 1: BOJ carry unwind
    p2a.p2a_composite_score  AS signal_1_boj,
    p2a.carry_unwind_phase   AS boj_phase,

    -- Signal 2: Iran nuclear threshold
    p2b.p2b_composite_score  AS signal_2_iran,
    p2b.iran_risk_phase      AS iran_phase,
    p2b.brent_current_usd    AS brent_usd,

    -- Signal 3: US-China reset
    p3.china_reset_score     AS signal_3_china_reset,
    p3.us_china_regime       AS china_regime,
    p3.taiwan_counter_score  AS taiwan_counter,
    p3.equity_proxy_score    AS china_equity_proxy,

    -- Signal 4: Export control bifurcation
    p4.p4_composite_score    AS signal_4_export,
    p4.bifurcation_index     AS export_bifurcation,

    -- GSI v3.0 live composite
    ROUND(
        COALESCE(p2a.p2a_composite_score, 3.8)   * 0.30 +
        COALESCE(p2b.p2b_composite_score, 3.5)   * 0.30 +
        COALESCE(p4.p4_composite_score,   3.9)   * 0.25 +
        (6.0 - COALESCE(p3.china_reset_score, 3.8)) * 0.15,
    2) AS gsi_v30_composite

FROM      geopolitics.pipeline2a_scores p2a
FULL OUTER JOIN geopolitics.pipeline2b_scores p2b
    ON p2a.run_date = p2b.run_date
FULL OUTER JOIN geopolitics.pipeline3_scores p3
    ON COALESCE(p2a.run_date, p2b.run_date) = p3.run_date
FULL OUTER JOIN geopolitics.pipeline4_scores p4
    ON COALESCE(p2a.run_date, p2b.run_date, p3.run_date) = p4.run_date
ORDER BY date DESC
LIMIT 30;
"""

print("\nFour-pipeline dashboard query (ready for October 31):")
print(DASHBOARD_QUERY)
```

---

## Key Concepts Summary

| Concept | Definition |
|---|---|
| **Inversion problem** | Signal 3 measures de-escalation; the GSI uses it as stress. `china_stress = 6.0 - china_reset_score`. High normalization → low stress → GSI pulled down. |
| **Slow vs. fast windows** | Diplomatic and trade layers use 14-day GDELT lookback. Taiwan uses 3-day. A Taiwan Strait incident terminates the reset in 72 hours; the May 2026 summit took 6 months to produce. |
| **Rare earth floor** | A confirmed rare earth / gallium / germanium export ban floors `trade_score` at 1.0 regardless of other signals. It immediately falsifies the managed pause thesis and triggers Pipeline 4 cross-reference. |
| **Equity weight dominance** | The equity layer (40%) dominates because markets integrate all available information faster than GDELT volume builds on a slow-moving variable like US-China relations. |
| **COPX disambiguation** | COPX also responds to supply disruption and USD moves unrelated to China. The four-proxy ensemble (MCHI 35%, COPX 30%, BHP 20%, KWEB 15%) detects whether the driver is China-specific. MCHI leading COPX → reset signal is real. COPX leading MCHI in isolation → supply or currency move, not reset. |
| **Taiwan override** | When `taiwan_counter >= 1.5`, apply the portfolio protocol one regime level lower than the classified label. Acute Taiwan tension structurally undermines any normalization claim. |
| **GSI v3.0** | The fully data-driven version activated October 31. All four components pipeline-derived; zero CEO judgmental estimates remain in the formula. |

---

## Investment Implications

### Current State: MANAGED_PAUSE

The CEO estimate (3.8) places the relationship at the boundary between MANAGED_PAUSE and NORMALIZATION. This is consistent with the May 2026 trade deal producing diplomatic credibility but not yet structural follow-through.

**What moves the composite score in August 2026:**

| Scenario | Expected reading | Portfolio action |
|---|---|---|
| Trade board produces concrete tariff cuts | Reset → 4.0–4.2 (NORMALIZATION) | KWEB: size to 3–4%. COPX: add 1–2%. |
| China delivers on critical minerals commitments | Reset → 4.0–4.3 (NORMALIZATION) | MCHI: consider starter alongside KWEB |
| Taiwan PLA exercises resume at scale (3d counter > 1.5) | Reset → 3.0–3.5 after Taiwan deduction | KWEB: reduce to 0%. Watch COPX. |
| Trade board stalls, tech restrictions expand | Reset → 2.5–3.0 (COLD_PEACE) | KWEB: exit. Review all China-adjacent positions. |
| China rare earth export ban | Reset → 1.0 (floor, DETERIORATING) | KWEB: exit immediately. Pipeline 4 cross-reference. |

### KWEB as Signal 3 Bellwether

The KWEB starter (1–2%) entered in prior sessions is the portfolio's active expression of Signal 3. It is the only position whose thesis is dominated by a single pipeline signal.

- Pipeline 3 MANAGED_PAUSE or NORMALIZATION → Hold or size up KWEB
- Pipeline 3 COLD_PEACE → Cut KWEB to 0%
- Pipeline 3 DETERIORATING → Full KWEB exit, no re-entry until reset resumes

This makes KWEB the most data-conditional position in the portfolio.

---

## Databricks Angle — The Equity Daily Table

Pipeline 3's equity proxy layer fetches COPX, MCHI, KWEB, and BHP directly from yfinance on each run. This works for real-time monitoring but not for historical backtesting.

**Next data engineering task (after Pipeline 4 confirmation):**

Create `geopolitics.equity_daily` — a unified daily close table for all proxy tickers across pipelines:

```python
# Notebook: equity_daily_builder.py
# Tickers: COPX, MCHI, KWEB, BHP, FRO, DHT (covers P2-B and P3 proxies)
# Frequency: daily, scheduled 5:30 UTC (before P2-A at 6:00)
# Schema: ticker, date, close, volume, 5d_return, 14d_return, 30d_return

import yfinance as yf
from pyspark.sql.functions import lag, col
from pyspark.sql.window import Window

tickers = ["COPX", "MCHI", "KWEB", "BHP", "FRO", "DHT"]

for ticker in tickers:
    hist = yf.Ticker(ticker).history(period="1y", interval="1d")
    # ... compute returns, write to geopolitics.equity_daily partitioned by ticker + date

# Once 90 days of Pipeline 3 history exists:
# Test hypothesis: GDELT US-China diplomatic_tone_score
# leads COPX forward_5d_return by 0–10 trading days.
# A correlation > 0.40 means Pipeline 3 is PREDICTIVE, not merely descriptive.
```

**Dataset to register:** `geopolitics.equity_daily` — shared asset across Pipelines 2-B and 3.

---

## Reflection Questions

**Question 1 — Regime boundary instability:**
The boundary between MANAGED_PAUSE (3.0–3.8) and NORMALIZATION (3.8+) is a cliff: a score of 3.79 triggers MANAGED_PAUSE protocol (hold KWEB at 1–2%), while 3.81 triggers NORMALIZATION (size KWEB to 3–4%). A 0.02-point difference in the composite should not generate a 2% portfolio swing. Design a hysteresis rule: the regime should only *upgrade* when the score has been above the threshold for N consecutive days, and only *downgrade* when below for M consecutive days. What are the appropriate values of N and M for a slow-moving variable like US-China relations? How does this interact with the 3-day Taiwan window, which can produce sudden score drops?

**Question 2 — The 14-day equity window and earnings contamination:**
The equity proxy uses 14-day returns for COPX, MCHI, KWEB, and BHP. Alibaba (BABA, which drives MCHI) reports quarterly earnings in August. A strong Alibaba earnings beat could push MCHI up 8–10% in a single day — triggering a NORMALIZATION regime signal from Pipeline 3 even if US-China diplomatic relations haven't changed at all. Design a filter that detects earnings-driven single-day spikes in MCHI and excludes them from the 14-day return calculation. What data source would you use to identify earnings dates? Is yfinance sufficient, or do you need a corporate calendar API?

**Question 3 — Building the COPX-GDELT predictive correlation:**
Pipeline 3's Databricks Angle describes a hypothesis: GDELT US-China diplomatic sentiment leads COPX forward 5-day returns by 0–10 trading days. After 90 days of Pipeline 3 data, Bolo runs the correlation study. The result: correlation = 0.18 (weak). Does this mean the hypothesis is wrong, or that the lag is different from 5 days? Design a systematic lag search: compute the correlation between `diplomatic_tone_score[t]` and `COPX_return[t+k]` for k = 1, 2, 3, ... 20 trading days. If you find a peak correlation of 0.42 at k = 8 (8-day lag), what are the trading implications? And what statistical test would you run to confirm this correlation is not spurious?

---

## CEO Closing Note

The complete Pipeline 3 code is now in Bolo's hands. Go-live: October 31, 2026 — 78 days.

**The immediate task is not Pipeline 3.**

Tomorrow — Saturday, August 15 — Pipeline 4 goes live. The code has been in the repository since Lesson 238. The only action required is execution: open Databricks, run the notebook, email the output to `ceo@prospectra.earth`.

The Pipeline 4 confirmation email unlocks the Signal 4 component of the GSI. Until that email arrives, the system is running on the CEO's judgmental estimate for 25% of the GSI formula. That is not good enough for a project that is supposed to demonstrate data-driven rigor.

**Engineering sequence as of August 14, 2026:**

```
August 15 (TOMORROW):   Pipeline 4 → LIVE
September 12:           Pipeline 2-A → LIVE. GSI v2.0 fully data-driven on Signal 1.
October 3:              Pipeline 2-B → LIVE. GSI v2.1 fully data-driven on Signals 1+2.
October 31:             Pipeline 3 → LIVE. GSI v3.0. All signals data-driven.
```

Every cell is written. Every pipeline is specced. The analytical system that was described in April 2026 will exist by October 31.

The only variable is Saturday.

Send the Pipeline 4 output to `ceo@prospectra.earth`.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session 249 | August 14, 2026 | Engineering Phase, Session 12*
*Pipeline 4 deadline: August 15, 2026 — TOMORROW*
*Pipeline 2-A deadline: September 12, 2026 — 29 days*
*Pipeline 2-B deadline: October 3, 2026 — 50 days*
*Pipeline 3 deadline: October 31, 2026 — 78 days*
*Next session: Pipeline 4 confirmation review + GSI v2.0 first reading*
