# Lesson 289 — Databricks Intelligence Platform Architecture: Mapping the Full Framework to a Working System

**Date:** 2026-09-02
**Session Type:** Daily Lesson
**Lesson Number:** 289 / ongoing
**Topic:** From Framework to Platform — Architecting the Geopolitical Intelligence System in Databricks
**Curriculum Arc:** Databricks Build Module — Lesson 1 (Opening the implementation sprint)

---

## Opening Question

*You now have a complete geopolitical investment framework. You know how to classify events, build intelligence pictures, construct thesis-driven positions, manage them through a lifecycle, and conduct post-mortems that compound into a better system over time.*

*Here is the uncomfortable question:*

**If someone handed you the Databricks workspace right now and said "build it" — where would you start? And more importantly: what exactly are you building toward?**

Most analysts who reach this stage have a clear mental model and a blurry system. The mental model is sophisticated. The system is a pile of notebooks with no architecture. The gap between the two is where projects stall — not for lack of intelligence, but for lack of engineering discipline applied to the right sequence.

This lesson closes that gap. We map the complete investment framework to a concrete platform architecture. Every pipeline, every table, every model, every dashboard — specified in sequence, with dependencies explicit.

The 3-month Databricks build clock is ticking. This is the blueprint.

---

## I. The Fundamental Design Question

Before writing a single line of code, answer this question:

**What decisions does this platform need to support, and for whom?**

For Prospectra, the answer is:

1. **Thesis construction** — Bolo needs to enter a new geopolitical position. The platform surfaces relevant historical analogues, current risk signals, and asset-channel correlations. It does not make the decision. It sharpens it.

2. **Position monitoring** — Live positions need ongoing thesis health scores. The platform runs the Three-Question Update Filter automatically, flags degradation, and surfaces the leading indicators Bolo defined at entry.

3. **Portfolio risk assessment** — The platform scores the aggregate portfolio for geopolitical concentration, correlation clusters, and tail-risk exposure.

4. **Briefing generation** — Weekly geopolitical intelligence briefings require event aggregation, significance scoring, and asset-class mapping. The platform automates the data layer; the CEO interprets and synthesizes.

**Everything in the architecture serves one of these four functions.** Any pipeline that doesn't map to one is out of scope.

---

## II. The Three-Layer Architecture

The platform has three layers, each building on the one below:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3 — DECISION SUPPORT                                  │
│  Dashboards / Alerts / Briefing Engine / Signal Delivery     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2 — INTELLIGENCE                                      │
│  Risk Indices / Regime Detection / Thesis Health Monitor     │
│  Asset-Channel Models / Correlation Engine / Post-Mortem DB  │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1 — DATA                                              │
│  GDELT Event Feed / FRED Macro / Yahoo Finance Prices        │
│  News Sentiment / Investment Log / Thesis Documents          │
└─────────────────────────────────────────────────────────────┘
```

**Layer 1 (Data)** is infrastructure. If Layer 1 fails, nothing works. Build this first, build it reliably, build it incrementally.

**Layer 2 (Intelligence)** is the analytical engine. This is where geopolitical framework meets data. Each component here translates a conceptual tool from the curriculum into a computable model.

**Layer 3 (Decision Support)** is the product. This is what Bolo sees and uses. It surfaces Layer 2 outputs in a form that is actionable within minutes, not hours.

**The build sequence is Layer 1 → Layer 2 → Layer 3.** This sequence is non-negotiable. Any shortcut to Layer 3 before Layer 1 is stable produces a dashboard built on sand.

---

## III. Layer 1 — Data Architecture

### 1.1 The Bronze / Silver / Gold Medallion Pattern

In Databricks, data quality is managed through three zones:

| Zone | Content | Transformation |
|---|---|---|
| **Bronze** | Raw ingested data, as-received, never modified | None |
| **Silver** | Cleaned, normalized, typed, deduplicated | Schema enforcement, null handling |
| **Gold** | Business-ready aggregated tables | Joins, feature engineering, rollups |

Every data source enters at Bronze and is promoted through Silver to Gold via structured pipelines. This ensures auditability — you can always trace any Gold metric back to the raw Bronze record.

### 1.2 Core Data Sources — Build Order

**Priority 1 (Week 1): Event and Macro Data**

| Source | What It Provides | Ingestion Method | Update Frequency |
|---|---|---|---|
| GDELT Project (GKG) | Geopolitical events, actor, tone, themes, country | Batch download via HTTP | Daily |
| FRED API | US macro indicators, yield curves, inflation, credit spreads | `fredapi` Python library | Daily |
| Yahoo Finance | Equity prices, commodity prices, FX rates, ETF prices | `yfinance` Python library | Daily |

**Priority 2 (Week 2): Derived and Proprietary Data**

| Source | What It Provides | Ingestion Method |
|---|---|---|
| Investment Log (internal) | Live positions, thesis assumptions, invalidation conditions | Delta table, manual/CEO-updated |
| Weekly Briefings (internal) | Structured event classifications from CEO sessions | Delta table, parsed from Markdown |
| GDELT GKG GoldsteinScale | Conflict intensity by country-pair | Derived from GDELT |

**Priority 3 (Weeks 3–4): Enhancement Data**

| Source | What It Provides | Ingestion Method |
|---|---|---|
| UN Comtrade | Trade flow data by country and commodity | API / bulk download |
| EIA API | Oil and gas supply, inventories, prices | EIA API (free) |
| World Bank Data | Sovereign debt, GDP, political risk ratings | `wbdata` Python library |

### 1.3 Gold Tables — The Six Core Tables

These are the analytical endpoints of Layer 1. Every Layer 2 model reads from Gold tables, never from Bronze or Silver directly.

| Gold Table | Primary Keys | Description |
|---|---|---|
| `geo_events_daily` | country, date | Daily geopolitical event counts, tone, actor types, top themes |
| `macro_indicators_daily` | indicator_code, date | US/Global macro: yields, spreads, CPI, PMI, trade balance |
| `asset_prices_daily` | ticker, date | Prices, returns, volume for target asset universe |
| `country_risk_scores` | country, date | Composite geopolitical risk score per country (Layer 2 output, stored back to Gold) |
| `investment_log` | position_id, version_date | Live position register with thesis, assumptions, invalidation conditions, P&L |
| `thesis_health_scores` | position_id, date | Weekly thesis health scores and assumption-level breakdown |

---

## IV. Layer 2 — Intelligence Architecture

Layer 2 is where the curriculum becomes code. Map each analytical module to a Databricks component:

### 2.1 Geopolitical Risk Index (GRI)

**What it does:** Produces a daily composite risk score (0–100) for each country. Inputs: GDELT event intensity, conflict escalation trend, actor network volatility, news sentiment.

**Framework source:** Lessons 1–12 (foundational framework), Lesson 64 (regime detection), Lesson 86 (risk pricing).

**Implementation:**
```python
# Databricks Notebook: intelligence/gri_calculator.py
# Reads: geo_events_daily, macro_indicators_daily
# Writes: country_risk_scores
# Schedule: Daily at 06:00 UTC after GDELT ingest completes
```

**Key design choice:** The GRI is a *relative* score — it measures deviation from a country's own baseline, not an absolute global ranking. A GRI spike of 15 points in Switzerland is more significant than a GRI spike of 15 points in Venezuela because Switzerland's baseline is low. Normalize by country.

### 2.2 Regime Change Detector

**What it does:** Identifies structural breaks in geopolitical relationships using rolling statistical tests. Flags when a country-pair relationship has shifted from stable to stressed — the precursor to supply disruptions, sanctions, and capital flow reversals.

**Framework source:** Lesson 64 (geopolitical regime detection), Lesson 71 (geopolitics of inflation), Lesson 276–284 (debt supercycle shifts).

**Implementation:**
```python
# Databricks Notebook: intelligence/regime_detector.py
# Method: CUSUM (Cumulative Sum) change point detection on GRI time series
# Reads: country_risk_scores
# Writes: regime_change_alerts
# Schedule: Weekly (structural changes are slow-moving)
```

### 2.3 Asset-Channel Correlation Engine

**What it does:** Computes rolling correlations between GRI signals (by country/theme) and asset returns (by class). Identifies which asset classes are most sensitive to geopolitical shifts in specific regions and themes. The empirical foundation of the thesis-construction process.

**Framework source:** Lesson 287 (trade construction — identifying asset channels).

**Implementation:**
```python
# Databricks Notebook: intelligence/correlation_engine.py
# Method: Rolling 90-day and 180-day correlations, lag analysis (1d, 1w, 1m)
# Reads: country_risk_scores, asset_prices_daily
# Writes: geo_asset_correlations
# Schedule: Weekly
```

**Key output:** A ranked table — for each geopolitical event type (conflict escalation, election uncertainty, sanctions imposition, trade restriction), which assets have historically shown the strongest and most consistent response, with median lag time.

### 2.4 Thesis Health Monitor

**What it does:** The automated implementation of the Three-Question Update Filter from Lesson 288. For each live position, scores each thesis assumption against current data and produces a weekly Thesis Health Score.

**Framework source:** Lesson 288 (trade lifecycle management).

**Implementation:**
```python
# Databricks Notebook: intelligence/thesis_health_monitor.py
# Reads: investment_log (live positions + assumptions), geo_events_daily, 
#         macro_indicators_daily, asset_prices_daily
# Writes: thesis_health_scores
# Logic: Rule-based scoring per assumption type:
#   - Geopolitical mechanism: GRI trend for relevant country/theme
#   - Asset channel: Rolling correlation strength
#   - Macro context: Relevant FRED indicators vs. thesis assumption
# Schedule: Weekly
```

### 2.5 Post-Mortem Database

**What it does:** Stores structured post-mortems for every closed position. Enables pattern analysis — which thesis types have been right, which failure modes recur, which asset channels have underperformed expectations.

**Framework source:** Lesson 288 (six-question post-mortem), Section 7 of PROJECT_FOUNDATION.md (investment log).

**Implementation:** This is the simplest component technically, but the most important for compounding the framework. A Delta table with a strict schema. Populated manually by CEO after each position closes. The learning machine.

---

## V. Layer 3 — Decision Support Architecture

Layer 3 is what Bolo uses. It must be fast, clear, and oriented to the four decision functions defined in Section I.

### 3.1 The Weekly Intelligence Dashboard

**Purpose:** Replace the manual weekly briefing with a data-backed synthesis. The CEO provides interpretation; the platform provides the signal landscape.

**Components:**
- World map: GRI scores by country, color-coded (green → red)
- Top 5 GRI movers (week-over-week), with GDELT event drivers
- Regime change alerts (from 2.2)
- Asset-channel heatmap: which asset classes are showing elevated geo-sensitivity this week
- Portfolio exposure overlay: how current positions are exposed to the week's risk landscape

### 3.2 The Thesis Health Dashboard

**Purpose:** Bolo opens this weekly. For each live position: current Thesis Health Score, score trend, which assumptions are degrading, leading indicators.

**Alert logic:** Push notification to Bolo if any position's Thesis Health Score drops below 6/10 or drops 2+ points in a single week.

### 3.3 The Position Construction Tool

**Purpose:** When Bolo is considering a new position, this tool surfaces the platform's relevant data. Input: event type, country, asset class. Output: historical GRI behavior for similar events, lagged asset correlations, comparable analogues from the post-mortem database.

---

## VI. Build Sequence and Milestones

### Phase 1 — Foundation (Weeks 1–3): Get Data Flowing

| Week | Task | Deliverable |
|---|---|---|
| 1 | GDELT ingest pipeline | Bronze → Silver → Gold `geo_events_daily` table updated daily |
| 1 | FRED ingest pipeline | Bronze → Silver → Gold `macro_indicators_daily` table updated daily |
| 2 | Yahoo Finance price pipeline | Bronze → Silver → Gold `asset_prices_daily` table |
| 2 | Investment log Delta table | Structured `investment_log` table with current positions |
| 3 | Data quality validation | Automated data quality tests using Databricks expectations |
| 3 | Correlation engine v1 | First asset-channel correlations from live data |

**Phase 1 success criterion:** Bolo can answer "what is today's GDELT event intensity for Saudi Arabia?" and "what is the current 90-day correlation between Saudi Arabia GRI and Brent crude?" with a Databricks query.

### Phase 2 — Intelligence (Weeks 4–8): Turn Data into Signals

| Week | Task | Deliverable |
|---|---|---|
| 4 | GRI calculator v1 | Country risk scores for top 20 geopolitically active countries |
| 5 | Regime change detector v1 | Structural break alerts from historical GDELT data |
| 6 | Thesis health monitor v1 | Manual scoring automated for 2 test positions |
| 7 | GRI backtesting | Validate GRI signals against historical commodity price moves |
| 8 | Investment log integration | Post-mortem database schema, first 5 historical entries |

### Phase 3 — Platform (Weeks 9–12): Package for Use

| Week | Task | Deliverable |
|---|---|---|
| 9 | Weekly Intelligence Dashboard (Databricks AI/BI) | Live dashboard: GRI world map + movers + asset heatmap |
| 10 | Thesis Health Dashboard | Per-position health scores with alert logic |
| 11 | Signal delivery mechanism | Weekly automated report generation |
| 12 | Track record documentation | Auditable investment log with 6+ months of entries and post-mortems |

---

## VII. Investment Implications

### Why Architecture Discipline Produces Investment Alpha

The platform architecture is not a software project. It is the operationalization of our investment edge.

**Edge 1 — Systematic frameworks applied consistently:** Layer 2 intelligence runs every week without fatigue, recency bias, or emotional response to recent P&L. This is the primary alpha source.

**Edge 2 — Long-horizon thinking:** The Regime Change Detector identifies structural shifts months before they reach consensus. The Asset-Channel Correlation Engine identifies which assets price structural shifts most efficiently. Together, they enable position construction 6–18 months ahead of the market.

**Edge 3 — Data infrastructure:** The Post-Mortem Database compounds the framework. Every closed position improves the model. This compounding effect means the platform becomes more accurate over time — an improving edge, not a static one.

**Edge 4 — Cross-domain synthesis:** The platform joins geopolitical event data with macro data with asset price data. This integration is not available from any single vendor. It is our proprietary synthesis.

---

## Databricks Angle

### The MVP Definition

The Minimum Viable Platform (MVP) — the earliest configuration that produces genuine investment signal — requires exactly:

1. `geo_events_daily` table updating reliably
2. `asset_prices_daily` table updating reliably
3. `geo_asset_correlations` computed weekly

With just these three components, Bolo can answer: *"When tension in the South China Sea spikes, which assets have historically responded, with what lag, and with what magnitude?"*

That is signal. Everything else is refinement.

**Build the MVP first. Resist the urge to build the full architecture before the MVP works.**

**Relevant datasets:**
- GDELT Project: `http://data.gdeltproject.org/gdeltv2/` (free, bulk download)
- FRED API: `https://fred.stlouisfed.org/docs/api/` (free API key)
- `yfinance` Python library (free, no key required for standard data)
- EIA API: `https://www.eia.gov/opendata/` (free)

**Immediate next action for Bolo:** Create the Databricks workspace folder structure:
```
/geopolitical-intelligence/
├── bronze/    # raw ingested data
├── silver/    # cleaned data
├── gold/      # analytical tables
├── intelligence/  # Layer 2 notebooks
└── dashboards/    # Layer 3 notebooks
```

Then build the GDELT ingest notebook. That is Week 1, Task 1. The blueprint is complete. The build begins now.

---

## Key Concepts Covered

1. **The four decision functions** — thesis construction, position monitoring, portfolio risk, briefing generation
2. **Three-layer architecture** — Data → Intelligence → Decision Support
3. **Medallion pattern** — Bronze/Silver/Gold for data quality management
4. **Six core Gold tables** — the analytical endpoints of Layer 1
5. **Five intelligence components** — GRI, Regime Detector, Correlation Engine, Thesis Health Monitor, Post-Mortem Database
6. **MVP definition** — the minimum viable configuration that produces genuine signal
7. **Build sequence** — Foundation → Intelligence → Platform, non-negotiable order

---

## Reflection Questions

1. **Architecture trade-offs:** The design prioritizes Layer 1 completeness before Layer 2, and Layer 2 completeness before Layer 3. What is the cost of violating this sequence — specifically, what breaks when you build dashboards before the data layer is stable?

2. **MVP discipline:** The MVP requires only three components (geo_events_daily, asset_prices_daily, geo_asset_correlations). What is the risk of *under-building* the MVP — stopping there without ever building the full intelligence layer?

3. **The compounding machine:** The Post-Mortem Database is described as the learning machine that compounds the framework. What specific mechanism allows past post-mortems to improve future thesis construction? How would you operationalize this in Databricks — specifically, what query would you run against the post-mortem database before constructing a new copper thesis?

---

## Questions for Next Session

- **Databricks implementation question:** The GDELT dataset is large (millions of rows per day for the full global feed). How should you approach ingesting only the geopolitically relevant subset — and what country and event-type filters produce the best signal-to-noise ratio for an investment-focused platform?
- **Architecture question:** The Thesis Health Monitor requires translating qualitative thesis assumptions ("DRC conflict disrupts copper supply") into computable rules. What is the right approach — rule-based scoring, NLP classification, or a hybrid? What are the failure modes of each?

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session: 2026-09-02 | Module: Databricks Build Module — Lesson 1 of Platform Implementation Sprint*
*Next topic: GDELT Architecture — Filtering the World's Event Stream for Investment Signal*
