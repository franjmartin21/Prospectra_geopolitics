# Databricks notebook source
# GDELT GKG 2.0 Extraction Notebook
# Downloads raw GKG CSV files for a given date → UC Volume
# Run as a Job task (not inside the SDP pipeline)

# COMMAND ----------

# Parameters — injected by the Job; defaults to yesterday UTC

import datetime

dbutils.widgets.text("run_date", "")

run_date_str = dbutils.widgets.get("run_date").strip()
if not run_date_str:
    run_date_str = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

run_date = datetime.datetime.strptime(run_date_str, "%Y-%m-%d")
print(f"Extracting GDELT GKG for: {run_date_str}")

# COMMAND ----------

import requests
import zipfile
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

VOLUME_BASE = "/Volumes/geopolitics/gdelt_narrative/raw_gkg"
GDELT_BASE  = "http://data.gdeltproject.org/gdeltv2"

date_str  = run_date.strftime("%Y%m%d")      # 20240115
year      = run_date.strftime("%Y")
month     = run_date.strftime("%m")
day       = run_date.strftime("%d")

output_dir = f"{VOLUME_BASE}/{year}/{month}/{day}"
os.makedirs(output_dir, exist_ok=True)

# COMMAND ----------

# Build list of 96 15-minute time slots for the day

def build_file_list(date: datetime.datetime) -> list[str]:
    """Return list of GKG 2.0 zip URLs for every 15-min slot in the given UTC day."""
    slots = []
    current = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end     = date.replace(hour=23, minute=45, second=0, microsecond=0)
    delta   = datetime.timedelta(minutes=15)
    while current <= end:
        ts = current.strftime("%Y%m%d%H%M%S")
        slots.append(f"{GDELT_BASE}/{ts}.gkg.csv.zip")
        current += delta
    return slots

urls = build_file_list(run_date)
print(f"Files to download: {len(urls)}")

# COMMAND ----------

# Download worker — idempotent (skips if already present)

def download_file(url: str) -> dict:
    filename = url.split("/")[-1].replace(".zip", "")
    dest_path = f"{output_dir}/{filename}"

    if os.path.exists(dest_path):
        return {"url": url, "status": "skipped", "path": dest_path}

    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 404:
            # GDELT occasionally has missing slots — not an error
            return {"url": url, "status": "missing", "path": None}
        resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            name = zf.namelist()[0]
            with zf.open(name) as f:
                content = f.read()

        with open(dest_path, "wb") as f:
            f.write(content)

        return {"url": url, "status": "ok", "path": dest_path, "bytes": len(content)}

    except Exception as e:
        return {"url": url, "status": "error", "error": str(e), "path": None}

# COMMAND ----------

# Parallel download — 8 threads

results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(download_file, url): url for url in urls}
    for future in as_completed(futures):
        results.append(future.result())

# COMMAND ----------

# Summary

ok      = [r for r in results if r["status"] == "ok"]
skipped = [r for r in results if r["status"] == "skipped"]
missing = [r for r in results if r["status"] == "missing"]
errors  = [r for r in results if r["status"] == "error"]

print(f"Downloaded : {len(ok)}")
print(f"Skipped    : {len(skipped)}  (already present)")
print(f"Missing    : {len(missing)} (GDELT gaps — normal)")
print(f"Errors     : {len(errors)}")

if errors:
    for e in errors:
        print(f"  ERROR: {e['url']} — {e['error']}")

# COMMAND ----------

# Write manifest for lineage

manifest = {
    "run_date"     : run_date_str,
    "total_slots"  : len(urls),
    "downloaded"   : len(ok),
    "skipped"      : len(skipped),
    "missing"      : len(missing),
    "errors"       : len(errors),
    "output_dir"   : output_dir,
    "extracted_at" : datetime.datetime.utcnow().isoformat() + "Z",
}

manifest_path = f"{output_dir}/_manifest.json"
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest written: {manifest_path}")

# COMMAND ----------

# Write _SUCCESS marker — pipeline checks for this before reading

success_path = f"{output_dir}/_SUCCESS"
with open(success_path, "w") as f:
    f.write(run_date_str)

print(f"_SUCCESS marker written: {success_path}")

if errors:
    raise RuntimeError(f"Extraction completed with {len(errors)} errors. Check output above.")
