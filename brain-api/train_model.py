import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
from app.features import extract_features

def generate_sample_data():
    """Generate sample phishing and legitimate URLs for training"""
    
    # Sample legitimate URLs
    legitimate_urls = [
        "https://www.google.com",
        "https://github.com/login",
        "https://www.amazon.com",
        "https://www.facebook.com",
        "https://www.linkedin.com",
        "https://stackoverflow.com/questions",
        "https://www.youtube.com/watch",
        "https://www.twitter.com",
        "https://www.reddit.com",
        "https://www.wikipedia.org/wiki",
        "https://mail.google.com",
        "https://drive.google.com",
        "https://docs.microsoft.com",
        "https://developer.mozilla.org",
        "https://pypi.org/project"
    ]
    
    # Sample phishing URLs (these are patterns commonly found in phishing)
    phishing_urls = [
        "http://192.168.1.1/login.html",
        "http://bit.ly/3xY7zK2",
        "https://secure-account-update.tk",
        "http://paypal-security.ml/ga",
        "https://verify-your-account.cf",
        "http://admin@facebook.com/login",
        "http://amazon-update-security.tk",
        "https://bank-verification.ml",
        "http://click-here-now.ga",
        "https://urgent-action-required.cf",
        "http://secure-payment-gateway.tk",
        "https://account-suspended.ml",
        "http://verify-identity-now.ga",
        "https://limited-time-offer.cf",
        "http://click-to-claim.tk"
    ]
    
    # Create more variations by adding common phishing patterns
    more_phishing = []
    for url in phishing_urls[:5]:
        more_phishing.append(url + "?id=123&token=abc")
        more_phishing.append(url.replace("http", "https"))
        more_phishing.append(url + "/login.php")
    
    phishing_urls.extend(more_phishing)
    
    # Create labels
    urls = legitimate_urls + phishing_urls
    labels = [0] * len(legitimate_urls) + [1] * len(phishing_urls)
    
    return urls, labels

def train_model():
    """Train and save the phishing detection model"""
    
    print("🚀 Starting ML model training...")
    
    # Generate training data
    urls, labels = generate_sample_data()
    print(f"📊 Generated {len(urls)} training samples")
    print(f"   - Legitimate: {sum(1 for l in labels if l == 0)}")
    print(f"   - Phishing: {sum(1 for l in labels if l == 1)}")
    
    # Extract features for all URLs
    print("🔍 Extracting features...")
    X = []
    valid_indices = []
    
    for i, url in enumerate(urls):
        try:
            features = extract_features(url)
            # Convert to array in consistent order
            feature_array = [features[key] for key in sorted(features.keys())]
            X.append(feature_array)
            valid_indices.append(i)
        except Exception as e:
            print(f"⚠️  Error processing URL {url}: {e}")
    
    # Filter labels to match valid features
    y = [labels[i] for i in valid_indices]
    X = np.array(X)
    y = np.array(y)
    
    print(f"✅ Successfully extracted features for {len(X)} URLs")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    print("📏 Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("🧠 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    print("📈 Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"🎯 Model Accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
    
    # Feature importance
    feature_names = sorted(extract_features("http://example.com").keys())
    importances = model.feature_importances_
    
    print("\n🔝 Top 10 Most Important Features:")
    top_indices = np.argsort(importances)[-10:][::-1]
    for i, idx in enumerate(top_indices):
        print(f"   {i+1}. {feature_names[idx]}: {importances[idx]:.3f}")
    
    # Save model and scaler
    print("💾 Saving model files...")
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model, 'models/phishing_model.joblib')
    joblib.dump(scaler, 'models/feature_scaler.joblib')
    joblib.dump(feature_names, 'models/feature_names.joblib')
    
    print("✅ Model training completed!")
    print("📁 Files saved in 'models/' directory:")
    print("   - phishing_model.joblib (trained model)")
    print("   - feature_scaler.joblib (feature scaler)")
    print("   - feature_names.joblib (feature order)")
    
    return model, scaler, feature_names

if __name__ == "__main__":
    train_model()
