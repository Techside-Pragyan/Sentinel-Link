from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import sys
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.feature_extractor import FeatureExtractor

app = FastAPI(title="Sentinel-Link API", description="Phishing Link Detection System API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and feature extractor
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/phishing_model.joblib")
FEATURE_NAMES_PATH = os.path.join(os.path.dirname(__file__), "../models/feature_names.joblib")

model = None
feature_names = None
extractor = FeatureExtractor()

@app.on_event("startup")
def load_resources():
    global model, feature_names
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print("Model not found. Please run the training script.")
        
    if os.path.exists(FEATURE_NAMES_PATH):
        feature_names = joblib.load(FEATURE_NAMES_PATH)

class URLRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    url: str
    prediction: str
    confidence: float
    features: dict

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: URLRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Try again later.")
    
    url = request.url
    features_dict = extractor.extract_features(url)
    
    if features_dict is None:
        raise HTTPException(status_code=400, detail="Invalid URL format.")
    
    # Convert features to list in correct order
    features_values = [features_dict[name] for name in feature_names]
    
    # Prediction
    prediction_idx = model.predict([features_values])[0]
    probabilities = model.predict_proba([features_values])[0]
    
    prediction_label = "phishing" if prediction_idx == 1 else "legitimate"
    confidence = float(probabilities[prediction_idx])
    
    return {
        "url": url,
        "prediction": prediction_label,
        "confidence": confidence,
        "features": features_dict
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
