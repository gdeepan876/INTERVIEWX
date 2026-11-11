"""
SQLAlchemy ORM Data Models for INTERVIEWX.
Defines tables for sessions, questions, answers, evaluations, and reports.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    role = Column(String(50), nullable=False)                 # Java, Python, Frontend, Backend
    interview_type = Column(String(30), nullable=False)       # Technical, HR
    difficulty = Column(String(20), nullable=False)           # Beginner, Intermediate, Advanced
    status = Column(String(20), default="in_progress")       # in_progress, completed, abandoned
    created_at = Column(DateTime, default=get_utc_now)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    questions = relationship("Question", back_populates="interview", cascade="all, delete-orphan", order_by="Question.question_order")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete-orphan")
    final_report = relationship("FinalReport", back_populates="interview", uselist=False, cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    question_order = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), default="primary")     # primary, follow_up
    topic_category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    interview = relationship("Interview", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    answer_text = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False, default=0)
    submitted_at = Column(DateTime, default=get_utc_now)

    # Relationships
    question = relationship("Question", back_populates="answers")
    interview = relationship("Interview", back_populates="answers")
    evaluation = relationship("Evaluation", back_populates="answer", uselist=False, cascade="all, delete-orphan")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    answer_id = Column(String(36), ForeignKey("answers.id", ondelete="CASCADE"), unique=True, nullable=False)
    score_total = Column(Float, nullable=False)               # 0.0 to 10.0
    score_correctness = Column(Float, nullable=False)         # 0.0 to 2.5
    score_relevance = Column(Float, nullable=False)           # 0.0 to 2.5
    score_clarity = Column(Float, nullable=False)             # 0.0 to 2.5
    score_depth = Column(Float, nullable=False)               # 0.0 to 2.5
    feedback_summary = Column(Text, nullable=False)
    suggestions = Column(Text, nullable=False)
    follow_up_needed = Column(Boolean, default=False)
    evaluated_at = Column(DateTime, default=get_utc_now)

    # Relationships
    answer = relationship("Answer", back_populates="evaluation")


class FinalReport(Base):
    __tablename__ = "final_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), unique=True, nullable=False)
    overall_score = Column(Float, nullable=False)             # Average 0.0 to 10.0
    performance_summary = Column(Text, nullable=False)
    strengths_json = Column(Text, nullable=False)             # JSON list string
    weaknesses_json = Column(Text, nullable=False)            # JSON list string
    recommendations_json = Column(Text, nullable=False)       # JSON list string
    generated_at = Column(DateTime, default=get_utc_now)

    # Relationships
    interview = relationship("Interview", back_populates="final_report")

