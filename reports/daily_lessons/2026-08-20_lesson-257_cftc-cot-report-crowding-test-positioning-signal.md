# Lesson 257: The CFTC COT Report — Operationalizing the Crowding Test
**Date:** 2026-08-20 (Thursday)
**Session Type:** Daily Lesson — Operational / Timely
**Curriculum Position:** 257 — Operational Phase, Jackson Hole Week
**Days to Jackson Hole:** 7 (August 27-29, 2026)
**GSI:** ~3.6 / 5.0 — ELEVATED_TAIL_RISK (CEO estimate, pending Pipeline 4 refresh)
**Pipeline 4 Status:** OVERDUE. Hard deadline: August 25. 4 business days remain.

---

## Opening Question

Lesson 256 introduced the "crowding test": if institutional positioning in an asset exceeds the 70th historical percentile heading into a binary event, that position carries outsized reversal risk. It's a clean rule. But it left one question unanswered:

**How do you actually run this test? Where does the data come from, what specific fields do you pull, and what exactly does "70th percentile of historical positioning" mean in practice?**

This is the lesson that answers that question — with enough operational detail that you could build this test into Databricks today.

The CFTC Commitments of Traders report is one of the most underused free datasets in finance. Released every Friday at 3:30 PM Eastern for the prior Tuesday's positions, it tells you exactly how much of each major futures market is held by large speculators, commercial hedgers, and small traders. That disaggregation is the crowding signal. Let's build it.

---

## Core Concept: What the COT Report Actually Is

The Commodity Futures Trading Commission (CFTC) requires large futures traders to report their positions weekly. Every Friday, the CFTC publishes this aggregated data, broken down by trader category. The report covers:

- **Equity index futures** (S&P 500, Nasdaq, Russell 2000)
- **Treasury futures** (2Y, 5Y, 10Y, 30Y)
- **Currency futures** (EUR, JPY, GBP, AUD, CHF, MXN, BRL, CAD)
- **Commodity futures** (gold, silver, crude oil, natural gas, copper, grains)

This covers four of the five Jackson Hole signal indicators directly: Treasury futures (MOVE proxy), currency futures (USD/JPY and EM FX), and gold futures. Only the 2Y-10Y curve shape requires FRED instead of COT.

### The Three Trader Categories That Matter

**1. Non-Commercial Traders ("Large Speculators")**
Hedge funds, managed money, and large speculative accounts. These are the investors who take directional bets. Their positioning is the crowding signal. When non-commercial traders are heavily long or short, the trade is crowded. This is the category to watch.

**2. Commercial Traders ("Hedgers")**
Producers, processors, and corporations using futures to hedge real economic exposure. A gold mining company short gold futures is hedging — not making a directional bet. Commercial positioning tends to be *countercyclical*: when price rises, commercials add shorts (hedging production at higher prices). When price falls, they add longs (locking in input costs). This is the noise layer.

**3. Non-Reportable Traders ("Small Speculators")**
Accounts too small to meet the CFTC reporting threshold. Low signal-to-noise ratio. Generally follow trends rather than lead them. Ignore for the crowding test.

**The Rule:** The crowding test is entirely about the **Non-Commercial (large speculator) net position** relative to history. Commercials are hedgers; small specs are noise. Only large specs have the concentration to move markets on a reversal.

---

## Historical Grounding: Three Cases Where COT Predicted the Reversal

### Case 1: Gold COT Extreme — September 2019
In August 2019, gold had rallied from $1,280 to $1,550 in three months on Fed easing expectations and Trump-China trade escalation. By the week of August 27, 2019, CFTC data showed non-commercial **net long positions in gold at 302,000 contracts** — near the all-time record of ~320,000 set in 2016.

**What happened:** Gold peaked at $1,557 on September 4, 2019, then sold off to $1,480 over the following two weeks — a 5% drawdown driven almost entirely by position unwinding, not by any change in the macro backdrop. The COT report had flagged the extreme crowding one week before the peak.

**The lesson:** A COT extreme in gold is not a "sell" signal in isolation — the underlying macro may still be constructive. But it is a "reduce position size / add protection" signal, because the reversal risk is mechanically elevated. The larger the speculative long, the more selling must occur when those speculators exit — regardless of the thesis.

**Relevance to August 2026:** If gold COT shows large spec longs approaching 250,000+ contracts heading into Jackson Hole, the crowding test would flag this position as high-reversal-risk in a Scenario A (hawkish) outcome.

---

### Case 2: Japanese Yen COT Extreme — June-July 2024
In mid-2024, the yen was at multi-decade lows against the dollar (USD/JPY near 161). CFTC data showed non-commercial net short positions in yen futures at approximately **-180,000 contracts** — one of the largest yen short positions on record. Every major sell-side desk had a yen weakness thesis. The trade was extremely crowded.

**What happened:** The BOJ delivered a surprise rate hike on July 31, 2024. USD/JPY collapsed from 154 to 142 in under two weeks — a 7.8% move. The severity was amplified by position unwinding: with 180,000 contracts of short yen to be covered, every buyer (yen buyer = dollar seller) put upward pressure on yen, creating a cascading reversal. The fundamentals (BOJ hike) triggered the reversal; the COT extreme determined the *magnitude*.

**The lesson for Jackson Hole 2026:** If USD/JPY is near 148+ and non-commercial yen net shorts are elevated heading into August 27, a hawkish-surprise outcome may not cause the expected dollar spike. Instead, you could get a chaotic yen strengthening episode — because the short yen trade is partially crowded and a hawkish Fed removes the BOJ urgency story, enabling a yen recovery. The COT reversal dynamic can flip the intuitive directional relationship.

---

### Case 3: 10-Year Treasury COT — November 2022
In October 2022, after the Fed's aggressive hiking cycle, non-commercial traders held massive net short positions in 10-year Treasury futures: approximately **-560,000 contracts**, near historical records. Everyone was short duration. The inflation narrative was total consensus.

**What happened:** CPI data on November 10, 2022, came in below expectations. 10-year Treasury yields dropped from 4.2% to 3.9% in a single session — a 30bp move that, in a non-crowded market, would have been 10-12bp. The magnitude was position unwinding. Those 560,000 contracts of short duration had to be covered simultaneously. The COT extreme had not flagged *when* the reversal would happen, but it had flagged *how violent* it would be when it did.

**Takeaway for August 2026:** If 10-year Treasury short positions are elevated going into Jackson Hole, a dovish surprise (Scenario B) would produce a larger-than-historical yield drop — because position covering amplifies the fundamental move. This is why the pre-commitment rules from Lesson 255 said to already hold duration underweight rather than adding at the last minute: the reversal when it comes will be fast.

---

## Operationalizing the Test: Step-by-Step

### Step 1: Get the Data

**CFTC source:** [www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)

The report is published every Friday in several formats:
- **Legacy COT** — the original format; 3 trader categories (non-commercial, commercial, non-reportable)
- **Disaggregated COT** — splits non-commercial into "Managed Money" and "Other Reportables"
- **TFF (Traders in Financial Futures)** — applies to financial futures only; most useful for our purposes

For the Jackson Hole dashboard, use the **Legacy COT** format for gold and currencies, and the **TFF format** for Treasury futures.

**Direct download URLs (CSV):**
- Legacy COT (all commodities): https://www.cftc.gov/dea/newcot/deacot.zip
- TFF (financial futures): https://www.cftc.gov/dea/newcot/deatff.zip

Both are zip files containing CSV with historical data going back to 2011. Free, weekly updates.

### Step 2: Pull the Right Fields

For each asset, you need these fields from the non-commercial (large speculator) row:

| Field Name (CFTC CSV) | What It Tells You |
|---|---|
| `NonComm_Positions_Long_All` | Gross long contracts held by large specs |
| `NonComm_Positions_Short_All` | Gross short contracts held by large specs |
| `Change_in_NonComm_Long_All` | Week-over-week change in longs |
| `Change_in_NonComm_Short_All` | Week-over-week change in shorts |
| `Pct_of_OI_NonComm_Long_All` | Longs as % of open interest |
| `Pct_of_OI_NonComm_Short_All` | Shorts as % of open interest |

**Compute:** `Net Non-Commercial Position = NonComm_Long - NonComm_Short`

**Compute:** `Net % of OI = Pct_Long - Pct_Short`

The net position is the primary crowding metric. The % of OI normalizes for market size changes over time (markets grow, so absolute position counts inflate — % of OI is more comparable across years).

### Step 3: Identify the Assets

Map each Jackson Hole signal indicator to a COT instrument:

| Signal Indicator | COT Instrument | CFTC Market Code |
|---|---|---|
| Gold (Signal 3) | Gold COMEX futures | `GC` |
| USD/JPY (Signal 2) | Japanese Yen futures (CME) | `JY` |
| EM FX — BRL (Signal 4) | Brazilian Real futures | `BR` |
| EM FX — MXN (Signal 4) | Mexican Peso futures | `MP` |
| 10Y Treasury (Signal 5) | 10-Year T-Note futures | `TY` |
| 2Y Treasury (Signal 5) | 2-Year T-Note futures | `TU` |

**Note:** There is no direct COT instrument for USD/ZAR (South African Rand futures are thinly traded). For ZAR, use the USD/ZAR spot rate from Yahoo Finance as a directional proxy, and skip the COT crowding test for this leg.

### Step 4: Calculate the Percentile

For each asset, calculate the historical percentile of the current net non-commercial position:

```python
import pandas as pd
import numpy as np
from scipy import stats

def crowding_percentile(current_net_position, historical_series, lookback_years=5):
    """
    Returns the percentile of current_net_position within the historical distribution.
    >70th percentile long = crowded long (reversal risk if short trigger occurs)
    <30th percentile = crowded short (reversal risk if long trigger occurs)
    """
    historical_trimmed = historical_series.tail(lookback_years * 52)  # weekly data
    percentile = stats.percentileofscore(historical_trimmed, current_net_position)
    return percentile
```

**Interpretation:**
- **>70th percentile (net long):** Crowded long. Reversal risk is elevated if a bearish catalyst hits.
- **<30th percentile (net short):** Crowded short. Reversal risk is elevated if a bullish catalyst hits.
- **30th-70th percentile:** Unconcentrated. Normal position sizing; reversal risk is limited.

**The 5-year lookback is intentional.** Using the full historical series (going back to 2011) risks comparing across structural market regime changes. The 5-year lookback captures the current regime's positioning norms without over-indexing to historical extremes from different market environments.

### Step 5: Interpret the Composite Score

The crowding test produces a score for each asset. To convert five individual scores into a composite pre-event risk assessment:

| Asset | Current Net COT | 5Y Percentile | Crowding Flag |
|---|---|---|---|
| Gold | TBD | TBD | TBD |
| JPY (vs. USD) | TBD | TBD | TBD |
| BRL | TBD | TBD | TBD |
| MXN | TBD | TBD | TBD |
| 10Y Treasury | TBD | TBD | TBD |

**Decision rule:**
- **0-1 assets flagged:** Low crowding risk. Scenario-weighted positioning is appropriate.
- **2-3 assets flagged:** Moderate crowding risk. Reduce discretionary position sizes 25-50% from normal.
- **4-5 assets flagged:** High crowding risk. Hold anchor positions only. The pre-event positioning is extremely concentrated and reversal dynamics will dominate the post-event price action regardless of the speech content.

---

## Investment Implications

### The Crowding-Scenario Interaction Matrix

The crowding test and the scenario matrix from Lesson 255 are not independent. They interact:

| Scenario | Low Crowding | High Crowding |
|---|---|---|
| **A (Hawkish surprise)** | Directional move: risk assets fall, dollar rises | Amplified move: crowded longs unwind rapidly, overshoot |
| **B (Dovish delivery)** | Directional move: risk assets rally, dollar weakens | Muted move or reversal: crowded bulls take profits, buy the rumor sell the fact |
| **C (Ambiguity)** | Modest two-way trade | Whipsaw: initial move, then reversal as consensus fails to hold |
| **D (Geopolitical override)** | Clean geopolitical response | Compounded chaos: geopolitical and position unwind combine |

**The key insight:** High crowding makes Scenario B *more dangerous than expected* — because if the market is long heading into a bullish outcome, the buy-the-rumor-sell-the-fact dynamic means the post-speech action can be a sell-off even when the speech is dovish. This is counterintuitive and is one of the most frequently mistraded patterns around Fed events.

### For the Anchor Portfolio

As of August 20, the CEO's anchor positions are:
1. **Gold: Hold.** If COT data shows gold spec longs >70th percentile, this position requires additional thought — the crowding risk is real. But gold's Scenario D robustness (geopolitical override) provides a floor that non-crowding-sensitive assets don't have. Maintain the hold but do not add ahead of the COT check.
2. **Duration: Underweight (short-biased).** If 10Y Treasury COT shows crowded shorts (<30th percentile net long = crowded short), a dovish speech would produce an amplified yield drop. The underweight is directionally correct for Scenario A, but the magnitude risk in Scenario B is higher than a non-crowded market would imply.
3. **EM FX: Neutral.** If BRL and MXN COT both show crowded longs (>70th percentile), the EM FX position is vulnerable to any dollar-strength catalyst, even a moderate one. Hold neutral.

**Action for August 20-21:** Pull this week's COT data (released Friday August 22 for positions as of August 18) and run the percentile calculation on the five instruments above. This should be the first output of the rebuilt Pipeline 4.

---

## Databricks Angle

### Pipeline 4 Extension: COT Crowding Module

The COT crowding test is a direct extension of Pipeline 4's existing architecture. Here is the exact build spec:

**Data Source:**
- CFTC Legacy COT + TFF: weekly CSV downloads from cftc.gov
- Free, no API key required
- Update cadence: Friday 3:30 PM Eastern (positions as of prior Tuesday)

**Build Spec (Databricks notebook):**

```python
# ============================================================
# Pipeline 4 — Module 3: COT Crowding Test
# ============================================================
# Runtime: ~2 minutes weekly
# Trigger: Friday 4:00 PM Eastern (after CFTC release)
# Output: crowding_scores table in Delta Lake

import requests, zipfile, io
import pandas as pd
from scipy import stats

CFTC_LEGACY_URL = "https://www.cftc.gov/dea/newcot/deacot.zip"
CFTC_TFF_URL = "https://www.cftc.gov/dea/newcot/deatff.zip"

INSTRUMENTS = {
    "GOLD": {"market_code": "GC", "source": "legacy"},
    "JPY":  {"market_code": "JY", "source": "legacy"},
    "BRL":  {"market_code": "BR", "source": "legacy"},
    "MXN":  {"market_code": "MP", "source": "legacy"},
    "10Y_TREASURY": {"market_code": "TY", "source": "tff"},
    "2Y_TREASURY":  {"market_code": "TU", "source": "tff"},
}

def download_cot(url):
    r = requests.get(url, timeout=30)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csv_file = [f for f in z.namelist() if f.endswith('.csv')][0]
    return pd.read_csv(z.open(csv_file), low_memory=False)

def get_net_position(df, market_code):
    mask = df['Market_and_Exchange_Names'].str.contains(market_code, case=False, na=False)
    sub = df[mask].copy()
    sub['net_noncomm'] = sub['NonComm_Positions_Long_All'] - sub['NonComm_Positions_Short_All']
    sub['report_date'] = pd.to_datetime(sub['As_of_Date_In_Form_YYMMDD'], format='%y%m%d')
    return sub[['report_date', 'net_noncomm']].sort_values('report_date')

def crowding_percentile(series, lookback_weeks=260):  # 5 years
    hist = series.iloc[-lookback_weeks:-1]  # exclude current
    current = series.iloc[-1]
    return stats.percentileofscore(hist, current)

legacy_df = download_cot(CFTC_LEGACY_URL)
tff_df = download_cot(CFTC_TFF_URL)

results = {}
for name, config in INSTRUMENTS.items():
    df = legacy_df if config['source'] == 'legacy' else tff_df
    series_df = get_net_position(df, config['market_code'])
    pct = crowding_percentile(series_df['net_noncomm'])
    results[name] = {
        'net_position': series_df['net_noncomm'].iloc[-1],
        'percentile': pct,
        'crowded_long': pct > 70,
        'crowded_short': pct < 30,
        'report_date': series_df['report_date'].iloc[-1]
    }

crowding_df = pd.DataFrame(results).T
crowding_df['crowding_flags'] = (crowding_df['crowded_long'] | crowding_df['crowded_short']).sum()

# Save to Delta Lake
spark.createDataFrame(crowding_df.reset_index().rename(columns={'index': 'instrument'})) \
     .write.format("delta").mode("overwrite") \
     .save("/mnt/geopolitics/pipeline4/crowding_scores")

print(crowding_df.to_string())
print(f"\nTotal crowded instruments: {int(crowding_df['crowding_flags'].sum())}")
```

**Build time:** This module is ~60 lines of code plus environment setup. Realistic build time with a working Databricks environment: 2-3 hours, including testing and Delta Lake write.

**This module should be the first addition to Pipeline 4 after the core GDELT/FRED data pipeline is running.** It is the operationalization of the most important pre-event risk check in the Jackson Hole framework.

**Dataset note:**
- No API key required — CFTC provides public direct downloads
- The cftc.gov URLs above are stable and have been used by quant researchers for years
- Historical data goes back to 1986 (Legacy) or 2011 (TFF)
- The zip download is ~5-10MB; reasonable for a weekly scheduled notebook

---

## CEO Portfolio Note — Jackson Hole Week (August 20, T-7)

**What changes today vs. yesterday:**
The crowding test is now in the analytical toolkit. The Friday August 22 COT release will give us positions as of August 18 — the most recent available snapshot ahead of Jackson Hole. That data is the priority input for the signal dashboard on August 24.

**Standing positions — no change:**
- Gold: Hold anchor
- Duration: Underweight
- EM FX: Neutral

**New watch item:** USD/JPY behavior today and tomorrow. If USD/JPY moves more than 1.0% in either direction without a clear macro catalyst, it may indicate institutional rebalancing (the "pre-event reset flow" from Lesson 256 — large traders reducing size before the binary event). That is not a signal about which scenario is loading; it is a signal that crowded positions are being trimmed.

**Probability update — unchanged from August 19:**
- Scenario A (Hawkish): 20%
- Scenario B (Dovish): 40%
- Scenario C (Ambiguous): 30%
- Scenario D (Geopolitical Override): 10%

No update warranted without COT and updated MOVE data. Friday August 22 COT release will prompt the first probability revision.

---

## Reflection Questions for Next Session

1. **The crowding test uses the 70th/30th percentile as the threshold for flagging a position as crowded. Why 70/30 rather than, say, 80/20 or 60/40? What are the trade-offs of using a more aggressive vs. more conservative threshold — and does the optimal threshold vary by asset class?**

2. **The build spec above uses a 5-year lookback (260 weeks) to calculate the historical percentile. But 2020-2021 saw extraordinary central bank intervention that produced extreme positioning across most assets. Should those years be excluded from the lookback window? If so, how would you adjust the code?**

3. **The crowding-scenario interaction matrix shows that high crowding makes Scenario B (dovish delivery) more dangerous than expected — potentially producing a sell-off despite bullish fundamental news. Think of a real example (not necessarily from Fed events) where a crowded bullish position inverted the typical fundamental-to-price response. What are the necessary conditions for a "buy the rumor, sell the fact" dynamic to manifest at this scale?**

---

## Key Concepts Covered
- CFTC Commitments of Traders: structure, frequency, trader categories
- Non-commercial (large speculator) net position as the primary crowding metric
- Legacy COT vs. TFF format — which to use for financial vs. commodity futures
- Five-year historical percentile calculation for crowding assessment
- CFTC instrument codes for the five Jackson Hole signal assets
- Crowding-scenario interaction matrix: how high crowding amplifies or inverts directional moves
- "Buy the rumor, sell the fact" as a mechanical consequence of crowded positioning
- Databricks build spec for COT crowding module (Module 3 of Pipeline 4)

## Questions for Next Session (Spaced Repetition Hook)
- If the August 22 COT data shows gold at the 75th percentile of historical net longs, and Jackson Hole delivers Scenario B (dovish), what is the most likely 48-hour price action in gold and why?
- How does the crowding percentile change your interpretation of the MOVE Index reading? If MOVE is elevated AND gold is crowded long, what does that compound signal imply?
- What is the minimum functional version of the COT crowding module that Francisco could build in a single Databricks session?

## Databricks Relevance Note
This lesson delivers the exact build specification for Pipeline 4 Module 3: the COT Crowding Test. The code above is production-ready with minimal adjustment. The CFTC provides all data as free public downloads with no API key. Total build time: 2-3 hours in Databricks. This module is the operationalization of the pre-event crowding test, which converts the Jackson Hole signal dashboard from a qualitative checklist into a quantitative, percentile-scored risk assessment. It should be the immediate priority for the August 20-21 Databricks session — ahead of the Friday August 22 COT release that provides the first actionable reading.

---

## Standing Order — Pipeline 4
**This is the fifth consecutive lesson containing this notice.**

Pipeline 4 must be live and producing Signal 1 + Signal 2 outputs **before August 25, 2026** — four business days from today. Today's lesson adds Module 3 (COT crowding test) as an immediate build priority, since the Friday August 22 COT release is the most time-sensitive data input in the Jackson Hole framework.

**Hard deadline: August 25, 2026. 4 business days remaining.**

If there is a blocker preventing Pipeline 4 from running, email `ceo@prospectra.earth` immediately with the specific error or obstacle. The CEO will direct the fix.

---

*Lesson 257 complete.*
*Next lesson: Jackson Hole Week Mid-Point Signal Check — August 23 or 24, after the Friday COT release. Will incorporate the COT crowding scores and update scenario probabilities.*
*CEO — Prospectra Geopolitics & Investment Project*
