import os
from fpdf import FPDF
from pathlib import Path

class CareerReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(99, 102, 241) # Indigo primary
        self.cell(0, 10, "AI Career Intelligence Platform - Summary Report", ln=True, align="C")
        self.set_draw_color(99, 102, 241)
        self.line(10, 22, 200, 22)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(156, 163, 175)
        self.cell(0, 10, f"Page {self.page_no()} | Confidential Career Intelligence Report", align="C")

def generate_pdf_report(user_data: dict, analysis_data: dict, output_path: str) -> str:
    """Generates a styled PDF report for downloadable career analysis."""
    pdf = CareerReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # User Profile Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Candidate Profile Summary", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Full Name: {user_data.get('full_name', 'N/A')}", ln=True)
    pdf.cell(0, 6, f"Email: {user_data.get('email', 'N/A')}", ln=True)
    pdf.cell(0, 6, f"Target Role: {user_data.get('current_role', 'Software Engineer')}", ln=True)
    pdf.ln(4)

    # Scores Section
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "ATS & Resume Evaluation Scores", ln=True)

    pdf.set_font("Helvetica", "", 10)
    ats = analysis_data.get('ats_score', 0)
    score = analysis_data.get('resume_score', 0)
    pdf.cell(0, 6, f"ATS Compatibility Score: {ats} / 100", ln=True)
    pdf.cell(0, 6, f"Overall Resume Quality Score: {score} / 100", ln=True)
    pdf.ln(4)

    # Extracted Skills
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Extracted Skills & Competencies", ln=True)
    pdf.set_font("Helvetica", "", 10)
    skills = analysis_data.get('extracted_skills', 'N/A')
    if isinstance(skills, list):
        skills = ", ".join(skills)
    pdf.multi_cell(0, 6, f"Skills: {skills}")
    pdf.ln(4)

    # Strengths & Weaknesses
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Key Strengths", ln=True)
    pdf.set_font("Helvetica", "", 10)
    strengths = analysis_data.get('strengths', [])
    if isinstance(strengths, list):
        for s in strengths:
            pdf.cell(0, 6, f"- {s}", ln=True)
    else:
        pdf.multi_cell(0, 6, str(strengths))
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Actionable Improvement Recommendations", ln=True)
    pdf.set_font("Helvetica", "", 10)
    tips = analysis_data.get('improvement_tips', [])
    if isinstance(tips, list):
        for t in tips:
            pdf.cell(0, 6, f"- {t}", ln=True)
    else:
        pdf.multi_cell(0, 6, str(tips))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    return output_path
