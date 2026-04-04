# Implementation Plan: GDELT Narrative Shift Detector
**Date:** 2026-04-04
**Catalog:** `geopolitics` | **Schema:** `gdelt_narrative`
**Delivery:** Databricks Asset Bundle (DABS), daily-scheduled job

---

## Overview

Four components wired together as a single DABS bundle:

```
[1] Extraction Notebook          — downloads GDELT GKG files → UC Volume
        ↓
[2] SDP Pipeline (Bronze→Gold)   — transforms raw files → Delta tables
        ↓
[3] Databricks Job               — orchestrates extract → pipeline, daily at 06:00 UTC
        ↓
[4] DABS Bundle                  — packages everything for one-command deploy/redeploy
```

---

## Repository Layout

Pipeline name (`gdelt_narrative`) is the organising unit in both `src/` and `resources/`, mirroring the UC schema name. Adding a second pipeline means adding a new sibling folder — nothing else changes.

```
databricks/
├── databricks.yml                              # DABS bundle root (includes all resource globs)
├── specs/
│   ├── 2026-04-04_gdelt_narrative_shift_detector.md
│   └── 2026-04-04_implementation_plan.md       ← this file
│
├── resources/
│   └── gdelt_narrative/
│       ├── pipeline.yml                        # SDP pipeline resource definition
│       └── job.yml                             # Job resource definition
│
└── src/
    ├── shared/
    │   └── uc_setup.py                         # One-time catalog/schema/volume setup (IF NOT EXISTS)
    │
    └── gdelt_narrative/                        # ← pipeline name matches UC schema name
        ├── extract/
        │   └── gdelt_extract.py                # Notebook: download GKG → Volume
        └── pipeline/
            ├── bronze.py                       # SDP: raw GKG → bronze Delta
            ├── silver.py                       # SDP: parse + country-pair filter → silver Delta
            └── gold.py                         # SDP: daily agg + rolling z-score → gold Delta
```

**Scaling pattern** — a second pipeline (e.g., `sanctions_tracker`) is just:
```
resources/
└── sanctions_tracker/
    ├── pipeline.yml
    └── job.yml

src/
└── sanctions_tracker/
    ├── extract/
    │   └── sanctions_extract.py
    └── pipeline/
        ├── bronze.py
        ├── silver.py
        └── gold.py
```

UC stays consistent: `geopolitics.sanctions_tracker.*`, volume at `/Volumes/geopolitics/sanctions_tracker/raw/`.
The `databricks.yml` root picks up new resources automatically via glob: `resources/**/*.yml`.

**The invariant:** `src/<pipeline_name>/` = `geopolitics.<pipeline_name>` in Unity Catalog.
You can always navigate from table name to source code and back without ambiguity.

---

## Component 1 — Extraction Notebook (`src/gdelt_narrative/extract/gdelt_extract.py`)

**Runtime:** Standard notebook, runs as a Job task (not inside the pipeline).

**What it does:**
1. Reads a `run_date` Job parameter (defaults to yesterday's UTC date)
2. Constructs the list of 96 GKG file URLs for that date (one per 15-minute slot)
3. Downloads each `.gkg.csv.zip`, unzips in-memory, writes raw CSV to UC Volume:
   ```
   /Volumes/geopolitics/gdelt_narrative/raw_gkg/YYYY/MM/DD/YYYYMMDDHHMMSS.gkg.csv
   ```
4. Writes a `_SUCCESS` marker file so the pipeline knows extraction is complete
5. Exits cleanly — no transformation here, pure I/O

**Key design decisions:**
- Uses `requests` + `zipfile` in Python (no Spark for download, avoids executor network issues)
- Parallelizes downloads with `ThreadPoolExecutor(max_workers=8)` — 96 files, ~15 min total otherwise
- Idempotent: skips files already present in the volume (safe to rerun)
- Writes a `manifest.json` per date with file count + download timestamps for lineage

**Parameters (Job-injected):**
```python
run_date: str   # "YYYY-MM-DD", defaults to yesterday
```

---

## Component 2 — SDP Pipeline (`src/gdelt_narrative/pipeline/`)

**Runtime:** Databricks Lakeflow Declarative Pipelines (SDP), triggered mode (not continuous).

The pipeline is three Python files, each declaring DLT tables. They are **all registered under a single pipeline** — SDP resolves the DAG automatically from `dlt.read()` references.

### `bronze.py` — Raw Ingest

```
Input:  /Volumes/geopolitics/gdelt_narrative/raw_gkg/**/*.gkg.csv
Output: geopolitics.gdelt_narrative.bronze_gkg_raw  (append-only, Auto Loader)
```

- Uses Auto Loader (`cloudFiles`) to incrementally pick up new files from the volume
- Reads as raw string columns — no parsing at this layer
- Adds `_ingest_timestamp`, `_source_file` metadata columns
- Schema: all 27 GKG columns as strings (GKG format is messy; parse in silver)

### `silver.py` — Parse + Filter

```
Input:  geopolitics.gdelt_narrative.bronze_gkg_raw
Output: geopolitics.gdelt_narrative.silver_country_pairs
```

Transformations applied:
1. Parse `DATE` column → proper timestamp
2. Explode `LOCATIONS` field (semicolon-separated) → array of location structs:
   ```
   {type, name, country_code, adm1, lat, lon, feature_id}
   ```
3. Extract `country_codes` set per article (distinct ISO country codes mentioned)
4. Parse `TONE` field (comma-separated) → 6 named columns:
   ```
   tone, pos_tone, neg_tone, polarity, activity_ref_density, self_ref_density
   ```
5. **Country-pair filter**: for each article, emit one row per matching pair:
   ```python
   PAIRS = {
       "US_CN": ("US", "CH"),   # GDELT uses FIPS country codes
       "US_RU": ("US", "RS"),
       "RU_EU": ("RS", "EI"),   # EU approximated as multiple — see note below
       "CN_TW": ("CH", "TW"),
       "SA_US": ("SA", "US"),
       "SA_CN": ("SA", "CH"),
       "IN_CN": ("IN", "CH"),
   }
   ```
   An article qualifies for pair `A_B` if both country codes appear in its locations.
6. Drop articles with `article_count` < 3 locations (noise filter)
7. Output schema:
   ```
   date DATE, pair_id STRING, tone DOUBLE, neg_tone DOUBLE,
   pos_tone DOUBLE, polarity DOUBLE, source_url STRING,
   _ingest_timestamp TIMESTAMP
   ```

> **Note on EU:** GDELT uses FIPS codes. "EU" as a bloc doesn't exist — we approximate Russia-EU pairs by requiring RS + any of {EI (Ireland), FR (France), GM (Germany), IT (Italy), PL (Poland)}. This is a known simplification; refine in v2.

### `gold.py` — Sentiment Index

```
Input:  geopolitics.gdelt_narrative.silver_country_pairs
Output: geopolitics.gdelt_narrative.gold_sentiment_index
```

Two DLT tables declared here:

**Table 1: `gold_daily_sentiment`** — daily aggregation
```sql
SELECT
    date,
    pair_id,
    COUNT(*)            AS article_count,
    AVG(tone)           AS avg_tone,
    AVG(neg_tone)       AS avg_neg_tone,
    AVG(pos_tone)       AS avg_pos_tone,
    AVG(polarity)       AS avg_polarity
FROM silver_country_pairs
GROUP BY date, pair_id
```

**Table 2: `gold_sentiment_index`** — rolling stats + z-score
```sql
SELECT
    date,
    pair_id,
    article_count,
    avg_tone,
    avg_neg_tone,
    AVG(avg_tone)   OVER w30  AS rolling_30d_mean,
    STDDEV(avg_tone) OVER w30 AS rolling_30d_std,
    (avg_tone - AVG(avg_tone) OVER w30)
        / NULLIF(STDDEV(avg_tone) OVER w30, 0)  AS z_score,
    ABS((avg_tone - AVG(avg_tone) OVER w30)
        / NULLIF(STDDEV(avg_tone) OVER w30, 0)) > 2.0  AS is_anomaly
FROM gold_daily_sentiment
WINDOW w30 AS (
    PARTITION BY pair_id
    ORDER BY date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
)
```

This is the **final investment signal table**. Partitioned by `pair_id`.

> **SDP mode note:** Because the z-score window looks back 30 rows, this table must run as a **full refresh** (or a `COMPLETE` materialized view). We configure `pipelines.reset.allowed = true` and use `dlt.create_materialized_view` for `gold_sentiment_index`. The daily aggregation (`gold_daily_sentiment`) is append-only streaming.

---

## Component 3 — Job (`resources/jobs/gdelt_daily_job.yml`)

```
Job: gdelt-narrative-daily
Schedule: 06:00 UTC daily (cron: "0 6 * * *")
Timezone: UTC

Tasks:
  Task 1: gdelt-extract
    Type: notebook
    Source: src/gdelt_narrative/extract/gdelt_extract.py
    Parameters:
      run_date: "{{job.start_time.iso_date_yesterday}}"   # dynamic value macro
    Cluster: job_cluster_extract (single-node, 8-core, spot)

  Task 2: gdelt-pipeline-trigger
    Type: pipeline
    Pipeline: gdelt-narrative-pipeline                    # references SDP pipeline by name
    Depends on: gdelt-extract (must succeed)

Email notifications:
  on_failure: [configured in bundle vars]
```

The job uses **two different compute types** intentionally:
- Task 1 (extract) runs on a small cluster — it's I/O bound, not compute bound
- Task 2 (pipeline) runs on SDP's managed serverless compute — no cluster to manage

---

## Component 4 — DABS Bundle (`databricks.yml`)

```yaml
bundle:
  name: gdelt-narrative-shift

variables:
  catalog:
    default: geopolitics
  schema:
    default: gdelt_narrative
  volume_path:
    default: /Volumes/geopolitics/gdelt_narrative/raw_gkg
  notification_email:
    default: ""          # set per environment or via CLI override

targets:
  dev:
    mode: development    # prefixes all resource names with your username
    default: true
    workspace:
      host: ${workspace.host}

  prod:
    mode: production
    workspace:
      host: ${workspace.host}
```

**Deploy commands:**
```bash
# first time
databricks bundle deploy --target dev

# subsequent deploys (same command, idempotent)
databricks bundle deploy --target dev

# run manually
databricks bundle run gdelt-narrative-daily --target dev

# promote to prod
databricks bundle deploy --target prod
```

**What DABS manages:**
- Creates/updates the SDP pipeline
- Creates/updates the job (with schedule)
- Manages pipeline ↔ job references automatically
- Does NOT manage the Unity Catalog schema or volume — those are prerequisites (created once manually or via a separate `setup.py` notebook)

---

## Prerequisites (one-time manual setup)

Before first bundle deploy, run this once in any notebook:

```python
spark.sql("CREATE CATALOG IF NOT EXISTS geopolitics")
spark.sql("CREATE SCHEMA IF NOT EXISTS geopolitics.gdelt_narrative")
spark.sql("""
    CREATE VOLUME IF NOT EXISTS geopolitics.gdelt_narrative.raw_gkg
    COMMENT 'Raw GDELT GKG CSV files, partitioned by date'
""")
```

Or we can add a `setup` notebook task that runs before everything else and is gated by `IF NOT EXISTS` — safe to re-run.

---

## Data Flow Summary

```
HTTP (data.gdeltproject.org)
        │ 96 files × ~5MB each = ~480MB/day
        ▼
/Volumes/geopolitics/gdelt_narrative/raw_gkg/YYYY/MM/DD/
        │ Auto Loader (incremental, schema inference)
        ▼
geopolitics.gdelt_narrative.bronze_gkg_raw          ← append-only Delta
        │ parse + explode + pair filter
        ▼
geopolitics.gdelt_narrative.silver_country_pairs    ← append-only Delta
        │ daily GROUP BY + 30d window
        ▼
geopolitics.gdelt_narrative.gold_daily_sentiment    ← append-only Delta
geopolitics.gdelt_narrative.gold_sentiment_index    ← materialized view (full refresh)
```

---

## Build Order

| Step | What | File |
|---|---|---|
| 1 | Write `databricks.yml` bundle root | `databricks/databricks.yml` |
| 2 | Write one-time UC setup notebook | `databricks/src/shared/uc_setup.py` |
| 3 | Write extraction notebook | `databricks/src/gdelt_narrative/extract/gdelt_extract.py` |
| 4 | Write bronze SDP layer | `databricks/src/gdelt_narrative/pipeline/bronze.py` |
| 5 | Write silver SDP layer | `databricks/src/gdelt_narrative/pipeline/silver.py` |
| 6 | Write gold SDP layer | `databricks/src/gdelt_narrative/pipeline/gold.py` |
| 7 | Write pipeline resource YAML | `databricks/resources/gdelt_narrative/pipeline.yml` |
| 8 | Write job resource YAML | `databricks/resources/gdelt_narrative/job.yml` |
| 9 | Deploy + smoke test | `databricks bundle deploy --target dev` |

---

## Open Questions (resolved)

| Question | Answer |
|---|---|
| Catalog | `geopolitics` |
| Schema | `gdelt_narrative` |
| Date range (initial backfill) | TBD — start with 90 days to validate signal, then extend |
| Compute for extract task | Job cluster, smallest spot instance available |
| Scheduling | Daily 06:00 UTC via Job schedule in DABS |
| SDP mode | Triggered (not continuous) |
| Gold z-score table | Materialized view, full refresh on each pipeline run |

---

*Ready to build. Proceed in the order above — Step 1 first (`databricks.yml`).*
