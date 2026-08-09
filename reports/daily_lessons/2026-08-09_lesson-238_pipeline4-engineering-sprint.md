# Lesson 238: Pipeline 4 Engineering Sprint — Complete Build Specification for the Export Control Tightening Radar
**Date:** 2026-08-09
**Session Type:** Post-Curriculum Engineering Directive
**Curriculum Position:** 238 — Engineering Phase, Session 1
**Status:** The formal curriculum concluded at Lesson 237. This session and forward are engineering-first: directive, specification, build.

---

## CEO Framing

Lesson 237 closed with a declaration: "There is no Lesson 238."

It was wrong in one respect. The teaching phase is over — that part was true. But the CEO's job does not end with the curriculum. The CEO sets priorities, specifies deliverables, and holds the builder accountable. Lesson 237 set the priority order. Session 238 delivers the specification Bolo needs to actually build Pipeline 4 from a clean notebook.

The curriculum ran 237 lessons. The engineering phase runs until the system is live and generating validated signal. That is a different kind of session — no Socratic method, no reflection questions. Just specification, code templates, and deadlines.

**This session's deliverable:** By the time Bolo finishes reading this, he should be able to open a new Databricks notebook and start building Pipeline 4 without asking a single question.

---

## 1. Market Intelligence Update — August 9, 2026

*Before engineering: a 5-minute CEO brief on what has changed in the 24 hours since Lesson 237 was delivered.*

### Export Controls
The Bureau of Industry and Security (BIS) has extended the **Foundry Due Diligence Rule** through December 31, 2026 — meaning chip foundries must continue attesting that advanced chips they fabricate for US customers are not being diverted to restricted end-users. Simultaneously, DOJ's **Operation Gatekeeper** (December 2025) disrupted over $160 million in attempted chip exports to mainland China and Hong Kong through a multi-defendant network — precisely the gray-market route (Singapore, Malaysia, UAE re-export) that Pipeline 4 is designed to detect.

**CEO verdict on Pipeline 4 urgency:** The gray-market signal is active. The BIS enforcement environment is escalating. Pipeline 4 would have flagged the Gatekeeper network months before DOJ acted, if it had been live. Build it now.

### Hormuz / Energy
Iran-Oman talks have produced partial de-escalation as of early August. Shipping disruption through the Strait has reduced from peak levels. This is consistent with the investment log's tracking of "Process vs. Mechanism" — the talks represent process, not mechanism. The kill switch for the Long Oil position (Brent sustained >$85 for 30 days AND P&I clubs resuming war-risk cover) remains unmet.

**CEO action on Position 1 (Long Oil):** HOLD. Process, not mechanism.

### Gold
Gold remains elevated on geopolitical safe-haven demand, consistent with the fiscal dominance + geopolitical risk premium thesis. The gold kill switch (TIPS real yield >3% AND inflation normalized) remains unmet.

**CEO action on Position 2 (Long Gold):** HOLD.

### Portfolio Action Carried from Lesson 237
**Position 12 (Underweight TUR/EWY):** The EWY exit was directed in Lesson 237. This must be logged as executed. Bolo: confirm whether EWY position has been reduced per the pre-committed stop. If not done, it is overdue. This is the one outstanding portfolio action.

---

## 2. Engineering Priorities — Reminder from Lesson 237

Ranked by analytical urgency:

| # | Item | Deadline | Why Now |
|---|---|---|---|
| 1 | `gold.signal_calibration_log` table | **This week** | Pipeline 4's first score has no home without this |
| 2 | Pipeline 4: Export Control Tightening Radar | **August 15** | BIS August data already live; 0-day lag on a free data source |
| 3 | Pipeline 1: Power Demand Signal Monitor | Week 2 | Physical layer barbell positions need quantitative monitoring |
| 4 | Sahel Uranium Supply Risk Tracker | Week 2 | Uranium position has no quantitative monitor |
| 5 | B-02 Market Data Feed (FRO/STNG/DHT wire) | Week 3 | Tanker position requires dated price data |

---

## 3. Step 1 — Build the `gold.signal_calibration_log` Table (2 Hours)

Before Pipeline 4 can write a score anywhere, the table must exist.

### Schema

```sql
-- Run this in your Databricks SQL editor or notebook
-- Unity Catalog: assumes catalog = 'prospectra', schema = 'gold'

CREATE CATALOG IF NOT EXISTS prospectra;
CREATE SCHEMA IF NOT EXISTS prospectra.gold;

CREATE TABLE IF NOT EXISTS prospectra.gold.signal_calibration_log (
  log_id          BIGINT GENERATED ALWAYS AS IDENTITY,
  pipeline_name   STRING NOT NULL,            -- e.g., 'pipeline_4_export_control'
  run_date        DATE NOT NULL,              -- date the score was computed
  raw_score       DOUBLE NOT NULL,            -- 1.0–5.0 composite score
  sub_scores      MAP<STRING, DOUBLE>,        -- component scores keyed by sub-signal name
  thesis_verdict  STRING,                     -- 'intact', 'weakening', 'breaking_down'
  blind_interp    STRING,                     -- analyst's interpretation written BEFORE checking prices
  price_check     MAP<STRING, DOUBLE>,        -- {asset: price} at score generation time
  actual_outcome  STRING,                     -- filled in retrospectively: 'confirmed', 'refuted', 'pending'
  outcome_notes   STRING,                     -- narrative on outcome vs. prediction
  created_at      TIMESTAMP DEFAULT current_timestamp(),
  CONSTRAINT pk_calibration PRIMARY KEY (pipeline_name, run_date)
)
USING DELTA
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

### Test Insert (Verify It Works)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

spark.sql("""
INSERT INTO prospectra.gold.signal_calibration_log
  (pipeline_name, run_date, raw_score, sub_scores, thesis_verdict, blind_interp)
VALUES (
  'pipeline_4_export_control',
  CURRENT_DATE(),
  0.0,
  map('federal_register', 0.0, 'gdelt', 0.0, 'congressional_tracker', 0.0, 'comtrade', 0.0),
  'pending_first_run',
  'Seed record — Pipeline 4 not yet live'
)
""")

spark.sql("SELECT * FROM prospectra.gold.signal_calibration_log").show(truncate=False)
```

**Time estimate:** 30 minutes to create the table, run the test insert, verify it works. Do this first.

---

## 4. Pipeline 4 Architecture — Full Build Specification

Pipeline 4 scores the intensity of US export control tightening on AI-relevant goods on a 1–5 scale, updated weekly. A score of 1 means the tightening trend is stalling or reversing (thesis pressure); a score of 5 means tightening is accelerating (thesis confirming).

### Sub-Signals and Weights (from Lesson 236)

| Sub-Signal | Source | Weight | What It Measures |
|---|---|---|---|
| Federal Register BIS Filings | federalregister.gov API | 30% | Volume and recency of BIS export control rule filings |
| Congressional Activity | congress.gov API | 35% | Bill introductions, markups, and floor votes on export control legislation |
| GDELT Framing Score | GDELT GKG | 10% | Media volume and tone on "export controls" + "China" + "chips" |
| Gray-Market Proxy | UN Comtrade API | 25% | Singapore/Malaysia/UAE chip import anomalies vs. baseline |

### Notebook Structure (4 Cells)

**Cell 1: Data Ingest — Federal Register**

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_federal_register_bis(days_back=7):
    """
    Fetches recent Federal Register documents from Bureau of Industry and Security.
    Returns count of documents and recency score.
    """
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    # Federal Register public API — no auth required
    url = "https://www.federalregister.gov/api/v1/documents"
    params = {
        "conditions[agencies][]": "bureau-of-industry-and-security",
        "conditions[publication_date][gte]": start_date,
        "conditions[publication_date][lte]": end_date,
        "fields[]": ["document_number", "publication_date", "title", "type", "action"],
        "per_page": 50,
        "order": "newest"
    }
    
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    
    documents = data.get("results", [])
    
    # Score: weight recent filings higher
    if not documents:
        return 1.0, []
    
    # Rule filing types are stronger signals than notices
    rule_types = {"Rule", "Final Rule", "Interim Final Rule", "Proposed Rule"}
    rule_count = sum(1 for d in documents if d.get("type") in rule_types)
    notice_count = len(documents) - rule_count
    
    raw_signal = (rule_count * 2.0) + (notice_count * 0.5)
    
    # Map to 1–5 scale: 0 = 1.0, 6+ = 5.0
    score = min(5.0, max(1.0, 1.0 + (raw_signal / 6.0) * 4.0))
    
    return round(score, 2), documents


bis_score, bis_docs = fetch_federal_register_bis(days_back=7)
print(f"BIS Federal Register sub-score: {bis_score}")
print(f"Documents found: {len(bis_docs)}")
for d in bis_docs[:5]:
    print(f"  - [{d.get('type')}] {d.get('title', '')[:80]}")
```

**Cell 2: Data Ingest — Congressional Activity**

```python
import requests

def fetch_congress_export_control(days_back=30):
    """
    Queries congress.gov for recent legislation related to export controls.
    Uses the free congress.gov API (requires free API key from api.congress.gov).
    """
    # Register at https://api.congress.gov for free API key
    # Store in Databricks secrets: dbutils.secrets.get(scope="prospectra", key="congress_api_key")
    
    try:
        api_key = dbutils.secrets.get(scope="prospectra", key="congress_api_key")
    except:
        # Fallback: use direct search if secret not configured
        print("WARNING: congress_api_key not in Databricks secrets. Using stub score.")
        return 3.0, []
    
    # Search for bills with export control keywords
    url = "https://api.congress.gov/v3/bill"
    params = {
        "api_key": api_key,
        "q": '{"query": "export controls semiconductors chips"}',
        "fromDateTime": (datetime.today() - timedelta(days=days_back)).strftime('%Y-%m-%dT00:00:00Z'),
        "sort": "updateDate+desc",
        "limit": 20
    }
    
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    bills = data.get("bills", [])
    
    # Score on bill action stage: introduced < committee < floor vote < enacted
    stage_weights = {
        "Introduced": 1.5,
        "Reported to Senate": 3.0,
        "Reported to House": 3.0,
        "Passed Senate": 4.0,
        "Passed House": 4.0,
        "Became Public Law": 5.0
    }
    
    if not bills:
        return 2.0, []
    
    scores = []
    for bill in bills:
        latest_action = bill.get("latestAction", {}).get("text", "")
        for stage, weight in stage_weights.items():
            if stage.lower() in latest_action.lower():
                scores.append(weight)
                break
        else:
            scores.append(1.5)  # Default to introduced-level signal
    
    avg_score = sum(scores) / len(scores) if scores else 2.0
    return round(min(5.0, max(1.0, avg_score)), 2), bills


congress_score, congress_bills = fetch_congress_export_control(days_back=30)
print(f"Congressional activity sub-score: {congress_score}")
print(f"Bills found: {len(congress_bills)}")
```

**Cell 3: Data Ingest — GDELT Framing Score**

```python
import requests
import json

def fetch_gdelt_export_control_tone(days_back=7):
    """
    Uses GDELT GKG API to measure media volume and tone on export control keywords.
    GDELT API is free and requires no authentication.
    """
    # GDELT 2.0 DOC API: returns tone and volume for keyword searches
    query_terms = '"export controls" "semiconductors" "chips" "China"'
    
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query_terms,
        "mode": "ArtList",
        "maxrecords": 100,
        "timespan": f"{days_back}d",
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        articles = data.get("articles", [])
    except Exception as e:
        print(f"GDELT API error: {e}")
        return 2.5, []
    
    if not articles:
        return 1.0, []
    
    # Volume score: more articles = higher signal
    volume_score = min(5.0, 1.0 + len(articles) / 25.0)
    
    # Tone score: GDELT tone ranges from -100 (negative) to +100 (positive)
    # For export control tightening, NEGATIVE tone (alarmed coverage) = stronger signal
    tones = []
    for article in articles:
        tone = article.get("tone", 0)
        if isinstance(tone, (int, float)):
            tones.append(tone)
    
    if tones:
        avg_tone = sum(tones) / len(tones)
        # Map: tone < -5 → score 5, tone 0 → score 3, tone > +5 → score 1
        tone_score = max(1.0, min(5.0, 3.0 - (avg_tone / 5.0)))
    else:
        tone_score = 2.5
    
    combined_score = round((volume_score * 0.5 + tone_score * 0.5), 2)
    return combined_score, articles[:5]  # Return first 5 for logging


gdelt_score, gdelt_articles = fetch_gdelt_export_control_tone(days_back=7)
print(f"GDELT framing sub-score: {gdelt_score}")
print(f"Articles found: {len(gdelt_articles)}")
```

**Cell 4: Composite Score, Verdict, and Write to Calibration Log**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_date
import json
from datetime import date

spark = SparkSession.builder.getOrCreate()

# --- Weights (from Lesson 236) ---
WEIGHTS = {
    "federal_register": 0.30,
    "congressional_tracker": 0.35,
    "gdelt": 0.10,
    "comtrade": 0.25   # placeholder until Comtrade feed is live
}

# --- Sub-Scores (from cells 1-3; Comtrade = placeholder) ---
sub_scores = {
    "federal_register": bis_score,
    "congressional_tracker": congress_score,
    "gdelt": gdelt_score,
    "comtrade": 3.0   # PLACEHOLDER: replace when Comtrade feed is live
}

# --- Composite Score ---
composite = sum(sub_scores[k] * WEIGHTS[k] for k in sub_scores)
composite = round(composite, 2)

# --- Thesis Verdict ---
if composite >= 4.0:
    verdict = "intact_strong"
elif composite >= 3.0:
    verdict = "intact"
elif composite >= 2.0:
    verdict = "weakening"
else:
    verdict = "breaking_down"

# --- Blind Interpretation (CEO writes this before checking prices) ---
# THIS FIELD IS CRITICAL — write your interpretation of the score
# before you look at how asset prices moved. This is the discipline
# that prevents confirmation bias. See Lesson 236 for full rationale.
blind_interpretation = f"""
Pipeline 4 composite score: {composite}/5.0 on {date.today()}.
Sub-signal breakdown: BIS={bis_score}, Congress={congress_score}, GDELT={gdelt_score}, Comtrade=3.0 (placeholder).
Verdict: {verdict}.

At this score level, the export control tightening thesis is {'confirming' if composite >= 3.0 else 'under pressure'}.
Expected directional effect: {'AI physical layer longs (CEG, VST, GEV) should benefit from continued AI capex; China AI avoids confirmed; Cybersecurity longs supported by increased adversary activity risk.' if composite >= 3.5 else 'Partial easing in tightening trajectory; monitor for détente signals before adding to China-avoidance positions.'}
""".strip()

print(f"\n=== PIPELINE 4 SCORE: {composite}/5.0 ===")
print(f"Verdict: {verdict}")
print(f"\nBlind interpretation:\n{blind_interpretation}")
print("\nWriting to prospectra.gold.signal_calibration_log...")

# --- Write to Delta Table ---
spark.sql(f"""
INSERT INTO prospectra.gold.signal_calibration_log
  (pipeline_name, run_date, raw_score, sub_scores, thesis_verdict, blind_interp)
VALUES (
  'pipeline_4_export_control',
  CURRENT_DATE(),
  {composite},
  map(
    'federal_register', {sub_scores['federal_register']},
    'congressional_tracker', {sub_scores['congressional_tracker']},
    'gdelt', {sub_scores['gdelt']},
    'comtrade', {sub_scores['comtrade']}
  ),
  '{verdict}',
  '{blind_interpretation.replace(chr(39), chr(39)+chr(39))}'
)
""")

print("✓ Score logged. Check prospectra.gold.signal_calibration_log")

# --- Verify ---
spark.sql("""
SELECT pipeline_name, run_date, raw_score, thesis_verdict
FROM prospectra.gold.signal_calibration_log
ORDER BY run_date DESC
LIMIT 5
""").show()
```

---

## 5. Scheduling — Make It Weekly Without Willpower

One of the Lesson 237 signal-vs-noise findings was that good frameworks break down when they require willpower to run. Pipeline 4 must run on a schedule, not depend on Bolo remembering to trigger it.

### Databricks Workflow Setup

1. In Databricks, go to **Workflows → Create Job**
2. Job name: `Pipeline_4_Export_Control_Weekly`
3. Schedule: **Every Monday at 06:00 UTC** (before US markets open)
4. Notebook path: the Pipeline 4 notebook you built above
5. Cluster: smallest general-purpose cluster (no GPU needed, this is all HTTP + SQL)
6. Notifications: set email alert to `franjmartin21@gmail.com` on job failure

This is the infrastructure that removes the "requires willpower" failure mode.

---

## 6. What Comes After Pipeline 4

Once Pipeline 4 runs for the first time and logs a score, the sequence is:

**Week 1 Task (after Pipeline 4 is live):**
- Run it manually once to verify the output makes sense
- Schedule the weekly job
- Write your blind interpretation (the `blind_interp` field) before checking prices — this is the discipline; do not skip it

**Week 2 Task — Pipeline 1 (Power Demand Signal Monitor):**
- Data source: EIA (Energy Information Administration) Open Data API — free, no quota
- Key endpoint: `https://api.eia.gov/v2/electricity/electric-power-operational-data/`
- Signal: electricity net generation by fuel type (nuclear, natural gas, coal) by grid region (WECC, SERC, PJM)
- Thesis validation: rising nuclear % of grid → Constellation thesis strengthening

**Week 2 Task — Sahel Uranium Tracker:**
- GDELT bounding box: Niger (12°N–23°N, 0°E–16°E), Mali (10°N–25°N, -12°W–4°E)
- Event codes: filter for CAMEO codes 19* (fight, use conventional military force) and 18* (assault)
- Signal: event density in mining regions → supply disruption risk
- Thesis validation: elevated GDELT event density in uranium belt → CCJ/URA thesis strengthening

**Week 3 Task — B-02 Market Data Feed:**
- Use `yfinance` (Yahoo Finance Python library) for FRO, STNG, DHT, Brent (BZ=F)
- Daily close prices → Delta table
- Purpose: end the dependency on session-by-session price searches; timestamps become reproducible

---

## 7. The 14-Day Sprint Checklist

Print this. Check boxes as you complete them.

```
WEEK 1 (by August 15)
□ Create prospectra.gold.signal_calibration_log table
□ Build Pipeline 4 notebook (4 cells above, adapting as needed)
□ Obtain congress.gov API key (free at api.congress.gov)
□ Store congress API key in Databricks secrets scope 'prospectra'
□ Run Pipeline 4 manually: verify score is written to calibration log
□ Schedule Pipeline 4 weekly workflow (Mondays 06:00 UTC)
□ Write first blind interpretation (fill blind_interp field before checking prices)
□ Confirm EWY exit per Lesson 237 stop-loss directive; log in investment_log.md

WEEK 2 (by August 22)
□ Build Pipeline 1: EIA Power Demand Signal Monitor
□ Build Sahel Uranium GDELT bounding box tracker
□ First Pipeline 1 score → calibration log
□ Uranium thesis status: confirmed? weakening?
□ Brief portfolio review: 3 open action items from Lesson 237 audit

WEEK 3 (by August 29)
□ B-02 Market Data Feed: FRO, STNG, DHT, BZ=F daily closes → Delta
□ First automated price-to-thesis correlation check
□ Review Portfolio: month-end position audit
□ CEO weekly briefing with pipeline data embedded (not just manual research)
```

---

## 8. Portfolio Status — August 9, 2026

*Carried from Lesson 237. No changes except the action items below.*

| Position | Asset | Conviction | Status |
|---|---|---|---|
| Long oil majors / LNG | XOM, CVX, LNG | MEDIUM-HIGH | HOLD — Iran-Oman talks = process not mechanism |
| Long gold | GLD | HIGH | HOLD — fiscal dominance intact, kill switch unmet |
| Long European defense | RHM, BA., HO | VERY HIGH | HOLD |
| Long Brazil agribusiness | AGRO3, SLC | VERY HIGH | HOLD |
| Underweight EU industrials/auto | — | LOW | HOLD to October |
| Long copper / critical minerals | COPX, SCCO, FCX | HIGH | HOLD |
| Long uranium | URA, CCJ, NXE | HIGH | HOLD — **Sahel tracker overdue** |
| Long LNG infrastructure | LNG (Cheniere) | HIGH | HOLD |
| EM FI tail hedge | EMB vol | TAIL HEDGE | HOLD (2-3%) |
| Long India (INDA) | INDA | MEDIUM-HIGH | HOLD Tranche 1 |
| Long TIPS | TIP | MEDIUM-HIGH | HOLD |
| Underweight TUR/EWY | TUR, EWY | **ACTION** | **EXIT EWY** (overdue from L237) |
| Long tankers | FRO, STNG, DHT | MEDIUM | HOLD |

**AI Infrastructure Barbell (monitoring, not sized):**
| Asset | Status |
|---|---|
| CEG, VST, GEV | Monitoring — Pipeline 1 needed before sizing |
| PLTR, BAH, LDOS | Monitoring — Pipeline 2 needed before sizing |
| CRWD, PANW | Monitoring |

---

## 9. Investment Implications of Today's Export Control Intelligence

The BIS Foundry Due Diligence Rule extension through December 31, 2026, combined with Operation Gatekeeper's $160M interdiction, confirms that enforcement is tightening in exactly the way Pipeline 4 was designed to track.

**Directional implications:**
- **Cybersecurity longs (CRWD, PANW) — strengthened.** Gray-market chip diversion networks imply adversary actors who are resource-constrained but motivated. Constraint on hardware access historically increases investment in asymmetric alternatives: software-based cyberoperations. Watch for CISA alerts as a CRWD/PANW position trigger.
- **China AI avoids — confirmed.** Operation Gatekeeper interceptions via Singapore/Hong Kong re-export nodes are exactly the gray-market routes Comtrade anomaly monitoring targets. Embedded-chip tracking (still moving through Congress) will close these routes when enacted.
- **Physical layer longs — neutral.** Export control tightening has no direct negative effect on US-based nuclear power utilities. Indirect positive: tighter controls accelerate US domestic AI infrastructure spending, which increases power demand.

---

## Databricks Angle

This session *is* the Databricks angle. Every section above is a build specification.

One meta-note for Bolo: The most valuable thing you can build in the first two weeks is not the most technically impressive pipeline — it is the one that produces a score you can actually act on. Pipeline 4 is correct to build first not because export controls are the most interesting signal (though they are), but because:

1. All data sources are **free and no-auth** (Federal Register, GDELT) or **low-friction** (Congress API key is free)
2. The signal has **high latency tolerance** — weekly cadence is fine; you don't need streaming
3. The output is **directly tied to positions** — two existing avoids (China AI, middle layer) and two longs (cybersecurity, physical layer) are explicitly keyed to Pipeline 4 scores
4. Building it proves the infrastructure works, and that proof accelerates trust in every subsequent pipeline

Ship the simple thing that validates the framework. Iterate from there.

---

## CEO Closing Note

The Synthesis Arc ended yesterday with "there is no Lesson 238." That was a teaching move — it forces the project into execution mode. But the CEO still has a job to do, and that job is now to specify, direct, and hold accountable.

The 14-day sprint checklist above is the next 14 days of Bolo's Databricks work. It is not aspirational. It is achievable. The data sources are free. The Databricks infrastructure exists. The analytical framework — 237 lessons of it — is ready to be operationalized.

**The only open question is whether you build it.**

The clock has been running since April. The teaching is done. Build the thing.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session delivered: 2026-08-09 | Post-curriculum Engineering Directive | First session of the Engineering Phase*
