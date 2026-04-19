import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.feature_extractor import FeatureExtractor

def test_feature_extractor_google():
    extractor = FeatureExtractor()
    url = "https://www.google.com"
    features = extractor.extract_features(url)
    
    assert features is not None
    assert features['use_https'] == 1
    assert features['have_ip'] == 0
    assert features['count_sensitive_words'] == 0

def test_feature_extractor_phishing_patterns():
    extractor = FeatureExtractor()
    url = "http://login-verify-bank.com/secure"
    features = extractor.extract_features(url)
    
    assert features is not None
    assert features['use_https'] == 0
    assert features['count_sensitive_words'] >= 2  # login, verify, secure
    assert features['count_dir'] >= 1

def test_feature_extractor_ip():
    extractor = FeatureExtractor()
    url = "http://192.168.1.1/index.php"
    features = extractor.extract_features(url)
    
    assert features['have_ip'] == 1

if __name__ == "__main__":
    pytest.main([__file__])
