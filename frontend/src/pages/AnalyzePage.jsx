import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileSpreadsheet, AlertCircle, Play, Loader2 } from 'lucide-react';
import StoryBoard from '../components/StoryBoard';
import AgentLog from '../components/AgentLog';

const API_BASE = 'http://127.0.0.1:5000';

function AnalyzePage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, uploading, analyzing, reporting, success, error
  const [message, setMessage] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');
  const [reportName, setReportName] = useState('');
  const [runId, setRunId] = useState(null);
  const [agentEvents, setAgentEvents] = useState([]);
  const [logExpanded, setLogExpanded] = useState(true);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus('idle');
      setMessage('');
      setAgentEvents([]);
    }
  };

  const startProcess = async () => {
    if (!file) return;

    setStatus('uploading');
    setMessage('Uploading raw data...');
    setAgentEvents([]);
    setLogExpanded(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/upload-stream`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      setStatus('analyzing');
      setMessage('Stock Analyst Agent is working...');

      let finalStatus = 'idle';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Parse SSE events from buffer
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.slice(6));

              // Update UI based on event type
              switch (event.type) {
                case 'agent_start':
                  if (event.content && event.content.toLowerCase().includes('reporter')) {
                    setStatus('reporting');
                  } else {
                    setStatus('analyzing');
                  }
                  setMessage(event.content || 'Agent is working...');
                  setAgentEvents(prev => [...prev, event]);
                  break;

                case 'tool_call':
                  setMessage('Executing analysis tool...');
                  setAgentEvents(prev => [...prev, event]);
                  break;

                case 'tool_result':
                  setAgentEvents(prev => [...prev, event]);
                  break;

                case 'thought':
                case 'action':
                case 'action_input':
                case 'log':
                case 'status':
                  setAgentEvents(prev => [...prev, event]);
                  break;

                case 'agent_complete':
                  setAgentEvents(prev => [...prev, event]);
                  break;

                case 'complete':
                  finalStatus = 'success';
                  setStatus('success');
                  setDownloadUrl(`${API_BASE}${event.download_url}`);
                  setReportName(event.filename);
                  setRunId(event.run_id);
                  setMessage('Analysis Complete! Your report is ready.');
                  setLogExpanded(false);
                  break;

                case 'error':
                  finalStatus = 'error';
                  setStatus('error');
                  setMessage(event.content || 'An error occurred.');
                  setAgentEvents(prev => [...prev, event]);
                  break;

                case 'keepalive':
                  // Ignore keepalive events
                  break;

                default:
                  setAgentEvents(prev => [...prev, event]);
              }
            } catch (parseErr) {
              // Skip malformed JSON
            }
          }
        }
      }

      // If we exited the loop without getting a 'complete' or 'error' event
      if (finalStatus !== 'success' && finalStatus !== 'error') {
        setStatus('error');
        setMessage('Connection closed unexpectedly.');
      }

    } catch (error) {
      console.error(error);
      setStatus('error');
      setMessage(error.message || 'An unexpected error occurred.');
    }
  };

  const triggerDownload = () => {
    if (downloadUrl) {
      window.open(downloadUrl, '_blank');
    }
  };

  const viewDashboard = () => {
    if (runId) {
      navigate(`/dashboard/${runId}`);
    }
  };

  const resetState = () => {
    setStatus('idle');
    setFile(null);
    setRunId(null);
    setAgentEvents([]);
    setMessage('');
    setDownloadUrl('');
    setReportName('');
  };

  return (
    <div className="analyze-page">
      <div className="page-header">
        <h1>Analyze Inventory</h1>
        <p className="page-subtitle">Upload your Tally export and let the AI crew analyze it</p>
      </div>

      <StoryBoard status={status} />

      {/* Agent Thought Log */}
      <AgentLog
        events={agentEvents}
        isExpanded={logExpanded}
        onToggle={() => setLogExpanded(prev => !prev)}
      />

      {/* Interaction Area */}
      <div className="interaction-zone">
        {status === 'success' ? (
          <div className="result-card">
            <FileSpreadsheet size={48} className="result-icon" />
            <h2>{reportName}</h2>
            <div className="result-actions">
              <button onClick={viewDashboard} className="btn-primary">
                View Dashboard
              </button>
              <button onClick={triggerDownload} className="btn-secondary">
                Download Report
              </button>
            </div>
            <button onClick={resetState} className="btn-text">
              Analyze Another File
            </button>
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
              <Upload size={48} color={file ? "#6366f1" : "#9ca3af"} />
              {file ? (
                <h3>{file.name}</h3>
              ) : (
                <>
                  <h3>Click to upload Tally Export</h3>
                  <p>or drag and drop .xlsx file here</p>
                </>
              )}
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept=".xlsx,.xls"
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
                {status !== 'idle' && status !== 'error' && (
                  <>
                    <Loader2 className="spin-slow" size={16} />
                    <span>{message}</span>
                  </>
                )}
              </div>
              <button
                className="btn-primary"
                disabled={!file || (status !== 'idle' && status !== 'error')}
                onClick={startProcess}
              >
                {status === 'idle' || status === 'error' ? (
                  <>
                    <Play size={18} /> Run Analysis Crew
                  </>
                ) : 'Processing...'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalyzePage;
