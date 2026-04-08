import React from 'react';
import { NavLink } from 'react-router-dom';
import { BarChart2, Upload, LayoutDashboard, Clock, MessageSquare, Shield } from 'lucide-react';

function Sidebar() {
  const navItems = [
    { path: '/', icon: Upload, label: 'Analyze', end: true },
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/history', icon: Clock, label: 'History' },
    { path: '/chat', icon: MessageSquare, label: 'Chat' },
    { path: '/audit', icon: Shield, label: 'Audit' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <BarChart2 size={28} />
        <span className="sidebar-logo-text">
          Inventory<span className="accent">AI</span>gent
        </span>
      </div>

      <nav className="sidebar-nav">
        {navItems.map(({ path, icon: Icon, label, end }) => (
          <NavLink
            key={path}
            to={path}
            end={end}
            className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
          >
            <Icon size={20} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <p>Powered by CrewAI + Gemini</p>
      </div>
    </aside>
  );
}

export default Sidebar;
