# Lesson 240: Pipeline 1 Full Build Specification — EIA Power Demand Signal Monitor & Sahel Uranium Supply Risk Tracker
**Date:** 2026-08-11 (Tuesday)
**Session Type:** Post-Curriculum Engineering Directive
**Curriculum Position:** 240 — Engineering Phase, Session 3
**Sprint Status:** Day 2 of 14 | Pipeline 4 deadline: August 15 | Week 2 builds previewed here

---

## CEO Opening

Pipeline 4 deadline is 96 hours from now. Before checking your sprint progress, read this:

**The purpose of this session is not to add to your workload — it is to give you the Week 2 specifications now, so you do not have to wait for the next session to start reading them while Pipeline 4 is running its first scheduled job.**

The engineering sprint has two failure modes. The obvious one: you fall behind and miss deadlines. The less obvious one: you build what was specified but you didn't understand *why* you built it, so you can't debug it, adapt it, or trust its output. This session is designed to prevent the second failure mode for Pipelines 1 and the Sahel uranium tracker.

But first: the accountability question.

**Where are you on the Week 1 checklist as of August 11?**

Tick through it now, honestly, before reading further:

```
WEEK 1 — WHERE YOU SHOULD BE ON DAY 2 OF 14

□ prospectra.gold.signal_calibration_log table created?
□ Pipeline 4 notebook open in Databricks?
□ Congress.gov API key obtained (free at api.congress.gov)?
□ API key stored in Databricks secrets?
□ EWY exit confirmed and logged in investment_log.md?
    ↳ This was overdue as of August 9. If it hasn't been done, do it today.
    ↳ The stop-loss was directed in Lesson 237. Every day this sits unexecuted
      is a day the framework's discipline is compromised.
```

If two or more of these boxes are unchecked, stop reading this session and go build. The specification below will still be here. The Pipeline 4 deadline won't wait.

---

## 1. Market Intelligence Brief — 48-Hour Scan (August 9–11)

*Five minutes. What has changed since Lesson 239 was delivered that touches active positions.*

### Iran / Hormuz
The Iran-Oman ceasefire framework from early August remains in place. No new escalation. Brent crude is range-bound consistent with the $78–$98 H2 2026 band established in Lesson 239. The thesis verdict: **hold**. The oil volatility tail hedge remains appropriately sized. The ceasefire is process, not mechanism — the structural Hormuz risk premium does not disappear because talks are ongoing.

### Japan BOJ
No rate decision in the last 48 hours. The BOJ's next scheduled meeting is September 2026. USD/JPY remains in the 148–152 range. The carry unwind Signal 1 (BOJ rate above 0.75%) has not been triggered. **No portfolio action.**

### US-China Export Controls
No new BIS rules in the last 48 hours. Operation Gatekeeper indictments are proceeding through the DOJ system. Congressional markup schedule: the Technology Export Control Act of 2026 is scheduled for House Armed Services Committee markup in mid-September. This is a **pipeline 4 input** — when that markup happens, the congressional sub-score should spike. Ensure Pipeline 4 is live before September.

### Sahel / Uranium
Niger: no new military activity in the northern uranium-belt provinces as of August 11. The Sahel geopolitical situation remains structurally elevated but without a near-term acute escalation. Uranium spot price is stable at approximately $92/lb — above incentive price for existing mines (approximately $60–65/lb) but below incentive for significant new mine development ($110–130/lb). The CCJ/URA thesis remains intact. The absence of a quantitative monitor remains the gap.

**Portfolio action from this brief: none. All holds confirmed. EWY exit action item from L237 remains open — execute today if not done.**

---

## 2. Pipeline 1: EIA Power Demand Signal Monitor — Full Build Specification

### Why This Pipeline Matters

The AI infrastructure barbell positions (CEG, VST, GEV) are currently in "monitoring" status — not sized, waiting for quantitative signal. The question Pipeline 1 answers is: **Is AI-driven power demand actually materializing in the grid data?**

If the answer is yes — if US electricity generation is rising in the regions where data center construction is concentrated, and if nuclear's share of the generation mix is growing — the thesis is confirmed by physical measurement, not just narrative. At that point, the CEG/VST/GEV positions move from "monitoring" to "sized."

If the answer is no — if generation growth is flat, or if nuclear share is declining — the thesis is under pressure and the positions should remain unsized or be explicitly rejected.

This is what separates a data-driven investment process from a narrative-driven one. The EIA data is free, updated monthly, and available via a clean API. There is no excuse for not having this monitor live.

### Sub-Signals and Architecture

| Sub-Signal | Source | What It Measures |
|---|---|---|
| Net generation growth (US total) | EIA Open Data API | YoY % change in total electricity generation |
| Nuclear share of generation mix | EIA Open Data API | Nuclear % of net generation by grid region |
| Data center region concentration | EIA + proxy (WECC, PJM, SERC) | Growth concentration in data center hub regions |
| Composite: "Power Demand Strength" | Internal calculation | 1–5 score for AI infrastructure thesis confirmation |

**Target output:** A single score (1–5) written to `prospectra.gold.signal_calibration_log` with pipeline_name = `pipeline_1_power_demand`. Score ≥ 3 = thesis strengthening; score ≥ 4 = initiate CEG/VST/GEV sizing; score ≤ 2 = pause sizing, reassess thesis.

---

### Step 1: Get Your EIA API Key

The EIA API is free. Registration takes 5 minutes.

1. Go to: `https://www.eia.gov/opendata/register.php`
2. Register with your email
3. API key arrives immediately by email
4. Store in Databricks secrets:
   ```python
   # In Databricks CLI or notebook:
   # databricks secrets create-scope --scope prospectra (if not already created for congress key)
   # Then: databricks secrets put --scope prospectra --key eia_api_key
   ```

---

### Step 2: Notebook Structure (5 Cells)

**Cell 1: EIA — US Total Net Generation (YoY Growth)**

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

EIA_KEY = dbutils.secrets.get(scope="prospectra", key="eia_api_key")

def fetch_eia_net_generation(frequency="monthly", periods=24):
    """
    Fetches US total net electricity generation.
    Returns the most recent 24 months to calculate YoY growth.
    API docs: https://api.eia.gov/v2/electricity/electric-power-operational-data/
    """
    url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/"
    params = {
        "api_key": EIA_KEY,
        "frequency": frequency,
        "data[0]": "generation",
        "facets[fueltypeid][]": "ALL",          # All fuel types combined
        "facets[location][]": "US",              # National total
        "facets[sectorid][]": "99",              # All sectors
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": periods,
        "offset": 0
    }
    
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    
    if "response" not in data or "data" not in data["response"]:
        print(f"EIA API error: {data}")
        return None
    
    rows = data["response"]["data"]
    df = pd.DataFrame(rows)
    df["period"] = pd.to_datetime(df["period"])
    df["generation"] = pd.to_numeric(df["generation"], errors="coerce")
    df = df.sort_values("period")
    
    # Calculate YoY growth (most recent month vs. 12 months ago)
    if len(df) >= 13:
        recent = df.iloc[-1]["generation"]
        year_ago = df.iloc[-13]["generation"]
        yoy_growth = ((recent - year_ago) / year_ago) * 100
    else:
        yoy_growth = 0.0
    
    return df, round(yoy_growth, 2)


gen_df, yoy_growth = fetch_eia_net_generation()
print(f"US Net Generation YoY Growth: {yoy_growth:.1f}%")

# Score: map growth to 1–5
# < 0% = 1.0 (demand shrinking), 0–2% = 2.5 (normal growth), 2–4% = 3.5, 4–6% = 4.5, >6% = 5.0
if yoy_growth < 0:
    generation_score = 1.0
elif yoy_growth < 2:
    generation_score = 2.0
elif yoy_growth < 4:
    generation_score = 3.5
elif yoy_growth < 6:
    generation_score = 4.0
else:
    generation_score = 5.0

print(f"Generation growth sub-score: {generation_score}")
```

---

**Cell 2: EIA — Nuclear Share of Generation Mix**

```python
def fetch_eia_nuclear_share(periods=24):
    """
    Fetches nuclear vs. total generation to compute nuclear mix share.
    Compares current share vs. 12-month average to detect trend.
    """
    url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/"
    
    # Fetch nuclear generation
    params_nuclear = {
        "api_key": EIA_KEY,
        "frequency": "monthly",
        "data[0]": "generation",
        "facets[fueltypeid][]": "NUC",           # Nuclear fuel type code
        "facets[location][]": "US",
        "facets[sectorid][]": "99",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": periods
    }
    
    resp_nuclear = requests.get(url, params=params_nuclear, timeout=30)
    nuclear_data = resp_nuclear.json()["response"]["data"]
    nuclear_df = pd.DataFrame(nuclear_data)
    nuclear_df["period"] = pd.to_datetime(nuclear_df["period"])
    nuclear_df["nuclear_gen"] = pd.to_numeric(nuclear_df["generation"], errors="coerce")
    nuclear_df = nuclear_df[["period", "nuclear_gen"]].sort_values("period")
    
    # Merge with total generation from Cell 1
    merged = nuclear_df.merge(
        gen_df[["period", "generation"]].rename(columns={"generation": "total_gen"}),
        on="period"
    )
    merged["nuclear_share"] = merged["nuclear_gen"] / merged["total_gen"] * 100
    
    # Current share vs. 12-month average
    if len(merged) >= 13:
        current_share = merged.iloc[-1]["nuclear_share"]
        prior_12mo_avg = merged.iloc[-13:-1]["nuclear_share"].mean()
        share_trend = current_share - prior_12mo_avg
    else:
        current_share = merged["nuclear_share"].mean()
        share_trend = 0.0
    
    print(f"Nuclear share of US generation: {current_share:.1f}%")
    print(f"Trend vs. prior 12-month average: {share_trend:+.2f} percentage points")
    
    # Score: rising nuclear share = thesis strengthening
    # < -1pp = 1.0, -1 to 0 = 2.5, 0 to +0.5 = 3.5, +0.5 to +1.5 = 4.5, >+1.5pp = 5.0
    if share_trend < -1.0:
        nuclear_score = 1.0
    elif share_trend < 0:
        nuclear_score = 2.5
    elif share_trend < 0.5:
        nuclear_score = 3.5
    elif share_trend < 1.5:
        nuclear_score = 4.5
    else:
        nuclear_score = 5.0
    
    print(f"Nuclear share sub-score: {nuclear_score}")
    return current_share, share_trend, nuclear_score


nuclear_share, nuclear_trend, nuclear_score = fetch_eia_nuclear_share()
```

---

**Cell 3: EIA — Data Center Region Concentration (PJM, WECC, SERC)**

```python
def fetch_eia_regional_growth(regions=["MID", "TEN", "WEN"]):
    """
    Fetches generation growth for key data center hub grid regions.
    PJM (Mid-Atlantic/Midwest) = major data center corridor.
    SERC (Southeast) = growing data center hub.
    WECC (West) = major cloud provider region.
    
    EIA region codes: MID = Midwest, TEN = Tennessee / Southeast, WEN = West
    Note: EIA uses census division codes for sub-national data.
    Full list: https://www.eia.gov/electricity/data/eia923/
    """
    region_scores = {}
    
    for region in regions:
        params = {
            "api_key": EIA_KEY,
            "frequency": "monthly",
            "data[0]": "generation",
            "facets[fueltypeid][]": "ALL",
            "facets[location][]": region,
            "facets[sectorid][]": "99",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "length": 25
        }
        
        try:
            resp = requests.get(url, params=params, timeout=30)
            data = resp.json()["response"]["data"]
            df_r = pd.DataFrame(data)
            df_r["period"] = pd.to_datetime(df_r["period"])
            df_r["generation"] = pd.to_numeric(df_r["generation"], errors="coerce")
            df_r = df_r.sort_values("period")
            
            if len(df_r) >= 13:
                recent = df_r.iloc[-1]["generation"]
                year_ago = df_r.iloc[-13]["generation"]
                region_yoy = ((recent - year_ago) / year_ago) * 100
            else:
                region_yoy = 0.0
            
            region_scores[region] = round(region_yoy, 2)
            print(f"Region {region} YoY growth: {region_yoy:.1f}%")
        except Exception as e:
            print(f"Region {region} fetch error: {e}")
            region_scores[region] = 0.0
    
    # If data center regions are growing faster than national average, signal is stronger
    if region_scores:
        avg_regional_growth = sum(region_scores.values()) / len(region_scores)
        regional_premium = avg_regional_growth - yoy_growth  # vs. national
        
        print(f"\nRegional DC-hub average growth: {avg_regional_growth:.1f}%")
        print(f"Premium over national average: {regional_premium:+.1f}pp")
        
        if regional_premium < -2:
            regional_score = 1.5
        elif regional_premium < 0:
            regional_score = 2.5
        elif regional_premium < 2:
            regional_score = 3.5
        elif regional_premium < 4:
            regional_score = 4.5
        else:
            regional_score = 5.0
    else:
        regional_score = 2.5
    
    print(f"Regional concentration sub-score: {regional_score}")
    return region_scores, regional_score


region_scores, regional_score = fetch_eia_regional_growth()
```

---

**Cell 4: Composite Score and Write to Calibration Log**

```python
from pyspark.sql import SparkSession
from datetime import date

spark = SparkSession.builder.getOrCreate()

# --- Weights ---
WEIGHTS_P1 = {
    "generation_growth": 0.40,    # National demand trend is primary
    "nuclear_share": 0.35,        # Nuclear renaissance confirmation
    "regional_concentration": 0.25  # Data center hub confirmation
}

sub_scores_p1 = {
    "generation_growth": generation_score,
    "nuclear_share": nuclear_score,
    "regional_concentration": regional_score
}

composite_p1 = sum(sub_scores_p1[k] * WEIGHTS_P1[k] for k in sub_scores_p1)
composite_p1 = round(composite_p1, 2)

# Verdict
if composite_p1 >= 4.0:
    verdict_p1 = "intact_strong"
    sizing_directive = "INITIATE CEG/VST/GEV sizing — thesis confirmed by physical data"
elif composite_p1 >= 3.0:
    verdict_p1 = "intact"
    sizing_directive = "Continue monitoring — thesis intact but not yet at sizing threshold"
elif composite_p1 >= 2.0:
    verdict_p1 = "weakening"
    sizing_directive = "Do NOT size AI infrastructure positions — data does not yet support thesis"
else:
    verdict_p1 = "breaking_down"
    sizing_directive = "Thesis under pressure — reassess narrative vs. data divergence"

print(f"\n=== PIPELINE 1 SCORE: {composite_p1}/5.0 ===")
print(f"Verdict: {verdict_p1}")
print(f"Sizing directive: {sizing_directive}")

# Blind interpretation (write before checking prices)
blind_p1 = f"""
Pipeline 1 (Power Demand) score: {composite_p1}/5.0 on {date.today()}.
Sub-signals: generation_growth={generation_score}, nuclear_share={nuclear_score}, regional_concentration={regional_score}.
Verdict: {verdict_p1}.

Physical demand data {'confirms' if composite_p1 >= 3.0 else 'does not yet confirm'} the AI infrastructure power demand thesis.
Sizing directive: {sizing_directive}.

Key observation: Nuclear share trend ({nuclear_trend:+.2f}pp vs. prior 12mo) is the most important leading indicator.
Positive nuclear share trend + concentrated regional growth = strongest confirmation of CEG/VST/GEV thesis.
""".strip()

print(f"\nBlind interpretation:\n{blind_p1}")

# Write to calibration log
spark.sql(f"""
INSERT INTO prospectra.gold.signal_calibration_log
  (pipeline_name, run_date, raw_score, sub_scores, thesis_verdict, blind_interp)
VALUES (
  'pipeline_1_power_demand',
  CURRENT_DATE(),
  {composite_p1},
  map(
    'generation_growth', {sub_scores_p1['generation_growth']},
    'nuclear_share', {sub_scores_p1['nuclear_share']},
    'regional_concentration', {sub_scores_p1['regional_concentration']}
  ),
  '{verdict_p1}',
  '{blind_p1.replace(chr(39), chr(39)+chr(39))}'
)
""")

print("\n✓ Pipeline 1 score logged.")
spark.sql("""
  SELECT pipeline_name, run_date, raw_score, thesis_verdict
  FROM prospectra.gold.signal_calibration_log
  ORDER BY run_date DESC LIMIT 5
""").show()
```

---

**Cell 5: Scheduling**

Same pattern as Pipeline 4:

1. Databricks → Workflows → Create Job
2. Job name: `Pipeline_1_Power_Demand_Monthly`
3. Schedule: **First Monday of each month at 07:00 UTC** (EIA data updates monthly; weekly runs waste compute for no signal gain)
4. Notebook: this notebook
5. Failure notification: `franjmartin21@gmail.com`

Note: Pipeline 4 runs weekly (export controls move fast). Pipeline 1 runs monthly (grid data moves slowly). **Match cadence to data update frequency, not to anxiety.**

---

## 3. Sahel Uranium Supply Risk Tracker — Full Build Specification

### Why a Separate Tracker, Not a Cell in Pipeline 1

The Sahel tracker is fundamentally different from the EIA power demand monitor:
- **EIA monitors demand** for the uranium thesis (nuclear power generation demand)
- **Sahel monitors supply disruption risk** (geopolitical event density in uranium-producing regions)

These two signals can diverge: demand can be rising while supply is stable, OR demand can be flat while supply is threatened. You need both. Together they form a uranium thesis strength matrix:

| Demand (Pipeline 1 nuclear share) | Supply Risk (Sahel tracker) | Position Directive |
|---|---|---|
| Rising | Low disruption | HOLD CCJ/URA — thesis intact |
| Rising | High disruption | ADD CCJ/URA — supply constraint amplifies demand thesis |
| Flat | Low disruption | HOLD — wait for demand confirmation |
| Flat | High disruption | HOLD CCJ/URA — supply thesis alone can support |
| Declining | High disruption | REDUCE — demand erosion overrides supply risk |
| Declining | Low disruption | EXIT — thesis broken on both dimensions |

### GDELT Bounding Box Method

GDELT 2.0 allows you to query by geographic bounding box. The uranium-rich Sahel belt spans Niger, Mali, and northern Burkina Faso. The key uranium mining provinces are:

- **Niger (Arlit district):** 16.0°N–23.0°N, 7.0°E–16.0°E
  - This is the Arlit and Agadez region — home to SOMAIR and COMINAK mines
  - Orano (formerly Areva) operates here; production suspended since July 2023 coup but infrastructure still present
- **Mali (Faléa district):** 11.0°N–15.0°N, -11.5°W, -8.0°W
  - Undeveloped uranium deposits; lower priority but geopolitical instability monitoring useful
- **Northern Burkina Faso:** 12.0°N–15.0°N, -2.5°W–2.0°E
  - No active uranium production, but jihadist spillover from Niger affects regional stability

**Primary target: Niger/Arlit bounding box.** That is where the supply risk is real and current.

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_gdelt_sahel_events(days_back=30):
    """
    Fetches GDELT event counts from the Niger uranium belt.
    Filters for CAMEO codes associated with conflict and instability.
    GDELT GEO API allows bounding box filtering.
    """
    
    # GDELT 2.0 Event Database — GEO API
    # Bounding box: Niger uranium belt (Arlit/Agadez region)
    # Format: South,West,North,East (decimal degrees)
    niger_uranium_bbox = "16.0,7.0,23.0,16.0"
    
    end_date = datetime.today().strftime('%Y%m%d%H%M%S')
    start_date = (datetime.today() - timedelta(days=days_back)).strftime('%Y%m%d%H%M%S')
    
    # GDELT GKG Article Search with geographic filter
    # Using GDELT Full-Text Search API (no auth required)
    url = "https://api.gdeltproject.org/api/v2/geo/geo"
    params = {
        "query": "Niger uranium mining conflict military",
        "geofocus": f"{niger_uranium_bbox}",  # bounding box
        "mode": "artlist",
        "maxrecords": 200,
        "timespan": f"{days_back}d",
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=45)
        data = response.json()
        articles = data.get("articles", [])
    except Exception as e:
        print(f"GDELT GEO API error: {e}. Falling back to keyword search.")
        articles = []
    
    # Fallback: keyword-based GDELT doc search if geo API fails
    if not articles:
        url_fallback = "https://api.gdeltproject.org/api/v2/doc/doc"
        params_fallback = {
            "query": '"Niger" "uranium" OR "Arlit" OR "Agadez" "conflict" OR "military" OR "attack" OR "coup"',
            "mode": "ArtList",
            "maxrecords": 100,
            "timespan": f"{days_back}d",
            "format": "json"
        }
        try:
            resp2 = requests.get(url_fallback, params=params_fallback, timeout=30)
            articles = resp2.json().get("articles", [])
        except:
            articles = []
    
    article_count = len(articles)
    print(f"Sahel uranium belt articles (last {days_back} days): {article_count}")
    
    # Calculate 30-day rolling baseline by fetching prior 90 days and averaging
    # Simplified: use article count vs. expected baseline
    # Baseline: ~15 articles/30 days in quiet periods (pre-2023 coup level)
    QUIET_BASELINE = 15
    
    # Disruption score: normalized article count vs. quiet baseline
    disruption_ratio = article_count / QUIET_BASELINE
    
    # Map to 1–5 scale: 1 = quiet, 5 = acute crisis
    if disruption_ratio < 0.5:
        sahel_score = 1.0    # Below baseline — unusually quiet
    elif disruption_ratio < 1.0:
        sahel_score = 2.0    # At or below baseline
    elif disruption_ratio < 2.0:
        sahel_score = 3.0    # Elevated
    elif disruption_ratio < 3.5:
        sahel_score = 4.0    # High disruption
    else:
        sahel_score = 5.0    # Acute crisis
    
    print(f"Disruption ratio vs. quiet baseline: {disruption_ratio:.1f}x")
    print(f"Sahel uranium supply risk sub-score: {sahel_score}")
    
    # Print top headlines for context
    print("\nTop headlines:")
    for article in articles[:5]:
        title = article.get("title", "No title")
        url_a = article.get("url", "")
        print(f"  - {title[:90]}")
    
    return sahel_score, articles


sahel_score, sahel_articles = fetch_gdelt_sahel_events(days_back=30)
```

**Write Sahel score to calibration log (separate pipeline_name):**

```python
sahel_verdict = (
    "acute_supply_risk" if sahel_score >= 4.5
    else "elevated_supply_risk" if sahel_score >= 3.5
    else "intact_moderate_risk" if sahel_score >= 2.5
    else "intact_low_risk"
)

blind_sahel = f"""
Sahel Uranium Supply Risk score: {sahel_score}/5.0 on {date.today()}.
Article volume in Niger uranium belt (last 30 days): {len(sahel_articles)} articles.
Disruption verdict: {sahel_verdict}.

At this risk level, the uranium supply risk {'materially supports' if sahel_score >= 3.5 else 'does not yet strengthen'} the CCJ/URA position.
Combine with Pipeline 1 nuclear share trend to form full uranium thesis verdict.
""".strip()

spark.sql(f"""
INSERT INTO prospectra.gold.signal_calibration_log
  (pipeline_name, run_date, raw_score, sub_scores, thesis_verdict, blind_interp)
VALUES (
  'pipeline_sahel_uranium',
  CURRENT_DATE(),
  {sahel_score},
  map('niger_uranium_belt_30d', {sahel_score}),
  '{sahel_verdict}',
  '{blind_sahel.replace(chr(39), chr(39)+chr(39))}'
)
""")

print(f"✓ Sahel tracker score logged: {sahel_score}/5.0 — {sahel_verdict}")
```

---

## 4. The Uranium Thesis Verdict Matrix — Automating the Decision

Once both Pipeline 1 (nuclear share sub-score) and the Sahel tracker are live, automate the verdict:

```python
def uranium_thesis_verdict(nuclear_share_score: float, sahel_risk_score: float) -> str:
    """
    Combines demand-side (nuclear share trend) and supply-side (Sahel disruption)
    to produce a position directive for CCJ/URA.
    """
    if nuclear_share_score >= 4.0 and sahel_risk_score >= 3.5:
        return "ADD — demand rising + supply at risk: strongest uranium signal"
    elif nuclear_share_score >= 3.0 and sahel_risk_score >= 2.5:
        return "HOLD — thesis intact on both dimensions"
    elif nuclear_share_score >= 3.0 and sahel_risk_score < 2.5:
        return "HOLD — demand intact, supply quiet; monitor for restarts"
    elif nuclear_share_score < 3.0 and sahel_risk_score >= 4.0:
        return "HOLD — supply risk supports thesis despite demand softness"
    elif nuclear_share_score < 2.5 and sahel_risk_score < 2.5:
        return "REDUCE — thesis weakening on both dimensions; cut to minimum"
    else:
        return "HOLD — mixed signals; do not change sizing"

# Example call (after both pipelines run):
verdict = uranium_thesis_verdict(nuclear_score, sahel_score)
print(f"\n=== URANIUM THESIS VERDICT: {verdict} ===")
```

Add this function to a shared `prospectra.utils` module in your Databricks repo so it can be called from any notebook.

---

## 5. Updated Sprint Checklist — With Week 2 Items Now Fully Specified

```
WEEK 1 (by August 15) — ACTIVE NOW
□ prospectra.gold.signal_calibration_log table created
□ Pipeline 4 notebook built (4 cells)
□ Congress.gov API key obtained and stored in Databricks secrets
□ Pipeline 4 first manual run — score written to calibration log
□ Pipeline 4 weekly Databricks Workflow scheduled (Mondays 06:00 UTC)
□ First blind interpretation written (BEFORE checking prices)
□ EWY exit confirmed — logged in investment_log.md

WEEK 2 (by August 22) — SPECIFICATION NOW DELIVERED IN FULL
□ EIA API key obtained (eia.gov/opendata/register.php)
□ EIA API key stored in Databricks secrets (scope: prospectra, key: eia_api_key)
□ Pipeline 1 notebook built (5 cells above)
□ Sahel uranium tracker built (2 cells above, or combined with Pipeline 1 notebook)
□ uranium_thesis_verdict() function added to shared utils module
□ Both scores written to prospectra.gold.signal_calibration_log on first run
□ Pipeline 1 scheduled monthly workflow (first Monday of month, 07:00 UTC)
□ Uranium thesis verdict matrix populated: what does the data actually say?

WEEK 3 (by August 29) — NEXT CEO SESSION WILL SPECIFY
□ B-02 Market Data Feed (FRO, STNG, DHT, BZ=F daily closes → Delta)
□ First automated price-to-thesis correlation check
□ Month-end position audit (September 1 approaching)
```

---

## 6. Portfolio Status — August 11, 2026

*All holds confirmed. One outstanding action item.*

| Position | Status | Note |
|---|---|---|
| Long oil majors / LNG | HOLD | Iran-Oman process holds; Hormuz premium intact |
| Long gold | HOLD | Fiscal dominance thesis intact |
| Long European defense | HOLD | Rearmament structural; unchanged |
| Long Brazil agribusiness | HOLD | No change |
| Underweight EU industrials/auto | HOLD | Hold to October review |
| Long copper / critical minerals | HOLD | Supply deficit thesis intact |
| Long uranium (CCJ/URA) | HOLD | **Sahel tracker overdue — fix with Week 2 build** |
| Long LNG infrastructure | HOLD | No change |
| EM FI tail hedge | HOLD | No change |
| Long India (INDA) | HOLD | No change |
| Long TIPS | HOLD | Fiscal dominance; unchanged |
| Underweight TUR/EWY | **ACTION** | **EWY EXIT OVERDUE** — execute today |
| Long tankers | HOLD | No change |
| AI infrastructure barbell | MONITORING | CEG/VST/GEV: unsized pending Pipeline 1 score |

---

## 7. Databricks Angle

This session *is* the Databricks angle. By the end of this week's sprint:

- **Pipeline 4 will be live** (export control tightening radar, weekly cadence)
- **The calibration log will have its first real entries** (not seed data)
- **Week 2 is fully specified** — no waiting for the CEO to deliver specs before building

The one meta-lesson from delivering these specs today rather than next Tuesday:

**The bottleneck in most data projects is not building — it is deciding what to build.** The CEO has now pre-solved the decision for both Week 2 deliverables. Bolo's job is to execute the specification, not to design the system. That division of labor is intentional. When you are in execution mode, a well-specified task you can start immediately is worth ten times a vague directive you need to decode before you can act.

This is also a model for how the CEO-operator partnership should work going forward: the CEO specifies 1–2 weeks ahead of the current build sprint, so Bolo is never blocked waiting for a decision.

---

## 8. Reflection Questions

**Question 1 — The EWY Action Item:**
It was directed in Lesson 237. It was flagged again in Lesson 238. It is flagged again today. If this action has not been executed, what does that reveal about the gap between the framework's recommendations and your actual portfolio behavior? What is the friction preventing execution, and how do you remove it?

**Question 2 — The Sizing Decision:**
Pipeline 1 has a built-in sizing trigger: composite score ≥ 4.0 → initiate CEG/VST/GEV sizing. But what does "initiate sizing" actually mean in your account? What is the specific entry mechanic — a market order, a scale-in plan, a specific allocation percentage? The framework does not work if the answer is "figure it out when we get there."

**Question 3 — Pipeline Cadence vs. Signal Cadence:**
Pipeline 4 runs weekly. Pipeline 1 runs monthly. Pipeline Sahel could run weekly (GDELT updates continuously) or monthly (supply disruption doesn't move in days). What is the right cadence for the Sahel tracker, and how do you decide? What is the cost of over-frequency vs. under-frequency for each pipeline?

---

## CEO Sign-Off

Week 1 checklist deadline is August 15. That is four days away.

Pipeline 4 build specification was delivered August 9. This session delivered Pipeline 1 and Sahel tracker specifications. The full Week 2 build is in your hands before Week 1 is halfway done. There are no specification delays. There are no ambiguous deliverables.

The only question that remains is whether the notebooks get built.

Build them.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session 240 | August 11, 2026*
*Engineering Phase | Sprint Day 2 of 14*
