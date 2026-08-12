from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class InterviewQuestion:
    id: Optional[int]
    job_role: str
    difficulty: str # 'Easy', 'Medium', 'Hard'
    question: str
    expected_answer_keywords: List[str] = field(default_factory=list)
    category: str = "Technical"
