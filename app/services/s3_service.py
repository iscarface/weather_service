import json
import logging
from datetime import datetime, timezone

from botocore.exceptions import NoCredentialsError, ClientError

from app.config import settings
from app.utils.s3 import get_s3_client


logger = logging.getLogger(__name__)
s3_client = get_s3_client()


def create_bucket(bucket_name: str):
    """Create a bucket if it doesn't already exist."""
    try:
        response = s3_client.list_buckets()
        if bucket_name in [bucket["Name"] for bucket in response.get("Buckets", [])]:
            logger.info(f"Bucket '{bucket_name}' already exists.")
            return
        s3_client.create_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        logger.error(f"Failed to create bucket: {e}")
    except NoCredentialsError:
        logger.error("S3 credentials not available.")


def save_to_s3(city: str, data: dict):
    """Save weather data to S3 with a timestamp."""
    timestamp = datetime.now(timezone.utc).isoformat()
    key = f"{city}_latest.json"
    try:
        s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
            Body=json.dumps(data),
            Metadata={"timestamp": timestamp},
            ContentType="application/json",
        )
        logger.info(f"Saved cache for {city} to S3 with timestamp {timestamp}.")
    except Exception as e:
        logger.error(f"Failed to save weather data to S3: {e}")


def get_from_s3(city: str, max_age_seconds: int = 300):
    """Retrieve weather data from S3 if valid (not expired)."""
    key = f"{city}_latest.json"
    try:
        response = s3_client.head_object(Bucket=settings.s3_bucket_name, Key=key)
        last_modified = response["LastModified"]

        if (datetime.now(timezone.utc) - last_modified).total_seconds() > max_age_seconds:
            logger.info(f"Cache expired for {city}.")
            return None

        cached_object = s3_client.get_object(Bucket=settings.s3_bucket_name, Key=key)
        cached_data = json.loads(cached_object["Body"].read())
        logger.info(f"Retrieved cache for {city} from S3.")
        return cached_data
    except s3_client.exceptions.NoSuchKey:
        logger.info(f"No cache found for {city}.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving cache for {city}: {e}")
        return None
