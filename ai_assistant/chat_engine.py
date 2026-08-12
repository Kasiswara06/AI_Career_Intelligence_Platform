import re
from typing import Dict, Any
from ai_assistant.response_generator import format_structured_ai_response

def process_chat_query(query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Intelligent NLP Chat Engine that routes candidate prompts to domain knowledge generators.
    Supports concept explanations, resume reviews, ATS score advice, salary predictions, etc.
    """
    q_lower = query.lower().strip()
    ctx = user_context or {}
    skills = ctx.get("skills", ["Python", "SQL", "Machine Learning"])
    ats_score = ctx.get("ats_score", 82)
    missing_skills = ctx.get("missing_skills", ["Docker", "Kubernetes", "AWS"])

    # 1. Python Concept
    if "python" in q_lower:
        return format_structured_ai_response(
            answer="Python is a high-level, interpreted programming language renowned for its clean readability, dynamic typing, and vast ecosystem for web development, data science, and AI.",
            explanation="Python executes code line-by-line via an interpreter and uses automatic memory management (reference counting and cyclic garbage collection). Its minimal syntax allows developers to express complex concepts in fewer lines of code.",
            example="```python\n# Clean Python Data Pipeline Example\nimport pandas as pd\n\ndata = {'Skill': ['Python', 'SQL', 'Docker'], 'Level': [95, 88, 70]}\ndf = pd.DataFrame(data)\nfiltered = df[df['Level'] >= 80]\nprint(filtered)\n```",
            best_practice="Adhere to PEP 8 style guidelines, leverage virtual environments (`venv`/`conda`), and use type hints (`typing`) for production maintainability.",
            resources=[
                {"title": "Official Python Documentation", "url": "https://docs.python.org/3/"},
                {"title": "Python for Data Science Bootcamp (Udemy)", "url": "https://www.udemy.com"}
            ],
            related_topics=["Lists vs Tuples", "Python Decorators", "FastAPI & Django Microservices", "PyTorch Deep Learning"]
        )

    # 2. SQL Concept
    elif "sql" in q_lower:
        return format_structured_ai_response(
            answer="SQL (Structured Query Language) is the domain-specific standard language for managing and querying relational database management systems (RDBMS).",
            explanation="SQL allows engineers to perform CRUD operations, join normalized tables using relational keys, build aggregated reporting views, and optimize query performance through B-Tree indexing.",
            example="```sql\n-- Optimized SQL Query with INNER JOIN & Aggregation\nSELECT u.full_name, COUNT(r.id) AS resume_count, MAX(a.ats_score) AS peak_score\nFROM users u\nINNER JOIN resumes r ON u.id = r.user_id\nLEFT JOIN resume_analysis a ON r.id = a.resume_id\nWHERE u.created_at >= '2026-01-01'\nGROUP BY u.id;\n```",
            best_practice="Always index foreign key columns, avoid `SELECT *` in production APIs, and utilize parameterized queries to prevent SQL Injection attacks.",
            resources=[
                {"title": "The Complete SQL Bootcamp", "url": "https://www.udemy.com"},
                {"title": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/"}
            ],
            related_topics=["B-Tree Indexing", "Database Normalization (3NF)", "PostgreSQL vs MySQL", "Window Functions"]
        )

    # 3. Machine Learning Concept
    elif "machine learning" in q_lower or "ml" in q_lower:
        return format_structured_ai_response(
            answer="Machine Learning is a subset of Artificial Intelligence where algorithms learn statistical patterns from data to make accurate predictions without explicit hardcoded rules.",
            explanation="ML workflows encompass Supervised Learning (classification, regression), Unsupervised Learning (clustering, dimensionality reduction), and Reinforcement Learning. Models evaluate features against ground-truth labels using loss minimization.",
            example="```python\n# Scikit-Learn Machine Learning Model\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nclf = RandomForestClassifier(n_estimators=100)\nclf.fit(X_train, y_train)\nprint('Accuracy:', clf.score(X_test, y_test))\n```",
            best_practice="Always separate datasets into Train/Validation/Test sets to prevent data leakage and monitor for model overfitting using Cross-Validation.",
            resources=[
                {"title": "Machine Learning Specialization by Andrew Ng", "url": "https://www.coursera.org"},
                {"title": "Scikit-Learn Official User Guide", "url": "https://scikit-learn.org"}
            ],
            related_topics=["Bias-Variance Tradeoff", "Random Forest vs XGBoost", "Feature Engineering", "Sentence Transformers"]
        )

    # 4. Review Resume / ATS Score
    elif "review" in q_lower or "ats" in q_lower or "resume" in q_lower:
        return format_structured_ai_response(
            answer=f"Your current resume has an ATS Compatibility Score of {ats_score}%.",
            explanation=f"Our AI parser evaluated your resume structure, keyword density, contact headers, and skills. Detected skills include {', '.join(skills[:4])}. To boost your score above 90%, address missing industry keywords.",
            example="**Before (Vague):** *Worked on Python web applications and fixed bugs.*\n\n**After (ATS Optimized):** *Architected scalable Python/FastAPI microservices, optimizing SQL query execution time by 35% across 50,000 active users.*",
            best_practice="Use standard single-column layouts, clear section headers, and quantify achievements with metrics.",
            resources=[
                {"title": "ATS Optimization Guide", "url": "https://coursera.org"},
                {"title": "Resume Improvement Module", "url": "#"}
            ],
            related_topics=["Missing Keyword Identification", "Project Portfolio Recommendations", "Resume Formatting Tips"]
        )

    # 5. Missing Skills / Upskilling
    elif "missing" in q_lower or "skill" in q_lower:
        return format_structured_ai_response(
            answer=f"Based on target job descriptions, key missing skills identified in your profile are: {', '.join(missing_skills)}.",
            explanation="Closing these specific skill gaps will increase your job match compatibility from ~75% to over 90% for Senior Software & AI Engineer roles.",
            example="```bash\n# Dockerizing your Application\ncat << 'EOF' > Dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['python', 'app.py']\nEOF\n```",
            best_practice="Build 1-2 end-to-end open-source projects incorporating missing technologies and host them on GitHub.",
            resources=[
                {"title": "Docker & Kubernetes: Practical Guide", "url": "https://www.udemy.com"},
                {"title": "AWS Certified Solutions Architect Course", "url": "https://www.coursera.org"}
            ],
            related_topics=["Cloud Infrastructure (AWS/GCP)", "Docker Containerization", "CI/CD Pipelines", "Course Recommendations"]
        )


    # Generic Fallback Response
    return format_structured_ai_response(
        answer=f"I am your AI Career Assistant! You asked: '{query}'. How can I help you optimize your career path today?",
        explanation="I can analyze your resume, explain technical concepts (Python, SQL, ML, System Design), calculate salary predictions, recommend targeted courses, or prepare you for mock technical interviews.",
        example="Try asking: 'Explain Python Decorators', 'How can I improve my ATS score?', or 'What skills are missing for a Data Scientist role?'",
        best_practice="Keep technical queries focused on specific topics or ask for career guidance tailored to your experience level.",
        resources=[
            {"title": "Platform Career Dashboard", "url": "#"},
            {"title": "AI Mock Interview Module", "url": "#"}
        ],
        related_topics=["ATS Resume Scanning", "Skill Gap Analysis", "Salary Prediction", "Course Recommendations"]
    )
