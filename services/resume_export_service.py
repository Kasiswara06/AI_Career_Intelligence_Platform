import os
import logging
from fpdf import FPDF
from utils.docx_generator import generate_resume_docx
from resume_builder.resume_formatter import format_resume_as_plain_text

logger = logging.getLogger(__name__)

class ResumePDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_resume_pdf(resume_dict: dict, output_filepath: str) -> str:
    """
    Generates a clean PDF file using FPDF2.
    """
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    name = resume_dict.get("full_name", "Candidate Name")
    email = resume_dict.get("email", "")
    phone = resume_dict.get("phone", "")
    loc = resume_dict.get("location", "")

    # Header Name
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, name.upper(), ln=True, align="C")

    # Contact line
    contact_parts = [p for p in [email, phone, loc] if p]
    if contact_parts:
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 6, " | ".join(contact_parts), ln=True, align="C")

    # Social links
    link_parts = []
    if resume_dict.get("linkedin"): link_parts.append(f"LinkedIn: {resume_dict['linkedin']}")
    if resume_dict.get("github"): link_parts.append(f"GitHub: {resume_dict['github']}")
    if link_parts:
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 6, " | ".join(link_parts), ln=True, align="C")

    pdf.ln(4)

    def add_pdf_section(title, text):
        if not text or not text.strip():
            return
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(37, 99, 235)
        pdf.cell(0, 8, title.upper(), ln=True)
        
        # Horizontal line
        pdf.set_draw_color(226, 232, 240)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(51, 65, 85)
        for line in text.split("\n"):
            if line.strip():
                # Clean non-latin-1 chars for fpdf std font
                clean_line = line.strip().replace("•", "-").replace("–", "-")
                pdf.multi_cell(0, 5, clean_line)
                pdf.ln(1)
        pdf.ln(3)

    add_pdf_section("Professional Summary", resume_dict.get("summary"))
    add_pdf_section("Technical Skills", resume_dict.get("skills"))
    add_pdf_section("Education", resume_dict.get("education"))
    add_pdf_section("Professional Experience", resume_dict.get("experience"))
    add_pdf_section("Key Projects", resume_dict.get("projects"))
    add_pdf_section("Certifications", resume_dict.get("certifications"))
    add_pdf_section("Achievements", resume_dict.get("achievements"))

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    pdf.output(output_filepath)
    return output_filepath


def export_all_resume_formats(user_id: int, version: int, resume_dict: dict) -> dict:
    """
    Generates and saves PDF, DOCX, and TXT files for a resume version.
    """
    base_dir = os.path.join("generated_resumes")
    pdf_dir = os.path.join(base_dir, "pdf")
    docx_dir = os.path.join(base_dir, "docx")
    txt_dir = os.path.join(base_dir, "txt")

    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(docx_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)

    filename_base = f"resume_user_{user_id}_v{version}"
    pdf_path = os.path.join(pdf_dir, f"{filename_base}.pdf")
    docx_path = os.path.join(docx_dir, f"{filename_base}.docx")
    txt_path = os.path.join(txt_dir, f"{filename_base}.txt")

    # Generate PDF
    try:
        generate_resume_pdf(resume_dict, pdf_path)
    except Exception as e:
        logger.error(f"Error generating PDF resume: {e}")

    # Generate DOCX
    try:
        generate_resume_docx(resume_dict, docx_path)
    except Exception as e:
        logger.error(f"Error generating DOCX resume: {e}")

    # Generate TXT
    plain_txt = format_resume_as_plain_text(resume_dict)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_txt)

    return {
        "pdf_path": pdf_path,
        "docx_path": docx_path,
        "txt_path": txt_path,
        "plain_text": plain_txt
    }
