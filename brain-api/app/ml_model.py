import joblib
import numpy as np
import os
import logging
from typing import Dict, Any, Optional
try:
    from app.features import extract_features
except ImportError:
    try:
        from .features import extract_features
    except ImportError:
        from features import extract_features

logger = logging.getLogger(__name__)

class PhishingMLModel:
    """Machine Learning model for phishing detection"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.scaler = None
        self.feature_names = None
        # Resolve model paths relative to this file to avoid working-directory issues
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.model_path = model_path or os.path.join(base_dir, 'models', 'phishing_model.joblib')
        self.scaler_path = os.path.join(base_dir, 'models', 'feature_scaler.joblib')
        self.feature_names_path = os.path.join(base_dir, 'models', 'feature_names.joblib')
        self.is_loaded = False
        
    def load_model(self) -> bool:
        """Load the trained ML model and related components"""
        try:
            if not os.path.exists(self.model_path):
                logger.error(f"Model file not found: {self.model_path}")
                return False

            # Load model components from resolved absolute paths
            self.model = joblib.load(self.model_path)
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
            else:
                logger.warning(f"Scaler file not found: {self.scaler_path}")

            if os.path.exists(self.feature_names_path):
                self.feature_names = joblib.load(self.feature_names_path)
            else:
                logger.warning(f"Feature names file not found: {self.feature_names_path}")
            
            self.is_loaded = True
            logger.info("✅ ML model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load ML model: {str(e)}")
            self.is_loaded = False
            return False
    
    def predict(self, url: str) -> Dict[str, Any]:
        """
        Make prediction for a given URL
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_loaded:
            if not self.load_model():
                # Fallback to dummy prediction if model loading fails
                return self._fallback_prediction(url)
        
        try:
            # Extract features
            features = extract_features(url)
            
            # Convert to array in the correct order
            feature_array = []
            for feature_name in self.feature_names:
                feature_array.append(features.get(feature_name, 0.0))
            
            feature_array = np.array(feature_array).reshape(1, -1)
            
            # Scale features
            scaled_features = self.scaler.transform(feature_array)
            
            # Make prediction
            prediction_proba = self.model.predict_proba(scaled_features)[0]
            prediction = self.model.predict(scaled_features)[0]
            
            # Calculate confidence
            confidence = max(prediction_proba)
            
            # Generate explanation based on feature importance
            explanation = self._generate_explanation(features, prediction_proba[1])
            
            return {
                "is_phishing": bool(prediction == 1),
                "confidence": float(confidence),
                "explanation": explanation,
                "phishing_probability": float(prediction_proba[1])
            }
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {str(e)}")
            return self._fallback_prediction(url)
    
    def _fallback_prediction(self, url: str) -> Dict[str, Any]:
        """Fallback prediction when ML model is unavailable"""
        logger.warning("⚠️  Using fallback prediction (ML model unavailable)")
        
        # Simple rule-based fallback
        features = extract_features(url)
        risk_score = 0.0
        
        if features.get('has_at_symbol', 0) > 0:
            risk_score += 0.3
        if features.get('has_ip_address', 0) > 0:
            risk_score += 0.4
        if features.get('url_length', 0) > 100:
            risk_score += 0.2
        if features.get('has_suspicious_tld', 0) > 0:
            risk_score += 0.3
        
        risk_score = min(1.0, risk_score)
        
        return {
            "is_phishing": risk_score > 0.5,
            "confidence": risk_score,
            "explanation": "Fallback prediction (ML model unavailable)",
            "phishing_probability": risk_score
        }
    
    def _generate_explanation(self, features: Dict[str, float], phishing_prob: float) -> str:
        """Generate human-readable explanation based on features and probability"""
        explanations = []
        
        # High probability explanations
        if phishing_prob > 0.8:
            if features.get('has_ip_address', 0) > 0:
                explanations.append("uses IP address instead of domain name")
            if features.get('has_at_symbol', 0) > 0:
                explanations.append("contains @ symbol (email-style URL)")
            if features.get('has_suspicious_tld', 0) > 0:
                explanations.append("uses suspicious top-level domain")
        
        # Medium probability explanations
        elif phishing_prob > 0.5:
            if features.get('url_length', 0) > 75:
                explanations.append("unusually long URL")
            if features.get('special_char_ratio', 0) > 0.2:
                explanations.append("high ratio of special characters")
            if features.get('dot_count', 0) > 4:
                explanations.append("excessive number of dots")
        
        # Low probability (legitimate indicators)
        else:
            if features.get('has_https', 0) > 0:
                explanations.append("uses secure HTTPS protocol")
            if features.get('domain_length', 0) < 20:
                explanations.append("reasonable domain length")
            explanations.append("matches legitimate URL patterns")
        
        if not explanations:
            explanations.append("no obvious suspicious patterns detected")
        
        return "URL " + ", ".join(explanations)

# Global model instance
ml_model = PhishingMLModel()
