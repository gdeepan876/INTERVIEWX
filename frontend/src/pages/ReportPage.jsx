import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import ScoreBadge from '../components/ScoreBadge';

export default function ReportPage({ interviewId, onNewInterview, onNavigate }) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);
  const [expandedQuestions, setExpandedQuestions] = useState({});

  useEffect(() => {
    let isMounted = true;

    async function loadReport() {
      setIsLoading(true);
      setErrorMessage(null);
      try {
        const reportData = await api.getReport(interviewId);
        if (isMounted) {
          setData(reportData);
          // By default expand the first question review
          setExpandedQuestions({ 0: true });
        }
      } catch (err) {
        if (isMounted) {
          setErrorMessage(err.message || 'Failed to load final report.');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    if (interviewId) {
      loadReport();
    }

    return () => {
      isMounted = false;
    };
  }, [interviewId]);

  const toggleQuestion = (index) => {
    setExpandedQuestions((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '64px 20px' }}>
        <div style={{ fontSize: '2rem', marginBottom: '16px' }}>⏳</div>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>
          Compiling Diagnostic Performance Report...
        </h3>
        <p style={{ color: 'var(--color-slate-500)', marginTop: '8px' }}>
          Aggregating dimensional evaluations, strengths, weaknesses, and improvement roadmaps.
        </p>
      </div>
    );
  }

  if (errorMessage || !data) {
    return (
      <div className="card" style={{ maxWidth: '600px', margin: '40px auto', textAlign: 'center' }}>
        <div style={{ fontSize: '2rem', color: 'var(--color-rose-500)', marginBottom: '12px' }}>⚠️</div>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '8px' }}>Unable to Load Report</h3>
        <p style={{ color: 'var(--color-slate-500)', marginBottom: '20px' }}>
          {errorMessage || 'Report data could not be found for this session.'}
        </p>
        <button className="btn btn-primary" onClick={onNewInterview}>
          Start a New Interview
        </button>
      </div>
    );
  }

  const { report, role, interview_type, difficulty, reviews } = data;

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto' }}>
      {/* Top Banner Header */}
      <div 
        className="card"
        style={{
          background: 'linear-gradient(135deg, var(--color-navy-900) 0%, var(--color-navy-800) 100%)',
          color: 'var(--color-white)',
          padding: '36px',
          marginBottom: '32px',
          border: '1px solid var(--color-navy-700)',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '20px' }}>
          <div>
            <div style={{ display: 'flex', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }}>
              <span className="badge badge-purple">{role}</span>
              <span className="badge badge-blue">{interview_type}</span>
              <span className="badge badge-navy" style={{ background: 'rgba(255, 255, 255, 0.15)' }}>{difficulty}</span>
            </div>
            <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '8px', letterSpacing: '-0.5px' }}>
              Final Interview Diagnostic Report
            </h1>
            <p style={{ color: 'var(--color-slate-300)', fontSize: '0.95rem' }}>
              Comprehensive performance appraisal and hiring readiness feedback.
            </p>
          </div>

          <div style={{ textAlign: 'center', background: 'rgba(255, 255, 255, 0.08)', padding: '20px 28px', borderRadius: '16px', border: '1px solid rgba(255, 255, 255, 0.15)' }}>
            <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '1px', color: '#DDD6FE', fontWeight: 600 }}>
              Overall Score
            </span>
            <div style={{ marginTop: '8px' }}>
              <ScoreBadge score={report.overall_score} max={10} size="large" />
            </div>
            <div style={{ marginTop: '10px', fontSize: '0.8rem', color: '#C4B5FD', fontWeight: 600 }}>
              {report.performance_rating}
            </div>
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <h3 className="card-title">Executive Performance Summary</h3>
        <p style={{ color: 'var(--color-navy-800)', fontSize: '0.975rem', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
          {report.performance_summary}
        </p>
      </div>

      {/* Strengths & Weaknesses 2-Column Grid */}
      <div className="grid-2" style={{ marginBottom: '24px' }}>
        {/* Strengths */}
        <div className="card" style={{ borderTop: '4px solid var(--color-emerald-500)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <span style={{ fontSize: '1.25rem' }}>✅</span>
            <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>
              Candidate Strengths
            </h4>
          </div>
          <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {report.strengths.map((str, idx) => (
              <li key={idx} style={{ fontSize: '0.9rem', color: 'var(--color-navy-800)', lineHeight: 1.5 }}>
                {str}
              </li>
            ))}
          </ul>
        </div>

        {/* Growth Areas */}
        <div className="card" style={{ borderTop: '4px solid var(--color-amber-500)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <span style={{ fontSize: '1.25rem' }}>🎯</span>
            <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>
              Areas for Improvement
            </h4>
          </div>
          <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {report.weaknesses.map((weak, idx) => (
              <li key={idx} style={{ fontSize: '0.9rem', color: 'var(--color-navy-800)', lineHeight: 1.5 }}>
                {weak}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recommendations & Action Plan */}
      <div className="card" style={{ borderTop: '4px solid var(--color-purple-600)', marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
          <span style={{ fontSize: '1.25rem' }}>🚀</span>
          <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>
            Actionable Next Steps & Study Roadmap
          </h4>
        </div>
        <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {report.recommendations.map((rec, idx) => (
            <li key={idx} style={{ fontSize: '0.9rem', color: 'var(--color-navy-800)', lineHeight: 1.5 }}>
              {rec}
            </li>
          ))}
        </ul>
      </div>

      {/* Question-by-Question Breakdown */}
      <div style={{ marginBottom: '36px' }}>
        <h3 style={{ fontSize: '1.3rem', fontWeight: 700, color: 'var(--color-navy-900)', marginBottom: '16px' }}>
          Question-by-Question Review ({reviews.length} questions)
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {reviews.map((rev, index) => {
            const isExpanded = !!expandedQuestions[index];
            return (
              <div 
                key={index} 
                className="card"
                style={{
                  padding: '20px',
                  borderLeft: rev.question_type === 'follow_up' ? '4px solid var(--color-purple-600)' : '4px solid var(--color-navy-800)',
                }}
              >
                <div 
                  onClick={() => toggleQuestion(index)}
                  style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', cursor: 'pointer', gap: '12px' }}
                >
                  <div>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '6px' }}>
                      <span className="badge badge-navy" style={{ fontSize: '0.72rem' }}>
                        Q{rev.question_order}
                      </span>
                      {rev.question_type === 'follow_up' && (
                        <span className="badge badge-purple" style={{ fontSize: '0.72rem' }}>
                          Follow-up
                        </span>
                      )}
                      {rev.topic_category && (
                        <span style={{ fontSize: '0.75rem', color: 'var(--color-slate-500)' }}>
                          {rev.topic_category}
                        </span>
                      )}
                    </div>
                    <h5 style={{ fontSize: '1.05rem', fontWeight: 600, color: 'var(--color-navy-900)' }}>
                      {rev.question_text}
                    </h5>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <ScoreBadge score={rev.score_total} max={10} />
                    <span style={{ fontSize: '1.25rem', color: 'var(--color-slate-400)' }}>
                      {isExpanded ? '▲' : '▼'}
                    </span>
                  </div>
                </div>

                {isExpanded && (
                  <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--border-light)' }}>
                    {/* Candidate Answer */}
                    <div style={{ marginBottom: '16px' }}>
                      <strong style={{ fontSize: '0.85rem', color: 'var(--color-slate-500)', textTransform: 'uppercase' }}>
                        Your Submitted Response:
                      </strong>
                      <div 
                        style={{ 
                          background: 'var(--color-slate-50)', 
                          padding: '12px 16px', 
                          borderRadius: '8px', 
                          marginTop: '6px',
                          fontSize: '0.925rem',
                          color: 'var(--color-navy-900)',
                          lineHeight: 1.6,
                          whiteSpace: 'pre-wrap'
                        }}
                      >
                        {rev.candidate_answer || 'No answer recorded.'}
                      </div>
                    </div>

                    {/* Feedback Summary */}
                    {rev.feedback_summary && (
                      <div style={{ marginBottom: '12px' }}>
                        <strong style={{ fontSize: '0.85rem', color: 'var(--color-purple-800)', textTransform: 'uppercase' }}>
                          Interviewer Critique:
                        </strong>
                        <p style={{ fontSize: '0.9rem', color: 'var(--color-navy-800)', marginTop: '4px', lineHeight: 1.5, whiteSpace: 'pre-line' }}>
                          {rev.feedback_summary}
                        </p>
                      </div>
                    )}

                    {/* Specific Suggestion */}
                    {rev.suggestions && (
                      <div>
                        <strong style={{ fontSize: '0.85rem', color: 'var(--color-amber-800)', textTransform: 'uppercase' }}>
                          Improvement Suggestion:
                        </strong>
                        <p style={{ fontSize: '0.9rem', color: 'var(--color-navy-800)', marginTop: '4px', lineHeight: 1.5 }}>
                          {rev.suggestions}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Navigation Actions */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', flexWrap: 'wrap', marginBottom: '40px' }}>
        <button className="btn btn-primary" onClick={onNewInterview} style={{ padding: '14px 28px' }}>
          Take Another Interview &rarr;
        </button>
        <button className="btn btn-secondary" onClick={() => onNavigate('history')} style={{ padding: '14px 28px' }}>
          View All History
        </button>
      </div>
    </div>
  );
}

