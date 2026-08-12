import re
import logging
from ai_assistant.llm_client import generate_llm_response

logger = logging.getLogger(__name__)

def evaluate_user_interview_answer(
    question: str,
    user_answer: str,
    domain: str = "Python Development",
    target_role: str = "Python Developer",
    difficulty: str = "Medium",
    model_answer: str = ""
) -> dict:
    """
    Evaluates candidate's answer with LLM / intelligent NLP heuristics.
    Returns:
    - Score (out of 10)
    - Correctness %
    - Technical Accuracy
    - Completeness
    - Communication
    - Better Answer
    - Missing Points
    - Interview Tip
    """
    answer_text = (user_answer or "").strip()
    words = answer_text.split()
    word_count = len(words)

    # Empty or ultra-short answer handler
    if word_count < 5:
        return {
            "score_out_of_10": 2,
            "overall_score_pct": 20,
            "correctness_pct": 15,
            "technical_accuracy": "Needs Improvement",
            "completeness": "Incomplete",
            "communication": "Needs Work",
            "better_answer": model_answer or "Provide a structured explanation covering core definition, practical example, and domain application.",
            "missing_points": ["Core technical definition", "Domain-specific terminology", "Practical code or implementation example", "Trade-offs or performance impact"],
            "interview_tip": "Always elaborate on technical definitions with a concrete example or STAR approach.",
            "feedback": "Answer was too brief. Expand on technical details and include practical examples."
        }

    # Attempt Gemini/LLM evaluation first
    system_prompt = f"""You are an expert technical interviewer evaluating a candidate for the role of {target_role} in the {domain} domain.
Evaluate the candidate's answer strictly and constructively.

Return your evaluation as structured JSON with exact keys:
- score_out_of_10 (integer 1 to 10)
- correctness_pct (integer 1 to 100)
- technical_accuracy ("Excellent", "Good", or "Needs Improvement")
- completeness ("Good", "Moderate", or "Needs Improvement")
- communication ("Good", "Clear", or "Needs Work")
- better_answer (string: an improved, interview-ready answer)
- missing_points (list of strings: points the candidate missed)
- interview_tip (string: short practical tip for the candidate)
"""
    user_prompt = f"""
Domain: {domain}
Target Role: {target_role}
Difficulty: {difficulty}

Question:
{question}

Candidate Answer:
{user_answer}

Expected Model Answer / Key Concepts:
{model_answer}
"""

    llm_resp = generate_llm_response(user_prompt, system_context=system_prompt)
    if llm_resp and llm_resp.get("text"):
        raw_text = llm_resp["text"]
        try:
            import json
            # Extract JSON block if surrounded by ```json ... ```
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                score = parsed.get("score_out_of_10", 7)
                return {
                    "score_out_of_10": score,
                    "overall_score_pct": score * 10,
                    "correctness_pct": parsed.get("correctness_pct", score * 9),
                    "technical_accuracy": parsed.get("technical_accuracy", "Good"),
                    "completeness": parsed.get("completeness", "Good"),
                    "communication": parsed.get("communication", "Good"),
                    "better_answer": parsed.get("better_answer", model_answer),
                    "missing_points": parsed.get("missing_points", ["Specific real-world metrics"]),
                    "interview_tip": parsed.get("interview_tip", "Keep your answer structured and clear."),
                    "feedback": f"Evaluated by {llm_resp.get('provider', 'AI Interviewer')}"
                }
        except Exception as e:
            logger.warning(f"Error parsing LLM response JSON: {e}")

    # Intelligent Heuristic Fallback Evaluation
    tech_terms = ["because", "function", "data", "system", "process", "memory", "method", "class", "result", "example", "performance", "api", "database", "model", "code"]
    hits = sum(1 for w in tech_terms if w in answer_text.lower())
    
    score_10 = min(10, max(4, 5 + (hits // 2) + (1 if word_count > 30 else 0)))
    corr_pct = min(95, score_10 * 9 + 5)
    
    tech_acc = "Excellent" if score_10 >= 8 else ("Good" if score_10 >= 6 else "Needs Improvement")
    comp_val = "Good" if word_count >= 40 else ("Moderate" if word_count >= 20 else "Needs Improvement")
    comm_val = "Good" if answer_text[0].isupper() and word_count >= 25 else "Clear"

    missing = []
    if hits < 3:
        missing.append(f"More domain-specific technical terms related to {domain}")
    if word_count < 35:
        missing.append("Elaboration on real-world use cases or system trade-offs")
    if "star" not in answer_text.lower() and "result" not in answer_text.lower():
        missing.append("Quantifiable outcomes or metrics")

    better = model_answer if model_answer else (
        f"In a {target_role} interview, address '{question}' by stating: "
        f"1) Core technical definition, 2) Practical code or architecture example, and 3) Performance trade-offs or business impact."
    )

    return {
        "score_out_of_10": score_10,
        "overall_score_pct": corr_pct,
        "correctness_pct": corr_pct,
        "technical_accuracy": tech_acc,
        "completeness": comp_val,
        "communication": comm_val,
        "better_answer": better,
        "missing_points": missing if missing else ["Deep architectural trade-offs"],
        "interview_tip": f"For {domain} questions, use structured points and explain trade-offs clearly.",
        "feedback": "Evaluated using Platform Career AI heuristic engine."
    }
