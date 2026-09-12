# Lesson 324 — The Weekly Signal Selection Protocol: From GRI Delta Scan to Publication Commitment

**Date:** 2026-09-13
**Session Type:** Daily Lesson
**Lesson Number:** 324 / ongoing
**Topic:** The Weekly Signal Selection Protocol — Operationalizing the GRI Delta Scan
**Curriculum Arc:** Live Operations Module — Lesson 9: Systematic Signal Generation

---

## Opening Question

*Signal #1 is live. You have a track record with one row. The question that determines whether the next 25 rows form a credible body of evidence — or a collection of opportunistic calls — is not "what does the GRI say this week?" It is:*

**"What is the decision process that produces Signal #2 — and is it identical to the process that will produce Signal #26?"**

The failure mode of a systematic research product built on a live publication schedule is not poor analysis. It is *inconsistent selection*. If Signal #2 is chosen because Turkey looks interesting this week, Signal #7 because you read a headline about Brazil, and Signal #14 because a quant fund analyst mentioned Pakistan in a newsletter — the track record will contain 26 individually defensible signals and no replicable methodology. An institutional reviewer will ask: "How do you select signals?" If the answer cannot be described in a process document that runs identically every Tuesday morning, the methodology is not systematic.

This lesson builds that process document.

---

## I. The Structure of the Weekly Cycle

The weekly signal selection cycle runs from Tuesday through Monday publication. The specific day assignments matter: they create a habit architecture that ensures the selection decision is made from data, not from recency bias, deadline pressure, or market noise.

### Tuesday: GRI Delta Scan (90 minutes)

The cycle begins with a structured database query against the GRI, not with reading news. News follows the scan — never precedes it. If the scan leads with news, selection will be biased toward countries with the most recent coverage, not countries with the highest analytically-significant GRI delta.

**The Tuesday scan protocol:**

```python
# weekly_signal_scan.py
# Run every Tuesday morning — the GRI delta scan that opens the signal selection process.
# Output: a ranked candidate list. The signal is selected from this list, not from news.

from pyspark.sql import functions as F

gri = spark.table("prospectra.silver.gri_weekly_scores")
track = spark.table("prospectra.gold.signal_track_record")

# ── 1. Calculate GRI delta for the past 4 weeks ──────────────────────────────
# Delta = (current week score - 4-week average) / historical std dev (z-score)
w = Window.partitionBy("country_code", "gri_sub_dimension").orderBy("week_date")
gri_with_stats = (
    gri
    .withColumn("rolling_4w_avg", F.avg("gri_score").over(w.rowsBetween(-4, -1)))
    .withColumn("rolling_std",    F.stddev("gri_score").over(w.rowsBetween(-12, -1)))
    .withColumn("gri_z_score",
        (F.col("gri_score") - F.col("rolling_4w_avg")) / F.col("rolling_std")
    )
)

# ── 2. Filter to this week's scores — keep only significant deltas ────────────
current_week = gri_with_stats.filter(F.col("week_date") == F.current_date() - 7)
candidates = (
    current_week
    .filter(F.abs("gri_z_score") >= 1.5)   # 1.5 std deviations = analytically significant
    .filter(F.col("gri_score").isNotNull())
)

# ── 3. Exclude recently covered countries (prevent geographic concentration) ──
recent_countries = (
    track
    .filter(F.col("publication_date") >= F.current_date() - 56)  # past 8 weeks
    .select("country_code").distinct()
)
candidates_filtered = candidates.join(recent_countries, on="country_code", how="left_anti")

# ── 4. Flag sub-dimension gaps (enforce systematic coverage) ─────────────────
dimension_counts = (
    track.groupBy("gri_sub_dimension").count().withColumnRenamed("count", "n_signals")
)
candidates_with_gap_flag = (
    candidates_filtered
    .join(dimension_counts, on="gri_sub_dimension", how="left")
    .withColumn("n_signals", F.coalesce("n_signals", F.lit(0)))
    .withColumn("underrepresented", F.col("n_signals") < 3)  # flag sub-dims with <3 signals
)

# ── 5. Rank candidates: z-score first, then underrepresented sub-dims ─────────
from pyspark.sql.window import Window as W
rank_window = W.orderBy(F.col("gri_z_score").desc(), F.col("underrepresented").desc())
ranked = (
    candidates_with_gap_flag
    .withColumn("rank", F.rank().over(rank_window))
    .filter(F.col("rank") <= 10)
    .select(
        "rank", "country_code", "country_name", "gri_sub_dimension",
        "gri_score", "rolling_4w_avg", "gri_z_score",
        "n_signals", "underrepresented"
    )
    .orderBy("rank")
)

ranked.show(10, truncate=False)
```

The output is a ranked list of up to 10 candidate countries and sub-dimensions. The top 3 by z-score become the "active candidates" that proceed to Wednesday's instrument and consensus check.

**Decision rule:** If no candidate has a z-score ≥ 1.5, do not manufacture a signal that week. Publish a "Signal Hold" note explaining that the GRI delta scan found no analytically significant movement and the next signal will run when the data warrants it. A signal hold is evidence of methodological discipline — not a failure. An institutional reviewer who sees three signal holds in a 26-signal track record will conclude the framework produces signals when the data justifies them, not on a forced weekly schedule.

---

## II. Wednesday: Instrument Selection and Consensus Check (60 minutes)

From Tuesday's ranked candidates, proceed to Wednesday's check on the top 3 candidates. The Wednesday work answers two questions for each candidate:
1. What is the appropriate instrument for this GRI signal — and is it liquid enough to have a clean outcome?
2. What is the current market consensus on this country and instrument — and does the GRI signal diverge?

### Instrument Selection Criteria

The GRI sub-dimension determines the instrument class. Map the sub-dimension to the instrument using this hierarchy:

| GRI Sub-Dimension | Primary Instrument | Rationale |
|---|---|---|
| `central_bank_independence` | Currency pair (USD/XXX) | Central bank risk prices directly into FX |
| `external_conflict_risk` | Sovereign CDS (5yr) or currency | External conflict = credit risk + currency flight |
| `political_stability` | Currency or country equity ETF | Political instability shows in FX before equities |
| `sanctions_risk` | Currency + sovereign spread | Sanctions impose both credit and FX dislocations |
| `fiscal_stress` | Sovereign bond spread (10yr vs. UST) | Fiscal deterioration prices into bond spreads |
| `rule_of_law` | Country equity ETF | Institutional degradation prices into equity premium |
| `resource_nationalism` | Commodity price (if applicable) or EM equity | Resource nationalism directly hits commodity supply |
| `capital_controls` | Currency pair (NDF if needed) | Capital controls most directly affect FX |

**Liquidity screen:** An instrument is eligible if it has at least $50M average daily volume (for ETFs) or a functioning derivative market (for currencies and CDS). Illiquid instruments produce untestable signals — if the instrument doesn't move cleanly on the event, the outcome cannot be attributed to the GRI call.

### Consensus Check Protocol

For each candidate instrument, record the following before selecting a signal:

1. **Forward market pricing:** What is the 1-month and 3-month implied move in the instrument? (For currencies: forward rate vs. spot. For bonds: current spread vs. 6-month average.)
2. **Sell-side consensus:** What is the dominant sell-side directional view? (30-second scan of one Bloomberg Intelligence piece or EM macro research note, if accessible.)
3. **Positioning data:** Is the instrument currently overbought or oversold by CTA/systematic positioning? (CFTC COT reports for currencies; ETF flows for equity.)

**Record this in a pre-signal consensus note**, committed to the decisions document before the signal is published. This note is the forensic evidence at Signal #26 that demonstrates whether each call was non-consensus at the time of publication.

The consensus check is non-negotiable. If you skip it for any signal, you cannot make the institutional claim that the track record demonstrates non-consensus analytical alpha. The check takes 20 minutes per candidate. Do it.

---

## III. Thursday: Historical Analogue Research (45 minutes)

The historical analogue is the mechanism that connects the GRI delta to the directional call on the instrument. It is not a rhetorical flourish — it is the framework's core analytical claim: "When this GRI sub-dimension moved by this magnitude in a structurally similar country, the instrument moved in this direction by this magnitude over this timeframe."

The Thursday work is to find the three best historical analogues for the selected candidate's GRI signal. The criteria for a strong analogue:

1. **Same sub-dimension**: The historical case involves the same GRI dimension (e.g., if the current signal is `central_bank_independence` deterioration, the analogue must also be a central bank independence event — not a generic EM sell-off).
2. **Similar GRI delta magnitude**: The historical z-score should be within 0.5 standard deviations of the current candidate's z-score.
3. **Similar structural context**: Country GDP per capita, debt-to-GDP, and reserve coverage within 30% of the current candidate's levels. A large-reserve, high-income country does not analogue cleanly to a reserve-constrained frontier market.
4. **Sufficient distance from current events**: The analogue should be from at least 3 years ago to avoid recency bias.

**The historical analogue generates three outputs:**
- The median price move in the instrument at 30, 60, and 90 days post-event
- The range of outcomes (floor and ceiling) across the comparable cases
- The event that triggered the repricing in the historical cases — which informs the `forward_watch_event` in the current signal

The falsifiability condition should name a specific event analogous to the historical trigger: not "deteriorating political conditions" but "presidential veto of the independent central bank appointment process" or "CDS spread exceeding 450bps." Specific. Named. Testable.

---

## IV. Friday: Signal Draft and Pre-Publication Conviction Check (45 minutes)

Friday's work is to write the signal draft and apply the conviction calibration policy written before Signal #1. No deviation. The policy is a commitment, not a guideline.

### The Pre-Publication Checklist

Before committing to the signal direction and conviction level, verify:

- [ ] GRI z-score is ≥ 1.5 and is the highest of the candidate set (or explicitly explain why a lower-ranked candidate was selected)
- [ ] The instrument has been selected per the sub-dimension mapping above
- [ ] The consensus note is written and committed — the signal's consensus divergence (or alignment) is documented
- [ ] At least one historical analogue has been identified with a quantified median price move
- [ ] The `forward_watch_event` names a specific, datable event (not a condition)
- [ ] The conviction level has been assigned per the written policy — not per how confident you feel this week

**The conviction double-check:** After assigning conviction, ask: "Would I assign this same conviction level to a signal with the same GRI z-score and catalyst clarity in a country I know less well?" If the answer is no — if the conviction is partly driven by familiarity with the country rather than the data — downgrade by one tier. Familiarity is a bias, not a signal.

### The Signal Structure (Standardized Format)

The signal must follow the same structure as Signal #1 — identical section headers, identical schema fields populated. The **only** variance between signals is the content, not the format.

```
SIGNAL #{N} — {COUNTRY} / {SUB-DIMENSION}
Publication date: {date}
Instrument: {instrument}
Direction: {LONG / SHORT / NEUTRAL}
Conviction: {HIGH / MEDIUM / LOW}
Timeframe: {30 / 60 / 90 days}
GRI delta: {z-score} (current: {score} vs. 4-week avg: {avg})
Historical analogue: {1-line description}
Falsifiability condition: {named event} by {date}
Forward watch event: {event}
Consensus divergence: {with-consensus / non-consensus} — {one sentence}
```

Every field. Every signal. The institutional reviewer at Signal #26 will read the first signal and the last. If the format has drifted, the methodology has drifted. Format stability is methodology stability.

---

## V. Monday: Publication and Schema Commit (30 minutes)

Monday's work is publication and the simultaneous commit of the signal to `prospectra.gold.signal_track_record`. The two actions happen in the same work block.

**The critical discipline:** Do not revise the signal after the Substack draft is sent. The moment the signal is in the Substack draft queue, the analysis is committed. Any revision after that point — even to "sharpen the language" — is a form of post-hoc optimization. The track record's credibility depends on the signal being committed before its outcome is known.

**The Monday schema commit:**

```python
from pyspark.sql import Row
import datetime

new_signal = Row(
    signal_id                  = "SIG-{N:03d}",
    publication_date           = datetime.date.today(),
    country_code               = "{ISO3}",
    country_name               = "{country}",
    gri_sub_dimension          = "{sub_dimension}",
    gri_score_at_signal        = {score},
    gri_weekly_delta           = {delta},
    gri_z_score                = {z_score},
    instrument                 = "{instrument}",
    direction                  = "{LONG/SHORT/NEUTRAL}",
    conviction                 = "{HIGH/MEDIUM/LOW}",
    timeframe_days             = {30/60/90},
    forward_watch_event        = "{specific named event}",
    forward_watch_date         = datetime.date({year}, {month}, {day}),
    historical_analogue        = "{one-line description}",
    falsifiability_condition   = "{named event by date}",
    consensus_divergence       = "{with/non-consensus}",
    instrument_vol_30d_at_signal = {vol},   # added at Signal #2
    outcome_direction_correct  = None,      # populated at target date
    outcome_price_change_pct   = None,      # populated at target date
    outcome_notes              = None,      # populated at target date
    analyst_notes              = "{this signal's one improvement over previous}"
)

signal_df = spark.createDataFrame([new_signal])
signal_df.write.format("delta").mode("append").saveAsTable("prospectra.gold.signal_track_record")
```

The Delta Lake transaction log records the exact timestamp of this commit. That timestamp — before the signal's outcome date — is the forensic proof that the call was made before the result was known.

---

## VI. The Weekly Rhythm as a Competitive Moat

The five-step weekly protocol — Tuesday scan, Wednesday consensus, Thursday analogue, Friday draft, Monday publish — is not just an operational habit. It is the analytical infrastructure that separates Prospectra from discretionary geopolitical commentary.

Most geopolitical research is produced in response to events: a crisis happens, an analyst writes about it. That research is valuable as context but does not generate alpha — the event has already repriced the instrument by the time the analysis is published.

Prospectra's competitive position is *pre-event*: the GRI delta scan identifies countries where analytical conditions are deteriorating before the market has priced the move. The Tuesday scan is the mechanism that maintains this pre-event advantage. If the scan runs on Tuesday, the signal is published Monday — the analyst has six days to think before publishing. If the signal selection is driven by Wednesday's news, the analysis is reactive by definition.

**The discipline of running Tuesday's scan before reading any news that week is the single most important operational habit in the signal production process.** Set a calendar block: Tuesday 8:00 AM — GRI delta scan. No news, no Bloomberg, no Twitter until after the scan is complete and the candidate list is ranked. The scan leads; the news confirms or contradicts.

---

## Investment Implications

### The Signal Cadence as Pricing Signal

The weekly signal protocol has an investment implication beyond the individual signals it produces: the existence of a systematic, pre-event scanning process in EM geopolitical risk means that Prospectra's selection of a country as a signal subject is itself a signal to the institutional investor community.

When Prospectra publishes a signal on Country X, the institutional reader's first question should be: "What did the GRI delta scan show this week that made Country X the highest-ranked candidate?" The answer to that question — available in the signal's `gri_z_score` and `gri_weekly_delta` fields — is the data point that distinguishes Prospectra's calls from commentary.

**For the Substack reader base:** Once the track record reaches 5–10 signals, begin publishing the GRI delta scan shortlist (the top 3–5 candidates that were *not* selected for the current signal) as a weekly companion post. The shortlist demonstrates the discipline of the selection process — showing the signals that were considered and rejected because their z-scores were lower or their sub-dimensions were already overrepresented. That transparency is the credibility architecture that differentiates systematic research from opinion.

**Asset class implication:** The Tuesday scan's output — countries where the GRI z-score exceeds 1.5 but instrument volatility remains low — is a list of potential asymmetric trades. Low volatility means cheap optionality. High GRI delta means a catalyst is building. For investors who trade options on EM currencies or equity ETFs, the scan shortlist identifies the countries where implied volatility may be systematically underpriced relative to the geopolitical event risk that has not yet been priced by the forward market.

---

## Databricks Angle

**Build: The Weekly Signal Selection Pipeline (Automated Tuesday Scan)**

The GRI delta scan described in Section I should be automated as a Databricks workflow that runs every Tuesday at 7:00 AM and writes its output to `prospectra.silver.signal_candidates_weekly`.

```python
# weekly_signal_scan_pipeline.py
# Databricks workflow — runs every Tuesday 07:00
# Writes ranked candidates to prospectra.silver.signal_candidates_weekly

from pyspark.sql import functions as F
from pyspark.sql.window import Window
import datetime

# ── Load and calculate GRI deltas ────────────────────────────────────────────
gri = spark.table("prospectra.silver.gri_weekly_scores")
track = spark.table("prospectra.gold.signal_track_record")

w = Window.partitionBy("country_code", "gri_sub_dimension").orderBy("week_date")
gri_zscored = (
    gri
    .withColumn("rolling_4w_avg", F.avg("gri_score").over(w.rowsBetween(-4, -1)))
    .withColumn("rolling_std",    F.stddev("gri_score").over(w.rowsBetween(-12, -1)))
    .withColumn("gri_z_score",
        (F.col("gri_score") - F.col("rolling_4w_avg")) / F.col("rolling_std")
    )
    .filter(F.col("week_date") == F.current_date() - 7)
    .filter(F.abs("gri_z_score") >= 1.5)
)

# ── Exclude recent countries ──────────────────────────────────────────────────
recent = track.filter(
    F.col("publication_date") >= F.current_date() - 56
).select("country_code").distinct()

dim_counts = (
    track.groupBy("gri_sub_dimension")
    .count().withColumnRenamed("count", "n_signals")
)

candidates = (
    gri_zscored
    .join(recent, on="country_code", how="left_anti")
    .join(dim_counts, on="gri_sub_dimension", how="left")
    .withColumn("n_signals", F.coalesce("n_signals", F.lit(0)))
    .withColumn("underrepresented", F.col("n_signals") < 3)
    .withColumn("scan_date", F.current_date())
    .withColumn("rank",
        F.rank().over(
            Window.orderBy(
                F.col("gri_z_score").desc(),
                F.col("underrepresented").desc()
            )
        )
    )
)

# ── Write to silver layer ─────────────────────────────────────────────────────
(
    candidates
    .filter(F.col("rank") <= 10)
    .write.format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable("prospectra.silver.signal_candidates_weekly")
)

print(f"Scan complete: {candidates.filter('rank <= 3').count()} active candidates for this week.")
candidates.filter("rank <= 3").show(truncate=False)
```

**Databricks workflow schedule:** Go to Databricks Workflows → Create Job → add this notebook → set trigger to "Scheduled" → CRON expression `0 7 * * 2` (7:00 AM every Tuesday). Add a Slack or email notification on failure.

**Why this matters:** When the scan runs automatically, it runs before you've read any news. The output is waiting in `prospectra.silver.signal_candidates_weekly` when you open Databricks on Tuesday morning. The data leads; the analysis follows. Remove the human from the scanning step and you remove the recency bias that would otherwise corrupt the selection process.

---

## Key Concepts Covered

1. **The Tuesday GRI delta scan** — the data-first process that opens the weekly signal selection cycle, using z-scores to identify analytically significant country/sub-dimension movements before any news input
2. **The geographic and sub-dimension exclusion filters** — the systematic rules that enforce coverage diversity and prevent the track record from concentrating in familiar countries
3. **The Wednesday consensus check** — the pre-publication protocol for documenting whether each signal is with-consensus or non-consensus at publication time, creating the forensic record needed for the institutional pitch
4. **The instrument selection hierarchy** — mapping GRI sub-dimensions to their natural instrument expressions based on transmission mechanism
5. **The historical analogue research protocol** — the Thursday process for identifying comparable cases that quantify the expected magnitude and timing of the instrument move
6. **The conviction double-check** — the practice of testing conviction assignments against unfamiliar countries to identify familiarity bias in the rating process
7. **The automated Tuesday scan pipeline** — the Databricks workflow that removes human timing bias from the candidate identification step

---

## Reflection Questions

1. **The scan-before-news discipline:** On Tuesday this week, set a calendar block for the GRI delta scan before you open any financial news. Run the scan query, write down the top 3 candidates and their z-scores. Then read the news. Ask: does any major news story this week correspond to a country in your top 3? If yes, the GRI is detecting the event signal. If no, you have a potential lead on a story the market hasn't fully priced. Which situation applies this week?

2. **Conviction policy review:** Pull up the conviction policy you committed before Signal #1. Now apply it to Signal #1 retroactively: if you apply the policy strictly — GRI z-score in the top quartile AND named catalyst within timeframe for `high` conviction — does Signal #1's conviction label hold? If it doesn't pass its own policy test, revise the policy now (before Signal #2), document the revision, and explain in the `analyst_notes` field why the policy changed. Revising the policy before Signal #2 is methodological learning. Revising it after Signal #5 is post-hoc rationalization.

3. **The shortlist transparency question:** Section VI proposes publishing the signal shortlist (the 3–5 candidates not selected each week) as a companion Substack post. Consider the tradeoff: publishing the shortlist demonstrates analytical discipline and builds credibility, but it also creates a public record of signals you considered and passed on. If a passed-over country subsequently has a major event, readers will see it in the historical shortlist. Is that risk worth the credibility benefit? What would a systematic research product publish: the shortlist with z-scores, a narrative summary of candidates considered, or nothing beyond the selected signal?

---

## Questions for Next Session (Spaced Repetition Hook)

- What were the top 3 candidates from this week's Tuesday GRI delta scan — country, sub-dimension, z-score?
- Was Signal #1 with-consensus or non-consensus at publication time? (Refer to the consensus note committed before publication.)
- Has the automated Tuesday scan pipeline been built and scheduled in Databricks?
- What was the `instrument_vol_30d_at_signal` for Signal #1 — and has it been backfilled into the schema?
- At Signal #2 publication, will the `analyst_notes` field name the specific improvement over Signal #1?

---

## Databricks Relevance Note

**The `signal_candidates_weekly` Table as a Research Asset**

The weekly scan output, persisted to `prospectra.silver.signal_candidates_weekly` with the scan date, becomes a research asset in its own right. At Signal #26, you can query this table to show an institutional reviewer the full universe of candidates that were identified but not selected over 26 weeks — demonstrating that the signals were chosen from a systematic scan rather than selected opportunistically. The unselected candidates (those that ranked in the top 10 but were not chosen) provide a natural counterfactual: if the GRI framework identifies countries correctly, the unselected candidates should also have exhibited notable instrument moves in the direction the z-score implied. Querying this counterfactual dataset — "what happened to the countries we identified but didn't signal on?" — is additional evidence that the GRI delta is predictive of market outcomes, not just correlated with events.

Build a quarterly notebook query: for each week's `rank 2` and `rank 3` candidates (the candidates identified but not selected), what was the instrument's directional move in the 60 days following the scan? If the GRI delta scan is doing its job, the moved-but-not-signaled candidates should show a non-random directional distribution. That result strengthens the framework's credibility even from signals you didn't publish.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 324 | September 13, 2026 | Live Operations Module — Lesson 9: Systematic Signal Generation*
