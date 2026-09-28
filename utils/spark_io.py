"""Small Spark helpers shared by all layers."""
import os
from pyspark.sql import SparkSession


def get_spark(app_name="medallion_pipeline"):
    spark = (
        SparkSession.builder.master("local[*]")
        .appName(app_name)
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def write_table(df, path, fmt, partition_col="snapshot_date"):
    """Overwrite a table folder, partitioned by snapshot_date (one sub-folder per snapshot)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    writer = df.write.mode("overwrite").format(fmt)
    if fmt == "csv":
        writer = writer.option("header", True)
    writer.partitionBy(partition_col).save(path)
    print(f"  wrote {path}")
