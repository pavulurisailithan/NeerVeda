# 🚀 NeerVeda Installation Guide

## Quick Installation (Choose One)

### Windows Users
```cmd
# Double-click start.bat
# OR run in command prompt:
start.bat
```

### Linux/Mac Users
```bash
# Make executable and run:
chmod +x start.sh
./start.sh
```

### Python Direct
```bash
# Install and run:
pip install -r requirements.txt
python start.py
```

## Manual Installation

### Step 1: Prerequisites
- Python 3.7+ installed
- Internet connection

### Step 2: Install Dependencies
```bash
pip install Flask==2.3.3
pip install pymongo==4.6.0
pip install flask-pymongo==2.3.0
pip install Werkzeug==2.3.7
pip install requests==2.31.0
pip install flask-cors==4.0.0
```

### Step 3: Run Application
```bash
python run.py
```

### Step 4: Access Application
Open browser: http://localhost:5000

## Features Available

✅ **All features work without MongoDB**
✅ **Demo login: any email/password**
✅ **Full UI functionality**
✅ **Real-time monitoring simulation**
✅ **Interactive maps**
✅ **Multi-language support**

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Python Not Found
- Install Python from https://python.org
- Add Python to PATH during installation

### Module Not Found
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Success Indicators

When running correctly, you should see:
```
🌱 NeerVeda Smart Agriculture Dashboard
✅ MongoDB connected successfully!
   OR
⚠️ Running in DEMO MODE - All features available
🚀 Starting Flask server...
* Running on http://0.0.0.0:5000
```