# Lesson 267: CB-TEXT-001 — Central Bank Text Intelligence Pipeline Implementation Sprint
**Date:** 2026-08-25 (Tuesday)
**Session Type:** Daily Lesson — Databricks Implementation Sprint
**Curriculum Position:** 267 — Operational Phase, Jackson Hole Week
**Priority: HIGH — Pipeline must be ready before Thursday 8:00 AM ET when Jackson Hole papers drop**
**GSI:** ~3.7 / 5.0 — ELEVATED_TAIL_RISK
**Days to Warsh Keynote:** 3

---

## Opening Question

**In Lesson 266, I gave you a five-question framework for reading a Jackson Hole paper and a keyword dictionary to score each paper against our four scenarios (A/B/C/D). I told you to have a pipeline ready to run Thursday morning at 8:00 AM ET. It is now Tuesday morning. You have approximately 48 hours. Here is the real question: what is the minimum viable version of this pipeline that you can actually build and run by Thursday morning — and what does "minimum viable" look like when the output needs to drive real portfolio decisions? Let's build it.**

This lesson is a Databricks implementation sprint. Unlike most lessons, which are primarily conceptual with a Databricks Angle at the end, this lesson *is* the Databricks Angle. We will spec and write the actual code, notebook by notebook, that constitutes CB-TEXT-001 in its minimum viable form. By the end of this lesson, you have a build plan with specific Databricks artifacts to create. By Wednesday evening, you have a working pipeline. By Thursday 8:15 AM, you have your first real output: a scenario probability score for the 2026 Jackson Hole papers.

---

## Part I: Scoping the Minimum Viable Pipeline

The full CB-TEXT-001 spec from Lesson 266 called for:
1. PDF ingestion (PyPDF2 or pdfplumber)
2. Preprocessing (spaCy/NLTK tokenization)
3. Keyword scoring (scenario A/B/C/D dictionaries)
4. Sentiment layer (FinBERT)
5. Delta table output

For a Thursday morning deadline, we need to make a pragmatic build decision. **Full sentiment modeling (Step 4) requires installing a HuggingFace model, which takes time to configure on a cluster and may surface dependency issues you don't have time to debug.** The keyword scoring pipeline (Steps 1–3 + 5) delivers 80% of the decision value in 20% of the build time.

**The Thursday-ready MVP:**
- PDF text extraction (via `pdfplumber` — more reliable than PyPDF2 on academic paper formatting)
- Clean text preprocessing (sentence tokenization + stopword removal)
- Scenario keyword scoring (A/B/C/D dictionaries, weighted frequency count)
- Confidence scoring (keyword density × proximity weighting)
- Delta table output with per-paper and aggregate scores
- Optional: basic FinBERT sentiment if cluster setup permits (do not block on this)

**The post-Jackson-Hole full build (next week):**
- Fine-tuned central bank language model
- FOMC statements + minutes ingestion (automated)
- Speaker attribution and tone modeling
- Historical backtesting against prior keynote outcomes

This is a deliberate architectural choice: build the MVP to extract real value from Thursday, then extend the model after the event. Do not let perfection block the signal.

---

## Part II: The Architecture — Three Databricks Notebooks

CB-TEXT-001 is implemented as three chained Databricks notebooks:

```
Notebook 1: cb_text_001_ingest.py
  → Takes PDF URL or uploaded file path
  → Extracts raw text per section (abstract, body, conclusion)
  → Writes to Delta: raw_text_store.jackson_hole_2026

Notebook 2: cb_text_001_score.py
  → Reads from raw_text_store
  → Applies keyword dictionaries
  → Computes scenario scores per paper
  → Writes to Delta: cb_text_signals.paper_scores_2026

Notebook 3: cb_text_001_aggregate.py
  → Reads paper_scores_2026
  → Computes conference-level aggregate scenario probabilities
  → Compares to market-implied scenario probabilities (from SOFR futures)
  → Outputs: deviation signal (where paper signal diverges from market pricing)
  → Writes to Delta: cb_text_signals.aggregate_signal_2026
```

This three-notebook structure is intentional: each notebook can be run and tested independently, and you can re-run notebook 2 (scoring) without re-ingesting if you update the keyword dictionaries.

---

## Part III: Notebook 1 — Ingestion

**Create this notebook as: `cb_text_001_ingest` in your Databricks workspace under a `CB_TEXT_001` folder.**

```python
# CB-TEXT-001 | Notebook 1: Ingest
# Extracts text from Jackson Hole academic papers (PDF)
# Output: Delta table raw_text_store.jackson_hole_2026

# ── Dependencies ──────────────────────────────────────────
# Install in cluster init or via %pip if not pre-installed:
# %pip install pdfplumber requests

import pdfplumber
import requests
import io
import re
from datetime import datetime
from pyspark.sql import Row
from delta.tables import DeltaTable

# ── Configuration ─────────────────────────────────────────
OUTPUT_TABLE = "raw_text_store.jackson_hole_2026"
SYMPOSIUM_YEAR = 2026
EVENT_DATE = "2026-08-27"

# ── Paper sources ─────────────────────────────────────────
# Populate with actual URLs when KC Fed publishes Thursday morning
# These are placeholder entries — update Thursday 8:00 AM ET
PAPERS = [
    {
        "paper_id": "jh_2026_paper_01",
        "title": "TBD — check kansascityfed.org Thursday 8:00 AM ET",
        "url": None,   # Replace with actual URL Thursday morning
        "local_path": None  # Alternative: upload PDF and provide DBFS path
    },
    {
        "paper_id": "jh_2026_paper_02",
        "title": "TBD",
        "url": None,
        "local_path": None
    },
    {
        "paper_id": "jh_2026_paper_03",
        "title": "TBD",
        "url": None,
        "local_path": None
    }
]

# ── Text extraction functions ─────────────────────────────
def extract_text_from_url(url: str) -> str:
    """Download PDF from URL and extract full text."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    pdf_bytes = io.BytesIO(response.content)
    return extract_text_from_bytes(pdf_bytes)

def extract_text_from_path(dbfs_path: str) -> str:
    """Extract text from a PDF already uploaded to DBFS."""
    with open(dbfs_path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())
    return extract_text_from_bytes(pdf_bytes)

def extract_text_from_bytes(pdf_bytes: io.BytesIO) -> str:
    """Core extraction: returns full text from PDF bytes."""
    full_text = []
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)
    return "\n".join(full_text)

def extract_sections(full_text: str) -> dict:
    """
    Attempt to split extracted text into logical sections.
    Falls back to full text if section boundaries can't be detected.
    """
    text_lower = full_text.lower()
    
    # Find abstract
    abstract_start = text_lower.find("abstract")
    intro_start = text_lower.find("introduction") 
    conclusion_start = text_lower.find("conclusion")
    
    sections = {
        "abstract": "",
        "body": "",
        "conclusion": "",
        "full_text": full_text
    }
    
    if abstract_start != -1 and intro_start != -1:
        sections["abstract"] = full_text[abstract_start:intro_start].strip()
    
    if intro_start != -1 and conclusion_start != -1:
        sections["body"] = full_text[intro_start:conclusion_start].strip()
    elif intro_start != -1:
        sections["body"] = full_text[intro_start:].strip()
    
    if conclusion_start != -1:
        sections["conclusion"] = full_text[conclusion_start:].strip()
    
    return sections

def clean_text(text: str) -> str:
    """Remove common PDF artifacts and normalize whitespace."""
    # Remove page numbers, headers/footers (heuristic: short lines)
    lines = text.split("\n")
    cleaned_lines = [
        line for line in lines 
        if len(line.strip()) > 20 or (line.strip() and not line.strip().isdigit())
    ]
    text = " ".join(cleaned_lines)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove hyphenation artifacts
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    return text

# ── Main ingestion loop ───────────────────────────────────
rows = []
ingestion_timestamp = datetime.utcnow().isoformat()

for paper in PAPERS:
    print(f"Processing: {paper['paper_id']} — {paper['title']}")
    
    try:
        if paper.get("url"):
            raw_text = extract_text_from_url(paper["url"])
        elif paper.get("local_path"):
            raw_text = extract_text_from_path(paper["local_path"])
        else:
            print(f"  ⚠ No source for {paper['paper_id']} — skipping (update URLs Thursday morning)")
            continue
        
        sections = extract_sections(raw_text)
        cleaned_full = clean_text(raw_text)
        
        rows.append(Row(
            paper_id=paper["paper_id"],
            title=paper["title"],
            symposium_year=SYMPOSIUM_YEAR,
            event_date=EVENT_DATE,
            raw_text=raw_text,
            cleaned_text=cleaned_full,
            abstract=clean_text(sections["abstract"]),
            body=clean_text(sections["body"]),
            conclusion=clean_text(sections["conclusion"]),
            char_count=len(cleaned_full),
            ingestion_timestamp=ingestion_timestamp,
            source_url=paper.get("url", ""),
            source_path=paper.get("local_path", "")
        ))
        print(f"  ✓ Extracted {len(cleaned_full):,} characters")
        
    except Exception as e:
        print(f"  ✗ Error on {paper['paper_id']}: {e}")

# ── Write to Delta ────────────────────────────────────────
if rows:
    df = spark.createDataFrame(rows)
    
    # Create database if it doesn't exist
    spark.sql("CREATE DATABASE IF NOT EXISTS raw_text_store")
    
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable(OUTPUT_TABLE)
    
    print(f"\n✓ Wrote {len(rows)} papers to {OUTPUT_TABLE}")
    display(df.select("paper_id", "title", "char_count", "ingestion_timestamp"))
else:
    print("\n⚠ No papers ingested. Update PAPERS list with URLs Thursday morning.")
    print("Pipeline shell is ready — run this notebook when papers are published.")
```

**Wednesday night task:** Run this notebook once with one of the placeholder entries to confirm the PDF extraction pipeline works. Use any publicly available Federal Reserve speech PDF as a test input (find one at federalreserve.gov/newsevents/speeches.htm). This proves the pipeline before Thursday.

---

## Part IV: Notebook 2 — Keyword Scoring

**Create as: `cb_text_001_score` in the same folder.**

```python
# CB-TEXT-001 | Notebook 2: Keyword Scoring Engine
# Applies scenario A/B/C/D keyword dictionaries to ingested papers
# Output: Delta table cb_text_signals.paper_scores_2026

import re
from collections import Counter, defaultdict
from pyspark.sql import Row
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, FloatType, MapType
from datetime import datetime

# ── Scenario keyword dictionaries ─────────────────────────
# Based on Lesson 265 linguistic decoder + Lesson 266 academic signal framework
# Weight = importance within scenario (1.0 = standard, 2.0 = high-signal phrase)

SCENARIO_KEYWORDS = {
    "A": {  # HAWKISH — No pivot, bar for cuts is high
        "persistent": 2.0,
        "embedded": 2.0,
        "supply-side constraint": 2.0,
        "supply side constraint": 2.0,
        "premature easing": 2.5,
        "credibility": 1.5,
        "price stability is not yet secured": 3.0,
        "not yet secured": 2.5,
        "price stability": 1.5,
        "inflation persistence": 2.0,
        "persistent inflation": 2.0,
        "above target": 1.5,
        "inflation expectations": 1.0,
        "de-anchoring": 2.0,
        "de anchoring": 2.0,
        "wage-price": 2.0,
        "wage price spiral": 2.5,
        "structural inflation": 2.0,
        "supply shock": 1.5,
        "restrictive stance": 1.5,
        "maintain current stance": 2.0,
        "risk of premature": 2.5,
    },
    "B": {  # PIVOT-LITE — Conditional openness, data-dependent
        "progress": 1.0,
        "encouraging": 1.5,
        "data-dependent": 2.0,
        "data dependent": 2.0,
        "meeting-by-meeting": 2.5,
        "meeting by meeting": 2.5,
        "labor market resilience": 2.0,
        "labor market remains": 1.5,
        "disinflation": 2.0,
        "disinflation progress": 2.5,
        "confidence is growing": 2.5,
        "approaching": 1.0,
        "toward target": 1.5,
        "conditional": 1.5,
        "appropriate calibration": 2.0,
        "carefully": 1.5,
        "prudent": 1.5,
        "balanced risk": 2.0,
        "two-sided risk": 2.0,
        "two sided risk": 2.0,
        "gradual normalization": 2.0,
        "normalization path": 1.5,
    },
    "C": {  # DOVISH — Explicit pivot, cut cycle beginning
        "confidence": 1.0,
        "sufficient confidence": 2.5,
        "balance of risks": 2.0,
        "appropriate to begin": 3.0,
        "recalibration": 2.0,
        "policy recalibration": 2.5,
        "well-positioned": 2.0,
        "well positioned": 2.0,
        "sustainably": 2.0,
        "sustainably converging": 2.5,
        "inflation sustainably": 2.0,
        "demand restraint achieved": 3.0,
        "policy space": 2.0,
        "adjustment": 1.0,
        "easing": 1.5,
        "pivot": 1.5,  # Media term, less likely in actual paper
        "accommodation": 1.5,
        "restrictive policy is no longer": 2.5,
        "normalization": 1.5,
        "rate reduction": 2.0,
    },
    "D": {  # AMBIGUITY / FINANCIAL STABILITY FOCUS
        "neutral rate uncertainty": 3.0,
        "neutral rate": 2.0,
        "r-star": 2.5,
        "r star": 2.5,
        "macro-financial": 2.0,
        "macro financial stability": 2.5,
        "financial stability": 2.0,
        "macroprudential": 2.0,
        "macro prudential": 2.0,
        "endogenous risk": 2.5,
        "non-linear": 2.0,
        "non linear dynamics": 2.0,
        "uncertainty": 1.0,
        "structural uncertainty": 2.0,
        "estimation uncertainty": 2.0,
        "regime change": 2.0,
        "regime shift": 2.0,
        "fragmentation": 2.0,
        "geopolitical fragmentation": 2.5,
        "supply-side structural": 2.0,
        "supply side structural": 2.0,
    }
}

# ── Scoring function ──────────────────────────────────────
def score_text_against_scenarios(text: str, keywords_dict: dict) -> dict:
    """
    Score a text against all scenario keyword dictionaries.
    Returns normalized scores and raw counts per scenario.
    """
    text_lower = text.lower()
    scores = {}
    counts = {}
    
    for scenario, keywords in keywords_dict.items():
        weighted_score = 0.0
        hit_count = 0
        
        for phrase, weight in keywords.items():
            phrase_lower = phrase.lower()
            # Count occurrences
            occurrences = len(re.findall(re.escape(phrase_lower), text_lower))
            if occurrences > 0:
                # Apply diminishing returns for repeated keywords (log scaling)
                import math
                effective_count = 1 + math.log(occurrences) if occurrences > 1 else 1
                weighted_score += effective_count * weight
                hit_count += occurrences
        
        scores[scenario] = round(weighted_score, 3)
        counts[scenario] = hit_count
    
    # Normalize scores to sum to 1.0 (probability-like)
    total = sum(scores.values())
    normalized = {}
    if total > 0:
        for s, v in scores.items():
            normalized[s] = round(v / total, 4)
    else:
        normalized = {s: 0.25 for s in scores}  # Flat prior if no keywords found
    
    return {
        "raw_scores": scores,
        "normalized_scores": normalized,
        "keyword_hits": counts,
        "total_weighted_score": round(total, 3)
    }

def identify_dominant_scenario(normalized_scores: dict) -> str:
    """Return the highest-scoring scenario."""
    return max(normalized_scores, key=normalized_scores.get)

def compute_confidence(normalized_scores: dict) -> float:
    """
    Confidence = margin between top and second-highest score.
    High margin = clear signal. Low margin = ambiguous.
    """
    sorted_scores = sorted(normalized_scores.values(), reverse=True)
    if len(sorted_scores) < 2:
        return 0.0
    return round(sorted_scores[0] - sorted_scores[1], 4)

# ── Main scoring loop ─────────────────────────────────────
# Read ingested papers from Delta
df_papers = spark.table("raw_text_store.jackson_hole_2026")
papers_list = df_papers.collect()

if not papers_list:
    print("⚠ No papers in raw_text_store.jackson_hole_2026 — run Notebook 1 first.")
else:
    rows = []
    scoring_timestamp = datetime.utcnow().isoformat()
    
    for paper in papers_list:
        print(f"Scoring: {paper['paper_id']}")
        
        # Score abstract (highest signal density)
        abstract_result = score_text_against_scenarios(
            paper["abstract"] or paper["cleaned_text"][:2000],
            SCENARIO_KEYWORDS
        )
        
        # Score conclusion (policy implications cluster here)
        conclusion_result = score_text_against_scenarios(
            paper["conclusion"] or paper["cleaned_text"][-2000:],
            SCENARIO_KEYWORDS
        )
        
        # Score full text
        full_result = score_text_against_scenarios(
            paper["cleaned_text"],
            SCENARIO_KEYWORDS
        )
        
        # Weighted composite: abstract (40%) + conclusion (35%) + full (25%)
        composite = {}
        for s in ["A", "B", "C", "D"]:
            composite[s] = round(
                0.40 * abstract_result["normalized_scores"].get(s, 0) +
                0.35 * conclusion_result["normalized_scores"].get(s, 0) +
                0.25 * full_result["normalized_scores"].get(s, 0),
                4
            )
        
        # Renormalize composite
        total_c = sum(composite.values())
        if total_c > 0:
            composite = {s: round(v / total_c, 4) for s, v in composite.items()}
        
        dominant = identify_dominant_scenario(composite)
        confidence = compute_confidence(composite)
        
        # Determine signal quality
        if confidence > 0.20:
            signal_quality = "CLEAR"
        elif confidence > 0.10:
            signal_quality = "MODERATE"
        else:
            signal_quality = "AMBIGUOUS"
        
        rows.append(Row(
            paper_id=paper["paper_id"],
            title=paper["title"],
            event_date=paper["event_date"],
            # Abstract scores
            abstract_score_A=abstract_result["normalized_scores"]["A"],
            abstract_score_B=abstract_result["normalized_scores"]["B"],
            abstract_score_C=abstract_result["normalized_scores"]["C"],
            abstract_score_D=abstract_result["normalized_scores"]["D"],
            # Conclusion scores
            conclusion_score_A=conclusion_result["normalized_scores"]["A"],
            conclusion_score_B=conclusion_result["normalized_scores"]["B"],
            conclusion_score_C=conclusion_result["normalized_scores"]["C"],
            conclusion_score_D=conclusion_result["normalized_scores"]["D"],
            # Composite scores
            composite_A=composite.get("A", 0.0),
            composite_B=composite.get("B", 0.0),
            composite_C=composite.get("C", 0.0),
            composite_D=composite.get("D", 0.0),
            # Signal interpretation
            dominant_scenario=dominant,
            confidence_score=confidence,
            signal_quality=signal_quality,
            # Keyword counts
            total_keyword_hits_full=full_result["keyword_hits"],
            # Metadata
            scoring_timestamp=scoring_timestamp
        ))
        
        print(f"  Dominant: Scenario {dominant} | Confidence: {confidence:.2%} | Quality: {signal_quality}")
        print(f"  A:{composite['A']:.2%} | B:{composite['B']:.2%} | C:{composite['C']:.2%} | D:{composite['D']:.2%}")
    
    # Write to Delta
    if rows:
        df_scores = spark.createDataFrame(rows)
        spark.sql("CREATE DATABASE IF NOT EXISTS cb_text_signals")
        df_scores.write \
            .format("delta") \
            .mode("overwrite") \
            .saveAsTable("cb_text_signals.paper_scores_2026")
        
        print(f"\n✓ Wrote {len(rows)} paper scores to cb_text_signals.paper_scores_2026")
        display(df_scores.select(
            "paper_id", "title", "dominant_scenario",
            "composite_A", "composite_B", "composite_C", "composite_D",
            "confidence_score", "signal_quality"
        ))
```

---

## Part V: Notebook 3 — Aggregate Signal and Market Deviation

**Create as: `cb_text_001_aggregate` in the same folder.**

```python
# CB-TEXT-001 | Notebook 3: Aggregate Signal & Market Deviation
# Combines per-paper scores into conference-level signal
# Computes deviation from market-implied scenario probabilities
# Output: Delta table cb_text_signals.aggregate_signal_2026

from pyspark.sql.functions import avg, col, lit, round as spark_round
from datetime import datetime

# ── Market-implied scenario probabilities ─────────────────
# UPDATE THESE MANUALLY Thursday morning before running
# Based on September SOFR implied cut probability
# From Lesson 265 baseline: A:30% / B:50% / C:12% / D:8%
# Adjust based on current SOFR implied probability at time of running

MARKET_IMPLIED = {
    "A": 0.30,  # Update Thursday based on SOFR futures
    "B": 0.50,  # Update Thursday based on SOFR futures
    "C": 0.12,  # Update Thursday based on SOFR futures
    "D": 0.08   # Residual
}

# ── Read paper scores ─────────────────────────────────────
df_scores = spark.table("cb_text_signals.paper_scores_2026")

if df_scores.count() == 0:
    print("⚠ No paper scores found — run Notebook 2 first.")
else:
    # ── Aggregate: simple average across papers ───────────
    # Each paper gets equal weight in the conference signal
    agg = df_scores.agg(
        avg(col("composite_A")).alias("paper_signal_A"),
        avg(col("composite_B")).alias("paper_signal_B"),
        avg(col("composite_C")).alias("paper_signal_C"),
        avg(col("composite_D")).alias("paper_signal_D"),
        avg(col("confidence_score")).alias("avg_confidence"),
    ).collect()[0]
    
    paper_signal = {
        "A": round(agg["paper_signal_A"], 4),
        "B": round(agg["paper_signal_B"], 4),
        "C": round(agg["paper_signal_C"], 4),
        "D": round(agg["paper_signal_D"], 4),
    }
    
    # ── Compute deviation from market pricing ─────────────
    # Positive deviation = paper signal is MORE hawkish/dovish than market
    # Negative deviation = market is more hawkish/dovish than paper signal
    deviation = {}
    for s in ["A", "B", "C", "D"]:
        deviation[s] = round(paper_signal[s] - MARKET_IMPLIED[s], 4)
    
    # ── Determine overall signal direction ────────────────
    # Find where paper signal most materially deviates from market
    max_deviation_scenario = max(deviation, key=lambda k: abs(deviation[k]))
    max_deviation_value = deviation[max_deviation_scenario]
    
    # Determine investable signal
    if abs(max_deviation_value) > 0.10:
        deviation_significance = "MATERIAL — Consider tactical adjustment"
    elif abs(max_deviation_value) > 0.05:
        deviation_significance = "MODERATE — Monitor, no action required"
    else:
        deviation_significance = "MINIMAL — Market and papers aligned"
    
    # Positive deviation on A = papers more hawkish than market → consider trim EM FX
    # Positive deviation on C = papers more dovish than market → consider add EM FX
    # Positive deviation on D = papers more ambiguous than market → add gold hedge
    SIGNAL_INTERPRETATION = {
        "A": "Papers more hawkish than market → trim EM FX, let dollar breathe",
        "B": "Papers confirm base case → no action, thesis confirmed",
        "C": "Papers more dovish than market → add EM FX basket, consider gold run",
        "D": "Papers more ambiguous than market → add gold, tighten EM FX stops"
    }
    
    # ── Print intelligence report ─────────────────────────
    print("=" * 60)
    print("CB-TEXT-001 | JACKSON HOLE 2026 | AGGREGATE SIGNAL REPORT")
    print("=" * 60)
    print(f"\nPaper Signal (aggregate across {df_scores.count()} papers):")
    for s in ["A", "B", "C", "D"]:
        bar = "█" * int(paper_signal[s] * 40)
        print(f"  Scenario {s}: {paper_signal[s]:.2%}  {bar}")
    
    print(f"\nMarket-Implied Scenario Probabilities:")
    for s in ["A", "B", "C", "D"]:
        bar = "█" * int(MARKET_IMPLIED[s] * 40)
        print(f"  Scenario {s}: {MARKET_IMPLIED[s]:.2%}  {bar}")
    
    print(f"\nDeviation (Paper Signal minus Market):")
    for s in ["A", "B", "C", "D"]:
        direction = "+" if deviation[s] >= 0 else ""
        print(f"  Scenario {s}: {direction}{deviation[s]:.2%}")
    
    print(f"\nPrimary Deviation: Scenario {max_deviation_scenario}")
    print(f"Deviation Magnitude: {max_deviation_value:+.2%}")
    print(f"Significance: {deviation_significance}")
    print(f"\nTactical Signal: {SIGNAL_INTERPRETATION.get(max_deviation_scenario, 'No clear signal')}")
    print(f"Average Paper Confidence Score: {agg['avg_confidence']:.2%}")
    print("=" * 60)
    
    # ── Write to Delta ────────────────────────────────────
    from pyspark.sql import Row
    result_row = Row(
        event="jackson_hole_2026",
        run_timestamp=datetime.utcnow().isoformat(),
        paper_signal_A=paper_signal["A"],
        paper_signal_B=paper_signal["B"],
        paper_signal_C=paper_signal["C"],
        paper_signal_D=paper_signal["D"],
        market_implied_A=MARKET_IMPLIED["A"],
        market_implied_B=MARKET_IMPLIED["B"],
        market_implied_C=MARKET_IMPLIED["C"],
        market_implied_D=MARKET_IMPLIED["D"],
        deviation_A=deviation["A"],
        deviation_B=deviation["B"],
        deviation_C=deviation["C"],
        deviation_D=deviation["D"],
        primary_deviation_scenario=max_deviation_scenario,
        deviation_significance=deviation_significance,
        avg_paper_confidence=round(agg["avg_confidence"], 4),
        papers_analyzed=df_scores.count(),
        tactical_signal=SIGNAL_INTERPRETATION.get(max_deviation_scenario, "No clear signal")
    )
    
    df_agg = spark.createDataFrame([result_row])
    df_agg.write \
        .format("delta") \
        .mode("append") \
        .saveAsTable("cb_text_signals.aggregate_signal_2026")
    
    print(f"\n✓ Aggregate signal written to cb_text_signals.aggregate_signal_2026")
```

---

## Part VI: Thursday Morning Protocol (The 8:00 AM Operating Procedure)

**Build the pipeline today and Wednesday. Thursday morning, execute this protocol:**

**8:00 AM ET — KC Fed publishes papers**
1. Open `kansascityfed.org/jackson-hole-economic-symposium/` in your browser
2. Copy PDF URLs for each paper
3. Update the `PAPERS` list in Notebook 1 with the actual URLs
4. Note the paper titles in the `PAPERS` list — the titles alone are your first signal (apply the five-question framework from Lesson 266)

**8:05–8:15 AM ET — Pipeline run**
5. Run Notebook 1 (ingestion) — should complete in 2–3 minutes
6. Run Notebook 2 (scoring) — should complete in under 1 minute
7. Run Notebook 3 (aggregate) — should complete in under 30 seconds
8. Read the aggregate signal report output

**8:15 AM ET — Pre-market signal assessment**
9. Compare the aggregate paper signal to your locked scenario matrix (A:30% / B:50% / C:12% / D:8%)
10. If deviation is MATERIAL, update your scenario probabilities before market open
11. Note the specific dominant scenario and tactical signal
12. Do NOT change your thesis-level positions based on paper signal alone — this is a probability refinement, not a thesis change

**Thursday evening (before Friday keynote)**
13. Lock your final scenario probabilities after the full Thursday academic session
14. Do not adjust these Friday morning based on pre-speech market moves

---

## Part VII: Extending to FOMC Statements and Minutes (Post-Jackson-Hole Build)

Once CB-TEXT-001 is validated on the Jackson Hole papers, the same pipeline applies to a continuous Fed text intelligence feed. The extension architecture:

```
NEW PIPELINE: CB-TEXT-002 (Continuous Fed Monitor)

Sources (all publicly available):
  - FOMC statements: federalreserve.gov/monetarypolicy/fomccalendars.htm
  - FOMC minutes (3-week lag): same URL, released 3 weeks post-meeting
  - Fed governor speeches: federalreserve.gov/newsevents/speeches.htm
  - Beige Book (8x per year): released 2 weeks before each FOMC

Update frequency: 
  - Statements/minutes: ingest within 15 minutes of release
  - Speeches: daily scrape of new publications
  - Beige Book: 8 ingestion events per year

Delta tables:
  - cb_text_signals.fomc_statements
  - cb_text_signals.fomc_minutes
  - cb_text_signals.fed_speeches
  - cb_text_signals.beige_book
  - cb_text_signals.fed_text_signal_composite (time series)

Use case:
  - Track how the A/B/C/D scenario balance evolves across FOMC cycles
  - Detect policy pivots 2–3 weeks before market consensus
  - Flag divergences between FOMC minutes and governor speeches
```

This is a significant platform component. Schedule as Week 1 post-Jackson-Hole build.

---

## Investment Implications

**Today's lesson is pure infrastructure.** The investment implications are downstream:

- A working CB-TEXT-001 pipeline gives you a 15-minute edge on Thursday morning in reading the paper signal before the broader market consensus forms
- The aggregate deviation score quantifies whether you should adjust scenario probabilities before Friday's speech
- The delta table output becomes a permanent record — the start of a time-series of Fed communication scores that will eventually serve as a systematic monetary overlay signal

**The meta-implication for the portfolio:**
Every day that market participants read central bank communication qualitatively and you read it systematically, you compound an analytical advantage. This is not a Jackson Hole trade. This is the beginning of a permanent infrastructure investment in decision quality.

---

## Databricks Build Checklist

Run through this checklist to confirm readiness before Thursday:

**Today (Tuesday):**
- [ ] Create `CB_TEXT_001` folder in Databricks workspace
- [ ] Create notebooks 1, 2, and 3 (copy code above)
- [ ] Install `pdfplumber` and `requests` on cluster (either init script or `%pip install`)
- [ ] Test Notebook 1 with a sample Federal Reserve speech PDF (confirm extraction works)
- [ ] Confirm Delta databases `raw_text_store` and `cb_text_signals` can be created

**Wednesday:**
- [ ] Run full pipeline end-to-end on a test PDF
- [ ] Confirm Notebook 3 output prints the aggregate signal report correctly
- [ ] Update `MARKET_IMPLIED` probabilities in Notebook 3 with Wednesday's SOFR reading
- [ ] Set a calendar reminder for 8:00 AM ET Thursday

**Thursday morning:**
- [ ] Retrieve paper URLs from kansascityfed.org at 8:00 AM ET
- [ ] Update `PAPERS` list in Notebook 1
- [ ] Execute notebooks 1 → 2 → 3 in sequence
- [ ] Read aggregate signal report
- [ ] Update scenario matrix if deviation is MATERIAL

---

## Reflection Questions

1. **The weighting question:** In the scoring engine, I weighted the abstract (40%), conclusion (35%), and full text (25%) of each paper. Is this weighting correct for extracting policy signal — or should the conclusion carry more weight than the abstract? What is the argument for each weighting scheme, and how would you test which performs better historically?

2. **The diminishing returns problem:** The scoring function applies log-scaling to repeated keyword occurrences (so the 10th occurrence of "persistent" counts for less than the first). Is this the right approach for academic papers, where an author may use a word once in the abstract and repeat it throughout with the same meaning? What alternative scoring functions would you consider?

3. **The false positive risk:** The keyword dictionaries can produce false positives. For example, "confidence" appears in Scenario C keywords — but a paper could discuss *falling* confidence in monetary policy frameworks, which is actually a hawkish signal. How would you add negation handling to the scoring function, and what would the implementation look like?

---

## Questions for Next Session

**Lesson 268** is the post-Warsh keynote signal read — delivered Friday afternoon or Saturday morning after the Jackson Hole speech. That lesson will:
- Decode which scenario materialized and assess market pricing accuracy
- Read the Thursday paper signal output from CB-TEXT-001 against the actual keynote outcome
- Determine whether any thesis-level portfolio adjustment is warranted
- Set up the September FOMC positioning framework

**Your immediate priority:** Build and test CB-TEXT-001 today (Tuesday). Set the pipeline live by Wednesday evening. Execute Thursday morning at 8:00 AM ET.

---

*Delivered: 2026-08-25 | CEO — Prospectra Geopolitics & Investment Project*
*Next: Lesson 268 — Post-Warsh Keynote Signal Read (deliver Friday Aug 28 afternoon or Saturday morning)*
