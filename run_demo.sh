#!/bin/bash
# RHISA Healthcare Chatbot - Demo Mode Launcher
# Runs without AWS resources for testing

echo "============================================================"
echo "RHISA Healthcare Chatbot - Demo Mode"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install requirements if needed
echo "Checking dependencies..."
pip install Flask flask-cors python-dotenv --quiet
echo ""

# Set environment variables
export FLASK_ENV=development
export PORT=5000

# Start demo server
echo "Starting RHISA Demo Server..."
echo "Server will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python app_demo.py
