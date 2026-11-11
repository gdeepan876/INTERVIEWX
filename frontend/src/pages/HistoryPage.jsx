import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import ScoreBadge from '../components/ScoreBadge';

export default function HistoryPage({ onSelectSession, onStartInterview }) {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);

  const fetchHistory = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      const data = await api.getHistory();
      setHistory(data);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to retrieve interview history.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this interview record?')) {
      return;
    }

    try {
      await api.deleteInterview(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      alert('Failed to delete session: ' + err.message);
    }
  };

  const formatDate = (isoStr) => {
    if (!isoStr) return 'N/A';
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return isoStr;
    }
  };

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-navy-900)' }}>
            Interview Session History
          </h1>
          <p style={{ color: 'var(--color-slate-500)', fontSize: '0.925rem', marginTop: '4px' }}>
            Review past scores, feedback, and performance diagnostic reports.
          </p>
        </div>

        <button className="btn btn-primary" onClick={onStartInterview}>
          Start New Interview &rarr;
        </button>
      </div>

      {errorMessage && (
        <div 
          style={{ 
            background: 'var(--color-rose-100)', 
            border: '1px solid var(--color-rose-500)', 
            color: 'var(--color-rose-800)',
            padding: '12px 16px',
            borderRadius: '8px',
            marginBottom: '20px'
          }}
        >
          {errorMessage}
        </div>
      )}

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: '48px 0', color: 'var(--color-slate-500)' }}>
          <div style={{ fontSize: '2rem', marginBottom: '12px' }}>⏳</div>
          <p>Loading session records from SQLite...</p>
        </div>
      ) : history.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '64px 24px' }}>
          <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📋</div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-navy-900)', marginBottom: '8px' }}>
            No Interview Records Found
          </h3>
          <p style={{ color: 'var(--color-slate-500)', maxWidth: '440px', margin: '0 auto 24px auto', fontSize: '0.95rem' }}>
            You haven't completed any interview sessions yet. Start a session now to test your skills and track your scores.
          </p>
          <button className="btn btn-primary" onClick={onStartInterview}>
            Launch Your First Interview
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {history.map((item) => (
            <div
              key={item.id}
              className="card"
              style={{
                padding: '20px 24px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
              onClick={() => onSelectSession(item.id)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div 
                  style={{ 
                    background: 'var(--color-purple-50)', 
                    color: 'var(--color-purple-700)',
                    width: '44px',
                    height: '44px',
                    borderRadius: '10px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.25rem',
                    fontWeight: 700
                  }}
                >
                  IX
                </div>

                <div>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '4px', flexWrap: 'wrap' }}>
                    <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>
                      {item.role}
                    </h4>
                    <span className="badge badge-purple" style={{ fontSize: '0.72rem' }}>
                      {item.interview_type}
                    </span>
                    <span className="badge badge-blue" style={{ fontSize: '0.72rem' }}>
                      {item.difficulty}
                    </span>
                    <span 
                      className={`badge ${item.status === 'completed' ? 'badge-success' : 'badge-warning'}`} 
                      style={{ fontSize: '0.72rem' }}
                    >
                      {item.status === 'completed' ? 'Completed' : 'In Progress'}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.825rem', color: 'var(--color-slate-400)' }}>
                    <span>Recorded: {formatDate(item.created_at)}</span> &bull; <span>{item.total_questions} Question(s)</span>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                {item.overall_score !== null && item.overall_score !== undefined ? (
                  <ScoreBadge score={item.overall_score} max={10} />
                ) : (
                  <span className="badge badge-navy">In Progress</span>
                )}

                <button
                  className="btn btn-secondary"
                  style={{ padding: '8px 14px', fontSize: '0.85rem' }}
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectSession(item.id);
                  }}
                >
                  View Report
                </button>

                <button
                  className="btn btn-danger"
                  style={{ padding: '8px 12px', fontSize: '0.85rem' }}
                  onClick={(e) => handleDelete(item.id, e)}
                  title="Delete Session"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

