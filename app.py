from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_cors import CORS
import random
import datetime
import json
import os
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'neerveda_secret_key_2024_secure'
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# In-memory storage for demo mode
demo_fields = [
    {'name': 'North Field', 'crop': 'Wheat', 'area': 5.2, 'moisture': 58, 'status': 'Monitor', 'latitude': 16.4333, 'longitude': 80.8500, 'lat': 16.4333, 'lng': 80.8500},
    {'name': 'South Field', 'crop': 'Corn', 'area': 8.7, 'moisture': 72, 'status': 'Optimal', 'latitude': 16.4300, 'longitude': 80.8550, 'lat': 16.4300, 'lng': 80.8550},
    {'name': 'East Field', 'crop': 'Soybeans', 'area': 6.5, 'moisture': 45, 'status': 'Dry', 'latitude': 16.4380, 'longitude': 80.8600, 'lat': 16.4380, 'lng': 80.8600}
]

demo_alerts = [
    {'field': 'East Field', 'message': 'Low moisture detected', 'status': 'Critical', 'time': '2 hours ago'},
    {'field': 'North Field', 'message': 'Moderate moisture level', 'status': 'Warning', 'time': '15 minutes ago'}
]

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/neerveda"
try:
    mongo = PyMongo(app)
    # Test connection
    mongo.db.command('ping')
    print("MongoDB connected successfully!")
    DATABASE_AVAILABLE = True
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Running in DEMO MODE - All features available without database")
    mongo = None
    DATABASE_AVAILABLE = False

# Global error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': 'Please try again later'}), 500

# Initialize sample data in MongoDB if collections are empty
def init_sample_data():
    if not mongo:
        return
    try:
        if mongo.db.fields.count_documents({}) == 0:
            fields = [
                {'name': 'North Field', 'crop': 'Wheat', 'area': 5.2, 'moisture': 58, 'status': 'Monitor', 'latitude': 16.4333, 'longitude': 80.8500, 'lat': 16.4333, 'lng': 80.8500},
                {'name': 'South Field', 'crop': 'Corn', 'area': 8.7, 'moisture': 72, 'status': 'Optimal', 'latitude': 16.4300, 'longitude': 80.8550, 'lat': 16.4300, 'lng': 80.8550},
                {'name': 'East Field', 'crop': 'Soybeans', 'area': 6.5, 'moisture': 45, 'status': 'Dry', 'latitude': 16.4380, 'longitude': 80.8600, 'lat': 16.4380, 'lng': 80.8600},
                {'name': 'West Field', 'crop': 'Cotton', 'area': 7.1, 'moisture': 65, 'status': 'Optimal', 'latitude': 16.4350, 'longitude': 80.8450, 'lat': 16.4350, 'lng': 80.8450}
            ]
            mongo.db.fields.insert_many(fields)
        
        if mongo.db.alerts.count_documents({}) == 0:
            alerts = [
                {'field': 'East Field', 'message': 'Low moisture detected', 'status': 'Critical', 'time': '2 hours ago'},
                {'field': 'North Field', 'message': 'Moderate moisture level', 'status': 'Warning', 'time': '15 minutes ago'}
            ]
            mongo.db.alerts.insert_many(alerts)
    except Exception as e:
        print(f"Error initializing sample data: {e}")

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/fields')
def fields():
    return render_template('fields.html')

@app.route('/add-data')
def add_data():
    return render_template('add_data.html')

@app.route('/crop-recommendations')
def crop_recommendations():
    return render_template('crop_recommendations.html')

@app.route('/crop-seasons')
def crop_seasons():
    return render_template('crop_seasons.html')

@app.route('/add-field')
def add_field():
    return render_template('add_field.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not mongo:
            # Demo mode - accept any credentials
            session['user'] = email
            flash('Logged in successfully (Demo mode)')
            return redirect(url_for('dashboard'))
        
        try:
            user = mongo.db.users.find_one({'email': email})
            if user and check_password_hash(user['password'], password):
                session['user'] = email
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Login error: {e}")
        
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if not mongo:
            # Demo mode - always succeed
            flash('Account created successfully (Demo mode)')
            return redirect(url_for('login'))
        
        try:
            if mongo.db.users.find_one({'email': email}):
                flash('Email already exists')
            else:
                hashed_password = generate_password_hash(password)
                mongo.db.users.insert_one({
                    'name': name,
                    'email': email,
                    'password': hashed_password
                })
                flash('Account created successfully')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Signup error: {e}")
            flash('Error creating account')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/add-field', methods=['POST'])
def api_add_field():
    data = request.get_json()
    # Add both lat/lng and latitude/longitude for compatibility
    if 'latitude' in data and 'longitude' in data:
        data['lat'] = data['latitude']
        data['lng'] = data['longitude']
    
    # Add user info if logged in
    if 'user' in session:
        data['user'] = session['user']
    
    if not mongo:
        # Add to in-memory storage for demo mode
        demo_fields.append(data)
        print(f"Field added to demo storage: {data['name']}")
        return jsonify({'status': 'success', 'message': 'Field added successfully (Demo mode)'})
    
    try:
        mongo.db.fields.insert_one(data)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error adding field: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/add-alert', methods=['POST'])
def add_alert():
    data = request.get_json()
    if not mongo:
        demo_alerts.append(data)
        print(f"Alert added to demo storage: {data['message']}")
        return jsonify({'status': 'success', 'message': 'Alert added successfully (Demo mode)'})
    
    try:
        mongo.db.alerts.insert_one(data)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error adding alert: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/add-sensor-data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    if not mongo:
        print(f"Sensor data would be added: {data}")
        return jsonify({'status': 'success', 'message': 'Sensor data added successfully (Demo mode)'})
    
    try:
        mongo.db.sensor_data.insert_one(data)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error adding sensor data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if mongo:
        try:
            mongo.db.contacts.insert_one(data)
        except Exception as e:
            print(f"Error saving contact: {e}")
    return jsonify({'status': 'success', 'message': 'Contact message received'})

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    if mongo:
        try:
            mongo.db.feedback.insert_one(data)
        except Exception as e:
            print(f"Error saving feedback: {e}")
    return jsonify({'status': 'success', 'message': 'Feedback received'})

@app.route('/api/fields')
def api_fields():
    if not mongo:
        # Return in-memory demo fields
        return jsonify(demo_fields)
    
    try:
        fields = list(mongo.db.fields.find({}, {'_id': 0}))
        if not fields:
            # Return demo fields if database is empty
            return jsonify(demo_fields)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify(demo_fields)
    
    # Simulate real-time data with slight variations
    for field in fields:
        field['moisture'] = max(20, min(80, field['moisture'] + random.randint(-3, 3)))
        if field['moisture'] < 30:
            field['status'] = 'Dry'
        elif field['moisture'] < 45:
            field['status'] = 'Monitor'
        elif field['moisture'] > 70:
            field['status'] = 'Wet'
        else:
            field['status'] = 'Optimal'
        
        # Ensure lat/lng properties exist for frontend compatibility
        if 'latitude' in field and 'longitude' in field:
            field['lat'] = field['latitude']
            field['lng'] = field['longitude']
        
        # Update in database
        if mongo:
            mongo.db.fields.update_one({'name': field['name']}, {'$set': {'moisture': field['moisture'], 'status': field['status']}})
    
    return jsonify(fields)

@app.route('/api/alerts')
def api_alerts():
    if not mongo:
        return jsonify(demo_alerts)
    
    try:
        alerts = list(mongo.db.alerts.find({}, {'_id': 0}))
        return jsonify(alerts)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify(demo_alerts)

@app.route('/api/sensor-data')
def api_sensor_data():
    # Try to get real sensor data from database first
    if mongo:
        try:
            stored_data = list(mongo.db.sensor_data.find({}, {'_id': 0}).sort('date', -1).limit(7))
            if stored_data:
                return jsonify(stored_data)
        except Exception as e:
            print(f"Error fetching sensor data: {e}")
    
    # Generate mock sensor data if no real data exists
    data = []
    for i in range(7):
        data.append({
            'date': (datetime.datetime.now() - datetime.timedelta(days=6-i)).strftime('%Y-%m-%d'),
            'moisture': random.randint(40, 75),
            'temperature': random.randint(25, 35),
            'rainfall': random.randint(0, 15)
        })
    return jsonify(data)

@app.route('/api/village-data/<village>')
def api_village_data(village):
    # Enhanced village data with more details
    village_data = {
        'Vijayawada': {
            'moisture': random.randint(60, 70), 'soilType': 'Alluvial', 'rainfall': '850mm', 
            'crops': ['Rice', 'Cotton', 'Wheat', 'Maize'], 'temperature': random.randint(28, 35),
            'ph': 6.8, 'nitrogen': 'Medium', 'phosphorus': 'High', 'potassium': 'Medium'
        },
        'Machilipatnam': {
            'moisture': random.randint(68, 76), 'soilType': 'Coastal', 'rainfall': '920mm', 
            'crops': ['Rice', 'Coconut', 'Sugarcane'], 'temperature': random.randint(26, 32),
            'ph': 7.2, 'nitrogen': 'High', 'phosphorus': 'Medium', 'potassium': 'High'
        },
        'Gudivada': {
            'moisture': random.randint(54, 62), 'soilType': 'Clay', 'rainfall': '780mm', 
            'crops': ['Cotton', 'Chili', 'Turmeric'], 'temperature': random.randint(29, 36),
            'ph': 6.5, 'nitrogen': 'Low', 'phosphorus': 'Medium', 'potassium': 'High'
        },
        'Jaggayyapeta': {
            'moisture': random.randint(57, 65), 'soilType': 'Red Soil', 'rainfall': '720mm', 
            'crops': ['Groundnut', 'Cotton', 'Maize'], 'temperature': random.randint(30, 37),
            'ph': 6.3, 'nitrogen': 'Medium', 'phosphorus': 'Low', 'potassium': 'Medium'
        },
        'Nuzvidu': {
            'moisture': random.randint(65, 73), 'soilType': 'Black Soil', 'rainfall': '800mm', 
            'crops': ['Cotton', 'Sunflower', 'Maize'], 'temperature': random.randint(28, 34),
            'ph': 7.0, 'nitrogen': 'High', 'phosphorus': 'High', 'potassium': 'Medium'
        },
        'Nandigama': {
            'moisture': random.randint(59, 67), 'soilType': 'Alluvial', 'rainfall': '760mm', 
            'crops': ['Rice', 'Sugarcane', 'Banana'], 'temperature': random.randint(27, 33),
            'ph': 6.9, 'nitrogen': 'Medium', 'phosphorus': 'High', 'potassium': 'High'
        },
        'Mylavaram': {
            'moisture': random.randint(62, 70), 'soilType': 'Red Soil', 'rainfall': '740mm', 
            'crops': ['Mango', 'Coconut', 'Cashew'], 'temperature': random.randint(26, 31),
            'ph': 6.4, 'nitrogen': 'Low', 'phosphorus': 'Medium', 'potassium': 'High'
        },
        'Tiruvuru': {
            'moisture': random.randint(55, 63), 'soilType': 'Sandy', 'rainfall': '680mm', 
            'crops': ['Groundnut', 'Sesame', 'Cotton'], 'temperature': random.randint(31, 38),
            'ph': 6.1, 'nitrogen': 'Low', 'phosphorus': 'Low', 'potassium': 'Medium'
        },
        'Kaikalur': {
            'moisture': random.randint(67, 75), 'soilType': 'Alluvial', 'rainfall': '890mm', 
            'crops': ['Rice', 'Aquaculture', 'Coconut'], 'temperature': random.randint(25, 30),
            'ph': 7.1, 'nitrogen': 'High', 'phosphorus': 'Medium', 'potassium': 'High'
        },
        'Bantumilli': {
            'moisture': random.randint(60, 68), 'soilType': 'Clay', 'rainfall': '770mm', 
            'crops': ['Rice', 'Vegetables', 'Flowers'], 'temperature': random.randint(27, 33),
            'ph': 6.7, 'nitrogen': 'Medium', 'phosphorus': 'High', 'potassium': 'Medium'
        }
    }
    return jsonify(village_data.get(village, {
        'moisture': random.randint(55, 65), 'soilType': 'Mixed', 'rainfall': '750mm', 
        'crops': ['Rice', 'Cotton'], 'temperature': random.randint(28, 34),
        'ph': 6.5, 'nitrogen': 'Medium', 'phosphorus': 'Medium', 'potassium': 'Medium'
    }))

@app.route('/api/crop-calendar')
def api_crop_calendar():
    # Crop calendar with planting and harvesting dates
    calendar = {
        'Kharif': {
            'season': 'June - October',
            'crops': {
                'Rice': {'plant': 'June-July', 'harvest': 'October-November', 'duration': '120-150 days'},
                'Cotton': {'plant': 'May-June', 'harvest': 'October-January', 'duration': '180-200 days'},
                'Maize': {'plant': 'June-July', 'harvest': 'September-October', 'duration': '90-120 days'},
                'Sugarcane': {'plant': 'February-April', 'harvest': 'December-March', 'duration': '10-18 months'}
            }
        },
        'Rabi': {
            'season': 'October - March',
            'crops': {
                'Wheat': {'plant': 'November-December', 'harvest': 'March-April', 'duration': '120-150 days'},
                'Barley': {'plant': 'October-November', 'harvest': 'March-April', 'duration': '120-140 days'},
                'Mustard': {'plant': 'October-November', 'harvest': 'February-March', 'duration': '120-150 days'},
                'Peas': {'plant': 'October-November', 'harvest': 'February-March', 'duration': '90-110 days'}
            }
        },
        'Zaid': {
            'season': 'March - June',
            'crops': {
                'Watermelon': {'plant': 'February-March', 'harvest': 'May-June', 'duration': '90-100 days'},
                'Cucumber': {'plant': 'February-March', 'harvest': 'April-May', 'duration': '50-70 days'},
                'Fodder': {'plant': 'March-April', 'harvest': 'May-June', 'duration': '60-90 days'},
                'Vegetables': {'plant': 'February-April', 'harvest': 'April-June', 'duration': '60-120 days'}
            }
        }
    }
    return jsonify(calendar)

@app.route('/api/weather-forecast')
def api_weather_forecast():
    # Mock 7-day weather forecast
    forecast = []
    for i in range(7):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'temperature': {'min': random.randint(22, 28), 'max': random.randint(30, 38)},
            'humidity': random.randint(60, 85),
            'rainfall': random.randint(0, 25),
            'wind_speed': random.randint(5, 20),
            'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Thunderstorm'])
        })
    return jsonify(forecast)

@app.route('/api/irrigation-schedule')
def api_irrigation_schedule():
    # Smart irrigation recommendations
    schedule = []
    for i in range(7):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        moisture_level = random.randint(40, 80)
        rainfall_forecast = random.randint(0, 15)
        
        if moisture_level < 40 and rainfall_forecast < 5:
            recommendation = 'High Priority - Irrigate immediately'
            priority = 'High'
        elif moisture_level < 60 and rainfall_forecast < 10:
            recommendation = 'Medium Priority - Irrigate if no rain'
            priority = 'Medium'
        else:
            recommendation = 'Low Priority - Monitor conditions'
            priority = 'Low'
            
        schedule.append({
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'moisture_level': moisture_level,
            'rainfall_forecast': rainfall_forecast,
            'recommendation': recommendation,
            'priority': priority
        })
    return jsonify(schedule)

@app.route('/api/weather')
def api_weather():
    weather_data = {
        'current': {
            'temperature': random.randint(25, 35),
            'humidity': random.randint(60, 85),
            'rainfall': random.randint(0, 10),
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy'])
        },
        'forecast': []
    }
    for i in range(5):
        date = datetime.datetime.now() + datetime.timedelta(days=i+1)
        weather_data['forecast'].append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': random.randint(22, 38),
            'rainfall': random.randint(0, 25),
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy'])
        })
    return jsonify(weather_data)

@app.route('/api/user-profile')
def api_user_profile():
    if 'user' not in session:
        # Return demo user data when not logged in
        return jsonify({
            'name': 'Demo User',
            'email': 'demo@example.com',
            'phone': '+91 98765 43210',
            'location': 'Vijayawada, Andhra Pradesh',
            'fields_count': len(demo_fields),
            'total_area': sum(field.get('area', 0) for field in demo_fields)
        })
    
    user_email = session['user']
    user_name = user_email.split('@')[0].title().replace('.', ' ')
    
    # Get user data from database if available
    user_data = {
        'name': user_name,
        'email': user_email,
        'phone': '+91 98765 43210',
        'location': 'Vijayawada, Andhra Pradesh',
        'fields_count': len(demo_fields) if not mongo else 0,
        'total_area': sum(field.get('area', 0) for field in demo_fields) if not mongo else 0
    }
    
    if mongo:
        try:
            # Get actual user data from database
            user_fields = list(mongo.db.fields.find({}))
            user_data['fields_count'] = len(user_fields)
            user_data['total_area'] = sum(field.get('area', 0) for field in user_fields)
        except Exception as e:
            print(f"Error fetching user data: {e}")
    
    return jsonify(user_data)

@app.route('/irrigation')
def irrigation():
    return render_template('irrigation.html')

if __name__ == '__main__':
    with app.app_context():
        init_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5000)