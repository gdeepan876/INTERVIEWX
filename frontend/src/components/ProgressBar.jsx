import React from 'react';

export default function ProgressBar({ current, total, isFollowUp }) {
  const percentage = Math.min(100, Math.round((current / total) * 100));

  return (
    <div style={{ margin: '16px 0 24px 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--color-navy-900)' }}>
            Question {current} of {total}
          </span>
          {isFollowUp && (
            <span className="badge badge-purple" style={{ fontSize: '0.72rem' }}>
              Adaptive Follow-up
            </span>
          )}
        </div>
        <span style={{ fontSize: '0.8rem', color: 'var(--color-slate-500)', fontWeight: 500 }}>
          {percentage}% Complete
        </span>
      </div>

      <div className="progress-container">
        <div 
          className="progress-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

