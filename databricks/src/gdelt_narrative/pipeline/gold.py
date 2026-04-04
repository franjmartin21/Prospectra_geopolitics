# Databricks notebook source
# SDP Gold Layer — Daily sentiment aggregation + rolling z-score index
# Input:  silver_country_pairs
# Output: gold_daily_sentiment (streaming append)
#         gold_sentiment_index (materialized view, full refresh)

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# COMMAND ----------

@dlt.table(
    name    = "gold_daily_sentiment",
    comment = "Daily average tone scores per country-pair. Append-only.",
    table_properties = {
        "quality": "gold",
        "delta.autoOptimize.optimizeWrite": "true",
        "pipelines.reset.allowed": "true",
    },
    partition_cols = ["pair_id"],
)
def gold_daily_sentiment():
    return (
        dlt.read_stream("silver_country_pairs")
            .groupBy("date", "pair_id")
            .agg(
                F.count("*")          .alias("article_count"),
                F.avg("tone")         .alias("avg_tone"),
                F.avg("neg_tone")     .alias("avg_neg_tone"),
                F.avg("pos_tone")     .alias("avg_pos_tone"),
                F.avg("polarity")     .alias("avg_polarity"),
            )
    )

# COMMAND ----------

@dlt.table(
    name    = "gold_sentiment_index",
    comment = "Rolling 30-day sentiment index with z-score anomaly detection. Full refresh materialized view. This is the primary investment signal table.",
    table_properties = {
        "quality": "gold",
        "pipelines.reset.allowed": "true",
    },
    partition_cols = ["pair_id"],
)
def gold_sentiment_index():
    from pyspark.sql.window import Window

    w30 = (
        Window
        .partitionBy("pair_id")
        .orderBy("date")
        .rowsBetween(-29, 0)   # 30-day trailing window (inclusive)
    )

    daily = dlt.read("gold_daily_sentiment")

    return (
        daily
        .withColumn("rolling_30d_mean", F.avg("avg_tone").over(w30))
        .withColumn("rolling_30d_std",  F.stddev("avg_tone").over(w30))
        .withColumn(
            "z_score",
            (F.col("avg_tone") - F.col("rolling_30d_mean"))
            / F.nullif(F.col("rolling_30d_std"), F.lit(0.0))
        )
        .withColumn(
            "is_anomaly",
            F.abs(F.col("z_score")) > F.lit(2.0)
        )
        .select(
            "date",
            "pair_id",
            "article_count",
            "avg_tone",
            "avg_neg_tone",
            "avg_pos_tone",
            "avg_polarity",
            "rolling_30d_mean",
            "rolling_30d_std",
            "z_score",
            "is_anomaly",
        )
    )
