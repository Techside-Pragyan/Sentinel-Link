import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Shield, ShieldAlert, ShieldCheck, History, ExternalLink, Info, Loader2, Search } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const savedHistory = localStorage.getItem('sentinel_history');
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

  const saveToHistory = (entry) => {
    const newHistory = [entry, ...history.slice(0, 9)];
    setHistory(newHistory);
    localStorage.setItem('sentinel_history', JSON.stringify(newHistory));
  };

  const handleCheck = async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, { url });
      setResult(response.data);
      saveToHistory({
        url: response.data.url,
        prediction: response.data.prediction,
        confidence: response.data.confidence,
        timestamp: new Date().toLocaleTimeString()
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to connect to API. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem' }}>
          <Shield size={48} color="#6366f1" />
          <h1>Sentinel Link</h1>
        </div>
        <p className="subtitle">
          Advanced phishing detection system powered by machine learning. 
          Protect yourself from malicious links in real-time.
        </p>
      </header>

      <main className="glass glass-card">
        <form onSubmit={handleCheck}>
          <div className="input-group">
            <input
              type="text"
              placeholder="Paste a suspicious URL here (e.g., https://example.com)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading || !url}>
              {loading ? <Loader2 className="loader" /> : <Search size={20} />}
              {loading ? 'Analyzing...' : 'Check'}
            </button>
          </div>
        </form>

        {error && (
          <div style={{ color: '#ef4444', marginTop: '1rem', textAlign: 'center' }}>
            {error}
          </div>
        )}

        {result && (
          <div className={`result-display ${result.prediction === 'phishing' ? 'result-phishing' : 'result-safe'}`}>
            <div className="result-icon">
              {result.prediction === 'phishing' ? <ShieldAlert size={64} /> : <ShieldCheck size={64} />}
            </div>
            <div className="result-title">
              {result.prediction === 'phishing' ? 'Phishing Detected!' : 'Link Appears Safe'}
            </div>
            <p>We are {Math.round(result.confidence * 100)}% confident about this prediction.</p>
            
            <div className="confidence-meter">
              <div 
                className="confidence-bar" 
                style={{ 
                  width: `${result.confidence * 100}%`,
                  backgroundColor: result.prediction === 'phishing' ? 'var(--danger)' : 'var(--safe)'
                }}
              ></div>
            </div>

            <div className="features-grid">
              {Object.entries(result.features).slice(0, 6).map(([key, value]) => (
                <div key={key} className="feature-item">
                  <div className="feature-label">{key.replace(/_/g, ' ')}</div>
                  <div className="feature-value">{typeof value === 'number' && value > 1 ? value : (value ? 'Yes' : 'No')}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <section className="history-section">
        <h2 className="history-title">
          <History size={24} />
          Recent Scans
        </h2>
        {history.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No recent scans yet.</p>
        ) : (
          history.map((item, index) => (
            <div key={index} className="glass history-item">
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontWeight: 600, fontSize: '1.1rem', maxWidth: '400px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {item.url}
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{item.timestamp}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <span style={{ 
                  padding: '0.25rem 0.75rem', 
                  borderRadius: '99px', 
                  fontSize: '0.8rem', 
                  fontWeight: 600,
                  backgroundColor: item.prediction === 'phishing' ? 'var(--danger-glow)' : 'var(--safe-glow)',
                  color: item.prediction === 'phishing' ? 'var(--danger)' : 'var(--safe)'
                }}>
                  {item.prediction.toUpperCase()}
                </span>
                <button 
                  onClick={() => setUrl(item.url)}
                  style={{ padding: '0.5rem', background: 'transparent', color: 'var(--text-muted)' }}
                >
                  <Search size={16} />
                </button>
              </div>
            </div>
          ))
        )}
      </section>

      <footer style={{ marginTop: 'auto', padding: '2rem 0', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <p>© 2026 Sentinel Link AI. Powered by XGBoost and Deep Learning.</p>
      </footer>
    </div>
  );
}

export default App;
