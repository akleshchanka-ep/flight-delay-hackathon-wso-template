#!/bin/bash
# Script to start the Flight Delay Prediction API server

echo "Starting Flight Delay Prediction API..."
echo "========================================="
echo ""
echo "API will be available at: http://localhost:8000"
echo "Interactive docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_ENV="$PROJECT_ROOT/flight_model_env/bin/python"

# Check if virtual environment exists
if [ ! -f "$PYTHON_ENV" ]; then
    echo "Error: Python virtual environment not found at $PYTHON_ENV"
    echo "Please ensure the virtual environment is created."
    exit 1
fi

# Run uvicorn using the virtual environment's Python
cd "$SCRIPT_DIR"
"$PYTHON_ENV" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
