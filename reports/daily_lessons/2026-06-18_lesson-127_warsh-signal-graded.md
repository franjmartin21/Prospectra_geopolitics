# Lesson 127: The Warsh Signal, Graded — Applying the Protocol to What Actually Happened

**Date:** 2026-06-18
**Session Type:** Daily Lesson
**Lesson Number:** 127 of ongoing curriculum
**Topic:** Executing a Pre-Committed Interpretation Protocol Against Real Fed Communication — and Auditing the Protocol Itself

---

## CEO Note Before We Begin

Warsh's press conference happened yesterday afternoon (June 17, 2:30 PM ET), as scheduled. We now have a transcript, a dot plot, and a market reaction. This session does exactly what Lesson 126 said it would do: run the four observables through `classify_warsh_signal()`, execute the resulting action on Positions 10 and 12, and stop.

One honest gap first: Lesson 126's reflection question 1 asked Bolo to pre-register a prediction — personal dot submitted, defense/tariff inflation mention, 2-year yield move in bps — before 2:30 PM ET. This session's inbox check (per standing protocol) found no reply on that thread and no pre-registered prediction on file. That means we cannot grade Bolo's calibration today. We log this as a missed data point rather than pretend it happened — the entire point of pre-registration is that it can't be reconstructed after the fact. Reflection Question 1 below reopens the practice for the next scheduled event instead.

What we *can* grade is the protocol itself — and it turns out the most valuable finding today isn't the FOMC signal. It's a flaw the protocol's own code almost introduced.

---

## Opening Framing Question

A protocol built in calm conditions is only as good as its weakest definition. Lesson 126 wrote the protocol in two places: a Python-style function with named parameters, and a prose checklist above it explaining what each parameter means. Today's question, before we even look at what Warsh said: **what happens when the prose definition is broader than the variable name that's supposed to represent it — and the real-world data lands in the gap between them?**

Hold that question. Section 3 below is a live example, not a hypothetical.

---

## Section 1: The Four Observables, As They Actually Occurred

**Rate decision:** FOMC voted 12-0 to hold the federal funds rate at 3.50%–3.75%. No surprise — this was a 97%+ market-implied certainty entering the meeting.

**Observable 1 — Did Warsh submit a personal dot?** **No.** Warsh explicitly declined to submit a forecast to the Summary of Economic Projections, while allowing the other 18 FOMC participants to submit theirs anonymously. He tied this to a position he has held publicly since his April 2026 confirmation hearing: "I do not believe in forward guidance on interest rates tied to economic data." This was not an improvised dodge — it was the execution of a stated, pre-existing philosophy.

**Observable 2 — Did he name defense spending, NATO's 5% commitment, or tariff pass-through explicitly as an inflation driver?** **Yes — tariffs, specifically.** Warsh and the post-meeting commentary identified an inflation pipeline of "PPI components accelerating and yet to reach the consumer, new tariffs being implemented, and wage growth remaining robust." Tariff pass-through was named directly, in causal language, as a forward-looking inflation source — not vague hand-waving about "uncertainty." No explicit mention of NATO or defense spending specifically; the fiscal-driver mention that materialized was the tariff channel, not the defense-spending channel.

**Observable 3 — 2-year Treasury yield move.** **+16 basis points**, to 4.216%, in the hours following the statement and press conference. That is a large one-day move for the most policy-sensitive point on the curve — unambiguous in direction.

**Observable 4 — "Data dependent" / "meeting-by-meeting" framing.** Mixed signal, lowest-confidence observable of the four. The post-meeting statement was shortened to roughly 130 words (from the multi-paragraph statements typical of the Powell era), explicitly stripping "outdated language" and forward-guidance phrasing, with Warsh describing the committee as "focusing on data and the committee's goals." That is data-anchored in spirit. But Warsh also explicitly distanced himself from "data dependent" as a stock phrase, since he considers the entire genre of forward-guidance-via-framing to be the thing he's trying to retire. Read this one as weakly supportive of "substance, not slogan" rather than a clean yes/no.

**Supporting context (not in the original four observables, but relevant):**
- Dot plot: 9 of 18 voting members project at least one hike before year-end; 6 of those project two 25bp hikes. Median projected federal funds rate for end-2026 rose to 3.8%, up from 3.4% in the March projection — a net hike from the current 3.5–3.75% range, not a cut.
- PCE inflation projection for year-end revised sharply up to 3.6%, from 2.7% in March.
- Warsh announced five new internal task forces (monetary policy operations, communications, data sources, productivity/labor market, and causes of inflation) — consistent with the "leaner, more humble Fed" framing previewed in Lesson 126.
- Equity markets sold off on the day; the move was characterized in coverage as the kind of one-day volatility spike a market unaccustomed to a quieter, more hawkish-leaning Fed produces.

---

## Section 2: Running `classify_warsh_signal()` With Real Inputs

```python
result = classify_warsh_signal(
    two_year_yield_change_bps=16,
    dot_plot_2026_cuts=0,                     # median dot implies a hike, not a cut
    personal_dot_submitted=False,
    mentions_defense_spending_inflation=True,  # tariff pass-through named explicitly
    uses_data_dependent_language=True,         # weak/mixed, see Observable 4 above
)

# result = {
#   "signal": "HAWKISH",
#   "position_10": "HOLD at 2-3% — differential sustains carry, tail risk persists",
#   "position_12": "NO ACTION — thesis CONFIRMED. Direct acknowledgment of
#                    fiscal/defense-driven inflation pressure validates the
#                    structural fiscal dominance read."
# }
```

**Signal classification: HAWKISH.** Both independent triggers fired — the 2-year yield move (+16bps, threshold was >10) and the dot plot (0 cuts, threshold was ==0). No ambiguity in this case; reality landed cleanly in one box, which is itself notable given Lesson 126 flagged AMBIGUOUS as "the most likely single outcome for a brand-new chair's first meeting." It wasn't. The market and the dot plot agreed, hard, in the same direction.

**Position 10 (EM Tail Hedge) action: HOLD at 2–3%.** The hawkish signal sustains the dollar-yen rate differential that underlies the carry trade, meaning the BOJ-unwind tail risk this hedge protects against has not diminished. No sizing change.

**Position 12 (Long TIPS) action: NO ACTION — thesis CONFIRMED.** This is the strongest outcome the protocol could produce from a single meeting, and it's worth being precise about why.

---

## Section 3: The Near-Miss in Protocol Design

Here is the gap the opening question pointed at. The function parameter is literally named `mentions_defense_spending_inflation` — a name anchored to the specific hypothesis Lessons 124–126 had been tracking (NATO's 5% GDP commitment as the leading edge of fiscal-dominance-driven inflation). But the **prose specification** in Lesson 126, Section 4, bullet 2, correctly defined the criterion more broadly: *"Does he name defense spending, NATO's 5% GDP commitment, or tariff pass-through explicitly as an inflation driver?"*

Warsh's actual answer satisfies the broad prose criterion (tariffs, named explicitly, as a forward inflation driver) but would fail a narrow literal reading of the variable name (he said nothing about defense spending or NATO). If Bolo — or a future automated version of this check — had mechanically searched the transcript for "defense" or "NATO" and stopped there, today's grading would have wrongly fallen into the neutral/ambiguous branch of the function (`NO ACTION — log as neutral input`) instead of the thesis-confirmed branch. Those two branches are not interchangeable: one logs a non-event, the other logs a structural confirmation feeding the Conviction Score Engine. Same transcript, opposite conclusion, depending on which definition you trust — the code or the prose.

**This is exactly the failure mode pre-commitment protocols exist to prevent, and exactly the failure mode that can creep back in through sloppy implementation.** The discipline isn't just "write the rule in advance." It's "make sure the rule you actually check against is the rule you meant to write." A variable name is a label, not a specification — and over a protocol's lifespan across multiple lessons (124 → 126 → executed in 127), the canonical definition has to live in one place, not be silently narrowed by whichever piece of code happens to get copy-pasted forward.

**Action taken:** the underlying observable should be renamed from `mentions_defense_spending_inflation` to `mentions_fiscal_inflation_driver` (covering defense spending, NATO commitments, *and* tariff pass-through under one explicit umbrella) before the next FOMC cycle. This is a one-line fix, but it's the one-line fix that determines whether the next grading session gets the right answer automatically or by lucky cross-referencing back to a different lesson's prose.

---

## Section 4: Resolving the Burns/Volcker Fork

Lesson 126, Section 3, posed a genuine ambiguity: a "leaner Fed" with less forward guidance could signal Volcker-style confidence (an institution secure enough in its independence to stop performing transparency theater) or could signal evasion (an institution avoiding a fiscal-dominance admission it can't make explicitly). The lesson specified two observable proxies to disambiguate: withheld dot + named driver = the strongest available confirmation of the *confident* read, because evasion-style minimalism would withhold both the dot *and* any specific causal admission, leaving markets with nothing concrete at all.

That is exactly what happened, in the stronger direction: Warsh withheld his dot **and** specifically named tariff pass-through as a forward inflation pressure, in addition to citing accelerating PPI and robust wage growth. That is substantive, falsifiable content delivered in a terse package — not silence dressed up as discipline. The combination reads as Volcker-style confidence: an institution willing to say a specific, uncomfortable thing (tariffs are inflationary, full stop) without padding it in qualifiers, while declining to play the dot-plot guessing game it considers performative. The fiscal dominance thesis underlying Position 12 gets a real, named data point in its favor today — not a strong one (this is one meeting, and the thesis was never staked on any single meeting), but a directionally correct one.

---

## Section 5: Closing the Loop on the G7 Évian Follow-Up

Lesson 126 also flagged a second open item: whether the G7 Évian summit (which closed June 17) produced a final communiqué on the rare earths secretariat dispute raised in the June 16 weekly briefing.

**Outcome:** The G7 did not produce France's proposed permanent Critical Minerals Secretariat — the US held its position from June 15 and blocked it, preferring bilateral deals over a standing multilateral body. But the summit did produce something arguably more investable: a **Leaders' Declaration on critical minerals**, committing the G7 to ensuring no single country supplies more than 60% of their rare earth and permanent-magnet imports by 2030, tightening toward 50% over time, plus the formal launch of a **Critical Minerals Resilience and Production Alliance** — a coordination platform for emergency response, supply chain intelligence sharing, and market monitoring. Rather than one comprehensive joint communiqué, the G7 opted for area-specific outcome documents.

**Read for the portfolio:** this is a SIGNAL, not noise, and the institutional fracture (no secretariat) is close to irrelevant to the investment thesis. The thesis on Western rare-earth producers (MP Materials, Lynas) was never about whether a Geneva-style secretariat exists — it was about whether G7 governments commit to numeric de-China-ification targets with teeth. A 60%-by-2030 ceiling, formally declared by all G7 members, is a harder commitment than a secretariat would have been. This reinforces the existing critical-minerals thesis language from the June 16 weekly briefing without requiring any new position — the structural long (currently expressed in the portfolio via the broader copper/critical-minerals position, COPX/SCCO/FCX) gets a confirming data point. A rare-earth-specific instrument (MP Materials, Lynas) remains a candidate for the next dedicated portfolio review, not a same-session addition — new positions don't get opened inside a grading exercise.

---

## Key Concepts Covered

- Executing a pre-committed decision protocol against real, messy data — and discovering that the data fit the categories cleanly while the *code* almost mis-scored it anyway
- The distinction between a rule's prose specification and its implementation — and why naming a variable for your leading hypothesis instead of the general principle creates a silent narrowing that can flip a downstream decision
- Resolving genuine interpretive ambiguity (Burns/Volcker fork) using pre-specified observable proxies rather than post-hoc narrative
- The cost of a missed pre-registration: a calibration exercise that can't be done retroactively, demonstrated rather than just asserted
- G7 institutional fracture (no secretariat) vs. substantive multilateral commitment (60%/2030 target) as two different things that get conflated in headline-level reporting

---

## Investment Implications

| Position | Pre-Committed Rule Applied | Actual Outcome | Action |
|---|---|---|---|
| **P-10 — EM Tail Hedge** | Hawkish → hold 2–3% | 2Y yield +16bps, dot plot 0 cuts → HAWKISH | **HOLD.** No sizing change. |
| **P-12 — Long TIPS** | Driver named + dot withheld → thesis confirmed | Dot withheld; tariff pass-through named explicitly as inflation driver | **NO ACTION — thesis CONFIRMED.** Logged as a positive data point for the rolling Conviction Score Engine (Layer 3.5), not a position change. |
| **Critical minerals (existing long)** | N/A — informational follow-up from L126 | G7 declared 60%-by-2030 / 50%-later rare-earth concentration ceiling; no secretariat | **No change.** Thesis reinforced; rare-earth-specific instrument (MP Materials/Lynas) remains a candidate for next portfolio review, not opened today. |

Investment log updated: the Long TIPS (2026-05-30) and EM Tail Hedge (2026-05-11) entries in `reports/investment_log.md` now carry a June 17/18 FOMC-grading note reflecting the above.

---

## Databricks Angle

This is event #1 for the `prospectra.portfolio.fomc_signal_log` table specified in Lesson 126. Here is the actual row to insert:

| meeting_date | personal_dot_submitted | fiscal_driver_named | fiscal_driver_type | two_year_yield_change_bps | dot_plot_2026_cuts | signal | p10_action | p12_action |
|---|---|---|---|---|---|---|---|---|
| 2026-06-17 | FALSE | TRUE | tariff_passthrough | +16 | 0 | HAWKISH | HOLD | NO_ACTION_CONFIRMED |

Two build notes for Bolo, both surfaced by today's grading exercise rather than planned in advance:

1. **Rename the field before the next insert.** `mentions_defense_spending_inflation` in the Lesson 126 spec should become `fiscal_driver_named` with a companion `fiscal_driver_type` enum (`defense_spending`, `tariff_passthrough`, `none`) — exactly as modeled in the table above. This makes Section 3's near-miss structurally impossible to repeat: the schema now forces you to record *which* driver fired, not just a boolean keyed to one hypothesis.
2. **Add a `prediction_log` companion table** keyed to lesson number, capturing pre-registered predictions (like the one Bolo was asked for and didn't submit) with a timestamp *before* the event resolves. If it isn't in a table with a pre-event timestamp, it isn't a real calibration exercise — it's a story told after the fact. This closes the gap from the CEO Note above structurally rather than relying on Bolo remembering to reply to an email.

---

## Reflection Questions

1. **The naming-gap question:** Section 3 showed that a narrowly-named code variable almost produced the wrong classification despite the prose specification being correct. Pick any other kill-switch rule from Lesson 124 (Positions 1–13) and check: does its variable name cover every condition its prose description allows for, or is there a similar narrowing hiding in it?

2. **The missed pre-registration:** No prediction was on file for grading this session. Is the right fix a process fix (set a calendar reminder, reply to the lesson email before 2:30 PM ET) or a structural fix (the Databricks `prediction_log` table from the Databricks Angle, which doesn't depend on remembering to email anyone)? Defend your answer in terms of what actually fails first under time pressure.

3. **Confirmation vs. conviction:** Position 12's thesis was "confirmed" today, but Section 4 was careful to call it directionally correct, not strong, because it's one meeting. What is the minimum number of FOMC cycles — each independently confirming the fiscal-dominance read the way today's did — before "confirmed-but-weak" should become "confirmed-and-strong" in the Conviction Score Engine? Name the number and justify it.

---

## Questions for Next Session

The Warsh protocol has now been built, executed, and audited once. The next scheduled binary catalyst on the calendar is the **Section 122 tariff cliff on July 24** — the expiration of the 150-day window on 15% surcharges flagged in the June 16 weekly briefing, with direct exposure for the European industrials underweight position and the USD/EUR call.

**Next session: Lesson 128 — Pre-Committing the July 24 Tariff Cliff Read, Before the Headlines Start.**

We will apply the same discipline used today — build the interpretation protocol and the decision matrix in calm conditions, five weeks ahead of the event, rather than reacting to it — to the binary tariff-cliff outcome (snap-back vs. extension vs. partial framework deal) and its effect on the European industrials underweight, USD/EUR, and the defense/critical-minerals longs.

Preview question: *Section 122's surcharge either snaps back, gets extended, or gets replaced by a negotiated framework. Which of those three outcomes is the market currently pricing as base case — and what is the specific, falsifiable signal that would tell you that pricing is wrong before July 24 arrives?*

---

## Sources Referenced

- [Here are the five big takeaways from Kevin Warsh's first meeting as Fed chairman — CNBC](https://www.cnbc.com/2026/06/17/here-are-the-five-big-takeaways-from-kevin-warshs-first-meeting-as-fed-chairman.html)
- [Fed interest rate decision June 2026 — CNBC](https://www.cnbc.com/2026/06/17/fed-interest-rate-decision-june-2026.html)
- [Fed Chair Warsh to withhold dot plot from outlook in first FOMC meeting — CryptoBriefing](https://cryptobriefing.com/fed-chair-warsh-dot-plot-outlook/)
- [Fed 'dot plot': Almost half of FOMC members project at least one interest rate hike this year — Yahoo Finance](https://finance.yahoo.com/economy/policy/article/fed-dot-plot-almost-half-of-fomc-members-project-at-least-one-interest-rate-hike-this-year-183645064.html)
- [June Fed Decision Delivered: Rates Held Unchanged but Dot Plot Significantly Raised — TradingKey](https://www.tradingkey.com/analysis/economic/central-banks/261973912-fed-federal-fomc-2-economic-projections-decision-rates-tradingkey)
- [2-year Treasury yield rockets higher as many Fed officials signal possible hike this year — CNBC](https://www.cnbc.com/amp/2026/06/17/treasury-yields-investors-await-warsh-fed-decision.html)
- [Fed leaves interest rates unchanged but signals higher rates are ahead — CNN Business](https://www.cnn.com/2026/06/17/business/live-news/federal-reserve-interest-rate-kevin-warsh)
- [Federal Reserve holds interest rates steady and hints at rate hike later this year — NPR](https://www.npr.org/2026/06/17/nx-s1-5860084/fed-chief-warsh-first-fomc-meeting)
- [Chairman Warsh's Press Conference, June 17, 2026 (transcript) — Federal Reserve](https://www.federalreserve.gov/mediacenter/files/FOMCpresconf20260617.pdf)
- [G7 Aims to See China Supply No More Than 60% of Rare Earths — Bloomberg](https://www.bloomberg.com/news/articles/2026-06-17/g7-aims-to-ensure-china-supplies-no-more-than-60-of-rare-earths)
- [G7 leaders' declaration on securing supply chains for critical minerals — G7 Évian 2026](https://www.elysee.fr/en/G7evian/2026/06/17/g7-leaders-declaration-on-securing-supply-chains-for-critical-minerals)
- [G7 establishes critical minerals alliance and crisis platform to counter China dependency — CryptoBriefing](https://cryptobriefing.com/g7-critical-minerals-alliance-platform/)

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson delivered: 2026-06-18 | Next lesson: #128 — Pre-Committing the July 24 Tariff Cliff Read*
