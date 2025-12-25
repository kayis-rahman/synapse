#!/bin/bash

# Start script for Model Switcher API Server
# This script runs the FastAPI server without requiring systemd service

echo "Starting Model Switcher API Server..."
echo "======================================"

# Check if python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 could not be found"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
if ! python3 -c "import fastapi; import uvicorn" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install fastapi uvicorn
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Start the FastAPI server on port 6006
echo "Starting server on port 6006..."
echo "Server will be available at http://localhost:6006"
echo "Use Ctrl+C to stop the server"

# Run the FastAPI server
python3 main.py --host 0.0.0.0 --port 6006