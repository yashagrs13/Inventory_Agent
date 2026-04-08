import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import AnalyzePage from './pages/AnalyzePage';
import DashboardPage from './pages/DashboardPage';
import HistoryPage from './pages/HistoryPage';
import ChatPage from './pages/ChatPage';
import AuditPage from './pages/AuditPage';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<AnalyzePage />} />
          <Route path="/dashboard/:runId?" element={<DashboardPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/audit" element={<AuditPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
