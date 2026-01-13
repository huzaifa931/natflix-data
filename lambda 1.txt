import boto3
import os
import urllib.request

s3 = boto3.client('s3')

def lambda_handler(event, context):
    github_url = os.environ['GITHUB_CSV_URL']
    bucket = os.environ['S3_BUCKET_NAME']
    key = os.environ['S3_KEY']

    with urllib.request.urlopen(github_url) as response:
        data = response.read()

    # SIMPLE VALIDATION (IMPORTANT)
    if b'<!DOCTYPE html>' in data[:200]:
        raise Exception("Downloaded HTML instead of CSV")

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=data
    )

    return {
        "statusCode": 200,
        "body": "CSV uploaded successfully"
    }
