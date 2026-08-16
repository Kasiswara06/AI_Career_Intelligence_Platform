import os
from pathlib import Path
from typing import Dict, Any
from utils.pdf_generator import generate_pdf_report
from config import BASE_DIR

def export_analysis_report(user_name: Any, analysis_data: Dict[str, Any], output_format: str = "pdf") -> str:
    """
    Generates and exports comprehensive PDF or HTML analysis reports to reports/ directory.
    """
    output_dir = BASE_DIR / "reports" / output_format.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if isinstance(user_name, dict):
        user_data = user_name
        name_str = user_data.get("full_name") or user_data.get("user_name") or "Candidate"
    else:
        name_str = str(user_name) if user_name else "Candidate"
        user_data = {
            "full_name": name_str,
            "email": analysis_data.get("email", "N/A"),
            "current_role": analysis_data.get("target_role") or analysis_data.get("recommended_career", "Software Engineer")
        }
        
    file_path = output_dir / f"Career_Report_{name_str.replace(' ', '_')}.pdf"
    generate_pdf_report(user_data, analysis_data, str(file_path))
    return str(file_path)
