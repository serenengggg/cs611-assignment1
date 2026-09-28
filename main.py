"""Runs the whole medallion pipeline: raw csv -> bronze -> silver -> gold (feature + label store)."""
import shutil
import os

from utils.config import DATAMART
from utils.spark_io import get_spark
from utils.bronze_processing import run_bronze
from utils.silver_processing import run_silver
from utils.gold_processing import run_gold


def main():
    if os.path.exists(DATAMART):
        shutil.rmtree(DATAMART)  # idempotent full rebuild
    spark = get_spark()
    run_bronze(spark)
    run_silver(spark)
    run_gold(spark)

    feats = spark.read.parquet(os.path.join(DATAMART, "gold", "feature_store"))
    labels = spark.read.parquet(os.path.join(DATAMART, "gold", "label_store"))
    print(f"feature_store: {feats.count()} rows x {len(feats.columns)} cols")
    print(f"label_store:   {labels.count()} rows, default rate = "
          f"{labels.agg({'label': 'avg'}).collect()[0][0]:.3f}")
    spark.stop()


if __name__ == "__main__":
    main()
