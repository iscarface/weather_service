from fastapi import APIRouter, HTTPException

from app.services.weather_service import fetch_weather_data, save_weather_log
from app.services.s3_service import get_from_s3, save_to_s3


router = APIRouter()


@router.get("/weather")
async def get_weather(city: str):
    """
    Fetch weather information for a given city.
    1. Check recent cached data in DynamoDB.
    2. If not cached, fetch data from OpenWeatherMap.
    3. Save the new data in DynamoDB.
    """
    try:
        # Check for recent data in DynamoDB
        cached_data = get_from_s3(city)
        if cached_data:
            return {"cached": True, "data": cached_data}

        # Fetch data from OpenWeatherMap
        weather_data = await fetch_weather_data(city)

        # Save the weather data to S3
        save_to_s3(city, weather_data)
        # Save the weather data to DynamoDB
        save_weather_log(city, weather_data)

        return {"cached": False, "data": weather_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
