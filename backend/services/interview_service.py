"""
Interview Service Orchestrator for INTERVIEWX.
Manages the lifecycle of an interview: initialization, Q&A progression,
adaptive follow-up generation, report generation, and session history.
"""

import json
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.models import Interview, Question, Answer, Evaluation, FinalReport
from services.question_bank import get_curated_questions
from services.evaluation_service import evaluate_candidate_answer, synthesize_final_report
from schemas.interview import (
    InterviewCreate,
    QuestionOut,
    InterviewStartResponse,
    EvaluationOut,
    AnswerSubmitResponse,
    FinalReportOut,
    DetailedReportReview,
    QuestionDetailReview,
    InterviewHistoryItem
)


# Standard number of primary questions per interview session
TOTAL_PRIMARY_QUESTIONS = 4


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def start_new_interview(db: Session, request: InterviewCreate) -> InterviewStartResponse:
    """
    Creates a new interview session in SQLite, loads the curated question pool,
    and stages the first question for the candidate.
    """
    # 1. Create Interview record
    interview = Interview(
        role=request.role,
        interview_type=request.interview_type,
        difficulty=request.difficulty,
        status="in_progress",
        created_at=get_utc_now()
    )
    db.add(interview)
    db.flush()  # Populates interview.id

    # 2. Retrieve curated question pool
    pool = get_curated_questions(request.role, request.interview_type, request.difficulty)
    first_q_data = pool[0] if pool else {
        "text": f"Please introduce yourself and explain your experience with {request.role}.",
        "category": "Introduction",
        "follow_up": "What is the most interesting technical project you have worked on recently?"
    }

    # 3. Create first Question record
    first_question = Question(
        interview_id=interview.id,
        question_order=1,
        question_text=first_q_data["text"],
        question_type="primary",
        topic_category=first_q_data.get("category", "General"),
        created_at=get_utc_now()
    )
    db.add(first_question)
    db.commit()
    db.refresh(interview)
    db.refresh(first_question)

    return InterviewStartResponse(
        interview_id=interview.id,
        role=interview.role,
        interview_type=interview.interview_type,
        difficulty=interview.difficulty,
        status=interview.status,
        total_questions_planned=TOTAL_PRIMARY_QUESTIONS,
        first_question=QuestionOut.model_validate(first_question)
    )


def submit_answer_and_get_feedback(
    db: Session,
    interview_id: str,
    question_id: str,
    answer_text: str
) -> AnswerSubmitResponse:
    """
    Processes candidate answer, persists it, invokes evaluation,
    and dynamically determines if a follow-up or the next primary question is up.
    """
    # 1. Validate interview exists and is active
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError("Interview session not found.")
    if interview.status == "completed":
        raise ValueError("This interview session has already been completed.")

    # 2. Validate question exists
    question = db.query(Question).filter(Question.id == question_id, Question.interview_id == interview_id).first()
    if not question:
        raise ValueError("Question not found for this interview session.")

    # Check if this question was already answered
    existing_answer = db.query(Answer).filter(Answer.question_id == question_id).first()
    if existing_answer:
        raise ValueError("This question has already been answered.")

    # 3. Save Candidate's Answer
    words = answer_text.strip().split()
    answer = Answer(
        question_id=question.id,
        interview_id=interview.id,
        answer_text=answer_text.strip(),
        word_count=len(words),
        submitted_at=get_utc_now()
    )
    db.add(answer)
    db.flush()

    # 4. Evaluate the Answer
    eval_result = evaluate_candidate_answer(
        question_text=question.question_text,
        question_category=question.topic_category,
        answer_text=answer_text.strip(),
        difficulty=interview.difficulty,
        role=interview.role
    )

    evaluation = Evaluation(
        answer_id=answer.id,
        score_total=eval_result["score_total"],
        score_correctness=eval_result["score_correctness"],
        score_relevance=eval_result["score_relevance"],
        score_clarity=eval_result["score_clarity"],
        score_depth=eval_result["score_depth"],
        feedback_summary=eval_result["feedback_summary"],
        suggestions=eval_result["suggestions"],
        follow_up_needed=eval_result["follow_up_needed"],
        evaluated_at=get_utc_now()
    )
    db.add(evaluation)
    db.flush()

    # 5. Determine Next Step (Follow-up vs Next Primary Question vs Completion)
    pool = get_curated_questions(interview.role, interview.interview_type, interview.difficulty)
    all_questions = db.query(Question).filter(Question.interview_id == interview_id).order_by(Question.question_order).all()
    primary_questions_count = sum(1 for q in all_questions if q.question_type == "primary")

    next_action = "next_question"
    next_question_obj: Optional[Question] = None

    # Check if follow-up is triggered (only for primary questions, and maximum 1 follow-up per session to avoid fatigue)
    existing_followups = sum(1 for q in all_questions if q.question_type == "follow_up")
    
    if question.question_type == "primary" and eval_result["follow_up_needed"] and existing_followups < 2:
        # Find follow-up text from pool matching current question index
        current_idx = min(primary_questions_count - 1, len(pool) - 1)
        curated_item = pool[current_idx] if current_idx >= 0 else pool[0]
        follow_up_prompt = curated_item.get("follow_up")
        
        if not follow_up_prompt:
            follow_up_prompt = f"Could you expand on that with a concrete practical example or mention any trade-offs you considered?"

        next_question_obj = Question(
            interview_id=interview.id,
            question_order=len(all_questions) + 1,
            question_text=f"[Follow-up] {follow_up_prompt}",
            question_type="follow_up",
            topic_category=f"{question.topic_category} (Follow-up)",
            created_at=get_utc_now()
        )
        db.add(next_question_obj)
        next_action = "follow_up"
    else:
        # Move to next primary question if limit not reached
        if primary_questions_count < min(TOTAL_PRIMARY_QUESTIONS, len(pool)):
            next_q_data = pool[primary_questions_count]
            next_question_obj = Question(
                interview_id=interview.id,
                question_order=len(all_questions) + 1,
                question_text=next_q_data["text"],
                question_type="primary",
                topic_category=next_q_data.get("category", "General"),
                created_at=get_utc_now()
            )
            db.add(next_question_obj)
            next_action = "next_question"
        else:
            # Interview questions finished
            next_action = "completed"

    db.commit()
    if next_question_obj:
        db.refresh(next_question_obj)

    evaluation_out = EvaluationOut(
        score_total=evaluation.score_total,
        score_correctness=evaluation.score_correctness,
        score_relevance=evaluation.score_relevance,
        score_clarity=evaluation.score_clarity,
        score_depth=evaluation.score_depth,
        feedback_summary=evaluation.feedback_summary,
        suggestions=evaluation.suggestions,
        follow_up_needed=evaluation.follow_up_needed,
        evaluation_mode=eval_result["evaluation_mode"]
    )

    return AnswerSubmitResponse(
        evaluation=evaluation_out,
        next_action=next_action,
        next_question=QuestionOut.model_validate(next_question_obj) if next_question_obj else None,
        current_question_order=question.question_order,
        total_questions_planned=TOTAL_PRIMARY_QUESTIONS
    )


def finalize_interview_and_generate_report(db: Session, interview_id: str) -> FinalReportOut:
    """
    Marks an interview as completed, calculates aggregate metrics across all evaluations,
    persists the final report in SQLite, and returns the report.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError("Interview session not found.")

    # Check if report already exists
    existing_report = db.query(FinalReport).filter(FinalReport.interview_id == interview_id).first()
    if existing_report:
        return FinalReportOut(
            id=existing_report.id,
            interview_id=existing_report.interview_id,
            overall_score=existing_report.overall_score,
            performance_rating="Completed",
            performance_summary=existing_report.performance_summary,
            strengths=json.loads(existing_report.strengths_json),
            weaknesses=json.loads(existing_report.weaknesses_json),
            recommendations=json.loads(existing_report.recommendations_json),
            evaluation_mode="rule_based_mock",
            generated_at=existing_report.generated_at
        )

    # Gather all evaluations for this interview
    answers = db.query(Answer).filter(Answer.interview_id == interview_id).all()
    evaluations = [a.evaluation for a in answers if a.evaluation]

    # Synthesize report data
    report_dict = synthesize_final_report(
        evaluations=evaluations,
        role=interview.role,
        difficulty=interview.difficulty,
        interview_type=interview.interview_type
    )

    now = get_utc_now()
    interview.status = "completed"
    interview.completed_at = now

    report = FinalReport(
        interview_id=interview.id,
        overall_score=report_dict["overall_score"],
        performance_summary=report_dict["performance_summary"],
        strengths_json=json.dumps(report_dict["strengths"]),
        weaknesses_json=json.dumps(report_dict["weaknesses"]),
        recommendations_json=json.dumps(report_dict["recommendations"]),
        generated_at=now
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return FinalReportOut(
        id=report.id,
        interview_id=report.interview_id,
        overall_score=report.overall_score,
        performance_rating=report_dict["performance_rating"],
        performance_summary=report.performance_summary,
        strengths=report_dict["strengths"],
        weaknesses=report_dict["weaknesses"],
        recommendations=report_dict["recommendations"],
        evaluation_mode=report_dict["evaluation_mode"],
        generated_at=report.generated_at
    )


def get_detailed_report_review(db: Session, interview_id: str) -> DetailedReportReview:
    """
    Returns full diagnostic report along with every question, candidate answer,
    and individual score breakdown for in-depth review.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise ValueError("Interview session not found.")

    report = db.query(FinalReport).filter(FinalReport.interview_id == interview_id).first()
    if not report:
        # If report not generated yet, generate it now
        report_out = finalize_interview_and_generate_report(db, interview_id)
    else:
        report_out = FinalReportOut(
            id=report.id,
            interview_id=report.interview_id,
            overall_score=report.overall_score,
            performance_rating="Completed",
            performance_summary=report.performance_summary,
            strengths=json.loads(report.strengths_json),
            weaknesses=json.loads(report.weaknesses_json),
            recommendations=json.loads(report.recommendations_json),
            evaluation_mode="rule_based_mock",
            generated_at=report.generated_at
        )

    questions = db.query(Question).filter(Question.interview_id == interview_id).order_by(Question.question_order).all()
    reviews = []
    for q in questions:
        ans = db.query(Answer).filter(Answer.question_id == q.id).first()
        ev = ans.evaluation if ans else None
        reviews.append(
            QuestionDetailReview(
                question_order=q.question_order,
                question_text=q.question_text,
                question_type=q.question_type,
                topic_category=q.topic_category,
                candidate_answer=ans.answer_text if ans else None,
                score_total=ev.score_total if ev else None,
                feedback_summary=ev.feedback_summary if ev else None,
                suggestions=ev.suggestions if ev else None
            )
        )

    return DetailedReportReview(
        report=report_out,
        role=interview.role,
        interview_type=interview.interview_type,
        difficulty=interview.difficulty,
        created_at=interview.created_at,
        completed_at=interview.completed_at,
        reviews=reviews
    )


def list_interview_history(db: Session, limit: int = 50, offset: int = 0) -> List[InterviewHistoryItem]:
    """
    Retrieves all past interview sessions in chronological order (newest first).
    """
    interviews = db.query(Interview).order_by(desc(Interview.created_at)).offset(offset).limit(limit).all()
    history = []
    for it in interviews:
        q_count = len(it.questions)
        score = it.final_report.overall_score if it.final_report else None
        history.append(
            InterviewHistoryItem(
                id=it.id,
                role=it.role,
                interview_type=it.interview_type,
                difficulty=it.difficulty,
                status=it.status,
                created_at=it.created_at,
                completed_at=it.completed_at,
                total_questions=q_count,
                overall_score=score,
                has_report=it.final_report is not None
            )
        )
    return history


def delete_interview_session(db: Session, interview_id: str) -> bool:
    """
    Permanently removes an interview session and all child records from SQLite.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        return False
    db.delete(interview)
    db.commit()
    return True
