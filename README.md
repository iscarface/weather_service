
# **Weather Service Application**

This project is a weather service application built with **FastAPI**, designed to fetch weather data from an external API (e.g., OpenWeatherMap) and store/cache the results in **S3-compatible storage (MinIO)** and **DynamoDB (local or AWS equivalent)**. It also features caching to reduce external API calls, with a cache expiration of 5 minutes.

### **Tech Stack**
- **FastAPI**: For building the RESTful API.
- **S3-Compatible Storage (MinIO)**: For caching weather data as JSON files.
- **DynamoDB (Local or AWS)**: For logging weather requests and storing metadata.
- **Docker & Docker Compose**: For containerization and managing services.
- **Python**: For the core application logic.
- **Testing Tools**: `pytest` and `moto` for unit and integration tests.

---

## **Setup and Run Instructions**

### **1. Prerequisites**
- Install **Docker** and **Docker Compose**:
  - [Docker Installation Guide](https://docs.docker.com/get-docker/)
  - Docker Compose is included with Docker Desktop for Windows and macOS.

### **2. Fill in the `.env` File**
Create a `.env` file in the root directory. Use the `.env.example` file as a reference to define all necessary environment variables. Example variables include:
```env
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
S3_ENDPOINT_URL=http://minio:9000
S3_BUCKET_NAME=weather-data
DYNAMODB_ENDPOINT_URL=http://dynamodb:8000
DYNAMODB_TABLE_NAME=weather_logs
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_REGION=us-west-2
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

### **3. Start the Project**
From the root directory, run the following command:
```bash
docker-compose -f deployment/docker-compose.yaml up --build --force-recreate
```

### **4. Access the Application**
The project will be accessible via `localhost`. For example:
- **Weather Endpoint**:
  ```
  http://localhost:8888/weather?city=Lagos,pt
  ```

---

## **Running Tests**

To run the tests inside the Docker container, use the following command:
```bash
docker exec -it weather_service pytest tests
```

---

## **Notes**
- Replace `your_openweathermap_api_key` with your actual OpenWeatherMap API key in the `.env` file.
- The application is configured to use **MinIO** (S3-compatible) and **DynamoDB Local** for local development.
