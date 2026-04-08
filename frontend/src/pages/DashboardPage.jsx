import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Package, AlertTriangle, XCircle, TrendingDown, ArrowLeft, Download, Mail, Send, Loader2 } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, LineChart, Line, CartesianGrid } from 'recharts';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

const COLORS = {
  healthy: '#10b981',
  low_stock: '#f59e0b',
  out_of_stock: '#ef4444',
  critical: '#dc2626'
};

function DashboardPage() {
  const { runId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [email, setEmail] = useState('');
  const [alertStatus, setAlertStatus] = useState('idle'); // idle, sending, success, error
  const [alertMessage, setAlertMessage] = useState('');

  // Forecast state
  const [forecasts, setForecasts] = useState(null);
  const [loadingForecasts, setLoadingForecasts] = useState(false);
  const [forecastError, setForecastError] = useState('');

  useEffect(() => {
    if (!runId) {
      // If no runId, try to load the latest run
      axios.get(`${API_BASE}/history`)
        .then(res => {
          const runs = res.data.runs;
          if (runs && runs.length > 0) {
            navigate(`/dashboard/${runs[0].id}`, { replace: true });
          } else {
            setLoading(false);
            setError('No analysis runs found. Upload a file first.');
          }
        })
        .catch(() => {
          setLoading(false);
          setError('Failed to load data.');
        });
      return;
    }

    axios.get(`${API_BASE}/results/${runId}`)
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.response?.data?.error || 'Failed to load results.');
        setLoading(false);
      });
  }, [runId, navigate]);

  useEffect(() => {
    if (activeTab === 'forecasts' && !forecasts && runId) {
      setLoadingForecasts(true);
      setForecastError('');
      axios.get(`${API_BASE}/forecast/top?run_id=${runId}`)
        .then(res => {
          setForecasts(res.data.forecasts || []);
          setLoadingForecasts(false);
        })
        .catch(err => {
          setForecastError(err.response?.data?.error || 'Failed to generate forecasts.');
          setLoadingForecasts(false);
        });
    }
  }, [activeTab, runId, forecasts]);

  const handleSendAlert = async () => {
    if (!email) return;
    setAlertStatus('sending');
    setAlertMessage('');

    try {
      const res = await axios.post(`${API_BASE}/alerts/send`, {
        run_id: runId,
        to_email: email
      });
      setAlertStatus('success');
      setAlertMessage(res.data.message || 'Alert sent successfully!');
    } catch (err) {
      setAlertStatus('error');
      setAlertMessage(err.response?.data?.error || 'Failed to send alert.');
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-loading">
          <div className="loading-spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-empty">
          <Package size={48} />
          <h2>{error}</h2>
          <button className="btn-primary" onClick={() => navigate('/')}>
            Go to Analyze
          </button>
        </div>
      </div>
    );
  }

  const stats = data.summary_stats;
  const pieData = [
    { name: 'Healthy', value: stats.healthy_count, color: COLORS.healthy },
    { name: 'Low Stock', value: stats.low_stock_count, color: COLORS.low_stock },
    { name: 'Out of Stock', value: stats.out_of_stock_count, color: COLORS.out_of_stock },
    { name: 'Critical', value: stats.critical_count, color: COLORS.critical },
  ].filter(d => d.value > 0);

  // Top critical items for bar chart
  const criticalItems = [
    ...(data.items.critical || []).map(i => ({ ...i, type: 'Critical' })),
    ...(data.items.low_stock || []).slice(0, 10).map(i => ({ ...i, type: 'Low Stock' })),
  ].slice(0, 10);

  const barData = criticalItems.map(item => ({
    name: item.Name.length > 20 ? item.Name.substring(0, 20) + '...' : item.Name,
    balance: item['Closing Balance'],
    fill: item.type === 'Critical' ? COLORS.critical : COLORS.low_stock
  }));

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <div className="page-header-top">
          <h1>Dashboard</h1>
          {data.download_url && (
            <button
              className="btn-secondary btn-sm"
              onClick={() => window.open(`${API_BASE}${data.download_url}`, '_blank')}
            >
              <Download size={16} /> Download Report
            </button>
          )}
        </div>
        <p className="page-subtitle">
          Analysis of <strong>{data.input_filename}</strong> &middot;{' '}
          {new Date(data.timestamp).toLocaleDateString('en-IN', {
            day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
          })}
        </p>
      </div>

      {/* Tabs */}
      <div className="dashboard-tabs">
        <button
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab-btn ${activeTab === 'items' ? 'active' : ''}`}
          onClick={() => setActiveTab('items')}
        >
          Item Details
        </button>
        <button
          className={`tab-btn ${activeTab === 'alerts' ? 'active' : ''}`}
          onClick={() => setActiveTab('alerts')}
        >
          Smart Alerts
        </button>
        <button
          className={`tab-btn ${activeTab === 'forecasts' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecasts')}
        >
          Depletion Forecast
        </button>
      </div>

      {activeTab === 'overview' && (
        <>
          {/* Stat Cards */}
          <div className="stat-grid">
            <div className="stat-card">
              <div className="stat-icon" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#6366f1' }}>
                <Package size={24} />
              </div>
              <div className="stat-info">
                <span className="stat-value">{stats.total_items}</span>
                <span className="stat-label">Total Items</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#ef4444' }}>
                <XCircle size={24} />
              </div>
              <div className="stat-info">
                <span className="stat-value">{stats.out_of_stock_count}</span>
                <span className="stat-label">Out of Stock</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' }}>
                <AlertTriangle size={24} />
              </div>
              <div className="stat-info">
                <span className="stat-value">{stats.low_stock_count}</span>
                <span className="stat-label">Low Stock</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon" style={{ background: 'rgba(220, 38, 38, 0.15)', color: '#dc2626' }}>
                <TrendingDown size={24} />
              </div>
              <div className="stat-info">
                <span className="stat-value">{stats.critical_count}</span>
                <span className="stat-label">Critical (Negative)</span>
              </div>
            </div>
          </div>

          {/* Charts */}
          <div className="chart-grid">
            <div className="chart-card">
              <h3>Stock Health Distribution</h3>
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={4}
                    dataKey="value"
                    animationBegin={0}
                    animationDuration={800}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: '#1e293b',
                      border: '1px solid rgba(255,255,255,0.1)',
                      borderRadius: '8px',
                      color: '#f8fafc'
                    }}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-card">
              <h3>Top Items Needing Attention</h3>
              {barData.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={barData} layout="vertical" margin={{ left: 20 }}>
                    <XAxis type="number" stroke="#94a3b8" />
                    <YAxis type="category" dataKey="name" width={120} stroke="#94a3b8" tick={{ fontSize: 12 }} />
                    <Tooltip
                      contentStyle={{
                        background: '#1e293b',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                        color: '#f8fafc'
                      }}
                    />
                    <Bar dataKey="balance" radius={[0, 4, 4, 0]} animationDuration={800}>
                      {barData.map((entry, index) => (
                        <Cell key={index} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="chart-empty">
                  <p>No critical or low stock items found 🎉</p>
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {activeTab === 'items' && (
        <div className="items-section">
          {/* Out of Stock Table */}
          {data.items.out_of_stock && data.items.out_of_stock.length > 0 && (
            <div className="data-table-card">
              <h3>
                <span className="table-badge badge-red">{data.items.out_of_stock.length}</span>
                Out of Stock Items
              </h3>
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Item Name</th>
                      <th>Closing Balance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.items.out_of_stock.map((item, i) => (
                      <tr key={i}>
                        <td>{i + 1}</td>
                        <td>{item.Name}</td>
                        <td className="text-red">{item['Closing Balance']}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Low Stock Table */}
          {data.items.low_stock && data.items.low_stock.length > 0 && (
            <div className="data-table-card">
              <h3>
                <span className="table-badge badge-amber">{data.items.low_stock.length}</span>
                Low Stock Items
              </h3>
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Item Name</th>
                      <th>Closing Balance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.items.low_stock.map((item, i) => (
                      <tr key={i}>
                        <td>{i + 1}</td>
                        <td>{item.Name}</td>
                        <td className="text-amber">{item['Closing Balance']}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Critical Table */}
          {data.items.critical && data.items.critical.length > 0 && (
            <div className="data-table-card">
              <h3>
                <span className="table-badge badge-red">{data.items.critical.length}</span>
                Critical Stock Items (Negative Balance)
              </h3>
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Item Name</th>
                      <th>Closing Balance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.items.critical.map((item, i) => (
                      <tr key={i}>
                        <td>{i + 1}</td>
                        <td>{item.Name}</td>
                        <td className="text-red">{item['Closing Balance']}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'alerts' && (
        <div className="alerts-section">
          <div className="alert-card">
            <div className="alert-header">
              <Mail size={32} color="#6366f1" />
              <div>
                <h3>Smart Reorder Alerts</h3>
                <p>Notify business owners or suppliers about critical stock items.</p>
              </div>
            </div>
            
            <div className="alert-form">
              <label>Recipient Email Address</label>
              <div className="alert-input-group">
                <input 
                  type="email" 
                  placeholder="supplier@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={alertStatus === 'sending'}
                />
                <button 
                  className="btn-primary"
                  onClick={handleSendAlert}
                  disabled={!email || alertStatus === 'sending' || (stats.critical_count === 0 && stats.out_of_stock_count === 0)}
                >
                  {alertStatus === 'sending' ? (
                    <><Loader2 size={16} className="spin-slow" /> Sending...</>
                  ) : (
                    <><Send size={16} /> Send Alert</>
                  )}
                </button>
              </div>
              {(stats.critical_count === 0 && stats.out_of_stock_count === 0) && (
                <p className="text-amber mt-2 text-sm">No critical or out of stock items to report in this run.</p>
              )}
            </div>

            {alertStatus === 'success' && (
              <div className="alert-message success">
                <p>{alertMessage}</p>
              </div>
            )}

            {alertStatus === 'error' && (
              <div className="alert-message error">
                <p>{alertMessage}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'forecasts' && (
        <div className="forecasts-section">
          {loadingForecasts ? (
            <div className="dashboard-loading">
              <div className="loading-spinner"></div>
              <p>Analyzing historical data to predict depletion...</p>
            </div>
          ) : forecastError ? (
            <div className="alert-message error">
              <p>{forecastError}</p>
            </div>
          ) : forecasts && forecasts.length > 0 ? (
            <div className="forecast-grid">
              {forecasts.map((f, i) => (
                <div key={i} className="chart-card forecast-card">
                  <div className="forecast-header">
                    <h3>{f.item_name}</h3>
                    <div className="forecast-badges">
                      {f.trend === 'decreasing' ? (
                        <>
                          <span className="badge badge-red">Est. Depletion: {f.estimated_depletion_date}</span>
                          <span className="badge badge-amber">{f.burn_rate_per_day} units/day</span>
                        </>
                      ) : (
                        <span className="badge badge-green">Stable Trend</span>
                      )}
                    </div>
                  </div>
                  
                  <div style={{ width: '100%', height: 280, marginTop: 20 }}>
                    <ResponsiveContainer>
                      <LineChart data={f.data_points} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis 
                          dataKey="date" 
                          stroke="#94a3b8" 
                          tick={{ fontSize: 12 }} 
                          tickFormatter={(val) => new Date(val).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
                        />
                        <YAxis stroke="#94a3b8" tick={{ fontSize: 12 }} />
                        <Tooltip 
                          contentStyle={{
                            background: '#1e293b',
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '8px',
                            color: '#f8fafc'
                          }}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="actual" stroke="#3b82f6" strokeWidth={2} name="Actual Stock" connectNulls />
                        <Line type="monotone" dataKey="predicted" stroke="#ef4444" strokeWidth={2} strokeDasharray="5 5" name="Forecast" connectNulls />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="chart-empty">
              <p>No low stock items require forecasting right now.</p>
            </div>
          )}
        </div>
      )}

      {/* Agent Summary */}
      {data.agent_output && (
        <div className="agent-summary-card">
          <h3>AI Agent Summary</h3>
          <p>{data.agent_output}</p>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;
