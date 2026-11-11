"""
FastAPI Router for INTERVIEWX.
Exposes REST endpoints for session setup, Q&A progression,
scoring, final reports, and Gemini AI endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.interview import (
    InterviewCreate,
    InterviewStartResponse,
    AnswerSubmit,
    AnswerSubmitResponse,
    FinalReportOut,
    DetailedReportReview,
    InterviewHistoryItem,
    AIGenerateQuestionsRequest,
    AIGenerateQuestionsResponse,
    AIGeneratedQuestionItem,
    AIEvaluateAnswerRequest,
    AIEvaluateAnswerResponse
)
from services import interview_service
from services import ai_service

router = APIRouter(prefix="/api/interviews", tags=["Interviews"])


# ============================================================
# Gemini AI Direct Endpoints
# ============================================================

@router.post(
    "/ai/generate-questions",
    response_model=AIGenerateQuestionsResponse,
    tags=["AI Integration"],
    summary="Generate Dynamic Interview Questions via Gemini"
)
def generate_questions_with_gemini(request: AIGenerateQuestionsRequest):
    """
    Generates tailored technical or HR interview questions using the Google Gemini API
    calibrated to the specified job role, interview type, and difficulty level.
    """
    try:
        raw_questions = ai_service.generate_ai_interview_questions(
            role=request.role,
            interview_type=request.interview_type,
            difficulty=request.difficulty,
            count=request.count,
            topic=request.topic
        )

        formatted_questions = [
            AIGeneratedQuestionItem(
                question_text=q.get("question_text", "No question text generated."),
                topic_category=q.get("topic_category", "General"),
                difficulty=q.get("difficulty", request.difficulty),
                key_concepts=q.get("key_concepts", []),
                follow_up_hint=q.get("follow_up_hint")
            )
            for q in raw_questions
        ]

        return AIGenerateQuestionsResponse(
            role=request.role,
            interview_type=request.interview_type,
            difficulty=request.difficulty,
            questions=formatted_questions,
            generated_by="google-genai"
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini Question Generation error: {str(e)}"
        )


@router.post(
    "/ai/evaluate-answer",
    response_model=AIEvaluateAnswerResponse,
    tags=["AI Integration"],
    summary="Evaluate Candidate Answer via Gemini"
)
def evaluate_answer_with_gemini(request: AIEvaluateAnswerRequest):
    """
    Evaluates a candidate's answer using the Google Gemini API.
    Returns:
    - Composite score out of 10.0 (with 4 sub-scores)
    - Itemized candidate strengths
    - Identified weaknesses & missing concepts
    - Actionable suggestions
    - An exemplary, production-grade improved answer
    """
    try:
        evaluation = ai_service.evaluate_ai_candidate_answer(
            question_text=request.question_text,
            answer_text=request.answer_text,
            role=request.role or "Software Engineer",
            difficulty=request.difficulty or "Intermediate",
            interview_type=request.interview_type or "Technical"
        )

        return AIEvaluateAnswerResponse(
            score_total=evaluation["score_total"],
            score_correctness=evaluation["score_correctness"],
            score_relevance=evaluation["score_relevance"],
            score_clarity=evaluation["score_clarity"],
            score_depth=evaluation["score_depth"],
            feedback_summary=evaluation["feedback_summary"],
            strengths=evaluation["strengths"],
            weaknesses=evaluation["weaknesses"],
            suggestions=evaluation["suggestions"],
            improved_answer=evaluation["improved_answer"],
            follow_up_needed=evaluation.get("follow_up_needed", False),
            follow_up_question=evaluation.get("follow_up_question"),
            evaluation_engine="google-genai",
            model=evaluation.get("model", "gemini")
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini Answer Evaluation error: {str(e)}"
        )


# ============================================================
# Session Management & Standard Q&A Endpoints
# ============================================================

@router.post("", response_model=InterviewStartResponse, status_code=status.HTTP_201_CREATED)
def create_interview(request: InterviewCreate, db: Session = Depends(get_db)):
    """
    Initializes a new interview session.
    Picks the first question based on selected role, type, and difficulty.
    """
    try:
        return interview_service.start_new_interview(db=db, request=request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create interview session: {str(e)}"
        )


@router.get("", response_model=List[InterviewHistoryItem])
def get_interview_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Returns list of all past interviews stored in SQLite, sorted newest first.
    """
    return interview_service.list_interview_history(db=db, limit=limit, offset=offset)


@router.post("/{interview_id}/answers", response_model=AnswerSubmitResponse)
def submit_answer(
    interview_id: str,
    payload: AnswerSubmit,
    db: Session = Depends(get_db)
):
    """
    Submits a candidate's answer for evaluation.
    Returns 4-pillar score breakdown, feedback, and next question or completion signal.
    """
    try:
        return interview_service.submit_answer_and_get_feedback(
            db=db,
            interview_id=interview_id,
            question_id=payload.question_id,
            answer_text=payload.answer_text
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating answer: {str(e)}"
        )


@router.post("/{interview_id}/complete", response_model=FinalReportOut)
def complete_interview(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """
    Concludes an interview session and calculates the final diagnostic report.
    """
    try:
        return interview_service.finalize_interview_and_generate_report(db=db, interview_id=interview_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.get("/{interview_id}/report", response_model=DetailedReportReview)
def get_interview_report(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves the complete report along with question-by-question candidate answers and scores.
    """
    try:
        return interview_service.get_detailed_report_review(db=db, interview_id=interview_id)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching report: {str(e)}"
        )


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(
    interview_id: str,
    db: Session = Depends(get_db)
):
    """
    Deletes an interview session and all its associated questions, answers, and evaluations.
    """
    success = interview_service.delete_interview_session(db=db, interview_id=interview_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
    return None
