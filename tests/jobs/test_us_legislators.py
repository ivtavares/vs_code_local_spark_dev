from pyspark.sql import SparkSession

from app_name.jobs.us_legislators import convert_us_legistator
from tests.constants import SAMPLE_BRONZE_US_LEGISLATOR
from tests.utils import load_file_into_bucket


def test_convert_us_legislator(spark_session: SparkSession, s3_client):
    bronze_bucket_name = "test-bronze"
    s3_bronze_file_name = "us_legislators/person.json"
    s3_bronze_file_path = "s3://" + "/".join([bronze_bucket_name, s3_bronze_file_name])
    load_file_into_bucket(s3_client, SAMPLE_BRONZE_US_LEGISLATOR, bronze_bucket_name, s3_bronze_file_name)

    silver_bucket_name = "test-silver"
    s3_silver_file_path = "s3://" + "/".join([silver_bucket_name, "us_legislators"])
    s3_client.create_bucket(Bucket=silver_bucket_name)

    convert_us_legistator(s3_bronze_file_path, s3_silver_file_path)

    df = spark_session.read.format('delta').load(s3_silver_file_path)

    assert df.count() > 0
