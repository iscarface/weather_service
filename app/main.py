import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.s3_service import create_bucket
from app.services.dynamodb_service import initialize_dynamodb
from app.routes.weather import router as weather_router
from app.config import settings


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing S3 bucket...")
        create_bucket(settings.s3_bucket_name)
        logger.info(f"S3 bucket '{settings.s3_bucket_name}' initialized successfully.")
        
        logger.info("Initializing DynamoDB table...")
        initialize_dynamodb()
        logger.info("DynamoDB table initialized successfully.")

        yield  # App is running

    except Exception as e:
        logger.error(f"Lifespan initialization failed: {e}")
        raise

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Include routes
app.include_router(weather_router, prefix="")

@app.get("/")
async def root():
    return {"message": "Weather API is running!"}
