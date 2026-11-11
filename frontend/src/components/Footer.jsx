import React from 'react';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>
          <strong>INTERVIEWX</strong> – Professional AI Interview Simulator for Engineers & HR Candidates.
        </p>
        <p style={{ fontSize: '0.8rem', color: 'var(--color-slate-500)' }}>
          Built with React, Python FastAPI & SQLite. Gemini LLM cognitive integration scheduled for Phase 4.
        </p>
      </div>
    </footer>
  );
}

