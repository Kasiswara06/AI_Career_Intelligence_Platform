-- DDL for saved_interview_questions table
CREATE TABLE IF NOT EXISTS saved_interview_questions (
    saved_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    domain TEXT,
    target_role TEXT,
    model_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
