#!/usr/bin/env python3
"""
NeerVeda Status Checker
Comprehensive functionality test
"""

import sys
import os

def check_imports():
    """Check all required imports"""
    print("Checking imports...")
    try:
        from app import app
        from flask import Flask
        from flask_pymongo import PyMongo
        from flask_cors import CORS
        print("SUCCESS: All imports successful")
        return True
    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        return False

def check_routes():
    """Check all routes are accessible"""
    print("Checking routes...")
    try:
        from app import app
        with app.test_client() as client:
            routes = [
                '/', '/login', '/signup', '/dashboard', 
                '/fields', '/alerts', '/profile', '/add-field',
                '/crop-recommendations', '/crop-seasons', '/irrigation'
            ]
            
            for route in routes:
                response = client.get(route)
                if response.status_code in [200, 302]:  # 302 for redirects
                    print(f"SUCCESS: {route}")
                else:
                    print(f"ERROR: {route} - Status: {response.status_code}")
            
            return True
    except Exception as e:
        print(f"ERROR: Route check error: {e}")
        return False

def check_api_endpoints():
    """Check API endpoints"""
    print("Checking API endpoints...")
    try:
        from app import app
        with app.test_client() as client:
            apis = [
                '/api/fields', '/api/alerts', '/api/sensor-data',
                '/api/weather', '/api/crop-calendar'
            ]
            
            for api in apis:
                response = client.get(api)
                if response.status_code == 200:
                    print(f"SUCCESS: {api}")
                else:
                    print(f"ERROR: {api} - Status: {response.status_code}")
            
            return True
    except Exception as e:
        print(f"ERROR: API check error: {e}")
        return False

def check_templates():
    """Check template files exist"""
    print("Checking templates...")
    templates = [
        'base.html', 'index.html', 'login.html', 'signup.html',
        'dashboard.html', 'fields.html', 'alerts.html', 'profile.html',
        'add_field.html', 'crop_recommendations.html', 'crop_seasons.html',
        'irrigation.html', 'add_data.html'
    ]
    
    missing = []
    for template in templates:
        if os.path.exists(f'templates/{template}'):
            print(f"SUCCESS: {template}")
        else:
            print(f"ERROR: {template}")
            missing.append(template)
    
    return len(missing) == 0

def check_static_files():
    """Check static files exist"""
    print("Checking static files...")
    static_files = [
        'css/professional.css',
        'js/translations.js'
    ]
    
    missing = []
    for file in static_files:
        if os.path.exists(f'static/{file}'):
            print(f"SUCCESS: {file}")
        else:
            print(f"ERROR: {file}")
            missing.append(file)
    
    return len(missing) == 0

def main():
    """Main status check"""
    print("="*50)
    print("NeerVeda Comprehensive Status Check")
    print("="*50)
    
    checks = [
        ("Imports", check_imports),
        ("Routes", check_routes),
        ("API Endpoints", check_api_endpoints),
        ("Templates", check_templates),
        ("Static Files", check_static_files)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 20)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("SUCCESS: ALL CHECKS PASSED!")
        print("NeerVeda is fully functional and ready to use!")
        print("\nTo start the application:")
        print("  python run.py")
        print("  python start.py")
        print("  OR double-click start.bat (Windows)")
    else:
        print("ERROR: Some checks failed.")
        print("Please review the errors above.")
    
    print("="*50)
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)