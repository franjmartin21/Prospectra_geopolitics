# Databricks notebook source
# GDELT GKG Backfill Notebook
#
# Downloads a sparse but representative sample of GKG files across a date range:
#   4 files per day at 00:00, 06:00, 12:00, 18:00 UTC
#   = Asian close, European open, US midday, US close news cycles
#
# Default: 2022-04-01 → yesterday (~2 years, ~2,920 files, ~3% of full dataset)
# Designed to be run once. Idempotent — skips already-present files.

# COMMAND ----------

import datetime

dbutils.widgets.text("start_date", "2022-04-01")
dbutils.widgets.text("end_date",   "")           # empty = yesterday UTC
dbutils.widgets.text("hours",      "0,6,12,18")  # UTC hours to download

start_str = dbutils.widgets.get("start_date").strip()
end_str   = dbutils.widgets.get("end_date").strip()
hours_str = dbutils.widgets.get("hours").strip()

start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d")
end_date   = (
    datetime.datetime.strptime(end_str, "%Y-%m-%d")
    if end_str
    else datetime.datetime.utcnow() - datetime.timedelta(days=1)
)
target_hours = [int(h) for h in hours_str.split(",")]

total_days = (end_date - start_date).days + 1
total_files = total_days * len(target_hours)

print(f"Backfill range : {start_date.date()} → {end_date.date()}")
print(f"Days           : {total_days}")
print(f"Hours/day      : {target_hours}")
print(f"Files planned  : {total_files:,}")

# COMMAND ----------

import requests
import zipfile
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

VOLUME_BASE = "/Volumes/geopolitics/gdelt_narrative/raw_gkg"
GDELT_BASE  = "http://data.gdeltproject.org/gdeltv2"

# COMMAND ----------

# Build full list of (date, url) tuples to download

def build_backfill_targets(
    start: datetime.datetime,
    end: datetime.datetime,
    hours: list[int]
) -> list[tuple[datetime.datetime, str]]:
    targets = []
    current = start
    while current <= end:
        for hour in hours:
            dt = current.replace(hour=hour, minute=0, second=0)
            ts = dt.strftime("%Y%m%d%H%M%S")
            url = f"{GDELT_BASE}/{ts}.gkg.csv.zip"
            targets.append((current, url))
        current += datetime.timedelta(days=1)
    return targets

targets = build_backfill_targets(start_date, end_date, target_hours)
print(f"Targets built: {len(targets):,}")

# COMMAND ----------

# Download worker — identical logic to daily extract, idempotent

def download_file(date: datetime.datetime, url: str) -> dict:
    year  = date.strftime("%Y")
    month = date.strftime("%m")
    day   = date.strftime("%d")
    output_dir = f"{VOLUME_BASE}/{year}/{month}/{day}"
    os.makedirs(output_dir, exist_ok=True)

    filename  = url.split("/")[-1].replace(".zip", "")
    dest_path = f"{output_dir}/{filename}"

    if os.path.exists(dest_path):
        return {"url": url, "status": "skipped", "path": dest_path}

    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 404:
            return {"url": url, "status": "missing", "path": None}
        resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            with zf.open(zf.namelist()[0]) as f:
                content = f.read()

        with open(dest_path, "wb") as f:
            f.write(content)

        return {"url": url, "status": "ok", "path": dest_path, "bytes": len(content)}

    except Exception as e:
        return {"url": url, "status": "error", "error": str(e), "path": None}

# COMMAND ----------

# Parallel download — 16 threads (more than daily job since we're batch)
# Progress logged every 200 files

results = []
completed = 0

with ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(download_file, date, url): (date, url) for date, url in targets}
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        completed += 1
        if completed % 200 == 0:
            ok      = sum(1 for r in results if r["status"] == "ok")
            skipped = sum(1 for r in results if r["status"] == "skipped")
            errors  = sum(1 for r in results if r["status"] == "error")
            print(f"  Progress: {completed:,}/{len(targets):,} | downloaded={ok} skipped={skipped} errors={errors}")

# COMMAND ----------

# Final summary

ok      = [r for r in results if r["status"] == "ok"]
skipped = [r for r in results if r["status"] == "skipped"]
missing = [r for r in results if r["status"] == "missing"]
errors  = [r for r in results if r["status"] == "error"]

print(f"\n{'='*50}")
print(f"BACKFILL COMPLETE")
print(f"{'='*50}")
print(f"Downloaded : {len(ok):,}")
print(f"Skipped    : {len(skipped):,}  (already present)")
print(f"Missing    : {len(missing):,} (GDELT gaps — normal)")
print(f"Errors     : {len(errors):,}")
total_bytes = sum(r.get("bytes", 0) for r in ok)
print(f"Total data : {total_bytes / 1e9:.2f} GB")

if errors:
    print("\nFirst 10 errors:")
    for e in errors[:10]:
        print(f"  {e['url']} — {e['error']}")

# COMMAND ----------

# Write a backfill manifest at volume root

manifest = {
    "backfill_start"  : start_str,
    "backfill_end"    : end_date.strftime("%Y-%m-%d"),
    "target_hours"    : target_hours,
    "files_planned"   : len(targets),
    "files_downloaded": len(ok),
    "files_skipped"   : len(skipped),
    "files_missing"   : len(missing),
    "files_errored"   : len(errors),
    "total_bytes"     : total_bytes,
    "completed_at"    : datetime.datetime.utcnow().isoformat() + "Z",
}

manifest_path = f"{VOLUME_BASE}/_backfill_manifest.json"
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"\nManifest written: {manifest_path}")
print("\nNext step: trigger a full pipeline refresh to process the backfilled files.")
print("Run: databricks bundle run gdelt_narrative_daily --target dev")
print("Or trigger a full refresh from the pipeline UI.")
