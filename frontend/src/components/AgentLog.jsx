import React, { useRef, useEffect } from 'react';
import { Brain, Wrench, CheckCircle, AlertCircle, MessageSquare, Zap, ChevronDown, ChevronUp } from 'lucide-react';

const EVENT_CONFIG = {
  agent_start: { icon: Zap, color: '#6366f1', label: 'Agent' },
  tool_call: { icon: Wrench, color: '#f59e0b', label: 'Tool' },
  tool_result: { icon: CheckCircle, color: '#10b981', label: 'Result' },
  thought: { icon: Brain, color: '#8b5cf6', label: 'Thinking' },
  action: { icon: Zap, color: '#6366f1', label: 'Action' },
  action_input: { icon: MessageSquare, color: '#94a3b8', label: 'Input' },
  agent_complete: { icon: CheckCircle, color: '#10b981', label: 'Done' },
  status: { icon: Zap, color: '#6366f1', label: 'Status' },
  log: { icon: MessageSquare, color: '#94a3b8', label: 'Log' },
  error: { icon: AlertCircle, color: '#ef4444', label: 'Error' },
};

function AgentLog({ events, isExpanded, onToggle }) {
  const logEndRef = useRef(null);

  useEffect(() => {
    if (isExpanded && logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [events, isExpanded]);

  // Filter out keepalive events
  const visibleEvents = events.filter(e => e.type !== 'keepalive' && e.type !== 'complete');

  if (visibleEvents.length === 0) return null;

  return (
    <div className="agent-log">
      <button className="agent-log-header" onClick={onToggle}>
        <div className="agent-log-title">
          <Brain size={18} />
          <span>Agent Thought Process</span>
          <span className="agent-log-count">{visibleEvents.length}</span>
        </div>
        {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </button>

      {isExpanded && (
        <div className="agent-log-body">
          {visibleEvents.map((event, index) => {
            const config = EVENT_CONFIG[event.type] || EVENT_CONFIG.log;
            const Icon = config.icon;
            const time = event.timestamp
              ? new Date(event.timestamp).toLocaleTimeString('en-IN', {
                  hour: '2-digit', minute: '2-digit', second: '2-digit'
                })
              : '';

            return (
              <div key={index} className="log-entry" style={{ '--entry-color': config.color }}>
                <div className="log-entry-icon">
                  <Icon size={14} />
                </div>
                <div className="log-entry-content">
                  <div className="log-entry-meta">
                    <span className="log-entry-label">{config.label}</span>
                    <span className="log-entry-time">{time}</span>
                  </div>
                  <p className="log-entry-text">{event.content}</p>
                </div>
              </div>
            );
          })}
          <div ref={logEndRef} />
        </div>
      )}
    </div>
  );
}

export default AgentLog;
