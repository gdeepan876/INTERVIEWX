"""
Pydantic Schemas for Request & Response Data Validation.
Enforces type safety and clean JSON serialization across all endpoints.
"""

from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


RoleType = Literal["Java Developer", "Python Developer", "Frontend Developer", "Backend Developer"]
InterviewType = Literal["Technical", "HR"]
DifficultyType = Literal["Beginner", "Intermediate", "Advanced"]


class InterviewCreate(BaseModel):
    role: RoleType = Field(..., description="Target job role")
    interview_type: InterviewType = Field(..., description="Technical or HR interview")
    difficulty: DifficultyType = Field(..., description="Difficulty level")


class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    interview_id: str
    question_order: int
    question_text: str
    question_type: str = Field(..., description="'primary' or 'follow_up'")
    topic_category: Optional[str] = None
    created_at: datetime


class InterviewStartResponse(BaseModel):
    interview_id: str
    role: str
    interview_type: str
    difficulty: str
    status: str
    total_questions_planned: int
    first_question: QuestionOut


class AnswerSubmit(BaseModel):
    question_id: str = Field(..., min_length=1, description="UUID of the question being answered")
    answer_text: str = Field(..., min_length=3, max_length=5000, description="The candidate's text response")

    @field_validator("answer_text")
    def validate_answer(cls, v: str) -> str:
        trimmed = v.strip()
        if len(trimmed) < 3:
            raise ValueError("Answer is too short. Please provide a meaningful response.")
        return trimmed


class EvaluationOut(BaseModel):
    score_total: float
    score_correctness: float
    score_relevance: float
    score_clarity: float
    score_depth: float
    feedback_summary: str
    suggestions: str
    follow_up_needed: bool
    evaluation_mode: str = Field("development_rule_based", description="Identifies evaluation engine")


class AnswerSubmitResponse(BaseModel):
    evaluation: EvaluationOut
    next_action: Literal["next_question", "follow_up", "completed"]
    next_question: Optional[QuestionOut] = None
    current_question_order: int
    total_questions_planned: int


class FinalReportOut(BaseModel):
    id: str
    interview_id: str
    overall_score: float
    performance_rating: str
    performance_summary: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    evaluation_mode: str
    generated_at: datetime


class QuestionDetailReview(BaseModel):
    question_order: int
    question_text: str
    question_type: str
    topic_category: Optional[str]
    candidate_answer: Optional[str]
    score_total: Optional[float]
    feedback_summary: Optional[str]
    suggestions: Optional[str]


class DetailedReportReview(BaseModel):
    report: FinalReportOut
    role: str
    interview_type: str
    difficulty: str
    created_at: datetime
    completed_at: Optional[datetime]
    reviews: List[QuestionDetailReview]


class InterviewHistoryItem(BaseModel):
    id: str
    role: str
    interview_type: str
    difficulty: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    total_questions: int
    overall_score: Optional[float] = None
    has_report: bool


# ============================================================
# Gemini AI Direct Endpoints Schemas
# ============================================================

class AIGenerateQuestionsRequest(BaseModel):
    role: RoleType = Field("Python Developer", description="Target job role")
    interview_type: InterviewType = Field("Technical", description="Technical or HR interview")
    difficulty: DifficultyType = Field("Intermediate", description="Difficulty level")
    count: int = Field(default=3, ge=1, le=10, description="Number of questions to generate (1-10)")
    topic: Optional[str] = Field(None, description="Optional specific topic (e.g. 'Asyncio', 'Spring Boot', 'STAR-Conflict')")


class AIGeneratedQuestionItem(BaseModel):
    question_text: str
    topic_category: str
    difficulty: str
    key_concepts: List[str] = []
    follow_up_hint: Optional[str] = None


class AIGenerateQuestionsResponse(BaseModel):
    role: str
    interview_type: str
    difficulty: str
    questions: List[AIGeneratedQuestionItem]
    generated_by: str = "google-genai"


class AIEvaluateAnswerRequest(BaseModel):
    question_text: str = Field(..., min_length=5, description="The interview question text")
    answer_text: str = Field(..., min_length=3, description="Candidate's text response")
    role: Optional[RoleType] = Field("Python Developer", description="Job role context")
    interview_type: Optional[InterviewType] = Field("Technical", description="Interview format")
    difficulty: Optional[DifficultyType] = Field("Intermediate", description="Experience difficulty level")


class AIEvaluateAnswerResponse(BaseModel):
    score_total: float = Field(..., description="Overall score out of 10.0")
    score_correctness: float = Field(..., description="Correctness sub-score (0.0 to 2.5)")
    score_relevance: float = Field(..., description="Relevance sub-score (0.0 to 2.5)")
    score_clarity: float = Field(..., description="Clarity sub-score (0.0 to 2.5)")
    score_depth: float = Field(..., description="Technical depth sub-score (0.0 to 2.5)")
    feedback_summary: str = Field(..., description="Qualitative feedback summary")
    strengths: List[str] = Field(..., description="Specific strengths demonstrated in the response")
    weaknesses: List[str] = Field(..., description="Identified gaps, inaccuracies, or areas needing depth")
    suggestions: str = Field(..., description="Actionable recommendations for improvement")
    improved_answer: str = Field(..., description="An exemplary, production-grade model answer")
    follow_up_needed: bool = Field(default=False, description="Whether a follow-up probe is warranted")
    follow_up_question: Optional[str] = Field(None, description="Context-aware follow-up question")
    evaluation_engine: str = Field("google-genai", description="Identifies the evaluation engine")
    model: str = Field("models/gemini-3.1-flash-lite", description="Underlying Gemini model utilized")

