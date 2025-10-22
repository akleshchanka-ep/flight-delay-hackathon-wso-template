#!/bin/bash

# Script to start both backend API and frontend development server

echo "🚀 Starting Flight Delay Predictor - Full Stack"
echo "================================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Check if backend virtual environment exists
if [ ! -d "$PROJECT_ROOT/flight_model_env" ]; then
    echo "❌ Error: Python virtual environment not found!"
    echo "Please run: python3 -m venv flight_model_env"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd "$PROJECT_ROOT/frontend"
    npm install
    cd "$PROJECT_ROOT"
fi

echo "🔧 Starting Backend API..."
# Start backend in background
cd "$PROJECT_ROOT/backend"
source ../flight_model_env/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd "$PROJECT_ROOT"

# Give backend time to start
sleep 3

echo "✅ Backend API started on http://localhost:8000"
echo ""
echo "🎨 Starting Frontend..."
# Start frontend in background
cd "$PROJECT_ROOT/frontend"
npm run dev &
FRONTEND_PID=$!
cd "$PROJECT_ROOT"

# Give frontend time to start
sleep 3

echo ""
echo "✅ Frontend started on http://localhost:4321"
echo ""
echo "================================================"
echo "🌐 Application URLs:"
echo "   Frontend:  http://localhost:4321"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "================================================"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Kill any remaining processes on these ports
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:4321 | xargs kill -9 2>/dev/null
    echo "✅ All servers stopped"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Wait for both processes
wait
