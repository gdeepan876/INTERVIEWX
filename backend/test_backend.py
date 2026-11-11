"""
End-to-End Test Suite for INTERVIEWX Backend.
Directly exercises services, models, evaluation engine, and router handlers.
"""

import sys
import os

# Ensure backend root is in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(backend_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
from database.session import SessionLocal, Base, engine
from schemas.interview import InterviewCreate, AnswerSubmit
from routers.interview_router import (
    create_interview,
    submit_answer,
    complete_interview,
    get_interview_report,
    get_interview_history,
    delete_interview
)


def run_full_verification():
    print("==================================================")
    print("  RUNNING INTERVIEWX BACKEND DIRECT VERIFICATION  ")
    print("==================================================")
    
    # Initialize SQLite tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Start new interview session for Python Developer
        print("\n[Test 1] Starting Python Developer (Technical, Intermediate) Interview...")
        req = InterviewCreate(
            role="Python Developer",
            interview_type="Technical",
            difficulty="Intermediate"
        )
        session = create_interview(request=req, db=db)
        interview_id = session.interview_id
        q1 = session.first_question
        print(f"-> PASSED: Session Created. ID: {interview_id}")
        print(f"   Q1 [{q1.topic_category}]: {q1.question_text}")

        # 2. Submit substantive answer for Q1
        print("\n[Test 2] Submitting Technical Answer for Q1...")
        answer_payload = AnswerSubmit(
            question_id=q1.id,
            answer_text=(
                "Python decorators are callables that accept a function as an argument and extend its behavior "
                "without modifying the original source code. Under the hood, decorators rely on closures and lexical scoping. "
                "When writing decorators with arguments, we define three nested functions: the outer accepts arguments, "
                "the middle accepts the target function, and the inner accepts the runtime arguments. "
                "We use functools.wraps to preserve docstrings and original function metadata."
            )
        )
        ans_res = submit_answer(interview_id=interview_id, payload=answer_payload, db=db)
        ev = ans_res.evaluation
        print(f"-> PASSED: Answer Evaluated. Total Score: {ev.score_total} / 10.0")
        print(f"   Breakdown -> Correctness: {ev.score_correctness} | Relevance: {ev.score_relevance} | Clarity: {ev.score_clarity} | Depth: {ev.score_depth}")
        print(f"   Mode: {ev.evaluation_mode}")
        print(f"   Next Action: {ans_res.next_action}")

        # 3. Answer follow-up or next question
        if ans_res.next_question:
            next_q = ans_res.next_question
            print(f"\n[Test 3] Answering Subsequent Question [{next_q.question_type}]...")
            print(f"   Question: {next_q.question_text}")
            q2_payload = AnswerSubmit(
                question_id=next_q.id,
                answer_text=(
                    "The Global Interpreter Lock (GIL) is a synchronization mechanism in CPython preventing multiple native threads "
                    "from executing Python bytecodes concurrently. This avoids race conditions in memory management (reference counting). "
                    "For I/O-bound tasks, threads release the GIL during network/disk calls, allowing high concurrency. "
                    "For CPU-bound tasks, we use multiprocessing to spawn separate OS processes with dedicated interpreter instances."
                )
            )
            ans2_res = submit_answer(interview_id=interview_id, payload=q2_payload, db=db)
            print(f"-> PASSED: Second Question Evaluated. Score: {ans2_res.evaluation.score_total} / 10.0")

        # 4. Conclude session and generate final report
        print("\n[Test 4] Finalizing Interview & Generating Diagnostic Report...")
        report = complete_interview(interview_id=interview_id, db=db)
        print(f"-> PASSED: Report Generated. Overall Score: {report.overall_score} / 10.0")
        print(f"   Performance Rating: {report.performance_rating}")
        print(f"   Strengths Identified ({len(report.strengths)}): {report.strengths}")
        print(f"   Weaknesses Identified ({len(report.weaknesses)}): {report.weaknesses}")
        print(f"   Recommendations ({len(report.recommendations)}): {report.recommendations}")

        # 5. Fetch detailed review report (question-by-question)
        print("\n[Test 5] Fetching Detailed Report Review...")
        detailed_report = get_interview_report(interview_id=interview_id, db=db)
        print(f"-> PASSED: Retrieved report for {detailed_report.role}. Q&A reviews: {len(detailed_report.reviews)}")
        for r in detailed_report.reviews:
            print(f"   * Q{r.question_order} ({r.question_type}): Score: {r.score_total}/10 | Text: {r.question_text[:60]}...")

        # 6. Check Interview History Listing
        print("\n[Test 6] Fetching Interview History Listing...")
        history = get_interview_history(limit=10, offset=0, db=db)
        print(f"-> PASSED: History contains {len(history)} session(s).")
        assert any(item.id == interview_id for item in history), "Session ID should be in history"

        print("\n==================================================")
        print("  ALL BACKEND INTEGRATION TESTS PASSED 100%!     ")
        print("==================================================")

    finally:
        db.close()


if __name__ == "__main__":
    run_full_verification()
