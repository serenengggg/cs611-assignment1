"""BRONZE: raw data landed as-is (all columns as string), plus ingestion metadata.

No cleaning, no typing, no filtering - bronze is the immutable source of truth
that lets us reprocess silver/gold at any time.
"""
import os
from pyspark.sql import functions as F

from utils.config import DATA_DIR, BRONZE, SOURCES
from utils.spark_io import write_table


def build_bronze_table(spark, name):
    df = (
        spark.read.option("header", True).option("inferSchema", False)
        .csv(os.path.join(DATA_DIR, SOURCES[name]))
        .withColumn("_source_file", F.lit(SOURCES[name]))
        .withColumn("_ingested_at", F.current_timestamp())
    )
    write_table(df, os.path.join(BRONZE, name), "csv")
    return df.count()


def run_bronze(spark):
    print("== BRONZE ==")
    for name in SOURCES:
        print(f"{name}: {build_bronze_table(spark, name)} rows")
