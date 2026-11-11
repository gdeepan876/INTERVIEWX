import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import QuestionCard from '../components/QuestionCard';
import FeedbackCard from '../components/FeedbackCard';
import ProgressBar from '../components/ProgressBar';

export default function InterviewRoomPage({ sessionData, onInterviewComplete, onExit }) {
  const [currentQuestion, setCurrentQuestion] = useState(sessionData.first_question);
  const [questionNumber, setQuestionNumber] = useState(1);
  const [answerText, setAnswerText] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [latestEvaluation, setLatestEvaluation] = useState(null);
  const [nextAction, setNextAction] = useState(null);
  const [queuedNextQuestion, setQueuedNextQuestion] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Word and character count
  const words = answerText.trim() ? answerText.trim().split(/\s+/).length : 0;
  const chars = answerText.length;

  const isFollowUp = currentQuestion?.question_type === 'follow_up';

  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    if (!answerText.trim() || answerText.trim().length < 3) {
      setErrorMessage('Please type a substantive answer (at least a few words) before submitting.');
      return;
    }

    setIsEvaluating(true);
    setErrorMessage(null);

    try {
      const response = await api.submitAnswer(
        sessionData.interview_id,
        currentQuestion.id,
        answerText.trim()
      );

      setLatestEvaluation(response.evaluation);
      setNextAction(response.next_action);
      setQueuedNextQuestion(response.next_question);
    } catch (err) {
      setErrorMessage(err.message || 'Error evaluating answer. Please try again.');
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleContinue = async () => {
    if (nextAction === 'completed' || !queuedNextQuestion) {
      // Complete interview and route to report
      setIsEvaluating(true);
      try {
        await api.completeInterview(sessionData.interview_id);
        onInterviewComplete(sessionData.interview_id);
      } catch (err) {
        setErrorMessage('Failed to finalize interview report: ' + err.message);
      } finally {
        setIsEvaluating(false);
      }
    } else {
      // Advance to next question
      setCurrentQuestion(queuedNextQuestion);
      setQuestionNumber((prev) => prev + 1);
      setAnswerText('');
      setLatestEvaluation(null);
      setNextAction(null);
      setQueuedNextQuestion(null);
      setErrorMessage(null);
    }
  };

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto' }}>
      {/* Header bar with Exit button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <span style={{ fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--color-purple-600)', letterSpacing: '0.5px', fontWeight: 700 }}>
            Active Interview Session
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--color-navy-900)' }}>
            {sessionData.role} Simulator
          </h2>
        </div>

        <button 
          className="btn btn-secondary" 
          style={{ fontSize: '0.85rem', padding: '8px 16px' }}
          onClick={() => {
            if (window.confirm('Are you sure you want to exit this interview? Your progress so far is saved in history.')) {
              onExit();
            }
          }}
        >
          Exit Session
        </button>
      </div>

      {/* Progress Bar */}
      <ProgressBar 
        current={questionNumber} 
        total={sessionData.total_questions_planned || 4} 
        isFollowUp={isFollowUp} 
      />

      {/* Question Card */}
      <QuestionCard 
        question={currentQuestion}
        role={sessionData.role}
        difficulty={sessionData.difficulty}
        interviewType={sessionData.interview_type}
      />

      {/* Error message banner */}
      {errorMessage && (
        <div 
          style={{ 
            background: 'var(--color-rose-100)', 
            border: '1px solid var(--color-rose-500)', 
            color: 'var(--color-rose-800)',
            padding: '12px 16px',
            borderRadius: '8px',
            marginTop: '16px',
            fontSize: '0.9rem'
          }}
        >
          {errorMessage}
        </div>
      )}

      {/* Answer Form (Hidden after submission until user clicks continue) */}
      {!latestEvaluation ? (
        <form onSubmit={handleSubmitAnswer} style={{ marginTop: '24px' }}>
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
              <label 
                htmlFor="candidate-answer" 
                style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-navy-900)' }}
              >
                Your Response
              </label>
              <div style={{ fontSize: '0.8rem', color: 'var(--color-slate-500)' }}>
                <span>{words} words</span> &bull; <span>{chars} characters</span>
              </div>
            </div>

            <textarea
              id="candidate-answer"
              rows={8}
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="State your answer clearly. Mention technical concepts, real-world examples, and trade-offs..."
              disabled={isEvaluating}
              style={{
                width: '100%',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--color-slate-300)',
                outline: 'none',
                resize: 'vertical',
                lineHeight: 1.6,
                color: 'var(--color-navy-900)',
                fontSize: '0.95rem',
                transition: 'border-color 0.2s ease',
              }}
              onFocus={(e) => (e.target.style.borderColor = 'var(--color-purple-600)')}
              onBlur={(e) => (e.target.style.borderColor = 'var(--color-slate-300)')}
            />

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', flexWrap: 'wrap', gap: '12px' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--color-slate-400)' }}>
                Tip: Pressing submit will trigger instant evaluation on correctness, relevance, clarity, and depth.
              </span>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={isEvaluating || !answerText.trim()}
                style={{ minWidth: '160px' }}
              >
                {isEvaluating ? 'Evaluating Answer...' : 'Submit Answer \u2192'}
              </button>
            </div>
          </div>
        </form>
      ) : (
        /* Evaluation Feedback Card */
        <FeedbackCard 
          evaluation={latestEvaluation}
          nextAction={nextAction}
          onContinue={handleContinue}
          isLastQuestion={nextAction === 'completed'}
        />
      )}
    </div>
  );
}

