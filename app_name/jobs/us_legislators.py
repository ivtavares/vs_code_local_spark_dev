from app_name.configs.spark_helper import create_delta_lake_session


def convert_us_legistator(bronze_path: str, silver_path: str):
    spark = create_delta_lake_session('us-legislator')
    df = spark.read.json(bronze_path)
    df.write.format('delta').save(silver_path)
    spark.stop()


if __name__ == '__main__':
    convert_us_legistator('s3://bronze/us_legislator', 's3://silver/us_legislator')
