import logging

import boto3
import pytest
import requests
from moto.server import ThreadedMotoServer
from pyspark.sql import SparkSession, session
from pytest import MonkeyPatch
from unittest.mock import Mock


MOTO_PORT = 5050
MOTO_ENDPOINT = f"http://localhost:{MOTO_PORT}"


@pytest.fixture(scope="session")
def monkeysession():
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(scope="session")
def spark_session(moto_server, monkeysession: MonkeyPatch) -> SparkSession:
    """Fixture for creating a Spark context."""
    spark_session = (
        SparkSession.builder.appName("test")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )

    hadoop_conf = spark_session._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
    hadoop_conf.set("fs.s3a.access.key", "mock")
    hadoop_conf.set("fs.s3a.secret.key", "mock")
    hadoop_conf.set("fs.s3a.endpoint", MOTO_ENDPOINT)
    hadoop_conf.set("fs.s3a.path.style.access", "true")
    hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")

    spark_session.stop_for_real = spark_session.stop
    monkeysession.setattr(session.SparkSession, "__new__", spark_session)
    monkeysession.setattr(session.SparkSession, "stop", Mock())

    yield spark_session
    spark_session.stop_for_real()


@pytest.fixture(scope="session")
def s3_client():
    """
    Fixture for creating an S3 client.
    """
    s3_endpoint_url = MOTO_ENDPOINT
    aws_access_key_id = "mock"
    aws_secret_access_key = "mock"

    s3_client = boto3.client(
        "s3",
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    yield s3_client


@pytest.fixture(scope="session")
def moto_server():
    """
    Fixture for starting the Moto server.
    """
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    try:
        requests.get(MOTO_ENDPOINT)
    except requests.exceptions.ConnectionError:
        server = ThreadedMotoServer(port=MOTO_PORT)
        server.start()
        yield server
        server.stop()
