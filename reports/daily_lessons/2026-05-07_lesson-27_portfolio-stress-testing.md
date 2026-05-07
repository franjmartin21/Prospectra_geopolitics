# Lesson 27 — Portfolio Stress Testing: Running Your Thesis Through a Crisis

**Date:** May 7, 2026
**Session Type:** Daily Lesson — Synthesis & Application Cycle, Lesson 3 of 12
**Delivered by:** CEO — Prospectra Geopolitics & Investment Project

---

## CEO Note

Lesson 26 gave you the architecture for holding multiple futures simultaneously — the scenario planning framework. But there is a critical gap between building a scenario plan and knowing whether your *actual portfolio* survives any of those scenarios. Most investors who build scenario plans never complete the final step: they do not run their real positions through the scenarios they just constructed.

Stress testing is that final step. It is the discipline of taking your current portfolio — actual weights, actual instruments, actual correlated exposures — and systematically subjecting it to adversarial conditions to discover what breaks before the market does it for you.

This lesson completes the scenario planning → stress testing arc. Scenario planning maps the territory. Stress testing tells you whether your current vehicle can navigate it.

---

## Opening Question

> In August 1998, Long-Term Capital Management was one of the most sophisticated investment operations in the world. It was run by two Nobel Prize winners in economics, former vice-chairman of the Federal Reserve, and the finest quantitative minds on Wall Street. Its risk models — built on five years of historical data — showed a 99% probability that the fund could not lose more than $45 million in a single day. On August 21, 1998, it lost $553 million in one day. Within six weeks, it had lost $4.6 billion. The fund's own models had assessed the probability of this outcome as essentially zero.
>
> The models were not wrong about the math. They were wrong about the world. What assumption, built into every risk model of that era, produced this catastrophic underestimate — and how do you build a portfolio that does not share that assumption?

Hold that question. The answer is the entire foundation of stress testing.

---

## 1. The LTCM Lesson: Why Standard Risk Measures Fail in a Crisis

The assumption that destroyed LTCM — and that is embedded in virtually every standard portfolio risk model — is **correlation stability**.

Value at Risk (VaR), the industry-standard risk measure, is calculated by estimating how asset prices move relative to each other based on historical data. LTCM's models used five years of data from 1993–1998. During those five years, the correlations between their positions behaved exactly as the models predicted: diversified, offsetting, generating a reliable stream of risk-adjusted returns.

The models predicted that in a crisis, the correlations would continue to behave as they had in calm periods. They did not.

When Russia defaulted on its sovereign debt in August 1998, every market simultaneously:
- Fled to U.S. Treasuries (the safe haven) — sending yields down
- Sold every illiquid, credit-exposed, or emerging-market instrument — simultaneously
- Triggered margin calls across every leveraged position globally

LTCM's positions — which had been carefully constructed to be uncorrelated with each other — suddenly became **perfectly correlated**. Not with the market. With each other. The fund was long liquidity risk everywhere and short U.S. Treasuries everywhere. In a crisis, that is one trade, not three hundred. The diversification was an illusion created by measuring correlations in calm conditions.

**This is the first law of stress testing:**

> In a crisis, correlations converge toward 1 on the downside and -1 vs. the safe haven. Diversification measured in calm markets is not diversification in crisis markets.

Standard risk models — VaR, standard deviation, Sharpe ratio — are built on calm-period correlations. They systematically understate tail risk. Stress testing is the discipline of measuring risk under the assumption that correlations are not stable.

---

## 2. The Three Types of Stress Tests

Not all stress tests are the same. There are three distinct methodologies, and a robust stress testing practice uses all three.

### Type 1 — Historical Stress Tests

Run your current portfolio through actual historical crisis episodes. Ask: if my current positions had existed in August 2008, August 1998, March 2020, or October 1987, what would have happened?

**The critical insight:** you are not using the historical crisis to predict the future. You are using it to understand how your portfolio's factor exposures have behaved under stress conditions in the past. Historical stress tests reveal hidden factor concentrations that correlation-blind models miss.

**Key historical stress scenarios for a geopolitically-informed portfolio:**

| Episode | Date | Core Shock | What It Tests |
|---|---|---|---|
| Asian Financial Crisis | 1997 | EM currency contagion | EM FX and equity correlations in dollar crunch |
| LTCM / Russia Default | 1998 | Liquidity shock + sovereign default | Liquidity risk across all credit-exposed instruments |
| Dot-com bust | 2000–2002 | Equity bubble + technology sector | Growth vs. value, technology concentration |
| 9/11 | Sept 2001 | Geopolitical shock (kinetic event in core market) | Defense, aviation, insurance, safe-haven flows |
| Global Financial Crisis | 2007–2009 | Credit market collapse + global recession | Correlation collapse, credit exposure, dollar funding |
| European Debt Crisis | 2010–2012 | Sovereign credit risk in developed markets | Peripheral sovereign spread widening |
| Oil Price Collapse | 2014–2016 | Commodity supply glut + dollar strengthening | Energy sector, EM commodity exporters, petrodollar recycling |
| COVID-19 Initial Shock | Feb–Mar 2020 | Simultaneous demand and supply shock | Everything correlated in initial phase; sector divergence after |
| 2022 Rate Shock | 2022 | Fastest rate hiking cycle in 40 years | Duration risk, fixed income, growth equity, TINA collapse |

**How to run a historical stress test:**
1. Take your current portfolio weights
2. Pull the actual daily or weekly returns of each asset/instrument during the stress period
3. Apply those returns to your current weights
4. Calculate the portfolio's hypothetical P&L during the stress period
5. Identify which positions were the largest losers and whether they were *supposed* to be hedges

### Type 2 — Hypothetical Scenario Stress Tests

These are forward-looking, constructed scenarios based on your scenario planning framework. Unlike historical stress tests, they are explicitly geopolitical — they test your portfolio against futures that have not yet occurred.

**Key geopolitical stress scenarios for a 2026 portfolio:**

| Scenario | Core Shock | Asset Classes Most Affected |
|---|---|---|
| Taiwan Strait blockade | Semiconductor supply shock + regional war risk | TSM/semiconductor equities, TWD, KRW, gold, defense, oil (if Strait closed) |
| Iran nuclear test | Middle East escalation + oil supply risk | Brent crude, Gulf sovereign spreads, gold, Israeli equities, USD |
| U.S. fiscal crisis / debt ceiling rupture | U.S. sovereign credit shock | U.S. Treasuries, USD, gold, all dollar-denominated EM debt |
| China property cascade + banking crisis | EM contagion, commodity demand collapse | Copper, iron ore, AUD, BRL, EM equities broadly |
| NATO-Russia direct engagement | European war risk + energy supply disruption | European equities, EUR, European gas, German Bunds, defense globally |
| Saudi regime change | OPEC cohesion collapse + oil market uncertainty | Oil price (direction uncertain), USD petrodollar recycling, Gulf equities |
| Dollar weaponization threshold | Major EM economies abandon SWIFT/USD settlement | Dollar index, BRICS currency alternatives, gold, EM local currency bonds |

### Type 3 — Sensitivity Analysis (Factor Stress Tests)

Rather than running a specific scenario, sensitivity analysis asks: how does the portfolio respond to changes in specific risk factors? This is more granular than scenario analysis and more useful for portfolio optimization.

**Key risk factors to stress:**

| Factor | Stress Range | Why It Matters |
|---|---|---|
| USD index | +15% / -15% | Dollar strength inversely correlated with EM, commodities, non-USD revenues |
| Oil price | +50% / -40% | Energy producers long, consumers short; geopolitical shock amplifier |
| U.S. 10Y yield | +200bps / -100bps | Duration risk in all fixed income; risk-free rate impact on equity valuations |
| VIX (implied volatility) | 40 / 80 | Liquidity risk, correlation collapse signal |
| Gold | +20% / +40% | Safe-haven demand signal; tests whether "crisis hedges" actually hedge |
| China GDP growth | -2% vs. consensus | Commodity demand impact, EM contagion, supply chain |

---

## 3. Historical Case Study: The 2022 Rate Shock and the 60/40 Failure

For 40 years, the standard institutional portfolio was 60% equities / 40% bonds. The logic was simple: in a recession, equities fall but central banks cut rates and bonds rally — the "negative correlation" between stocks and bonds provided diversification.

**2022 demonstrated that this correlation is not structural — it is conditional.**

The 60/40 portfolio assumes that the primary risk being hedged is recession/deflation. In that environment:
- Equities fall (earnings decline)
- Bonds rally (central banks cut rates)
- The hedge works

But the 2022 shock was **inflation** — the highest CPI readings since the early 1980s. In an inflationary environment:
- Equities fall (rate hikes compress multiples, especially growth)
- **Bonds also fall** (yields rise to fight inflation)
- The correlation flips from negative to positive
- Both sides of the "hedge" lose simultaneously

**Result:** The 60/40 portfolio lost approximately 16–20% in 2022 — one of its worst performances in a century. Not because the world was unusual, but because the *type* of shock was outside the conditions the diversification was designed to handle.

**The stress test lesson:** Before trusting any diversification relationship, ask: *under what conditions does this correlation hold, and under what conditions does it break?* The 60/40 hedge holds in deflationary recessions. It breaks in inflationary shocks. Every hedge in your portfolio has a conditional structure. Stress testing is the discipline of finding those conditions.

**The geopolitical dimension:** Geopolitical shocks tend to be *stagflationary* — they disrupt supply (inflationary) while damaging demand (recessionary). The 2022 shock was catalyzed by the Russia-Ukraine war driving energy prices to record levels while the Fed was already fighting COVID-era inflation. Geopolitical investors need stress tests that explicitly model stagflationary scenarios — the condition under which most standard "diversified" portfolios fail.

---

## 4. Running the Prospectra Thesis Through a Stress Test

The current Prospectra investment thesis (from Lessons 11, 25, and 26) is directionally:
- Long European defense equities (structural rearmament thesis)
- Long energy/commodities with supply disruption exposure (oil, gas, uranium)
- Long critical minerals (copper, lithium — energy transition + geopolitical supply risk)
- Cautious on semiconductor exposure without hedges (Taiwan concentration)
- Gold as structural hedge (5–10% allocation)
- Underweight China equities
- Selective EM FX (avoiding dollar-sensitive EM, favoring commodity exporters)

**Let's run this through three stress scenarios:**

### Stress Test A: Global Recession (Demand Collapse)

Trigger: U.S. Fed overtightens, global growth slows sharply, commodity demand collapses.

| Position | Expected Stress Performance | Why |
|---|---|---|
| European defense equities | Moderate negative (−15%–20%) | Defense budgets may face pressure; "fiscal consolidation" narrative |
| Energy/commodities | Strongly negative (−25%–40%) | Demand collapse; oil to $55–65; copper −30% |
| Critical minerals | Strongly negative (−30%–45%) | EV demand falls; China industrial slowdown |
| Gold | Positive (+10%–20%) | Safe haven; real rates fall as Fed reverses |
| Semiconductor hedges | Positive (if short or hedged) | Risk-off benefits hedges |

**Verdict:** The current thesis is long commodity beta. In a pure demand-collapse recession, it gets hurt significantly. The gold position and semiconductor hedges partially offset. This is a *known and accepted* risk — long-horizon commodity exposure requires tolerating recession drawdowns.

**Portfolio action:** Ensure gold allocation is at the full 5–10% range. Consider adding a USD long as a recession hedge (dollar typically strengthens in risk-off). Check that energy and critical minerals positions have 18–24 month minimum horizon before revisiting thesis.

### Stress Test B: Taiwan Strait Crisis (Geopolitical Shock)

Trigger: PLA initiates blockade of Taiwan strait; semiconductor supply disruption; regional war risk.

| Position | Expected Stress Performance | Why |
|---|---|---|
| European defense equities | Strongly positive (+20%–40%) | Global defense spending accelerates; direct beneficiary |
| Energy/commodities | Mixed (oil +20%–30%; copper −10%–15%) | South China Sea shipping disruption spikes oil; copper demand falls on China slowdown |
| Critical minerals | Negative (−20%–30%) | China controls rare earth supply chains; conflict disrupts processing |
| Gold | Strongly positive (+15%–25%) | Safe haven bid |
| Semiconductor exposure (unhedged) | Strongly negative (−35%–50%) | TSMC supply shock is the thesis shock |

**Verdict:** The thesis is reasonably positioned for a Taiwan crisis *if* semiconductor exposure is hedged. European defense and gold are the key beneficiaries. Critical minerals are a weak point — China's dominance of rare earth processing makes this a liability in a Taiwan scenario, not an asset.

**Portfolio action:** Critical minerals thesis needs to be refined to distinguish between *production* exposure (long Chile copper, Australian lithium) and *processing* exposure (which runs through China). In a Taiwan crisis, production is fine; processing is disrupted. Size accordingly.

### Stress Test C: Dollar Weaponization Threshold

Trigger: BRICS+ launches viable alternative settlement system; major oil exporters begin accepting non-dollar settlement; dollar index -10%–15% over 18 months.

| Position | Expected Stress Performance | Why |
|---|---|---|
| European defense equities | Neutral to positive | NATO countries benefit from relative dollar weakness; revenues in EUR |
| Energy/commodities | Strongly positive (oil priced in non-USD = dollar-weaker) | Classic dollar-commodity inverse |
| Critical minerals | Positive | Commodity complex benefits from dollar weakness |
| Gold | Strongly positive (+20%–30%) | Classic dollar hedge; central bank accumulation accelerates |
| EM FX (commodity exporters) | Positive | Dollar weakness broadly EM-positive; commodity exporters doubly so |

**Verdict:** The thesis has high positive exposure to a dollar-weakening scenario. This is structurally coherent — commodity/energy/gold/EM FX all benefit. But it creates concentration: if the dollar unexpectedly strengthens (e.g., U.S. fiscal crisis paradoxically drives safe-haven dollar demand), the entire commodity-EM complex gets hurt simultaneously.

**Portfolio action:** Maintain some explicit USD exposure (Treasuries or USD cash) as a hedge against a paradoxical dollar-strengthening crisis. Size at 5–8% of portfolio — enough to dampen the correlation, not enough to negate the thesis.

---

## 5. The Correlation Collapse Map

Every stress test generates the same insight eventually: when you need diversification most, it is often least available. This is not a failure of diversification theory — it is a structural feature of how markets work during crises.

**Why correlations collapse in a crisis:**

1. **Forced selling:** Leveraged investors face margin calls and must liquidate regardless of fundamentals. They sell everything — even uncorrelated assets — to meet cash requirements. This mechanically creates correlation.

2. **Liquidity flight:** In a crisis, investors distinguish only between "liquid" and "illiquid" — not between fundamentally different asset classes. Everything illiquid gets sold; everything liquid gets bought.

3. **Risk factor concentration:** Most portfolios have hidden common factor exposures (dollar sensitivity, interest rate sensitivity, China growth sensitivity) that are invisible in calm markets but dominate in stress.

**Building a correlation-robust portfolio:**

The portfolio that actually diversifies in a crisis has exposures to genuinely *orthogonal* risk factors — factors that are structurally uncorrelated because they respond to different economic mechanisms:

| Factor Pair | Structural Orthogonality | Crisis Correlation Risk |
|---|---|---|
| Gold + Oil | High — gold is safe-haven; oil is demand/supply risk | Low — they diverge in most crisis types |
| Gold + USD | High — structurally inverse | Low — gold hedges dollar risk specifically |
| Defense equities + EM equities | High — defense benefits when EM suffers geopolitically | Low — these genuinely move oppositely in conflict scenarios |
| Oil + Copper | Low — both commodity beta, both China-correlated | High — crash together in demand-collapse scenarios |
| EM FX + commodity | Low — commodity exporters are the same trade | High — identical dollar-sensitivity |

**The Prospectra portfolio implicit concentration:** Long oil + long copper + long EM commodity FX is essentially **one trade** — long China industrial demand + long global growth. If that single factor moves against you, all three positions move together. The gold and defense positions provide genuine orthogonality. Everything else is factor concentration dressed as diversification.

---

## 6. The Stress Test Protocol — A Repeatable Process

Stress testing is not a one-time exercise. It is a quarterly or event-triggered discipline. Here is the operational protocol:

**Quarterly Stress Test (every 90 days):**

1. **Map current portfolio weights** — explicit positions by instrument and asset class
2. **Run historical stress tests** — overlay current weights on the 3–5 most relevant historical crises
3. **Run scenario stress tests** — overlay current weights on the current scenario set (from Lesson 26's scenario planning framework)
4. **Run factor sensitivity analysis** — stress each major risk factor (±15% for each)
5. **Identify the worst single scenario** — what is the maximum drawdown from any single coherent stress scenario?
6. **Check for correlation collapse** — identify positions that are supposed to hedge each other; verify they are structurally orthogonal, not just historically uncorrelated
7. **Decide on three actions** — for each stress test, identify no more than three portfolio adjustments that reduce the worst-case outcome without meaningfully sacrificing the base-case thesis
8. **Document** — write the stress test results and portfolio actions into the investment log

**Event-Triggered Stress Tests:**
Run a mini stress test whenever:
- A major geopolitical event changes the scenario probability weights by more than 10%
- The VIX exceeds 30 (implies markets are pricing elevated stress)
- One of the leading indicators from the scenario framework triggers
- Any position moves more than 15% in a week without a clear fundamental reason

---

## Investment Implications

| Application | Insight | Directional Action |
|---|---|---|
| Critical minerals thesis refinement | Production exposure ≠ processing exposure; China controls processing | Prefer Australian/Chilean producers; underweight anything with Chinese processing concentration |
| Gold allocation | Genuinely orthogonal to most other thesis positions; hedges recession AND dollar weakness AND crisis scenarios | Full 5–10% structural allocation; do not trade it as a tactical position |
| USD cash allocation | Paradoxical dollar strengthening in crisis is a real risk; provides firepower for counter-cyclical buying | 5–8% in USD cash/short Treasuries as correlation hedge and dry powder |
| EM FX / commodity correlation | EM commodity FX and oil/copper are the same trade | Consolidate sizing — do not treat these as separate diversification contributions |
| European defense | Orthogonal to all three stress scenarios tested; positive in B and C, modest negative in A | Maintain as core Tier 1 position; this is the portfolio's most robust individual thesis |
| Scenario B tail hedge | Unhedged TSMC / semiconductor exposure has negative expected value | Size semiconductor exposure with explicit Scenario B hedge (put options, reduced exposure, or Taiwan-adjacent short) |

**CEO Portfolio Note:** The Prospectra thesis survives all three stress scenarios with acceptable drawdown *if* two adjustments are made: (1) refine critical minerals to separate production from processing exposure, and (2) maintain genuine orthogonal hedges (gold, USD, defense) at full weight. The thesis's primary vulnerability is its implicit China-industrial-demand concentration across commodity positions. This is a known, managed risk — not a fatal flaw. Long-horizon conviction is appropriate. But the 90-day stress test discipline is non-negotiable: this concentration must be monitored as the thesis evolves.

---

## Databricks Angle

**Pipeline: Automated Portfolio Stress Testing Engine**

This is the most operationally critical pipeline in the Prospectra architecture — the tool that makes stress testing a systematic, repeatable discipline rather than a manual exercise.

```
Pipeline Design: Stress Test Engine

INPUTS:
1. Portfolio weights table (updated monthly or on position change)
   - Instrument, asset class, weight, entry price, horizon

2. Historical price data (Yahoo Finance via yfinance Python library)
   - Daily returns for all instruments, 1995–present
   - Additional macro series from FRED: VIX, USD index, gold, oil, 10Y yield

3. Scenario definitions table (from Lesson 26's scenario framework)
   - Scenario name, shocked factor, shock magnitude, correlated factor moves

PROCESSING:

Module 1 — Historical Stress Tests:
- For each defined crisis period (table of start/end dates and labels)
- Pull historical returns for each instrument during the period
- Apply to current portfolio weights
- Output: P&L waterfall by position and in aggregate for each crisis period

Module 2 — Hypothetical Scenario Stress Tests:
- For each defined geopolitical scenario
- Apply factor shocks using a factor-return mapping table
  (e.g., "Taiwan Strait blockade" → oil +25%, TSMC -40%, gold +20%, defense +30%)
- Map each portfolio instrument to the relevant factors
- Output: Estimated portfolio P&L under each scenario

Module 3 — Correlation Stress Analysis:
- Compute rolling 90-day and 30-day correlation matrices across all portfolio instruments
- Compute the correlation matrix during defined stress periods
- Flag instrument pairs where calm-period correlation diverges significantly from stress-period correlation
- Output: Correlation collapse risk report

Module 4 — Factor Concentration Report:
- Run factor attribution: decompose portfolio returns into common factors
  (dollar sensitivity, China beta, commodity beta, interest rate duration, etc.)
- Flag any single factor that explains >30% of portfolio variance
- Output: Factor concentration dashboard

OUTPUT:
- Databricks AI/BI Dashboard: Current portfolio stress test results (updated monthly)
- Alerts table: trigger when any scenario loss exceeds configured threshold
- Correlation collapse warning: when stress-period correlations diverge from calm-period
- Quarterly stress test report (PDF export)
```

**Key datasets and libraries:**
- `yfinance` — free historical price data for all major instruments (Python)
- `fredapi` — Federal Reserve Economic Data (FRED): macro factors
- `pandas`, `numpy`, `scipy` — correlation matrices, factor decomposition
- `sklearn` — PCA for factor extraction from return time series
- Databricks Delta Lake: versioned portfolio weights table (audit trail for investment log)

**Priority pipeline for Phase 2 (Weeks 4–8):** The stress testing engine should be the first analytical pipeline built after the basic data ingestion is working. It does not require sophisticated ML — it requires clean historical data, a parameterized scenario definition table, and reliable factor mapping. This can be operational within 2–3 Databricks sessions once the data feeds are live.

---

## Reflection Questions

1. The 2022 60/40 failure revealed that the bonds-as-hedge assumption was conditional on deflation/recession as the primary risk. Every portfolio has these conditional assumptions — relationships that work in one regime and fail in another. Think about the current Prospectra thesis: what is the *single most important conditional assumption* that the thesis depends on? What would have to be true for that assumption to break — and how would you know it was breaking before the portfolio told you?

2. The LTCM case study shows that Nobel Prize-winning economists with perfect mathematical models can be catastrophically wrong because their models were calibrated on the wrong historical period. LTCM used 5 years of data (1993–1998) — a period of unusually low volatility and globalization-driven correlation. When you run historical stress tests, you have to choose which historical periods are relevant. How do you decide which past crises are analogous to present risks — and which are misleading because the structural conditions were fundamentally different? Is the 1998 Russia default a useful analog for a potential 2026 China property crisis, or are the structural differences large enough to make the comparison dangerous?

3. The correlation collapse map identified that oil + copper + EM commodity FX is essentially one trade — long China industrial demand. But the thesis holds all three *for different reasons*: oil for energy geopolitics, copper for the energy transition, EM FX for dollar multipolarization. If the investment thesis reasons are genuinely distinct, does it matter that the *realized* correlations are the same? Is there a version of the thesis that captures all three narratives while reducing the concentration — or is the concentration the price of having a coherent geopolitical view?

---

## Questions for Next Session (Spaced Repetition)

- Lesson 26 (Scenario Planning): We constructed a Taiwan 2×2 matrix and assigned 40% probability to "Status Quo + Economic Competition." The stress test in Lesson 27 showed that a recession scenario (Stress Test A) hits the commodity thesis significantly. Under what conditions would Scenario C (Status Quo) coincide with a global recession — and if that combination is plausible, how does it change the scenario probability weights you assigned?
- Lesson 14 (Sanctions Architecture): The stress test for a potential China crisis identified that EM commodity FX could be hurt in a demand-collapse scenario. But in Lesson 14, we established that the dollar-weaponization threshold is approaching. How do you hold both simultaneously — long EM commodity FX as a dollar-multipolarization thesis AND stress-test the position against a China-induced demand collapse?

---

*Synthesis & Application Cycle — Lesson 3 of 12*
*Next: Lesson 28 — The Geopolitical Investment Clock: Regime Detection and Cycle Positioning*
*CEO — Prospectra Geopolitics & Investment Project*
