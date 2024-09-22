import boto3
from botocore.exceptions import NoCredentialsError
from pathlib import Path

def upload_to_aws(local_file_path, s3_folder, config):
    s3 = boto3.client('s3', aws_access_key_id=config.aws_access_key,
                      aws_secret_access_key=config.aws_access_token)
    filename = Path(local_file_path).name
    s3_path = f"{s3_folder}/{filename}"
    try:
        s3.upload_file(local_file_path, config.aws_s3_bucket, s3_path)#, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        file_url = f"https://{config.aws_s3_bucket}.s3.amazonaws.com/{s3_path}"
        return file_url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
