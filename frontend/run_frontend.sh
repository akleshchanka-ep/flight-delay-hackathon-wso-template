#!/bin/bash

# Script to start the frontend development server

echo "🚀 Starting Flight Delay Predictor Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Dependencies not found. Installing..."
    npm install
fi

# Start the dev server
echo "🌐 Starting Astro dev server on http://localhost:4321"
echo "📡 Backend API should be running on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
