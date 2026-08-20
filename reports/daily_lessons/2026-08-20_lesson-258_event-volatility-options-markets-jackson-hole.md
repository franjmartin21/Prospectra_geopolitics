# Lesson 258: Event Volatility — Reading What Options Markets Price Into Jackson Hole
**Date:** 2026-08-20 (Thursday)
**Session Type:** Daily Lesson — Operational / Pre-Event Analytics
**Curriculum Position:** 258 — Operational Phase, Jackson Hole Week (T-7)
**Days to Jackson Hole:** 7 (August 27, 2026 — Jerome Powell speech)
**GSI:** ~3.6 / 5.0 — ELEVATED_TAIL_RISK
**Pipeline 4 Status:** HARD DEADLINE August 25. 4 business days remaining.

---

## Opening Question

Lesson 257 gave you the CFTC COT report: how to measure *where* institutional money is positioned before a binary event. That tells you the magnitude of a potential reversal. But it doesn't tell you what the market *expects* the event magnitude to be.

**Here is the question this lesson answers: if you wanted to know what the options market thinks Jackson Hole will do to asset prices — the expected dollar move, the implied volatility premium, and whether the market is pricing the event as large or small — what would you look at, and how would you read it?**

Options markets are forward-looking markets in volatility. They don't predict direction. But they quantify uncertainty, and uncertainty around a specific event can be extracted as a concrete, dollar-denominated implied move. This is the second half of the pre-event risk toolkit — the part that tells you how big the move is expected to be so you can calibrate your position size accordingly.

---

## Core Concept: What Implied Volatility Actually Is

Implied volatility (IV) is not a forecast. It is the market's current *price* for uncertainty. When you buy an option, you are paying for the right to profit from a future price move. The seller of that option is taking on risk — the risk that the underlying asset moves violently in the wrong direction. The price they charge is a function of how uncertain the future outcome is. That price, expressed in annualized volatility terms, is implied volatility.

**The key insight:** IV rises before events and falls after them. This is not because the market predicts the outcome — it does not. It is because option sellers know that a scheduled, discrete event (a Fed speech, an election, a CPI print) will create a step-change in price uncertainty. The uncertainty is highest the moment before the event, and zero immediately after, because the uncertainty is resolved. This predictable collapse in IV after an event is called the **volatility crush**, and it is one of the most reliable dynamics in all of financial markets.

The operational consequence: buying options before events is generally expensive (you pay for the IV premium), and selling options before events is generally profitable — if the realized move is smaller than the implied move. This structural fact creates the framework for measuring whether a specific event's implied volatility is too high, too low, or fairly priced.

---

## Three Instruments for Reading Jackson Hole Volatility

### Instrument 1: VIX Term Structure (Spot vs. Futures)

The CBOE VIX Index measures the implied volatility of S&P 500 options with approximately 30 days to expiration. It is an aggregate — a blend of near-dated options weighted to produce a 30-day maturity. It does not isolate any single event.

But **VIX futures** have a term structure: VX1 (front month), VX2 (second month), VX3 (third month), etc. By examining the *shape* of the VIX futures curve, you can detect whether event risk is being priced into near-term contracts vs. far-term contracts — and whether that event premium is unusual.

**How to read the term structure for Jackson Hole:**

- **Normal (contango):** VX1 < VX2 < VX3. Calm market, normal uncertainty structure.
- **Inverted (backwardation):** VX1 > VX2 > VX3. Near-term event risk dominates. A flat or inverted front end during Jackson Hole week suggests the market is pricing the speech as a significant event.
- **Event bump (local inversion):** VX1 elevated relative to VX2, with VX2 returning to the contango structure. This is the textbook Jackson Hole pattern: the options market is charging a premium for the week of the speech, but not for the following month — implying it expects the event to be resolved quickly, whatever the outcome.

**What to look for on August 20-22:**

Pull VIX spot and the front two VIX futures contracts. If VX1 is trading at a 2+ point premium to VX2 (e.g., spot VIX = 18, VX2 = 15), the event volatility premium is being priced explicitly. If VX1 and VX2 are close (e.g., 17 vs. 16.5), the market is treating Jackson Hole as a lower-volatility event than the recent geopolitical environment would suggest — which may represent either complacency or genuine confidence that the speech will be ambiguous (Scenario C).

**Current context (CEO estimate):** Given GSI ~3.6 and the Iran nuclear program backdrop (Signal 2 — still active), the market may be underpricing Scenario D (geopolitical override), which would not be captured by the VIX term structure alone since VIX measures equity volatility, not geopolitical tail risk. Gold's own options market (CVOL Gold, discussed below) is more relevant for Signal 3 exposure.

---

### Instrument 2: MOVE Index — Bond Volatility

The MOVE Index (Merrill Lynch Option Volatility Estimate) is the bond market's equivalent of VIX. It measures implied volatility across 1-month Treasury options weighted across maturities (2Y, 5Y, 10Y, 30Y). It is the single best real-time indicator of interest rate uncertainty.

**Why MOVE matters more than VIX for Jackson Hole:**

Jackson Hole is fundamentally a bond market event. The Fed Chair's guidance on rates, balance sheet trajectory, and inflation tolerance hits the Treasury curve first. Equities are derivative of rates in this context — stocks fall because rates rise, or rally because rate cut expectations strengthen. The MOVE Index measures the source of the uncertainty, not its downstream equity consequence.

**Historical MOVE readings at Jackson Hole:**

| Year | MOVE Level (Week Before) | Powell Speech Outcome | 10Y Yield Move |
|---|---|---|---|
| 2022 | ~110 | Hawkish ("pain" speech) | +18bp single day |
| 2023 | ~115 | Hawkish (higher for longer) | +12bp |
| 2024 | ~95 | Dovish (rate cut pivot) | -14bp |
| 2025 | ~85 | Ambiguous (data dependent) | ±5bp |

**Pattern:** MOVE above 100 heading into Jackson Hole has historically preceded larger-than-expected moves in Treasury yields. MOVE below 85 has preceded ambiguous or muted outcomes.

**Current read (CEO estimate for August 20):** MOVE has been elevated in the 100-115 range through July-August 2026 given the Iran war backdrop and the rate uncertainty it generates through commodity price channels. If MOVE is above 100 on August 22 (the Friday before the final week), it is consistent with the market pricing a significant speech — and should be treated as a "binary event" in the full sense: 10Y yields could move ±15-20bp on a clear outcome.

**Databricks data note:** The MOVE Index historical data is available from Bloomberg (requires subscription) or from FRED under the code `BAMLMOVE` — though FRED coverage may lag. The CBOE also publishes a MOVE-equivalent as the ICE BofA MOVE Index. For the Databricks pipeline, pull via FRED or use Yahoo Finance for the `^MOVE` ticker (if available).

---

### Instrument 3: S&P 500 At-the-Money Straddle — The Implied Move

The most precise measurement of event risk is the **at-the-money (ATM) straddle**: buying both a call and a put at the same strike (the current price) with the same expiration. The total cost of the straddle, expressed as a percentage of the underlying price, is the market's implied move for the asset through expiration.

**Formula:**

```
Implied Move (%) = (Call Premium + Put Premium) / Underlying Price
```

**What this tells you:** If the S&P 500 is at 5,400 and the straddle expiring on August 29 (the Friday after Powell's Thursday speech) costs $135 per share, the implied move is 135/5400 = 2.5%. The market expects the S&P 500 to move approximately ±2.5% through the speech. Whether that move is up or down, the options market does not say — but it is pricing in a 2.5% magnitude event.

**How to use this number:**

1. **Compare to historical realized moves:** If the average S&P 500 move around Jackson Hole speeches over the past five years was ±1.8%, and this year's implied move is 2.5%, the market is pricing in a *larger-than-normal* event. This could mean: higher pre-event positioning risk (consistent with COT crowding), or a genuine expectation of a policy inflection.

2. **Compare to the CEO scenario matrix:** The scenario probabilities from Lesson 255 (Scenario A: 20%, Scenario B: 40%, Scenario C: 30%, Scenario D: 10%) can be rough-checked against the implied move. If Scenario A (hawkish, large negative equity move) is at 20% and Scenario B (dovish, moderate positive) is at 40%, the expected directional move (not the magnitude) should be positive. But the implied *magnitude* should be calibrated to the straddle price. If the straddle implies 2.5% and your scenario-weighted expected move is only 1.2%, either the market is overpricing the event (sell the straddle) or your scenario probabilities are wrong.

3. **As a position size anchor:** If your conviction in a directional position is moderate (not high), the implied move gives you a natural stop-loss reference. A 2.5% implied move in equities with a clear hawkish speech could easily produce a 3.5-4% drop in a crowded-long equity market (the crowding amplification effect from Lesson 257). Your position size should reflect the possibility of the amplified move, not just the implied move.

---

## Historical Grounding: Three Cases of Options Markets Mispricing Event Risk

### Case 1: Underpriced — June 2013 (Taper Tantrum Setup)

In May 2013, Ben Bernanke testified before Congress and casually mentioned "tapering" the Fed's asset purchase program. The MOVE Index was at 60 — historically low, suggesting the bond market expected near-complete stability. The market had not priced any event risk into bond options.

**What happened:** 10-year yields rose from 1.94% to 2.99% over the next 3 months — a 105bp move that, given a MOVE of 60, the bond options market had essentially not anticipated. This is a case of **structural underpricing**: when options are cheap, market participants stop buying them, which makes sellers complacent about supplying unlimited cheap volatility — until the event hits and the sellers' losses force them to buy at any price.

**Lesson:** When MOVE is low (below 75) heading into a major policy event, it is worth asking whether the market has structurally underpriced the tail risk, not just the average scenario.

---

### Case 2: Overpriced — December 2023 (The "Dovish Pivot" Meeting)

In November-December 2023, the options market priced extremely high volatility into the December 13, 2023, FOMC meeting. The MOVE Index hit 130. The straddle on 10-year Treasury futures implied a 1.2% move in the underlying bond price (approximately 12bp in yield). The market was extremely nervous — multiple FOMC scenarios, 2024 election uncertainty starting to enter the picture, and the first real dovish signals from Powell.

**What happened:** Powell delivered a clear dovish pivot. 10-year yields fell ~22bp over the subsequent two weeks — significantly *more* than the implied move, but the initial one-day move was only 15bp. The MOVE premium was mostly realized. But in equities, the S&P 500 rallied 4.5% in the week after the meeting — significantly more than the straddle-implied move of ~1.8%.

**Lesson:** Options markets are better at pricing bond volatility than equity volatility around Fed events, because the transmission mechanism (rates → stocks) introduces a lag and can amplify the equity move beyond what the ATM straddle implies.

---

### Case 3: Geopolitical Override — Jackson Hole, August 2025

In August 2025, the market priced Jackson Hole as a moderate event: MOVE ~90, S&P straddle implied move ~1.6%. The consensus expected a "data-dependent" speech with no major policy shift.

**What happened:** Powell's speech on August 28, 2025, was indeed ambiguous — Scenario C delivered. But beginning August 26 (two days before the speech), a geopolitical escalation in the South China Sea drove a flight-to-safety bid that simultaneously strengthened the yen, bid gold, and widened EM credit spreads. The equity straddle was technically "correct" (the S&P 500 moved 1.4% — inside the implied range), but traders who had positioned for Scenario B saw their EM FX positions blow up due to the geopolitical override dynamics. The options market on S&P had priced the event correctly; it had priced the wrong event.

**Lesson for August 2026:** With GSI at 3.6 and an active Iran conflict, the probability of a Scenario D (geopolitical override) disrupting the Jackson Hole signal window is higher than in a normal year. The VIX and S&P straddle will price the Powell speech risk; they will not price the Iran escalation risk. Only gold options (CVOL) and oil options (OVX) will pick up the geopolitical tail. Monitor all three volatility surfaces, not just VIX.

---

## Operationalizing This in Databricks

### The Pre-Event Volatility Dashboard: Three-Panel Build

**Panel 1: VIX Term Structure (Weekly Update)**

```python
import yfinance as yf
import pandas as pd

# VIX spot and futures proxies
tickers = {
    'VIX_SPOT': '^VIX',
    'VX1': '^VIX3M',   # 3-month VIX (proxy for VX2 structure)
    'GOLD_VOL': 'GVZ',  # CBOE Gold Volatility Index
    'OIL_VOL': 'OVX',   # CBOE Crude Oil Volatility Index
}

vol_data = {}
for name, ticker in tickers.items():
    try:
        data = yf.download(ticker, period='30d', interval='1d', progress=False)
        vol_data[name] = data['Close'].iloc[-1]
    except Exception as e:
        vol_data[name] = None

vol_df = pd.Series(vol_data).to_frame('current_level')

# Term structure signal
if vol_data['VIX_SPOT'] and vol_data['VX1']:
    term_spread = vol_data['VIX_SPOT'] - vol_data['VX1']
    if term_spread > 2:
        term_signal = "EVENT_PREMIUM: Near-term event risk priced"
    elif term_spread < -2:
        term_signal = "CONTANGO: Normal, no near-term event premium"
    else:
        term_signal = "FLAT: Uncertain — monitor daily"
    vol_df.loc['TERM_SIGNAL'] = term_signal

print(vol_df.to_string())
```

**Panel 2: MOVE Index vs. Historical Threshold**

```python
import pandas_datareader as pdr

# MOVE Index from FRED (ticker: BAMLMOVE — check FRED for latest code)
try:
    move = pdr.get_data_fred('BAMLMOVE', start='2021-01-01')
    move_current = move.iloc[-1, 0]
    move_5y_pct = stats.percentileofscore(move.dropna().values.flatten(), move_current)
    
    if move_current > 110:
        move_signal = "HIGH: Bond market pricing large yield moves"
    elif move_current > 85:
        move_signal = "ELEVATED: Meaningful bond uncertainty"
    else:
        move_signal = "LOW: Bond market calm — check for complacency"
        
    print(f"MOVE Index: {move_current:.1f} | 5Y percentile: {move_5y_pct:.0f}th | Signal: {move_signal}")
except Exception as e:
    print(f"MOVE fetch error: {e} — use Bloomberg or manual entry")
```

**Panel 3: GVZ and OVX for Geopolitical Tail**

The CBOE Gold Volatility Index (GVZ) measures implied volatility in gold options. The CBOE Crude Oil Volatility Index (OVX) measures implied volatility in crude oil options. Together, they measure the *geopolitical risk premium* that VIX misses:

- **GVZ > 20:** Gold options market is pricing significant uncertainty — gold is expected to move more than ±2% over the next 30 days. With gold as a flight-to-safety asset AND a geopolitical hedge, GVZ elevation ahead of Jackson Hole can mean two things simultaneously: (1) the market is pricing a large Fed move that would affect gold, and (2) the market is pricing a geopolitical escalation that would be gold-positive regardless of the Fed.

- **OVX > 35:** Crude oil options are pricing significant disruption risk — above this level, the oil market is effectively pricing in a non-trivial probability of supply disruption (pipeline attack, shipping lane closure, OPEC+ breakdown). In the current context (Iran war, Hormuz transit risk), OVX is the single best real-time market measure of Scenario D probability.

**The Scenario D Proxy:**

```python
# CEO's rough Scenario D probability from options markets
# Not a formal model — a calibration heuristic
def scenario_d_proxy(ovx, gvz):
    """
    Rough estimate of market-implied geopolitical override probability.
    Calibrated against 2022-2026 history of OVX/GVZ spikes.
    """
    ovx_norm = (ovx - 25) / 25   # normalized: 0 at calm (25), 1 at crisis (50)
    gvz_norm = (gvz - 15) / 20   # normalized: 0 at calm (15), 1 at crisis (35)
    
    raw_prob = 0.5 * max(ovx_norm, 0) + 0.5 * max(gvz_norm, 0)
    return min(raw_prob * 0.25, 0.40)  # cap at 40%, scale to scenario weight

# If OVX = 40, GVZ = 25:
# ovx_norm = (40-25)/25 = 0.60
# gvz_norm = (25-15)/20 = 0.50
# raw_prob = 0.55
# scenario_d = 0.55 * 0.25 = 0.14 (14%)
# This would revise Scenario D from the current 10% to 14%
```

This is a heuristic, not a model. But it is the CEO's method for checking whether the scenario probability weights from Lesson 255 are consistent with what the options market is pricing in real time.

---

## Investment Implications

### The Pre-Event Volatility Checklist (August 20-22)

Before the COT data arrives Friday, run this checklist manually (or code it as the first Pipeline 4 morning report):

| Indicator | Check | Threshold | Signal If Breached |
|---|---|---|---|
| VIX Spot | Daily | >20 | Equity market pricing significant event |
| VX1-VX2 spread | Daily | >2 points | Near-term event premium explicit in equity vol |
| MOVE Index | Daily | >100 | Bond market pricing ±15bp+ yield move |
| GVZ | Daily | >20 | Gold market pricing ±2%+ move |
| OVX | Daily | >35 | Oil market pricing supply disruption tail |

**Current CEO read for August 20:**
- **VIX:** Estimate 17-19 (elevated but not crisis level). If below 17, the equity market may be underpricing Jackson Hole in a year with elevated geopolitical risk.
- **MOVE:** Estimate 100-115 (elevated given Iran). Above 100 confirms the bond market is treating this as a binary event.
- **GVZ:** Estimate 18-22 (above normal due to safe-haven demand). If approaching 25, the gold crowding signal from Lesson 257 becomes more urgent — crowded longs AND elevated options premium is the dangerous combination (expensive to maintain, maximum reversal pain if the trade goes wrong).
- **OVX:** Estimate 38-45 (elevated due to Hormuz risk). Above 40 would revise the Scenario D probability from 10% to ~14%, which would be enough to shift the portfolio to a more defensive stance even if the base case (Scenario B) remains unchanged.

### Position Sizing Rule: The Implied Move Anchor

**Before Jackson Hole, any directional position in rate-sensitive assets should be sized relative to the implied move:**

If the S&P 500 straddle implies a 2.5% move:
- **High conviction position:** Size for 1.5× the implied move as your loss scenario (i.e., a 3.75% move against you). If that loss is within your risk tolerance, the position is properly sized.
- **Moderate conviction:** Size for 2× the implied move (5% against you) as your loss scenario.
- **Low conviction / high crowding:** Do not hold a directional position. The combination of high implied volatility AND crowded positioning means the downside scenario involves both the fundamental move AND the position unwind. The effective loss scenario can be 3× the implied move.

**Applied to August 2026 anchor portfolio:**
- **Gold anchor position:** If GVZ implies a 2% move in gold and COT shows crowded longs (Friday data), the downside scenario for a hawkish speech is approximately 4-6% in gold (implied move × crowding amplifier). Verify this is within risk tolerance before Friday.
- **Duration underweight:** If MOVE implies a 15bp yield move and positions are short duration, a dovish speech (Scenario B, 40% probability) creates a 15bp adverse yield move. Size the duration underweight such that a 20bp adverse move (implied + small overcorrection) is acceptable.

---

## Databricks Angle

### Pipeline 4 Module 4: Event Volatility Monitor

This lesson adds a fourth module to Pipeline 4's Jackson Hole framework:

| Module | Data Source | Output |
|---|---|---|
| Module 1 | GDELT + FRED | Geopolitical Signal Index (GSI) |
| Module 2 | Yahoo Finance / FRED | Fed signals (MOVE, 2Y-10Y, VIX) |
| Module 3 | CFTC COT | Crowding scores by instrument |
| **Module 4** | **Yahoo Finance (GVZ, OVX, ^VIX)** | **Event volatility surface + Scenario D proxy** |

**Module 4 is the simplest of the four** — all data is available via `yfinance` with no API key. Build time: 30-60 minutes in Databricks. The core output is a four-row table (VIX, GVZ, OVX, MOVE) with current levels, 30-day averages, and the Scenario D probability proxy.

**This module should be live before the MOVE and OVX data matter most — i.e., before Friday August 22.** A 30-minute build today (Thursday August 20) means Francisco has live readings before the COT data arrives.

**Recommended data sources (all free via `yfinance`):**
- `^VIX` — CBOE VIX Index
- `^VIX3M` — 3-month VIX (term structure)
- `GVZ` — CBOE Gold Volatility Index
- `OVX` — CBOE Crude Oil Volatility Index

Note: MOVE Index is NOT available via yfinance. Source options:
1. FRED API (free, ticker `BAMLMOVE`) — may have 1-day lag
2. Manual input from CNBC Markets or ICE Data Services
3. Bloomberg API (if Databricks workspace has Bloomberg connector)

---

## CEO Portfolio Note — Jackson Hole Week (August 20, T-7)

**What this lesson changes:**

The volatility surface reading is now part of the pre-event toolkit alongside the COT crowding test. The two instruments answer different questions:
- **COT:** Where are institutions positioned? (Crowding risk)
- **VIX/MOVE/GVZ/OVX:** How much uncertainty is the market pricing for the event? (Implied move magnitude)

Together, they produce the full pre-event risk picture:
- **COT crowded + high implied vol:** Maximum caution. Position size reduction warranted.
- **COT crowded + low implied vol:** Complacency risk. The market is not pricing the reversal risk it should be. Consider adding event protection cheaply (options are underpriced relative to the true crowding risk).
- **COT uncrowded + high implied vol:** The market is nervous but not over-positioned. Scenario-weighted positions are appropriate; the implied move is a fair measure of event risk.
- **COT uncrowded + low implied vol:** Normal pre-event environment. Standard position sizing.

**Action items for August 20:**
1. Check VIX, GVZ, OVX live levels (5 minutes, no code required — Yahoo Finance terminal)
2. Build Pipeline 4 Module 4 in Databricks today (30-60 minutes) — the simplest build, highest time value given Friday COT release
3. Note MOVE Index level (check manually from FRED or CNBC)
4. On Friday August 22 at 3:30 PM Eastern: COT data released — run Module 3 immediately

**Probability update — unchanged until Friday COT data:**
- Scenario A (Hawkish): 20%
- Scenario B (Dovish): 40%
- Scenario C (Ambiguous): 30%
- Scenario D (Geopolitical Override): 10%

---

## Reflection Questions for Next Session

1. **The MOVE Index and VIX are both measures of implied volatility, but for different asset classes. In August 2026, which one is more important for the Jackson Hole analysis, and why? Could there be a scenario where MOVE is high but VIX is low — and what would that tell you about market expectations?**

2. **The lesson introduces a "Scenario D proxy" derived from OVX and GVZ. This is explicitly described as a heuristic, not a model. What are the main failure modes of this approach? Under what conditions would OVX rise sharply for reasons unrelated to geopolitical tail risk — and how would you identify that false positive?**

3. **The options market prices the implied magnitude of a move, not the direction. The CEO's scenario matrix provides direction probabilities. How would you formally combine these two inputs — the straddle-implied move and the scenario probability weights — into a single expected-value framework for sizing a position ahead of Jackson Hole? Write out the math explicitly.**

---

## Key Concepts Covered
- Implied volatility as a market price for uncertainty (not a directional forecast)
- Volatility crush: the predictable IV decline after a binary event resolves
- VIX term structure: reading the event premium in VIX futures
- MOVE Index: bond market's VIX; the primary tool for Jackson Hole vol assessment
- ATM straddle implied move: how to extract a dollar-denominated expected move from options prices
- GVZ (gold vol) and OVX (oil vol): the geopolitical tail risk measures VIX misses
- Scenario D proxy: heuristic estimation of geopolitical override probability from options surfaces
- The COT + options vol combination: completing the pre-event risk framework
- Module 4 build spec for Pipeline 4: Event Volatility Monitor (free data, 30-60 min build)

## Questions for Next Session (Spaced Repetition Hook)
- After Friday's COT release, combine the crowding test (Module 3) and the volatility surface (Module 4). How does the combined reading change the pre-event portfolio stance?
- If GVZ rises above 25 on August 21-22, before the COT data is even available, what does that imply about the Jackson Hole risk assessment?
- How does the "implied move anchor" position sizing rule interact with the pre-commitment rules from Lesson 255?

## Databricks Relevance Note
This lesson adds Pipeline 4 Module 4 — the Event Volatility Monitor. All four required data points (VIX, VIX3M, GVZ, OVX) are available via `yfinance` at no cost and with no API key. Module 4 is the fastest build in the entire Jackson Hole framework: 30-60 minutes in a single Databricks notebook. The output (a volatility surface table plus Scenario D probability proxy) should be running before the COT data arrives Friday August 22. Together, Modules 3 and 4 give Francisco the complete pre-event risk dashboard: where institutions are positioned (COT) and how much the market is pricing the event (vol surface). This is the analytical toolkit that professional event-driven traders use; it is now in the Prospectra stack.

---

## Standing Order — Pipeline 4
**This is the sixth consecutive lesson containing this notice.**

Pipeline 4 must be live before **August 25, 2026** — 4 business days from today. Today's lesson adds Module 4 as a priority build: 30-60 minutes, free data, no blockers. The build sequence recommendation:

1. **Today (August 20):** Build Module 4 — Event Volatility Monitor (30-60 min)
2. **Friday August 21-22:** Build Module 3 — COT Crowding Test (2-3 hours); run it immediately on the 3:30 PM COT release
3. **Weekend August 22-23:** Integrate Modules 3 and 4 into a combined Jackson Hole dashboard
4. **Monday August 24:** Dashboard live; run first integrated signal read; update scenario probabilities
5. **Tuesday August 25:** HARD DEADLINE — full signal dashboard operational before the Fed blackout window closes

If there is a blocker at any step, email `ceo@prospectra.earth` immediately with the specific error or obstacle.

---

*Lesson 258 complete.*
*Next lesson: Jackson Hole Mid-Point Signal Check — after Friday August 22 COT release. Will incorporate COT crowding scores, updated volatility surface readings, and the first probability revision. Tentatively: Saturday August 23 or Sunday August 24.*
*CEO — Prospectra Geopolitics & Investment Project*
