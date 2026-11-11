"""
Integration test for the new Gemini AI endpoints.
Directly tests:
1. POST /api/interviews/ai/generate-questions
2. POST /api/interviews/ai/evaluate-answer
"""

import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(backend_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from schemas.interview import (
    AIGenerateQuestionsRequest,
    AIEvaluateAnswerRequest
)
from routers.interview_router import (
    generate_questions_with_gemini,
    evaluate_answer_with_gemini
)


def run_gemini_endpoint_tests():
    print("==================================================")
    print("   TESTING GEMINI AI BACKEND API ENDPOINTS        ")
    print("==================================================")

    # 1. Test Question Generation Endpoint
    print("\n[Test 1] POST /api/interviews/ai/generate-questions...")
    q_req = AIGenerateQuestionsRequest(
        role="Java Developer",
        interview_type="Technical",
        difficulty="Intermediate",
        count=2,
        topic="JVM Garbage Collection"
    )
    q_resp = generate_questions_with_gemini(request=q_req)
    assert len(q_resp.questions) >= 1, "Should generate at least 1 question"
    print(f"-> PASSED: Generated {len(q_resp.questions)} question(s) via Gemini!")
    for i, q in enumerate(q_resp.questions, 1):
        print(f"   Q{i} [{q.topic_category}]: {q.question_text}")
        print(f"      Key Concepts: {q.key_concepts}")

    # 2. Test Answer Evaluation Endpoint
    print("\n[Test 2] POST /api/interviews/ai/evaluate-answer...")
    target_q = q_resp.questions[0].question_text
    sample_answer = (
        "Java's Garbage Collector automatically manages memory in the heap by reclaiming memory occupied by "
        "unreachable objects. In the generational hypothesis, memory is divided into Young Generation (Eden, S0, S1) "
        "and Old (Tenured) Generation. New objects start in Eden and survive minor GCs to be promoted to Old. "
        "Collectors like G1GC split the heap into equal regions and collect regions with the most garbage first to minimize pause times."
    )
    eval_req = AIEvaluateAnswerRequest(
        question_text=target_q,
        answer_text=sample_answer,
        role="Java Developer",
        interview_type="Technical",
        difficulty="Intermediate"
    )
    eval_resp = evaluate_answer_with_gemini(request=eval_req)
    assert 0.0 <= eval_resp.score_total <= 10.0, "Score should be between 0 and 10"
    assert len(eval_resp.strengths) > 0, "Should identify strengths"
    assert len(eval_resp.weaknesses) > 0, "Should identify weaknesses or areas for improvement"
    assert len(eval_resp.improved_answer) > 20, "Should provide an improved model answer"

    print(f"-> PASSED: Answer Evaluated by Gemini!")
    print(f"   Total Score: {eval_resp.score_total} / 10.0")
    print(f"   Correctness: {eval_resp.score_correctness} | Relevance: {eval_resp.score_relevance} | Clarity: {eval_resp.score_clarity} | Depth: {eval_resp.score_depth}")
    print(f"   Feedback: {eval_resp.feedback_summary}")
    print(f"   Strengths: {eval_resp.strengths}")
    print(f"   Weaknesses: {eval_resp.weaknesses}")
    print(f"   Suggestions: {eval_resp.suggestions}")
    print(f"\n   --- Improved Model Answer ---\n   {eval_resp.improved_answer}\n")

    print("==================================================")
    print("   ALL GEMINI AI ENDPOINTS VERIFIED & WORKING!    ")
    print("==================================================")


if __name__ == "__main__":
    run_gemini_endpoint_tests()

