#!/bin/bash

echo "========================================"
echo "  NeerVeda Smart Agriculture Dashboard"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
echo "Installing/updating requirements..."
pip install -r requirements.txt

# Start the application
echo ""
echo "Starting NeerVeda..."
echo "Open your browser and go to: http://localhost:5000"
echo ""
python start.py