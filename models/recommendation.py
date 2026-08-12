from dataclasses import dataclass
from typing import Optional

@dataclass
class Recommendation:
    id: Optional[int]
    user_id: int
    type: str # 'career', 'job', 'course', 'improvement'
    title: str
    details: str
    match_score: float = 0.0
