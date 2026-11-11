import React from 'react';

export default function ScoreBadge({ score, max = 10, size = 'normal' }) {
  if (score === null || score === undefined) {
    return <span className="badge badge-navy">Pending</span>;
  }

  const numericScore = typeof score === 'number' ? score : parseFloat(score);

  let pillClass = 'score-pill-mid';
  if (numericScore >= 8.0) {
    pillClass = 'score-pill-high';
  } else if (numericScore < 5.0) {
    pillClass = 'score-pill-low';
  }

  const style = size === 'large' 
    ? { fontSize: '1.75rem', padding: '8px 20px', borderRadius: '12px' } 
    : {};

  return (
    <div className={`score-pill ${pillClass}`} style={style}>
      <span>{numericScore.toFixed(1)}</span>
      <span style={{ fontSize: size === 'large' ? '1rem' : '0.8rem', opacity: 0.75 }}>/ {max}</span>
    </div>
  );
}

