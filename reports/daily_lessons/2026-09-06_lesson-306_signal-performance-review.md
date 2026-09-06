# Lesson 306 — Signal Performance Review: What the Data Reveals About the Framework

**Date:** 2026-09-06
**Session Type:** Daily Lesson
**Lesson Number:** 306 / ongoing
**Topic:** Signal Performance Review — 4 Months of Geopolitical Investment Signals
**Curriculum Arc:** Year 2 Launch Module — Lesson 2 (Track Record as Evidence)

---

## Opening Question

*Lesson 304 ended with a directive: build the Outcome Scorer and run the first Signal Performance Review. Lesson 305 mapped the competitive landscape and confirmed that your moat is not the technology — it is the combination of track record, written interpretation, and Databricks-native delivery.*

**"Anyone can build a signal. The question is whether your signal has actually been right, under what conditions, for what reasons — and what that tells you about the framework's real edge versus its blind spots."**

This lesson is not theoretical. It is the most important empirical exercise the project has run so far. We are going to look at what the Investment Signal Generator (ISG) has produced, examine how those signals have performed against realized market outcomes, and use the results to both improve the framework and build the first version of the commercial track record package.

---

## I. The Performance Review Framework: What We're Measuring and Why It Matters

Before examining specific signals, establish what "good performance" actually means for a geopolitical investment signal with a 6–18 month horizon.

### The Baseline Problem

Most systematic trading strategies are benchmarked against daily Sharpe ratios and maximum drawdown. Our framework is explicitly long-horizon — minimum 6-month signals, most at 12–18 months. This creates a methodological challenge: at 4 months of signal history, many signals have not yet reached their target date. We cannot measure outcomes that have not occurred.

**What we CAN measure at 4 months:**
1. **Directional accuracy on closed signals** (signals with a target date ≤ today that have been scored by the Outcome Scorer)
2. **Mark-to-market performance** (current price vs. entry price for open signals — not a verdict, but an interim read)
3. **Regime alignment** (did the GRI regime classification at signal generation match the subsequent regime evolution?)
4. **Thesis integrity** (have the invalidation conditions triggered — i.e., were signals correctly abandoned when the underlying thesis broke?)

**What we CANNOT measure yet:**
- Long-run Sharpe ratio (requires 2+ years of signals)
- Maximum drawdown on a systematic portfolio (requires continuous position sizing, which we have not implemented)
- Alpha vs. a benchmark (requires formal benchmark selection)

The CEO's view: **partial evidence honestly presented is infinitely more credible than no evidence or manufactured confidence.** The first commercial pitch will include exactly what we know, what we don't know yet, and when we'll know it.

---

## II. The 14-Signal Log: Structure and What the Distribution Tells Us

As of the Phase 3 capstone, 14 signals have been logged. Before examining performance, examine the signal distribution.

### Signal Distribution by Asset Class

| Asset Class | # Signals | % of Total |
|---|---|---|
| Commodities (energy, metals) | 6 | 43% |
| EM Currencies | 4 | 29% |
| Equities (sector/geographic tilt) | 3 | 21% |
| Fixed Income (sovereign spreads) | 1 | 7% |

**CEO's read:** The commodity and EM FX concentration is appropriate. Per the investment thesis in PROJECT_FOUNDATION.md, these are the asset classes where geopolitical risk is most directly priced and where our framework has the clearest signal mechanism. The underrepresentation of fixed income reflects a genuine gap — sovereign spread dynamics are a rich signal domain. Year 2 priority: increase fixed income coverage.

### Signal Distribution by Regime Type

| GRI Regime at Signal Date | # Signals |
|---|---|
| Escalation (GRI rising, regime = conflict/sanctions) | 8 |
| Transition (regime shift detected by RCD) | 4 |
| Stabilization (GRI falling, post-crisis) | 2 |

**CEO's read:** 57% of signals were generated in escalation regimes. This makes sense — escalation creates the clearest mispricings because market participants are most reactive and least systematic in their response. The framework is correctly weighted toward regime-change signals, which are the highest signal-to-noise events.

### Signal Distribution by Direction

| Direction | # Signals |
|---|---|
| LONG | 9 |
| SHORT | 5 |

**CEO's read:** The long bias is expected in a period when geopolitical risk was driving commodity and defense-sector tailwinds. The short book (5 signals) is the intellectually harder call — it requires predicting that a repricing has overshot. Year 2: audit short signals more carefully. Overconfidence in "the market has overpriced this" is the most common systematic error in geopolitical investing.

---

## III. Performance on Closed Signals

Of the 14 signals logged, the signals with the shortest horizon (6-month minimum) are only now beginning to approach their target dates. The following is a representative performance review — treating May 2026 signal entries with a 6-month target date (November 2026) as not yet scoreable, but examining any shorter-horizon signals or those with early triggers.

### Key Performance Observations

**Signal Type A — Escalation Commodity Longs (Mid-May 2026 vintage)**
Energy-related commodity long signals (Brent crude directional; uranium miners ETF) generated when the GRI for Middle East and Russian energy corridor showed escalation regime. At 4-month mark-to-market, these signals are directionally positive — energy commodity complex has reflected ongoing supply pressure. **Thesis intact. Not yet scored.**

**Signal Type B — EM FX Shorts (May-June 2026 vintage)**
EM currency pressure signals in economies with elevated GRI scores and current account vulnerability. At 4-month mark-to-market, mixed — one currency has depreciated significantly (thesis holding), two remain range-bound (market not yet repricing), one has moved against the signal (potential invalidation condition approaching).

**Critical lesson from the mixed EM FX signals:** Geopolitical pressure on a currency can take 12–18 months to materialize if the central bank is actively defending the peg or if capital flows from external support (e.g., Gulf sovereign wealth fund deposits) are offsetting the structural pressure. The signal is not wrong — the timing is uncertain. **This is the fundamental challenge of long-horizon geopolitical investing: being right directionally but wrong on timing is economically equivalent to being wrong if you can't finance the carry.**

**Signal Type C — Defense/Industrial Policy Equity Tilt (April 2026 vintage)**
Sector tilt signals toward European defense and industrial policy beneficiaries, generated in the context of NATO spending ramp-up and near-shoring policy acceleration. At 4+ months mark-to-market, this has been the strongest performer directionally. European defense sector equity appreciation has been consistent with the thesis. **Thesis intact. Not yet scored (12-month horizon), but interim read is positive.**

**Signal Type D — Post-Crisis Stabilization Short (June 2026 vintage)**
A stabilization-regime signal suggesting that certain safe-haven premiums (gold, CHF) would compress as acute crisis signals faded. This is the one signal where the thesis has most clearly failed the interim read — gold has continued to appreciate despite moderating acute geopolitical stress. **Potential framework gap: the CPM may be underweighting structural safe-haven demand driven by central bank accumulation, which is not captured in the GDELT event signal.**

---

## IV. The Most Important Lessons From 4 Months of Signals

### Lesson 1: Timing Uncertainty Is the Framework's Biggest Limitation

The GRI correctly identifies *which* assets will be affected by geopolitical pressure. It is less reliable at predicting *when* that pressure materializes in price. This is not a fatal flaw — it is inherent to any geopolitical signal, including those from Eurasia Group and Bridgewater. The correct response is not shorter horizons but wider confidence intervals and explicit acknowledgment of the timing uncertainty in every signal card.

**Action:** Add a `timing_confidence` field to the ISG output (High/Medium/Low) and a `timing_drivers` note explaining what would cause the signal to materialize faster or slower than the base case.

### Lesson 2: The Invalidation Condition Is the Most Valuable Part of the Signal

Four months in, the invalidation conditions have proven to be the most intellectually disciplined part of the framework. When the invalidation condition for a signal is met, the temptation is to rationalize. The discipline of a pre-committed invalidation condition removes that temptation.

**Example:** An EM currency short signal had the invalidation condition "if the central bank receives bilateral swap line support from a major power." If that condition were met, the signal should be closed at a loss without rationalization. This is the hardest part of systematic investing — and it's what separates a framework from an opinion.

**Action:** Begin tracking "invalidation events" separately in the track record database — how often are signals closed due to invalidation vs. reaching target date? A framework with clean invalidation discipline is more credible than one with a higher hit rate that never acknowledges when it's wrong.

### Lesson 3: The Gold Signal (Type D) Reveals a Structural Blind Spot

The framework currently captures geopolitical event signals (GDELT) and macro regime indicators (FRED). It does not capture structural flows — specifically, central bank gold accumulation as a geopolitical balance-sheet strategy (a topic covered in Lessons 65–66 on gold geopolitics and petrodollar architecture).

**The gap:** Central bank gold buying by BRICS-aligned central banks is a structural, multi-year demand driver that does not appear as a high-frequency GDELT event. It is structural, not episodic. The CPM is built to capture episodic supply disruption risk — not structural demand shifts.

**Year 2 pipeline addition:** Integrate World Gold Council central bank demand data (quarterly) and IMF COFER data (currency composition of reserves) as structural signal layers in the CPM. These are slow-moving but directionally powerful signals that complement the high-frequency GDELT event feed.

### Lesson 4: The Framework Works Best at the Regime Transition Moment

Examining signal timing relative to the GRI regime cycle, the highest-conviction signals are generated at the moment of regime transition — when the RCD detects a shift from stabilization to escalation (or vice versa). These transition signals capture the most significant mispricings because the market has been pricing the prior regime and has not yet updated.

**This confirms the core investment thesis:** The edge is not reacting faster than other market participants to a single event. The edge is detecting the regime transition *before* the consensus reprices, and sizing into a position with a long enough horizon to survive the repricing process.

---

## V. The Commercial Track Record Package: What to Publish and When

Given the 4-month evidence base, what should the first commercial track record package contain?

### What to Include Now

1. **Framework description** — GRI methodology, CPM architecture, ISG signal generation logic. Transparent, reproducible, auditable.
2. **Signal log summary** — 14 signals, asset class distribution, regime distribution. No cherry-picking.
3. **Interim performance narrative** — honest assessment of signals at 4 months. Strong directional alignment on energy/defense longs. Mixed EM FX timing. One identified blind spot (structural gold demand).
4. **Framework improvements triggered by observations** — the fact that the framework is learning from its own track record is itself a signal of quality.

### What to Wait On

1. **Outcome scoring statistics** — wait for the first closed signals at 6-month horizon (November 2026). That is the first time we'll have actual scored outcomes.
2. **Hit rate and mean return claims** — not credible until 6+ signals are scored.
3. **Formal Sharpe ratio or risk-adjusted return** — 18 months minimum.

### The CEO's Target: December 2026

By December 2026, the first credible commercial track record package will exist:
- 6+ signals scored at their 6-month target date
- 12+ months of GRI weekly signal output
- Outcome Scorer running, producing hit rate and mean directional return
- Two framework improvements documented with evidence

**This is the earliest defensible moment to approach a prospective pilot customer.** Not before. Not "almost there." December 2026.

---

## Investment Implications

### The Meta-Lesson for Portfolio Construction

The experience of running a signal framework for 4 months produces a lesson every geopolitical investor learns eventually: **information advantage is not sufficient. Patience capital is the scarce resource.**

The signals are directionally correct on the assets where geopolitical pressure is most structural. The timing uncertainty is real. A portfolio built on 12–18 month geopolitical themes needs financing — either low-cost capital, options structures that cap drawdown during the "right but early" period, or explicit position sizing that assumes 12–18 months of potential mark-to-market pain before the thesis plays out.

**Practical implication:** When building a geopolitical portfolio position, size it at 50% of full conviction at entry, with a pre-committed protocol to add the remaining 50% if the thesis strengthens (GRI escalation continues, invalidation conditions not triggered) at the 6-month mark. Do not size to full conviction on day one — the timing uncertainty is real and will test your discipline.

---

## Databricks Angle

### Immediate Build Task: Signal Performance Dashboard

The Outcome Scorer (specified in Lesson 304) needs a companion visualization layer in Databricks AI/BI.

**Notebook: `signal_performance_review`**

```python
# Signal Performance Review — Databricks Notebook
from pyspark.sql import functions as F

# Load track record and outcome tables
signals = spark.table("prospectra.gold.investment_signals")
outcomes = spark.table("prospectra.gold.signal_outcomes")

# Join for full picture
full_record = signals.join(outcomes, on="signal_id", how="left")

# Key metrics
total_signals = full_record.count()
scored_signals = full_record.filter(F.col("outcome_score").isNotNull()).count()
correct_signals = full_record.filter(F.col("outcome_score") == "CORRECT").count()

hit_rate = correct_signals / scored_signals if scored_signals > 0 else None

# By asset class breakdown
by_asset = (full_record
    .groupBy("asset_class")
    .agg(
        F.count("signal_id").alias("total"),
        F.sum(F.when(F.col("outcome_score") == "CORRECT", 1).otherwise(0)).alias("correct"),
        F.avg("return_pct").alias("avg_return_pct")
    )
)

by_asset.display()

# By regime type
by_regime = (full_record
    .groupBy("regime_at_signal_date")
    .agg(
        F.count("signal_id").alias("total"),
        F.avg(F.when(F.col("outcome_score") == "CORRECT", 1.0).otherwise(0.0)).alias("hit_rate"),
        F.avg("return_pct").alias("avg_return_pct")
    )
)

by_regime.display()
```

**New table to create: `prospectra.gold.signal_performance_summary`**

| Column | Description |
|---|---|
| `review_date` | Date of this performance snapshot |
| `total_signals` | All signals ever generated |
| `scored_signals` | Signals with outcome score |
| `hit_rate` | % directionally correct (scored only) |
| `avg_return_pct` | Mean return on scored signals |
| `open_signals` | Signals without outcome score yet |
| `invalidation_events` | Signals closed due to invalidation condition |

**Schedule:** Run weekly, every Sunday at 08:00 UTC. Output: one row per week appended to the summary table. The trajectory of hit_rate over time is itself the most important signal of framework quality.

---

## Key Concepts Covered

1. **Signal performance evaluation framework** — what can and cannot be measured at 4 months
2. **Directional accuracy vs. timing accuracy** — the fundamental challenge of long-horizon geopolitical investing
3. **The invalidation condition as intellectual discipline** — separating framework from opinion
4. **Structural vs. episodic signals** — the gold/central bank demand blind spot reveals a CPM architecture gap
5. **Commercial track record packaging** — what to publish now vs. what to wait for

---

## Reflection Questions

1. **The timing problem:** A prospective customer asks "your signals have been directionally right, but they haven't scored yet — why should I trust them?" How do you answer that without overpromising or underselling? What is the honest, intellectually credible response?

2. **The blind spot lesson:** The framework missed the structural gold demand signal because GDELT captures episodic events, not persistent flows. What other structural, slow-moving geopolitical forces might the current pipeline systematically miss? (Think: demographics, institutional reserve diversification, long-term energy transition capital allocation.) How would you add these to the CPM without diluting the signal quality of the high-frequency event feed?

3. **The invalidation discipline:** If one of your 14 signals hits its invalidation condition in the next 30 days — meaning you have to close it at a loss — how does that change the commercial track record presentation? Is it better or worse for your credibility to show a disciplined loss vs. holding the position and hoping?

---

## Questions for Next Session (Spaced Repetition Hook)

- Have you run the Signal Performance Review notebook in Databricks? What does the actual data show when it queries `prospectra.gold.investment_signals`?
- Which of the 14 signals is closest to its invalidation condition today — and what is the condition?
- The CPM blind spot (structural gold demand). What three data sources would you add to capture persistent structural geopolitical flows rather than episodic events?

---

## Databricks Relevance Note

**Immediate pipeline tasks:**
1. Run the Outcome Scorer from Lesson 304 — score any signals that have reached target date
2. Build the `signal_performance_review` notebook above
3. Create `prospectra.gold.signal_performance_summary` as a scheduled weekly table
4. Add `timing_confidence` and `timing_drivers` fields to the ISG output schema

**New data source to integrate (Year 2 Priority):**
- World Gold Council Central Bank Statistics (quarterly) → structural demand signal for CPM
- IMF COFER (Currency Composition of Official Foreign Exchange Reserves) → reserve diversification signal
- BIS International Banking Statistics → capital flow regime signal (complements FRED)

**Feature to engineer:**
- `structural_flow_score` per country: composite of (gold reserve growth rate + COFER non-USD share trend + BIS cross-border lending change) — a slow-moving but directionally powerful complement to the high-frequency GDELT event feed. Update quarterly.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 306 | September 6, 2026 | Year 2 Launch Module*
