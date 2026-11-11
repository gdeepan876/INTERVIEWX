import React from 'react';
import ScoreBadge from './ScoreBadge';

export default function FeedbackCard({ evaluation, nextAction, onContinue, isLastQuestion }) {
  if (!evaluation) return null;

  return (
    <div 
      className="card" 
      style={{ 
        marginTop: '24px', 
        borderLeft: '4px solid var(--color-purple-600)',
        background: '#FAF5FF',
        boxShadow: 'var(--shadow-md)'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '20px' }}>
        <div>
          <span className="badge badge-purple" style={{ marginBottom: '6px' }}>
            Instant AI Evaluation
          </span>
          <h4 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>
            Evaluation & Score Breakdown
          </h4>
        </div>

        <ScoreBadge score={evaluation.score_total} max={10} size="large" />
      </div>

      {/* 4 Pillars Breakdown Grid */}
      <div 
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
          gap: '12px',
          marginBottom: '20px',
          background: 'var(--color-white)',
          padding: '16px',
          borderRadius: '12px',
          border: '1px solid var(--color-purple-200)'
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--color-slate-500)', textTransform: 'uppercase', fontWeight: 600 }}>
            Correctness
          </div>
          <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--color-navy-900)', marginTop: '4px' }}>
            {evaluation.score_correctness.toFixed(1)} <span style={{ fontSize: '0.75rem', color: 'var(--color-slate-400)' }}>/ 2.5</span>
          </div>
        </div>

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--color-slate-500)', textTransform: 'uppercase', fontWeight: 600 }}>
            Relevance
          </div>
          <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--color-navy-900)', marginTop: '4px' }}>
            {evaluation.score_relevance.toFixed(1)} <span style={{ fontSize: '0.75rem', color: 'var(--color-slate-400)' }}>/ 2.5</span>
          </div>
        </div>

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--color-slate-500)', textTransform: 'uppercase', fontWeight: 600 }}>
            Clarity
          </div>
          <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--color-navy-900)', marginTop: '4px' }}>
            {evaluation.score_clarity.toFixed(1)} <span style={{ fontSize: '0.75rem', color: 'var(--color-slate-400)' }}>/ 2.5</span>
          </div>
        </div>

        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--color-slate-500)', textTransform: 'uppercase', fontWeight: 600 }}>
            Technical Depth
          </div>
          <div style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--color-navy-900)', marginTop: '4px' }}>
            {evaluation.score_depth.toFixed(1)} <span style={{ fontSize: '0.75rem', color: 'var(--color-slate-400)' }}>/ 2.5</span>
          </div>
        </div>
      </div>

      {/* Qualitative Feedback */}
      <div style={{ marginBottom: '16px' }}>
        <h5 style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--color-navy-900)', marginBottom: '4px' }}>
          Interviewer Feedback:
        </h5>
        <p style={{ fontSize: '0.925rem', color: 'var(--color-navy-800)', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
          {evaluation.feedback_summary}
        </p>
      </div>

      {/* Actionable Suggestions */}
      <div style={{ marginBottom: '24px' }}>
        <h5 style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--color-purple-800)', marginBottom: '4px' }}>
          Actionable Suggestions for Improvement:
        </h5>
        <p style={{ fontSize: '0.925rem', color: 'var(--color-navy-800)', lineHeight: 1.6 }}>
          {evaluation.suggestions}
        </p>
      </div>

      {/* Follow-up notice */}
      {nextAction === 'follow_up' && (
        <div 
          style={{
            background: 'var(--color-purple-100)',
            border: '1px dashed var(--color-purple-600)',
            padding: '12px 16px',
            borderRadius: '8px',
            marginBottom: '20px',
            fontSize: '0.875rem',
            color: 'var(--color-purple-800)',
            fontWeight: 500
          }}
        >
          Adaptive Follow-Up Triggered: The interviewer has prepared a context-aware follow-up question to probe deeper into your answer.
        </div>
      )}

      {/* Action CTA */}
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <button className="btn btn-primary" onClick={onContinue}>
          {nextAction === 'completed' || isLastQuestion
            ? 'Generate Final Diagnostic Report'
            : (nextAction === 'follow_up' ? 'Answer Follow-Up Question' : 'Proceed to Next Question')}
          <span>&rarr;</span>
        </button>
      </div>
    </div>
  );
}

