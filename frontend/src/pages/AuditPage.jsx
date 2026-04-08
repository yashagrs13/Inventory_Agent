import React, { useState, useRef } from 'react';
import { Shield, Upload, AlertCircle, FileText, CheckCircle, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

function AuditPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, processing, success, error
  const [message, setMessage] = useState('');
  const [report, setReport] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus('idle');
      setMessage('');
      setReport(null);
    }
  };

  const startAudit = async () => {
    if (!file) return;

    setStatus('processing');
    setMessage('Financial Compliance Auditor is reviewing the ledger...');
    setReport(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/audit/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setStatus('success');
      setMessage('Ledger Audit Complete');
      setReport(response.data.report);

    } catch (error) {
      console.error(error);
      setStatus('error');
      setMessage(error.response?.data?.error || error.message || 'An unexpected error occurred.');
    }
  };

  const resetState = () => {
    setStatus('idle');
    setFile(null);
    setMessage('');
    setReport(null);
  };

  return (
    <div className="audit-page">
      <div className="page-header">
        <h1>Ledger Audit</h1>
        <p className="page-subtitle">Upload complete ledger exports for AI-driven risk assessment</p>
      </div>

      <div className="interaction-zone" style={{ marginTop: '30px' }}>
        {status === 'success' ? (
          <div className="audit-result-container">
            <div className="result-card" style={{ marginBottom: '24px' }}>
              <Shield size={48} className="result-icon" color="#10b981" />
              <h2>Audit Complete</h2>
              <p className="text-muted">The agent has finished reviewing {file.name}.</p>
              <div className="result-actions" style={{ marginTop: '20px' }}>
                <button onClick={resetState} className="btn-secondary">
                  Audit Another Ledger
                </button>
              </div>
            </div>

            <div className="alert-card" style={{ maxWidth: '100%', textAlign: 'left' }}>
              <div className="alert-header">
                <FileText size={24} color="#6366f1" />
                <h3>Financial Risk Summary</h3>
              </div>
              <div className="markdown-body" style={{ color: 'var(--text-main)', lineHeight: '1.7' }}>
                <ReactMarkdown>{report}</ReactMarkdown>
              </div>
            </div>
          </div>
        ) : (
          <div className="upload-card">
            <div
              className="drop-zone"
              onClick={() => fileInputRef.current.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
              }}
            >
              <Upload size={48} color={file ? "#10b981" : "#9ca3af"} />
              {file ? (
                <h3 style={{ color: '#10b981' }}>{file.name} ready for audit</h3>
              ) : (
                <>
                  <h3>Click to upload Ledger Export</h3>
                  <p>or drag and drop .xlsx or .csv file here</p>
                </>
              )}
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept=".xlsx,.xls,.csv"
                onChange={handleFileChange}
              />
            </div>

            {status === 'error' && (
              <div className="error-banner">
                <AlertCircle size={20} />
                <span>{message}</span>
              </div>
            )}

            <div className="action-area">
              <div className="status-text">
                {status === 'processing' && (
                  <>
                    <Loader2 className="spin-slow" size={16} />
                    <span>{message}</span>
                  </>
                )}
              </div>
              <button
                className="btn-primary"
                disabled={!file || status === 'processing'}
                onClick={startAudit}
                style={{ background: status === 'idle' ? '#10b981' : undefined }}
              >
                {status === 'idle' || status === 'error' ? (
                  <>
                    <Shield size={18} /> Run Compliance Audit
                  </>
                ) : 'Auditing...'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AuditPage;
