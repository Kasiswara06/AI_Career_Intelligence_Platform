-- DDL for resume_builder table
CREATE TABLE IF NOT EXISTS resume_builder (
    builder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resume_version INT DEFAULT 1,
    target_role TEXT DEFAULT 'AI Engineer',
    template TEXT DEFAULT 'ATS-Friendly',
    summary TEXT,
    skills TEXT,
    education TEXT,
    experience TEXT,
    projects TEXT,
    certifications TEXT,
    achievements TEXT,
    ats_score INT DEFAULT 85,
    file_path_pdf TEXT,
    file_path_docx TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
