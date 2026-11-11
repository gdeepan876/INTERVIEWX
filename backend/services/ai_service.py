"""
Google Gemini AI Service for INTERVIEWX.
Integrates the official google-genai Python SDK to:
1. Generate dynamic interview questions based on role, type, and difficulty.
2. Evaluate candidate answers across 4 core dimensions (Score / 10, Strengths, Weaknesses, Improved Answer).
"""

import json
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

from config import settings

logger = logging.getLogger("interviewx.ai")


def get_genai_client() -> genai.Client:
    """
    Initializes and returns the Gemini API client using the environment API key.
    Raises ValueError if the API key is missing.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured in backend/.env. "
            "Please add your Gemini API key to backend/.env."
        )
    return genai.Client(api_key=api_key)


def generate_ai_interview_questions(
    role: str,
    interview_type: str,
    difficulty: str,
    count: int = 3,
    topic: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generates interview questions using Gemini based on role, interview type, and difficulty.
    Returns a structured list of question objects.
    """
    client = get_genai_client()

    topic_instruction = f" Focus specifically on the topic: '{topic}'." if topic else ""
    
    prompt = f"""
You are an expert Principal Software Engineer and Technical Recruiter conducting an interview.
Generate {count} realistic, insightful interview questions for a candidate applying for the position of:
- Role: {role}
- Interview Type: {interview_type} (Technical or HR/Behavioral)
- Difficulty Level: {difficulty}{topic_instruction}

Guidelines:
- For Technical interviews, focus on core architecture, frameworks, edge cases, trade-offs, and practical debugging scenarios.
- For HR interviews, focus on behavioral scenarios, collaboration, conflict resolution, ownership, and the STAR method.
- Calibrate the question depth strictly for the {difficulty} level.

Return ONLY a valid JSON array of objects. Each object must have:
- "question_text": string (the exact question the interviewer asks)
- "topic_category": string (e.g., 'Concurrency', 'JVM Internals', 'STAR-Teamwork')
- "difficulty": string ('{difficulty}')
- "key_concepts": list of strings (3-4 essential technical concepts or behavioral attributes expected in a strong answer)
- "follow_up_hint": string (a natural follow-up question if the candidate gives a shallow response)
"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.4,
            )
        )

        raw_text = response.text.strip()
        data = json.loads(raw_text)

        # Ensure return is a list
        if isinstance(data, dict):
            # Sometimes models wrap in {"questions": [...]}
            if "questions" in data and isinstance(data["questions"], list):
                return data["questions"]
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError(f"Unexpected JSON format from Gemini: {raw_text[:100]}")

    except Exception as e:
        logger.error(f"Error calling Gemini for question generation: {e}")
        raise RuntimeError(f"Gemini Question Generation failed: {str(e)}")


def evaluate_ai_candidate_answer(
    question_text: str,
    answer_text: str,
    role: str = "Software Engineer",
    difficulty: str = "Intermediate",
    interview_type: str = "Technical"
) -> Dict[str, Any]:
    """
    Evaluates a candidate's answer using Gemini.
    Returns a score out of 10, dimensional breakdown, strengths, weaknesses,
    suggestions, and a production-grade improved answer.
    """
    client = get_genai_client()

    prompt = f"""
You are an authoritative Senior Interviewer and Hiring Committee Member assessing a candidate.
Evaluate the candidate's answer to the interview question below.

Context:
- Role: {role}
- Interview Format: {interview_type}
- Difficulty Level: {difficulty}

Interview Question:
\"\"\"{question_text}\"\"\"

Candidate's Answer:
\"\"\"{answer_text}\"\"\"

Evaluation Criteria (Total Score = 10.0 points):
1. Correctness (0.0 to 2.5 pts): Technical accuracy, factual correctness, appropriate terminology.
2. Relevance (0.0 to 2.5 pts): Direct answering of the prompt without unnecessary filler.
3. Clarity (0.0 to 2.5 pts): Coherence, structure, and professional articulation.
4. Technical Depth (0.0 to 2.5 pts): Explanation of internal mechanisms, trade-offs, edge cases, and best practices.

Return ONLY a valid JSON object matching this schema:
{{
  "score_total": float (sum of the 4 dimensions, 0.0 to 10.0, rounded to 1 decimal),
  "score_correctness": float (0.0 to 2.5),
  "score_relevance": float (0.0 to 2.5),
  "score_clarity": float (0.0 to 2.5),
  "score_depth": float (0.0 to 2.5),
  "feedback_summary": string (2-3 sentences summarizing the candidate's performance),
  "strengths": [list of strings, 2-3 specific strengths noted in the answer],
  "weaknesses": [list of strings, 1-3 specific gaps, inaccuracies, or missed topics],
  "suggestions": string (actionable advice on how the candidate can deliver a better answer),
  "improved_answer": string (an exemplary, production-grade model answer demonstrating how a top candidate would answer this question at the {difficulty} level),
  "follow_up_needed": boolean (true if answer has intriguing claims or gaps requiring a follow-up),
  "follow_up_question": string or null (the follow-up question to probe further, or null if follow_up_needed is false)
}}
"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )

        raw_text = response.text.strip()
        data = json.loads(raw_text)

        # Validate required fields and ensure correct types
        score_total = float(data.get("score_total", 0.0))
        score_total = min(10.0, max(0.0, round(score_total, 1)))

        return {
            "score_total": score_total,
            "score_correctness": round(float(data.get("score_correctness", 0.0)), 1),
            "score_relevance": round(float(data.get("score_relevance", 0.0)), 1),
            "score_clarity": round(float(data.get("score_clarity", 0.0)), 1),
            "score_depth": round(float(data.get("score_depth", 0.0)), 1),
            "feedback_summary": data.get("feedback_summary", "Evaluation complete."),
            "strengths": data.get("strengths", ["Addressed the core question"]),
            "weaknesses": data.get("weaknesses", ["Could provide more technical depth"]),
            "suggestions": data.get("suggestions", "Review core framework concepts and trade-offs."),
            "improved_answer": data.get("improved_answer", "An exemplary answer was not generated."),
            "follow_up_needed": bool(data.get("follow_up_needed", False)),
            "follow_up_question": data.get("follow_up_question"),
            "evaluation_engine": "google-genai",
            "model": settings.GEMINI_MODEL
        }

    except Exception as e:
        logger.error(f"Error calling Gemini for answer evaluation: {e}")
        raise RuntimeError(f"Gemini Answer Evaluation failed: {str(e)}")

