import boto3
from botocore.exceptions import ClientError

from app.config import settings
from app.utils.dynamodb import get_dynamodb_client


# Initialize DynamoDB client with dummy credentials


def initialize_dynamodb():
    """Create the DynamoDB table if it doesn't exist."""
    table_name = settings.dynamodb_table_name
    dynamodb_client = get_dynamodb_client()

    try:
        # Check if the table already exists
        existing_tables = dynamodb_client.list_tables()["TableNames"]
        if table_name in existing_tables:
            print(f"Table '{table_name}' already exists.")
            return

        # Create the table
        dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "city", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "weather_timestamp", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "city", "AttributeType": "S"},
                {"AttributeName": "weather_timestamp", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        print(f"Table '{table_name}' created successfully.")
    except ClientError as e:
        print(f"Failed to create table: {e}")
