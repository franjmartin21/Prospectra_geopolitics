# Lesson 375 — Scaling the Research Function: Building Institutional-Grade Analytical Infrastructure

**Date:** 2026-09-27
**Session Type:** Daily Lesson
**Topic:** Scaling the Research Function — from Founder-Led Insight to Institutional Analytical Organization
**Curriculum Position:** Post-Series A Operations Arc (Lesson 375 of ongoing program)

---

## Opening Question

Here is the tension at the center of every research business that survives its founding phase:

**The founder's insight is the reason you exist. But founder-dependent insight is also the reason you won't scale.**

Eurasia Group, MSCI, and Goldman Sachs Research all began as the extended thinking of one or two unusually capable people. They became institutions when the *process* — not the person — became the source of analytical output. But every attempt to institutionalize research risks destroying the very thing that made it valuable: the non-consensus, contrarian, high-conviction thinking that clients paid for precisely because it couldn't be found in the consensus.

So: **how do you scale research quality without institutionalizing mediocrity?**

This is the problem Prospectra must solve as it deploys Series A capital.

---

## Core Concept: The Research Production System

A research organization is a factory. The raw material is information. The product is calibrated, actionable, differentiated insight. Between raw material and finished product, there is a *process* — and the quality of that process determines whether your research is worth paying for or merely worth reading.

### The Three Failure Modes

**1. The Star Analyst Trap**
Every signal is routed through one or two people. Output quality is excellent but unpredictable. The business cannot be sold, cannot grow beyond a handful of clients, and collapses when the analyst leaves or burns out. This describes most independent research shops and why most of them fail to institutionalize.

**2. The Committee Trap**
Research is "approved" by consensus, meaning it converges to the consensus view. No one is wrong — and no one is right in any useful sense. This is the failure mode of large investment banks, whose public research has been shown empirically to lag rather than lead market moves. Committee processes are structurally hostile to non-consensus calls.

**3. The Factory Trap**
Research becomes data formatting. Analysts spend 80% of their time cleaning, aggregating, and presenting data rather than interpreting it. Signal disappears under noise. The product looks comprehensive but clients stop acting on it. This is the failure mode of data vendors who pivoted to "research."

### The Solution: The Analytical Hierarchy

Top-tier research organizations — Eurasia Group, BCA Research, Gavekal, Absolute Strategy Research — share a common architecture:

```
TIER 1: ANALYTICAL LEADERSHIP (1-3 people)
- Set the house view and the contrarian calls
- Hold the intellectual standards
- Sign off on all market-moving research
- Own the client relationships at the most senior level

TIER 2: RESEARCH ANALYSTS (3-10 people)
- Own specific geographies, sectors, or analytical frameworks
- Produce primary analysis with accountability to house methodology
- Challenge the house view through structured devil's advocacy
- Track record logged and reviewed quarterly

TIER 3: RESEARCH ASSOCIATES / DATA INFRASTRUCTURE
- Feed the data layer: GDELT ingestion, market data, alternative data
- Produce structured briefings (not analysis) that analysts synthesize
- Maintain the data platform — the Databricks layer
- Quality control on data sourcing and methodology compliance
```

The critical design principle: **Tier 3 is automated as far as possible. Tier 2 is hired for judgment, not execution. Tier 1 is not replaceable — it is the brand.**

---

## Historical Grounding: How the Best Research Organizations Scaled

### Eurasia Group — Bremmer's Model

Ian Bremmer founded Eurasia Group in 1998. For its first five years, Bremmer *was* the product. Every client called Bremmer. Every research note carried Bremmer's fingerprints.

The institutionalization moment came when Bremmer built the **G-Zero framework** — a conceptual model rigorous enough that analysts without his specific background could apply it consistently to new events. The framework became the institutionalization mechanism. Not a process manual — a *framework* that encoded his analytical judgment into a form others could operate.

By 2010, Eurasia Group had 50+ analysts. Bremmer remained the public face and the setter of the house view. But Tier 2 analysts could write research that read like Eurasia Group without Bremmer personally authoring every sentence.

**Key lesson for Prospectra:** The GRI (Geopolitical Risk Index) is your institutionalization mechanism. If the GRI is rigorous, transparent, and methodologically reproducible, it encodes the analytical judgment into infrastructure that scales beyond Francisco.

### Gavekal Research — The Partnership Model

Gavekal was founded by Louis-Vincent Gave and Charles Gave (his father) with Anatole Kaletsky. Three contrarian minds, each with a different analytical lens (markets, macro, geopolitics). They resolved the Star Analyst Trap by making the partnership itself the brand — no single star, but a house of views held together by a common macro framework.

Their model: senior partners are expected to disagree publicly and productively. The research is better *because* of internal tension, not despite it.

**Key lesson for Prospectra:** As you hire Tier 2 analysts, you want their disagreement. A research culture where juniors agree with the CEO produces the Committee Trap. Build structured devil's advocacy into the process.

### MSCI — The Data-to-Framework Pipeline

MSCI (originally Morgan Stanley Capital International) did something different: they built the data infrastructure first, then layered interpretation on top. The MSCI indices became the industry standard not because MSCI had the best analysts — they didn't — but because they had the most defensible data methodology. Research became the value-add on top of a structural data moat.

**Key lesson for Prospectra:** The Databricks platform is your MSCI layer. If the GRI pipeline is auditable, defensible, and reproducible, you have a structural moat that pure analyst shops don't. Research quality compounds on top of data infrastructure quality.

---

## The Prospectra Research Architecture (Post-Series A Build)

Given the three failure modes and the historical models, here is the research architecture that Prospectra should build with Series A capital:

### Phase 1: Codify the Methodology (Months 1-2)

Before hiring anyone, document the analytical process so precisely that it can be followed by someone other than Francisco. This is the **Prospectra Research Methodology** — not a loose set of principles but a specific protocol:

- How a GRI score is calculated (input weights, data sources, update frequency)
- How a signal is validated before publication (backtesting standard, timeframe, asset classes covered)
- How a contrarian call is distinguished from the consensus (the devil's advocacy protocol)
- How client-facing research is reviewed before release (editorial standard, sign-off hierarchy)
- How track record is logged and scored (the outcome-scoring protocol from Lesson 325)

This document becomes the hiring standard and the quality control mechanism.

### Phase 2: First Analytical Hire (Months 3-4)

The first analyst hire is not about expanding coverage — it is about proving that a second mind can produce research at the Prospectra standard. Hire criteria:
- Primary analytical domain that is adjacent to Francisco's (e.g., European macro and FX, or Southeast Asia political risk)
- Intellectual honesty: they need to be willing to disagree with the house view and defend the disagreement
- Framework-oriented: they think in systems, not events
- Will not leave for Goldman in 18 months

Test: Give them a live geopolitical event. Ask them to produce a GRI impact assessment using the methodology document without your help. If they can do it — and you'd feel confident publishing their output — hire them.

### Phase 3: Data Infrastructure Staffing (Months 4-6)

Hire or contract one Databricks/data engineer whose sole job is maintaining and extending the data pipeline: GDELT ingestion, alternative data integration, model validation, and dashboard maintenance. This frees Tier 2 analysts from data work entirely.

This hire is not a research analyst. They will never produce a client-facing output. But they are the reason research quality doesn't degrade as volume increases.

### Phase 4: Editorial Layer (Month 6+)

As output scales (weekly signals, monthly deep dives, quarterly briefings), an editorial layer becomes necessary:
- Research review before publication (not for analytical accuracy — Francisco holds that — but for clarity, concision, and presentation standard)
- Client communications management (routing, follow-up, relationship notes in CRM)
- Track record maintenance (the log must be updated systematically, not just when you remember)

This can be a part-time editorial hire or a skilled contractor initially.

---

## Investment Implications

### What Research Moats Are Worth

The market for geopolitical intelligence has a structural problem: most of it is commoditized. Bloomberg Terminal delivers news. Reuters Breakingviews delivers opinion. Twitter delivers hot takes. The moat in research is not access to information — it is the *quality of the framework applied to that information*.

Firms with genuine research moats command 5-10x the pricing of commodity information services:
- MSCI charges hundreds of thousands per year for index access — the moat is methodology defensibility
- Eurasia Group charges $100K-$500K+ for access to their senior analysts — the moat is non-consensus judgment
- BCA Research's subscriptions are $15K-$25K/user/year — the moat is the macro framework, not the data

**Investment implication for Prospectra:** The GRI + Databricks infrastructure is the defensible moat. Research quality is what justifies premium pricing. If you commoditize the research by hiring volume over quality, you compete on price and lose. Hire for judgment and protect the analytical standard.

### Asset Classes Most Sensitive to Research Quality

The clients who value research quality most are:
1. **Long-only institutional investors** (sovereign wealth funds, pension funds, asset managers) — they have time horizons that match systematic analysis
2. **Macro hedge funds** — they need the non-consensus view because they can't generate alpha on consensus
3. **Family offices** — they want the framework, not just the signal
4. **Corporates with geopolitical exposure** — they want structured risk assessment, not journalism

These are also the clients with the largest check sizes and the longest retention. The research architecture you build determines which of these you can credibly serve.

---

## Databricks Angle

**The Research Quality Dashboard**

Build a Databricks-powered internal dashboard that tracks research quality metrics in real-time:

| Metric | Description | Data Source |
|---|---|---|
| GRI Score Accuracy | How often GRI signal direction matched subsequent asset price move | Market data vs. GRI log |
| Signal Conviction Distribution | Spread of high/medium/low conviction calls over time | Internal signal log |
| Track Record P&L | Simulated return of all signals with standard execution | Market data |
| Coverage Velocity | Number of countries/themes updated per week | GRI pipeline |
| Research Lag | Time from event to published analysis | GDELT event data vs. publication date |

**Pipeline Idea:** Connect the Signal Log to the Market Data pipeline and generate a rolling Sharpe ratio equivalent for research calls. If GRI-driven signals can demonstrate positive risk-adjusted return over 6-18 month horizons, this becomes the primary sales tool. Not testimonials — an auditable track record with methodology transparency.

**Dataset:** Internal Signal Log (already being built), Yahoo Finance/FRED for market data, GDELT for event timing.

---

## Reflection Questions

1. **The Star Analyst Trap:** Prospectra's brand is currently Francisco. How specifically would you distinguish between protecting the analytical standard (good) and creating dependency on a single person (dangerous)? What is the concrete test that tells you you've crossed from the first into the second?

2. **The Methodology Document:** Eurasia Group's G-Zero framework was what allowed Bremmer to scale. What is the equivalent for Prospectra? If you had to write the core framework in three pages — the intellectual model that all Prospectra research applies — what would it say?

3. **Tier 3 Automation:** The thesis is that Databricks automates Tier 3 so analysts focus on judgment. But which parts of the current analytical process are actually automatable — and which parts *look* automatable but actually require judgment? Walk through the GRI production process and label each step.

---

## Market Connection

The research business model is structurally similar to brand-equity investing: the moat is perception-plus-reality, and the cost of losing the moat is catastrophic and fast. Research firms that compromise their analytical standard for revenue volume (more reports, more clients, lower prices) almost always fail to recover. The quality destruction compounds faster than the revenue benefit.

**CEO Portfolio Note:** As Prospectra deploys Series A capital, the highest-return allocation is the one that protects the analytical standard longest. That means hiring slowly and correctly, automating infrastructure aggressively, and never publishing research you'd be embarrassed by in retrospect. Every low-quality output reduces the price you can charge for the next 50.

---

## Questions for Next Session

- How does Prospectra's pricing architecture change as a second analyst joins? Does each analyst expand TAM (new coverage) or deepen existing coverage (higher quality per geography)?
- At what revenue level does an in-house data science team become more cost-effective than Databricks licensing?
- What is the Prospectra research review protocol? Walk me through how a published signal gets from initial hypothesis to client delivery.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session: 2026-09-27 | Lesson 375 of 375+*
*Next: Lesson 376 — [CEO to determine based on Prospectra's active priorities]*
