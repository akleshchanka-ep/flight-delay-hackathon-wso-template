#!/usr/bin/env python3
"""
Flight Delay Prediction API
============================

FastAPI application for predicting flight delays and retrieving airport information.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import joblib
import pandas as pd
import json
import os
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Flight Delay Prediction API",
    description="API for predicting flight delays and retrieving airport information",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and data
model = None
label_encoders = None
feature_columns = None
airports_df = None

# Request/Response Models
class PredictionRequest(BaseModel):
    day_of_week: int = Field(..., ge=1, le=7, description="Day of the week (1=Monday, 7=Sunday)")
    origin_airport_id: int = Field(..., description="ID of the origin airport")
    dest_airport_id: int = Field(..., description="ID of the destination airport")
    
    @field_validator('day_of_week')
    @classmethod
    def validate_day_of_week(cls, v):
        if v < 1 or v > 7:
            raise ValueError('day_of_week must be between 1 and 7')
        return v

class PredictionResponse(BaseModel):
    delay_probability: float = Field(..., ge=0, le=1, description="Probability of delay > 15 minutes")
    confidence: float = Field(..., ge=0, le=1, description="Confidence level of prediction")
    prediction: str = Field(..., description="Human-readable prediction result")

class Airport(BaseModel):
    airport_id: int
    airport_name: str
    city: str
    state: str

class AirportsResponse(BaseModel):
    total: int
    airports: List[Airport]

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool

# Startup event to load model
@app.on_event("startup")
async def load_model():
    """Load the trained model and associated data on startup."""
    global model, label_encoders, feature_columns, airports_df
    
    try:
        # Determine the correct path to models directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models')
        
        logger.info(f"Loading model from {models_dir}")
        
        # Load model and encoders
        model = joblib.load(os.path.join(models_dir, 'flight_delay_model.pkl'))
        label_encoders = joblib.load(os.path.join(models_dir, 'label_encoders.pkl'))
        
        # Load feature columns
        with open(os.path.join(models_dir, 'feature_columns.json'), 'r') as f:
            feature_columns = json.load(f)
        
        # Load airports data
        airports_df = pd.read_csv(os.path.join(models_dir, 'airports.csv'))
        
        # Sort airports by name for consistent ordering
        airports_df = airports_df.sort_values('AirportName').reset_index(drop=True)
        
        logger.info("Model and data loaded successfully!")
        logger.info(f"Available airports: {len(airports_df)}")
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Flight Delay Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "airports": "/airports",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_delay(request: PredictionRequest):
    """
    Predict the probability of a flight being delayed by more than 15 minutes.
    
    Args:
        request: PredictionRequest containing day_of_week, origin_airport_id, and dest_airport_id
    
    Returns:
        PredictionResponse with delay probability, confidence, and prediction
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Validate airport IDs exist
        if request.origin_airport_id not in airports_df['AirportID'].values:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid origin_airport_id: {request.origin_airport_id}"
            )
        
        if request.dest_airport_id not in airports_df['AirportID'].values:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid dest_airport_id: {request.dest_airport_id}"
            )
        
        # Create input data with default values for features not provided
        # Using typical values based on the dataset
        input_data = pd.DataFrame({
            'Month': [6],  # Mid-year default
            'DayofMonth': [15],  # Mid-month default
            'DayOfWeek': [request.day_of_week],
            'OriginAirportID': [request.origin_airport_id],
            'DestAirportID': [request.dest_airport_id],
            'CRSDepTime_Hour': [12],  # Noon default
            'CRSArrTime_Hour': [14],  # 2 PM default
            'Carrier': [0]  # Default encoded carrier
        })
        
        # Make prediction
        probability = model.predict_proba(input_data)[0, 1]
        prediction = model.predict(input_data)[0]
        
        # Calculate confidence (using the max probability as a proxy for confidence)
        confidence = max(model.predict_proba(input_data)[0])
        
        # Determine prediction text
        prediction_text = "LIKELY DELAYED" if prediction == 1 else "LIKELY ON TIME"
        
        logger.info(
            f"Prediction: day={request.day_of_week}, "
            f"origin={request.origin_airport_id}, dest={request.dest_airport_id}, "
            f"prob={probability:.4f}, result={prediction_text}"
        )
        
        return PredictionResponse(
            delay_probability=float(probability),
            confidence=float(confidence),
            prediction=prediction_text
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/airports", response_model=AirportsResponse, tags=["Airports"])
async def get_airports(
    limit: int = 100,
    offset: int = 0
):
    """
    Get a list of all airports sorted alphabetically by name.
    
    Args:
        limit: Maximum number of airports to return (default: 100)
        offset: Number of airports to skip for pagination (default: 0)
    
    Returns:
        AirportsResponse with total count and list of airports
    """
    if airports_df is None:
        raise HTTPException(status_code=500, detail="Airports data not loaded")
    
    try:
        # Validate parameters
        if limit < 1 or limit > 1000:
            raise HTTPException(status_code=400, detail="limit must be between 1 and 1000")
        
        if offset < 0:
            raise HTTPException(status_code=400, detail="offset must be non-negative")
        
        # Get total count
        total = len(airports_df)
        
        # Apply pagination
        paginated_df = airports_df.iloc[offset:offset + limit]
        
        # Convert to response format
        airports_list = [
            Airport(
                airport_id=int(row['AirportID']),
                airport_name=str(row['AirportName']),
                city=str(row['City']),
                state=str(row['State'])
            )
            for _, row in paginated_df.iterrows()
        ]
        
        logger.info(f"Returning {len(airports_list)} airports (offset={offset}, limit={limit})")
        
        return AirportsResponse(
            total=total,
            airports=airports_list
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching airports: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch airports: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
