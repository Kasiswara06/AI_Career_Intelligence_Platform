import pandas as pd
from typing import List, Dict, Any
from config import COURSES_CSV

DEFAULT_COURSES = [
    {
        "course_title": "Python for Data Science and Machine Learning Bootcamp",
        "skill": "python",
        "platform": "Udemy",
        "duration": "25 hours",
        "link": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/"
    },
    {
        "course_title": "Machine Learning Specialization by Andrew Ng",
        "skill": "machine learning",
        "platform": "Coursera",
        "duration": "3 months",
        "link": "https://www.coursera.org/specializations/machine-learning-introduction"
    },
    {
        "course_title": "Deep Learning Specialization",
        "skill": "deep learning",
        "platform": "Coursera",
        "duration": "4 months",
        "link": "https://www.coursera.org/specializations/deep-learning"
    },
    {
        "course_title": "The Complete SQL Bootcamp",
        "skill": "sql",
        "platform": "Udemy",
        "duration": "9 hours",
        "link": "https://www.udemy.com/course/the-complete-sql-bootcamp/"
    },
    {
        "course_title": "Docker & Kubernetes: The Practical Guide",
        "skill": "docker",
        "platform": "Udemy",
        "duration": "23 hours",
        "link": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"
    },
    {
        "course_title": "React - The Complete Guide (incl Hooks, React Router, Redux)",
        "skill": "react",
        "platform": "Udemy",
        "duration": "48 hours",
        "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
    },
    {
        "course_title": "AWS Certified Solutions Architect Associate",
        "skill": "aws",
        "platform": "A Cloud Guru / Udemy",
        "duration": "27 hours",
        "link": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"
    }
]

def recommend_courses(missing_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Takes a list of missing skills and returns structured course recommendations,
    including platform, duration, links, and learning roadmaps.
    """
    recommended = []
    missing_lower = [s.lower().strip() for s in missing_skills]

    # Try loading from CSV
    courses_db = DEFAULT_COURSES
    if COURSES_CSV.exists():
        try:
            df = pd.read_csv(COURSES_CSV)
            courses_db = df.to_dict('records')
        except Exception:
            pass

    for course in courses_db:
        target_skill = course.get("skill", "").lower()
        if target_skill in missing_lower or any(m in target_skill for m in missing_lower):
            recommended.append({
                "course_title": course.get("course_title", course.get("title", "Online Masterclass")),
                "target_skill": target_skill.capitalize(),
                "platform": course.get("platform", "Coursera/Udemy"),
                "duration": course.get("duration", "10-20 hours"),
                "link": course.get("link", "https://coursera.org"),
            })

    # Fallback if no specific matches found
    if not recommended and missing_skills:
        for skill in missing_skills[:4]:
            recommended.append({
                "course_title": f"Mastering {skill.capitalize()} for Industry Standard Projects",
                "target_skill": skill.capitalize(),
                "platform": "Udemy / Coursera",
                "duration": "15 hours",
                "link": f"https://www.google.com/search?q={skill}+online+course"
            })

    return recommended
