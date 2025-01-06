from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.routes.weather.get_from_s3")
@patch("app.routes.weather.fetch_weather_data")
@patch("app.routes.weather.save_to_s3")
def test_weather_endpoint(mock_save_to_s3, mock_fetch_weather_data, mock_get_from_s3):
    # Mock valid cache
    mock_get_from_s3.return_value = {"temperature": 20}  # Ensure consistency
    response = client.get("/weather?city=London")
    assert response.status_code == 200
    assert response.json()["cached"] is True
    assert response.json()["data"]["temperature"] == 20

    # Mock cache miss
    mock_get_from_s3.return_value = None  # Simulate no cache
    mock_fetch_weather_data.return_value = {"temperature": 25}  # Ensure correct mock
    response = client.get("/weather?city=London")
    assert response.status_code == 200
    assert response.json()["cached"] is False
    assert response.json()["data"]["temperature"] == 25


@patch("app.routes.weather.get_from_s3")
@patch("app.routes.weather.fetch_weather_data")
@patch("app.routes.weather.save_to_s3")
def test_weather_endpoint_invalid_city(mock_save_to_s3, mock_fetch_weather_data, mock_get_from_s3):
    # Simulate no cache and API failure for invalid city
    mock_get_from_s3.return_value = None
    mock_fetch_weather_data.side_effect = Exception("City not found")

    response = client.get("/weather?city=InvalidCity")
    assert response.status_code == 500
    assert response.json()["detail"] == "City not found"


@patch("app.routes.weather.get_from_s3")
@patch("app.routes.weather.fetch_weather_data")
@patch("app.routes.weather.save_to_s3")
def test_weather_endpoint_external_api_failure(mock_save_to_s3, mock_fetch_weather_data, mock_get_from_s3):
    # Simulate no cache and external API failure
    mock_get_from_s3.return_value = None
    mock_fetch_weather_data.side_effect = Exception("External API error")

    response = client.get("/weather?city=London")
    assert response.status_code == 500
    assert response.json()["detail"] == "External API error"


@patch("app.routes.weather.get_from_s3")
@patch("app.routes.weather.fetch_weather_data")
@patch("app.routes.weather.save_to_s3")
def test_weather_endpoint_s3_failure(mock_save_to_s3, mock_fetch_weather_data, mock_get_from_s3):
    # Simulate cache failure in S3 and successful API fetch
    mock_get_from_s3.side_effect = Exception("S3 access error")
    mock_fetch_weather_data.return_value = {"temperature": 25}
    mock_save_to_s3.side_effect = Exception("S3 save error")

    response = client.get("/weather?city=London")
    assert response.status_code == 500
    assert response.json()["detail"] == "S3 access error"
