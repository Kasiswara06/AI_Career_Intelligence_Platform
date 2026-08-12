import json
import logging
import re
from ai_assistant.llm_client import generate_llm_response
from ai_models.domain_question_generator import get_domain_questions
from ai_models.resume_question_generator import generate_resume_questions
from ai_models.answer_generator import generate_model_answer_package
from ai_models.interview_evaluator import evaluate_user_interview_answer

logger = logging.getLogger(__name__)

INTERVIEW_SYSTEM_PROMPT = """You are an expert technical interviewer and career mentor.

Generate interview questions specifically for the user's selected domain and target job role.

For EVERY question, ALWAYS generate a technically accurate model answer.

Never return only a question.

Personalize questions using the user's resume, skills, projects, education, certifications, and experience when available.

Do not invent information about the user's resume.

For technical questions:
provide a clear model answer, explanation, example, key points, and interview tip.

For coding questions:
provide correct code, explanation, expected output when applicable, and complexity.

For HR questions:
provide a natural, professional model answer personalized to the candidate.

For behavioral questions:
use the STAR format when appropriate.

For resume/project questions:
ask about technologies, architecture, decisions, challenges, results, and improvements actually mentioned in the resume.

Adapt questions and answers to the selected domain, role, difficulty, and question type.

Do not use the same question set for every domain."""


def generate_personalized_interview_questions(
    domain: str,
    target_role: str,
    resume_data: dict = None,
    difficulty: str = "Medium",
    question_type: str = "Mixed",
    count: int = 10
) -> list:
    """
    Generates personalized interview questions AND COMPLETE MODEL ANSWERS based on:
    User Domain + Target Job Role + Resume Skills + Resume Projects + Experience + Education + Selected Difficulty
    """
    resume_info = resume_data or {}
    skills = resume_info.get("skills", [])
    projects = resume_info.get("projects", "")

    # 1. Attempt LLM generation first
    llm_prompt = f"""
Domain: {domain}
Target Role: {target_role}
Difficulty: {difficulty}
Question Type: {question_type}
Number of Questions Needed: {count}

Candidate Resume Context:
- Skills: {', '.join(skills) if skills else 'Software Development'}
- Projects: {projects if projects else 'N/A'}
- Experience: {resume_info.get('experience', 'N/A')}
- Education: {resume_info.get('education', 'N/A')}

Generate a JSON array of {count} objects. Every object MUST contain ALL of these keys:
- question (string)
- category (string: Technical, HR, Behavioral, Coding, Scenario-Based, Project-Based, Resume-Based)
- difficulty (string: Easy, Medium, Hard)
- model_answer (string: complete interview-ready answer)
- explanation (string: simple explanation)
- example (string: code snippet or practical example with output/complexity)
- key_points (array of strings: 3-5 concise bullet points)
- interview_tip (string: practical tip)
"""

    llm_resp = generate_llm_response(llm_prompt, system_context=INTERVIEW_SYSTEM_PROMPT)
    if llm_resp and llm_resp.get("text"):
        try:
            raw_text = llm_resp["text"]
            json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
            if json_match:
                parsed_list = json.loads(json_match.group(0))
                if isinstance(parsed_list, list) and len(parsed_list) > 0:
                    formatted = []
                    for idx, q in enumerate(parsed_list[:count], 1):
                        q_obj = {
                            "question_id": idx,
                            "question": q.get("question", f"Question {idx}"),
                            "domain": domain,
                            "role": target_role,
                            "category": q.get("category", question_type if question_type != "Mixed" else "Technical"),
                            "question_type": q.get("category", "Technical"),
                            "difficulty": q.get("difficulty", difficulty),
                            "model_answer": q.get("model_answer", ""),
                            "explanation": q.get("explanation", ""),
                            "example": q.get("example", ""),
                            "key_points": q.get("key_points", []),
                            "interview_tip": q.get("interview_tip", "")
                        }
                        
                        # Fallback pkg if any missing key
                        if not q_obj["model_answer"] or not q_obj["explanation"]:
                            pkg = generate_model_answer_package(q_obj["question"], domain=domain, target_role=target_role, difficulty=q_obj["difficulty"], resume_context=resume_info)
                            q_obj["model_answer"] = q_obj["model_answer"] or pkg["model_answer"]
                            q_obj["explanation"] = q_obj["explanation"] or pkg["explanation"]
                            q_obj["example"] = q_obj["example"] or pkg["example"]
                            q_obj["key_points"] = q_obj["key_points"] or pkg["key_points"]
                            q_obj["interview_tip"] = q_obj["interview_tip"] or pkg["interview_tip"]

                        formatted.append(q_obj)

                    return formatted
        except Exception as e:
            logger.warning(f"Error parsing LLM personalized questions JSON: {e}")

    # 2. Heuristic Domain + Resume Generator Fallback
    domain_qs = get_domain_questions(domain, target_role, difficulty=difficulty, count=max(count // 2, 3))
    resume_qs = generate_resume_questions(resume_info, domain=domain, target_role=target_role, count=max(count - len(domain_qs), 3))

    combined = domain_qs + resume_qs
    
    if question_type and question_type != "Mixed":
        filtered = [q for q in combined if question_type.lower() in q.get("question_type", "").lower() or question_type.lower() in q.get("category", "").lower()]
        if len(filtered) >= 3:
            combined = filtered

    final_list = []
    for idx, q in enumerate(combined[:count], 1):
        q_copy = dict(q)
        q_copy["question_id"] = idx
        q_copy["domain"] = domain
        q_copy["role"] = target_role

        if not q_copy.get("explanation") or not q_copy.get("key_points"):
            pkg = generate_model_answer_package(q_copy["question"], domain=domain, target_role=target_role, difficulty=q_copy.get("difficulty", "Medium"), resume_context=resume_info)
            q_copy["model_answer"] = q_copy.get("model_answer") or pkg["model_answer"]
            q_copy["explanation"] = pkg["explanation"]
            q_copy["example"] = q_copy.get("example") or pkg["example"]
            q_copy["key_points"] = pkg["key_points"]
            q_copy["interview_tip"] = pkg["interview_tip"]

        final_list.append(q_copy)

    return final_list[:count]


def evaluate_interview_answer(question: str, user_answer: str) -> dict:
    """Wrapper function for evaluation."""
    return evaluate_user_interview_answer(question=question, user_answer=user_answer)

def generate_interview_questions(role: str = "Python Developer", candidate_skills: list = None, difficulty: str = "Medium", count: int = 5) -> list:
    """Wrapper function."""
    domain = "Python Development" if "python" in role.lower() else "Software Development"
    return generate_personalized_interview_questions(
        domain=domain,
        target_role=role,
        resume_data={"skills": candidate_skills if isinstance(candidate_skills, list) else []},
        difficulty=difficulty,
        count=count
    )

def generate_resume_interview_questions(skills_list: list = None, projects_list: list = None) -> list:
    """Wrapper function."""
    return generate_resume_questions(
        resume_data={"skills": skills_list or [], "projects": projects_list or ""},
        domain="Python Development",
        target_role="Python Developer"
    )

def answer_natural_language_question(query: str) -> dict:
    """Natural Language Engine."""
    pkg = generate_model_answer_package(query)
    return {
        "topic": f"Inquiry: '{query[:40]}...'",
        "query": query,
        "correct_answer": pkg["model_answer"],
        "detailed_explanation": pkg["explanation"],
        "simple_explanation": pkg["explanation"],
        "example": pkg["example"],
        "real_world_use_case": f"Applying technical principles in enterprise software development.",
        "best_interview_answer": pkg["model_answer"],
        "common_mistakes": "Giving high-level generic answers without technical details or metrics.",
        "additional_tips": pkg["interview_tip"],
        "related_questions": ["What are key trade-offs?", "How do you test this in production?"]
    }
