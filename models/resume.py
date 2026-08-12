from dataclasses import dataclass
from typing import Optional

@dataclass
class Resume:
    id: Optional[int]
    user_id: int
    resume_name: str
    resume_path: str
    file_type: str
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[str] = "0 KB"
    version: int = 1
    resume_score: int = 0
    ats_score: int = 0
    extracted_text: Optional[str] = ""
    is_active: bool = True
    status: str = "Active"
    uploaded_at: Optional[str] = None
    updated_at: Optional[str] = None
