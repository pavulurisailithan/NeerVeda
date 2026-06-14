#!/usr/bin/env python3
"""
NeerVeda - Smart Agriculture Dashboard
Run this file to start the application
"""

from app import app

if __name__ == '__main__':
    print("Starting NeerVeda Dashboard...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)