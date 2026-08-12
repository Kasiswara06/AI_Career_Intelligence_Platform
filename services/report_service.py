import os
from pathlib import Path
from typing import Dict, Any
from utils.pdf_generator import generate_pdf_report
from config import BASE_DIR

def export_analysis_report(user_name: str, analysis_data: Dict[str, Any], output_format: str = "pdf") -> str:
    """
    Generates and exports comprehensive PDF or HTML analysis reports to reports/ directory.
    """
    output_dir = BASE_DIR / "reports" / output_format.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / f"Career_Report_{user_name.replace(' ', '_')}.pdf"
    generate_pdf_report(user_name, analysis_data, str(file_path))
    return str(file_path)
