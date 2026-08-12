import re
from ai_models.answer_generator import generate_model_answer_package

def generate_resume_questions(resume_data: dict, domain: str = "Python Development", target_role: str = "Python Developer", count: int = 5) -> list:
    """
    Generates personalized questions AND model answers directly derived from candidate's actual resume content.
    Includes HR ("Tell me about yourself"), Behavioral (STAR method), Coding, and Project-based questions.
    """
    skills = resume_data.get("skills", [])
    projects = resume_data.get("projects", "") or ""
    education = resume_data.get("education", "") or ""
    certifications = resume_data.get("certifications", "") or ""
    experience = resume_data.get("experience", "") or ""

    questions = []

    # 1. HR Question + Model Answer ("Tell me about yourself")
    res_skills_str = ", ".join(skills[:3]) if skills else "Software Engineering"
    questions.append({
        "question": "Tell me about yourself.",
        "category": "HR",
        "question_type": "HR",
        "difficulty": "Easy",
        "domain": domain,
        "role": target_role,
        "model_answer": f"I hold a background in {education if education else 'Computer Science'} with strong technical expertise in {res_skills_str}. In my practical projects and experience ({experience}), I focused on building reliable features and optimizing performance. I am passionate about applying my skills to excel as a {target_role} in the {domain} domain.",
        "explanation": "A great 'Tell me about yourself' answer follows the Present-Past-Future structure: 1) Present role & core skills, 2) Past project/work highlights, and 3) Future career alignment with this role.",
        "example": f"Outline: 'I am a candidate specializing in {res_skills_str}. Recently, I worked on {projects if projects else 'scalable projects'} where I delivered measurable results. I am excited about this {target_role} position because it matches my core technical strengths.'",
        "key_points": [
            "Keep answer between 90-120 seconds",
            f"Highlight top skills ({res_skills_str})",
            "Present -> Past -> Future structure",
            "Align directly with target role requirements"
        ],
        "interview_tip": "Do not repeat your resume line-by-line. Focus on your top technical highlights and career enthusiasm."
    })

    # 2. Project-Based Resume Questions + Answers
    if projects:
        proj_lines = [p.strip() for p in re.split(r'[\n;,•]', str(projects)) if len(p.strip()) > 5]
        for p in proj_lines[:2]:
            questions.append({
                "question": f"Why did you choose your architecture/stack for the '{p}' project and how did you evaluate its performance?",
                "category": "Project-Based",
                "question_type": "Project-Based",
                "difficulty": "Medium",
                "domain": domain,
                "role": target_role,
                "model_answer": f"For '{p}', I evaluated key technical requirements such as latency, scalability, and data volume before selecting our tech stack. I evaluated system performance using quantitative metrics like response latency, prediction precision/recall, and memory consumption under stress testing.",
                "explanation": "Interviewers ask this to test your engineering decision-making, trade-off analysis, and ability to measure results quantitatively.",
                "example": f"Example Answer Structure:\n- Architecture: Layered architecture with API backend and relational/NoSQL storage.\n- Evaluation: Measured query response time (reduced by 40%) and confusion matrix precision/recall.",
                "key_points": [
                    "Explain architectural rationale",
                    "State technical trade-offs evaluated",
                    "Highlight quantitative metrics (latency, precision, throughput)",
                    "Detail your individual contribution"
                ],
                "interview_tip": "Focus 70% of your answer on your specific design choices and concrete metrics."
            })

    # 3. Behavioral STAR Question + Answer
    questions.append({
        "question": "Describe a challenging technical problem you faced in a project and how you resolved it.",
        "category": "Behavioral",
        "question_type": "Behavioral",
        "difficulty": "Hard",
        "domain": domain,
        "role": target_role,
        "model_answer": "Situation: During project release, we encountered unexpected query bottlenecks under load. Task: My responsibility was to identify the root failure and restore latency within SLA. Action: I profiled the application, added database indexing, implemented Redis caching, and optimized API endpoints. Result: Query latency dropped by 75% and throughput doubled.",
        "explanation": "Behavioral questions are best structured using the STAR framework: Situation, Task, Action, and Result.",
        "example": "STAR Breakdown:\n- Situation: Unexpected bottleneck during testing\n- Task: Restore SLA performance within 2 hours\n- Action: Added query indexing & Redis caching\n- Result: 75% speedup & 0 data loss",
        "key_points": [
            "Situation → Set background context",
            "Task → Specify your objective",
            "Action → Describe exact technical steps YOU executed",
            "Result → Deliver quantifiable outcome metrics"
        ],
        "interview_tip": "Always end your STAR response with a clear quantifiable result (e.g. % performance increase)."
    })

    # 4. Coding Question + Answer
    questions.append({
        "question": f"Write a Python program to find the largest number in a list of integers.",
        "category": "Coding",
        "question_type": "Coding",
        "difficulty": "Medium",
        "domain": domain,
        "role": target_role,
        "model_answer": "```python\ndef find_largest(numbers):\n    if not numbers:\n        return None\n    largest = numbers[0]\n    for num in numbers:\n        if num > largest:\n            largest = num\n    return largest\n\n# Example Usage:\nnumbers = [10, 25, 7, 40, 15]\nprint(find_largest(numbers))\n```",
        "explanation": "Iterate through the list maintaining a tracking variable for the maximum element seen so far. `max()` is the Python built-in alternative.",
        "example": "Input: [10, 25, 7, 40, 15]\nOutput: 40\nTime Complexity: O(N)\nSpace Complexity: O(1) Auxiliary Space",
        "key_points": [
            "Single-pass linear scan approach",
            "Time Complexity: O(N)",
            "Space Complexity: O(1) Auxiliary Space",
            "Handles empty list edge cases"
        ],
        "interview_tip": "Mention built-in `max(numbers)` first, then implement the linear loop to demonstrate algorithmic understanding."
    })

    # 5. Skill-Based Resume Questions + Answers
    for skill in skills[:3]:
        s_clean = skill.strip()
        if not s_clean:
            continue
        questions.append({
            "question": f"Your resume mentions experience with {s_clean}. How have you applied {s_clean} in production or complex project scenarios?",
            "category": "Resume Skill",
            "question_type": "Technical",
            "difficulty": "Medium",
            "domain": domain,
            "role": target_role,
            "model_answer": f"I used {s_clean} to implement core features, build scalable data pipelines, and handle asynchronous tasks. By adhering to design patterns and performance optimization guidelines, I ensured high reliability and maintainability.",
            "explanation": f"Demonstrates hands-on mastery of {s_clean} beyond basic syntax knowledge.",
            "example": f"```python\n# Practical usage of {s_clean}\n# Handled data processing and API integration cleanly\n```",
            "key_points": [
                f"Hands-on production usage of {s_clean}",
                "Frameworks & libraries used in tandem",
                "Performance optimization & maintainability"
            ],
            "interview_tip": f"Be ready to mention specific frameworks or libraries you paired with {s_clean}."
        })

    # Ensure all questions have complete answer package
    for q in questions:
        if not q.get("explanation") or not q.get("key_points"):
            pkg = generate_model_answer_package(q["question"], domain=domain, target_role=target_role, difficulty=q.get("difficulty", "Medium"), resume_context=resume_data)
            q["model_answer"] = q.get("model_answer") or pkg["model_answer"]
            q["explanation"] = pkg["explanation"]
            q["example"] = q.get("example") or pkg["example"]
            q["key_points"] = pkg["key_points"]
            q["interview_tip"] = pkg["interview_tip"]

    return questions[:count]
