# Lesson 152: The Databricks Build Review — CEO Audit, Gap Analysis, and Reboot

**Date:** 2026-07-06
**Session Type:** Daily Lesson — CEO Operational Review
**Lesson Number:** 152
**Topic:** Honest Assessment of the Databricks Build at the 3-Month Mark
**Preceding Arc:** Lesson 150 (Full Framework Synthesis), Lesson 151 (Tail Risk Stress Test)

---

## Opening Question

> The 3-month project deadline was July 4, 2026. It passed two days ago.
>
> The original commitment, stated in PROJECT_FOUNDATION.md: *"By July 2026 — GDELT + market data pipeline live in Databricks; Geopolitical Risk Index producing scores for 10+ countries; Investment thesis documented with 6+ months of tracked recommendations."*
>
> Here is the question: **How much of that did we actually deliver?**
>
> Not what was learned. Not what was analyzed. What was *built*, *committed*, and *running* in a production Databricks environment — as of today?
>
> Before answering, resist the temptation to conflate intellectual work with deployed infrastructure. A spec is not a pipeline. A lesson that describes a Databricks architecture is not a Databricks architecture. The market does not give credit for lesson notes. It gives credit for running systems that produce actionable signals.
>
> This lesson is the honest audit. It will be uncomfortable. That is the point.

---

## I. The 3-Month Scorecard — What Was Promised vs. What Was Built

The project committed to three goals by July 2026. Let us grade them explicitly.

---

### GOAL 1: LEARN — Build Framework-Level Understanding

**Commitment:** 12-lesson curriculum delivered and internalized.

**What actually happened:**

The 12-topic curriculum was fully delivered by April 23, 2026 — in the first 19 days of the project. Then the curriculum kept going. 140 additional lessons were delivered through July 6, covering every major topic in geopolitics, international finance, crisis economics, monetary architecture, and investment framework construction. The final three lessons (148–151) produced a full five-layer investment framework synthesized from 148 lessons of groundwork.

**Grade: A — and then some.**

The learning goal was not just met; it was exceeded by an order of magnitude. The curriculum that was supposed to take 12 sessions and 3 weeks ran to 151 sessions over 13 weeks and produced a more sophisticated analytical framework than the original scope envisioned.

**The honest caveat:** This surplus of learning is part of what consumed the bandwidth that was supposed to go into building. More on that shortly.

**PROGRESS.md status:** 0 quizzes passed. 0 LEARN XP earned. This is the single most embarrassing gap in the scoreboard. 152 lessons delivered. Zero formally verified. The knowledge exists — the accountability mechanism for verifying it does not. Francisco (Bolo) needs to run `/quiz` for Lessons 1 through 12 to begin clearing this backlog.

---

### GOAL 2: INVEST — Build a Systematic Investment Process

**Commitment:** Investment thesis documented with 6+ months of tracked recommendations.

**What actually happened:**

The investment log (`reports/investment_log.md`) is among the most detailed outputs of the entire project. As of July 6, 2026, it contains **10 active or formally logged positions**, all opened between April 4 and June 16, 2026:

| Position | Opened | Current Status | Conviction |
|---|---|---|---|
| Long energy (XOM, CVX, LNG) | Apr 4 | HOLD — kill switch not triggered | MEDIUM |
| Long gold | Apr 4 | HOLD — kill switch not triggered | HIGH |
| Long European defense (Rheinmetall, BAES) | Apr 4 | HOLD | VERY HIGH |
| Long Brazilian agribusiness (AGRO3, SLC) | Apr 4 | HOLD | VERY HIGH |
| Long copper (COPX, SCCO, FCX) | Apr 24 | HOLD | HIGH |
| Long uranium (URA, CCJ, NXE) | May 11 | HOLD | HIGH |
| Long LNG infrastructure (Cheniere) | May 11 | HOLD | HIGH |
| Tail hedge — EM fixed income | May 11 | HOLD — 2-3% position | TAIL HEDGE |
| Long India (INDA) | May 30 | HOLD — Tranche 1 (4%) | MEDIUM-HIGH |
| Long TIPS (TIP) | May 30 | HOLD | MEDIUM-HIGH |
| Underweight EM energy importers (TUR, EWY) | May 30 | HOLD — 6-week clock running | MEDIUM |
| Long tankers (FRO, STNG, DHT) | Jun 16 | HOLD | MEDIUM |

Every position was opened with an explicit thesis, falsification trigger, and time horizon. The Hormuz crisis produced real-time application of the framework over 30+ lessons, tracking the evolution of a live geopolitical event from initial disruption through MOU signing, re-escalation, Lebanese complication, Bahrain domain shift, and partial normalization.

**Grade: B+.**

The investment process exists, is active, and is generating real analytical output. The gap: no positions have resolved (all opened within 3 months; the minimum horizon is 6–18 months — this is correct by design). The INTEL track on the scoreboard shows 0 XP because resolutions take time. This is not a failure — it is the expected state at 3 months for a long-horizon investor. The track record will be auditable by October 2026 on the earliest-opened positions.

The remaining gaps: (1) The Lesson 151 positions — reduced EM high-yield duration, cash reserve for EM entry, TSMC put spread — need to be formally added to the investment log. (2) The FRED/Yahoo Finance data that was supposed to automate falsification-trigger monitoring is not running. Positions are being monitored manually through research sessions. This is sustainable for 10 positions; it becomes unsustainable at 20+.

---

### GOAL 3: BUILD — Databricks Analytical Platform Live

**Commitment:** GDELT + market data pipeline live; Geopolitical Risk Index producing scores for 10+ countries; Phase 1 complete.

**What actually happened:**

This is the honest part. Here is the complete build status as of July 6, 2026:

| Pipeline | Phase | Status | Notes |
|---|---|---|---|
| **B-01: GDELT Event Feed** | Phase 1 | **COMPLETED ✓** | Deployed via DAB (commit ff4818a). Bronze → Silver → Gold. Daily at 06:00 UTC. Country-pair sentiment z-scores running. |
| **B-02: Market Data Feed** | Phase 1 | **NOT STARTED** | Full spec written April 24. Build never executed. |
| **B-03: News Sentiment (GDELT GKG)** | Phase 1 | **NOT STARTED** | Blocked by B-02. |
| **B-04: Correlation Engine** | Phase 1 | **NOT STARTED** | Blocked by B-02. |
| **B-05: Geopolitical Risk Index** | Phase 2 | **LOCKED** | Spec written (June 2026). Requires Phase 1 complete. |
| **B-06: Commodity Pressure Model** | Phase 2 | **LOCKED** | Requires Phase 1 complete. |
| **B-07: Regime Change Detector** | Phase 2 | **LOCKED** | Requires Phase 1 complete. |
| **B-08: Investment Signal Generator** | Phase 2 | **LOCKED** | Requires Phase 1 complete. |

**Phase 1 completion rate: 1 of 4 pipelines (25%).**

**Grade: D.**

B-01 is well-built, well-specified, and running. The GDELT pipeline is production-quality infrastructure. But B-02 — the Market Data Feed — was declared urgent on April 24 with a hard deadline of April 27. That deadline was missed by 10 weeks. Every subsequent pipeline (B-03, B-04, the entire Phase 2 intelligence layer) is blocked behind it.

The spec for B-02 exists. It is complete. Every notebook is fully written out in `reports/market_analysis/2026-04-24_databricks-session-B02-market-data-feed.md`. The code is ready to copy into Databricks and run. This is not a design problem or an ambiguity problem. It is an execution problem.

---

## II. The Root Cause Analysis — Why the Build Stalled

The project has a structural imbalance: **the learning function crowded out the building function.**

This is not a criticism of the learning quality — the lessons were excellent. It is a statement about the operating rhythm:

- **151 lessons delivered** in 94 days = 1.6 lessons per day on average
- **1 pipeline deployed** in 94 days = 0.01 pipelines per day on average

Every 6am session defaulted to a new lesson. The Hormuz crisis generated a legitimate burst of daily analytical sessions from June 16 through July 5 (Lessons 125–151 over 20 days). But before the crisis, between April and June, the build sessions that were specified as required were skipped in favor of additional curriculum topics.

**The operating rhythm failure:**

The PROJECT_FOUNDATION.md specified: *"Every 1–2 days: lesson. Weekly: Databricks build session via `/databricks`."*

The actual operating rhythm: 151 lessons. 0 Databricks build sessions after April 24. The CEO did not enforce the weekly build cadence.

**The second cause — spec inflation without execution:**

The June 2 Databricks spec (`2026-06-02_regime_classifier_pipeline.md`) is a sophisticated design for the Regime Classifier. It was written and committed while B-02 was still unbuilt. Writing new specs for Phase 2 when Phase 1 is incomplete is a form of intellectual progress that does not deliver working infrastructure.

The lesson: **A spec is a liability until it is deployed. An undeployed spec represents work that must still be done, complexity that must be maintained, and a commitment that will someday be called due.** Specifying ahead of building is fine in moderation. Three Phase 2 specs with zero Phase 1 pipelines completed is a planning problem.

---

## III. The Reboot Plan — What Happens Now

The 3-month deadline is not an ending condition. It was a milestone. The project continues. The question is what changes.

**Change 1: B-02 gets built in the next Databricks session. No exceptions.**

The B-02 spec is complete. Every notebook is written. The only remaining action is to open Databricks, create the `prospectra.market_data` schema, and run the four notebooks in sequence. This should take 2–3 hours. It was supposed to happen April 27. It needs to happen within the next 7 days.

**Bolo's immediate action:** Run B-02 per the April 24 spec. Step-by-step:
1. Create Unity Catalog schema: `prospectra.market_data` (one SQL cell)
2. Run `01_ingest_yahoo_finance.py` — verify >15,000 rows, all 19 tickers present
3. Run `02_ingest_fred_api.py` — verify >12 series, >300 observations each
4. Run `03_transform_silver_market_data.py` — unified time series with metadata
5. Run `04_position_alerts.py` — backtest: confirm energy alert would have fired April 20 at $87/bbl
6. Schedule daily jobs: Yahoo at 6pm ET, FRED at 7pm ET
7. Commit to `databricks/` and message CEO with git commit hash

The code is already written. This is a copy-paste-and-run exercise.

**Change 2: The PROGRESS.md scoreboard must be activated.**

The LEARN track has 152 lessons delivered and 0 quizzes completed. The scoreboard only awards XP on quiz completion — this was designed correctly. The backlog needs to start clearing. Target: 2 quizzes per session until L-01 through L-12 are cleared. Run `/quiz` next session.

**Change 3: The operating rhythm resets to its original design.**

| Session Type | Cadence | What Happens |
|---|---|---|
| Morning lesson | Every 1–2 days | Continue at current depth |
| **Databricks build session** | **Every week minimum** | **Actually happens now — not just specified** |
| Portfolio review | Bi-weekly | Review investment log; log any new positions |
| Framework audit | Monthly | Audit the investment calls against reality |

The CEO takes direct accountability for enforcing the build cadence. The next 12 weeks are Phase 2. The learning is substantially complete. The build is where the intellectual work converts into analytical infrastructure.

**Change 4: Resolve the Lesson 151 position additions.**

The following positions identified in Lesson 151 need to be added to the investment log:
1. **Reduce EM high-yield duration** — below neutral vs. EM benchmark; structural pre-positioning for Tail Risk 3
2. **Cash reserve 3–5% earmarked for EM entry** — hold in T-bills; deploy when EMBI+ >500bps
3. **TSMC put spread, 0.5% portfolio** — 12-month puts, 25–30% OTM, rolling annually

CEO will add these in the next portfolio review session.

---

## IV. The Build Roadmap — Next 12 Weeks

The revised build plan, accounting for the 10-week Phase 1 delay:

### Weeks 1–2 (July 7–20)
**Goal: Complete Phase 1**

| Pipeline | Who | Deadline | Deliverable |
|---|---|---|---|
| B-02: Market Data Feed | Bolo | July 13 | All 4 notebooks running; daily job scheduled; commit to `databricks/` |
| B-03: News Sentiment (GDELT GKG) | Bolo | July 20 | GKG sentiment pipeline; daily sentiment scores by theme and geography |

B-03 uses the same GDELT source as B-01 but ingests the Global Knowledge Graph (GKG) instead of the core events table. The architecture is identical to B-01 — Bronze/Silver/Gold, DABS deployment. CEO will write the spec if not already started.

### Weeks 3–4 (July 21 – August 3)
**Goal: Complete B-04 and open Phase 2**

| Pipeline | Who | Deadline | Deliverable |
|---|---|---|---|
| B-04: Correlation Engine | Bolo + CEO | August 3 | GDELT event counts × Brent price cross-correlation with 0–10d lag analysis; first investable signal documented |

B-04 is the validation moment for the entire intelligence thesis. If GDELT Iran conflict event counts show a measurable lead correlation with Brent price changes at any lag from 1–5 days, the platform has produced its first genuine signal. If not, that is equally important information — it means the event-based signal requires different data or a different construction.

**First correlation hypothesis:** GDELT daily Iran conflict event count for pair `US_RU` and `SA_US` predicts Brent crude price changes at a 1–3 day lag. Test period: January–July 2026. Threshold: |r| > 0.30 at any single lag. If confirmed, this becomes the first formally validated geopolitical investment signal in the Databricks platform.

### Weeks 5–8 (August 4–31)
**Goal: Phase 2 intelligence layer**

| Pipeline | Who | Deadline | Deliverable |
|---|---|---|---|
| B-05: Geopolitical Risk Index | CEO directs, Bolo builds | August 17 | Composite country risk scores for 10+ countries; daily output |
| B-06: Commodity Pressure Model | CEO directs, Bolo builds | August 31 | Multi-factor Brent and copper pressure score; supply disruption risk |

The B-05 Geopolitical Risk Index was specified in the June 2 spec. This is the platform's first genuine intelligence product — not raw data, not normalized time series, but a synthesized risk score that translates geopolitical event data into a single comparable metric across countries.

**B-05 target output:**
```python
# Output table: geopolitics.intelligence.country_risk_daily
# Columns: date, country_iso, risk_score (0–100), risk_tier (LOW/MEDIUM/HIGH/CRISIS)
# risk_score composition:
#   0.35 × gdelt_conflict_z_score (from B-01)
#   0.25 × news_sentiment_negativity (from B-03)
#   0.20 × macro_stress_index (from B-02: FX volatility, HY spreads)
#   0.20 × manual_event_flags (CEO-logged structural events)
# Countries: US, CN, RU, IR, DE, FR, UA, SA, IN, BR, TW, IL
```

### Weeks 9–12 (September 1–28)
**Goal: Signal generation and platform packaging**

| Pipeline | Who | Deadline | Deliverable |
|---|---|---|---|
| B-07: Regime Change Detector | CEO directs, Bolo builds | Sep 14 | Regime classifier live with 4-state output |
| B-08: Investment Signal Generator | CEO directs, Bolo builds | Sep 28 | End-to-end signal table: geopolitical event → asset class tilt |
| Databricks AI/BI Dashboards | Bolo | Sep 28 | Visualizations for Bolo's daily use |

B-08 is the project's final deliverable — the Investment Signal Generator that runs the five-layer framework as a rule-based pipeline. It is the Databricks operationalization of everything built in the 152-lesson curriculum. If it works, the platform produces weekly asset class recommendations without manual analysis. If it doesn't, we have 12 weeks of evidence about why — which is also a product specification for Version 2.

---

## V. The Tail Risk Pipelines — Lesson 151 Integration

Lesson 151 specified three tail risk monitor pipelines that extend the existing architecture. These are **not** new Phase 1 pipelines — they are extensions of B-02 and B-05 that can be built once the base infrastructure is running.

**Priority order (per Lesson 151 Reflection Question 3):**

| Rank | Pipeline | Rationale |
|---|---|---|
| 1 | **Dollar Sudden Stop Monitor** | ACM term premium (FRED) and TIC data are already in B-02's spec. This is incremental: add two derived metrics to the existing FRED ingestion, and build a composite score from data already flowing. Monitoring frequency: daily. Time from output to signal: immediate. Portfolio exposure: the short-TLT and long-gold positions together represent the most capital at risk. |
| 2 | **EM Debt Cascade Monitor** | EMBI+ spread and IMF watch data are achievable via B-02 additions and GDELT keyword filtering (already in B-01/B-03). Monitoring frequency: daily. Key signal: EMBI+ threshold crossing is a hard decision rule (when to deploy the 3–5% cash reserve). |
| 3 | **Taiwan Black Swan Monitor** | AIS maritime data is the novel addition — it requires a new data source (MarineTraffic or VesselFinder API) not currently in scope. Build this last, after core infrastructure is stable. |

---

## VI. The Investment Log Discipline — What the Platform Must Automate

The investment log currently contains 12 positions tracked manually through research sessions. Each position has:
- An entry thesis
- A falsification trigger
- A time horizon
- Manual updates as events evolve

The Databricks platform's Job 1 — before signals, before regime classification, before anything — is to **automate falsification trigger monitoring for each active position.** This is what B-02/B-04 were supposed to deliver by April 27.

**The positions and their automated monitoring requirements:**

| Position | Falsification Trigger | Data Required | B-02 Coverage |
|---|---|---|---|
| Long energy | Brent <$80 sustained + 3 weekly closes | `DCOILBRENTEU` | ✓ In spec |
| Long gold | TIPS real yield >3% sustained 60d AND Brent <$75 | `T10YIE`, `DCOILBRENTEU` | ✓ In spec |
| Long EU defense | NATO burden-sharing reversed + EU defense budget cut | GDELT + manual flag | Partial (B-01 + manual) |
| Long Brazilian agri | US-China agri trade restored | GDELT trade events | B-01 partial |
| Long copper | 3 monthly closes below $9,500/mt | Copper spot | Not yet in spec — add to B-02 |
| Long uranium | Uranium spot below $55/lb × 3 months | Uranium spot (add to B-02) | Not yet in spec |
| Long LNG infra | Iran deal + Qatar full exports | GDELT + manual | B-01 partial |
| EM tail hedge | BOJ meeting dates + yen/EMB correlation | `EURUSD=X` proxy + BOJ dates | Partial |
| Long India (INDA) | India-Pakistan war escalation | GDELT + manual | B-01 partial |
| Long TIPS | CPI <2.5% × 3 months + defense below 3% GDP | `CPIAUCSL` | ✓ In spec |
| Short EM importers | Brent <$80 sustained 6 weeks | `DCOILBRENTEU` | ✓ In spec |
| Long tankers | P&I club resumes Hormuz war-risk coverage | Manual + Lloyd's feed | Manual only |

The additions not yet in B-02's spec:
- **Copper spot price** (LME or proxy: `HG=F` futures)
- **Uranium spot** (UXC or proxy: `URA` price × adjustment)
- **BOJ meeting dates** (calendar import — 8 meetings per year)
- **EMBI+ spread** (JP Morgan; available via FRED as `BAMLH0A0HYM2` proxy or direct Bloomberg)

**CEO action:** Update the B-02 spec to include these four additions before Bolo builds.

---

## VII. Key Concepts — Lesson 152

- **Spec is a liability until deployed:** An unbuilt spec represents future work, not current progress. Multiple Phase 2 specs written while Phase 1 is incomplete is planning without execution.
- **Learning-building imbalance:** The most common failure mode in analytical infrastructure projects is that intellectual work (frameworks, analysis, writing) crowds out execution work (building, testing, deploying). This project fell into that pattern.
- **Phase gates matter:** Phase 2 intelligence cannot run without Phase 1 data. Unlocking B-05 requires B-02, B-03, and B-04 to be running in production. No architectural cleverness substitutes for the base layer being live.
- **Falsification trigger automation is the MVP:** Before signals, before regime classification, before dashboards — the first value the Databricks platform delivers is automated monitoring of the 12 active position kill conditions. This is why B-02 was urgent on April 24 and remains urgent on July 6.
- **The 3-month mark is a reset, not a terminus:** Project deadlines in early-stage analytical projects function as checkpoints, not completion events. The question at the deadline is not "did we deliver everything?" but "where are we, what changed, and what does the next 12 weeks look like?" Honest assessment is more valuable than optimistic spin.

---

## VIII. Reflection Questions

1. **The Accountability Question:** The B-02 spec was written on April 24 with a hard deadline of April 27. It is now July 6 — 10 weeks later. The spec is unchanged. What was the actual constraint? Was it technical difficulty, time availability, competing priorities, or something else? Being honest about the root cause determines whether the new July 13 deadline is credible. The CEO cannot force the answer — but the answer matters for whether the Reboot Plan sticks.

2. **The Data Infrastructure Question:** If you could build only one pipeline in the next 7 days — B-02 (Market Data Feed) or B-05 (Geopolitical Risk Index) — which would you choose and why? The correct answer is B-02, because B-05 is locked behind it. But argue the case explicitly: what capability does the platform gain from each, and which capability gap is costing the project the most right now?

3. **The Signal Validation Question:** Once B-02 and B-04 are running, the first question is: does GDELT event data actually lead Brent crude price changes at a 1–5 day lag? Design the test you would run. Specify the exact data pull, the correlation metric, the threshold for "signal found," and the interpretation framework for each outcome: (a) correlation found above 0.3, (b) correlation found 0.1–0.3, (c) no correlation found. What does each outcome imply for the platform's design?

---

## IX. Investment Implications — Lesson 152

The Databricks build review does not change the existing portfolio positions — all falsification triggers remain unmet. But it adds one new decision:

**The tankers monitoring gap is now a formal directive.** Lesson 138 escalated the FRO/STNG/DHT price monitoring to a Databricks task. That task is still outstanding. B-02's first priority after the base spec is live is to add FRO, STNG, and DHT as covered tickers so the tanker thesis can be monitored systematically rather than through manual research sessions.

**New positions to add to investment log (from Lesson 151):**

| Position | Instrument | Size | Horizon | Falsification |
|---|---|---|---|---|
| Reduce EM high-yield duration | Underweight EMHYLD vs. EM IG | Reduce 2–3% | Structural | US 10Y yield <3.5% sustained AND EM current accounts improve 3+ quarters |
| Cash reserve — EM entry | T-bills, earmarked | 3–5% | Hold until EMBI+ >500bps | EMBI+ tightens to <300bps (no crisis entry point) |
| TSMC put spread | 12-month puts, 25–30% OTM | 0.5% | Rolling 12-month | Cross-Strait talks with credible de-escalation framework + PLA exercise reduction |

**Revised Portfolio Summary — July 6, 2026:**

Unchanged from Lesson 151. All existing positions hold. Three new positions (above) to be formally logged in investment_log.md.

---

## X. CEO's Note — Lesson 152

This was the hardest lesson to write.

It would have been easier to turn Lesson 152 into another content-rich exploration of a new topic — the regulatory architecture of derivative markets, or the geopolitics of debt restructuring in frontier markets, or perhaps a deep dive on the Bank for International Settlements. All legitimate. All useful. And all of them would have been a choice to continue doing what the project does well (learn) while avoiding what it has not done (build).

The scoreboard is unambiguous:
- **LEARN XP: 0 / 1,320** (quizzes unrun — the only gating mechanism)
- **INTEL XP: 0 / ~1,500** (positions open; no resolutions yet — correct for long-horizon investors)
- **BUILD XP: 250 / ~1,600** (one pipeline of four)

The project has produced 152 lessons of world-class analytical content. It has a live investment framework applied to a dozen active positions. It has an investment log that rivals the research process at many small funds. These are genuine achievements.

The Databricks platform is not one of them — yet.

The next 12 weeks are the build phase. The learning is substantially complete. The framework is built. The question is whether it converts into infrastructure that runs without the CEO conducting a daily lesson.

**The target for September 28, 2026:** B-01 through B-08 all deployed. Daily signals running. Investment log falsification triggers automated. The platform producing a weekly asset class tilt recommendation that can be reviewed against the CEO's manually-constructed view — and graded on whether they agree.

If the platform and the CEO agree, it validates the framework. If they disagree, one of them is wrong — and figuring out which one is the most valuable analytical exercise the project can produce.

That audit begins when the platform is running.

*Build it.*

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 152 delivered: 2026-07-06*
*Topic: Databricks Build Review — CEO Audit at the 3-Month Mark*
*Summary: 1 of 4 Phase 1 pipelines deployed (B-01 ✓, B-02–B-04 not started). Full reboot plan specified. B-02 deadline: July 13. Phase 1 complete target: July 20. Phase 2 complete target: August 31. Platform live target: September 28.*
*Direct action required: Bolo builds B-02 per April 24 spec within 7 days.*
