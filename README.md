# 🔍 Phishing Detection System

A comprehensive phishing detection system with web frontend, REST API, and browser extension for real-time protection.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Browser        │    │  Orchestrator    │    │  Brain API      │
│  Extension      │◄──►│  Service        │◄──►│  (ML Models)    │
│                 │    │  (Spring Boot)  │    │  (FastAPI)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
       │                        │                        │
       └────────────────────────┴────────────────────────┘
                          Web Frontend
```

## 🚀 Quick Start

### Prerequisites
- Java 11
- Python 3.8+
- Maven 3.6+

### 1. Clone and Setup
```bash
git clone <repository-url>
cd PhishingDetectionSystem
```

### 2. Start All Services
```bash
./start-system.sh
```

This will start:
- 🧠 Brain API (port 8000) - ML model serving
- 🌐 Orchestrator Service (port 8080) - REST API
- 🎨 Web Frontend (served by Orchestrator)

### 3. Test the System
```bash
# Test API directly
curl -X POST http://localhost:8080/api/v1/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Open web interface
open http://localhost:8080
```

## 📁 Project Structure

```
PhishingDetectionSystem/
├── brain-api/                 # Python ML API (FastAPI)
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── features.py       # Feature extraction
│   │   └── ml_model.py       # ML model loading/inference
│   ├── models/               # Trained ML models
│   └── requirements.txt      # Python dependencies
├── orchestrator-service/      # Java Spring Boot API
│   ├── src/main/java/com/phishing/orchestrator/
│   │   ├── controller/       # REST controllers
│   │   ├── service/          # Business logic
│   │   ├── dto/              # Data transfer objects
│   │   ├── model/            # Database models
│   │   └── config/           # Configuration
│   ├── src/main/resources/
│   │   └── static/index.html # Web frontend
│   └── pom.xml               # Maven configuration
├── browser-extension/         # Chrome/Firefox extension
│   ├── manifest.json         # Extension manifest
│   ├── background.js         # Service worker
│   ├── popup.html/js         # Extension popup
│   └── icons/                # Extension icons
└── start-system.sh           # Integration script
```

## 🔧 Manual Setup

### Backend Services

#### Brain API (Python)
```bash
cd brain-api
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Orchestrator Service (Java)
```bash
cd orchestrator-service
mvn clean compile
mvn spring-boot:run
```

### Browser Extension

#### Chrome
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `browser-extension` folder

#### Firefox
1. Open `about:debugging`
2. Click "This Firefox" → "Load Temporary Add-on"
3. Select `browser-extension/manifest.json`

## 🎨 Frontend Features

- **URL Input**: Clean interface for entering URLs to check
- **Real-time Analysis**: Instant feedback with confidence scores
- **Responsive Design**: Works on desktop and mobile
- **Error Handling**: Graceful error messages and loading states

## 🔌 API Endpoints

### Orchestrator Service (Port 8080)

#### POST `/api/v1/check`
Check if a URL is phishing.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "isPhishing": false,
  "confidence": 0.85,
  "explanation": "URL appears safe based on analysis"
}
```

#### GET `/api/v1/health`
Health check endpoint.

### Brain API (Port 8000)

#### POST `/predict`
Direct ML prediction (used internally).

## 🛡️ Browser Extension Features

- **Automatic Detection**: Monitors all visited websites
- **Browser Notifications**: Alerts for detected phishing sites
- **Manual Checking**: Popup interface for URL testing
- **Service Status**: Shows backend connectivity status

## 🧠 ML Model

The system uses a trained machine learning model that analyzes:
- URL structure and patterns
- Domain characteristics
- Content features
- Historical patterns

Model files are stored in `brain-api/models/`:
- `phishing_model.joblib` - Trained classifier
- `feature_scaler.joblib` - Feature normalization
- `feature_names.joblib` - Feature metadata

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :8080
# Kill the process
kill -9 <PID>
```

#### Java Compilation Errors
- Ensure Java 11 is installed: `java -version`
- Clear Maven cache: `mvn clean`

#### Python Import Errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### Extension Not Loading
- Check browser console for errors
- Ensure manifest.json is valid JSON
- Verify all required files exist

### Service Health Checks

```bash
# Brain API
curl http://localhost:8000/docs

# Orchestrator
curl http://localhost:8080/api/v1/health
```

## 🔒 Security Considerations

- The extension communicates with localhost services
- CORS is configured for development
- In production, implement proper authentication
- Use HTTPS for API communications

## 📊 Monitoring

- Service health endpoints for monitoring
- Request logging in both services
- Error handling with appropriate HTTP status codes

## 🚀 Deployment

### Production Setup
1. Configure proper CORS origins
2. Set up HTTPS certificates
3. Configure database for persistence
4. Set up monitoring and logging
5. Deploy services behind reverse proxy

### Docker Support
Future enhancement: Add Docker Compose for containerized deployment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper testing
4. Submit a pull request

## 📄 License

[Add your license information here]

---

**Built with:** Spring Boot, FastAPI, Chrome Extension API, scikit-learn