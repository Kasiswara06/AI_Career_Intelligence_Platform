-- Database table script for chat_history module
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    session_title VARCHAR(255) DEFAULT 'New Chat Session',
    is_favorite BOOLEAN DEFAULT FALSE,
    question LONGTEXT NOT NULL,
    answer LONGTEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
