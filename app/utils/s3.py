from functools import lru_cache

import boto3

from app.config import settings


@lru_cache()
def get_s3_client():
    """Return a singleton DynamoDB client."""
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
