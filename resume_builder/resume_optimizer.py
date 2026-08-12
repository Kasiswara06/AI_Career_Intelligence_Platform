import logging
from ai_assistant.llm_client import generate_llm_response

logger = logging.getLogger(__name__)

def improve_resume_section_content(section_name: str, current_content: str, target_role: str = "AI Engineer") -> str:
    """
    Uses AI to enhance phrasing, action verbs, and impact of a resume section without fabricating fake experience or skills.
    """
    if not current_content or not current_content.strip():
        return current_content

    prompt = f"""
You are an expert ATS Resume Editor and Career Coach.
Optimize the following resume section text for a target role of '{target_role}'.

Rules:
1. Preserve 100% of factual information (do NOT invent new companies, degrees, dates, or skills).
2. Enhance action verbs (e.g., Developed, Designed, Automated, Optimized, Implemented).
3. Use bullet points and clear, professional formatting suitable for ATS parsers.
4. Keep output concise and ready to insert directly into a resume.

Target Role: {target_role}
Section: {section_name}
Original Content:
{current_content}

Return ONLY the improved section text.
"""
    try:
        res = generate_llm_response(prompt)
        improved_text = res.get("text", "") if isinstance(res, dict) else str(res or "")
        if improved_text and len(improved_text.strip()) > 10:
            return improved_text.strip()
    except Exception as e:
        logger.warning(f"AI section improvement fallback due to: {e}")

    return current_content
