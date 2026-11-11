/**
 * INTERVIEWX API Client Service.
 * Provides clean asynchronous methods for interacting with the FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    if (response.status === 204) {
      return null;
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMessage = data?.detail || `API request failed with status ${response.status}`;
      throw new ApiError(errorMessage, response.status, data);
    }

    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network or server unreachable error
    throw new ApiError(
      'Cannot connect to the INTERVIEWX backend. Ensure the FastAPI server is running on port 8000.',
      0,
      error
    );
  }
}

export const api = {
  // Check backend server health
  checkHealth() {
    return request('/health');
  },

  // Start a new interview session
  startInterview(role, interviewType, difficulty) {
    return request('/interviews', {
      method: 'POST',
      body: JSON.stringify({
        role,
        interview_type: interviewType,
        difficulty,
      }),
    });
  },

  // Submit candidate answer and receive evaluation + next question
  submitAnswer(interviewId, questionId, answerText) {
    return request(`/interviews/${interviewId}/answers`, {
      method: 'POST',
      body: JSON.stringify({
        question_id: questionId,
        answer_text: answerText,
      }),
    });
  },

  // Conclude interview and generate summary report
  completeInterview(interviewId) {
    return request(`/interviews/${interviewId}/complete`, {
      method: 'POST',
    });
  },

  // Get full diagnostic report with all Q&A reviews
  getReport(interviewId) {
    return request(`/interviews/${interviewId}/report`);
  },

  // Get list of all previous interview sessions
  getHistory() {
    return request('/interviews');
  },

  // Delete an interview record from history
  deleteInterview(interviewId) {
    return request(`/interviews/${interviewId}`, {
      method: 'DELETE',
    });
  },
};

