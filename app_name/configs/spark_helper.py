from pyspark.sql import SparkSession
from typing import List


def create_delta_lake_session(app_name: str, jars_packages: List[str] = [], **extra_configs: str) -> SparkSession:
    builder = SparkSession.builder.appName(app_name)

    jars_packages = ["io.delta:delta-core_2.12:2.1.0"] + jars_packages
    jars_packages = ",".join(jars_packages)

    builder = (
        builder.config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
    )

    for key, value in extra_configs.items():
        builder = builder.config(key, value)

    spark = builder.getOrCreate()
    return spark
