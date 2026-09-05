# Lesson 300 — Phase 2 Begins: The Commodity Pressure Model

**Date:** 2026-09-05
**Session Type:** Daily Lesson
**Lesson Number:** 300 / ongoing
**Topic:** Databricks Intelligence Module — Commodity Pressure Model (CPM)
**Curriculum Arc:** Databricks Build Module — Phase 2, Lesson 1 (data → signal → intelligence → positions)

---

## Opening Question

*Phase 1 is complete. You have a Geopolitical Risk Index that scores 20+ countries daily, classifies them into risk regimes, fires alerts, and delivers a morning note to your inbox.*

Here is the question that opens Phase 2:

**"A country's GRI score just spiked 2 standard deviations above its 90-day mean. Which commodity moves first — and in which direction?"**

If you cannot answer that question systematically, you have a risk detection system but not an investment system. Phase 2 converts risk scores into directional asset views. The Commodity Pressure Model (CPM) is the first and most tractable component because the linkage from geopolitical event to commodity price is more mechanical than any other asset class. Supply disruption risk is not a soft thesis — it has a physical logic.

Lesson 300 specifies the architecture, logic, and Databricks implementation plan for the CPM.

---

## I. Why Commodities First

Three reasons to begin Phase 2 with commodities rather than equities or FX:

**1. The causal chain is observable.** A conflict near the Strait of Hormuz → tanker traffic disruption risk → oil supply uncertainty → WTI/Brent spread widening → oil price upward pressure. Every link in that chain is measurable. Equity repricing runs through ten layers of analyst estimate revisions; commodity pressure runs through two.

**2. The signal lead time is actionable.** Commodity futures markets price in geopolitical disruption risk 2–6 weeks before the disruption is confirmed or denied. The CPM's job is to flag when GRI movement in specific geographies historically preceded commodity moves — giving a systematic framework for position timing.

**3. You already have the supply geography data.** GDELT events are geolocated. The critical commodity chokepoints — Hormuz (oil/LNG), Malacca (oil/LNG), Suez (oil/grain), Ukraine (wheat/corn/sunflower), DRC/Zambia (copper/cobalt), Chile/Peru (copper/lithium) — are fixed coordinates. Mapping GRI scores to these locations is a deterministic join.

---

## II. The Commodity Pressure Model — Conceptual Architecture

The CPM answers one question per commodity per day:

> **"Is geopolitical pressure on [commodity X]'s supply geography currently above or below historical norms, and in which direction is it trending?"**

The output is a **Commodity Pressure Score (CPS)** — a normalized index from -2 to +2:

| Score | Interpretation |
|---|---|
| > +1.5 | **Strong upward pressure** — multiple supply geographies under elevated stress |
| +0.5 to +1.5 | **Moderate upward pressure** — localized disruption risk |
| -0.5 to +0.5 | **Neutral** — no significant geopolitical signal |
| -0.5 to -1.5 | **Moderate downward pressure** — supply route de-escalation |
| < -1.5 | **Strong downward pressure** — bilateral agreements or ceasefire dynamics reducing risk |

The CPS feeds directly into the Investment Signal Generator (Phase 2, Lesson 3) to produce directional views.

---

## III. The Five Commodity Modules

The CPM covers five commodity groups, each with its own supply geography mapping:

### Module 1 — Crude Oil & LNG

**Key geographies:** Middle East (GCC + Iran), Russia, West Africa (Nigeria), Libya
**Key chokepoints:** Strait of Hormuz, Bab-el-Mandeb, Suez Canal, Turkish Straits
**GRI → CPS logic:**
- Iran GRI > 75th percentile: Hormuz disruption multiplier = 1.3x
- Russia GRI trending up AND Ukraine GRI trending up: pipeline disruption signal
- Libya GRI spike: OPEC swing producer disruption

**Target assets:** WTI futures, Brent futures, TTF natural gas, LNG spot (JKM)

### Module 2 — Copper & Critical Minerals

**Key geographies:** Chile, Peru, DRC, Zambia, Indonesia (nickel)
**No chokepoints** — land route disruption and mine-level political risk dominate
**GRI → CPS logic:**
- Chile/Peru GRI above 60th percentile: labor unrest / nationalization risk
- DRC GRI sustained elevation: artisanal mining disruption (cobalt supply signal)
- Indonesia GRI spike: export ban risk (nickel, bauxite)

**Target assets:** LME Copper (LMAHDS03), LME Nickel, LME Cobalt, Lithium Carbonate Spot

### Module 3 — Agricultural Commodities

**Key geographies:** Ukraine, Russia (Black Sea), Argentina, Brazil
**Key chokepoints:** Turkish Straits (Black Sea grain corridor), Panama Canal (US grain)
**GRI → CPS logic:**
- Ukraine GRI > 80th percentile: Black Sea corridor disruption → wheat/corn/sunflower upward pressure
- Argentina GRI spike: FX crisis → export withholding risk → soybean price distortion
- Russia GRI + Turkey GRI simultaneously elevated: grain deal collapse risk

**Target assets:** CBOT Wheat, CBOT Corn, CBOT Soybeans, CME Sunflower Oil

### Module 4 — Uranium & Nuclear Fuel

**Key geographies:** Kazakhstan, Niger, Namibia, Australia (political stability benchmark)
**GRI → CPS logic:**
- Kazakhstan GRI elevation: ~42% of global uranium production at risk
- Niger GRI spike (post-2023 coup baseline): French supply chain disruption
- Russia GRI sustained: secondary effects on enrichment capacity (ROSATOM dependency)

**Target assets:** UXC Uranium Spot (U3O8), Sprott Physical Uranium Trust (SRUUF)

### Module 5 — Rare Earths & Semiconductor Materials

**Key geographies:** China (dominant), Myanmar (heavy rare earths), South Africa (platinum group)
**GRI → CPS logic:**
- China GRI elevated + US-China friction index elevated: export restriction probability model
- Myanmar GRI sustained: tantalum/tin supply disruption
- South Africa GRI elevation: platinum/palladium/rhodium mine disruption (power, strikes)

**Target assets:** MP Materials (MP), Lynas (LYC.AX), Palladium futures (CME PAD)

---

## IV. The Technical Architecture in Databricks

### Gold Table: `gri_commodity_pressure`

```python
# Schema
schema = StructType([
    StructField("date", DateType()),
    StructField("commodity_module", StringType()),      # "crude_oil", "copper", "agriculture", etc.
    StructField("commodity_name", StringType()),         # "WTI", "LME_Copper", "CBOT_Wheat"
    StructField("contributing_countries", ArrayType(StringType())),
    StructField("weighted_gri_input", DoubleType()),     # Supply-share-weighted avg GRI
    StructField("cps_raw", DoubleType()),                # Pre-normalization score
    StructField("cps_normalized", DoubleType()),         # -2 to +2 z-score
    StructField("cps_regime", StringType()),             # "strong_up", "moderate_up", "neutral", etc.
    StructField("trend_7d", DoubleType()),               # 7-day CPS change
    StructField("signal_fired", BooleanType()),          # True if CPS crossed regime boundary
    StructField("signal_direction", StringType()),       # "upward_pressure", "downward_pressure", "none"
    StructField("pipeline_run_ts", TimestampType())
])
```

### The Weighting Engine

The CPM's analytical edge is supply-share weighting. A GRI spike in Nigeria matters less for global oil than a GRI spike in Saudi Arabia because Nigeria produces ~1.4 mb/d vs Saudi Arabia's ~9.5 mb/d. Every country in the supply geography matrix is assigned a **supply share weight** based on its percentage of global production/export of the relevant commodity.

```python
# Supply share weights (example: crude oil)
CRUDE_OIL_WEIGHTS = {
    "Saudi Arabia": 0.107,   # ~10.7% global supply
    "Russia": 0.112,         # ~11.2% (post-sanction adjusted)
    "United States": 0.143,  # ~14.3% (minimal geopolitical risk weight)
    "Iraq": 0.046,
    "UAE": 0.044,
    "Iran": 0.038,           # Under sanctions — disruption asymmetric
    "Kuwait": 0.026,
    "Nigeria": 0.014,
    "Libya": 0.011,
    "Kazakhstan": 0.019
}

def compute_weighted_gri(country_gri_scores: dict, weights: dict) -> float:
    """Supply-share-weighted average GRI for a commodity."""
    total_weight = sum(weights.get(c, 0) for c in country_gri_scores)
    if total_weight == 0:
        return 0.0
    return sum(
        country_gri_scores[c] * weights.get(c, 0)
        for c in country_gri_scores
        if c in weights
    ) / total_weight
```

### The Chokepoint Multiplier

For commodities with critical chokepoints, the CPM applies a multiplier when GRI elevation is detected in the chokepoint country:

```python
CHOKEPOINT_MULTIPLIERS = {
    # (chokepoint_country, commodity_module): multiplier
    ("Iran", "crude_oil"): 1.35,        # Hormuz closure risk
    ("Yemen", "crude_oil"): 1.15,       # Bab-el-Mandeb
    ("Egypt", "crude_oil"): 1.20,       # Suez
    ("Egypt", "agriculture"): 1.25,     # Suez grain transit
    ("Turkey", "agriculture"): 1.30,    # Black Sea corridor
    ("Ukraine", "agriculture"): 1.40,   # Source, not transit
    ("Panama", "agriculture"): 1.10,    # Panama Canal US grain
    ("Indonesia", "copper"): 1.15,      # Nickel export ban precedent
    ("China", "rare_earths"): 1.50,     # Dominant production + export control risk
}

def apply_chokepoint_multiplier(base_cps: float, elevated_countries: list, commodity: str) -> float:
    multiplier = 1.0
    for country in elevated_countries:
        key = (country, commodity)
        if key in CHOKEPOINT_MULTIPLIERS:
            multiplier = max(multiplier, CHOKEPOINT_MULTIPLIERS[key])
    return base_cps * multiplier
```

### Normalization: The Z-Score Window

To make CPS comparable across time and commodity, normalize against a 180-day rolling window:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

window_180d = Window.partitionBy("commodity_name").orderBy("date").rowsBetween(-180, 0)

df_cps = df_raw.withColumn(
    "cps_mean_180d", F.avg("cps_raw").over(window_180d)
).withColumn(
    "cps_std_180d", F.stddev("cps_raw").over(window_180d)
).withColumn(
    "cps_normalized",
    F.when(F.col("cps_std_180d") > 0,
        (F.col("cps_raw") - F.col("cps_mean_180d")) / F.col("cps_std_180d")
    ).otherwise(0.0)
).withColumn(
    "cps_normalized", F.least(F.greatest(F.col("cps_normalized"), F.lit(-2.0)), F.lit(2.0))
)
```

---

## V. Backtesting Framework — Validating the CPM Before Going Live

Before the CPM drives any position recommendation, it must pass a basic validation test. The question: **does CPS elevation precede commodity price increases with statistical significance?**

**Test design:**

1. Pull historical CPS (reconstructed from GDELT historical data) for 2018–2024
2. Pull corresponding commodity price returns (WTI, LME Copper, CBOT Wheat, etc.)
3. Define "CPS signal": CPS crosses from neutral to moderate_up or strong_up
4. Measure: average commodity return over 5, 10, 20, 30 days following signal
5. Compare: signal-following returns vs. unconditional returns (all trading days)

**Success threshold:** Signal-following returns exceed unconditional returns by >100bps on a 20-day horizon, with hit rate >55%.

If the CPM does not clear this threshold for a given commodity module, that module's CPS output is flagged as "informational only" — it appears in dashboards but does not feed the Investment Signal Generator.

---

## VI. Integration with the Morning Note (Lesson 299 Architecture)

The CPM output connects directly into the CEO Morning Note:

```
COMMODITY PRESSURE SUMMARY — 2026-09-05
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Crude Oil         ██████████░░  CPS: +1.2  [MODERATE UP]
  LME Copper        ████░░░░░░░░  CPS: +0.3  [NEUTRAL]
  CBOT Wheat        ████████████  CPS: +1.8  [STRONG UP]  ⚠ SIGNAL FIRED
  Uranium           █████░░░░░░░  CPS: +0.4  [NEUTRAL]
  Rare Earths       ██████░░░░░░  CPS: +0.5  [MODERATE UP]

Top driver: Ukraine GRI +1.8σ (7-day trend) → Black Sea corridor risk elevated
Action: Review CBOT wheat position thesis. Chokepoint multiplier active (Turkey 1.3x).
```

---

## Investment Implications

The CPM produces its highest alpha signals in three scenarios:

**1. Pre-conflict elevation (weeks before kinetic escalation)**
When GRI scores in supply geographies rise steadily for 2–4 weeks before a widely-reported military escalation, the CPM has already fired. The commodity market tends to price disruption risk sharply at the point of widely-reported escalation — but the patient investor who entered on the CPM signal captured the move with better risk/reward.

**2. De-escalation false recovery**
When a ceasefire or negotiation announcement drives commodity prices sharply lower, the CPM may still show elevated underlying risk (because GDELT event counts and tone remain elevated even as a headline agreement is signed). This is a short-sale or re-entry signal — the market repriced too quickly.

**3. Structural supply shift detection**
When a country's GRI remains elevated for >90 days (not a spike but a sustained regime change), the CPM enters a "structural pressure" mode that weights the signal toward longer-horizon positions (6–18 months) rather than tactical trades.

**Asset classes most directly affected:**
- **Commodities:** Direct signal via CPS
- **EM equities:** Commodity exporter equities (Chile copper miners, Saudi Aramco, Brazilian agricultural companies)
- **EM FX:** Commodity-linked currencies (CLP, PEN, ZAR, RUB, BRL) — the CPM is a leading indicator for EM FX moves
- **Developed market inflation:** CPS elevation in agriculture and energy is a 4–8 week leading indicator for headline CPI surprises

---

## Databricks Angle

**Build priority for this week:**

1. Create `supply_geography_weights` Delta table — commodity → country → weight (static, maintained quarterly)
2. Create `chokepoint_multipliers` Delta table — country + commodity → multiplier
3. Write `silver_commodity_pressure_raw` pipeline: joins `gold_gri_scores` → weights → raw CPS per commodity
4. Write `gold_commodity_pressure_signals` pipeline: normalization + regime classification + signal detection
5. Extend `gold_ceo_morning_note` to include CPM section

**Relevant datasets:**
- **EIA (eia.gov):** Country-level oil and gas production data (annual, free)
- **USGS Mineral Commodity Summaries:** Country production shares for copper, lithium, cobalt, REE (annual, free)
- **USDA PSD Database:** Production, Supply, and Distribution data for agricultural commodities by country
- **World Nuclear Association:** Uranium production data by country

**Pipeline estimate:** 3–4 Databricks notebooks, ~150 lines of PySpark total. This is a 2-day build for Bolo.

---

## Questions for Next Session

1. **Supply weights are static in this architecture — updated quarterly. What would change if you made them dynamic (updated monthly from EIA/USGS live data), and is the added complexity worth it?**

2. **The chokepoint multiplier is currently additive (takes the maximum multiplier). What are the failure modes of this design — when would it overstate or understate pressure?**

3. **The 180-day normalization window was chosen to balance recency and stability. How would the CPM behave differently with a 90-day window? A 365-day window? What kind of geopolitical events would each window miss?**

---

## CEO Note — Milestone 300

Lesson 300. We entered this project with a 12-topic curriculum and a thesis that geopolitical events systematically misprice financial assets. We now have:
- 300 lessons delivered covering geopolitics, macroeconomics, financial architecture, and data engineering
- A complete Phase 1 Databricks pipeline: GDELT ingestion → GRI signal → dashboard → morning note
- A live investment framework with documented theses and tracked calls
- Phase 2 beginning today with the Commodity Pressure Model — the bridge from risk detection to investment action

The 3-month clock from the original PROJECT_FOUNDATION.md is well past. The framework has compounded. The edge is real when it's applied with discipline. Phase 2 is where the framework becomes a systematic investment process. Build it well.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 300 delivered 2026-09-05*
