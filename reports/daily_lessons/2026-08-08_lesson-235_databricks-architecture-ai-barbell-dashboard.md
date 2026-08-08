# Lesson 235: Databricks Architecture Review — Building the AI Infrastructure Barbell Dashboard
**Date:** 2026-08-08
**Session Type:** Daily Lesson
**Curriculum Position:** 235 of extended curriculum
**Series:** The Synthesis Arc — Lesson 2 of 4

---

## CEO Note

Lesson 234 completed the conceptual synthesis: six positions, a barbell thesis, four monitoring pipelines specified. That lesson did what a strategy document is supposed to do — it produced explicit, falsifiable claims.

This lesson does what an engineering document is supposed to do: it maps the architecture against reality, sequences the build, and gives Bolo a prioritized brief that can be executed this week.

The distinction between "strategy" and "engineering" is important. Most analytical projects fail not because the framework was wrong but because the monitoring infrastructure was never built, so the framework was never tested against real data. We are closing that gap now.

This lesson also answers the three spaced repetition questions from Lesson 234. All three have direct architectural implications.

---

## Opening Question

*You are the lead engineer on the Databricks build. You have been handed the barbell thesis from Lesson 234: six positions, four monitoring pipelines, four external data sources that don't yet exist in the project.*

*You have two weeks of engineering time. The Lesson 234 brief implies this pipeline architecture should eventually run. But "eventually" is not a plan.*

*Before reading further: given what you know about the project's existing infrastructure (GDELT event feed, FRED macro data, Yahoo Finance price data — all specified as Phase 1 targets in PROJECT_FOUNDATION.md), write down:*

*1. Which of the four new pipelines can be built fastest, because it reuses the most existing infrastructure?*
*2. Which pipeline, if it returned signal in the next 30 days, would most directly validate or invalidate the position you are least confident about?*
*3. Are those the same pipeline — or a different one? If different, which do you build first?*

*Your answer to question 3 is your architecture priority. Write it before reading.*

---

## 1. Spaced Repetition: NVIDIA and the Barbell

**From Lesson 234:** *Is NVIDIA a barbell company (benefits from all layers), or is its valuation most exposed to middle-layer pressure?*

This question requires surgical precision, because the sloppy answer ("NVIDIA is everywhere, so it benefits everywhere") is wrong — and the overcorrected answer ("NVIDIA's CUDA is middle-layer, so it's at risk") misidentifies the primary moat.

### The Correct Framing

NVIDIA's business has three components that map imperfectly onto the barbell:

**Component 1: GPU Hardware (Physical Layer)**
This is NVIDIA's primary economic engine. Data center GPU revenue (~$35B+ annualized in 2026) comes from selling H100s, H200s, and Blackwell chips to hyperscalers, government customers, and enterprises. This is physical-layer revenue — it earns whether the customer uses the chips to run a closed model, an open-source model, or their own fine-tuned model. Open-source AI does *not* reduce demand for NVIDIA GPUs; if anything, it increases GPU demand because open-source models require compute-side investment to close the capability gap. Every Llama fine-tuning run and every DeepSeek R2 inference query runs on GPU silicon.

**Component 2: CUDA Software Ecosystem (Stickiness Amplifier)**
CUDA is not a "middle layer" in the sense that frontier model API providers are middle layer. CUDA is a lock-in mechanism that makes NVIDIA GPUs more defensible than the hardware specifications alone. The switching cost from CUDA to ROCm (AMD) or OneAPI (Intel) is high enough that most AI workloads stay on NVIDIA even when AMD hardware is competitive on raw compute. This is not the middle-layer risk — closed model API providers have weak switching costs (you can call a different API). CUDA has very high switching costs.

The medium-term risk to CUDA is not open-source AI commoditization. It is the rise of RISC-V based accelerators (e.g., China's Cambricon, or emerging eFPGA architectures) and the possibility that the next-generation AI workload (sparse transformers, neuromorphic architectures) does not map efficiently to the CUDA programming model. This is a 7–10 year risk, not a 3-year risk.

**Component 3: NIM Microservices and Enterprise Software (Emerging Middle-Layer Exposure)**
NVIDIA is building an enterprise AI software layer — NVIDIA AI Enterprise, NIM microservices, DGX Cloud — that is genuinely in the middle layer. These products package model deployment and optimization tooling and compete with cloud-native AI deployment services. This is the smallest revenue segment and the highest-risk one under the barbell thesis.

### CEO Verdict: NVIDIA Is a Physical-Layer Asset With a Stickiness Amplifier

The barbell thesis does not argue against NVIDIA. It argues against companies whose *primary moat is model API access*. NVIDIA's primary moat is GPU hardware, amplified by CUDA switching costs. The enterprise software segment is a small and growing middle-layer exposure, but it is not yet material to the investment thesis.

**The correct view:** NVIDIA at current valuations embeds two risk premia that are real but manageable on a 3-year horizon: (1) parallel hardware ecosystem development (Huawei Ascend, domestic RISC-V accelerators reducing China revenue), and (2) a shift in AI workload architecture away from dense transformer models that heavily favor NVIDIA's memory bandwidth and CUDA programming model. Neither risk materializes in the next 12–18 months. On a 6–18 month thesis horizon, NVIDIA is a physical-layer long, not a middle-layer avoid.

**Barbell classification: Physical Layer — Long. Conditional on monitoring the parallel hardware ecosystem risk.**

---

## 2. Spaced Repetition: Pipeline Infrastructure Overlap Analysis

**From Lesson 234:** *Which of the four new pipelines has the most overlap with existing infrastructure — and which requires entirely new data source connections?*

This is both a technical question and a strategic one. The answer determines which pipeline gets built first.

Let me map each pipeline against the three existing Phase 1 data sources:

| Pipeline | Overlap with GDELT | Overlap with FRED | Overlap with Yahoo Finance | Net Assessment |
|---|---|---|---|---|
| **1. Power Demand Signal Monitor** (EIA, PJM/MISO, EPA) | GDELT can scrape PPA news announcements — partial overlap | EIA data format is similar to FRED (time series, API-based) — structural overlap, not data overlap | Power utility stock prices already available — price signal present | **Moderate overlap.** EIA ingestion is a FRED-pattern reuse. GDELT covers the news layer. New: EIA API connection, grid operator data. |
| **2. Government AI Procurement Tracker** (USASpending.gov, SAM.gov, Federal Register) | GDELT captures major contract news — marginal overlap only | None | Defense contractor prices available — price signal present | **Low overlap.** All three primary data sources are new. USASpending.gov has a clean REST API, but the data model is entirely different from anything in Phase 1. |
| **3. Open-Source Capability Gap Tracker** (Hugging Face, ArXiv, LM-sys) | None | None | Pure-play AI company stocks available — price signal marginal | **Minimal overlap.** All three primary sources are entirely new. No Phase 1 infrastructure applies. This is the most greenfield pipeline. |
| **4. Export Control Tightening Radar** (Federal Register, BIS filings, trade data via Census/UN Comtrade) | **GDELT is a primary source here** — export control events, BIS announcement coverage, trade policy news are core GDELT event types | None | Chip stocks (NVDA, ASML, AMAT) already available via Yahoo Finance — price reaction data present | **Highest overlap.** GDELT already processes the news events this pipeline needs. New: Federal Register API connection, Comtrade trade flow data. |

### The Answer

**Pipeline 4 (Export Control Tightening Radar)** has the most overlap with existing infrastructure — GDELT is its primary signal source, and Yahoo Finance already captures the chip stock price reactions. The delta to build is:
1. A Federal Register API filter for BIS (Bureau of Industry and Security) filings
2. A UN Comtrade or Census Bureau API connection for Singapore/Malaysia/UAE chip import anomaly detection
3. A signal scoring function that combines GDELT event tone + Federal Register filing velocity + chip re-export volume into a single export control tightening score

**Pipeline 3 (Open-Source Capability Gap Tracker)** requires the most entirely new infrastructure — Hugging Face API, ArXiv metadata parser, LM-sys Chatbot Arena scraper, and a benchmark normalization layer. It is the most complex build and the most greenfield.

---

## 3. Spaced Repetition: The Audit Question

**From Lesson 234 (Synthesis Arc Checkpoint):** *After Lesson 237, the audit question: "Was the framework right?" or "Were the specific calls right?"*

This is a methodological question with a methodological answer.

**The wrong approach:** Answer either question in isolation.

- "Were the specific calls right?" answered in isolation tells you nothing about whether you were right *for the right reasons*. A call can be right because of a lucky macro event that your framework didn't predict. A call can be wrong because of a Black Swan that no framework could have predicted. Outcome-only attribution is how investors develop false confidence in broken frameworks.

- "Was the framework right?" answered in isolation is unfalsifiable. Frameworks are abstract. A framework can always be post-hoc rationalized to explain any outcome. If you don't anchor the framework evaluation to specific predictions, the audit is a narrative exercise, not an analytical one.

**The correct approach — a two-stage audit:**

**Stage 1 — Call-Level Audit:**
For each investment log entry from the past 12 months, answer three questions:
1. Was the call directionally correct at the stated time horizon?
2. Was the *reasoning* sound given information available at the time of the call? (Not: was the reasoning correct in hindsight.)
3. If the call was wrong: was it wrong because of a framework error (we misunderstood the mechanism), a data error (we had wrong inputs), or a random event (unpredictable exogenous shock)?

**Stage 2 — Framework-Level Audit:**
Aggregate the call-level findings:
- What percentage of calls were right for the right reasons?
- Are the errors clustered by framework element (e.g., "we consistently overestimated geopolitical risk premium compression timelines")?
- Which framework element — if corrected — would have produced the largest improvement in call accuracy?

**The audit order:** Stage 1 first, Stage 2 synthesized from Stage 1. The framework verdict is a function of the call-level findings, not independent of them.

**CEO Note on Lesson 237:** This audit methodology will be the explicit structure of Lesson 237. The audit is not a retrospective; it is a calibration exercise that improves Lesson 238 and beyond.

---

## 4. The Architecture Review — Build Priority and Technical Brief

With the infrastructure overlap analysis complete, here is the full architecture brief for the AI Infrastructure Barbell Dashboard in Databricks.

### Priority Order

**Build order: 4 → 1 → 2 → 3**

This priority balances two criteria: (a) fastest time to first signal, and (b) most direct thesis validation. The order is not arbitrary — it is the sequence that produces maximum intelligence within 30 days given existing infrastructure.

| Priority | Pipeline | Rationale |
|---|---|---|
| **1st** | Pipeline 4: Export Control Tightening Radar | GDELT already running. Add BIS Federal Register filter + Comtrade. First signal in 5–7 days. Validates the China-avoid position with the shortest thesis horizon. |
| **2nd** | Pipeline 1: Power Demand Signal Monitor | EIA API mirrors FRED pattern — low implementation complexity. PPA news coverage already in GDELT. Validates the CEG/VST/GEV long thesis. First signal in 10–14 days. |
| **3rd** | Pipeline 2: Government AI Procurement Tracker | USASpending.gov has a clean API. New data model but well-documented. Validates the PLTR/BAH/LDOS thesis. First signal in 14–21 days. |
| **4th** | Pipeline 3: Open-Source Capability Gap Tracker | Most complex. Requires Hugging Face API + ArXiv parser + LM-sys scraper + benchmark normalization. Validates the middle-layer avoid thesis with the longest horizon. First signal in 21–30 days. |

### Architecture Diagram — The AI Infrastructure Barbell Dashboard

```
╔══════════════════════════════════════════════════════════════════════╗
║          AI INFRASTRUCTURE BARBELL DASHBOARD — DATABRICKS            ║
║                       Unity Catalog Layer                            ║
╚══════════════════════════════════════════════════════════════════════╝

INGEST LAYER (Bronze)
─────────────────────────────────────────────────────────────────────

  [GDELT Feed]          [EIA API]         [USASpending.gov]  [HuggingFace API]
  (existing Phase 1)    (new — EIA v2)    (new — USASpend)   (new — HF Hub)
       │                    │                    │                  │
       │               [FRED API]          [SAM.gov API]      [ArXiv API]
  (existing Phase 1)    (existing P1)      (new — SAM)        (new — ArXiv)
       │                    │                    │                  │
  [Yahoo Finance]       [EPA EGRID]        [Fed Register]     [LM-sys Chatbot]
  (existing Phase 1)    (new — EPA API)    (new — FR API)     (new — scraper)
       │                    │                    │                  │
  [UN Comtrade API]         │           [Congress.gov API]         │
  (new — trade data)        │            (new — bill tracker)      │
       │                    │                    │                  │
       ▼                    ▼                    ▼                  ▼

PIPELINE TABLES (Bronze → Silver)
─────────────────────────────────────────────────────────────────────

  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
  │  PIPELINE 4     │  │  PIPELINE 1      │  │  PIPELINE 2  │  │  PIPELINE 3      │
  │  Export Control │  │  Power Demand    │  │  Gov't AI    │  │  Open-Source     │
  │  Tightening     │  │  Signal Monitor  │  │  Procurement │  │  Capability Gap  │
  │  Radar          │  │                  │  │  Tracker     │  │  Tracker         │
  │                 │  │                  │  │              │  │                  │
  │ Signals:        │  │ Signals:         │  │ Signals:     │  │ Signals:         │
  │ - BIS filing    │  │ - DC % of grid   │  │ - AI award   │  │ - OS vs closed   │
  │   velocity      │  │   demand (weekly)│  │   velocity   │  │   benchmark gap  │
  │ - GDELT export  │  │ - Nuclear util   │  │ - Vendor     │  │ - China model    │
  │   event tone    │  │   rate (%)       │  │   market     │  │   parity index   │
  │ - SG/MY/AE chip │  │ - PPA news       │  │   share      │  │ - Download       │
  │   re-export vol │  │   announcement   │  │ - New entrant│  │   velocity       │
  │ - Congress bill │  │   count          │  │   threshold  │  │ - Model release  │
  │   progress      │  │ - Utility stock  │  │ - DOD budget │  │   cadence        │
  │                 │  │   implied power  │  │   allocation │  │                  │
  │ Score: 1–5      │  │   demand premium │  │              │  │ Score: 1–5       │
  │ (tight → loose) │  │ Score: 1–5       │  │ Score: 1–5   │  │ (gap → parity)   │
  └────────┬────────┘  └────────┬─────────┘  └──────┬───────┘  └────────┬─────────┘
           │                   │                    │                   │
           └───────────────────┴────────────────────┴───────────────────┘
                                          │
                                          ▼

THESIS SCORING LAYER (Silver → Gold)
─────────────────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────────────────────┐
  │                    BARBELL THESIS SCORECARD                        │
  │                                                                    │
  │  Position               Pipeline(s)    Score    Status             │
  │  ─────────────────────────────────────────────────────────────     │
  │  CEG/VST/GEV (Long)     P1             1–5      [██████░░░░] 6/10  │
  │  PLTR/BAH/LDOS (Long)   P2             1–5      [████░░░░░░] 4/10  │
  │  SNOW/Databricks (Long) P2+P3          1–5      [████░░░░░░] 4/10  │
  │  CRWD/PANW (Long)       P4+P2          1–5      [███████░░░] 7/10  │
  │  Frontier API (Avoid)   P3             1–5      [████████░░] 8/10  │
  │  China AI (Avoid)       P4             1–5      [█████████░] 9/10  │
  │                                                                    │
  │  COMPOSITE BARBELL SCORE: [computed weekly]                        │
  │  LAST UPDATED: [pipeline run timestamp]                            │
  └────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼

ALERT LAYER
─────────────────────────────────────────────────────────────────────

  When ≥2 pipeline scores cross threshold → generate position review alert
  → Write to reports/investment_log.md (alert entry)
  → Email to franjmartin21@gmail.com (weekly digest)
  → Flag in Databricks AI/BI dashboard (visual)

```

---

## 5. Technical Specifications — What Bolo Builds This Week

### Immediate Build: Pipeline 4 (Export Control Tightening Radar)

**Time estimate:** 5–7 days to first signal.

**Step 1 — Federal Register API Filter (Days 1–2)**

The Federal Register has a public REST API (`https://www.federalregister.gov/api/v1/`) with no authentication required. The filter needed:

```python
# Databricks notebook — Federal Register BIS Monitor
import requests
from datetime import datetime, timedelta

BASE_URL = "https://www.federalregister.gov/api/v1/articles"

def fetch_bis_filings(days_back=7):
    """Fetch BIS export control rule filings from the past N days."""
    since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    params = {
        "conditions[agencies][]": "commerce-bureau-of-industry-and-security",
        "conditions[publication_date][gte]": since_date,
        "fields[]": ["title", "publication_date", "abstract", "html_url", 
                     "document_number", "type"],
        "per_page": 100,
        "order": "newest"
    }
    
    response = requests.get(BASE_URL, params=params)
    filings = response.json().get("results", [])
    
    # Score: count filings per week as velocity metric
    return {
        "filing_count": len(filings),
        "filing_velocity_score": min(5, len(filings) // 2 + 1),
        "filings": filings
    }
```

**Step 2 — GDELT Export Control Event Filter (Days 1–2, extend existing pipeline)**

Add a GDELT event filter to the existing GDELT feed for export control event codes. GDELT CAMEO codes relevant to export controls:
- `0233`: Appeal to engage in material cooperation
- `1631`: Impose economic sanctions
- `1633`: Impose restrictions on imports/exports
- `1634`: Impose travel restrictions (proxy for diplomatic hostility)
- `163`: Impose blockade/restriction

Add a filter to the existing GDELT pipeline that extracts events where `ActionGeo_CountryCode IN ('US', 'CH')` AND `EventCode IN ('1631', '1633', '1634')` — this captures US export restriction events targeted at China.

**Step 3 — Comtrade Trade Flow Monitor (Days 3–5)**

UN Comtrade API (free tier, 100 requests/hour) for chip re-export anomaly detection:

```python
# Target commodities: HS codes for semiconductors
# 8542: Electronic integrated circuits
# 8471: ADP machines (proxy for server/GPU shipments)

TARGET_COUNTRIES = {
    "SGP": "Singapore",  # Major re-export hub
    "MYS": "Malaysia",   # Penang semiconductor corridor
    "ARE": "UAE",        # Dubai gray market proxy
    "VNM": "Vietnam"     # Emerging re-export route
}

TARGET_HS_CODES = ["8542", "8471"]
REPORTER_USA = "842"  # US as reporter
FLOW_EXPORT = 2       # Export flow
```

Query: US exports of 8542/8471 to each target country, monthly, comparing to 24-month average. Anomaly = +2 standard deviations from mean in the 6 months following a new export control round. This is the gray market detection signal.

**Step 4 — Signal Scoring Function (Days 5–7)**

```python
def compute_export_control_score(
    bis_filing_velocity,    # filings/week (0–10+)
    gdelt_event_tone,       # average tone of export control events (-10 to +10)
    reexport_anomaly_score, # z-score of re-export volume vs. baseline
    congress_bill_stage     # 0=no bill, 1=introduced, 2=committee, 3=floor, 4=enacted
):
    """
    Returns 1–5 score where:
    1 = Export controls loosening (détente signal)
    3 = Baseline (no change)
    5 = Export controls tightening aggressively (China-avoid thesis strengthening)
    """
    velocity_score = min(5, max(1, bis_filing_velocity / 2))
    tone_score = 5 - min(4, max(0, (gdelt_event_tone + 10) / 5))  # negative tone → high score
    reexport_score = min(5, max(1, 3 + reexport_anomaly_score))    # high anomaly → gray market → still flowing → lower avoid signal
    bill_score = congress_bill_stage + 1
    
    # Weight: BIS filings most important, tone second, bill stage third, re-export as modifier
    composite = (velocity_score * 0.35 + tone_score * 0.30 + 
                 bill_score * 0.25 + (5 - reexport_score) * 0.10)
    
    return round(composite, 1)
```

### Week 2 Build: Pipeline 1 (Power Demand Signal Monitor)

**Step 1 — EIA API Connection**

EIA has a public API (`https://api.eia.gov/v2/`) requiring a free API key. Key endpoint: `electricity/rto/region-data` for real-time grid demand by region (PJM, MISO, ERCOT, WECC). Weekly data sufficient for thesis monitoring.

The FRED API pattern in the existing Prospectra codebase should map directly — both are time series REST APIs with similar response structures.

**Step 2 — Nuclear Utilization Scraper**

EIA's `electricity/electric-power-operational-data` endpoint provides monthly plant-level generation data by fuel type. Filter for nuclear plants. Utilization rate = actual generation / maximum capacity.

**Step 3 — PPA News Filter from GDELT**

GDELT Global Knowledge Graph (GKG) theme filter for power purchase agreements. GDELT GKG theme: `ECON_ENERGYCOMPANY` + `ENV_NUCLEARPOWER` within 30-word window. Count of co-occurrence in US news = PPA announcement proxy.

---

## 6. Databricks Angle — The 30-Day Build Plan

**Week 1 (August 8–15):**
- Pipeline 4: Federal Register API + GDELT export control filter + Comtrade connection
- Deliverable: First export control tightening score by August 15

**Week 2 (August 15–22):**
- Pipeline 1: EIA API connection + nuclear utilization query + PPA GDELT filter
- Deliverable: First power demand signal score by August 22

**Week 3 (August 22–29):**
- Pipeline 2: USASpending.gov API + SAM.gov connection + Federal Register AI policy filter
- Deliverable: First government procurement score by August 29

**Week 4 (August 29 – September 5):**
- Pipeline 3: Hugging Face API + ArXiv metadata + LM-sys scraper + benchmark normalization
- Deliverable: First open-source capability gap score by September 5

**Dashboard integration (September 5–12):**
- Unity Catalog consolidation of all four pipeline outputs
- Barbell Thesis Scorecard table in Gold layer
- Alert logic (email trigger when ≥2 signals cross threshold)
- Databricks AI/BI dashboard visualization

**Target completion: September 12 — the dashboard goes live with real data.**

This is the moment the project transitions from framework to evidence. Lesson 236 (scheduled for next week) will review the first pipeline outputs and interpret the initial signals.

---

## 7. Investment Implications

The architecture review has a direct investment implication beyond the portfolio positions: **the dashboard itself is a testable hypothesis about information advantage.**

If the four pipelines — once live — produce signal that consistently leads asset price movements by 5–15 days, we have established that: (a) the data sources are informative, (b) our signal construction is sound, and (c) the geopolitical framework correctly identifies which data matters. That is a strong foundation for the Goal 3 (commercial product) evaluation in Q4 2026.

If the pipelines produce signal that does not lead price movements, we learn something equally valuable: either the data is noisier than expected, the market is already pricing these signals efficiently, or our signal construction requires revision. A negative result is not a failure — it is calibration.

**The critical discipline:** Don't adjust signal construction after observing prices. That is data mining, not signal development. The pipeline scoring functions defined in Section 5 are committed before we see the first output. They can be revised after a formal review in Lesson 237, with explicit documentation of what changed and why.

---

## 8. Reflection Questions

1. **The scoring functions in Section 5 use specific weights (e.g., BIS filing velocity = 35% of export control score). Those weights are constructed from first principles — not from statistical estimation. In quantitative finance, weights derived from first principles are called "prior beliefs" in a Bayesian framework. As we accumulate 30–60 days of pipeline data, we will be able to estimate the empirical relationship between each sub-signal and asset price movements. At what point — how many data points, over what time horizon — would you feel comfortable replacing the first-principles weights with empirically estimated weights? What is the risk of moving too early?**

2. **The Comtrade chip re-export anomaly detection uses Singapore, Malaysia, UAE, and Vietnam as proxy countries for gray market chip flows. This works if the gray market routes are stable. But gray market supply chains adapt — if monitoring of these four countries increases pressure, the routes shift to Turkey, India, or Gulf states not on our list. How would you design a monitoring system that detects new routing channels as they emerge, rather than hard-coding the four current proxy countries?**

3. **The 30-day build plan asks Bolo to connect four entirely new data sources and build four pipeline scoring functions while the existing Phase 1 infrastructure (GDELT, FRED, Yahoo Finance) is presumably still running. In practice, is it better to build all four new pipelines in parallel (faster, but splits engineering attention), or serially in the priority order defined here (slower to full coverage, but each pipeline is properly validated before the next begins)? How do you resolve the tension between speed-to-signal and signal quality?**

---

## Questions for Next Session (Spaced Repetition)

- *From this lesson:* The Federal Register API filter in Section 5 queries BIS filings by agency. Before Lesson 236, explore the Federal Register API docs and identify: (a) whether the API supports filtering by document type (proposed rule vs. final rule — the distinction matters for signal timing), and (b) what the average lag is between a proposed rule and a final rule for export control filings historically.

- *From this lesson:* The barbell dashboard's alert logic triggers when "≥2 pipeline scores cross threshold." We did not define what "cross threshold" means quantitatively. Before Lesson 236, propose a threshold definition: what score level (e.g., above 4.0 of 5.0), what directional movement (e.g., a one-week change of ≥1.0), and what confirmation window (single reading vs. two consecutive readings) should constitute an alert trigger?

- *Synthesis Arc checkpoint:* Lesson 236 will review the first pipeline outputs. If Pipeline 4 (Export Control) returns a score of 4.5 — strongly signaling tightening — in its first week, would you immediately increase conviction on the China-avoid position, or wait for confirmation from a second pipeline reading? What is the decision rule for acting on a first-run signal before you have calibration data?

---

## Series Progress: The Synthesis Arc

**Synthesis Arc — Lessons:**
- ✅ Lesson 234: From AI Infrastructure Framework to Explicit Portfolio Positions
- ✅ Lesson 235: Databricks Architecture Review — Building the AI Infrastructure Barbell Dashboard *(this lesson)*
- ⬜ Lesson 236: Live Signal Generation — Reading the First Pipeline Outputs
- ⬜ Lesson 237: Track Record Documentation and Framework Audit (12-Month Milestone)

**CEO Directive to Bolo:** Begin Week 1 of the 30-day build plan immediately. The Federal Register API and the GDELT export control filter extension are the first two tasks — both can be completed in parallel within 48 hours. The first score should be in your hands by August 15. If you hit a technical blocker on the Comtrade API (rate limits, data format issues), flag it directly and we will substitute Census Bureau USA Trade Online data as an alternative.

The 3-month clock noted in PROJECT_FOUNDATION.md expires in approximately 4 weeks. We have frameworks. We have positions. We need data. The build starts now.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session delivered: 2026-08-08 | Lesson 235 of extended curriculum | Synthesis Arc, Lesson 2 of 4*
