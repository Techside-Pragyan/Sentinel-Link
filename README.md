# 🛡️ Sentinel Link: AI-Powered Phishing Detection

Sentinel Link is a production-ready, full-stack cybersecurity tool designed to identify malicious URLs using advanced machine learning and rule-based feature engineering.

## 🚀 Features
- **Real-time URL Scanning**: Instant analysis of any URL.
- **Machine Learning Engine**: Trained using Random Forest with custom feature engineering.
- **Explainable AI**: Breaks down *why* a link is flagged (URL length, IP address, HTTPS presence, etc.).
- **Premium UI**: Modern dark-mode dashboard with Glassmorphism and smooth animations.
- **Scan History**: Keeps track of your recently scanned links locally.
- **RESTful API**: Fast and scalable backend powered by FastAPI.

## 🛠️ Tech Stack
- **Frontend**: React.js, Vite, Lucide Icons, Vanilla CSS (Premium Design).
- **Backend**: FastAPI (Python), Uvicorn.
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib.
- **Feature Engineering**: Custom extractor (Tldextract, Regex).

## 📊 Feature Extraction Logic
The system extracts 13+ features from each URL, including:
- **Structural**: URL length, Domain length, Subdomain count.
- **Security**: Presence of HTTPS, IP address usage.
- **Patterns**: Number of dots, hyphens, slashes, and sensitive keywords (login, bank, etc.).
- **Redirection**: Detection of double slashes or URL shorteners.

## 📁 Project Structure
```text
Sentinel-Link/
├── backend/            # FastAPI source code
│   ├── utils/          # Feature extraction logic
│   └── main.py         # API endpoints
├── frontend/           # React + Vite source code
├── models/             # Saved ML models (.joblib)
├── notebooks/          # Training scripts
├── tests/              # Unit tests
└── data/               # Dataset storage
```

## ⚙️ How to Run

### 1. Setup Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. (Optional) Re-train Model
```bash
python notebooks/train_model.py
```

## 🧪 Testing
Run unit tests with:
```bash
pytest tests/test_features.py
```

## 🎯 Goal
To provide an easy-to-use yet powerful tool that helps users identify phishing threats before they become victims. Sentinel Link can be extended into a browser extension or a mailing server filter.