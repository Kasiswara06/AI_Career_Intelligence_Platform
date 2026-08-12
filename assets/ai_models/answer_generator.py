import re
import logging
from ai_assistant.llm_client import generate_llm_response

logger = logging.getLogger(__name__)

def generate_model_answer_package(
    question: str,
    domain: str = "Python Development",
    target_role: str = "Python Developer",
    difficulty: str = "Medium",
    question_type: str = "Technical",
    resume_context: dict = None
) -> dict:
    """
    Generates a complete, interview-ready model answer package for any question:
    - model_answer
    - explanation
    - example
    - key_points (list or markdown bullet points)
    - interview_tip
    """
    q_lower = question.lower()
    
    # 1. Attempt LLM generation first for rich context
    system_prompt = f"""You are an expert technical interviewer and career mentor.
For the question provided, generate a complete interview-ready model answer package for a candidate interviewing for {target_role} in {domain}.

Return a structured JSON object with EXACT keys:
- model_answer (string: complete interview-ready answer)
- explanation (string: simple explanation of the concept)
- example (string: code snippet or practical example with output/complexity if applicable)
- key_points (list of strings: 3-5 concise summary bullet points)
- interview_tip (string: practical advice on how to deliver this answer in an interview)
"""
    user_prompt = f"""
Domain: {domain}
Target Role: {target_role}
Difficulty: {difficulty}
Question Type: {question_type}

Question:
{question}
"""

    llm_resp = generate_llm_response(user_prompt, system_context=system_prompt)
    if llm_resp and llm_resp.get("text"):
        try:
            import json
            raw_text = llm_resp["text"]
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                if parsed.get("model_answer"):
                    return {
                        "model_answer": parsed.get("model_answer", ""),
                        "explanation": parsed.get("explanation", ""),
                        "example": parsed.get("example", ""),
                        "key_points": parsed.get("key_points", []),
                        "interview_tip": parsed.get("interview_tip", "")
                    }
        except Exception as e:
            logger.warning(f"Error parsing LLM model answer package: {e}")

    # 2. Intelligent Deterministic Fallback Generator
    if "list" in q_lower and "tuple" in q_lower:
        return {
            "model_answer": "A list is a mutable collection, meaning its elements can be changed after creation. A tuple is immutable, meaning its elements cannot be changed after creation.",
            "explanation": "Lists allow adding, removing, and modifying elements in-place. Tuples are allocated with fixed memory size at creation, making them faster, hashable, and safer for fixed records.",
            "example": "```python\nmy_list = [1, 2, 3]\nmy_list[0] = 10  # Valid modification\n\nmy_tuple = (1, 2, 3)\n# my_tuple[0] = 10  # Raises TypeError\n```\nThe list can be modified, while the tuple cannot be modified.",
            "key_points": [
                "List → Mutable (can modify elements)",
                "Tuple → Immutable (cannot modify after creation)",
                "Lists use square brackets []",
                "Tuples use parentheses ()"
            ],
            "interview_tip": "Mention mutability and give a short example instead of only giving the definition."
        }

    elif "overfit" in q_lower:
        return {
            "model_answer": "Overfitting occurs when a machine learning model learns the training data too closely, including its noise and unnecessary patterns. As a result, it performs very well on training data but poorly on unseen test data.",
            "explanation": "High variance causes the model to memorize specific training data points rather than generalizing the true underlying data distribution pattern.",
            "example": "```python\n# Detecting Overfitting\ntrain_accuracy = 0.99\ntest_accuracy = 0.65  # Significant gap indicates overfitting!\n```",
            "key_points": [
                "Use cross-validation (K-Fold)",
                "Apply L1/L2 Regularization",
                "Gather more training data or apply data augmentation",
                "Perform feature selection to reduce noise",
                "Apply Dropout for neural networks & prune decision trees"
            ],
            "interview_tip": "Always explain overfitting using the difference between training performance and test performance."
        }

    elif "join" in q_lower:
        return {
            "model_answer": "An INNER JOIN returns only rows that have matching values in both tables. A LEFT JOIN returns all rows from the left table and matching rows from the right table. If no match exists, the right-side columns contain NULL.",
            "explanation": "JOINs combine relational data using primary/foreign keys. INNER JOIN filters out unmatched rows on both sides, while LEFT JOIN preserves all left-hand records.",
            "example": "```sql\nSELECT e.name, d.department_name\nFROM employees e\nLEFT JOIN departments d\nON e.department_id = d.department_id;\n```",
            "key_points": [
                "INNER JOIN → returns only matching records in both tables",
                "LEFT JOIN → returns all left records + matching right records",
                "Unmatched rows in LEFT JOIN yield NULL values for right table columns"
            ],
            "interview_tip": "Draw a mental Venn diagram and mention that LEFT JOIN is ideal when you don't want to lose primary table records."
        }

    elif "tell me about yourself" in q_lower or "about yourself" in q_lower:
        res_skills = ", ".join(resume_context.get("skills", ["Software Development"])[:4]) if resume_context else "software engineering and cloud systems"
        res_edu = resume_context.get("education", "Computer Science") if resume_context else "Computer Science"
        return {
            "model_answer": f"I hold a degree in {res_edu} with strong technical expertise in {res_skills}. In my previous projects, I built end-to-end applications focusing on clean code, performance optimization, and reliable delivery. I am passionate about applying my skills as a {target_role} in the {domain} domain.",
            "explanation": "Structure your response into 3 parts: Present (current skills/role), Past (key project highlights), and Future (why this target role aligns with your career goals).",
            "example": "Elevator Pitch Outline: 'I am a [Target Role] specializing in [Core Skills]. Recently, I built [Key Project] which [Measurable Outcome]. I am excited to bring this expertise to your team.'",
            "key_points": [
                "Keep response between 90 to 120 seconds",
                "Highlight core technical skills and major project wins",
                "Align your closing statement directly with the target job role"
            ],
            "interview_tip": "Avoid repeating your entire resume chronologically. Focus on your strongest skills and most impactful projects."
        }

    elif "star" in q_lower or "challenging" in q_lower or "conflict" in q_lower or "problem you faced" in q_lower:
        return {
            "model_answer": "In a recent project, our production deployment faced an unexpected latency spike under heavy user load (Situation). My task was to isolate the bottleneck and restore latency under 200ms within 2 hours (Task). I profiled database queries, identified missing index lookups, added Redis caching, and reconfigured connection pooling (Action). As a result, response time dropped by 80% and system throughput increased by 3x (Result).",
            "explanation": "Use the STAR framework: Situation sets context, Task defines responsibility, Action details concrete steps, and Result highlights measurable metrics.",
            "example": "STAR Breakdown:\n- Situation: High API latency on peak release\n- Task: Restore latency under SLA limit\n- Action: Added query indexing & Redis caching\n- Result: 80% speedup & zero downtime",
            "key_points": [
                "Situation → Context & background",
                "Task → Objective & responsibility",
                "Action → Specific technical steps YOU took (70% of answer)",
                "Result → Measurable outcome and ROI"
            ],
            "interview_tip": "Always conclude behavioral answers with a quantifiable metric (e.g., 50% performance increase or 10 hours saved per week)."
        }

    elif "largest" in q_lower or "reverse" in q_lower or "code" in q_lower or "coding" in q_lower or question_type.lower() == "coding":
        return {
            "model_answer": "To solve this problem efficiently, iterate through the dataset or use optimized built-in functions while tracking maximum/pointer values.",
            "explanation": "Use a single pass approach to achieve linear time complexity O(N) with O(1) auxiliary space.",
            "example": "```python\ndef find_largest(numbers):\n    if not numbers:\n        return None\n    largest = numbers[0]\n    for num in numbers:\n        if num > largest:\n            largest = num\n    return largest\n\n# Example Usage:\nnumbers = [10, 25, 7, 40, 15]\nprint(find_largest(numbers))  # Output: 40\n```\nApproach: Single-pass linear scan.\nTime Complexity: O(N)\nSpace Complexity: O(1)",
            "key_points": [
                "Approach: Single pass iteration",
                "Time Complexity: O(N)",
                "Space Complexity: O(1) Auxiliary Space",
                "Edge cases: Empty list or single element list"
            ],
            "interview_tip": "State your time and space complexities explicitly before writing code."
        }

    # General Fallback Answer Package
    return {
        "model_answer": f"For '{question}', provide a structured technical definition, explain why this concept matters in {domain}, describe how you implement it as a {target_role}, and highlight key trade-offs.",
        "explanation": f"This question tests core domain knowledge in {domain} and practical problem-solving as a {target_role}.",
        "example": f"```python\n# Implementation pattern for {domain}\ndef demonstrate_concept():\n    # Process data and handle trade-offs\n    return 'Concept applied successfully'\n```",
        "key_points": [
            f"Core principle in {domain}",
            "Implementation best practices",
            "Performance and trade-off considerations"
        ],
        "interview_tip": "Structure your response into 3 parts: Definition, Practical Example, and Performance Trade-offs."
    }
