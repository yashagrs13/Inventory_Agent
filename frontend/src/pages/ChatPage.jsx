import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2, MessageSquare } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'bot',
      content: "Hello! I'm your Inventory Data Analyst. You can ask me questions about your past inventory runs, out of stock items, or overall stock trends. For example: 'Which items were out of stock in the most recent run?'"
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { id: Date.now(), role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/query`, {
        message: userMessage
      });

      setMessages(prev => [
        ...prev,
        { id: Date.now(), role: 'bot', content: response.data.response }
      ]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [
        ...prev,
        { 
          id: Date.now(), 
          role: 'error', 
          content: "Sorry, I encountered an error while querying the database. Please try again." 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-page">
      <div className="page-header">
        <h1>Chat with Data</h1>
        <p className="page-subtitle">Ask questions about your inventory in plain English</p>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`chat-message ${msg.role}`}>
              <div className="chat-avatar">
                {msg.role === 'user' ? <User size={18} /> : 
                 msg.role === 'error' ? <MessageSquare size={18} color="#ef4444" /> :
                 <Bot size={18} />}
              </div>
              <div className="chat-bubble">
                {msg.content.split('\n').map((line, i) => (
                  <span key={i}>
                    {line}
                    <br />
                  </span>
                ))}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="chat-message bot loading">
              <div className="chat-avatar">
                <Bot size={18} />
              </div>
              <div className="chat-bubble">
                <Loader2 className="spin-slow" size={18} />
                <span>Analyzing database...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question..."
            rows={1}
            disabled={isLoading}
          />
          <button 
            className="btn-primary icon-btn" 
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
