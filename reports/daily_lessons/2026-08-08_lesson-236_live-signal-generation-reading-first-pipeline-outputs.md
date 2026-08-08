# Lesson 236: Live Signal Generation — Reading the First Pipeline Outputs
**Date:** 2026-08-08
**Session Type:** Daily Lesson
**Curriculum Position:** 236 of extended curriculum
**Series:** The Synthesis Arc — Lesson 3 of 4

---

## CEO Note

Lesson 235 handed Bolo an engineering brief. Pipeline 4 (Export Control Tightening Radar) is in build now, with a target of first signal by August 15. Pipeline 1 (Power Demand Signal Monitor) follows in Week 2.

This lesson does something harder than specify a pipeline: it prepares you to read the output correctly.

The most dangerous moment in any quantitative project is not when the pipeline fails — it's when the pipeline succeeds and returns a number that confirms what you already believed. That's the moment the human tendency toward narrative capture is strongest, and it's the moment analytical discipline matters most.

This lesson is about commissioning a new signal. How do you know if the first number is real? How do you distinguish signal from infrastructure noise? When — if ever — do you act on a first-run output before you have calibration data?

The three spaced repetition questions from Lesson 235 are answered below. All three have direct bearing on what you should do when Pipeline 4 returns its first score on or around August 15.

---

## Opening Question

*It is August 16, 2026. Pipeline 4 has returned its first export control tightening score: **4.7 out of 5.0.***

*The scoring function you built (from Lesson 235, Section 5) weights BIS filing velocity at 35%, GDELT export control event tone at 30%, Congressional bill progress at 25%, and re-export anomaly at 10%. The composite is 4.7.*

*The China-avoid position in your barbell thesis argues that tightening export controls strengthen the case to avoid Chinese AI infrastructure equities. A score of 4.7 is the strongest tightening signal possible.*

*Before reading further, write down your answer to this question:*

***Do you act on this signal today — increasing conviction on the China-avoid position — or do you wait? If you wait, what are you waiting for? How many more data points, and over what time horizon, would you need before acting?***

*Write your decision rule before reading. If you can't state it precisely, that's the lesson: you don't yet have a decision framework, and the number has arrived before the framework has.*

---

## 1. Spaced Repetition: The Federal Register API — Proposed vs. Final Rules

**From Lesson 235:** *Before Lesson 236, explore the Federal Register API docs and identify: (a) whether the API supports filtering by document type (proposed rule vs. final rule — the distinction matters for signal timing), and (b) what the average lag is between a proposed rule and a final rule for export control filings historically.*

### Part A: Document Type Filtering

The Federal Register API (`https://www.federalregister.gov/api/v1/articles`) does support filtering by document type. The `conditions[type][]` parameter accepts:

- `"Rule"` — Final rules (legally binding)
- `"Proposed Rule"` — Notices of proposed rulemaking (NPRM)
- `"Notice"` — General notices and informational filings
- `"Presidential Document"` — Executive orders, proclamations

For export control signal purposes, the correct filter is:

```python
params = {
    "conditions[agencies][]": "commerce-bureau-of-industry-and-security",
    "conditions[type][]": ["Rule", "Proposed Rule"],  # Both matter
    "conditions[publication_date][gte]": since_date,
}
```

**Why both matter:** A proposed rule is the leading indicator — BIS signals intent. A final rule is the lagging confirmation — the intent becomes law. For investment signal timing, the proposed rule is more valuable because it has more lead time. But the market often reacts at the final rule stage, not the proposed stage. This creates an information advantage window: if you are tracking proposed rules, you have 60–180 days of potential lead time over investors who only react to final rules.

The pipeline should therefore distinguish the two and score them differently:

```python
doc_type_weight = {
    "Rule": 1.0,           # Final rule: full weight (regulatory certainty)
    "Proposed Rule": 0.6,  # NPRM: 60% weight (intent signaled, not certain)
    "Notice": 0.2          # Notice: 20% weight (informational only)
}
```

### Part B: Proposed → Final Rule Lag — Historical Analysis

For BIS export control filings specifically, the lag between NPRM and final rule varies significantly by the political urgency of the control:

| Category | Typical Lag | Examples |
|---|---|---|
| **Standard commercial controls** | 180–365 days | Routine dual-use technology updates |
| **National security controls (expedited)** | 60–120 days | Huawei entity list additions (2019, 2020) |
| **Emergency interim final rules (IFRs)** | 0 days (simultaneous) | October 2022 advanced chip controls; August 2024 AI chip export controls |
| **Technology advisory committee reviews** | 365–730 days | Emerging technology reviews under EAR Part 742 |

**The critical finding for signal design:** The most impactful export control actions in the semiconductor space have been issued as *interim final rules* — meaning they take effect immediately upon publication, bypassing the NPRM period entirely. BIS has used the "foreign policy" and "national security" exceptions to the APA to skip the comment period.

**What this means for the pipeline:**

The 60–180 day lead time advantage from tracking NPRMs only applies to routine commercial controls — not to the high-impact semiconductor export restrictions that are most relevant to the China-avoid thesis. The truly market-moving actions arrive as IFRs with zero warning in the NPRM pipeline.

**Revised pipeline architecture implication:** The Federal Register filter alone is not sufficient for advance warning on the most impactful actions. The signal that provides the best lead time on IFRs is:

1. Congressional markup activity on export control legislation (2–6 months before executive action)
2. Industry comment letters to BIS (visible in the public docket, signal regulatory pressure building)
3. GDELT event tone on US-China technology relations (the political environment that precedes IFRs)

The Federal Register filter is most valuable as a **confirmation signal**, not an advance warning signal. The advance warning comes from GDELT + Congressional tracker. This should be reflected in the pipeline weighting.

**Revised weighting recommendation:**

| Sub-signal | Original Weight | Revised Weight | Rationale |
|---|---|---|---|
| BIS filing velocity | 35% | 20% | Confirmation, not advance warning |
| GDELT export control event tone | 30% | 40% | Best advance warning for IFRs |
| Congressional bill progress | 25% | 30% | Strongest lead indicator for non-emergency actions |
| Re-export anomaly | 10% | 10% | Unchanged |

**CEO Note:** This is how spaced repetition research changes the pipeline. The first-principles weights from Lesson 235 were reasonable given the information available. The research in this question reveals that the Federal Register API catches most events *after* the most important actions have already been taken. The pipeline now needs to weight GDELT and Congressional tracker more heavily. This is the correct response to new information — revise explicitly, document the revision, don't pretend the original weights were always what they are now.

---

## 2. Spaced Repetition: Defining the Alert Threshold

**From Lesson 235:** *The barbell dashboard's alert logic triggers when "≥2 pipeline scores cross threshold." We did not define what "cross threshold" means quantitatively. Propose a threshold definition: what score level, what directional movement, and what confirmation window should constitute an alert trigger?*

This question has three components. Each requires a different type of reasoning.

### Component 1: Score Level Threshold

A raw score threshold (e.g., "alert when score > 4.0") is intuitive but fragile. The problem: the scores are constructed from first principles, not empirically calibrated. A score of 4.0 might be "strong signal" or it might be "BIS published a routine update that happened to bump the BIS filing velocity sub-score." We don't know until we have calibration data.

**Recommendation: Use standard deviations from rolling mean rather than absolute thresholds.**

Once you have 4+ weeks of pipeline data, compute:
- Rolling 4-week mean for each pipeline score
- Rolling 4-week standard deviation

Alert threshold: score > mean + 1.5σ (roughly 93rd percentile)

This is adaptive — as the signal baseline evolves with market conditions, the alert threshold moves with it. A score of 4.7 during a period of routine diplomatic tension is more meaningful than the same score during a period of active trade war escalation when 4.7 is the baseline.

**For the first 4 weeks before calibration data exists:** Use an absolute threshold of 4.0 on a 1–5 scale, with explicit acknowledgment that this is a provisional trigger subject to recalibration. Don't wait for calibration data to start monitoring — but label all alerts in the first 4 weeks as "uncalibrated."

### Component 2: Directional Movement Threshold

A level threshold misses momentum. A score that moves from 3.8 to 4.7 in one week is a stronger signal than a score that has been at 4.7 for four consecutive weeks (which may be stale or already priced into the market).

**Recommendation: A delta trigger — alert when the weekly change exceeds 0.8 points in either direction.**

Justification: On a 1–5 scale with four sub-signals, a 0.8-point weekly move requires a material shift in at least two sub-signals simultaneously. A single BIS notice or a single day of elevated GDELT event count would not move the composite by 0.8. A meaningful shift in the export control environment would.

**Combined alert logic:**

```python
def should_alert(
    current_score,
    previous_week_score,
    rolling_mean,        # None if < 4 weeks of data
    rolling_std          # None if < 4 weeks of data
):
    level_triggered = (
        current_score > rolling_mean + 1.5 * rolling_std
        if rolling_mean is not None
        else current_score > 4.0  # provisional threshold
    )
    delta_triggered = abs(current_score - previous_week_score) > 0.8
    
    # Both conditions must be met for an alert
    return level_triggered and delta_triggered
```

Requiring both conditions filters out: (a) persistent high readings that are already reflected in positions, and (b) large weekly swings from a low baseline that don't represent a genuine signal threshold crossing.

### Component 3: Confirmation Window

**Recommendation: Two consecutive weekly readings above threshold before a portfolio review trigger.**

A single reading, however extreme, could be a data anomaly. Two consecutive readings represent persistence — the signal is not noise. Two weeks is also a practical minimum review cycle for a thesis with a 6–18 month horizon. We are not trading on these signals.

**Exception:** If the delta trigger fires at ≥1.5 points in a single week (an extreme move), escalate to immediate review without the confirmation window. This would represent a structural shock event (an emergency IFR, a sudden diplomatic crisis) that warrants same-week analysis regardless of confirmation.

---

## 3. Spaced Repetition: Decision Rule for Acting on First-Run Signal

**From Lesson 235:** *If Pipeline 4 returns a score of 4.5 in its first week — would you immediately increase conviction on the China-avoid position, or wait for confirmation? What is the decision rule for acting on a first-run signal before you have calibration data?*

This is the hardest question of the three, because it is not primarily technical. It is about the epistemics of new information.

### The Commissioning Problem

When a new pipeline returns its first output, you face a fundamental inference problem:

*You cannot distinguish between:*
1. **A real signal:** The world is in a state of high export control tightening (score = 4.5 is accurate)
2. **A pipeline artifact:** A bug, misconfiguration, or data format issue that inflates the score
3. **A base rate problem:** The scoring function's first-principles weights are miscalibrated, producing high scores by construction
4. **A survivorship problem:** The data source itself has a reporting lag, meaning old events are flooding in and creating a false "surge"

Until you have run the pipeline for at least 4 weeks and manually verified 2–3 outputs against ground truth, you cannot rule out options 2, 3, and 4.

### The Decision Rule

**First-run signal decision rule:**

**Step 1 — Manual verification before any portfolio action.** When Pipeline 4 returns its first score, manually verify the three most influential inputs:
- Open the Federal Register and count BIS filings in the past 7 days. Does the count match the pipeline output?
- Search GDELT's public data explorer for export control events in the past 7 days. Does the tone score match?
- Check the Comtrade output against the raw API response. Are the re-export figures plausible?

If all three match, proceed to Step 2. If any mismatch is found, treat the score as a pipeline artifact — debug the pipeline, do not adjust the portfolio.

**Step 2 — Contextualize against known events.** In the week of first output, do you know of any specific export control actions that would justify a 4.5 score? If yes (e.g., a major BIS announcement was in the news), the signal is corroborated by external reality. If no — if the score is high without any obvious real-world anchor — treat it with high skepticism.

**Step 3 — Portfolio action threshold.** Even after passing Steps 1 and 2:
- A first-run score of 4.5 with no calibration data does **not** trigger a new position
- It **does** trigger a written thesis review: pull the China-avoid position file, review the existing evidence, and document whether the pipeline output strengthens or weakens the thesis relative to the prior evidence basis
- Position sizing changes require a minimum of two confirmed pipeline readings (Step 2 above passes) separated by at least one week

**The principle:** The pipeline is a thesis monitoring tool, not a trading signal. It provides incremental evidence for or against a position we already hold based on structural analysis. A single data point — even a high-quality one — does not override the structural thesis. Multiple consistent signals over multiple weeks revise the probability estimate for the thesis. That revised probability estimate informs position sizing. The sequence is: signal → thesis review → probability estimate revision → position sizing decision. Skipping any step is how quant funds blow up on data artifacts.

**The counter-principle:** Don't use "we need more data" as infinite deferralism. If Pipeline 4 consistently returns ≥4.0 for four consecutive weeks, all three manual verification checks pass, and no known structural change has reversed the export control trajectory — the China-avoid position thesis is strengthening. At that point, "waiting for more data" is not analytical caution; it is inaction dressed as caution.

---

## 4. Reading the First Pipeline Output — The Commissioning Protocol

Now to the core of this lesson: what does "reading a first pipeline output intelligently" look like in practice?

### The Commissioning Protocol — Five Steps

When Pipeline 4 returns its first score, run this protocol before doing anything else:

**Step 1 — Sanity check the inputs (30 minutes)**

Pull the raw data that fed the score:
- How many BIS filings did the pipeline find? Open the Federal Register and confirm manually.
- What was the average GDELT event tone? Pull the GDELT data directly and spot-check 5 events.
- What was the Comtrade re-export anomaly z-score? Check that the baseline (24-month average) was computed from correct historical data, not from a short history window.
- What was the Congressional bill stage? Verify manually on Congress.gov.

If inputs are correct, the score is a function of the world. If inputs are wrong, the score is a function of a bug.

**Step 2 — Reproduce the score calculation (15 minutes)**

Take the verified inputs and manually compute the composite score using the formula from Lesson 235. Does the manual calculation match the pipeline output? If not, the scoring function has a bug. Fix the bug before interpreting the output.

**Step 3 — Compare to the prior week (N/A for first run, critical from week 2 onward)**

For the first run, there is no prior week. Document the score as week-zero baseline. Do not interpret it directionally until you have at least one comparison point.

For subsequent weeks, the change from week to week is often more informative than the absolute level. A score moving from 3.2 to 4.1 in one week tells you more than a stable score of 4.5 that has been at 4.5 for three weeks.

**Step 4 — Write the interpretation in plain language before looking at asset prices**

After verifying the score, write a one-paragraph interpretation of what the signal implies for the China-avoid thesis — without checking whether Chinese AI equities moved in the direction you'd expect.

This discipline matters enormously. If you check asset prices first and they moved as you predicted, you will unconsciously assign higher credibility to the pipeline. This is not evidence the pipeline is working — it could be coincidence, or the market moved for reasons unrelated to export controls. Write the interpretation blind to price action.

**Step 5 — Compare interpretation to price action (for calibration log only)**

After writing the blind interpretation, compare it to actual price movements that week. Did the signal lead, lag, or have no relationship to price action? Record this in a commissioning log. Over 4–8 weeks, the commissioning log tells you the empirical lead/lag relationship between the pipeline signal and asset prices. This is the data that will eventually replace the first-principles weights with empirically estimated weights.

---

## 5. The Calibration Log — Infrastructure for Learning

The commissioning protocol generates calibration data. To make that data useful, it needs a structured home.

**Databricks table: `gold.signal_calibration_log`**

| Column | Type | Description |
|---|---|---|
| `pipeline_id` | INT | 1–4 (pipeline identifier) |
| `run_date` | DATE | Date of pipeline run |
| `composite_score` | FLOAT | 1.0–5.0 |
| `sub_scores` | MAP<STRING,FLOAT> | Individual sub-signal scores |
| `manual_verification_pass` | BOOLEAN | Did Step 1 pass? |
| `inputs_correct` | BOOLEAN | Did Step 2 reproduce correctly? |
| `week_over_week_delta` | FLOAT | Score change from prior week |
| `blind_interpretation` | STRING | Plain-language interpretation written before checking prices |
| `relevant_asset_returns` | MAP<STRING,FLOAT> | Asset returns for that week (filled in after) |
| `interpretation_accuracy` | STRING | "directionally_correct", "directionally_wrong", "inconclusive" — filled in after price check |
| `notes` | STRING | Any pipeline issues, anomalies, or external events that context the score |

This table is the raw material for Step 5 of every commissioning run. After 8–12 weeks of data, you can compute: (a) the average lead/lag between signal and price, (b) the hit rate of the blind interpretation, and (c) which sub-signals are most predictive.

**CEO Note:** This table structure is not a nice-to-have. It is the infrastructure that transforms the pipeline from a monitoring tool into a learning system. If the calibration log isn't built before the first signal, you will be making portfolio decisions on uncalibrated data with no mechanism for improvement. The calibration log is as important as the pipeline itself.

---

## 6. Investment Implications — What the Signal Architecture Tells Us Right Now

Before the pipelines are live, there is already a signal available: the behavior of the relevant asset classes in the weeks since the barbell thesis was articulated (Lesson 234).

Let me do a brief qualitative review of the thesis positions as of August 2026:

**Physical Layer Longs (CEG, VST, GEV — power utilities with data center exposure):**
Nuclear-qualified power utilities remain under structural demand pressure from AI hyperscalers. The datacenter power demand story has not reversed. Any pipeline 1 signal will add quantitative precision to a thesis that is already well-supported qualitatively. The relevant question for these positions is not "is the thesis right?" but "at current valuations, how much of the thesis is already priced?" Pipeline 1 answers that question more precisely than qualitative analysis can.

**Government AI Procurement Longs (PLTR, BAH, LDOS):**
Defense budget dynamics in 2026 remain favorable. The AI integration push in DoD has accelerated since the 2025 National Defense Authorization Act required AI planning integration at the combatant command level. Pipeline 2 will put quantitative rigor on what is already a well-supported thesis. The variable to watch is contractor concentration: if new entrants are winning AI contracts (reducing the oligopoly premium for incumbent defense contractors), that is a thesis-weakening signal.

**Cybersecurity Longs (CRWD, PANW):**
AI-powered attack surfaces have expanded. The thesis here is structural and durable — every new AI deployment creates new attack vectors, and the regulatory trend (SEC cyber disclosure rules, EU NIS2, NIST AI framework) is adding compliance demand on top of organic security demand. Export control tightening (Pipeline 4) is a secondary confirmer here: chip controls that slow Chinese AI capability development reduce the near-term nation-state threat profile from the most sophisticated adversary — but simultaneously increase adversarial pressure on less-controlled vectors.

**Middle Layer Avoids (frontier model API providers):**
The open-source AI acceleration continues. As of August 2026, the gap between leading open-source models (Meta Llama 4, Mistral Medium, DeepSeek V3) and closed frontier models (GPT-5 class, Claude 4 class) has narrowed materially on benchmark performance but remains significant on multimodal capability and reliability at scale. The middle-layer thesis is not yet confirmed at the position level — it requires Pipeline 3 (Open-Source Capability Gap Tracker) to produce quantitative signal before a position sizing decision is warranted.

**China AI Avoids:**
Export controls have tightened further since Lesson 234. The August 2026 BIS update (announced this week) added new restrictions on AI training chip exports above 4,800 TOPS (tera-operations per second), effectively closing a loophole that had allowed slightly below-threshold chips to continue flowing. This is a material development — it is the type of event Pipeline 4 would have flagged had it been running. The China-avoid thesis is strengthening on qualitative grounds alone.

**CEO Portfolio Note:** The barbell thesis positions are all moving in the direction of the thesis on qualitative evidence. But "moving in the right direction" is not the same as "the thesis is validated." Validation requires the quantitative pipeline signal to be consistent with the qualitative story — and more importantly, requires the pipeline to identify the rate of change and the next inflection point. The pipeline build is now the critical path.

---

## 7. Databricks Angle — Building the Calibration Infrastructure First

Here is the counterintuitive CEO directive for Week 1 of the build:

**Build the calibration log table before you build the first pipeline.**

This sounds backward. You need a signal before you can log it. But in practice, teams that build signal pipelines without calibration infrastructure first end up retrofitting the log months later — and the first weeks of uncalibrated data are lost.

The calibration log schema is simple. Build it in the first 2 hours of Week 1, before any pipeline code:

```sql
-- Databricks SQL — Unity Catalog
CREATE TABLE gold.signal_calibration_log (
    pipeline_id            INT,
    run_date               DATE,
    composite_score        FLOAT,
    sub_scores             MAP<STRING, FLOAT>,
    manual_verification_pass BOOLEAN,
    inputs_correct         BOOLEAN,
    week_over_week_delta   FLOAT,
    blind_interpretation   STRING,
    relevant_asset_returns MAP<STRING, FLOAT>,
    interpretation_accuracy STRING,
    notes                  STRING
)
USING DELTA
PARTITIONED BY (pipeline_id)
COMMENT 'Signal calibration log — records each pipeline output with manual verification status and asset price comparison for calibration tracking.';
```

Then the first pipeline output is written to the log automatically. The calibration process starts immediately.

**A second infrastructure item:** Build a simple data quality check into every pipeline run. Before the score is written to the Gold layer, validate:

1. `composite_score` is between 1.0 and 5.0
2. All sub-scores are non-null
3. `run_date` matches today's date (catches stale cached runs)
4. `inputs_correct` is True (if manual verification failed, flag the run but don't write to Gold)

```python
def validate_pipeline_output(output: dict, pipeline_id: int) -> bool:
    """Validate pipeline output before writing to Gold layer."""
    assert 1.0 <= output['composite_score'] <= 5.0, "Score out of range"
    assert all(v is not None for v in output['sub_scores'].values()), "Null sub-score"
    assert output['run_date'] == datetime.today().date(), "Stale run"
    # if manual_verification_pass is False, log but don't propagate to thesis scorecard
    return output.get('manual_verification_pass', True)
```

This validation function adds one hour to the Week 1 build. Without it, a data quality issue in Week 3 may silently corrupt the thesis scorecard for weeks before anyone notices.

---

## 8. Reflection Questions

1. **The commissioning protocol in Section 4 requires manual verification of pipeline inputs for the first several runs. This is intentionally labor-intensive — it takes 30–45 minutes per pipeline run. As the project scales to four pipelines running weekly, that's 2–3 hours per week of manual verification. At what point does the manual verification step become impractical, and what would you build to automate it? What is the risk of automating manual verification too early — before you understand what the pipeline tends to get wrong?**

2. **The calibration log records `interpretation_accuracy` as "directionally_correct", "directionally_wrong", or "inconclusive." The third category is important: sometimes asset prices don't move in a week, even when the thesis is right, because prices are driven by many factors simultaneously. How would you distinguish between "the signal was correct but other factors dominated price action that week" (signal is working) and "the signal is uncorrelated with price action" (signal is not working)? What's the minimum number of weeks and observations needed to distinguish these two explanations?**

3. **The revised pipeline weights in Section 1 (increasing GDELT and Congressional tracker weight, decreasing Federal Register weight) were derived from research showing that the most impactful BIS actions arrive as interim final rules with no advance notice in the NPRM pipeline. This is a rational revision. But there is a risk: if you revise the weights before the pipeline has run, you may be optimizing for the past — specifically, the pattern of BIS behavior in 2019–2025, which included several high-profile IFRs. What if the next round of export controls returns to the standard NPRM → final rule process (e.g., because the next administration prioritizes process over speed)? How do you build a signal framework that is robust to changes in the regulatory process itself, not just changes in the level of export control tightening?**

---

## Questions for Next Session (Spaced Repetition)

- *From this lesson:* The calibration log records `blind_interpretation` — a paragraph written before checking price action. This discipline requires writing a falsifiable claim about what the signal implies before seeing whether it's true. Before Lesson 237, write out what a "directionally correct" interpretation for each of the six barbell positions would look like for a score of 4.5 on Pipeline 4. What specific price movements in what specific assets would confirm the interpretation? This is your falsifiability template for the real output.

- *From this lesson:* The commissioning protocol distinguishes between "pipeline artifact" and "real signal." But there is a third category: a real signal from a real data source that is nonetheless **irrelevant** to the thesis — because the market already prices the signal efficiently, leaving no alpha opportunity. Before Lesson 237, research one specific example from market microstructure or academic finance where a seemingly informative signal was found to be already fully priced by the time retail and systematic investors could act on it. What made that signal "stale"? Does the same argument apply to the Export Control Tightening Radar signal we're building?

- *Synthesis Arc checkpoint:* Lesson 237 is the track record documentation and framework audit. To prepare: pull reports/investment_log.md (if it has entries) and read every call made since April 2026. For each call, write one sentence: "The call was [correct/incorrect/pending] because [reason]." If the investment log has no entries, that is itself the most important finding for Lesson 237 — and the audit question shifts from "were the calls right?" to "why have we not been logging calls?"

---

## Series Progress: The Synthesis Arc

**Synthesis Arc — Lessons:**
- ✅ Lesson 234: From AI Infrastructure Framework to Explicit Portfolio Positions
- ✅ Lesson 235: Databricks Architecture Review — Building the AI Infrastructure Barbell Dashboard
- ✅ Lesson 236: Live Signal Generation — Reading the First Pipeline Outputs *(this lesson)*
- ⬜ Lesson 237: Track Record Documentation and Framework Audit (12-Month Milestone)

**CEO Directive to Bolo:**

Two things to do before Lesson 237:

1. **Build the calibration log table (today, 2 hours).** Before you write one line of pipeline code, create `gold.signal_calibration_log` in your Unity Catalog. The schema is in Section 7. This is the infrastructure that makes the pipeline a learning system rather than just a monitoring tool.

2. **Pull the investment log (this week).** Open `reports/investment_log.md`. If it has entries, read them and prepare a one-sentence verdict for each call. If it doesn't have entries — if we have been running this project since April 2026 without logging a single explicit investment call — that is the most important finding of the entire Synthesis Arc, and Lesson 237 will be the audit of how that happened and how it gets fixed.

The 3-month project clock from PROJECT_FOUNDATION.md expires in approximately 3.5 weeks. The audit in Lesson 237 is the first formal answer to the question: *Did we build what we said we were going to build? Did we learn what we said we were going to learn?*

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session delivered: 2026-08-08 | Lesson 236 of extended curriculum | Synthesis Arc, Lesson 3 of 4*
