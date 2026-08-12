-- Recommended Courses table schema
CREATE TABLE IF NOT EXISTS recommended_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_title VARCHAR(255) NOT NULL,
    platform VARCHAR(100),
    duration VARCHAR(50),
    target_skill VARCHAR(100),
    link VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
