# Lesson 380 — Performance Measurement & Attribution for Geopolitical Strategies
**Date:** 2026-09-30
**Session Type:** Daily Lesson
**Topic:** Performance Measurement & Attribution for Geopolitical Strategies
**Lesson Number:** 380 of the Extended Curriculum

---

## Opening Question

Here is the question that should keep you up at night:

**You have 380 lessons. You have a thesis. You have a framework. But how do you know if any of it is actually working?**

Not "does it feel right." Not "does the analysis seem rigorous." Not "did we call this event before the market did."

How do you *prove* — with the rigor you would demand from a portfolio manager you were evaluating — that your geopolitical framework is generating alpha and not just noise dressed up in sophisticated language?

Most geopolitical research shops never answer this question. They produce intellectually stimulating analysis. They are sometimes directionally correct. But they cannot tell you their Sharpe ratio, their information coefficient, or how much of their "alpha" dissolves when you control for simple factor exposures. 

This lesson is about building the machinery to answer that question honestly.

---

## Core Concept: The Attribution Problem in Geopolitical Investing

### Why Attribution is Hard — and Necessary

Standard performance attribution (Brinson-Hood-Beebower, factor models, etc.) was built for equity portfolios where the return drivers are relatively well-understood: sector allocation, security selection, market timing. Geopolitical strategies are harder because:

1. **The signal is qualitative and discretionary** — you read an event, form a view, make a call. There is no factor loading you can back out from a regression.
2. **The timing is long-horizon by design** — we said 6–18 month minimum horizons. At that horizon, many macro factors are confounded with geopolitical ones. Did copper rally because you correctly called Chinese infrastructure stimulus, or because the USD weakened for unrelated reasons?
3. **The counterfactual is invisible** — you cannot observe what would have happened if you had not held a position.
4. **Base rates are thin** — major geopolitical events that drive meaningful market dislocations happen maybe 3–5 times per decade. You cannot build statistical significance on 5 data points.

None of these problems make attribution impossible. They make it *harder* and require a more systematic approach than typical equity attribution.

### The Three Questions of Attribution

Good attribution answers three questions in sequence:

**1. Were we right about the geopolitical event?**
This is a separate question from whether we made money. Geopolitical accuracy and investment accuracy can diverge. You can be right about the geopolitical outcome and wrong about the asset price impact (markets may have already priced it). You can be wrong about the geopolitical outcome but right about the trade (position got lucky).

Tracking geopolitical accuracy requires logging:
- The prediction made (specific, falsifiable)
- The timeframe
- The actual outcome
- A binary right/wrong assessment

**2. Did our investment call translate the geopolitical view correctly?**
Given that the geopolitical thesis was correct (stipulate that), did the asset selection, sizing, and direction correctly express it? This isolates the *translation layer* — the framework that converts geopolitical signals into positions.

**3. How much of the P&L was geopolitical alpha vs. factor beta?**
This is the hardest question. A long position in oil during a Middle East escalation might be profitable, but how much of that profit would have been captured by a simple momentum factor or an energy sector ETF? The *geopolitical alpha* is the return above and beyond what a naive, non-geopolitical investor would have captured by accident.

---

## The Performance Measurement Framework

### Level 1 — Geopolitical Accuracy Score (GAS)

Build a log of every geopolitical prediction made, structured as:

| Field | Description |
|---|---|
| Date issued | When the call was made |
| Event prediction | Specific, falsifiable statement ("OPEC+ will cut production by >1mb/d within 90 days") |
| Confidence level | 1–5 scale |
| Timeframe | Specific deadline |
| Outcome | What actually happened |
| Accuracy | Correct / Partially correct / Incorrect |
| Notes | Why the call was right or wrong |

Track: **Hit rate by confidence level** (calibration). A well-calibrated analyst who says "70% confidence" should be right ~70% of the time. If your 5/5 confidence calls are right 55% of the time, your confidence is miscalibrated — a diagnostic in itself.

### Level 2 — Investment Signal Score (ISS)

For each geopolitical call that was *correct*, did the investment recommendation capture value?

Measure:
- **Direction accuracy:** Was long/short/avoid the right call?
- **Asset selection accuracy:** Was the specific instrument the right vehicle?
- **Timing accuracy:** Was the entry/exit timing consistent with the thesis (not just lucky)?
- **Sizing accuracy:** Did conviction-sizing correlate with actual outcomes?

This layer tells you whether your geopolitical framework translates into investable signals, independently of whether those signals are profitable after fees.

### Level 3 — Alpha Attribution

This is where you need a factor model. The logic:

**Total Return = Market Beta + Factor Beta + Geopolitical Alpha + Noise**

For a commodity-heavy geopolitical portfolio, the relevant factors are:
- Market beta (general risk-on/risk-off)
- Energy sector beta (passive exposure to energy moves)
- Dollar beta (USD strength/weakness driving commodity prices mechanically)
- Volatility regime (VIX-driven risk premiums)
- Momentum factor (was the position trending already?)

**Geopolitical Alpha = Total Return − (Market Beta × market return) − (Factor Beta × factor returns)**

The residual — if positive and persistent — is what your geopolitical framework is actually contributing. Everything else was available to a passive index investor who never read a single geopolitical analysis.

---

## Historical Grounding: The Bridge Water & CIA Example

Two cases illuminate how serious practitioners approach this:

**Ray Dalio / Bridgewater:** The Pure Alpha fund was built explicitly on the idea that macro/geopolitical alpha is real but must be proven systematically. Dalio built a 30+ year track record of logging every call, every thesis, every prediction — creating what he called a "baseball card" for every investment concept. The discipline was not just intellectual hygiene; it was a discovery engine. By tracking where they were systematically wrong, they improved the framework itself.

**The Intelligence Community:** The CIA and US intelligence community confronted the attribution problem decades before Wall Street took it seriously. Philip Tetlock's work (Superforecasting) emerged partly from studying why intelligence analysts were so poorly calibrated — and why most never got honest feedback on their predictions. The solution was systematic tracking, Brier scores, and calibration training. The result: superforecasters with structured feedback significantly outperformed unstructured analysts on geopolitical prediction accuracy. The lesson: **feedback loops are the technology.** The framework improves only if it is systematically tested against reality.

---

## Investment Implications

### For Prospectra

We are at an inflection point in the project. With 380 lessons delivered and a Databricks platform in development, the question is no longer "do we have a framework?" — we do. The question is: **does the framework actually work, and how do we know?**

This has direct implications for the investment thesis:

1. **Without attribution, the framework cannot improve.** Qualitative frameworks without measurement tend to suffer from confirmation bias — we remember the calls that worked and explain away the ones that didn't. Systematic logging breaks this.

2. **Attribution data is also the product.** If we eventually want to offer this as a commercial research service, institutional investors will ask for a track record. Not "qualitative insights." A track record — with hit rates, information coefficients, and alpha attribution. Building this now, while we have no clients, is when it is cheapest to be disciplined.

3. **Directional view on assets:** The market for "geopolitical research" is crowded with qualitative narratives. The market for *quantitatively validated* geopolitical signals with attribution data is much thinner. That is our differentiated position if we build the measurement infrastructure seriously.

### Asset Class Implications

- **Commodities:** Most susceptible to geopolitical mispricings. Also where passive factor exposures are most likely to confound attribution. Build the factor model here first.
- **EM currencies:** Geopolitical alpha is real but thin — the exchange rate literature suggests most FX moves are driven by macro, not geopolitics per se. High bar for demonstrating alpha.
- **Defense equities:** Easier attribution (binary conflict escalation → defense premium), but market is efficient at pricing known conflicts quickly.
- **Sovereign spreads:** Excellent attribution venue — political risk premium is directly observable in the spread over risk-free, and events have clear dates.

---

## Databricks Angle

This lesson has the highest direct Databricks relevance of any in the curriculum:

### Pipeline 1 — Prediction Logger
Build a structured prediction tracking table in the Databricks lakehouse:
- Schema: `prediction_id`, `date_issued`, `event_category`, `prediction_text`, `confidence_score`, `timeframe_days`, `outcome_date`, `outcome_text`, `accuracy_binary`, `notes`
- Delta table enables versioning, audit trail
- Ingest daily from a structured logging process (could be automated from CEO session outputs)

### Pipeline 2 — Factor Model Builder
Build the attribution factor model in Databricks:
- Pull daily returns for geopolitical portfolio positions (Yahoo Finance / FRED)
- Pull daily returns for relevant factor benchmarks (energy sector ETF, DXY, VIX, momentum)
- Run OLS regression: position return ~ factor returns (rolling 90-day window)
- Extract residuals = candidate geopolitical alpha
- Databricks ML Runtime: use MLflow to version each model fit and track alpha estimates over time

### Pipeline 3 — Calibration Dashboard
- Aggregate GAS scores by confidence bucket
- Plot predicted hit rate vs. actual hit rate → calibration curve
- Track ISS metrics over time
- Databricks AI/BI: build a live calibration dashboard showing framework accuracy by event category

**Key insight:** The attribution pipeline is not overhead — it *is* the product. An institutional investor buys the dashboard, not the narrative.

---

## Reflection Questions

1. **The Calibration Test:** If you were to score your own confidence on the geopolitical calls made over the last 6 months, would you expect your 4/5-confidence calls to be right 75–85% of the time? What would it mean for your framework if the actual hit rate came in at 55%?

2. **The Factor Stripping Exercise:** Take any strong investment call you remember making (e.g., long energy during a Middle East escalation). How would you structure the factor model to determine how much of that return was passive energy beta vs. genuine geopolitical alpha? What specific factors would you include, and why?

3. **The Feedback Loop Design:** Given that major geopolitical events with investment consequences happen only a few times per year, how would you build a feedback loop that generates enough signal to improve the framework within a 12-month window? What proxies or leading indicators could you track more frequently as intermediate verification?

---

## Questions for Next Session (Spaced Repetition Hook)

- We have now built measurement infrastructure. What does an honest 6-month audit of Prospectra's geopolitical calls reveal? (CEO will run this audit in the next session and bring findings.)
- How should confidence calibration scores change the weighting of geopolitical signals in the Databricks investment signal generator?
- What is the minimum track record length required before we can claim statistical validity for our alpha estimate?

---

*Lesson delivered by the AI CEO — Prospectra Geopolitics & Investment Project*
*Date: 2026-09-30 | Lesson 380 of Extended Curriculum*
