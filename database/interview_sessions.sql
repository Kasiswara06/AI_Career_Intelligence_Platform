-- DDL for interview_sessions table
CREATE TABLE IF NOT EXISTS interview_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    domain TEXT NOT NULL,
    target_role TEXT NOT NULL,
    difficulty TEXT DEFAULT 'Medium',
    total_questions INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    technical_score INTEGER DEFAULT 0,
    communication_score INTEGER DEFAULT 0,
    readiness_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
