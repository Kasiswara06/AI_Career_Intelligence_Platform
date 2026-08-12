-- Resume Analysis Table DDL
CREATE TABLE IF NOT EXISTS resume_analysis (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    resume_id INT NOT NULL,
    user_id INT NOT NULL,
    resume_score INT DEFAULT 0,
    ats_score INT DEFAULT 0,
    extracted_skills TEXT,
    extracted_education TEXT,
    extracted_experience TEXT,
    extracted_projects TEXT,
    missing_skills TEXT,
    strengths TEXT,
    weaknesses TEXT,
    improvement_tips TEXT,
    summary TEXT,
    analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
