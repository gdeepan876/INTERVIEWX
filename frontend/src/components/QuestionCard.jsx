import React from 'react';

export default function QuestionCard({ question, role, difficulty, interviewType }) {
  if (!question) return null;

  const isFollowUp = question.question_type === 'follow_up';

  return (
    <div className="card" style={{ borderColor: isFollowUp ? 'var(--color-purple-600)' : 'var(--border-light)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span className="badge badge-navy">{role}</span>
          <span className="badge badge-purple">{difficulty}</span>
          <span className="badge badge-blue">{interviewType}</span>
          {question.topic_category && (
            <span style={{ fontSize: '0.8rem', color: 'var(--color-slate-500)', fontWeight: 500 }}>
              Category: {question.topic_category}
            </span>
          )}
        </div>

        {isFollowUp && (
          <span className="badge badge-purple">
            Targeted Follow-up Question
          </span>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
        <div 
          style={{
            background: isFollowUp ? 'linear-gradient(135deg, #7C3AED, #9333EA)' : 'var(--color-navy-800)',
            color: '#FFFFFF',
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: '1rem',
            flexShrink: 0
          }}
        >
          {isFollowUp ? 'AI+' : 'AI'}
        </div>

        <div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--color-navy-900)', lineHeight: 1.5 }}>
            {question.question_text}
          </h3>
          <p style={{ fontSize: '0.825rem', color: 'var(--color-slate-500)', marginTop: '8px' }}>
            Provide your detailed response below. Focus on technical specifics, practical examples, and clear structure.
          </p>
        </div>
      </div>
    </div>
  );
}

