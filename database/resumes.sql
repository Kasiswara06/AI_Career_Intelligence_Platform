-- Schema for Resumes Table
-- Compatible with MySQL 8.0+ and SQLite 3.x

CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    resume_name VARCHAR(255) NOT NULL,
    resume_path VARCHAR(500) NOT NULL,
    filename VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(50) NOT NULL,
    file_size VARCHAR(50) DEFAULT '0 KB',
    version INT DEFAULT 1,
    resume_score INT DEFAULT 0,
    ats_score INT DEFAULT 0,
    extracted_text LONGTEXT,
    is_active BOOLEAN DEFAULT TRUE,
    status VARCHAR(50) DEFAULT 'Active',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
