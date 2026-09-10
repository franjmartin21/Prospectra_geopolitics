# Lesson 318 — Writing Post #1: From GRI Data to Published Signal

**Date:** 2026-09-10
**Session Type:** Daily Lesson
**Lesson Number:** 318 / ongoing
**Topic:** Post #1 Execution — Country Selection, Five-Component Draft, and the 48-Hour Review
**Curriculum Arc:** Live Operations Module — Lesson 3: Writing the Signal

---

## Opening Question

*Today is Thursday, September 10. Post #1 goes live Monday morning, September 14. The outreach messages go out today and tomorrow. The Substack URL should exist by end of day.*

**"You have a publication name, a five-component architecture, a 20-person outreach list, and four days. The single task that separates a successful launch from a delayed launch is writing a draft that you're willing to send to someone you respect before Monday. What makes a first post good enough to send — and what makes it good enough to publish?"**

Those are different questions. A draft you're willing to send to a trusted contact is one where the analytical logic holds and the investment implication is falsifiable. A draft you're willing to publish is one where you've checked the logic under adversarial conditions, trimmed every sentence that doesn't pull its weight, and confirmed that the five-component structure is intact and the claim is yours to make.

This lesson builds both: the first draft and the editing pass. It walks through country selection, the component-by-component writing process, the benchmark for each section, and the 48-hour review window before Monday's post goes live.

The lesson is practical. By the time you finish reading it, you should have enough structure to open a document and write a post. If you finish the lesson without starting the draft, the lesson has failed.

---

## I. Country Selection: The Three Criteria for Post #1

Post #1 is not the place to pick the hardest signal. It is the place to pick the clearest signal — one where the GRI movement is unambiguous, the investment implication is directional, and the historical analogue is specific enough to be credible.

**Criterion 1: Significant GRI movement in the week of September 7–13.**

Pull the weekly GRI scores from your Databricks pipeline for all countries in your coverage universe. Sort by absolute weekly change (up or down). Post #1 should feature the country with the largest single-week GRI movement — not because it's the most interesting geopolitically, but because it's the most defensible analytically. When a first-time reader asks "why this country, this week?" the answer is: "Because this is where the data moved most."

If two countries show comparable movement, apply Criteria 2 and 3 as tiebreakers.

**Criterion 2: A clear, attributable mechanism.**

The GRI moved because something happened. The "something" must be:
- Publicly documented (news sources your reader can verify independently)
- Attributable to a specific driver (an election result, a central bank action, a military development, a diplomatic breakdown)
- Explainable in two sentences

If the GRI moved and you cannot state the mechanism in two sentences, the data pipeline may be working correctly but the mechanism is not yet clear enough to publish. Either wait for more clarity, or choose the country with the next-largest movement that does have a clear mechanism.

**Criterion 3: An investment implication with a specific, checkable asset.**

The implication must name a specific, liquid, investable instrument — not "EM equities generally" but "Turkish lira," "South African rand," "copper futures," "the iShares MSCI Turkey ETF (TUR)." The implication must have a direction (long or short or avoid), a timeframe (30 days, 90 days, 6 months), and a falsifiable condition (what would have to be true to change the view).

Vague implications ("investors should watch this space") are not signals. They are noise. If you cannot state the implication in one sentence with a named instrument, a direction, and a timeframe, the mechanism analysis is not complete.

**What to do if the GRI pipeline is not yet running at publication frequency:**

If the GDELT pipeline is not yet producing weekly GRI scores by September 13, use the manual scoring protocol: score the country across the three sub-dimensions (institutional stability, economic pressure, social cohesion) on a 0–10 scale using five published sources for each dimension. Document the sources in the draft. The analytical logic is identical; the data infrastructure will catch up. Do not delay Post #1 waiting for automated scores. The point of Post #1 is not to demonstrate automated infrastructure — it is to demonstrate analytical judgment.

---

## II. Writing the Five Components — Benchmarks and Common Errors

### Component 1: The Signal Headline (1 sentence, ~15–20 words)

**Purpose:** Tell the reader exactly what moved, in which direction, and why it matters in one sentence.

**Benchmark format:**
> [Country]'s GRI [rose/fell] [X] points this week on [mechanism in 3–5 words], reaching [score] — the [highest/lowest] reading since [reference date].

**Example:**
> Turkey's GRI rose 8.3 points this week on central bank governor resignation, reaching 61.2 — the highest reading since the 2021 lira crisis.

**Common errors:**
- The headline is too vague: "Geopolitical risk increased in Turkey this week." (Which dimension? By how much? Compared to what?)
- The mechanism is too long: "...following the abrupt resignation of the central bank governor under political pressure from the presidency, which raised concerns about monetary policy independence and fiscal credibility among institutional investors." (That's the mechanism paragraph, not the headline)
- The score is omitted: "Turkey's GRI spiked this week." (Readers cannot assess magnitude without the number)

### Component 2: The Mechanism (150–200 words)

**Purpose:** Explain what happened, why it moved the GRI, and which sub-dimension drove the movement.

**Benchmark structure:**
1. What happened (2–3 sentences, factual, dated)
2. Which GRI sub-dimension it affected and why (1–2 sentences, analytical)
3. What the sub-score history suggests about severity (1 sentence, contextual)

**Example:**
> On September 8, [Country]'s central bank governor announced his resignation, effective immediately, following public disagreement with the Finance Ministry over the pace of rate cuts. The governor had been the primary institutional anchor for currency credibility since the 2022 stabilization package; his departure removes the one figure institutional investors most closely associated with monetary orthodoxy.
>
> The resignation affected the Institutional Stability sub-dimension of the GRI primarily — specifically the "monetary authority independence" component, which tracks signals of political pressure on central bank governance. This sub-score fell from 6.8 to 4.1 in a single week; the only comparable single-week fall was in October 2021, which preceded a 30% depreciation of the lira over the following 90 days.
>
> The overall GRI rise reflects the market interpretation that this is not an isolated personnel change but a policy signal: the governing coalition is signaling a move to looser monetary conditions ahead of the 2027 elections.

**Common errors:**
- The mechanism is a news summary rather than an analytical interpretation: the reader can read the news themselves. The value is the GRI sub-dimension linkage and the historical context.
- The sub-score is not connected to the mechanism: if the GRI moved but you don't explain which component drove it and why, the signal architecture is not visible to the reader.

### Component 3: Historical Analogue (100–150 words, including a specific data point)

**Purpose:** Ground the current signal in a historical precedent that allows the reader to calibrate expected magnitude and direction.

**Benchmark structure:**
1. The analogue date and country (could be the same country or a different one with the same mechanism)
2. What happened to the named asset class in the 30–90 days following that signal
3. One sentence on what was different about that situation (to avoid false precision)

**Example:**
> The closest analogue is Turkey in October 2021, when the third central bank governor resignation in 18 months preceded an 18% depreciation of the lira against the dollar in 30 days and a 41% depreciation over 90 days. The USD/TRY rate moved from 9.2 to 11.1 in the month following the resignation announcement.
>
> The critical difference: the 2021 episode involved three governor changes in 18 months, signaling sustained political interference. The current situation is a single departure; if the replacement demonstrates credibility within 30 days, the lira impact may be contained to 8–12% rather than repeating the 2021 trajectory.

**Common errors:**
- The analogue is too general: "Turkey has had currency crises before." (Specific dates, specific instruments, specific magnitudes only)
- The analogue is stated without a falsifiability note: claiming the current situation will replicate the analogue exactly is not analysis, it's prediction. Always note what makes this situation different.

### Component 4: Investment Implication (75–100 words)

**Purpose:** State the directional view with an instrument, timeframe, and falsifiability condition.

**Benchmark structure:**
1. The instrument and direction (1 sentence)
2. The timeframe (included in sentence 1)
3. The conviction level (low/medium/high)
4. The falsifiability condition: what would change the view (1 sentence)

**Example:**
> **Directional view:** Short USD/TRY (long Turkish lira) is not the trade here. The GRI signal is consistent with continued lira pressure over a 30–90 day horizon; the institutional uncertainty premium will not clear until the replacement governor demonstrates monetary independence. The cleaner expression is via TUR put options with a 60-day expiry if you have derivatives access, or underweight Turkish equities in an EM portfolio. **Conviction: Medium.** The view changes if the replacement governor is drawn from outside the political inner circle and makes a credible first policy statement within two weeks of appointment.

**Common errors:**
- No instrument named: "Turkish assets look vulnerable." (Which ones? Equities, bonds, currency, all three?)
- No timeframe: "We expect lira pressure." (Over what horizon?)
- No falsifiability: "We remain bearish on Turkey." (This is not a falsifiable claim — what would make you bullish?)
- The implication is a hedge: "Investors should monitor this situation carefully." (This is not an implication; it is a disclaimer)

### Component 5: Forward Watch (50–75 words)

**Purpose:** Tell the reader what to watch in the next 7 days that will either confirm or contradict the signal.

**Benchmark structure:**
1. The specific observable event (named, dated if possible)
2. What outcome would confirm the bearish signal
3. What outcome would reduce it

**Example:**
> **Watch this week:** The announcement of the new central bank governor appointment (expected within 72 hours). If the appointment is a current or former MPC member with a track record of rate orthodoxy — confirm bearish lira signal. If the appointment is a political figure with no monetary policy background — escalate to High conviction. If the appointment is delayed beyond one week — lira continues to reprice the uncertainty premium and the 30-day price target moves lower.

**Common errors:**
- The forward watch is too vague: "Monitor central bank communications." (Monitor specifically what? What would confirm the signal?)
- The forward watch names nothing observable: "Watch for sentiment changes in EM." (This is not watchable on a weekly basis)

---

## III. The New Reader Note (Post #1 Only)

As described in Lesson 317, Post #1 carries a second section after the signal: the 100-word "Why This Exists" note placed after the signal content. That note is already drafted in Lesson 317. Copy it verbatim for Post #1; do not modify it for the first publication.

The note reads:

> *A note for new readers: Prospectra is a geopolitical intelligence platform for EM investors. The signal you just read is generated by the Prospectra GRI — a composite weekly score built on GDELT event data, news sentiment, and macroeconomic indicators. Every number in this post is dated, sourced, and falsifiable. The investment implication carries an explicit timeframe and the conditions under which we'd change our view. If you want to understand the methodology behind these scores, or explore the full platform with 10+ country coverage, reply to this email. — F.M.*

From Post #2 onward, this note is replaced with a two-line footer referencing the Substack archive and the trial request mechanism.

---

## IV. The Draft Timeline: Thursday–Sunday

**Thursday September 10 (today):** 
1. Pull GRI scores. Select the country.
2. Write Component 1 (headline) and Component 2 (mechanism) — these are the analytical core and require the most research.
3. Send the outreach messages to the first 10 contacts on your list (Tier 1 priority).

**Friday September 11:**
1. Write Components 3, 4, and 5 (analogue, implication, forward watch).
2. Paste the Lesson 317 new reader note after Component 5.
3. Full draft is complete.
4. Send the remaining 10 outreach messages.

**Saturday September 12 (Review Day):**
1. Send the full draft to two people from your Tier 3 validator list (people whose analytical judgment you trust). Ask a single question: "Is the investment implication specific enough that you could act on it? If not — what's missing?"
2. Read the draft aloud. Every sentence that you stumble reading should be rewritten or cut.
3. Check each component against the benchmark in this lesson. Are all five present? Does each component meet its word count range? Is every number sourced?

**Sunday September 13 (Final Edit):**
1. Apply validator feedback.
2. Run the editing checklist (Section V).
3. Schedule the Substack post for 7:00 AM Monday, September 14.
4. Write and schedule the LinkedIn post for 7:30 AM Monday.
5. The week is closed.

---

## V. The Editing Checklist (Run Before Scheduling)

Run this checklist against the final draft before scheduling. A "no" on any item means the draft is not ready to publish.

**Analytical integrity:**
- [ ] The GRI score change is a specific number (not "rose significantly")
- [ ] The mechanism is attributed to a specific, dated event (not "recent developments")
- [ ] The historical analogue includes a date, a country (may be the same), and a specific magnitude (not "similar events in the past")
- [ ] The investment implication names a specific instrument
- [ ] The investment implication has a direction (long/short/underweight/avoid)
- [ ] The investment implication has a timeframe (30-day, 90-day, 6-month)
- [ ] The investment implication has a falsifiability condition ("the view changes if...")
- [ ] The forward watch names something observable within 7 days

**Voice and length:**
- [ ] No sentence begins with "It is important to note that..."
- [ ] No sentence contains the phrase "geopolitical uncertainty" without specifying which geopolitical uncertainty
- [ ] No sentence contains the phrase "investors should monitor" without specifying what to monitor and what a monitoring result means
- [ ] Headline: ≤20 words
- [ ] Mechanism: 150–200 words
- [ ] Historical analogue: 100–150 words
- [ ] Investment implication: 75–100 words
- [ ] Forward watch: 50–75 words
- [ ] New reader note: ≤110 words
- [ ] Total post length: 600–750 words

**Structural completeness:**
- [ ] All five components are present in order
- [ ] The new reader note is placed after Component 5
- [ ] No component is missing or merged with another
- [ ] The post has a title that matches the headline format

**The test that matters most:** Forward this post to one person from your ICP. If they respond with "this is useful" or a substantive question about the signal, the post is ready. If they respond with "interesting" or nothing, the analytical depth or the relevance selection needs work. Post #2 is the correction mechanism — but only if you sent Post #1 and measured the response.

---

## VI. What Post #1 Is Not Trying to Do

Post #1 has one job: demonstrate that the Prospectra GRI produces a specific, defensible, investment-relevant signal, and that Francisco Martín can explain it clearly.

Post #1 is not trying to:
- Establish methodological credibility (that's the About page and the archive over 12 weeks)
- Prove the infrastructure (the Databricks pipeline can be mentioned but not featured — institutional readers don't care about your tech stack in Post #1)
- Convert subscribers to paid customers (that's Posts 8–16, when the track record is visible)
- Be comprehensive about the country (200 words on the mechanism, not a 1,000-word country report)

The instinct toward comprehensiveness is the enemy of a readable first signal. The five-component format is a constraint, not a suggestion. Every paragraph that does not fit one of the five components belongs in a deep dive or an appendix, not in the weekly signal.

The post is 650 words. It takes four minutes to read. A portfolio manager reads it between meetings on a Monday morning, flags the investment implication for their Tuesday morning team meeting, and either acts on it or files it in the mental model of EM risk. That is the use case. Write for that reader, in that moment.

---

## Investment Implications

### The Signal as Reputation Capital: How Publication Quality Compounds

Every published signal is a dated, public record of analytical judgment. At 52 signals (one year), the Prospectra archive contains 52 investment implications — each with a named instrument, a direction, a timeframe, and a falsifiability condition. Every one of those can be audited.

This is qualitatively different from the way most macro analysts at banks and asset managers communicate. Bank research typically hedges at every level: "we see risks on both sides," "the situation warrants close monitoring," "investors should consider their own risk tolerance." The hedging is rational — a bank analyst who publishes a falsifiable call and is wrong faces internal and external accountability. An independent signal publisher who publishes a falsifiable call and is wrong builds credibility by explaining what they got wrong and why.

**The investment implication for how to think about this publication:**

The Prospectra track record is not just a marketing asset — it is a systematic audit log of the analytical framework. After 52 signals:

1. What is the win rate on directional calls within the stated timeframe?
2. Which mechanisms (central bank, election, military escalation, sanctions) have the highest predictive accuracy?
3. Which asset classes (currency, equities, rates, commodities) show the tightest correlation between GRI movement and price response?

A framework that has been tested against 52 public, falsifiable signals is the kind of framework that institutional investors pay for. Not because of the signal per se — many signals exist. But because the audit trail demonstrates that the methodology is consistent and the analyst is accountable.

**The compounding dynamic:** Win rate at signal 1 is irrelevant. Win rate at signal 52, compared to a benchmark, is the product you're selling. Every Monday's 75-minute workflow is a data point in the track record. The track record is the asset. The track record starts Monday.

---

## Databricks Angle

**Build: `prospectra.gold.signal_track_record` — The Audit Table**

Start logging every signal in a structured table from Day 1. The schema:

```python
signal_schema = StructType([
    StructField("signal_id", StringType(), False),          # e.g. "2026-09-14-TUR"
    StructField("publication_date", DateType(), False),
    StructField("country_iso", StringType(), False),         # ISO 3166-1 alpha-3
    StructField("gri_score_start", FloatType(), True),       # score at signal publication
    StructField("gri_change_week", FloatType(), True),       # weekly delta
    StructField("mechanism_tag", StringType(), True),        # "central_bank", "election", "military", "sanctions", "diplomatic"
    StructField("instrument", StringType(), False),           # e.g. "USD/TRY"
    StructField("direction", StringType(), False),            # "long", "short", "underweight", "avoid"
    StructField("timeframe_days", IntegerType(), False),      # 30, 60, 90, 180
    StructField("conviction", StringType(), True),            # "low", "medium", "high"
    StructField("falsifiability_condition", StringType(), True),
    # Outcome fields — populated when timeframe expires:
    StructField("outcome_date", DateType(), True),
    StructField("price_at_signal", FloatType(), True),
    StructField("price_at_expiry", FloatType(), True),
    StructField("direction_correct", BooleanType(), True),    # did price move in signaled direction?
    StructField("magnitude_pct", FloatType(), True),          # actual price move as %
    StructField("falsifiability_triggered", BooleanType(), True),  # did the falsifiability condition fire?
    StructField("outcome_notes", StringType(), True)           # qualitative post-mortem
])
```

**The audit query (run weekly after 8 signals):**

```python
track_record = spark.sql("""
  SELECT
    mechanism_tag,
    direction,
    COUNT(*) AS signals_issued,
    SUM(CASE WHEN direction_correct THEN 1 ELSE 0 END) AS correct_direction,
    ROUND(100.0 * SUM(CASE WHEN direction_correct THEN 1 ELSE 0 END) / 
          COUNT(CASE WHEN outcome_date IS NOT NULL THEN 1 END), 1) AS win_rate_pct,
    ROUND(AVG(CASE WHEN direction_correct THEN magnitude_pct END), 2) AS avg_win_magnitude,
    ROUND(AVG(CASE WHEN NOT direction_correct THEN ABS(magnitude_pct) END), 2) AS avg_loss_magnitude,
    
    -- Profit factor (total wins / total losses in magnitude terms)
    ROUND(SUM(CASE WHEN direction_correct THEN ABS(magnitude_pct) ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN NOT direction_correct THEN ABS(magnitude_pct) ELSE 0 END), 0), 2) AS profit_factor
  FROM prospectra.gold.signal_track_record
  WHERE outcome_date IS NOT NULL
  GROUP BY mechanism_tag, direction
  ORDER BY win_rate_pct DESC
""")
```

Log the first signal manually on September 14. The table is the foundation of the institutional pitch at month 6: "Here are 26 signals, here is the win rate by mechanism, here is the profit factor." No track record table means no institutional pitch. Start it Monday.

---

## Key Concepts Covered

1. **The three-criteria country selection framework** — GRI magnitude, mechanism clarity, instrument specificity
2. **Five-component benchmarks** — word counts, structural requirements, and common errors for each component
3. **The draft timeline** — Thursday through Sunday execution plan for Post #1
4. **The editing checklist** — 15-point pre-publication quality check
5. **What Post #1 is not trying to do** — the instinct toward comprehensiveness is the enemy of a readable signal
6. **Signal as reputation capital** — how 52 dated, falsifiable calls compound into the institutional credibility asset
7. **The `signal_track_record` table** — the audit infrastructure that makes the pitch possible at month 6

---

## Reflection Questions

1. **Country selection:** After pulling this week's GRI scores, what is the country with the largest single-week change? Does it meet all three criteria — significant movement, attributable mechanism, specific investable instrument? If the top mover fails Criterion 3, what is the second-largest mover, and does it meet all three?

2. **The falsifiability test:** Take the investment implication you plan to publish and state the condition under which you would publicly revise the call in a future issue. If you cannot state that condition in one sentence, the implication is not falsifiable — it's a directional bias statement. What's the condition?

3. **The validator question:** Who from your Tier 3 validator list will you send the draft to on Saturday? What specific question will you ask them? ("Does this feel right?" is not a question; "Is the investment implication specific enough that you could bring it to a Tuesday morning team meeting at your fund?" is a question.)

---

## Questions for Next Session (Spaced Repetition Hook)

- Is Post #1 drafted? What country, what mechanism, what implication?
- Has the `signal_track_record` table schema been created in Databricks?
- Did the pre-launch outreach go out? What was the response rate?
- What is the Substack URL?

---

## Databricks Relevance Note

**From Weekly Signal to Structured Dataset**

The Prospectra Signal exists in two forms simultaneously: as a publication (read by humans) and as a structured data entry (logged by the CEO in the track record table). This duality is the architectural principle that distinguishes Prospectra from every other macro/geopolitical newsletter.

Every other signal newsletter in the market — from Byrne Hobart to Michael Pettis to Erik Townsend — publishes qualitative analysis. The author's credibility rests on their reputation, not on a queryable dataset of their calls. Prospectra's credibility, over time, rests on both: the analyst's voice and the auditable record.

After 52 signals, the track record table is the dataset that no competitor can replicate without also publishing 52 signals in the same structured format. The data moat is built one Monday at a time.

Build the table. Log every signal. The moat starts September 14.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 318 | September 10, 2026 | Live Operations Module — Lesson 3: Writing the Signal*
