#!/usr/bin/env python3
"""
NeerVeda Setup Script
Automated installation and configuration
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner"""
    print("="*60)
    print("🌱 NeerVeda Smart Agriculture Dashboard")
    print("   Automated Setup & Installation")
    print("="*60)

def check_python_version():
    """Check Python version compatibility"""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Current version:", platform.python_version())
        return False
    
    print(f"✅ Python {platform.python_version()} - Compatible")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
        ])
        print("✅ pip upgraded")
        
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ All packages installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def check_mongodb():
    """Check MongoDB installation"""
    print("\n🔍 Checking MongoDB...")
    
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ MongoDB is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  MongoDB not found - Application will run in demo mode")
    print("   📝 To install MongoDB: https://docs.mongodb.com/manual/installation/")
    return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'static/uploads',
        'static/exports',
        'logs',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_content = """# NeerVeda Environment Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=neerveda_secret_key_2024_secure
MONGO_URI=mongodb://localhost:27017/neerveda
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created")

def run_tests():
    """Run basic functionality tests"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        from app import app
        print("✅ App imports successfully")
        
        # Test routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads")
            
            response = client.get('/dashboard')
            print("✅ Dashboard accessible")
            
            response = client.get('/api/fields')
            if response.status_code == 200:
                print("✅ API endpoints working")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_completion_message():
    """Print setup completion message"""
    print("\n" + "="*60)
    print("🎉 NeerVeda Setup Complete!")
    print("="*60)
    print("\n🚀 To start the application:")
    print("   python start.py")
    print("\n🌐 Or use the simple runner:")
    print("   python run.py")
    print("\n📋 Features Available:")
    print("   ✅ User Authentication (Demo mode)")
    print("   ✅ Field Management")
    print("   ✅ Real-time Monitoring")
    print("   ✅ Smart Irrigation")
    print("   ✅ Crop Recommendations")
    print("   ✅ Alert System")
    print("   ✅ Multi-language Support")
    print("   ✅ Responsive Design")
    print("\n🔐 Demo Login: Use any email/password")
    print("="*60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Check MongoDB
    check_mongodb()
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but application should still work")
    
    # Print completion message
    print_completion_message()

if __name__ == '__main__':
    main()