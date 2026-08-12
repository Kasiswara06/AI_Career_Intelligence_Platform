import logging
from ai_assistant.llm_client import generate_llm_response

logger = logging.getLogger(__name__)

REWRITE_PROMPT_TEMPLATES = {
    "Improve sentence/section": "Improve the flow, readability, and clarity of the following text while keeping all facts identical.",
    "Make it ATS-friendly": "Optimize the following text for ATS parsers by integrating clean structure, standard industry terms, and clear formatting.",
    "Make it more professional": "Rewrite the following text using formal executive tone, clear professional syntax, and industry standard phrasing.",
    "Make it concise": "Condense the following text into punchy, high-impact bullet points without losing any key facts or details.",
    "Add strong action verbs": "Enhance the following resume text by starting every bullet point with powerful action verbs (e.g. Developed, Implemented, Designed, Automated, Engineered, Analyzed)."
}

def ai_rewrite_resume_text(
    original_text: str,
    rewrite_mode: str = "Make it ATS-friendly",
    target_role: str = "AI Engineer",
    section_name: str = "General Section"
) -> str:
    """
    Section 15 AI Rewrite tool.
    Supports 5 custom rewrite modes:
    - Improve sentence/section
    - Make it ATS-friendly
    - Make it more professional
    - Make it concise
    - Add strong action verbs
    Preserves original candidate facts 100% (Section 15 & Section 20 requirement).
    """
    if not original_text or not original_text.strip():
        return original_text

    instruction = REWRITE_PROMPT_TEMPLATES.get(rewrite_mode, REWRITE_PROMPT_TEMPLATES["Make it ATS-friendly"])

    prompt = f"""
You are an expert ATS Resume Editor and Career Strategist.

Target Job Role: {target_role}
Section: {section_name}
Goal: {instruction}

Strict Mandatory Rules:
1. Preserve 100% of factual information (do NOT invent new companies, degrees, dates, metrics, or skills).
2. Maintain clean, ATS-parsed formatting (use standard bullet points where appropriate).
3. Do NOT add conversational meta-text or preambles.

Original Text:
{original_text}

Return ONLY the rewritten, optimized text.
"""
    try:
        res = generate_llm_response(prompt)
        text = res.get("text", "") if isinstance(res, dict) else str(res or "")
        if text and len(text.strip()) > 10:
            return text.strip()
    except Exception as e:
        logger.warning(f"AI section rewrite fallback due to: {e}")

    return original_text


def improve_resume_section_content(section_name: str, current_content: str, target_role: str = "AI Engineer") -> str:
    """Backwards compatibility wrapper for section improver."""
    return ai_rewrite_resume_text(
        original_text=current_content,
        rewrite_mode="Make it ATS-friendly",
        target_role=target_role,
        section_name=section_name
    )
