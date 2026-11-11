import React, { useState } from 'react';
import { api } from '../services/api';

const ROLES = [
  { id: 'Java Developer', title: 'Java Developer', icon: '☕', desc: 'Core Java, Spring Boot, Concurrency, JVM Internals' },
  { id: 'Python Developer', title: 'Python Developer', icon: '🐍', desc: 'CPython, Asyncio, Decorators, FastAPI, ORMs' },
  { id: 'Frontend Developer', title: 'Frontend Developer', icon: '⚛️', desc: 'React, Modern JS, Performance, Web Vitals, a11y' },
  { id: 'Backend Developer', title: 'Backend Developer', icon: '⚙️', desc: 'System Design, REST APIs, Databases, Caching, Auth' },
];

const TYPES = [
  { id: 'Technical', title: 'Technical Interview', icon: '💻', desc: 'Syntax, data structures, algorithms, frameworks, and architecture trade-offs.' },
  { id: 'HR', title: 'HR & Behavioral Interview', icon: '🤝', desc: 'STAR methodology, conflict resolution, teamwork, communication, and ownership.' },
];

const DIFFICULTIES = [
  { id: 'Beginner', title: 'Beginner', badge: '0 - 2 Yrs', desc: 'Core principles, fundamental definitions, and standard conventions.' },
  { id: 'Intermediate', title: 'Intermediate', badge: '2 - 5 Yrs', desc: 'Practical trade-offs, edge-case debugging, and framework internals.' },
  { id: 'Advanced', title: 'Advanced', badge: '5+ Yrs', desc: 'Complex system design, distributed consistency, and technical leadership.' },
];

export default function SetupPage({ onSessionStarted }) {
  const [selectedRole, setSelectedRole] = useState('Java Developer');
  const [selectedType, setSelectedType] = useState('Technical');
  const [selectedDifficulty, setSelectedDifficulty] = useState('Intermediate');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedRole || !selectedType || !selectedDifficulty) {
      setErrorMessage('Please select a Role, Interview Type, and Difficulty Level.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const sessionData = await api.startInterview(selectedRole, selectedType, selectedDifficulty);
      onSessionStarted(sessionData);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to start interview session. Ensure the backend server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ marginBottom: '28px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--color-navy-900)', marginBottom: '8px' }}>
          Configure Your Interview Session
        </h1>
        <p style={{ color: 'var(--color-slate-500)', fontSize: '1rem' }}>
          Customize the AI interviewer persona to simulate your upcoming job interview.
        </p>
      </div>

      {errorMessage && (
        <div 
          style={{ 
            background: 'var(--color-rose-100)', 
            border: '1px solid var(--color-rose-500)', 
            color: 'var(--color-rose-800)',
            padding: '14px 18px',
            borderRadius: '10px',
            marginBottom: '24px',
            fontSize: '0.925rem'
          }}
        >
          <strong>Error: </strong> {errorMessage}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Step 1: Select Role */}
        <div style={{ marginBottom: '32px' }}>
          <label style={{ display: 'block', fontSize: '1rem', fontWeight: 700, color: 'var(--color-navy-900)', marginBottom: '12px' }}>
            1. Select Target Job Role
          </label>
          <div className="grid-2">
            {ROLES.map((role) => {
              const isSelected = selectedRole === role.id;
              return (
                <div
                  key={role.id}
                  onClick={() => setSelectedRole(role.id)}
                  style={{
                    background: isSelected ? 'var(--color-purple-50)' : 'var(--color-white)',
                    border: `2px solid ${isSelected ? 'var(--color-purple-600)' : 'var(--border-light)'}`,
                    borderRadius: '12px',
                    padding: '18px 20px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '14px',
                    transition: 'all 0.2s ease',
                    boxShadow: isSelected ? 'var(--shadow-purple)' : 'none'
                  }}
                >
                  <div style={{ fontSize: '1.75rem' }}>{role.icon}</div>
                  <div>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: isSelected ? 'var(--color-purple-800)' : 'var(--color-navy-900)' }}>
                      {role.title}
                    </h3>
                    <p style={{ fontSize: '0.825rem', color: 'var(--color-slate-500)', marginTop: '4px', lineHeight: 1.4 }}>
                      {role.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Step 2: Select Type */}
        <div style={{ marginBottom: '32px' }}>
          <label style={{ display: 'block', fontSize: '1rem', fontWeight: 700, color: 'var(--color-navy-900)', marginBottom: '12px' }}>
            2. Select Interview Type
          </label>
          <div className="grid-2">
            {TYPES.map((t) => {
              const isSelected = selectedType === t.id;
              return (
                <div
                  key={t.id}
                  onClick={() => setSelectedType(t.id)}
                  style={{
                    background: isSelected ? 'var(--color-purple-50)' : 'var(--color-white)',
                    border: `2px solid ${isSelected ? 'var(--color-purple-600)' : 'var(--border-light)'}`,
                    borderRadius: '12px',
                    padding: '18px 20px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '14px',
                    transition: 'all 0.2s ease',
                    boxShadow: isSelected ? 'var(--shadow-purple)' : 'none'
                  }}
                >
                  <div style={{ fontSize: '1.75rem' }}>{t.icon}</div>
                  <div>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: isSelected ? 'var(--color-purple-800)' : 'var(--color-navy-900)' }}>
                      {t.title}
                    </h3>
                    <p style={{ fontSize: '0.825rem', color: 'var(--color-slate-500)', marginTop: '4px', lineHeight: 1.4 }}>
                      {t.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Step 3: Select Difficulty */}
        <div style={{ marginBottom: '36px' }}>
          <label style={{ display: 'block', fontSize: '1rem', fontWeight: 700, color: 'var(--color-navy-900)', marginBottom: '12px' }}>
            3. Select Difficulty & Experience Level
          </label>
          <div className="grid-3">
            {DIFFICULTIES.map((d) => {
              const isSelected = selectedDifficulty === d.id;
              return (
                <div
                  key={d.id}
                  onClick={() => setSelectedDifficulty(d.id)}
                  style={{
                    background: isSelected ? 'var(--color-purple-50)' : 'var(--color-white)',
                    border: `2px solid ${isSelected ? 'var(--color-purple-600)' : 'var(--border-light)'}`,
                    borderRadius: '12px',
                    padding: '18px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    boxShadow: isSelected ? 'var(--shadow-purple)' : 'none'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: isSelected ? 'var(--color-purple-800)' : 'var(--color-navy-900)' }}>
                      {d.title}
                    </h3>
                    <span className="badge badge-purple">{d.badge}</span>
                  </div>
                  <p style={{ fontSize: '0.825rem', color: 'var(--color-slate-500)', lineHeight: 1.4 }}>
                    {d.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Summary Card */}
        <div 
          className="card" 
          style={{ 
            background: 'var(--color-navy-900)', 
            color: 'var(--color-white)', 
            marginBottom: '28px',
            padding: '20px 24px'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
            <div>
              <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--color-purple-200)', letterSpacing: '1px', fontWeight: 600 }}>
                Selected Configuration Summary
              </span>
              <div style={{ display: 'flex', gap: '8px', marginTop: '6px', flexWrap: 'wrap' }}>
                <span className="badge badge-navy" style={{ background: 'var(--color-navy-800)', border: '1px solid var(--color-navy-700)' }}>
                  Role: {selectedRole}
                </span>
                <span className="badge badge-purple">
                  Format: {selectedType}
                </span>
                <span className="badge badge-blue">
                  Level: {selectedDifficulty}
                </span>
              </div>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={isLoading}
              style={{ padding: '14px 28px', fontSize: '1rem' }}
            >
              {isLoading ? 'Initializing Simulator...' : 'Launch Interview Session \u2192'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

