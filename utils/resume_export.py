import os
import logging
from services.resume_export_service import generate_resume_pdf, export_all_resume_formats
from utils.docx_generator import generate_resume_docx
from resume_builder.resume_formatter import format_resume_as_plain_text

logger = logging.getLogger(__name__)

def export_resume_all_formats(user_id: int, version: int, resume_dict: dict) -> dict:
    """
    Exports PDF, DOCX, and TXT files for the resume version (Section 16 requirement).
    Returns filepaths and formatted plain text string for easy copying.
    """
    return export_all_resume_formats(user_id, version, resume_dict)


def get_copyable_resume_text(resume_dict: dict) -> str:
    """
    Returns clean plain text resume content formatted for 1-click clipboard copying.
    """
    return format_resume_as_plain_text(resume_dict)
