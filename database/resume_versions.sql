-- Schema for resume_versions table
-- Compatible with MySQL 8.0+ and SQLite 3.x

CREATE TABLE IF NOT EXISTS resume_versions (
    version_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    resume_id INT DEFAULT NULL,
    version_name VARCHAR(150) DEFAULT 'Resume Version',
    target_role VARCHAR(150) DEFAULT 'AI Engineer',
    template VARCHAR(100) DEFAULT 'Modern ATS',
    resume_content TEXT,
    summary TEXT,
    skills TEXT,
    education TEXT,
    experience TEXT,
    projects TEXT,
    certifications TEXT,
    achievements TEXT,
    ats_score INT DEFAULT 85,
    is_active BOOLEAN DEFAULT FALSE,
    file_path_pdf VARCHAR(500),
    file_path_docx VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
