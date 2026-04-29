import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
from app.features import extract_features

"""
🧠 PHISHING DETECTION MODEL TRAINING

📊 RECOMMENDED KAGGLE DATASET:
   "Phishing Website Detection" by Eswar Chandt
   Link: https://www.kaggle.com/datasets/eswarchandt/phishing-website-detection
   Size: ~88,000 samples
   
📝 DATASET CITATION (APA Format):
   Chandt, E. (2022). Phishing Website Detection [Dataset]. 
   Kaggle. Retrieved from https://www.kaggle.com/datasets/eswarchandt/phishing-website-detection

📦 ALTERNATIVE DATASETS:
   - URL Phishing Detection (11,000 samples)
   - Phishing Domain Detection (6,000+ samples)
   - Search Kaggle for more recent datasets

⚙️  USAGE:
   python train_model.py                              # Uses data/phishing_dataset.csv
   python train_model.py "path/to/your/dataset.csv"  # Uses custom path
"""

def load_kaggle_dataset(dataset_path='data/phishing_dataset.csv'):
    """
    Load training data from Kaggle dataset CSV file
    
    📥 SETUP INSTRUCTIONS:
    1. Download a phishing dataset from Kaggle:
       - Visit: https://www.kaggle.com/datasets
       - Search for: "phishing URLs" or "phishing websites"
       - Popular options:
         * "Phishing Website Detection" dataset
         * "URL Phishing Detection Dataset"
    
    2. Place your CSV file in: brain-api/data/
       Expected columns in CSV:
       - 'url' (or 'URL'): The URL to classify
       - 'label' (or 'class'): 0 for legitimate, 1 for phishing
    
    3. Update the dataset_path parameter if your file has a different name
    
    Args:
        dataset_path (str): Path to the CSV file
        
    Returns:
        tuple: (urls, labels)
    """
    
    # ⚠️  TODO: Update this path with your Kaggle dataset file
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(
            f"❌ Dataset not found at: {dataset_path}\n"
            f"📁 Please place your Kaggle CSV file there first.\n"
            f"ℹ️  See function docstring for setup instructions."
        )
    
    print(f"📂 Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Normalize column names (handle different naming conventions)
    df.columns = df.columns.str.lower().str.strip()
    
    # Find URL column
    url_col = None
    for col in ['url', 'link', 'website']:
        if col in df.columns:
            url_col = col
            break
    
    if url_col is None:
        raise ValueError(f"❌ No URL column found. Available columns: {df.columns.tolist()}")
    
    # Find label column
    label_col = None
    for col in ['label', 'class', 'classification', 'type', 'phishing']:
        if col in df.columns:
            label_col = col
            break
    
    if label_col is None:
        raise ValueError(f"❌ No label column found. Available columns: {df.columns.tolist()}")
    
    urls = df[url_col].tolist()
    labels = df[label_col].tolist()
    
    # Ensure labels are 0 or 1
    labels = [int(1 if x == 1 else 0) for x in labels]
    
    return urls, labels

def train_model(dataset_path='data/phishing_dataset.csv'):
    """
    Train and save the phishing detection model using Kaggle dataset
    
    Args:
        dataset_path (str): Path to the CSV file containing phishing URLs dataset
    """
    
    print("🚀 Starting ML model training with real Kaggle dataset...")
    
    # Load real dataset from Kaggle
    urls, labels = load_kaggle_dataset(dataset_path)
    print(f"📊 Loaded {len(urls)} training samples from Kaggle dataset")
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
    import sys
    
    # Check if dataset path is provided as command line argument
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
        print(f"📌 Using dataset path from argument: {dataset_path}")
        train_model(dataset_path)
    else:
        print("📌 Using default dataset path: data/phishing_dataset.csv")
        train_model()

