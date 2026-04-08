import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, BarChart2, ArrowRight, GitCompare } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

function HistoryPage() {
  const navigate = useNavigate();
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState([]);
  const [comparison, setComparison] = useState(null);
  const [comparing, setComparing] = useState(false);

  useEffect(() => {
    axios.get(`${API_BASE}/history`)
      .then(res => {
        setRuns(res.data.runs || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const toggleSelect = (id) => {
    setSelected(prev => {
      if (prev.includes(id)) return prev.filter(x => x !== id);
      if (prev.length >= 2) return [prev[1], id];
      return [...prev, id];
    });
    setComparison(null);
  };

  const compareRuns = async () => {
    if (selected.length !== 2) return;
    setComparing(true);
    try {
      const res = await axios.get(`${API_BASE}/compare`, {
        params: { run1: selected[0], run2: selected[1] }
      });
      setComparison(res.data);
    } catch (err) {
      console.error(err);
    }
    setComparing(false);
  };

  const formatDelta = (val) => {
    if (val > 0) return <span className="delta-up">+{val} ↑</span>;
    if (val < 0) return <span className="delta-down">{val} ↓</span>;
    return <span className="delta-neutral">0 →</span>;
  };

  if (loading) {
    return (
      <div className="history-page">
        <div className="dashboard-loading">
          <div className="loading-spinner"></div>
          <p>Loading history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="page-header">
        <h1>Analysis History</h1>
        <p className="page-subtitle">View past analyses and compare results over time</p>
      </div>

      {selected.length === 2 && (
        <div className="compare-bar">
          <span>{selected.length} runs selected</span>
          <button className="btn-primary btn-sm" onClick={compareRuns} disabled={comparing}>
            <GitCompare size={16} />
            {comparing ? 'Comparing...' : 'Compare'}
          </button>
          <button className="btn-text" onClick={() => { setSelected([]); setComparison(null); }}>
            Clear
          </button>
        </div>
      )}

      {/* Comparison Result */}
      {comparison && (
        <div className="comparison-card">
          <h3>Comparison Results</h3>
          <div className="comparison-grid">
            <div className="comparison-col">
              <h4>Run #{comparison.run1.id}</h4>
              <p className="comparison-date">{new Date(comparison.run1.timestamp).toLocaleDateString('en-IN')}</p>
              <div className="comparison-stats">
                <span>Out of Stock: {comparison.run1.out_of_stock_count}</span>
                <span>Low Stock: {comparison.run1.low_stock_count}</span>
                <span>Critical: {comparison.run1.critical_count}</span>
              </div>
            </div>
            <div className="comparison-delta">
              <h4>Change</h4>
              <div className="comparison-stats">
                <span>Out of Stock: {formatDelta(comparison.delta.out_of_stock)}</span>
                <span>Low Stock: {formatDelta(comparison.delta.low_stock)}</span>
                <span>Critical: {formatDelta(comparison.delta.critical)}</span>
              </div>
            </div>
            <div className="comparison-col">
              <h4>Run #{comparison.run2.id}</h4>
              <p className="comparison-date">{new Date(comparison.run2.timestamp).toLocaleDateString('en-IN')}</p>
              <div className="comparison-stats">
                <span>Out of Stock: {comparison.run2.out_of_stock_count}</span>
                <span>Low Stock: {comparison.run2.low_stock_count}</span>
                <span>Critical: {comparison.run2.critical_count}</span>
              </div>
            </div>
          </div>

          {/* AI Narrative */}
          {comparison.narrative && (
            <div className="comparison-narrative">
              <h4>🧠 AI Analysis</h4>
              <p>{comparison.narrative}</p>
            </div>
          )}
          {comparison.narrative_error && (
            <div className="comparison-narrative narrative-fallback">
              <p>AI comparison unavailable — showing data only.</p>
            </div>
          )}
        </div>
      )}

      {/* Timeline */}
      {runs.length === 0 ? (
        <div className="dashboard-empty">
          <Clock size={48} />
          <h2>No analysis runs yet</h2>
          <p>Upload a file to get started</p>
          <button className="btn-primary" onClick={() => navigate('/')}>
            Go to Analyze
          </button>
        </div>
      ) : (
        <div className="history-timeline">
          {runs.map((run) => (
            <div
              key={run.id}
              className={`history-card ${selected.includes(run.id) ? 'selected' : ''}`}
              onClick={() => toggleSelect(run.id)}
            >
              <div className="history-card-header">
                <div className="history-date">
                  <Clock size={14} />
                  {new Date(run.timestamp).toLocaleDateString('en-IN', {
                    day: 'numeric', month: 'short', year: 'numeric',
                    hour: '2-digit', minute: '2-digit'
                  })}
                </div>
                <div className={`history-status status-${run.status}`}>
                  {run.status}
                </div>
              </div>
              <h3>{run.input_filename}</h3>
              <div className="history-stats">
                <span className="hs-total">{run.total_items} items</span>
                <span className="hs-oos">{run.out_of_stock_count} out of stock</span>
                <span className="hs-low">{run.low_stock_count} low</span>
                <span className="hs-crit">{run.critical_count} critical</span>
              </div>
              <button
                className="btn-text history-view-btn"
                onClick={(e) => { e.stopPropagation(); navigate(`/dashboard/${run.id}`); }}
              >
                View Dashboard <ArrowRight size={14} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default HistoryPage;
