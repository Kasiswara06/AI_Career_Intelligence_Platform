-- Job Matching history database table schema
CREATE TABLE IF NOT EXISTS job_matching (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER,
    resume_score INTEGER DEFAULT 0,
    ats_score INTEGER DEFAULT 0,
    match_percentage REAL DEFAULT 0.0,
    matching_skills TEXT,
    missing_skills TEXT,
    recommended_skills TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
