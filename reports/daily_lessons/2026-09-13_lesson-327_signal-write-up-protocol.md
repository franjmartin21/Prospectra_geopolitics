# Lesson 327 — The Signal Write-Up Protocol: From Conviction to Published Prose

**Date:** 2026-09-13
**Session Type:** Daily Lesson
**Lesson Number:** 327 / ongoing
**Topic:** The Signal Write-Up Protocol — Converting Completed Analysis into Publishable Signal
**Curriculum Arc:** Live Operations Module — Lesson 12: The Last Mile

---

## Opening Question

*You've completed the 5-layer analysis stack from Lesson 326. Ninety minutes of structured work. Turkey's GRI delta is Explanation 3 — a structural shift. You've identified the mechanism (government seizure of independent judiciary, 3-month window), the asset (TRY/USD), the pricing gap (sell-side consensus still treating the risk as bounded), and the time horizon (90 days to first outcome checkpoint). You have conviction.*

**"You open a blank Substack draft. What is the first sentence — and why does that sentence determine whether an institutional reader subscribes, forwards the signal to their CIO, or closes the tab?"**

The failure mode of the last mile is not analytical. You've already done the analysis. The failure is *translation*: converting rigorous private analysis into prose that is immediately legible to a time-constrained institutional reader who has not done your 90 minutes of work and will not do it. If the write-up buries the thesis, obscures the directional call, or hedges the conviction you actually hold — the track record will be correct but invisible. Correct analysis that isn't read generates no track record, no subscribers, and no product.

This lesson defines the precise protocol for converting a completed 5-layer analysis into a signal post that is accurate, legible, and positions Prospectra as a systematic research product rather than a newsletter.

---

## I. The Institutional Reader's Reading Pattern

Before writing a single word, understand how your target reader will read what you write.

A macro PM or quant analyst approaching a signal post from an unfamiliar research product will follow a four-step reading pattern:

**Step 1 — The Scan (10 seconds).** They read the headline and the first two sentences. If those two sentences contain: (a) a country or asset, (b) a directional call, and (c) a time horizon — they continue. If any of those three elements is absent, they close the tab. They have 40 other things to read today.

**Step 2 — The Mechanism Check (60 seconds).** They read the section that explains *why* the call is correct. They are not reading for novelty — they are reading to assess whether the mechanism is coherent, specific, and distinct from what they already believe. If the mechanism is vague ("geopolitical uncertainty may affect the currency"), they classify the source as noise and move on. A specific mechanism ("the TRY's forward curve does not yet reflect judicial independence removal reducing FDI inflows; that channel has a 90-day lag to pricing") is what stops them.

**Step 3 — The Falsification Check (30 seconds).** An institutional reader trusts a research product that names what would make it wrong more than one that doesn't. If your post says "we would close this thesis if the Central Bank announces emergency rate coordination with the IMF before Day 45" — they take you more seriously. It demonstrates you are not committed to being right, you are committed to being accurate.

**Step 4 — The Source Assessment (30 seconds).** They look at the data sources you cite. GDELT event counts, asset price data from FRED, TRY/USD forward curve from Bloomberg. If the sources are named specifically — not "market data" but "GDELT Cameo 145 event counts over 14-day window, 12-month NDF market from Bloomberg" — the post signals that there is a reproducible methodology behind it.

Four steps. Under two minutes. This is what your write-up must survive.

---

## II. The Signal Post Structure

Every Prospectra signal post follows a fixed six-section structure. The structure is not optional — it is the product. When an institutional subscriber sees the structure at Signal #2, they should recognize it from Signal #1. By Signal #10, they should know exactly where to look for the falsification condition. Consistency in structure is the first form of institutional credibility.

### Section 1 — The Headline (one line)

**Format:** `[COUNTRY/ASSET] | [DIRECTION] | [TIMEFRAME] | Signal #[N]`

**Example:** `TURKEY (TRY/USD) | BEARISH TRY | 90-Day Horizon | Signal #2`

The headline is a data field, not a title. It gives an experienced reader everything they need to triage the signal before reading a word of prose. Do not make the headline clever, evocative, or thematic. Make it a structured identifier.

### Section 2 — The Thesis (two sentences, maximum)

The thesis states the call and the core mechanism. Nothing else.

**Format:** "We are [directional view] on [asset/instrument] over a [timeframe] horizon. Our view is driven by [specific mechanism] which we estimate has not yet been priced into [specific market indicator or forward curve]."

**Example:** "We are bearish TRY/USD over a 90-day horizon. Our view is driven by the Turkish government's formal removal of Central Bank board independence (July 2026), which we estimate is not yet fully priced into the 3-month NDF forward curve, which implies only 4% TRY depreciation versus our modeled 12–18%."

Note what is absent: hedge language ("may", "could", "might"), uncertainty signaling ("it is possible that"), or both sides ("while there are offsetting factors..."). The thesis states the conviction you reached in the 5-layer analysis stack. If you don't have conviction, the signal is not ready to publish. Go back to Layer 3.

### Section 3 — The Evidence Stack (three to five bullet points)

This section presents the evidence from Layers 1–4 of the analysis process in compressed form. Each bullet follows a format:

`[Data source] | [Observation] | [Interpretation]`

**Example bullets:**
- `GDELT GRI | Turkey GRI delta: +18 points over 14 days, 3rd highest in 40-country scan | Multi-event pattern (judicial, economic, diplomatic), not single news cycle; structurally driven`
- `GDELT Event Type | Conflict events (CAMEO 14x) +34% vs 90-day baseline; Protest events (CAMEO 14) +61% | Domestic political stress concurrent with diplomatic row — dual-vector deterioration`
- `TRY/USD forward curve (Bloomberg, 3-month NDF) | 4.1% implied depreciation | Sell-side consensus models 4–6%; Prospectra GRI-based model implies 12–18% based on FDI inflow disruption channel`
- `EM peers | Mexico (similar CB independence removal, 2021) | 17% MXN depreciation over 90-day post-event window; Turkish sovereign spread has moved +80bps vs Mexico's +140bps in analogous period — incomplete convergence`

Three bullets is sufficient. Five is the maximum. More than five bullets signals that you don't know which evidence is load-bearing. Cut to the strongest.

### Section 4 — The Falsification Condition

This section is the most important sentence in the post from an institutional credibility standpoint. It states, clearly and in advance, what observable outcome would cause you to close or reverse the thesis before the scheduled outcome date.

**Format:** "We close this thesis before the scheduled outcome date if: [observable condition]."

**Example:** "We close this thesis before the scheduled outcome date if: (1) the Turkish Central Bank announces a coordinated rate path with IMF technical assistance before Day 45, or (2) the TRY/USD 3-month NDF implied depreciation closes above 9% (indicating significant market re-pricing of the risk we identify, eliminating the pricing gap that justifies the call)."

The falsification condition is not a stop-loss. It is the analytical condition that would change your view of the thesis mechanism — not the price at which you would capitulate. Stop-losses belong in position management. Falsification conditions belong in systematic research.

### Section 5 — The Databricks Note (three to four lines)

This section makes Prospectra's methodology legible and differentiates it from qualitative macro commentary. It names the specific data infrastructure behind the call.

**Format:** Brief description of the pipeline that produced the signal, the specific query or model, and the output metric.

**Example:** "This signal was generated from the Prospectra GRI pipeline (GDELT CAMEO event data, 14-day rolling window, 40-country scan). The GRI delta for Turkey was computed from the weighted conflict/mediation/tone composite score. Forward curve data from Bloomberg. The pricing gap estimate is derived from the EM peer analog model (Mexico CB independence removal, 2021) applied to the Turkish NDF surface. Full methodology documentation: [link]."

This section functions as institutional due diligence material. A quant fund analyst will screenshot this section and send it to their data team. It is not marketing — it is evidence that the methodology is reproducible.

### Section 6 — The Track Record Header (auto-updated)

Every post should include a live track record table as a header block — updated at each publication. This is not manually maintained. It should be pulled from the Databricks investment log and rendered as a static table in the post.

**Format:**

| Signal | Asset | Direction | Horizon | Outcome | Correct? |
|---|---|---|---|---|---|
| #1 | [asset] | [direction] | [days] | [outcome if closed] | [Y/N/Open] |
| #2 | [asset] | [direction] | [days] | Open | — |

At Signal #2, one row is Open. By Signal #26, this table is the most important document in the pitch. Protect it with the outcome scoring protocol from Lesson 325.

---

## III. The Four Writing Rules

Once the structure is clear, four writing rules govern every sentence in every section.

**Rule 1: State the direction before the reasoning.** The first sentence of Sections 2 and 3 states the directional call — not the context, the background, or the setup. A reader who has not yet encountered your framework does not need to understand Turkey's history before knowing you are bearish TRY. They need the call first, the mechanism second. Background last, if at all.

**Rule 2: Every number must have a source.** "12–18% implied depreciation" must be followed by "(GRI-based model; see methodology)". "80bps sovereign spread move" must be followed by "(Bloomberg, 12-month CDS)". A number without a source is a claim. A number with a source is evidence. Write evidence, not claims.

**Rule 3: Cut the hedge language on the second draft.** In the first draft, write freely — you will naturally include hedges ("this may suggest", "it is possible that", "we note some uncertainty around"). In the second draft, identify every hedge and ask: does this hedge reflect genuine analytical uncertainty (keep it) or does it reflect social discomfort with stating a conviction plainly (cut it)? Cut every hedge in the second category. If you are not willing to state a directional call without hedging it, the signal is not ready.

**Rule 4: The last sentence of the post is the signal's expiration date.** Every post ends with: "This signal will be scored on [specific date, in approximately 60–90 days]. Scoring protocol: [link to Lesson 325 methodology post]. Next signal: [date of next GRI scan]."

---

## IV. Time Budget for the Write-Up

The write-up block follows the 90-minute analysis block. Its time allocation:

| Task | Time |
|---|---|
| Draft Section 2 (Thesis) | 10 minutes |
| Draft Section 3 (Evidence bullets) | 20 minutes |
| Draft Section 4 (Falsification) | 10 minutes |
| Draft Section 5 (Databricks note) | 10 minutes |
| Draft Section 6 (Track record table) | 5 minutes |
| Second draft: cut hedges, add sources | 15 minutes |
| Headline and final review | 5 minutes |
| **Total** | **75 minutes** |

The write-up should never exceed 75 minutes. If the write-up is taking longer, the problem is not the writing — it is that the conviction from the analysis stack is not fully formed. Stop writing. Go back to Layer 3 (Mechanism) or Layer 4 (Market Pricing) of the analysis. Re-run those layers. Then return to the write-up.

A write-up that exceeds 75 minutes is diagnostic data, not a time management problem.

---

## Investment Implications

The write-up protocol is not soft process documentation — it is the product specification. The six-section structure defines what Prospectra *is* to an institutional reader. The four writing rules determine whether that institutional reader forwards the signal to their CIO or archives it. The 75-minute time budget enforces the feedback loop between conviction quality and write-up quality.

The Substack subscription model for a systematic research product is not driven by content volume. It is driven by signal legibility and track record integrity. A reader who understands exactly what they are getting (a directional call, a mechanism, a falsification condition, a scoring date) and gets it in exactly that format every week will subscribe. A reader who must decode each post's structure to find the thesis will not.

**Asset class note:** The write-up protocol has a direct implication for the long-horizon investment thesis this project manages. Every call made internally for the investment log should be written in the same six-section format — not because the investment log has institutional readers, but because the discipline of writing the falsification condition *before* the outcome forces the CEO and Bolo to identify the mechanism before having an outcome to rationalize. The single largest source of track record contamination is retrospective thesis construction. The write-up protocol prevents it.

---

## Databricks Angle

**Auto-generation of Section 6 (Track Record Table)**

The track record table in every signal post should be auto-generated from a Databricks query against the investment log, not manually maintained. The target pipeline:

```
investment_log (Delta table)
  → filter: signal_type = 'substack'
  → join: signal_outcomes (on signal_id, if outcome_date <= today)
  → render: six-column table (signal_id, asset, direction, horizon_days, outcome, correct)
  → output: markdown-formatted string, auto-appended to Substack draft via API
```

**Relevant datasets:**
- `investment_log` (internal, built in Phase 1)
- `signal_outcomes` (new table: tracks scoring events, price sources, scoring timestamps per Lesson 325 protocol)

**Pipeline milestone:** By Signal #5, this automation should be live. Manually updating the track record table is the highest-risk path to inadvertent track record contamination — a copy-paste error on an outcome column is indistinguishable from deliberate manipulation to an outside reviewer. Automate it as if it will be audited, because eventually it will be.

**Feature engineering note:** The write-up's evidence bullets (Section 3) can be partially auto-drafted from the GRI scan query output. Once the 5-layer analysis stack is formalized as a Databricks notebook, the output of Layers 1–3 (source interrogation, mechanism identification, peer comparison) can be rendered as draft bullet text using a templated prompt, with the analyst reviewing and editing for accuracy. This reduces the write-up time budget and ensures the evidence bullets are always grounded in the actual data query, not recalled from memory.

---

## Reflection Questions

1. **The hedge audit.** Take Signal #1's write-up and apply Writing Rule 3 to it: identify every instance of hedge language. For each hedge, decide: does it reflect genuine analytical uncertainty (keep) or social discomfort with stating conviction plainly (cut)? What changes?

2. **The scan test.** Read the first two sentences of Signal #1. Does an institutional reader find: (a) the asset, (b) the directional call, and (c) the time horizon? If any of the three is absent, what would you rewrite?

3. **The falsification condition.** State the falsification condition for Signal #1. Write it in the format from Section 4 of this lesson. Is it based on an analytical condition (a change in the mechanism) or a price condition (a stop-loss)? If it's a price condition, what would make it an analytical condition instead?

---

## Questions for Next Session

- **Spaced repetition — Lesson 325:** The outcome scoring protocol specifies the precise sequence of actions on the day a signal closes. Does the falsification condition from today's lesson interact with that protocol? If you close a signal early (before the scheduled date) because the falsification condition fires, what does the outcome score? How does that appear in the track record?

- **Looking forward — Lesson 328:** The write-up protocol defines the internal process. The next question is external: how does the signal reach the institutional readers Prospectra is building toward? That requires a distribution protocol — not just publishing on Substack, but systematic outreach to the specific institutional contacts that convert to paid subscribers.

---

*Lesson 327 of ongoing curriculum. CEO — Prospectra Geopolitics & Investment Project.*
*Next lesson: Lesson 328 — The Distribution Protocol: Getting Signals in Front of Institutional Readers*
