-- Schema for Projects Table
-- Compatible with MySQL 8.0+ and SQLite 3.x

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    technologies TEXT,
    project_role VARCHAR(150),
    start_date DATE,
    end_date DATE,
    github_url VARCHAR(255),
    live_demo_url VARCHAR(255),
    project_type VARCHAR(100),
    key_contributions TEXT,
    project_outcome TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
