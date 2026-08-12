-- Database table script for salary_prediction module
CREATE TABLE IF NOT EXISTS salary_prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id VARCHAR(100) UNIQUE,
    user_id INT NOT NULL,
    resume_id INT,
    resume_score INT DEFAULT 0,
    ats_score INT DEFAULT 0,
    predicted_salary DECIMAL(10, 2) DEFAULT 0.0,
    minimum_salary DECIMAL(10, 2) DEFAULT 0.0,
    maximum_salary DECIMAL(10, 2) DEFAULT 0.0,
    confidence INT DEFAULT 85,
    experience_level VARCHAR(100) DEFAULT 'Mid-Level',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
