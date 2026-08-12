from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Job:
    id: Optional[int]
    title: str
    company: str
    location: str
    experience_required: str
    salary_range: str
    description: str
    required_skills: List[str] = field(default_factory=list)
