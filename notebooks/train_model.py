import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import sys
import os

# Add backend to path to import FeatureExtractor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.feature_extractor import FeatureExtractor

def train_model():
    dataset_url = "https://raw.githubusercontent.com/picopalette/phishing-detection-using-ml/master/datasets/urldata.csv"
    
    print(f"Downloading dataset from {dataset_url}...")
    try:
        df = pd.read_csv(dataset_url)
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        # Fallback to creating a very small synthetic dataset for demo purposes if download fails
        print("Creating synthetic dataset for demo...")
        data = {
            'url': [
                'https://www.google.com', 'https://www.facebook.com', 'https://www.microsoft.com',
                'http://secure-login-bank.com', 'http://update-your-account.xyz', 'http://paypal-security-check.info'
            ],
            'label': [0, 0, 0, 1, 1, 1]
        }
        df = pd.DataFrame(data)

    print(f"Dataset loaded. Shape: {df.shape}")
    
    # Handle different column names if necessary
    # Assuming columns are 'Domain' or 'url' and 'Label' or 'label'
    url_col = 'Domain' if 'Domain' in df.columns else 'url'
    label_col = 'Label' if 'Label' in df.columns else 'label'
    
    # Preprocessing
    df = df.dropna()
    
    extractor = FeatureExtractor()
    
    print("Extracting features (this may take a while)...")
    # Limiting to 5000 rows for speed in this environment
    df = df.head(5000)
    
    feature_list = []
    labels = []
    
    for index, row in df.iterrows():
        feat = extractor.extract_features(row[url_col])
        if feat:
            feature_list.append(list(feat.values()))
            labels.append(row[label_col])
            
    X = np.array(feature_list)
    y = np.array(labels)
    
    print(f"Features extracted. X shape: {X.shape}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), '../models/phishing_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save feature names for reference in API
    feature_names = list(extractor.extract_features("https://example.com").keys())
    joblib.dump(feature_names, os.path.join(os.path.dirname(__file__), '../models/feature_names.joblib'))

if __name__ == "__main__":
    train_model()
