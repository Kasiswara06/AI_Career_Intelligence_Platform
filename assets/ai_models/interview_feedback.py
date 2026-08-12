def generate_final_interview_report(
    evaluations: list,
    domain: str,
    target_role: str,
    total_questions: int = 10,
    skipped_count: int = 0
) -> dict:
    """
    Generates comprehensive Final Interview Report after completing mock interview session.
    """
    answered_count = len(evaluations)
    skipped_count = max(skipped_count, total_questions - answered_count)

    if not evaluations:
        return {
            "overall_score": 0,
            "technical_score": 0,
            "communication_score": 0,
            "problem_solving_score": 0,
            "domain_knowledge": 0,
            "resume_knowledge": 0,
            "confidence": 0,
            "questions_answered": 0,
            "questions_skipped": total_questions,
            "strengths": ["Session initiated."],
            "weaknesses": ["No questions answered."],
            "topics_to_improve": [f"Core {domain} fundamentals"],
            "recommended_learning": [f"Review {domain} documentation and standard interview question sets."],
            "interview_readiness": "Needs Practice"
        }

    avg_score_10 = sum(e.get("score_out_of_10", 5) for e in evaluations) / len(evaluations)
    avg_corr_pct = sum(e.get("correctness_pct", 50) for e in evaluations) / len(evaluations)

    overall_score = int(avg_corr_pct * (answered_count / total_questions))
    tech_score = int(min(98, avg_corr_pct + 2))
    comm_score = int(min(95, 75 + (answered_count * 2)))
    prob_score = int(min(95, avg_corr_pct - 3))
    domain_know = int(min(98, avg_corr_pct + 4))
    resume_know = int(min(95, 80 + (answered_count * 1.5)))
    conf_score = int(min(95, 70 + (answered_count * 2.5)))

    # Readiness Classification
    if overall_score >= 80:
        readiness = "🔥 Highly Prepared & Interview Ready"
    elif overall_score >= 60:
        readiness = "🟡 Moderately Prepared (Minor Review Needed)"
    else:
        readiness = "🔴 Needs Practice & Topic Revision"

    strengths = [
        f"Demonstrated clear understanding of core concepts in {domain}.",
        "Good response structure and technical vocabulary."
    ]
    if answered_count >= total_questions * 0.8:
        strengths.append(f"High completion rate ({answered_count}/{total_questions} questions answered).")

    weaknesses = []
    if skipped_count > 0:
        weaknesses.append(f"Skipped {skipped_count} question(s) during the session.")
    if avg_score_10 < 7:
        weaknesses.append("Answers lacked deep architectural trade-offs or practical code examples.")

    topics_to_improve = [
        f"Advanced {domain} optimization techniques",
        f"{target_role} system design and trade-off analysis",
        "STAR method structuring for behavioral and scenario questions"
    ]

    recommended_learning = [
        f"Deep dive into modern {domain} design patterns and production best practices.",
        f"Practice mock coding and scenario questions for {target_role}.",
        "Record and listen to practice answers to improve delivery speed and confidence."
    ]

    return {
        "overall_score": overall_score,
        "technical_score": tech_score,
        "communication_score": comm_score,
        "problem_solving_score": prob_score,
        "domain_knowledge": domain_know,
        "resume_knowledge": resume_know,
        "confidence": conf_score,
        "questions_answered": answered_count,
        "questions_skipped": skipped_count,
        "strengths": strengths,
        "weaknesses": weaknesses if weaknesses else ["Minor timing variations during delivery."],
        "topics_to_improve": topics_to_improve,
        "recommended_learning": recommended_learning,
        "interview_readiness": readiness
    }
