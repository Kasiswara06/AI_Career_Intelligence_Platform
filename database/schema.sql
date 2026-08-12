-- Master Schema for AI Resume Screening & Career Intelligence Platform
-- Compatible with MySQL 8.0+ and SQLite 3.x

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS login_activity (
    login_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    logout_time DATETIME NULL,
    login_status VARCHAR(50) DEFAULT 'SUCCESS',
    session_id VARCHAR(100),
    ip_address VARCHAR(50) DEFAULT '127.0.0.1',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    pincode VARCHAR(20),
    college VARCHAR(255),
    university VARCHAR(255),
    qualification VARCHAR(100),
    branch VARCHAR(100),
    cgpa DECIMAL(4,2),
    graduation_year INT,
    skills TEXT,
    technical_skills TEXT,
    soft_skills TEXT,
    experience_years DECIMAL(4,1) DEFAULT 0.0,
    current_company VARCHAR(150),
    current_role VARCHAR(150),
    previous_companies TEXT,
    projects TEXT,
    certifications TEXT,
    career_objective TEXT,
    linkedin_url VARCHAR(255),
    github_url VARCHAR(255),
    portfolio_url VARCHAR(255),
    profile_photo VARCHAR(255),
    completion_percentage INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size VARCHAR(50) DEFAULT '0 KB',
    version INT DEFAULT 1,
    resume_score INT DEFAULT 0,
    ats_score INT DEFAULT 0,
    extracted_text LONGTEXT,
    is_active BOOLEAN DEFAULT TRUE,
    status VARCHAR(50) DEFAULT 'Active',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

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


CREATE TABLE IF NOT EXISTS resume_analysis (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    resume_id INT NOT NULL,
    user_id INT NOT NULL,
    resume_score INT DEFAULT 0,
    ats_score INT DEFAULT 0,
    resume_quality VARCHAR(50) DEFAULT 'Good',
    completeness_pct INT DEFAULT 0,
    extracted_skills TEXT,
    extracted_education TEXT,
    extracted_experience TEXT,
    extracted_projects TEXT,
    missing_skills TEXT,
    strengths TEXT,
    weaknesses TEXT,
    improvement_tips TEXT,
    summary TEXT,
    analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) DEFAULT 'Technical',
    proficiency VARCHAR(50) DEFAULT 'Intermediate',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_matching (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT,
    job_title VARCHAR(150),
    company VARCHAR(150),
    match_percentage DECIMAL(5,2) DEFAULT 0.0,
    matching_skills TEXT,
    missing_skills TEXT,
    ats_compatibility INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

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

CREATE TABLE IF NOT EXISTS salary_prediction (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    prediction_id VARCHAR(100),
    user_id INT NOT NULL,
    resume_id INT,
    resume_score INT DEFAULT 0,
    ats_score INT DEFAULT 0,
    predicted_salary DECIMAL(10,2) DEFAULT 0.0,
    minimum_salary DECIMAL(10,2) DEFAULT 0.0,
    maximum_salary DECIMAL(10,2) DEFAULT 0.0,
    confidence INT DEFAULT 85,
    experience_level VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

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

CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    certificate_name VARCHAR(255) NOT NULL,
    issuing_organization VARCHAR(255) NOT NULL,
    issue_date DATE,
    expiry_date DATE,
    credential_id VARCHAR(100),
    credential_url VARCHAR(255),
    certificate_path VARCHAR(500),
    title VARCHAR(255),
    issuer VARCHAR(255),
    file_path VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    job_title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    location VARCHAR(100),
    experience_level VARCHAR(50),
    required_skills TEXT,
    job_description TEXT NOT NULL,
    salary_range VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interview_questions (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    role VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    model_answer TEXT NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'Medium',
    confidence_tips TEXT,
    common_mistakes TEXT,
    time_complexity VARCHAR(50),
    space_complexity VARCHAR(50),
    code_solution TEXT
);

CREATE TABLE IF NOT EXISTS interview_history (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question TEXT NOT NULL,
    category VARCHAR(50),
    user_answer TEXT,
    ai_feedback TEXT,
    score INT DEFAULT 0,
    technical_score INT DEFAULT 0,
    communication_score INT DEFAULT 0,
    confidence_score INT DEFAULT 0,
    interview_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mock_interview (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    target_role VARCHAR(150),
    total_questions INT DEFAULT 0,
    score INT DEFAULT 0,
    completion_time INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    chat_id VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    session_title VARCHAR(255) DEFAULT 'New Chat Session',
    is_favorite BOOLEAN DEFAULT 0,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


