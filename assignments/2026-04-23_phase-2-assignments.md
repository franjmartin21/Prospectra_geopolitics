# Assignments — April 23, 2026
*Issued after: Full curriculum completion (12/12 lessons delivered)*

---

## Priority 1 — URGENT: Clear the Quiz Backlog

**The LEARN track has 0 XP. 12 lessons delivered, zero quizzes passed. This is the most important thing to fix.**

| Task | Action | Target |
|---|---|---|
| L-01 Quiz | Run `/quiz` — answer 4/5 correctly to close the quest | This session |
| L-02 Quiz | Run `/quiz` for Geography as Destiny | Next session |
| Continue through L-12 | 2 quizzes per session until cleared | By May 1 |

---

## Priority 2 — Databricks Phase 1 Completion (CRITICAL PATH)

Phase 1 was due at end of Week 3 (approx. May 2). B-01 is done. Three pipelines remain.

| Pipeline | Spec | Target Date | Status |
|---|---|---|---|
| **B-02: Market Data Feed** | Yahoo Finance / FRED → daily prices for target asset classes (Brent crude, gold, EUR/USD, EM equity indices, copper, defense ETFs). Delta Lake table. | April 27 | NOT STARTED |
| **B-03: News Sentiment Pipeline** | GDELT GKG → sentiment scores by theme and geography. Key themes: energy, sanctions, trade, military. 30-day rolling index. | May 1 | NOT STARTED |
| **B-04: Correlation Engine** | Event signal (GDELT) + sentiment (GKG) → asset price lag analysis. Output: correlation matrix + signal lead/lag table. | May 3 | NOT STARTED |

**B-02 unblocks B-04. B-03 unblocks full Phase 2. Build in order.**

Databricks specs directory: `/databricks/specs/` — CEO will write the B-02 spec as the next Databricks session task.

---

## Priority 3 — Copper Research (Before Opening Investment Position)

The copper thesis was flagged in the Investment Log (Apr 23) as a candidate but not yet open. Before formally opening:

1. Build B-02 with copper spot price (HG=F or COPX ETF) included in Market Data Feed
2. Run a correlation analysis: GDELT conflict/mining events in Chile/Peru vs. copper price
3. Review supply pipeline: Cobre Panama (closed 2023), Quebrada Blanca ramp, Congo DRC risk
4. Confirm demand-side: EV adoption curve, grid infrastructure spending (IRA allocations)

**Target to open the position: after B-02 is live and at least one correlation analysis is run.**

---

## Ongoing — Reading (Carry-Forward from April 4)

| Book | Assignment | Status |
|---|---|---|
| Mearsheimer — *Tragedy of Great Power Politics* | Chapters 1–3 | Pending |
| Dalio — *Principles for Dealing with the Changing World Order* | Full book | Ongoing |
| Keohane & Nye — *Power and Interdependence* | Chapter 1 | Pending |

---

## Reflection Questions — Carry-Forward (From April 4, L-01)

These were never formally answered. Bring answers to next CEO check-in:

1. US-China: which framework (realist, liberal, constructivist) has the most predictive power for the next 5 years — and what does your answer imply for your portfolio?
2. At what specific threshold would you conclude the liberal international order is no longer valid for pricing risk? What changes in your portfolio on that day?
3. Saudi Arabia runs simultaneous relationships with the US, China, and Russia. Which framework best describes Saudi behavior — and what does it tell you about where the petrodollar system goes?

---

## Accountability Check

Reply to this session's briefing email by **Sunday April 27** with:
- L-01 and L-02 quizzes — passed or attempted?
- B-02 status — started or done?
- Reflection questions — answers or reasons they're still pending

The 3-month clock runs to July 4. We are 19 days in. We are on track on knowledge delivery and investment thesis. We are behind on Databricks and XP validation. Catch-up window is this week.
