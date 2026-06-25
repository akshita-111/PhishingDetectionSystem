from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging
from contextlib import asynccontextmanager
from .features import extract_features
from .ml_model import ml_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    try:
        loaded = ml_model.load_model()
        if loaded:
            logger.info("ML model loaded on startup")
        else:
            logger.warning("ML model not loaded on startup; falling back to rules")
    except Exception as e:
        logger.error(f"Exception while loading ML model on startup: {e}")
    
    yield
    
    # Shutdown (if needed)
    logger.info("Application shutting down")


app = FastAPI(title="Phishing Detection API", version="1.0.0", lifespan=lifespan)


class URLRequest(BaseModel):
    url: str


class PredictionResponse(BaseModel):
    is_phishing: bool
    confidence: float
    explanation: str


def generate_ml_prediction(url: str) -> Dict[str, Any]:
    """
    Generate prediction using the trained ML model.
    Falls back to rule-based prediction if ML model is unavailable.
    """
    try:
        prediction = ml_model.predict(url)
        return {
            "is_phishing": prediction["is_phishing"],
            "confidence": prediction["confidence"],
            "explanation": prediction["explanation"]
        }
    except Exception as e:
        logger.error(f"ML prediction failed: {str(e)}")
        # Fallback to simple rule-based prediction
        features = extract_features(url)
        risk_score = 0.0
        
        if features.get('has_at_symbol', 0) > 0:
            risk_score += 0.3
        if features.get('has_ip_address', 0) > 0:
            risk_score += 0.4
        if features.get('url_length', 0) > 100:
            risk_score += 0.2
        
        risk_score = min(1.0, risk_score)
        
        return {
            "is_phishing": risk_score > 0.5,
            "confidence": risk_score,
            "explanation": "Fallback prediction (ML model error)"
        }


@app.post("/predict", response_model=PredictionResponse)
async def predict_phishing(request: URLRequest):
    """
    Predict whether a URL is phishing or not.
    
    Args:
        request: URLRequest containing the URL to analyze
        
    Returns:
        PredictionResponse with prediction results
    """
    try:
        logger.info(f"Received prediction request for URL: {request.url}")
        
        # Generate prediction using ML model
        prediction = generate_ml_prediction(request.url)
        
        logger.info(f"ML prediction result: {prediction}")
        
        return PredictionResponse(**prediction)
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "brain-api"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Phishing Detection API", "version": "1.0.0"}
