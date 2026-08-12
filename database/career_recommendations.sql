-- Career Recommendations Table DDL
CREATE TABLE IF NOT EXISTS career_recommendations (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    target_role VARCHAR(150),
    current_gap TEXT,
    recommended_skills TEXT,
    recommended_courses TEXT,
    career_roadmap TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
