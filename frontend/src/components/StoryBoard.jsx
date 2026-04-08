import React from 'react';
import { BarChart2, FileText, CheckCircle, Loader2 } from 'lucide-react';

function StoryBoard({ status }) {
  return (
    <div className="story-board">
      {/* Agent 1: Analyst */}
      <div className={`agent-card ${['analyzing', 'reporting', 'success'].includes(status) ? 'active' : ''}`}>
        <div className="icon-wrapper analyst">
          {status === 'analyzing' ? <Loader2 className="spin" /> : <BarChart2 />}
        </div>
        <h3>Stock Analyst</h3>
        <p>Identifies low stock &amp; critical items</p>
      </div>

      <div className={`connector ${['reporting', 'success'].includes(status) ? 'active' : ''}`}>
        <div className="line"></div>
      </div>

      {/* Agent 2: Reporter */}
      <div className={`agent-card ${['reporting', 'success'].includes(status) ? 'active' : ''}`}>
        <div className="icon-wrapper reporter">
          {status === 'reporting' ? <Loader2 className="spin" /> : <FileText />}
        </div>
        <h3>Business Reporter</h3>
        <p>Summarizes insights for executives</p>
      </div>

      <div className={`connector ${status === 'success' ? 'active' : ''}`}>
        <div className="line"></div>
      </div>

      {/* Outcome */}
      <div className={`agent-card ${status === 'success' ? 'active' : ''} outcome`}>
        <div className="icon-wrapper success">
          <CheckCircle />
        </div>
        <h3>Ready</h3>
        <p>Final Report Generated</p>
      </div>
    </div>
  );
}

export default StoryBoard;
