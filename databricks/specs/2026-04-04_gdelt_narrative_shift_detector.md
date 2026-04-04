# Spec: GDELT Narrative Shift Detector
**Date:** 2026-04-04
**Assignment:** Databricks Build — Week 1
**Target file:** `databricks/01_gdelt_narrative_shift.py`

---

## What Is This Thing?

Before any code, you need a mental model of what we are actually building and why it matters as an investment tool.

### The Core Idea

News coverage of country-pairs (e.g., US-China, Russia-Europe, Saudi Arabia-US) has a measurable **emotional tone** that shifts over time. These shifts often *precede* — or at minimum *coincide with* — policy events: sanctions, trade deals, military posturing, diplomatic ruptures.

The GDELT Narrative Shift Detector answers one question:

> **"Is the global narrative about [Country A ↔ Country B] getting warmer or colder — and is the current trajectory unusual compared to the past 30 days?"**

That question, answered systematically across a matrix of country-pairs, becomes a **macro risk signal** you can overlay against asset prices and policy event calendars.

---

## What Is GDELT?

GDELT (Global Database of Events, Language, and Tone) is a real-time open-source intelligence dataset that monitors broadcast, print, and web news in 100+ languages across virtually every country.

It has two main components relevant to us:

### 1. GDELT Event Database (GKG's cousin)
Tracks discrete geopolitical *events*: who did what to whom, where, when. Uses the CAMEO ontology (Conflict and Mediation Event Observations) to classify events into ~300 categories (verbal conflict, military action, diplomatic cooperation, etc.).

### 2. GDELT Global Knowledge Graph (GKG) — what we use
Operates at the *article* level, not the event level. For every news article ingested, GKG extracts:

| Field | What it contains |
|---|---|
| `DATE` | Publication datetime (15-minute buckets) |
| `THEMES` | Controlled vocabulary tags (e.g., `TAX_FNCACT_PRESIDENT`, `ECON_TRADE_DISPUTE`) |
| `LOCATIONS` | Countries/cities mentioned |
| `PERSONS` | Named individuals |
| `ORGANIZATIONS` | Named orgs |
| `TONE` | 6 numerical scores (see below) |
| `GCAM` | 2,000+ dimensional sentiment across dictionaries |
| `SOURCEURL` | Original article URL |

### The Tone Vector (the signal we care about)
Every GKG record includes 6 tone scores computed from the article's full text:

```
Tone, PositiveTone, NegativeTone, Polarity, ActivityReferenceDensity, SelfReferenceDensity
```

- **Tone**: overall sentiment score (positive = cooperative framing, negative = conflictual/threatening)
- **PositiveTone / NegativeTone**: split scores, useful because an article can contain both
- **Polarity**: absolute emotional intensity (ignores direction)

For narrative shift detection, we focus on **Tone** (overall) and **NegativeTone** (conflict escalation).

---

## How Country-Pair Sentiment Works

GDELT GKG doesn't natively score "US-China" as a pair. We construct it:

1. **Filter articles** where both `LOCATIONS` contain Country A and Country B (e.g., "United States" and "China")
2. **Extract Tone** from those articles
3. **Aggregate** to daily mean tone score per country-pair
4. **Compute a 30-day rolling index**: rolling mean + rolling z-score to detect statistically unusual shifts

The z-score is the key signal: if today's tone is 2+ standard deviations below the 30-day rolling mean, something anomalous is happening in the narrative — even if the absolute tone level seems normal.

---

## Architecture

```
GDELT GKG (public BigQuery / HTTP download)
         │
         ▼
[Bronze Layer] — raw GKG records in Delta table
         │
         ▼
[Silver Layer] — filtered by country-pair, exploded tone fields
         │
         ▼
[Gold Layer] — daily aggregate tone per country-pair
         │
         ▼
[Analytics Layer] — 30-day rolling mean, rolling std, z-score
         │
         ▼
[Policy Event Overlay] — join with known policy dates from a manual/enriched table
         │
         ▼
[Output] — dashboard-ready Delta table + visualization
```

### Data Source Options

| Option | Pros | Cons |
|---|---|---|
| **GDELT BigQuery public dataset** | Full history, SQL-native, fast | Requires GCP billing account |
| **GDELT 2.0 HTTP downloads** (15-min CSV files) | Free, no auth | Must handle incremental ingestion, file parsing |
| **GDELT Analysis Service (GAS)** | Pre-aggregated | Less granular, limited customization |

**For this build: GDELT 2.0 HTTP downloads ingested via Databricks Auto Loader.** This avoids GCP dependency and teaches the full ingestion pattern.

---

## Country-Pair Matrix (initial scope)

| Pair ID | Country A | Country B | Why it matters |
|---|---|---|---|
| `US_CN` | United States | China | Tech war, Taiwan risk, treasury holdings |
| `US_RU` | United States | Russia | Energy sanctions, NATO proxy conflict |
| `RU_EU` | Russia | European Union | Gas dependency, reconstruction financing |
| `CN_TW` | China | Taiwan | Semiconductor supply chain, war risk premium |
| `SA_US` | Saudi Arabia | United States | Petrodollar, OPEC+ compliance |
| `SA_CN` | Saudi Arabia | China | Petro-yuan, multipolar pivot signal |
| `IN_CN` | India | China | Border tensions, non-aligned realignment |

---

## Policy Event Calendar (overlay data)

We maintain a small seed table of known policy events to overlay on the sentiment index:

```python
policy_events = [
    {"date": "2022-02-24", "pair": "US_RU", "event": "Russia invades Ukraine"},
    {"date": "2022-10-07", "pair": "US_CN", "event": "Biden chip export controls"},
    {"date": "2023-08-11", "pair": "US_CN", "event": "Fitch US credit downgrade"},
    {"date": "2024-01-13", "pair": "CN_TW", "event": "Taiwan presidential election"},
    # ... expand over time
]
```

The overlay answers: **"Did the narrative shift precede, coincide with, or lag behind the policy event?"** That's the analytical payoff — it tells you whether markets could have had early warning.

---

## Investment Signal Logic

```
IF z_score < -2.0 AND pair = "US_CN":
    → Elevated conflict narrative → elevated risk premium on:
       - Taiwan semiconductor names (TSMC, ASML)
       - US tech exposed to China revenue (AAPL, NVDA)
       - RMB/USD exchange rate volatility

IF z_score > +2.0 AND pair = "US_CN":
    → Unusually cooperative framing → watch for:
       - Trade deal speculation
       - Chinese equities relief rally (FXI)
       - Reduced hedging cost on EM exposure
```

These rules are heuristics to start. The Databricks build will produce the data; the investment interpretation layer comes in Lesson 6 (China's Rise & Multipolar Transition).

---

## Output Schema (Gold Table)

```sql
CREATE TABLE prospectra.geopolitics.narrative_sentiment (
    date            DATE,
    pair_id         STRING,        -- e.g., 'US_CN'
    country_a       STRING,
    country_b       STRING,
    article_count   INT,           -- articles mentioning both countries
    avg_tone        DOUBLE,        -- mean Tone score
    avg_neg_tone    DOUBLE,        -- mean NegativeTone score
    rolling_30d_mean DOUBLE,
    rolling_30d_std  DOUBLE,
    z_score         DOUBLE,        -- (avg_tone - rolling_mean) / rolling_std
    is_anomaly      BOOLEAN        -- abs(z_score) > 2.0
)
USING DELTA
PARTITIONED BY (pair_id)
```

---

## What We Are NOT Building (scope control)

- We are not doing NLP from scratch — GDELT provides pre-computed tone
- We are not building a real-time streaming pipeline (batch daily is fine for Week 1)
- We are not connecting to live market data yet (that's a later build)
- We are not using BigQuery (HTTP downloads only, to avoid GCP dependency)

---

## Implementation Plan

| Step | File | Description |
|---|---|---|
| 1 | `01_gdelt_narrative_shift.py` | Full notebook: Bronze → Silver → Gold → analytics |
| 2 | (future) `02_policy_event_overlay.py` | Enrich with policy event calendar |
| 3 | (future) `03_asset_price_correlation.py` | Join sentiment index with Yahoo Finance prices |

---

## GDELT GKG File Format Reference

GKG 2.0 master files are tab-separated, one record per article. Relevant columns for our use:

```
Col 1:  GKGRECORDID
Col 2:  DATE (YYYYMMDDHHMMSS)
Col 10: LOCATIONS  (semicolon-separated; each entry: Type#Name#CountryCode#ADM1#Lat#Lon#FeatureID)
Col 15: TONE       (comma-separated: Tone,Pos,Neg,Polarity,ActivityRef,SelfRef)
```

Master file list URL pattern:
```
http://data.gdeltproject.org/gdeltv2/YYYYMMDDHHMMSS.gkg.csv.zip
```

Master index (last 15 minutes, updated every 15 min):
```
http://data.gdeltproject.org/gdeltv2/lastupdate.txt
```

Historical bulk index:
```
http://data.gdeltproject.org/gdeltv2/masterfilelist.txt
```

---

## Questions to Resolve Before Coding

1. **Date range**: Start with 2022-01-01 to present? Or a narrower window first to validate the pipeline?
2. **Databricks catalog**: What Unity Catalog catalog name are we writing to? (`prospectra`? `main`?)
3. **Compute**: Serverless SQL warehouse for ingestion, or a cluster?
4. **Volume path**: Where in Unity Catalog volumes do raw GKG files land? (e.g., `/Volumes/prospectra/raw/gdelt/`)
5. **Scheduling**: Manual trigger for now, or a Databricks Job on daily schedule?

---

*This spec is the contract. We don't write a line of implementation code until this is reviewed.*
