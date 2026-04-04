# Databricks notebook source
# SDP Bronze Layer — Raw GKG ingest via Auto Loader
# Reads raw .gkg.csv files from UC Volume → bronze_gkg_raw Delta table
# Append-only streaming; schema inferred from first batch then locked.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType
)

# COMMAND ----------

# GKG 2.0 has 27 tab-separated columns.
# We declare them all as strings at bronze — silver handles parsing.
# Column names follow the official GDELT GKG 2.0 codebook.

GKG_SCHEMA = StructType([
    StructField("GKGRECORDID",           StringType(), True),
    StructField("DATE",                  StringType(), True),
    StructField("SourceCollectionIdentifier", StringType(), True),
    StructField("SourceCommonName",      StringType(), True),
    StructField("DocumentIdentifier",    StringType(), True),
    StructField("Counts",                StringType(), True),
    StructField("V2Counts",              StringType(), True),
    StructField("Themes",                StringType(), True),
    StructField("V2Themes",              StringType(), True),
    StructField("Locations",             StringType(), True),
    StructField("V2Locations",           StringType(), True),
    StructField("Persons",               StringType(), True),
    StructField("V2Persons",             StringType(), True),
    StructField("Organizations",         StringType(), True),
    StructField("V2Organizations",       StringType(), True),
    StructField("V2Tone",                StringType(), True),
    StructField("Dates",                 StringType(), True),
    StructField("GCAM",                  StringType(), True),
    StructField("SharingImage",          StringType(), True),
    StructField("RelatedImages",         StringType(), True),
    StructField("SocialImageEmbeds",     StringType(), True),
    StructField("SocialVideoEmbeds",     StringType(), True),
    StructField("Quotations",            StringType(), True),
    StructField("AllNames",              StringType(), True),
    StructField("Amounts",               StringType(), True),
    StructField("TranslationInfo",       StringType(), True),
    StructField("Extras",                StringType(), True),
])

# COMMAND ----------

VOLUME_PATH = "/Volumes/geopolitics/gdelt_narrative/raw_gkg"

@dlt.table(
    name    = "bronze_gkg_raw",
    comment = "Raw GDELT GKG 2.0 records ingested via Auto Loader. All columns as strings. Append-only.",
    table_properties = {
        "quality": "bronze",
        "pipelines.reset.allowed": "true",
    }
)
def bronze_gkg_raw():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.schemaLocation", f"{VOLUME_PATH}/_autoloader_schema/bronze")
            .option("sep", "\t")
            .option("header", "false")
            .option("quote", "")           # GKG files are not quoted
            .option("escape", "")
            .option("multiLine", "false")
            .option("enforceSchema", "true")
            .option("columnNameOfCorruptRecord", "_corrupt_record")
            .schema(GKG_SCHEMA)
            .load(f"{VOLUME_PATH}/**/*.gkg.csv")
            .withColumn("_ingest_timestamp", F.current_timestamp())
            .withColumn("_source_file",      F.input_file_name())
    )
