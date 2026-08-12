from typing import Dict, Any, List

def format_structured_ai_response(
    answer: str,
    explanation: str,
    example: str,
    best_practice: str,
    resources: List[Dict[str, str]],
    related_topics: List[str]
) -> Dict[str, Any]:
    """
    Formats response into the mandatory 6-part AI Assistant structure:
    1. Answer
    2. Explanation
    3. Example
    4. Best Practice
    5. Resources
    6. Related Topics
    """
    return {
        "answer": answer,
        "explanation": explanation,
        "example": example,
        "best_practice": best_practice,
        "resources": resources,
        "related_topics": related_topics
    }
