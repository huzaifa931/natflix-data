import json
import boto3

s3 = boto3.client('s3')

PROCESSED_BUCKET = "netflix-data-001"

def lambda_handler(event, context):
    try:
        record = event['Records'][0]
        source_bucket = record['s3']['bucket']['name']
        source_key = record['s3']['object']['key']

        # Validate CSV file
        if not source_key.endswith(".csv"):
            raise Exception("Not a CSV file")

        response = s3.head_object(Bucket=source_bucket, Key=source_key)

        if response['ContentLength'] == 0:
            raise Exception("Empty file")

        # Copy to processed bucket
        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
        }

        processed_key = source_key.replace("raw/", "processed/")

        s3.copy_object(
            CopySource=copy_source,
            Bucket=PROCESSED_BUCKET,
            Key=processed_key
        )

        # Delete from raw
        s3.delete_object(
            Bucket=source_bucket,
            Key=source_key
        )

        return {
            "statusCode": 200,
            "body": "File validated and moved to processed layer"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
