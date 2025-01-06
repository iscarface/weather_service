from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings): 
    # OpenWeatherMap API Key
    openweathermap_api_key: str = Field(..., json_schema_extra={"env": "OPENWEATHERMAP_API_KEY"})
    
    # S3 Configuration
    s3_endpoint_url: str = Field("http://localhost:9000", json_schema_extra={"env": "S3_ENDPOINT_URL"})
    s3_bucket_name: str = Field(..., json_schema_extra={"env": "S3_BUCKET_NAME"})

    # DynamoDB
    dynamodb_endpoint_url: str = Field("http://dynamodb:8888", json_schema_extra={"env": "DYNAMODB_ENDPOINT_URL"})
    dynamodb_table_name: str = Field(..., json_schema_extra={"env": "DYNAMODB_TABLE_NAME"})

    # AWS General
    aws_access_key_id: str = Field(..., json_schema_extra={"env": "AWS_ACCESS_KEY_ID"})
    aws_secret_access_key: str = Field(..., json_schema_extra={"env": "AWS_SECRET_ACCESS_KEY"})
    aws_region: str = Field("us-west-2", json_schema_extra={"env": "AWS_REGION"})

    # MinIO Configuration
    minio_root_user: str = Field(..., json_schema_extra={"env": "MINIO_ROOT_USER"})
    minio_root_password: str = Field(..., json_schema_extra={"env": "MINIO_ROOT_PASSWORD"})

    # Use ConfigDict for Pydantic 2.0+
    model_config = ConfigDict(env_file=".env")

# Create a global settings instance
settings = Settings()
