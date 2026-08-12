-- DDL for interview_questions table
CREATE TABLE IF NOT EXISTS interview_questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    user_id INTEGER,
    domain TEXT,
    target_role TEXT,
    role TEXT,
    category TEXT,
    question TEXT NOT NULL,
    question_type TEXT DEFAULT 'Technical',
    difficulty TEXT DEFAULT 'Medium',
    model_answer TEXT NOT NULL,
    explanation TEXT,
    example TEXT,
    key_points TEXT,
    interview_tip TEXT,
    user_answer TEXT,
    user_score INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id) ON DELETE CASCADE
);
