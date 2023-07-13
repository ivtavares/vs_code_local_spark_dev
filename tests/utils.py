def load_file_into_bucket(s3_client, file_path: str, target_bucket_name: str, target_file_path: str):
    s3_client.create_bucket(Bucket=target_bucket_name)

    with open(file_path, "rb") as f:
        s3_client.upload_fileobj(f, target_bucket_name, target_file_path)
