# Databricks notebook source
# One-time Unity Catalog setup for the geopolitics project.
# All statements use IF NOT EXISTS — safe to re-run at any time.

# COMMAND ----------

catalog = "geopolitics"

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"USE CATALOG {catalog}")

# COMMAND ----------

# gdelt_narrative schema + volume

spark.sql("CREATE SCHEMA IF NOT EXISTS geopolitics.gdelt_narrative")

spark.sql("""
    CREATE VOLUME IF NOT EXISTS geopolitics.gdelt_narrative.raw_gkg
    COMMENT 'Raw GDELT GKG 2.0 CSV files, partitioned by date (YYYY/MM/DD)'
""")

print("geopolitics.gdelt_narrative schema and raw_gkg volume: OK")

# COMMAND ----------

# Verify

display(spark.sql("SHOW SCHEMAS IN geopolitics"))
display(spark.sql("SHOW VOLUMES IN geopolitics.gdelt_narrative"))
