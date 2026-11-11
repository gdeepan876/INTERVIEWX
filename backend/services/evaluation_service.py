"""
Evaluation Engine for INTERVIEWX.
Transparently evaluates candidate responses across 4 core criteria:
1. Correctness (0.0 - 2.5)
2. Relevance (0.0 - 2.5)
3. Clarity (0.0 - 2.5)
4. Technical Depth (0.0 - 2.5)

Note on AI Integration:
In strict compliance with project guidelines, this module operates in
Rule-Based Development Mode until the Google Gemini API is integrated in Phase 4.
It explicitly discloses this in its feedback strings and does not fabricate fake AI claims.
"""

from typing import Dict, Any, Tuple, Optional
from config import settings


def evaluate_candidate_answer(
    question_text: str,
    question_category: Optional[str],
    answer_text: str,
    difficulty: str,
    role: str
) -> Dict[str, Any]:
    """
    Evaluates a candidate's answer.
    Currently uses an objective heuristic rubric measuring length, structural clarity,
    relevance indicators, and technical specificity.
    Discloses that this is Rule-Based Development Mode.
    """
    words = answer_text.strip().split()
    word_count = len(words)
    char_count = len(answer_text.strip())

    # If Gemini LLM is enabled and configured:
    if settings.LLM_ENABLED and settings.GEMINI_API_KEY:
        try:
            from services.ai_service import evaluate_ai_candidate_answer
            ai_eval = evaluate_ai_candidate_answer(
                question_text=question_text,
                answer_text=answer_text,
                role=role,
                difficulty=difficulty,
                interview_type="Technical" if "Technical" in role else "HR"
            )
            return {
                "score_total": ai_eval["score_total"],
                "score_correctness": ai_eval["score_correctness"],
                "score_relevance": ai_eval["score_relevance"],
                "score_clarity": ai_eval["score_clarity"],
                "score_depth": ai_eval["score_depth"],
                "feedback_summary": ai_eval["feedback_summary"],
                "suggestions": ai_eval["suggestions"],
                "improved_answer": ai_eval.get("improved_answer"),
                "strengths": ai_eval.get("strengths", []),
                "weaknesses": ai_eval.get("weaknesses", []),
                "follow_up_needed": ai_eval["follow_up_needed"],
                "follow_up_question": ai_eval.get("follow_up_question"),
                "evaluation_mode": "gemini_ai"
            }
        except Exception as e:
            # Fall back gracefully to heuristic mode if API call fails
            pass

    # Heuristic scoring based on response quality metrics:
    # 1. Relevance: Checks if answer contains substantive words related to question
    relevance_score = 1.0
    question_words = set(w.lower() for w in question_text.split() if len(w) > 3)
    answer_words = set(w.lower() for w in words if len(w) > 3)
    overlap = len(question_words.intersection(answer_words))
    if overlap >= 3:
        relevance_score = 2.5
    elif overlap >= 1:
        relevance_score = 2.0
    else:
        relevance_score = 1.5

    # 2. Clarity: Evaluates sentence structure, punctuation, and length
    clarity_score = 1.0
    has_punctuation = any(p in answer_text for p in [".", ",", ";", ":", "-", "\n"])
    if word_count >= 30 and has_punctuation:
        clarity_score = 2.5
    elif word_count >= 15:
        clarity_score = 2.0
    elif word_count >= 5:
        clarity_score = 1.5
    else:
        clarity_score = 1.0

    # 3. Technical Depth: Calibrated according to difficulty level
    depth_score = 1.0
    target_words = 60 if difficulty == "Advanced" else (40 if difficulty == "Intermediate" else 25)
    
    # Check for technical buzzwords / keywords / structural formatting
    code_or_structure_indicators = ["because", "for example", "trade-off", "specifically", "internally", "however", "therefore", "in contrast", "pattern", "performance"]
    structure_hits = sum(1 for ind in code_or_structure_indicators if ind in answer_text.lower())
    
    if word_count >= target_words and structure_hits >= 2:
        depth_score = 2.5
    elif word_count >= target_words * 0.6:
        depth_score = 2.0
    elif word_count >= 10:
        depth_score = 1.5
    else:
        depth_score = 1.0

    # 4. Correctness: In heuristic mode, combines length and relevance
    correctness_score = round(min(2.5, max(1.0, (relevance_score * 0.6 + depth_score * 0.4))), 1)

    # Composite score calculation (Sum of 4 pillars = 0 to 10)
    score_total = round(correctness_score + relevance_score + clarity_score + depth_score, 1)
    score_total = min(10.0, max(1.0, score_total))

    # Follow-up decision logic:
    # Trigger a follow-up if answer is brief (< 30 words) or moderately scored (< 7.5),
    # encouraging the candidate to defend or deepen their answer.
    follow_up_needed = (word_count < 35 or score_total < 7.5)

    # Transparent, honest feedback formulation
    feedback_intro = "[Development Evaluation Mode - Rule-Based Engine]\n"
    if score_total >= 8.5:
        summary = (
            f"{feedback_intro}Excellent response! Your answer demonstrates thorough understanding of {question_category or 'the topic'} "
            f"with clear articulation ({word_count} words). Your explanation flows logically."
        )
        suggestions = (
            "To make your answer even stronger in a real interview, consider highlighting a production case study, "
            "metrics, or edge-case trade-offs you encountered when applying this concept."
        )
    elif score_total >= 6.5:
        summary = (
            f"{feedback_intro}Solid foundational response. You covered the primary concepts of {question_category or 'the question'}, "
            f"but would benefit from deeper technical specifics and architectural context."
        )
        suggestions = (
            f"Elaborate further on internal mechanisms and contrasting options. For {role} at the {difficulty} level, "
            "interviewers look for explicit explanations of why certain choices are preferred."
        )
    else:
        summary = (
            f"{feedback_intro}Your answer provides a brief starting point, but lacks the necessary depth and structure "
            f"expected for a {difficulty}-level {role} interview."
        )
        suggestions = (
            "Structure your response with clear definitions, concrete examples, and address the 'why' behind the mechanism, "
            "not just the 'what'. Aim for at least 3-4 structured sentences."
        )

    return {
        "score_total": score_total,
        "score_correctness": correctness_score,
        "score_relevance": relevance_score,
        "score_clarity": clarity_score,
        "score_depth": depth_score,
        "feedback_summary": summary,
        "suggestions": suggestions,
        "follow_up_needed": follow_up_needed,
        "evaluation_mode": "rule_based_mock"
    }


def synthesize_final_report(
    evaluations: list,
    role: str,
    difficulty: str,
    interview_type: str
) -> Dict[str, Any]:
    """
    Computes cumulative performance summary, identified strengths,
    growth areas, and recommended next steps based on session evaluations.
    """
    if not evaluations:
        return {
            "overall_score": 0.0,
            "performance_rating": "Incomplete",
            "performance_summary": "Session ended before any evaluations could be processed.",
            "strengths": ["None recorded"],
            "weaknesses": ["Session incomplete"],
            "recommendations": ["Retake the interview to receive a full diagnostic report."],
            "evaluation_mode": "rule_based_mock"
        }

    scores = [e.score_total for e in evaluations]
    overall_score = round(sum(scores) / len(scores), 1)

    avg_correctness = sum(e.score_correctness for e in evaluations) / len(evaluations)
    avg_relevance = sum(e.score_relevance for e in evaluations) / len(evaluations)
    avg_clarity = sum(e.score_clarity for e in evaluations) / len(evaluations)
    avg_depth = sum(e.score_depth for e in evaluations) / len(evaluations)

    strengths = []
    weaknesses = []
    recommendations = []

    # Assess strengths
    if avg_relevance >= 2.0:
        strengths.append(f"Strong topic relevance: Consistently kept answers focused on the core {role} questions.")
    if avg_clarity >= 2.0:
        strengths.append("Clear communication: Expressed thoughts with coherent grammatical structure and flow.")
    if avg_depth >= 2.0:
        strengths.append(f"Good technical depth: Demonstrated sound domain knowledge suited for {difficulty} level.")
    if avg_correctness >= 2.0:
        strengths.append("Accurate fundamental concepts and appropriate technical terminology.")

    if not strengths:
        strengths.append("Demonstrated willingness to tackle all questions and engage in the interview simulation.")

    # Assess weaknesses
    if avg_depth < 2.0:
        weaknesses.append(f"Technical depth: Answers occasionally stayed surface-level without explaining internal mechanisms or trade-offs.")
    if avg_clarity < 2.0:
        weaknesses.append("Conciseness and structure: Answers could be structured more cleanly using frameworks like STAR or bulleted concepts.")
    if avg_relevance < 2.0:
        weaknesses.append("Directness: Some responses took time to address the exact question asked.")

    if not weaknesses:
        weaknesses.append("Minor edge-case coverage: Could expand on performance benchmarks under extreme load.")

    # Generate actionable recommendations
    recommendations.append(f"Review core design patterns, edge cases, and best practices standard for {difficulty} {role} roles.")
    recommendations.append("When answering, first state the direct high-level answer in 1 sentence, then follow with 2-3 supporting technical details or trade-offs.")
    if interview_type == "HR":
        recommendations.append("Apply the STAR method (Situation, Task, Action, Result) rigorously to provide concrete behavioral evidence.")
    else:
        recommendations.append("Practice describing memory models, computational complexity (Big O), and production failure modes.")

    # Performance rating
    if overall_score >= 8.5:
        performance_rating = "Exemplary Candidate (Strong Hire Recommendation)"
    elif overall_score >= 7.0:
        performance_rating = "Proficient Candidate (Hire Recommendation)"
    elif overall_score >= 5.0:
        performance_rating = "Developing Candidate (Potential with Further Study)"
    else:
        performance_rating = "Needs Significant Improvement (Review Core Fundamentals)"

    summary = (
        f"[Development Evaluation Mode - Rule-Based Engine]\n"
        f"The candidate completed a {difficulty}-level {interview_type} interview for the {role} position, "
        f"answering {len(evaluations)} question(s) with an overall average score of {overall_score} / 10.0. "
        f"Performance rating: {performance_rating}."
    )

    return {
        "overall_score": overall_score,
        "performance_rating": performance_rating,
        "performance_summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "evaluation_mode": "rule_based_mock"
    }

