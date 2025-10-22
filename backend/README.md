# Flight Delay Prediction API - Backend

FastAPI-based REST API for predicting flight delays and retrieving airport information.

## Features

- **Prediction Endpoint**: Predict flight delay probability based on day of week and airport IDs
- **Airports Endpoint**: Retrieve sorted list of airports with pagination
- **Health Check**: Monitor API and model status
- **OpenAPI Documentation**: Interactive API documentation at `/docs`

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

## Running the Server

### Development Mode

Run using uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use Python directly:
```bash
python main.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Root
- `GET /` - API information and available endpoints

### Health Check
- `GET /health` - Check API health and model status

### Predictions
- `POST /predict` - Predict flight delay probability

**Request Body:**
```json
{
  "day_of_week": 5,
  "origin_airport_id": 13930,
  "dest_airport_id": 12892
}
```

**Response:**
```json
{
  "delay_probability": 0.3245,
  "confidence": 0.8912,
  "prediction": "LIKELY ON TIME"
}
```

### Airports
- `GET /airports?limit=100&offset=0` - Get sorted list of airports

**Response:**
```json
{
  "total": 350,
  "airports": [
    {
      "airport_id": 10397,
      "airport_name": "Hartsfield-Jackson Atlanta International",
      "city": "Atlanta",
      "state": "GA"
    }
  ]
}
```

## API Documentation

Once the server is running, visit:
- Interactive docs (Swagger UI): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc
- OpenAPI schema: http://localhost:8000/openapi.json

## Testing the API

### Using curl

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Predict Delay:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"day_of_week": 5, "origin_airport_id": 13930, "dest_airport_id": 12892}'
```

**Get Airports:**
```bash
curl "http://localhost:8000/airports?limit=10&offset=0"
```

### Using Python

```python
import requests

# Predict delay
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "day_of_week": 5,
        "origin_airport_id": 13930,
        "dest_airport_id": 12892
    }
)
print(response.json())

# Get airports
response = requests.get("http://localhost:8000/airports?limit=10")
print(response.json())
```

## Project Structure

```
backend/
├── main.py          # FastAPI application
├── openapi.yaml     # OpenAPI 3.0 specification
└── README.md        # This file
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- All dependencies from Phase 1 (pandas, scikit-learn, etc.)

## Notes

- The API automatically loads the trained model from the `../models` directory on startup
- CORS is enabled for all origins (configure for production)
- Default values are used for features not provided in the prediction request
- Airports are sorted alphabetically by name
