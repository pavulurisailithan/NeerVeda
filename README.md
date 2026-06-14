# 🌱 NeerVeda - Smart Agriculture Dashboard

**A comprehensive Flask-based web application for modern agricultural field management with real-time monitoring, AI-powered insights, and smart irrigation control.**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Optional-orange.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Start (3 Steps)

### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone and navigate
git clone <repository-url>
cd NeerVeda

# 2. Run automated setup
python setup.py

# 3. Start the application
python start.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start application
python run.py

# 3. Open browser
# http://localhost:5000
```

## ✨ Key Features

### 🏡 **Field Management**
- Add, view, and monitor agricultural fields with GPS locations
- Interactive maps with real-time field status
- Comprehensive field analytics and statistics
- Export field data to CSV

### 📊 **Real-time Monitoring**
- Soil moisture, temperature, and rainfall tracking
- Live sensor data visualization
- Historical data analysis and trends
- Automated data collection

### 🤖 **AI-Powered Insights**
- Intelligent crop recommendations based on soil conditions
- Weather-based farming suggestions
- Seasonal crop planning assistance
- Yield optimization recommendations

### 💧 **Smart Irrigation**
- Automated irrigation scheduling
- Water usage optimization
- Weather integration for smart watering
- Remote irrigation control

### 🚨 **Alert System**
- Critical condition notifications
- Customizable alert thresholds
- Email and SMS notifications
- Real-time monitoring alerts

### 🌐 **Multi-language Support**
- English and Telugu (తెలుగు) interface
- Complete UI translation
- Cultural adaptation for Indian farmers

### 👤 **User Management**
- Secure authentication system
- Personal user profiles
- Role-based access control
- Session management

## 📱 Application Pages

| Page | URL | Description |
|------|-----|-------------|
| 🏠 Home | `/` | Landing page with language switching |
| 🔐 Login | `/login` | User authentication (demo: any credentials) |
| 📝 Signup | `/signup` | User registration |
| 📊 Dashboard | `/dashboard` | Main monitoring dashboard |
| 🌾 Fields | `/fields` | Field management with live GPS |
| ➕ Add Field | `/add-field` | Add new fields with GPS coordinates |
| 🚨 Alerts | `/alerts` | System alerts and notifications |
| 🌱 Crop Recommendations | `/crop-recommendations` | AI crop suggestions |
| 📅 Crop Seasons | `/crop-seasons` | Seasonal farming calendar |
| 💧 Irrigation | `/irrigation` | Smart irrigation control |
| 👤 Profile | `/profile` | User profile management |
| 📊 Add Data | `/add-data` | Manual data entry |

## 🔌 API Endpoints

### Field Management
- `GET /api/fields` - Get all fields with locations
- `POST /api/add-field` - Add new field
- `GET /api/user-profile` - Get user profile data

### Monitoring & Alerts
- `GET /api/alerts` - Get alert notifications
- `POST /api/add-alert` - Create new alert
- `GET /api/sensor-data` - Get sensor readings
- `POST /api/add-sensor-data` - Add sensor data

### Weather & Recommendations
- `GET /api/weather` - Get weather data
- `GET /api/weather-forecast` - Get weather forecast
- `GET /api/village-data/<village>` - Get village-specific data
- `GET /api/crop-calendar` - Get crop calendar
- `GET /api/irrigation-schedule` - Get irrigation schedule

## 🛠️ Technology Stack

### Backend
- **Flask 2.3+** - Web framework
- **Python 3.7+** - Programming language
- **MongoDB** - Database (optional)
- **PyMongo** - MongoDB driver
- **Werkzeug** - Security utilities

### Frontend
- **HTML5** - Markup
- **Tailwind CSS** - Styling framework
- **JavaScript ES6+** - Client-side logic
- **Feather Icons** - Icon library
- **Leaflet.js** - Interactive maps

### Features
- **Responsive Design** - Mobile-first approach
- **PWA Ready** - Progressive web app capabilities
- **Multi-language** - i18n support
- **Real-time Updates** - Live data synchronization

## 🎯 Demo Mode Features

**NeerVeda works perfectly without any database setup!**

When MongoDB is unavailable, the application automatically switches to demo mode:

✅ **Full Functionality**
- All pages accessible without database
- Complete user interface and interactions
- Sample field data with GPS locations
- Login with any email/password combination
- Add fields (logged but not permanently saved)
- Real-time data simulation
- Interactive maps with sample data
- Language switching works perfectly
- All API endpoints functional

✅ **Perfect for Testing**
- No setup required
- Instant deployment
- Full feature demonstration
- Safe for development

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://localhost:27017/neerveda
```

### MongoDB Setup (Optional)
```bash
# Install MongoDB Community Edition
# https://docs.mongodb.com/manual/installation/

# Start MongoDB service
mongod

# The application will automatically detect and use MongoDB
```

## 🚀 Deployment

### Local Development
```bash
python start.py
# Access: http://localhost:5000
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t neerveda .
docker run -p 5000:5000 neerveda
```

## 📊 System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **RAM**: 512 MB
- **Storage**: 100 MB
- **Network**: Internet connection for maps and weather

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 2 GB
- **Storage**: 1 GB
- **Database**: MongoDB 4.4+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Farmers** - For inspiring this project
- **Open Source Community** - For amazing tools and libraries
- **Contributors** - For making this project better

## 📞 Support

- **Documentation**: [Wiki](../../wiki)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)

---

**Made with ❤️ for sustainable agriculture and smart farming**