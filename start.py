#!/usr/bin/env python3
"""
NeerVeda - Smart Agriculture Dashboard
Complete startup script with full functionality
"""

import os
import sys
import subprocess
import time
from app import app, init_sample_data

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'pymongo', 'flask_pymongo', 
        'werkzeug', 'requests', 'flask_cors'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                *missing_packages
            ])
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def check_mongodb():
    """Check MongoDB connection"""
    print("\n🔍 Checking MongoDB connection...")
    
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"⚠️  MongoDB not available: {e}")
        print("📝 Application will run in DEMO MODE with full functionality")
        return False

def initialize_app():
    """Initialize the application with sample data"""
    print("\n🚀 Initializing NeerVeda application...")
    
    with app.app_context():
        try:
            init_sample_data()
            print("✅ Sample data initialized")
        except Exception as e:
            print(f"⚠️  Sample data initialization: {e}")
    
    print("✅ Application initialized successfully!")

def print_startup_info():
    """Print startup information"""
    print("\n" + "="*60)
    print("🌱 NeerVeda - Smart Agriculture Dashboard")
    print("="*60)
    print("🌐 Server: http://localhost:5000")
    print("📱 Mobile: http://0.0.0.0:5000")
    print("\n📋 Available Pages:")
    print("   • Home: http://localhost:5000/")
    print("   • Dashboard: http://localhost:5000/dashboard")
    print("   • Fields: http://localhost:5000/fields")
    print("   • Alerts: http://localhost:5000/alerts")
    print("   • Profile: http://localhost:5000/profile")
    print("   • Login: http://localhost:5000/login")
    print("\n🔐 Demo Login: Any email/password works!")
    print("="*60)

def main():
    """Main startup function"""
    print("🌱 Starting NeerVeda Smart Agriculture Dashboard...")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Exiting...")
        sys.exit(1)
    
    # Check MongoDB
    mongodb_available = check_mongodb()
    
    # Initialize app
    initialize_app()
    
    # Print startup info
    print_startup_info()
    
    # Start the application
    try:
        print("\n🚀 Starting Flask server...")
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=5000,
            use_reloader=False  # Prevent double startup messages
        )
    except KeyboardInterrupt:
        print("\n\n👋 NeerVeda server stopped. Thank you for using our platform!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()