# Lesson 248: Pipeline 3 Architecture — US-China Diplomatic Reset Monitor
**Date:** 2026-08-14 (Friday)
**Session Type:** Engineering Phase — Pipeline Architecture Preview
**Curriculum Position:** 248 — Engineering Phase, Session 11
**Pipeline 4 Deadline:** August 15, 2026 — **TOMORROW**
**Pipeline 2-A Deadline:** September 12, 2026 — 29 days
**Pipeline 2-B Deadline:** October 3, 2026 — 50 days
**Pipeline 3 Deadline:** October 31, 2026 — 78 days

---

## CEO Opening Question

The May 2026 Trump-Xi Beijing summit produced a "managed trade" truce: $17 billion in annual US agricultural purchases, a bilateral board of trade for non-sensitive goods, selective tariff reductions, and vague Chinese commitments on critical minerals. The analyst community has already called it "unlikely to be sustainable."

Here is the question for today:

**If the truce is fragile — if Taiwan, tech restrictions, and industrial subsidies remain unresolved — then is the US-China relationship *de-escalating* or merely *pausing*? And if the distinction matters for portfolio construction, how do you build a pipeline that can tell the difference?**

This is the architectural challenge that makes Pipeline 3 harder to build than Pipelines 2-A or 2-B. The BOJ hiking cycle has a scheduled meeting calendar. Iran's nuclear enrichment has quantitative thresholds. US-China diplomatic relations have neither. They evolve continuously, ambiguously, and reversibly. The pipeline must distinguish genuine normalization from tactical ceasefire — and do so with freely available data.

That is what we are building today.

---

## Why Pipeline 3 Is the Most Difficult in the GSI Architecture

### The Three Signal Types

| Signal | What it measures | Nature of change | Early warning possible? |
|---|---|---|---|
| Signal 1 — BOJ | Interest rate differential / carry unwind | Threshold event (rate decision) | Yes — meeting calendar |
| Signal 2 — Iran | Nuclear threshold proximity | Binary crossing (no calendar) | Yes — GDELT enrichment news |
| Signal 3 — US-China | Diplomatic relationship quality | Continuous spectrum | Partially — GDELT tone, equity proxies |

Signals 1 and 2 measure **stress escalation** — they go from low to high when something bad is happening. Pipeline 3 measures something fundamentally different: **the degree of normalization** in the world's most consequential bilateral relationship. This creates three architectural problems that do not exist in the other pipelines:

---

### Problem 1: The Inversion Problem

In the GSI formula, Signal 3 is used as a *stress* input — but Pipeline 3 measures *de-escalation*. The two are related but not identical:

```
china_stress = 6.0 - china_reset_score
```

When Pipeline 3 shows a high reset score (strong de-escalation), china_stress is low, and the GSI is pulled down. When Pipeline 3 shows a low reset score (relationship deteriorating), china_stress is high, and the GSI is pulled up.

This inversion is intentional: the US-China relationship is the structural backdrop for the entire geopolitical risk regime. High normalization → other risks are contained in a stable systemic environment. High deterioration → every other risk is amplified because the two superpowers are not cooperating to manage them.

The May 2026 trade deal moved the CEO's judgmental estimate from 3.2 (previously DETERIORATING) to 3.8 (MANAGED PAUSE). But the analyst warning — "unlikely to be sustainable" — is itself a data point the pipeline should eventually detect.

---

### Problem 2: The Slow-Moving Variable Problem

Signal 1 (BOJ carry) can move from 2.0 to 4.5 in a single trading day if the BOJ surprises with a hike. Signal 2 (Iran) can move from 2.5 to 4.0 overnight if the IAEA detects 90% HEU enrichment.

Signal 3 (US-China) moves on a different clock:
- A tariff increase takes weeks to implement after announcement
- A diplomatic chill takes months to produce observable trade data
- A technology restriction takes years to produce chip supply chain effects

**Design implication:** Pipeline 3 should use a longer lookback window than Pipelines 2-A and 2-B. The GDELT window in P2-A and P2-B is 7 days. Pipeline 3 should use a 14-day primary window and a 30-day trend window — because a 7-day blip in US-China headlines does not move the structural relationship.

---

### Problem 3: The Symmetry Problem

US-China headlines are generated continuously and in large volume. Unlike Iran nuclear news — which is distinguishable between "background noise" and "threshold approach" — US-China news has no clear threshold to detect. Every week produces:
- Trade enforcement news (routine)
- Technology restriction updates (semi-routine)
- Taiwan proximity incidents (infrequent, high importance)
- Diplomatic engagement signals (variable frequency)
- Chinese economic data (high frequency, variable relevance)

The pipeline cannot simply count articles. It must weight them by diplomatic significance *and* distinguish between bilateral signaling (where both sides are deliberately communicating) and unilateral pressure (where one side is ratcheting up coercion undetected by the other).

This requires a more sophisticated keyword architecture than Pipeline 2-B — four distinct signal layers, not two.

---

## The Four-Layer Architecture of Pipeline 3

```
PIPELINE 3: US-China Diplomatic Reset Monitor
Version: 1.0

SIGNAL LAYERS:
  Layer 1: GDELT Diplomatic Tone Score
             → Measures: quality of diplomatic engagement (meetings, statements, agreements)
             → Primary signal for genuine normalization vs. tactical truce
  
  Layer 2: GDELT Trade Normalization Score
             → Measures: observable trade cooperation indicators (tariff cuts, purchase agreements)
             → Confirms diplomatic words with economic actions
  
  Layer 3: GDELT Taiwan Risk Counter-Signal
             → Measures: Taiwan tension level — the #1 risk to reset sustainability
             → SUBTRACTS from the reset score (more Taiwan tension = less trust in the reset)
  
  Layer 4: Equity Proxy Score
             → Measures: COPX, MCHI, KWEB, BHP/RIO market behavior
             → Markets confirm or deny what diplomatic language claims

OUTPUTS:
  1. diplomatic_tone_score:       float (1.0–5.0) — GDELT diplomatic engagement quality
  2. trade_normalization_score:   float (1.0–5.0) — trade cooperation confirmation
  3. taiwan_counter_score:        float (0.0–2.0) — subtracted from reset (more tension = lower reset)
  4. equity_proxy_score:          float (1.0–5.0) — market confirmation
  5. china_reset_score:           float (1.0–5.0) — GSI Signal 3 input (5.0 = full normalization)
  6. us_china_regime:             string — "DETERIORATING" / "COLD_PEACE" / "MANAGED_PAUSE" / "NORMALIZATION" / "RESET_ACHIEVED"

FREQUENCY: Daily (run at 7:00 UTC — 30 minutes after Pipeline 2-B)
DESTINATION: Delta table `geopolitics.pipeline3_scores`
ALERT THRESHOLD: china_reset_score drop of 0.5+ in 14-day window → email Bolo
                  taiwan_counter_score > 1.5 → email Bolo (Taiwan escalation overriding reset)
```

The regime labels are designed to communicate the *quality* of the relationship, not just its direction:

| Regime | china_reset_score | Meaning |
|---|---|---|
| DETERIORATING | 1.0–2.0 | Active coercion / tariff escalation / diplomatic breakdown |
| COLD_PEACE | 2.0–3.0 | No active escalation but no cooperation; strategic competition at full intensity |
| MANAGED_PAUSE | 3.0–3.8 | Tactical truce with unresolved structural issues (current state, Aug 2026) |
| NORMALIZATION | 3.8–4.5 | Genuine bilateral cooperation emerging; structural issues being addressed |
| RESET_ACHIEVED | 4.5–5.0 | Strategic competition receding; sustained bilateral institutions emerging |

The CEO's current judgmental estimate (3.8) sits at the boundary between MANAGED_PAUSE and NORMALIZATION. This is deliberate: the May 2026 deal produced enough diplomatic activity to qualify as normalization on paper, but the "unlikely to be sustainable" assessment means the structural foundation is not there yet.

---

## Pipeline 3 Full Architecture — The Four GDELT Signal Layers in Detail

### Layer 1: Diplomatic Tone Keywords

These keywords detect *quality* diplomatic engagement — not just that US-China officials spoke, but that they produced cooperative outcomes.

```python
# HIGH-VALUE DIPLOMATIC SIGNALS (push reset score up)
DIPLOMATIC_ENGAGEMENT_KEYWORDS = {
    # Presidential / Head of State level (highest signal value)
    "xi trump meeting": 3.5,
    "xi biden meeting": 3.5,  # Historical fallback
    "us china summit": 3.5,
    "presidential call china": 3.0,
    
    # Institutional engagement (durable signal)
    "us china working group": 2.5,
    "us china trade commission": 2.5,
    "us china strategic dialogue": 3.0,
    "board of trade us china": 3.0,  # May 2026 deal mechanism
    "us china economic dialogue": 2.5,
    "us china military hotline": 3.0,  # Military-to-military = high signal of trust
    "us china military communication": 2.5,
    "us china commander call": 2.8,
    
    # Specific normalization acts
    "us china tariff reduction": 3.0,
    "us china tariff rollback": 3.0,
    "us china sanctions relief": 2.8,
    "us china visa agreement": 2.0,
    "us china scientific cooperation": 2.0,
    "us china climate agreement": 2.2,
    "us china fentanyl cooperation": 2.2,  # A prior concrete output
    
    # Diplomatic language indicating cooperation
    "constructive relationship us china": 2.5,
    "strategic stability us china": 2.5,
    "managing competition us china": 2.0,
    "guardrails us china": 2.0,
    "candid discussions us china": 1.5,
}

# DIPLOMATIC DETERIORATION SIGNALS (push reset score down)
DIPLOMATIC_DETERIORATION_KEYWORDS = {
    "us china sanctions": -2.0,
    "us china decoupling": -2.5,
    "china entity list": -2.0,
    "us china expulsion": -3.0,  # Diplomatic expulsions = serious breakdown
    "us china ambassador recalled": -3.5,
    "us china diplomatic downgrade": -3.5,
    "us china trade war resumed": -3.0,
    "us china tariff increase": -2.5,
    "us china new tariffs": -2.5,
    "china retaliation us": -2.0,
    "us chip ban china": -2.0,
    "us china tech war": -2.2,
}
```

**Calibration logic:**
- Background diplomatic noise (routine meetings, speeches): 20–40 weighted mentions/2 weeks → COLD_PEACE baseline (~2.5)
- Active normalization phase (post-summit follow-through): 60–100 mentions → MANAGED_PAUSE (~3.0–3.8)
- Genuine institutional build-out (working groups, agreements): 100–150 mentions → NORMALIZATION (~3.8–4.3)
- Full reset (historical comparison: Nixon-era opening): 150+ mentions of new cooperation → RESET_ACHIEVED

---

### Layer 2: Trade Normalization Keywords

Diplomatic words without economic follow-through are noise. Layer 2 tracks whether the trade relationship is actually normalizing.

```python
TRADE_NORMALIZATION_KEYWORDS = {
    # Agricultural purchases (core May 2026 deal mechanism)
    "china us agricultural purchase": 2.5,
    "china soybean purchase us": 2.0,
    "china us farm goods": 2.0,
    "china agricultural import us": 2.0,
    
    # Technology / manufacturing re-linkage
    "us china supply chain": 1.8,
    "china us manufacturing": 1.5,
    "apple china production": 1.5,
    "us china investment": 1.8,
    "us china joint venture": 2.0,
    
    # Trade volume signals
    "us china trade surplus": 1.2,       # Low signal — structural, not policy-driven
    "us china trade balance": 1.2,
    "us china exports increase": 2.0,
    "us china imports normalized": 2.0,
    
    # Critical minerals (specific May 2026 deal element)
    "china critical minerals us": 2.5,
    "china rare earth us supply": 2.5,
    "china minerals agreement": 3.0,
}

TRADE_DETERIORATION_KEYWORDS = {
    "china export ban": -2.5,
    "china rare earth ban": -3.0,   # This is a crisis signal
    "china gallium ban": -2.8,
    "china germanium ban": -2.8,
    "us import ban china": -2.0,
    "us china trade deficit widening": -1.5,
    "china dumping us": -1.8,
    "china overcapacity us": -1.8,
    "us anti-dumping china": -1.5,
}
```

**The rare earth trigger:** A Chinese rare earth export ban (gallium, germanium, graphite) is the single most dangerous trade-layer event — it immediately falsifies the "managed pause" thesis and signals that China is weaponizing the reset's goodwill. The pipeline gives it a -3.0 weight and should cross-reference with Pipeline 4 (export controls) for convergence.

---

### Layer 3: Taiwan Counter-Signal

Taiwan is the reset's termination condition. If PLA military activity around Taiwan escalates to the point where the US is forced to respond, the bilateral reset ends — regardless of what the trade board is doing. Layer 3 tracks this counter-signal and subtracts it from the reset score.

```python
TAIWAN_RISK_KEYWORDS = {
    # Military activity (direct escalation signal)
    "pla taiwan strait exercise": 2.5,
    "china military taiwan": 2.0,
    "taiwan strait tension": 2.0,
    "china taiwan military drill": 2.5,
    "pla carrier taiwan": 3.0,
    "china taiwan blockade": 4.0,
    "taiwan invasion china": 4.0,
    "china taiwan war": 4.0,
    
    # Political escalation
    "china taiwan arms sales us": 1.8,
    "us taiwan arms deal": 1.8,
    "taiwan independence declaration": 3.5,
    "china taiwan sanctions": 2.0,
    "china taiwan threat": 1.5,
    
    # Diplomatic crisis
    "us taiwan visit china protest": 1.5,
    "china us taiwan crisis": 2.5,
    "china suspend talks taiwan": 2.5,
}

def compute_taiwan_counter(raw_taiwan_signal):
    """
    Taiwan counter-signal: scored 0.0–2.0, subtracted from reset score.
    
    0.0 = No Taiwan escalation (reset unaffected)
    0.5 = Background Taiwan friction (China protestations, routine)
    1.0 = Elevated Taiwan tension (arms sale, China exercises, minor crisis)
    1.5 = Acute Taiwan tension (large-scale exercises, diplomatic crisis)
    2.0 = Taiwan conflict (blockade, invasion — reset is over)
    
    This cap at 2.0 is intentional: even in a Taiwan crisis, the minimum reset
    floor is 1.0 (not zero) because some bilateral communication channels remain.
    Total China stress ceiling is achieved through china_stress = 6.0 - 1.0 = 5.0.
    """
    if raw_taiwan_signal <= 5:
        return 0.0           # Baseline Taiwan noise
    elif raw_taiwan_signal <= 20:
        return 0.3 + (raw_taiwan_signal - 5) / 15 * 0.5    # 0.3–0.8
    elif raw_taiwan_signal <= 60:
        return 0.8 + (raw_taiwan_signal - 20) / 40 * 0.7   # 0.8–1.5
    elif raw_taiwan_signal <= 120:
        return 1.5 + (raw_taiwan_signal - 60) / 60 * 0.4   # 1.5–1.9
    else:
        return 2.0  # Conflict-level Taiwan escalation
```

**Structural asymmetry:** The Taiwan counter-signal is *additive to stress* (subtracted from reset), but its source events are *fast-moving* in a way that the reset is not. The May 2026 trade deal took 6 months to negotiate. A Taiwan Strait incident takes 72 hours to escalate into a crisis that terminates the reset conversation. Pipeline 3 must have a short-window scan specifically for Taiwan (3-day lookback vs. 14-day for the diplomatic layer).

---

### Layer 4: Equity Proxy Score

The equity proxies answer the question the GDELT data cannot: **Does the market believe the reset is real?**

When diplomats announce cooperation but markets sell Chinese equities and copper miners, that is a signal that the institutional investors — who have more information than GDELT can detect — are not convinced. When markets rally on US-China cooperation news, that is confirmation.

```python
US_CHINA_EQUITY_PROXIES = {
    "COPX":  {"name": "Global X Copper Miners ETF", "signal": "positive",
              "weight": 0.30,
              "rationale": "China consumes ~50% of world copper. Trade normalization → construction/manufacturing acceleration → copper demand."},
    
    "MCHI":  {"name": "iShares MSCI China ETF", "signal": "positive",
              "weight": 0.35,
              "rationale": "Broadest China equity proxy. US-China normalization reduces country-level political risk premium → multiple expansion."},
    
    "KWEB":  {"name": "KraneShares CSI China Internet", "signal": "positive",
              "weight": 0.15,
              "rationale": "China tech sentiment proxy. Already in portfolio — cross-references Signal 3 with active position."},
    
    "BHP":   {"name": "BHP Group ADR", "signal": "positive",
              "weight": 0.20,
              "rationale": "Iron ore demand proxy. Australia-China trade (70% of BHP revenue exposed) is the most direct beneficiary of US-China détente normalizing global trading environment."},
}

def compute_equity_proxy_score():
    """
    Compute equity proxy score: do markets confirm the diplomatic reset?
    
    Logic: compute each proxy's 14-day return (matching Pipeline 3 lookback window).
    Weight by importance. Score the weighted composite return against a calibration
    table that maps portfolio-of-proxies return → reset confirmation score.
    
    Rationale for 14-day vs. 5-day (used in P2-A and P2-B):
    US-China normalization is slow-moving. A 5-day return captures noise (earnings,
    Chinese PMI release, commodity price day-moves). A 14-day return captures the
    structural market response to diplomatic developments.
    
    Returns score 1.0–5.0 where:
    5.0 = All proxies surging (market fully believes the reset)
    3.0 = Mixed signals (market partially convinced)
    1.0 = All proxies declining (market not convinced; diplomatic words are noise)
    """
    import yfinance as yf
    
    proxy_returns = {}
    weighted_return = 0.0
    
    for ticker, meta in US_CHINA_EQUITY_PROXIES.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="30d", interval="1d")
            if not hist.empty:
                close = hist["Close"].dropna()
                if len(close) >= 14:
                    ret_14d = float(close.iloc[-1] / close.iloc[-15] - 1)
                else:
                    ret_14d = float(close.iloc[-1] / close.iloc[0] - 1)
                proxy_returns[ticker] = ret_14d
                weighted_return += ret_14d * meta["weight"]
                print(f"  {meta['name']} ({ticker}): 14d return {ret_14d:+.2%}")
        except Exception as e:
            print(f"  {ticker} fetch error: {e}")
            proxy_returns[ticker] = 0.0
    
    # Map weighted composite return → equity proxy score
    if weighted_return < -0.05:
        equity_score = max(1.0, 1.5 + weighted_return * 10)   # Strong decline → low score
    elif weighted_return < 0:
        equity_score = 1.5 + weighted_return / 0.05 * 0.5      # Mild decline → 1.5
    elif weighted_return < 0.02:
        equity_score = 2.0 + weighted_return / 0.02 * 0.5      # Flat → 2.0–2.5
    elif weighted_return < 0.05:
        equity_score = 2.5 + (weighted_return - 0.02) / 0.03 * 1.0  # 2.5–3.5
    elif weighted_return < 0.08:
        equity_score = 3.5 + (weighted_return - 0.05) / 0.03 * 0.8  # 3.5–4.3
    elif weighted_return < 0.12:
        equity_score = 4.3 + (weighted_return - 0.08) / 0.04 * 0.5  # 4.3–4.8
    else:
        equity_score = min(5.0, 4.8 + (weighted_return - 0.12) / 0.08 * 0.2)
    
    print(f"\n  Weighted composite 14d return: {weighted_return:+.2%}")
    print(f"  EQUITY PROXY SCORE: {equity_score:.2f}/5.0")
    
    return equity_score, proxy_returns, weighted_return
```

**August 14 equity context:** Copper futures have been trading in the $6.40–$6.55 range, with COPX surging on Chinese infrastructure investment pledges in early August, then softening as elevated prices dampened actual demand (Yangshan premium declining from $115 to $96/ton). This mixed signal is consistent with a MANAGED_PAUSE: the trade deal provided a floor, but neither the Chinese economy nor the US-China relationship has produced enough genuine momentum to drive sustained copper outperformance.

Expected equity proxy score in August 2026: **2.8–3.4** — markets are pricing the managed pause correctly, not a full reset.

---

## Composite Score and Regime Classification

```python
def compute_china_reset_score(diplomatic_score, trade_score, taiwan_counter,
                               equity_score):
    """
    Composite: china_reset_score = weighted sum of three signals, minus Taiwan counter.
    
    Weights:
    - Diplomatic tone (GDELT):         35% — diplomatic words are the leading signal
    - Trade normalization (GDELT):     25% — economic follow-through confirms words
    - Equity proxy (market):           40% — markets confirm or deny both
    
    Then: subtract taiwan_counter (0.0–2.0) from the raw weighted sum.
    Floor at 1.0.
    
    Design principle: equity gets the highest weight because it integrates all public
    information. When diplomats say one thing and markets price another, markets
    are usually right on a 14-day horizon.
    """
    raw_reset = (
        diplomatic_score * 0.35 +
        trade_score      * 0.25 +
        equity_score     * 0.40
    )
    
    adjusted_reset = raw_reset - taiwan_counter
    china_reset = min(5.0, max(1.0, adjusted_reset))
    
    # Regime classification
    if china_reset >= 4.5:
        regime = "RESET_ACHIEVED"
        regime_note = "Strategic competition receding — bilateral institutions durable"
    elif china_reset >= 3.8:
        regime = "NORMALIZATION"
        regime_note = "Genuine cooperation emerging — structural issues being addressed"
    elif china_reset >= 3.0:
        regime = "MANAGED_PAUSE"
        regime_note = "Tactical truce — unresolved structural issues, reset not secure"
    elif china_reset >= 2.0:
        regime = "COLD_PEACE"
        regime_note = "No active escalation but no cooperation — strategic competition at full intensity"
    else:
        regime = "DETERIORATING"
        regime_note = "Active coercion or tariff escalation — GSI stress elevated"
    
    return china_reset, regime, regime_note
```

---

## What the First Pipeline 3 Reading Should Show

The CEO's current judgmental estimate for Signal 3 is **3.8 / MANAGED_PAUSE** (set following the May 2026 Trump-Xi summit). Based on the August 14, 2026 market environment:

| Condition | Expected Score | Interpretation |
|---|---|---|
| Diplomatic GDELT flat, COPX/MCHI mixed, no Taiwan | **3.3–3.8** | In line with CEO estimate. Managed pause confirmed. |
| Diplomatic GDELT active (board of trade news), COPX/MCHI rising | **3.8–4.3** | Above CEO estimate. Normalization emerging — KWEB size-up warranted. |
| Taiwan strait incident, COPX/MCHI declining | **2.8–3.3** | Below CEO estimate. Reset fragility confirmed — reduce KWEB. |
| Trade board stalls, China imposes new restrictions | **2.0–3.0** | COLD_PEACE. GSI stress rises. Reverse any KWEB position. |

**CEO's expectation for first Pipeline 3 reading:** 3.3–3.8 / MANAGED_PAUSE

The equity proxies (COPX at $6.45/lb, MCHI showing China at mixed growth signals) are consistent with a market that has priced the managed pause but not a reset. The Yangshan copper premium declining from $115 to $96 suggests China's domestic demand recovery is below the level that would generate genuine copper demand pull — which is consistent with MANAGED_PAUSE, not NORMALIZATION.

---

## GSI v3.0 — The Complete Signal Architecture

When Pipeline 3 goes live on October 31, the GSI will be fully data-driven for the first time. This is the target architecture:

```python
def compute_gsi_v30(boj_score, iran_score, china_reset_score, export_control_score):
    """
    GSI v3.0 — All four signals driven by live pipelines.
    Activated: October 31, 2026
    
    Weights (unchanged from v1.0 design):
    - Signal 1 — BOJ carry unwind:        30%
    - Signal 2 — Iran nuclear threshold:  30%
    - Signal 4 — Export control:          25%
    - Signal 3 — China reset (inverted):  15%
    """
    china_stress = 6.0 - china_reset_score  # Inversion: high reset = low stress
    
    gsi = (
        boj_score           * 0.30 +
        iran_score          * 0.30 +
        export_control_score * 0.25 +
        china_stress        * 0.15
    )
    return min(5.0, max(1.0, gsi))
```

**Why Signal 3 carries only 15%:** The US-China relationship is the most important bilateral relationship in the world — but it changes *slowly*. A fast-moving GSI (responding to BOJ surprises and Iran nuclear threshold news in days) does not benefit from a slow-moving variable at high weight. The 15% weight means Signal 3 provides a persistent structural modifier — a headwind or tailwind that adjusts the risk level without dominating it. It is the background radiation of the GSI.

**Current GSI v2.1 estimate (CEO judgmental):**

| Component | Estimated Score | Weight | Contribution |
|---|---|---|---|
| Signal 1 — BOJ | 3.8 | 0.30 | 1.14 |
| Signal 2 — Iran | 3.5 | 0.30 | 1.05 |
| Signal 4 — Export Control | 3.9 | 0.25 | 0.98 |
| Signal 3 — China reset | 3.8 → stress 2.2 | 0.15 | 0.33 |
| **GSI v2.1 Composite** | — | — | **3.50** |

Portfolio regime: **ELEVATED_TAIL_RISK.** No change from prior sessions. Pipeline 4 confirmation tomorrow (August 15) will replace the Signal 4 estimate with live data.

---

## Pipeline 3 Build Timeline

```
October 31, 2026 — Go-live (78 days)

Pre-requisites:
  ✓ FRED API key (already in secrets from Pipeline 2-A)
  ✓ yfinance (installed on ML Runtime)
  ✓ geopolitics database (created in Pipeline 4 go-live)
  □ No new credentials required — Pipeline 3 uses only GDELT (free) + yfinance (free) + FRED (keyed)

Build sequence:
  Cell 1  — Configuration (GDELT lookback = 14 days, equity lookback = 14 days)
  Cell 2  — Diplomatic tone keywords and Layer 1 GDELT query
  Cell 3  — Trade normalization keywords and Layer 2 GDELT query
  Cell 4  — Taiwan counter-signal keywords and Layer 3 GDELT query (3-day window)
  Cell 5  — Equity proxy score (COPX, MCHI, KWEB, BHP — 14d returns)
  Cell 6  — Composite score and regime classification
  Cell 7  — Portfolio protocol (KWEB, COPX positioning by regime)
  Cell 8  — Write to Delta: geopolitics.pipeline3_scores
  Cell 9  — GSI v3.0 integration (replaces CEO estimate for Signal 3)
  Cell 10 — Cross-pipeline dashboard query (all four signals)

Full code: delivered in Lesson 249 (next session after Pipeline 4 go-live confirmed)
```

The complete code will be delivered as Lesson 249, following the same format as Lessons 246 (Pipeline 2-A) and 247 (Pipeline 2-B). Today's lesson is the architectural preview — understanding *why* Pipeline 3 is built the way it is before seeing *how* it is built.

---

## Databricks Angle — The COPX-GDELT Correlation Study

Pipeline 3 introduces the most interesting testable hypothesis in the entire Databricks project:

**Hypothesis:** Weekly GDELT US-China diplomatic sentiment leads COPX forward 5-day returns by 0–10 trading days.

The mechanism:
1. US-China diplomatic language improves (GDELT detects it first)
2. Market participants who read GDELT or trade headline sentiment begin buying COPX
3. COPX price rises over the following 5–10 days as more investors price the normalization
4. The lag between GDELT signal and COPX return is the alpha window

If this hypothesis holds, Pipeline 3 becomes a *predictive* tool for COPX, not just a descriptive one. The Databricks build that tests it:

```python
# After Pipeline 3 has 90 days of history:
from pyspark.sql.functions import lag, lead, col
from pyspark.sql.window import Window

w = Window.orderBy("run_date")

df = spark.table("geopolitics.pipeline3_scores") \
    .select("run_date", "diplomatic_tone_score", "china_reset_score") \
    .join(
        spark.table("geopolitics.equity_daily")  # COPX, MCHI daily close
            .filter(col("ticker") == "COPX")
            .select("date", "close", "forward_5d_return"),  # pre-computed
        on=[col("run_date") == col("date")],
        how="left"
    )

# Compute rolling correlation: diplomatic_tone_score → COPX forward_5d_return
from pyspark.sql.functions import corr

correlation_df = df.select(
    corr("diplomatic_tone_score", "forward_5d_return").alias("gdelt_copx_correlation")
)

correlation_df.show()
```

**What a strong positive correlation (>0.40) would mean:** The GDELT diplomatic tone score is a leading indicator for copper miner equity performance. This validates the proxy construction thesis and gives the system its first genuinely *predictive* signal, not just a descriptive monitoring tool.

**What a weak correlation (<0.15) would mean:** GDELT headlines lag market pricing — the market sees the diplomatic signals before GDELT volume builds. This would invert the architecture: equity proxies should be the primary signal, GDELT the confirming one. The CEO will adjust Signal 3 weights if the correlation study shows this.

**Dataset to add:** `geopolitics.equity_daily` — a unified daily close table for all proxy tickers (COPX, MCHI, KWEB, BHP, FRO, DHT). This becomes a shared data asset across Pipelines 2-B and 3. **Bolo: when Pipeline 4 is confirmed live, this is the next data engineering task — one table, four tickers, daily yfinance pull, partitioned by date.**

---

## Key Concepts Summary

| Concept | Definition |
|---|---|
| **Inversion problem** | Signal 3 measures de-escalation, but the GSI uses it as a stress input. The formula `china_stress = 6.0 - china_reset_score` converts between the two. High de-escalation → low stress → GSI pulled down. |
| **Managed pause vs. normalization** | A managed pause is a tactical ceasefire with unresolved structural issues (trade deficits, tech restrictions, Taiwan). Normalization is the systematic unwinding of those issues through durable bilateral institutions. The May 2026 trade deal is a managed pause. |
| **Taiwan counter-signal** | The termination condition for the US-China reset. PLA military activity around Taiwan is scored separately (3-day window vs. 14-day for diplomatic layer) because Taiwan escalation moves fast while the reset moves slowly. Scored 0.0–2.0 and subtracted from the reset composite. |
| **Equity proxy weight dominance** | Signal 3 gives 40% weight to equity proxies (vs. 25% in Pipeline 2-B). This reflects the efficient market principle: in a slow-moving variable like US-China relations, market prices integrate all available information faster than GDELT volume does. |
| **COPX-GDELT correlation hypothesis** | The testable prediction that GDELT US-China diplomatic sentiment leads COPX forward returns by 0–10 trading days. If confirmed, Pipeline 3 becomes a predictive tool for copper miner equities — the system's first alpha-generating signal. |
| **GSI v3.0** | The fully data-driven version of the Geopolitical Signal Index, active when Pipeline 3 goes live on October 31, 2026. All four components are pipeline-derived; no CEO judgmental estimates remain in the formula. |

---

## Investment Implications

### The US-China Reset as a Portfolio Modifier

The current MANAGED_PAUSE regime (3.8 → china_stress 2.2) is contributing 0.33 to the GSI composite — the lowest contribution of any signal component. This is structurally correct: a managed pause is better than cold peace, but it is not a reason to take on China exposure.

**What would change the portfolio calculus:**

| Scenario | Pipeline 3 reading | Portfolio action |
|---|---|---|
| Trade board produces concrete tariff cuts | Reset score → 4.2 (NORMALIZATION) | KWEB: size up to 3–4%. COPX: add as commodity exposure. |
| China delivers on rare earth commitments | Reset score → 4.0–4.3 | MCHI: consider adding alongside KWEB |
| Taiwan PLA exercises resume at scale | Reset score → 3.0 (taiwan_counter 0.8+) | KWEB: reduce to 0%. COPX: hold (China stress → copper ambiguous) |
| Trade board stalls, tech restrictions expand | Reset score → 2.5–3.0 (COLD_PEACE) | KWEB: exit. China-adjacent positions: review all |
| China rare earth export ban | Reset score → 1.8–2.5 (DETERIORATING) | Full defensive posture. Cross-reference Pipeline 4 — this is the exact event P4 was built to detect. |

### KWEB Position as the Signal 3 Bellwether

The KWEB starter (1–2%, entered in prior sessions) is the active portfolio expression of Signal 3. It is the only existing position that requires Pipeline 3 to remain in MANAGED_PAUSE or better to be held.

- Signal 3 MANAGED_PAUSE or NORMALIZATION → Hold or add KWEB
- Signal 3 COLD_PEACE → Cut KWEB to 0%, monitor
- Signal 3 DETERIORATING → Full KWEB exit, no re-entry until reset resumes

This makes KWEB the most information-dependent position in the portfolio — its thesis is the most dependent on a single signal (Signal 3) of any active position.

---

## Reflection Questions

**Question 1 — The slow vs. fast variable calibration problem:**
Pipeline 3 uses a 14-day GDELT lookback and 14-day equity proxy window, vs. 7 days for Pipelines 2-A and 2-B. But Taiwan escalation uses a 3-day window. Describe the information loss and information gain from each choice. If a major US-China diplomatic breakthrough happens on Day 1 of a 14-day window and is immediately followed by a Taiwan incident on Day 12 — what does the composite show at Day 14, and is that the correct reading? How would you design a recency-weighted GDELT scoring function (as introduced in Question 1 of Lesson 247) that handles this asymmetry without manual intervention?

**Question 2 — The equity proxy circularity problem:**
Pipeline 3 uses COPX and MCHI as equity proxies to *confirm* GDELT-detected diplomatic normalization. But COPX also responds to China's domestic demand cycle (infrastructure spending, real estate recovery), the global copper supply curve (mining output, Chilean strikes), and the US dollar (copper is priced in USD). A COPX rally driven by a Chilean mining strike would produce a false positive in Pipeline 3 — signaling US-China normalization when the real driver is supply disruption. Design a filter that distinguishes COPX moves driven by US-China sentiment vs. COPX moves driven by supply factors. What additional data sources would you add to Pipeline 3 to disambiguate?

**Question 3 — The architecture decision question:**
Signal 3 is weighted at only 15% in the GSI, vs. 30% each for Signals 1 and 2. The justification is that US-China relations change slowly. But this logic is wrong in tail events: if China invades Taiwan, Signal 3 should dominate the GSI entirely — not contribute 15%. Design a dynamic weighting scheme where Signal 3's weight scales up in proportion to the Taiwan counter-signal. At what taiwan_counter level should Signal 3's weight transition from 15% to 30%? To 50%? What are the second-order effects on the GSI's behavior if Signal 3 becomes dominant during a Taiwan crisis?

---

## CEO Closing Note — The Deadline Is Tomorrow

Pipeline 4 goes live tomorrow — Saturday, August 15, 2026.

This is not a soft deadline. It is the foundation of the entire analytical architecture. Without Pipeline 4 live:
- The export control bifurcation signal (Signal 4) remains a CEO estimate
- The GSI v2.1 formula continues to use a judgmental placeholder for 25% of its weight
- The Delta table `geopolitics.pipeline4_scores` does not exist, which means the cross-pipeline dashboard query in Pipeline 2-A Cell 9 and Pipeline 2-B Cell 9 will fail when those pipelines go live

**Tomorrow's task for Bolo — four steps:**

1. Open Databricks workspace: `https://dbc-2faae908-ade9.cloud.databricks.com`
2. Locate the Pipeline 4 notebook (built in Lesson 238 / August 9 session)
3. Run all cells in sequence
4. Email the output (P4 composite score, bifurcation index, regime label, and screenshot) to `ceo@prospectra.earth`

The CEO will be watching for that email.

Today's lesson (Pipeline 3 architecture) is the roadmap for October 31. Tomorrow's execution (Pipeline 4 go-live) is the foundation for everything between now and then. Neither waits for the other to be more convenient.

**The engineering sequence as of August 14, 2026:**

```
August 15 (tomorrow):  Pipeline 4 → LIVE. First live GSI signal. Email CEO.
September 12:          Pipeline 2-A → LIVE. GSI v2.0 fully data-driven on Signal 1.
October 3:             Pipeline 2-B → LIVE. GSI v2.1 fully data-driven on Signals 1+2.
October 31:            Pipeline 3 → LIVE. GSI v3.0. All signals data-driven.
```

Complete Pipeline 4 code: delivered in Lesson 238. No new code is required for Saturday. The only task is execution.

Send the output to `ceo@prospectra.earth` by end of day Saturday.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session 248 | August 14, 2026 | Engineering Phase, Session 11*
*Pipeline 4 deadline: August 15, 2026 — TOMORROW*
*Pipeline 2-A deadline: September 12, 2026 — 29 days*
*Pipeline 2-B deadline: October 3, 2026 — 50 days*
*Pipeline 3 deadline: October 31, 2026 — 78 days*
*Next session: Pipeline 3 complete code (Lesson 249) — delivered after Pipeline 4 confirmation received*
