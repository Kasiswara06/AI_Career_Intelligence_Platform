-- DDL for interview_question_bank table
CREATE TABLE IF NOT EXISTS interview_question_bank (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    domain TEXT NOT NULL,
    target_role TEXT NOT NULL,
    question_type TEXT DEFAULT 'Technical',
    difficulty TEXT DEFAULT 'Medium',
    question TEXT NOT NULL,
    model_answer TEXT NOT NULL,
    explanation TEXT,
    example TEXT,
    key_points TEXT,
    interview_tip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
