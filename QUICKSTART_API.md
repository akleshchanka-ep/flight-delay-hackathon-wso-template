# Quick Start Guide - Flight Delay API

## Phase 2 Complete! 🎉

The FastAPI backend has been successfully implemented with all required endpoints.

## What's Been Built

### 1. Backend Structure
```
backend/
├── main.py           # FastAPI application
├── openapi.yaml      # OpenAPI 3.0 specification
├── test_api.py       # API test suite
├── run_server.sh     # Server startup script
└── README.md         # Detailed documentation
```

### 2. API Endpoints

#### Health Check
```bash
GET /health
```

#### Predict Flight Delay
```bash
POST /predict
Content-Type: application/json

{
  "day_of_week": 5,
  "origin_airport_id": 13930,
  "dest_airport_id": 12892
}
```

#### Get Airports List
```bash
GET /airports?limit=100&offset=0
```

## How to Run

### 1. Start the Server

**Option A - Using the startup script:**
```bash
cd backend
./run_server.sh
```

**Option B - Using uvicorn directly:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option C - Using Python:**
```bash
cd backend
python main.py
```

### 2. Access the API

- **API Base URL:** http://localhost:8000
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

### 3. Test the API

Run the test suite:
```bash
cd backend
python test_api.py
```

## Example Usage

### Using curl

**Make a prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "day_of_week": 5,
    "origin_airport_id": 13930,
    "dest_airport_id": 12892
  }'
```

**Get airports:**
```bash
curl "http://localhost:8000/airports?limit=10"
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
# Output:
# {
#   "delay_probability": 0.3245,
#   "confidence": 0.8912,
#   "prediction": "LIKELY ON TIME"
# }

# Get airports
response = requests.get("http://localhost:8000/airports?limit=5")
print(response.json())
# Output:
# {
#   "total": 350,
#   "airports": [
#     {
#       "airport_id": 10397,
#       "airport_name": "Hartsfield-Jackson Atlanta International",
#       "city": "Atlanta",
#       "state": "GA"
#     },
#     ...
#   ]
# }
```

### Using JavaScript/Fetch

```javascript
// Predict delay
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    day_of_week: 5,
    origin_airport_id: 13930,
    dest_airport_id: 12892
  })
})
  .then(res => res.json())
  .then(data => console.log(data));

// Get airports
fetch('http://localhost:8000/airports?limit=10')
  .then(res => res.json())
  .then(data => console.log(data));
```

## Key Features

✅ **OpenAPI 3.0 Specification** - Complete API documentation in `backend/openapi.yaml`

✅ **Prediction Endpoint** - Returns delay probability, confidence, and human-readable prediction

✅ **Airports Endpoint** - Sorted alphabetically with pagination support

✅ **Interactive Documentation** - Swagger UI at `/docs` for testing

✅ **Health Check** - Monitor API and model status

✅ **CORS Enabled** - Ready for frontend integration

✅ **Error Handling** - Validates input and provides clear error messages

✅ **Type Safety** - Using Pydantic models for request/response validation

## Technical Details

- **Framework:** FastAPI 0.104+
- **Server:** Uvicorn with auto-reload
- **Validation:** Pydantic v2
- **Model:** Loaded from `../models/flight_delay_model.pkl`
- **Data:** Airports from `../models/airports.csv`

## Next Steps

Ready for **Phase 3: Create a user-friendly frontend!**

The API is fully functional and ready to be consumed by a frontend application.

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Model not found:**
Ensure you've completed Phase 1 and the model exists at `models/flight_delay_model.pkl`

**Dependencies missing:**
```bash
pip install -r requirements.txt
```
