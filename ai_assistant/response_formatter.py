import re
from typing import Dict, Any

def format_ai_career_response(raw_text: str, question: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures every response follows a structured, informative presentation:
    1. Direct Answer
    2. Detailed Explanation
    3. Code / Practical Example
    4. Best Practice
    5. Interview Tip
    6. Related Topics
    7. Resources
    """
    candidate_name = context_data.get("candidate_name", "Candidate")
    detected_skills = ", ".join(context_data.get("skills", ["Python", "SQL"])[:5])
    missing_skills = context_data.get("missing_skills", "Docker, AWS")

    # If raw_text is supplied from LLM (Gemini / OpenAI / Ollama), use it directly
    if raw_text and len(raw_text.strip()) > 30:
        return {
            "answer": raw_text.strip(),
            "explanation": f"This guidance considers your active resume (`{context_data.get('resume_name', 'Active Resume')}`), ATS score ({context_data.get('ats_score', 85)}%), and current candidate profile.",
            "example": "```python\n# Candidate Career Execution Code\ndef optimize_profile(skills, target_role):\n    return f'Mastering {skills} boosts candidate match score to 90%+'\n```",
            "best_practice": "Maintain standard ATS formatting, quantify project achievements, and align keywords with job postings.",
            "interview_tip": f"Expect technical questions on {detected_skills}. Be prepared to explain architectural trade-offs.",
            "related_topics": ["ATS Optimization", "Skill Gap Analysis", "Mock Interviews", "Salary Negotiation"],
            "resources": [
                {"title": "Platform Skill Gap Audit", "url": "#"},
                {"title": "Technical Career Roadmap", "url": "https://roadmap.sh"}
            ]
        }

    # Deterministic Intelligent Technical & Career Response Engine
    q_lower = question.lower()

    if "python" in q_lower:
        answer = f"**Python** is a high-level, interpreted, dynamically-typed programming language widely used in AI, Data Science, Web Development, and Automation. Based on your profile, Python is a core competency for your career path."
        explanation = "Python features clean syntax, extensive libraries (NumPy, Pandas, PyTorch, Scikit-learn, Streamlit, FastAPI), and strong community support for machine learning pipelines and backend systems."
        example = """```python
# Python List Comprehension & Decorator Example
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_execution
def process_skills(skills_list):
    return [skill.upper() for skill in skills_list]

print(process_skills(["python", "sql", "pytorch"]))
# Output: ['PYTHON', 'SQL', 'PYTORCH']
```"""
        best_practice = "Follow PEP 8 style guidelines, use type hints, write unit tests with pytest, and handle exceptions gracefully using try-except blocks."
        interview_tip = "Be prepared to explain Python memory management, GIL (Global Interpreter Lock), decorators, generators, and mutable vs immutable data types."

    elif "java" in q_lower:
        answer = "**Java** is a robust, object-oriented, cross-platform programming language powered by the JVM (Java Virtual Machine). It is widely used for enterprise backends, Android apps, and distributed systems."
        explanation = "Key Java concepts include Object-Oriented Programming (Abstraction, Encapsulation, Inheritance, Polymorphism), Garbage Collection, Multithreading, and the Spring Boot framework."
        example = """```java
// Java OOP & Stream API Example
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        List<String> skills = List.of("java", "spring", "sql", "docker");
        List<String> upperSkills = skills.stream()
                                         .map(String::toUpperCase)
                                         .collect(Collectors.toList());
        System.out.println(upperSkills);
    }
}
```"""
        best_practice = "Follow standard naming conventions, manage memory with try-with-resources, use Spring Boot dependency injection, and write clean unit tests with JUnit."
        interview_tip = "Prepare to answer questions on JVM memory model (Heap vs Stack), HashMap internal working, String immutability, and multithreading synchronizations."

    elif "sql" in q_lower or "database" in q_lower or "dbms" in q_lower or "join" in q_lower:
        answer = "**SQL (Structured Query Language)** is the standard language for managing relational databases like MySQL and PostgreSQL. SQL queries allow efficient data querying, manipulation, and schema definition."
        explanation = "INNER JOIN returns matching rows from both tables. LEFT JOIN returns all rows from the left table. Subqueries and window functions (e.g. ROW_NUMBER, DENSE_RANK) provide advanced analytical filtering."
        example = """```sql
-- SQL Aggregation & Window Function Example
SELECT 
    user_id,
    full_name,
    COUNT(id) as total_resumes,
    DENSE_RANK() OVER (ORDER BY COUNT(id) DESC) as rank_num
FROM users u
LEFT JOIN resumes r ON u.id = r.user_id
GROUP BY user_id, full_name;
```"""
        best_practice = "Always index foreign keys and frequently queried columns, avoid `SELECT *` in production, and use parameterized queries to prevent SQL injection."
        interview_tip = "Expect questions on SQL JOIN differences, GROUP BY vs HAVING, indexing strategies (B-Tree), ACID properties, and query optimization."

    elif "machine learning" in q_lower or "ml" in q_lower or "data science" in q_lower or "ai" in q_lower:
        answer = "**Machine Learning (ML)** is a subset of AI where systems learn patterns from data to make predictions without explicit programming. Data Science combines statistical analysis, ML algorithms, and domain expertise."
        explanation = "The ML pipeline consists of Data Preprocessing -> Feature Engineering -> Model Selection -> Training -> Evaluation (Accuracy, Precision, Recall, F1) -> Hyperparameter Tuning -> Model Deployment."
        example = """```python
# Scikit-Learn Machine Learning Classifier Example
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, preds):.2%}")
```"""
        best_practice = "Prevent data leakage by splitting train/test sets before feature scaling, handle missing values systematically, and monitor for model drift post-deployment."
        interview_tip = "Be ready to explain Bias-Variance Tradeoff, Precision vs Recall trade-offs, Cross-Validation strategies, and how to fix Overfitting."

    elif "resume" in q_lower or "ats" in q_lower:
        answer = f"Based on your active resume (`{context_data.get('resume_name', 'Active Resume')}`), your **Resume Score is {context_data.get('resume_score', 88)}%** and your **ATS Compatibility Score is {context_data.get('ats_score', 90)}%**."
        explanation = f"Your resume highlights `{detected_skills}`. Adding missing technical skills like `{missing_skills}` and using a clean 1-column layout will increase ATS screening pass rates above 92%."
        example = """```markdown
# Recommended Resume Bullet Point Format (STAR Technique)
• Engineered real-time resume parsing microservice using Python & MySQL, increasing parsing accuracy to 95% and reducing execution time by 40%.
• Implemented automated ATS screening module processing 500+ candidate applications daily.
```"""
        best_practice = "Use standard section headers, start bullet points with strong action verbs (Engineered, Implemented, Optimized), and quantify achievements with metrics."
        interview_tip = "In interview introductions, deliver your 90-second elevator pitch connecting your technical projects to the target role's key requirements."

    elif "salary" in q_lower or "package" in q_lower:
        answer = f"Your estimated market salary potential is **₹ {context_data.get('expected_salary_lpa', 8.5)} LPA** based on your experience level, technical skills, and target job role."
        explanation = f"Your current core skills (`{detected_skills}`) establish a solid foundation. Acquiring high-demand skills like `{missing_skills}` increases market value by +15% to +25%."
        example = """```python
# Market Salary Growth Calculator
def estimate_salary(base_lpa, experience_years, skill_multiplier=1.15):
    return round(base_lpa * (1 + 0.10 * experience_years) * skill_multiplier, 2)

print(f"Estimated Market Range: {estimate_salary(8.0, 2)} LPA")
```"""
        best_practice = "Research industry salary benchmarks (25th to 75th percentiles), highlight deployed projects, and frame salary expectations around proven technical impact."
        interview_tip = "When discussing salary expectations, provide a well-researched target range and emphasize how your skills solve the team's key challenges."

    elif "interview" in q_lower:
        answer = "Technical and behavioral interviews test domain knowledge, problem-solving ability, system design intuition, and communication."
        explanation = "Use the **STAR Method** (Situation, Task, Action, Result) for behavioral questions, and explain trade-offs clearly during technical and coding questions."
        example = """```markdown
# STAR Method Structure for Interviews
• Situation: Team needed automated candidate screening with high accuracy.
• Task: Build scalable MySQL + Python backend for ATS matching.
• Action: Designed parameterized query layer, indexed foreign keys, deployed Streamlit UI.
• Result: Achieved sub-second query latency and 92% matching accuracy.
```"""
        best_practice = "Think out loud during coding rounds, clarify edge cases before coding, and ask insightful questions about engineering culture at the end."
        interview_tip = "Review core data structures, algorithms, SQL queries, system design principles, and your resume projects before the interview."

    elif "project" in q_lower or "github" in q_lower:
        answer = "Adding well-architected projects to your profile demonstrates hands-on implementation capabilities to technical recruiters and hiring managers."
        explanation = "A standout engineering project includes clean modular code, comprehensive README documentation, environment setup instructions, unit tests, and live deployment links."
        example = """```markdown
# Recommended GitHub README Structure
# Project Title: AI Career Intelligence Platform
## Features: Resume Analysis, ATS Matching, AI Assistant, Interview Prep
## Tech Stack: Python, MySQL, Streamlit, Scikit-Learn
## Setup:
1. `pip install -r requirements.txt`
2. `streamlit run app.py`
```"""
        best_practice = "Host code on GitHub with clear commit history, include architecture diagrams, write unit tests, and provide a live demo link."
        interview_tip = "Be prepared to walk through your code step-by-step, explaining why you selected specific libraries, algorithms, or database designs."

    else:
        answer = f"**Query Resolution for '{question}':** To succeed in technical roles, mastering foundational concepts, writing clean code, and building real-world projects are essential."
        explanation = f"Combining your skills in `{detected_skills}` with continuous learning in targeted areas like `{missing_skills}` will enhance your career progression and project readiness."
        example = f"""```python
# Technical Best Practice Example
def execute_technical_workflow(query="{question}"):
    print(f"Executing resolution strategy for: {{query}}")
    return True

execute_technical_workflow()
```"""
        best_practice = "Focus on clean architecture, write self-documenting code with unit tests, and practice continuous learning using official documentation."
        interview_tip = "Structure your responses clearly, communicate your thought process, and ground technical explanations with real-world project examples."

    return {
        "answer": answer,
        "explanation": explanation,
        "example": example,
        "best_practice": best_practice,
        "interview_tip": interview_tip,
        "related_topics": ["Python & Technical Skills", "ATS & Resume Optimization", "Skill Gap Analysis", "Mock Interview Preparation"],
        "resources": [
            {"title": "Platform ATS Resume Review", "url": "#"},
            {"title": "Interactive Interview Preparation", "url": "#"}
        ]
    }

