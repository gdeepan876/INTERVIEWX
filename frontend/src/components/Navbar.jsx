import React from 'react';

export default function Navbar({ currentRoute, onNavigate }) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <a 
          href="#home" 
          className="brand-link" 
          onClick={(e) => { e.preventDefault(); onNavigate('home'); }}
        >
          <div className="brand-logo-badge">IX</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span className="brand-title">INTERVIEWX</span>
              <span className="brand-subtitle">Simulator</span>
            </div>
          </div>
        </a>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div className="mode-badge" title="Rule-based heuristic evaluator active. Gemini API scheduled for Phase 4.">
            <span className="mode-dot"></span>
            <span>Pre-LLM Dev Mode</span>
          </div>

          <nav className="nav-links">
            <button
              className={`nav-item ${currentRoute === 'home' ? 'active' : ''}`}
              onClick={() => onNavigate('home')}
            >
              Home
            </button>
            <button
              className={`nav-item ${currentRoute === 'setup' || currentRoute === 'room' ? 'active' : ''}`}
              onClick={() => onNavigate('setup')}
            >
              Start Interview
            </button>
            <button
              className={`nav-item ${currentRoute === 'history' ? 'active' : ''}`}
              onClick={() => onNavigate('history')}
            >
              History
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}

