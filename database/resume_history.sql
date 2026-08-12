-- Schema for Resume History Table
-- Compatible with MySQL 8.0+ and SQLite 3.x

CREATE TABLE IF NOT EXISTS resume_history (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    resume_id INT NOT NULL,
    user_id INT NOT NULL,
    version INT NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(255) NOT NULL,
    ats_score INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Archived',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
