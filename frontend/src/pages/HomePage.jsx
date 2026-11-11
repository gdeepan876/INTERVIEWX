import React from 'react';

export default function HomePage({ onStartInterview, onNavigate }) {
  const roles = [
    { title: 'Java Developer', icon: '☕', desc: 'Core Java, Spring Boot, Concurrency, JVM Internals & Microservices.' },
    { title: 'Python Developer', icon: '🐍', desc: 'CPython Internals, Asyncio, Decorators, FastAPI, ORM & Profiling.' },
    { title: 'Frontend Developer', icon: '⚛️', desc: 'React, Modern JS, Performance, Web Vitals, State & Accessibility.' },
    { title: 'Backend Developer', icon: '⚙️', desc: 'System Design, REST/gRPC, SQL/NoSQL, Caching, Auth & Scalability.' },
  ];

  const pillars = [
    { name: 'Correctness', weight: '2.5 pts', desc: 'Factual, conceptual, and syntactic accuracy of technical explanations.' },
    { name: 'Relevance', weight: '2.5 pts', desc: 'Direct, focused response addressing the prompt without extraneous filler.' },
    { name: 'Clarity', weight: '2.5 pts', desc: 'Logical sentence flow, structured explanation, and professional phrasing.' },
    { name: 'Technical Depth', weight: '2.5 pts', desc: 'Discussion of edge cases, internal mechanisms, and architectural trade-offs.' },
  ];

  return (
    <div>
      {/* Pre-LLM Architecture Transparency Notice */}
      <div className="notice-box">
        <span className="notice-icon">ℹ️</span>
        <div className="notice-text">
          <strong>Pre-LLM Architecture Mode Active:</strong> INTERVIEWX is currently operating in 
          Structured Rule-Based Evaluation Mode. All database schemas, session workflows, multi-dimensional scoring 
          rubrics, and question progression loops are fully operational. Full cognitive Gemini LLM API integration 
          is planned for Phase 4.
        </div>
      </div>

      {/* Hero Section */}
      <div 
        className="card" 
        style={{ 
          background: 'linear-gradient(135deg, var(--color-navy-900) 0%, var(--color-navy-800) 100%)',
          color: 'var(--color-white)',
          padding: '48px 36px',
          marginBottom: '40px',
          border: '1px solid var(--color-navy-700)',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <div style={{ maxWidth: '680px', position: 'relative', zIndex: 1 }}>
          <span 
            className="badge badge-purple" 
            style={{ 
              background: 'rgba(124, 58, 237, 0.25)', 
              color: '#DDD6FE', 
              borderColor: 'rgba(124, 58, 237, 0.5)',
              marginBottom: '16px' 
            }}
          >
            Realistic AI Interview Simulator
          </span>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800, lineHeight: 1.2, marginBottom: '16px', letterSpacing: '-0.5px' }}>
            Ace Your Next Tech or HR Interview with INTERVIEWX
          </h1>
          <p style={{ fontSize: '1.1rem', color: 'var(--color-slate-300)', lineHeight: 1.6, marginBottom: '28px' }}>
            Practice real technical challenges and behavioral STAR questions. Receive instant multi-dimensional 
            evaluations, adaptive follow-ups, and a comprehensive performance diagnostic report.
          </p>
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            <button 
              className="btn btn-primary" 
              style={{ padding: '14px 28px', fontSize: '1.05rem' }}
              onClick={onStartInterview}
            >
              Start Interview Now &rarr;
            </button>
            <button 
              className="btn btn-secondary" 
              style={{ background: 'rgba(255, 255, 255, 0.1)', color: '#FFFFFF', borderColor: 'rgba(255, 255, 255, 0.2)' }}
              onClick={() => onNavigate('history')}
            >
              View Interview History
            </button>
          </div>
        </div>
      </div>

      {/* Supported Roles Grid */}
      <div style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '8px', color: 'var(--color-navy-900)' }}>
          Target Job Roles
        </h2>
        <p style={{ color: 'var(--color-slate-500)', marginBottom: '20px', fontSize: '0.95rem' }}>
          Select from specialized role tracks with curated technical problem domains and realistic HR behavioral questions.
        </p>

        <div className="grid-4">
          {roles.map((r, i) => (
            <div key={i} className="card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ fontSize: '2rem', marginBottom: '12px' }}>{r.icon}</div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '8px', color: 'var(--color-navy-900)' }}>
                  {r.title}
                </h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--color-slate-500)', lineHeight: 1.5 }}>
                  {r.desc}
                </p>
              </div>
              <div style={{ marginTop: '16px', display: 'flex', gap: '6px' }}>
                <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>Technical</span>
                <span className="badge badge-blue" style={{ fontSize: '0.7rem' }}>HR</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Multi-Dimensional Scoring Rubric */}
      <div style={{ marginBottom: '40px' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '8px', color: 'var(--color-navy-900)' }}>
          Standardized 10-Point Evaluation Rubric
        </h2>
        <p style={{ color: 'var(--color-slate-500)', marginBottom: '20px', fontSize: '0.95rem' }}>
          Every answer is assessed across four key pillars summing to an objective score out of 10.
        </p>

        <div className="grid-4">
          {pillars.map((p, i) => (
            <div key={i} className="card" style={{ padding: '20px', borderTop: '3px solid var(--color-purple-600)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--color-navy-900)' }}>{p.name}</h4>
                <span className="badge badge-purple">{p.weight}</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--color-slate-500)', lineHeight: 1.5 }}>
                {p.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* How it Works / Workflow */}
      <div className="card" style={{ background: '#FFFFFF', padding: '32px' }}>
        <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '24px', textAlign: 'center', color: 'var(--color-navy-900)' }}>
          How INTERVIEWX Simulates Real Interviews
        </h3>

        <div className="grid-3">
          <div style={{ textAlign: 'center', padding: '12px' }}>
            <div 
              style={{ 
                width: '48px', 
                height: '48px', 
                borderRadius: '50%', 
                background: 'var(--color-purple-100)', 
                color: 'var(--color-purple-700)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                margin: '0 auto 16px auto',
                fontSize: '1.25rem',
                fontWeight: 700
              }}
            >
              1
            </div>
            <h4 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '8px' }}>Configure Your Session</h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--color-slate-500)', lineHeight: 1.5 }}>
              Choose your job role, interview type (Technical or HR), and experience level (Beginner, Mid, Senior).
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '12px' }}>
            <div 
              style={{ 
                width: '48px', 
                height: '48px', 
                borderRadius: '50%', 
                background: 'var(--color-purple-100)', 
                color: 'var(--color-purple-700)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                margin: '0 auto 16px auto',
                fontSize: '1.25rem',
                fontWeight: 700
              }}
            >
              2
            </div>
            <h4 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '8px' }}>Live Interactive Q&A</h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--color-slate-500)', lineHeight: 1.5 }}>
              Type your answers in the simulated room. Receive immediate feedback and tackle adaptive follow-up questions.
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '12px' }}>
            <div 
              style={{ 
                width: '48px', 
                height: '48px', 
                borderRadius: '50%', 
                background: 'var(--color-purple-100)', 
                color: 'var(--color-purple-700)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                margin: '0 auto 16px auto',
                fontSize: '1.25rem',
                fontWeight: 700
              }}
            >
              3
            </div>
            <h4 style={{ fontSize: '1.05rem', fontWeight: 600, marginBottom: '8px' }}>Diagnostic Performance Report</h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--color-slate-500)', lineHeight: 1.5 }}>
              Get a comprehensive breakdown of strengths, weaknesses, and a tailored study roadmap saved to history.
            </p>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '28px' }}>
          <button className="btn btn-primary" onClick={onStartInterview}>
            Launch Your Interview Simulator &rarr;
          </button>
        </div>
      </div>
    </div>
  );
}

