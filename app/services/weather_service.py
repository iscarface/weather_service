import datetime
import boto3
import httpx
from app.utils.dynamodb import get_dynamodb_client
from app.config import settings
import logging

logger = logging.getLogger(__name__)
dynamodb_client = get_dynamodb_client()


def save_weather_log(city: str, weather_data: dict):
    """Save weather data to DynamoDB."""
    weather_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        dynamodb_client.put_item(
            TableName=settings.dynamodb_table_name,
            Item={
                "city": {"S": city},
                "weather_timestamp": {"S": weather_timestamp},
                "weather_data": {"S": str(weather_data)},
            },
        )
        logger.info(f"Weather data for {city} saved to DynamoDB.")
    except Exception as e:
        logger.error(f"Failed to save weather data to DynamoDB: {e}")


def get_recent_weather_log(city: str):
    """Fetch recent weather data from DynamoDB."""
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=5)).isoformat()
    try:
        response = dynamodb_client.query(
            TableName=settings.dynamodb_table_name,
            KeyConditionExpression="city = :city AND weather_timestamp > :cutoff",
            ExpressionAttributeValues={
                ":city": {"S": city},
                ":cutoff": {"S": cutoff},
            },
        )
        logger.info(f"Fetched recent weather logs for {city}.")
        return response.get("Items", [])
    except Exception as e:
        logger.error(f"Failed to query DynamoDB: {e}")
        return None


async def fetch_weather_data(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={settings.openweathermap_api_key}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            logger.info(f"Fetched weather data for {city} from OpenWeatherMap.")
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch weather data for {city}: {e}")
        raise
