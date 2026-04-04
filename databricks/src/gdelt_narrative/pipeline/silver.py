# Databricks notebook source
# SDP Silver Layer — Parse + country-pair filter
# Input:  bronze_gkg_raw
# Output: silver_country_pairs

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

# COMMAND ----------

# Country-pair matrix — GDELT uses FIPS-10 country codes, not ISO-2
PAIRS = [
    ("US_CN", "US", "CH"),
    ("US_RU", "US", "RS"),
    ("CN_TW", "CH", "TW"),
    ("SA_US", "SA", "US"),
    ("SA_CN", "SA", "CH"),
    ("IN_CN", "IN", "CH"),
    # Spain bilateral pairs (FIPS code: SP)
    ("SP_RU", "SP", "RS"),
    ("SP_CN", "SP", "CH"),
    ("SP_US", "SP", "US"),
]

# EU approximation: any article mentioning one of these major EU economies
# qualifies as "EU" for bloc-level pairs (RU_EU, US_EU, CN_EU, SP_EU).
# FIPS codes: GM=Germany, FR=France, IT=Italy, SP=Spain, PL=Poland, EI=Ireland
EU_FIPS = ["GM", "FR", "IT", "SP", "PL", "EI"]

# EU_FIPS excluding Spain — used for SP_EU so we don't match Spain with itself
EU_FIPS_NO_SP = ["GM", "FR", "IT", "PL", "EI"]

# Multi-country EU pairs: (pair_id, other_country_fips, eu_fips_list)
EU_PAIRS = [
    ("RU_EU", "RS",  EU_FIPS),       # Russia vs EU bloc
    ("US_EU", "US",  EU_FIPS),       # US vs EU bloc
    ("CN_EU", "CH",  EU_FIPS),       # China vs EU bloc
    ("SP_EU", "SP",  EU_FIPS_NO_SP), # Spain vs rest of EU (intra-EU tensions)
]

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
    # Use split column with getItem() — do NOT wrap in F.col()
    tone_split = F.split(F.col("V2Tone"), ",")
    df = (df
        .withColumn("tone",                 tone_split.getItem(0).cast(DoubleType()))
        .withColumn("pos_tone",             tone_split.getItem(1).cast(DoubleType()))
        .withColumn("neg_tone",             tone_split.getItem(2).cast(DoubleType()))
        .withColumn("polarity",             tone_split.getItem(3).cast(DoubleType()))
        .withColumn("activity_ref_density", tone_split.getItem(4).cast(DoubleType()))
        .withColumn("self_ref_density",     tone_split.getItem(5).cast(DoubleType()))
    )

    # --- Extract country codes from V2Locations via SQL expression ---
    # V2Locations format: "type#name#countrycode#adm1#lat#lon#featureid;..."
    # element_at is 1-indexed in Spark SQL
    df = df.withColumn(
        "country_codes",
        F.array_distinct(
            F.expr("""
                filter(
                    transform(
                        filter(split(V2Locations, ';'), loc -> length(loc) > 0),
                        loc -> element_at(split(loc, '#'), 3)
                    ),
                    cc -> cc is not null and length(cc) > 0
                )
            """)
        )
    )

    # Drop articles with fewer than 2 country mentions
    df = df.filter(F.size(F.col("country_codes")) >= 2)

    # --- Build matched_pairs column ---
    pair_cases = []

    # Simple bilateral pairs
    for pair_id, fips_a, fips_b in PAIRS:
        pair_cases.append(
            F.when(
                F.array_contains(F.col("country_codes"), fips_a) &
                F.array_contains(F.col("country_codes"), fips_b),
                F.lit(pair_id)
            )
        )

    # EU multi-country pairs: other_country + any member of the pair's EU list qualifies
    for pair_id, other_fips, eu_list in EU_PAIRS:
        eu_check = " OR ".join([f"array_contains(country_codes, '{c}')" for c in eu_list])
        eu_match = F.array_contains(F.col("country_codes"), other_fips) & F.expr(f"({eu_check})")
        pair_cases.append(F.when(eu_match, F.lit(pair_id)))

    df = df.withColumn("matched_pairs", F.array_compact(F.array(*pair_cases)))
    df = df.filter(F.size(F.col("matched_pairs")) > 0)

    # Explode: one row per matched pair
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
