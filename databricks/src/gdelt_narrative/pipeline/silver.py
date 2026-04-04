# Databricks notebook source
# SDP Silver Layer — Parse + country-pair filter
# Input:  bronze_gkg_raw
# Output: silver_country_pairs

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import (
    ArrayType, StructType, StructField,
    StringType, DoubleType
)

# COMMAND ----------

# Country-pair matrix (GDELT uses FIPS-10 country codes, not ISO-2)
# Each entry: (pair_id, fips_a, fips_b)
# For EU pairs we check Russia against any of the 5 major EU economies.

PAIRS = [
    ("US_CN", "US", "CH"),
    ("US_RU", "US", "RS"),
    ("CN_TW", "CH", "TW"),
    ("SA_US", "SA", "US"),
    ("SA_CN", "SA", "CH"),
    ("IN_CN", "IN", "CH"),
]

# Russia-EU: RS + any of these qualifies as RU_EU
EU_FIPS = {"EI", "FR", "GM", "IT", "PL"}

# COMMAND ----------

@dlt.table(
    name    = "silver_country_pairs",
    comment = "GKG articles filtered to target country-pairs with parsed tone scores. One row per article per matched pair.",
    table_properties = {
        "quality": "silver",
        "pipelines.reset.allowed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
    }
)
def silver_country_pairs():
    bronze = dlt.read_stream("bronze_gkg_raw")

    # --- Parse DATE ---
    df = bronze.withColumn(
        "article_date",
        F.to_date(F.col("DATE"), "yyyyMMddHHmmss")
    )

    # --- Parse V2Tone: "tone,pos,neg,polarity,activity_ref,self_ref" ---
    tone_split = F.split(F.col("V2Tone"), ",")
    df = (df
        .withColumn("tone",                 F.col(tone_split[0]).cast(DoubleType()))
        .withColumn("pos_tone",             F.col(tone_split[1]).cast(DoubleType()))
        .withColumn("neg_tone",             F.col(tone_split[2]).cast(DoubleType()))
        .withColumn("polarity",             F.col(tone_split[3]).cast(DoubleType()))
        .withColumn("activity_ref_density", F.col(tone_split[4]).cast(DoubleType()))
        .withColumn("self_ref_density",     F.col(tone_split[5]).cast(DoubleType()))
    )

    # --- Extract country codes from V2Locations ---
    # V2Locations format: "type#name#countrycode#adm1#lat#lon#featureid;..."
    # We extract the country code (3rd field of each semicolon-delimited entry)
    df = df.withColumn(
        "country_codes",
        F.array_distinct(
            F.transform(
                F.filter(
                    F.split(F.col("V2Locations"), ";"),
                    lambda loc: F.length(loc) > 0
                ),
                lambda loc: F.element_at(F.split(loc, "#"), 3)
            )
        )
    )

    # Drop articles with fewer than 3 country mentions (noise filter)
    df = df.filter(F.size(F.col("country_codes")) >= 2)

    # --- Explode into one row per matched country-pair ---
    # Build a column of matched pair_ids for this article, then explode

    pair_exprs = []
    for pair_id, fips_a, fips_b in PAIRS:
        pair_exprs.append(
            F.when(
                F.array_contains(F.col("country_codes"), fips_a) &
                F.array_contains(F.col("country_codes"), fips_b),
                F.lit(pair_id)
            )
        )

    # RU_EU: RS + any EU member
    eu_array = F.array(*[F.lit(c) for c in sorted(EU_FIPS)])
    ru_eu_match = (
        F.array_contains(F.col("country_codes"), "RS") &
        (F.size(F.array_intersect(F.col("country_codes"), eu_array)) > 0)
    )
    pair_exprs.append(F.when(ru_eu_match, F.lit("RU_EU")))

    df = df.withColumn(
        "matched_pairs",
        F.array_compact(F.array(*pair_exprs))
    )

    # Keep only articles that matched at least one pair
    df = df.filter(F.size(F.col("matched_pairs")) > 0)

    # Explode: one row per pair
    df = df.withColumn("pair_id", F.explode(F.col("matched_pairs")))

    return df.select(
        F.col("article_date").alias("date"),
        F.col("pair_id"),
        F.col("tone"),
        F.col("pos_tone"),
        F.col("neg_tone"),
        F.col("polarity"),
        F.col("DocumentIdentifier").alias("source_url"),
        F.col("_ingest_timestamp"),
        F.col("_source_file"),
    )
