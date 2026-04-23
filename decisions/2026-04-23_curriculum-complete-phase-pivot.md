# Decision — Curriculum Phase Complete: Pivot to Consolidation & Build

**Date:** April 23, 2026
**Trigger:** All 12 lessons delivered as of this session. First full curriculum pass complete.

---

## Decision

The project pivots from lesson-delivery mode to consolidation-and-build mode. The next phase has three parallel tracks:

1. **Quiz clearance** — work through all 12 lesson quizzes to earn LEARN XP and validate actual comprehension (not just delivery).
2. **Databricks catch-up** — complete B-02, B-03, and B-04 before the end of Phase 1 (target: May 3).
3. **Selective deep dives** — the CEO will trigger `/deepdive` sessions for topics connected to live geopolitical events, replacing the daily lesson slot now that the curriculum is done.

---

## Reasoning

**Why pivot now?**
The 12-topic curriculum was designed to build the foundational framework. It has been delivered in 19 days — aggressive but appropriate given the 3-month deadline. However, delivery without retention is not learning. The quiz track exists precisely to enforce this. Zero LEARN XP after 12 lessons is a problem that must be corrected.

**Why is Databricks urgent?**
Phase 1 (Weeks 1–3) was supposed to have all four foundation pipelines running. We are in Week 3 and only B-01 is live. B-02 (Market Data Feed) is the highest priority — without it, the Correlation Engine (B-04) cannot be built, and the entire Phase 2 intelligence layer is blocked.

**Alternatives considered:**
- Continue delivering more lessons / advancing curriculum — rejected. The framework is in place. More theory without retention or data infrastructure doesn't compound. 
- Begin Phase 2 pipelines now — rejected. Phase 1 must be complete first. The correlation engine requires both event data (GDELT, done) and market data (Yahoo/FRED, not done).

---

## Implications

- No new lessons until L-01 quiz is passed.
- Weekly briefings continue unchanged (Mondays).
- Deep dives triggered by the CEO on live geopolitical events — not on a fixed schedule.
- Copper thesis candidate (Investment Log, Apr 23) should be formally opened after GDELT copper-event correlation analysis is run in Databricks — this is a B-02/B-03 dependency.

---

## Owner

- **Quiz track:** Bolo (run `/quiz` each session)
- **B-02 Market Data Feed:** Bolo (target: by April 27)
- **B-03 News Sentiment Pipeline:** Bolo (target: by May 1)
- **B-04 Correlation Engine:** Bolo (target: by May 3)
- **Deep dive triggers:** CEO-initiated based on weekly briefing events
