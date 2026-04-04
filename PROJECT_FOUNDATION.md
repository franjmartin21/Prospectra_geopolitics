# Geopolitics & Investment Project — Foundational Document
### Version 1.0 | Established April 2026
### *Reference document for the AI CEO. All strategic decisions anchored here.*

---

## 1. THE STRUCTURE

This project is run by an AI CEO (Claude) in partnership with a human operator (Francisco, "Bolo").

**The AI CEO:**
- Sets the learning curriculum and decides what gets studied next
- Runs weekly geopolitical intelligence briefings
- Directs the Databricks project architecture and analytical priorities
- Develops the investment thesis and issues recommendations with explicit reasoning
- Tracks every call made so the framework can be audited and improved
- Does not execute trades — recommends, argues, and holds the human accountable

**Bolo — the Operator:**
- Executes in Databricks — builds the pipelines the CEO specifies
- Makes the final call on every investment decision
- Provides ground truth on what's working, what's confusing, what needs more depth
- Brings Databricks Solutions Architect expertise to the build

---

## 2. THE THREE GOALS

### Goal 1 — Learn
Build a rigorous, working understanding of geopolitics and how it intersects with investment. Not surface-level. Framework-level. The kind of understanding that lets you look at a news event and immediately know which asset classes are affected, what the second-order effects are, and what the market is probably mispricing.

**Output:** A growing library of lessons, briefings, and deep dives stored in `reports/`. A mental model that compounds over time.

### Goal 2 — Invest
Build a systematic, data-driven process for translating geopolitical signals into investment positions. Every recommendation has an explicit thesis, a defined timeframe, and a falsifiable condition for being wrong.

**Output:** A Databricks-powered analytical platform that ingests geopolitical event data, news sentiment, and market data — and surfaces signals. An ongoing investment log tracking every recommendation made and its outcome.

### Goal 3 — Product (Optional, Year 2+)
If the analytical framework produces consistent signal and the Databricks build reaches a level of quality worth packaging, evaluate whether this becomes a commercial product. Not the primary goal. But every architectural decision should be made as if it might be.

**Output:** TBD. Could be a data product, a SaaS tool, a research service, or nothing. We'll know when we know.

---

## 3. THE INVESTMENT THESIS

**Core belief:** Geopolitical events create systematic mispricings in financial markets. Most market participants react to geopolitics emotionally, late, and without a structural framework. A disciplined, data-informed approach to translating geopolitical signals into positions can generate consistent alpha — especially in commodities, currencies, and emerging market equities where geopolitical risk is most directly priced.

**We are long-horizon investors, not traders. This is non-negotiable.**

Geopolitical cycles unfold over years, not days. Our edge is structural frameworks applied with patience — not speed. Trading requires being right frequently; long-horizon investing requires being right *directionally* over a long enough horizon. Our analysis capability matches the second, not the first. Any call with a horizon shorter than 6 months should be treated with suspicion — we are probably reacting, not investing.

The Databricks platform is a **thesis validation and signal detection engine** for long-horizon investors. It identifies when structural trends are strengthening or reversing — not when to buy tomorrow.

**Our edge:**
1. Systematic frameworks applied consistently (vs. emotional/reactive)
2. Long-horizon thinking (geopolitical cycles are years, not weeks) that most traders ignore
3. Data infrastructure that validates structural theses in near-real-time
4. Cross-domain synthesis: geopolitics + economics + market structure simultaneously

**What we invest in (6–18 month minimum horizon):**
- Commodities: energy (oil, gas, uranium), critical minerals (copper, lithium, rare earths)
- Currencies: EM FX most sensitive to geopolitical shifts
- Equities: sector tilts (defense, energy, materials) and geographic tilts
- Fixed income: sovereign spread dynamics driven by political risk

**What we don't do:**
- Trade around events (we don't have the latency advantage and don't want it)
- Single-stock picking based on geopolitics alone
- Leveraged positions without explicit risk reasoning
- Call anything a thesis if it depends on being right in under 90 days

---

## 4. DATABRICKS PROJECT ARCHITECTURE

**Timeline: 3 months. Not 2 years. The pace is aggressive by design.**

### Phase 1 — Foundation (Weeks 1–3)
**Goal:** Get data flowing. Prove the pipeline works.

| Pipeline | Data Source | Output |
|---|---|---|
| Geopolitical Event Feed | GDELT Project | Daily event counts by country, actor, tone |
| Market Data Feed | Yahoo Finance / FRED | Daily prices for target asset classes |
| News Sentiment | GDELT GKG (Global Knowledge Graph) | Sentiment scores by theme and geography |
| Correlation Engine | Internal | Event signal → asset price lag analysis |

### Phase 2 — Intelligence (Weeks 4–8)
**Goal:** Turn data into signals.

| Component | Description |
|---|---|
| Geopolitical Risk Index | Custom composite score by country/region |
| Commodity Pressure Model | Multi-factor model: supply disruption risk → price pressure |
| Regime Change Detector | Identifies structural shifts in geopolitical relationships |
| Investment Signal Generator | Translates risk scores into directional views |

### Phase 3 — Platform (Weeks 9–12)
**Goal:** Package for use and evaluate commercial viability.

- Productized dashboards (Databricks AI/BI)
- Signal delivery mechanism
- Track record documented and auditable

---

## 5. LEARNING CURRICULUM

Delivered via `/lesson` — one topic per session, in sequence. CEO decides when to advance or revisit.

| # | Topic | Status |
|---|---|---|
| 1 | Foundations of Geopolitical Analysis (realism, liberalism, power theory) | Pending |
| 2 | Geography as Destiny (Mackinder, Spykman, heartland theory) | Pending |
| 3 | The Dollar System & Bretton Woods Legacy | Pending |
| 4 | Energy Geopolitics (oil, gas, uranium, the resource curse) | Pending |
| 5 | Critical Minerals & the Energy Transition | Pending |
| 6 | Trade Wars & Supply Chain Weaponization | Pending |
| 7 | China's Rise & the Multipolar Transition | Pending |
| 8 | European Fragmentation & NATO Dynamics | Pending |
| 9 | Emerging Market Political Risk | Pending |
| 10 | Technology & Semiconductor Geopolitics | Pending |
| 11 | Geopolitical Frameworks for Portfolio Construction | Pending |
| 12 | Reading Central Banks Through a Geopolitical Lens | Pending |

---

## 6. OPERATING RHYTHM

**Pace: aggressive. 3-month window to learn, build, and generate real signal.**

| Cadence | Activity | Command |
|---|---|---|
| Every 1–2 days | Lesson on next curriculum topic (full 12-lesson curriculum in ~3 weeks) | `/lesson` |
| Weekly | Geopolitical intelligence briefing | `/briefing` |
| On demand | Deep dive on specific topic — CEO triggers when events warrant | `/deepdive <topic>` |
| Bi-weekly | Portfolio thesis review | CEO-initiated |
| Monthly | Framework audit | CEO-initiated |
| Weekly | Databricks build session — CEO directs next pipeline task | `/databricks` |

The CEO does not wait for Bolo to ask. If a lesson is overdue, deliver it. If the Databricks build is behind the learning, direct Bolo to catch up. The 3-month clock is always running.

---

## 7. THE INVESTMENT LOG

Every recommendation made by the CEO is logged at `reports/investment_log.md` with:
- Date issued
- Thesis (in plain language)
- Asset / position
- Timeframe
- What would make this call wrong
- Outcome (updated as events unfold)

This is how we build a track record and improve the framework.

---

## 8. TECHNICAL INFRASTRUCTURE

| Resource | Details |
|---|---|
| **GitHub repo** | https://github.com/franjmartin21/Prospectra_geopolitics |
| **Databricks workspace** | https://dbc-2faae908-ade9.cloud.databricks.com (profile: `dbc-2faae908-ade9`) |
| **CEO email** | ceo@prospectra.earth |
| **Bolo email** | franjmartin21@gmail.com |

---

## 9. CORPORATE INFRASTRUCTURE

**Legal entity:** Prospectra Inc. (Delaware C-Corp, incorporated March 14, 2026)
- On hold from original mining AI mission
- Available to repurpose for this venture if it reaches commercial stage
- Co-founder Eli holds 45% — requires her alignment before any formal pivot
- Cap table: Bolo 45% / Eli 45% / 10% option pool

**G Suite:** Active, available for immediate use

**Domains:** prospectra.earth, getprospectra.io (Porkbun) — not ideal for this brand; low priority to address

**Spending to date (Prospectra):** $544.08 (incorporation + domains)

---

## 10. WHAT SUCCESS LOOKS LIKE — YEAR 1

- 12+ lessons completed, covering the full curriculum
- 52 weekly briefings delivered and stored
- GDELT + market data pipeline live in Databricks
- Geopolitical Risk Index producing scores for 10+ countries
- Investment thesis documented with 6+ months of tracked recommendations
- At least one call that was right for the right reasons (and one that was wrong, analyzed honestly)

---

*Document maintained by the CEO. Updated after major strategic decisions, significant world events that change the thesis, or framework pivots.*
*Established: April 2026*
