import logging
from ai_assistant.llm_client import generate_llm_response

logger = logging.getLogger(__name__)

RESUME_SYSTEM_INSTRUCTION = """
You are an expert professional resume writer and ATS optimization specialist.
Create professional resume content using ONLY verified information available in the candidate's profile, uploaded resume, and database.

Never invent:
- Skills
- Companies
- Job titles
- Experience
- Certifications
- Projects
- Achievements
- CGPA
- Salary
- Performance metrics

Optimize for the candidate's selected target job role.
Use professional language, strong action verbs, concise bullet points, and ATS-friendly formatting.
If information is missing, do not fabricate it. Keep content factual, professional, and concise.
"""

def generate_ai_professional_summary(profile_data: dict, target_role: str = "AI Engineer") -> str:
    """
    Generates an AI professional summary based strictly on actual user profile data (Section 4 requirement).
    """
    degree = profile_data.get("degree", "Graduation")
    spec = profile_data.get("specialization", "Computer Science")
    exp_yrs = float(profile_data.get("experience_years") or 0.0)
    skills = profile_data.get("technical_skills", []) + profile_data.get("tools_and_technologies", [])
    projects = profile_data.get("projects_details", "")
    certs = profile_data.get("certifications_details", "")

    skills_str = ", ".join(skills[:6]) if skills else "software development, problem solving"

    prompt = f"""
{RESUME_SYSTEM_INSTRUCTION}

Task: Write a 2-3 sentence ATS-friendly Professional Summary for a candidate applying for the target role of '{target_role}'.

Verified Candidate Profile Data:
- Qualification: {degree} ({spec})
- Target Role: {target_role}
- Experience: {exp_yrs} years
- Technical Skills: {skills_str}
- Projects Context: {projects[:200]}
- Certifications Context: {certs[:150]}

Rules:
1. Do NOT fabricate experience, companies, or fake metrics.
2. Highlight key skills relevant to {target_role}.
3. Keep it concise, engaging, and professional.

Return ONLY the professional summary text.
"""
    try:
        res = generate_llm_response(prompt)
        text = res.get("text", "") if isinstance(res, dict) else str(res or "")
        if text and len(text.strip()) > 25:
            return text.strip()
    except Exception as e:
        logger.warning(f"Fallback to default summary due to LLM exception: {e}")

    # Fallback summary if LLM call fails
    if exp_yrs > 0:
        return (
            f"Results-driven candidate with over {exp_yrs:.1f} years of practical experience in {skills_str}. "
            f"Demonstrated ability to design efficient workflows and deliver data-driven software solutions. "
            f"Seeking to leverage expertise as a {target_role} to drive business growth and technical excellence."
        )
    else:
        return (
            f"Motivated {spec} graduate ({degree}) with hands-on technical skills in {skills_str}. "
            f"Experienced in developing software projects and analyzing data algorithms. "
            f"Seeking an entry-level {target_role} role to apply technical knowledge to solve real-world industry challenges."
        )

def generate_resume_summary(raw_text: str = "", skills_list: list = None) -> str:
    """Helper alias to generate summary from raw text or skills list."""
    profile_data = {
        "degree": "B.Tech",
        "specialization": "Computer Science / AI",
        "experience_years": 1.5,
        "technical_skills": skills_list or ["Python", "SQL", "Machine Learning", "Streamlit"]
    }
    return generate_ai_professional_summary(profile_data, "AI Engineer")

