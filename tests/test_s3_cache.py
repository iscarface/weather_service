import pytest
import json
from moto import mock_aws
from datetime import datetime, timedelta
from app.utils.s3 import get_s3_client
from app.services.s3_service import save_to_s3, get_from_s3
from app.config import settings

@pytest.fixture(scope="function")
def s3_client():
    """Fixture to mock S3 and ensure bucket exists."""
    with mock_aws():
        client = get_s3_client()
        # Create the bucket if it doesn't exist
        bucket_name = settings.s3_bucket_name
        existing_buckets = client.list_buckets().get("Buckets", [])
        if not any(bucket["Name"] == bucket_name for bucket in existing_buckets):
            client.create_bucket(Bucket=bucket_name)
        yield client


def test_save_to_s3(s3_client):
    city = "London"
    data = {"temperature": 15}
    save_to_s3(city, data)

    response = s3_client.get_object(Bucket=settings.s3_bucket_name, Key=f"{city}_latest.json")
    saved_data = json.loads(response["Body"].read())

    assert saved_data == data

def test_get_from_s3_valid_cache(s3_client):
    city = "London"
    data = {"temperature": 15}
    save_to_s3(city, data)

    cached_data = get_from_s3(city)
    assert cached_data == data

def test_get_from_s3_expired_cache(s3_client, monkeypatch):
    city = "London"
    data = {"temperature": 15}
    save_to_s3(city, data)

    # Simulate expired cache
    monkeypatch.setattr("datetime.datetime", lambda: datetime.now(datetime.UTC) + timedelta(minutes=6))

    cached_data = get_from_s3(city)
    assert cached_data is None
