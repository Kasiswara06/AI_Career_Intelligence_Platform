-- DDL for interview_preferences table
CREATE TABLE IF NOT EXISTS interview_preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    domain TEXT NOT NULL,
    target_role TEXT NOT NULL,
    experience_level TEXT DEFAULT 'Mid Level',
    difficulty TEXT DEFAULT 'Medium',
    question_type TEXT DEFAULT 'Mixed',
    question_count INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
