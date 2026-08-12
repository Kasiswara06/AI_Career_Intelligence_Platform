import sqlite3
import logging
from database.connection import get_connection, close_connection
from config import DB_TYPE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, SQLITE_DB_PATH

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initializes tables and seeds initial data."""
    conn, db_engine = get_connection()
    cursor = conn.cursor()

    if db_engine == "mysql":
        # Create MySQL Tables
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                mobile VARCHAR(20) NOT NULL,
                age INT NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS login_activity (
                login_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                logout_time DATETIME NULL,
                login_status VARCHAR(50) DEFAULT 'SUCCESS',
                session_id VARCHAR(100),
                ip_address VARCHAR(50) DEFAULT '127.0.0.1',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                skill_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) DEFAULT 'Technical',
                proficiency VARCHAR(50) DEFAULT 'Intermediate',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS job_matching (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS salary_prediction (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                resume_id INT,
                predicted_salary DECIMAL(10,2) DEFAULT 0.0,
                min_salary DECIMAL(10,2) DEFAULT 0.0,
                max_salary DECIMAL(10,2) DEFAULT 0.0,
                experience_level VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS certificates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                certificate_name VARCHAR(255),
                issuing_organization VARCHAR(255),
                issue_date DATE,
                expiry_date DATE,
                credential_id VARCHAR(100),
                credential_url VARCHAR(255),
                certificate_path VARCHAR(500),
                title VARCHAR(255),
                issuer VARCHAR(255),
                file_path VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(150) NOT NULL,
                company VARCHAR(150) NOT NULL,
                location VARCHAR(100),
                experience_level VARCHAR(50),
                required_skills TEXT,
                job_description TEXT NOT NULL,
                salary_range VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS career_recommendations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                target_role VARCHAR(150),
                current_gap TEXT,
                recommended_skills TEXT,
                recommended_courses TEXT,
                career_roadmap TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS skill_gap (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                resume_id INT,
                job_id INT,
                matching_skills TEXT,
                missing_skills TEXT,
                skill_match_pct DECIMAL(5,2) DEFAULT 0.0,
                skill_gap_pct DECIMAL(5,2) DEFAULT 0.0,
                career_readiness_score INT DEFAULT 0,
                recommended_skills TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS course_recommendations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_title VARCHAR(255) NOT NULL,
                platform VARCHAR(100),
                target_skill VARCHAR(100),
                difficulty VARCHAR(50),
                duration VARCHAR(50),
                link VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_preferences (
                preference_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE NOT NULL,
                domain VARCHAR(100) NOT NULL,
                target_role VARCHAR(150) NOT NULL,
                experience_level VARCHAR(50) DEFAULT 'Mid Level',
                difficulty VARCHAR(50) DEFAULT 'Medium',
                question_type VARCHAR(50) DEFAULT 'Mixed',
                question_count INT DEFAULT 10,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_question_bank (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                domain VARCHAR(100) NOT NULL,
                target_role VARCHAR(150) NOT NULL,
                question_type VARCHAR(50) DEFAULT 'Technical',
                difficulty VARCHAR(20) DEFAULT 'Medium',
                question TEXT NOT NULL,
                model_answer TEXT NOT NULL,
                explanation TEXT,
                example TEXT,
                key_points TEXT,
                interview_tip TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS saved_interview_questions (
                saved_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                question_id INT NOT NULL,
                question TEXT NOT NULL,
                domain VARCHAR(100),
                target_role VARCHAR(150),
                model_answer TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_builder (
                builder_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                resume_version INT DEFAULT 1,
                target_role VARCHAR(150) DEFAULT 'AI Engineer',
                template VARCHAR(50) DEFAULT 'ATS-Friendly',
                summary TEXT,
                skills TEXT,
                education TEXT,
                experience TEXT,
                projects TEXT,
                certifications TEXT,
                achievements TEXT,
                ats_score INT DEFAULT 85,
                file_path_pdf VARCHAR(500),
                file_path_docx VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_versions (
                version_id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_sessions (
                session_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                domain VARCHAR(100) NOT NULL,
                target_role VARCHAR(150) NOT NULL,
                difficulty VARCHAR(50) DEFAULT 'Medium',
                total_questions INT DEFAULT 0,
                score INT DEFAULT 0,
                technical_score INT DEFAULT 0,
                communication_score INT DEFAULT 0,
                readiness_score INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                id INT,
                session_id INT,
                user_id INT,
                domain VARCHAR(100),
                target_role VARCHAR(150),
                role VARCHAR(150),
                category VARCHAR(50),
                question TEXT NOT NULL,
                question_type VARCHAR(50) DEFAULT 'Technical',
                difficulty VARCHAR(20) DEFAULT 'Medium',
                model_answer TEXT NOT NULL,
                explanation TEXT,
                example TEXT,
                key_points TEXT,
                interview_tip TEXT,
                user_answer TEXT,
                user_score INT DEFAULT 0,
                score INT DEFAULT 0,
                feedback TEXT,
                confidence_tips TEXT,
                common_mistakes TEXT,
                time_complexity VARCHAR(50),
                space_complexity VARCHAR(50),
                code_solution TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
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
            """,
            """
            CREATE TABLE IF NOT EXISTS mock_interview (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                target_role VARCHAR(150),
                total_questions INT DEFAULT 0,
                score INT DEFAULT 0,
                completion_time INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                action VARCHAR(255) NOT NULL,
                details TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
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
            """
        ]
        for q in queries:
            cursor.execute(q)
        conn.commit()
    else:
        # Create SQLite Tables
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                mobile TEXT NOT NULL,
                age INTEGER NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS login_activity (
                login_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                logout_time TIMESTAMP NULL,
                login_status TEXT DEFAULT 'SUCCESS',
                session_id TEXT,
                ip_address TEXT DEFAULT '127.0.0.1',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                date_of_birth TEXT,
                gender TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                pincode TEXT,
                college TEXT,
                university TEXT,
                qualification TEXT,
                branch TEXT,
                cgpa REAL,
                graduation_year INTEGER,
                skills TEXT,
                technical_skills TEXT,
                soft_skills TEXT,
                experience_years REAL DEFAULT 0.0,
                current_company TEXT,
                current_role TEXT,
                previous_companies TEXT,
                projects TEXT,
                certifications TEXT,
                career_objective TEXT,
                linkedin_url TEXT,
                github_url TEXT,
                portfolio_url TEXT,
                profile_photo TEXT,
                completion_percentage INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                extracted_text TEXT,
                is_active BOOLEAN DEFAULT 1,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                resume_score INTEGER DEFAULT 0,
                ats_score INTEGER DEFAULT 0,
                resume_quality TEXT DEFAULT 'Good',
                completeness_pct INTEGER DEFAULT 0,
                extracted_skills TEXT,
                extracted_education TEXT,
                extracted_experience TEXT,
                extracted_projects TEXT,
                missing_skills TEXT,
                strengths TEXT,
                weaknesses TEXT,
                improvement_tips TEXT,
                summary TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill_name TEXT NOT NULL,
                category TEXT DEFAULT 'Technical',
                proficiency TEXT DEFAULT 'Intermediate',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS job_matching (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_id INTEGER,
                job_title TEXT,
                company TEXT,
                match_percentage REAL DEFAULT 0.0,
                matching_skills TEXT,
                missing_skills TEXT,
                ats_compatibility INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS salary_prediction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                resume_id INTEGER,
                predicted_salary REAL DEFAULT 0.0,
                min_salary REAL DEFAULT 0.0,
                max_salary REAL DEFAULT 0.0,
                experience_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project_name TEXT NOT NULL,
                description TEXT NOT NULL,
                technologies TEXT,
                project_role TEXT,
                start_date TEXT,
                end_date TEXT,
                github_url TEXT,
                live_demo_url TEXT,
                project_type TEXT,
                key_contributions TEXT,
                project_outcome TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                certificate_name TEXT,
                issuing_organization TEXT,
                issue_date TEXT,
                expiry_date TEXT,
                credential_id TEXT,
                credential_url TEXT,
                certificate_path TEXT,
                title TEXT,
                issuer TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                experience_level TEXT,
                required_skills TEXT,
                job_description TEXT NOT NULL,
                salary_range TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS career_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_role TEXT,
                current_gap TEXT,
                recommended_skills TEXT,
                recommended_courses TEXT,
                career_roadmap TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS skill_gap (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                resume_id INTEGER,
                job_id INTEGER,
                matching_skills TEXT,
                missing_skills TEXT,
                skill_match_pct REAL DEFAULT 0.0,
                skill_gap_pct REAL DEFAULT 0.0,
                career_readiness_score INTEGER DEFAULT 0,
                recommended_skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS course_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_title TEXT NOT NULL,
                platform TEXT,
                target_skill TEXT,
                difficulty TEXT,
                duration TEXT,
                link TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_preferences (
                preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                domain TEXT NOT NULL,
                target_role TEXT NOT NULL,
                experience_level TEXT DEFAULT 'Mid Level',
                difficulty TEXT DEFAULT 'Medium',
                question_type TEXT DEFAULT 'Mixed',
                question_count INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_question_bank (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                domain TEXT NOT NULL,
                target_role TEXT NOT NULL,
                question_type TEXT DEFAULT 'Technical',
                difficulty TEXT DEFAULT 'Medium',
                question TEXT NOT NULL,
                model_answer TEXT NOT NULL,
                explanation TEXT,
                example TEXT,
                key_points TEXT,
                interview_tip TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS saved_interview_questions (
                saved_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                domain TEXT,
                target_role TEXT,
                model_answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_builder (
                builder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                resume_version INTEGER DEFAULT 1,
                target_role TEXT DEFAULT 'AI Engineer',
                template TEXT DEFAULT 'ATS-Friendly',
                summary TEXT,
                skills TEXT,
                education TEXT,
                experience TEXT,
                projects TEXT,
                certifications TEXT,
                achievements TEXT,
                ats_score INTEGER DEFAULT 85,
                file_path_pdf TEXT,
                file_path_docx TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resume_versions (
                version_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                resume_id INTEGER DEFAULT NULL,
                version_name TEXT DEFAULT 'Resume Version',
                target_role TEXT DEFAULT 'AI Engineer',
                template TEXT DEFAULT 'Modern ATS',
                resume_content TEXT,
                summary TEXT,
                skills TEXT,
                education TEXT,
                experience TEXT,
                projects TEXT,
                certifications TEXT,
                achievements TEXT,
                ats_score INTEGER DEFAULT 85,
                is_active BOOLEAN DEFAULT 0,
                file_path_pdf TEXT,
                file_path_docx TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                domain TEXT NOT NULL,
                target_role TEXT NOT NULL,
                difficulty TEXT DEFAULT 'Medium',
                total_questions INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                technical_score INTEGER DEFAULT 0,
                communication_score INTEGER DEFAULT 0,
                readiness_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                id INTEGER,
                session_id INTEGER,
                user_id INTEGER,
                domain TEXT,
                target_role TEXT,
                role TEXT,
                category TEXT,
                question TEXT NOT NULL,
                question_type TEXT DEFAULT 'Technical',
                difficulty TEXT DEFAULT 'Medium',
                model_answer TEXT NOT NULL,
                explanation TEXT,
                example TEXT,
                key_points TEXT,
                interview_tip TEXT,
                user_answer TEXT,
                user_score INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                feedback TEXT,
                confidence_tips TEXT,
                common_mistakes TEXT,
                time_complexity TEXT,
                space_complexity TEXT,
                code_solution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS interview_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                category TEXT,
                user_answer TEXT,
                ai_feedback TEXT,
                score INTEGER DEFAULT 0,
                technical_score INTEGER DEFAULT 0,
                communication_score INTEGER DEFAULT 0,
                confidence_score INTEGER DEFAULT 0,
                interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS mock_interview (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_role TEXT,
                total_questions INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                completion_time INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                session_id TEXT NOT NULL,
                session_title TEXT DEFAULT 'New Chat Session',
                is_favorite BOOLEAN DEFAULT 0,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        ]
        for q in queries:
            cursor.execute(q)
        conn.commit()

    # Column migration safety check for users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user'")
        conn.commit()
    except Exception:
        pass

    # Column migration safety check for profiles table
    new_cols = [
        ("pincode", "TEXT"),
        ("technical_skills", "TEXT"),
        ("soft_skills", "TEXT"),
        ("career_objective", "TEXT")
    ]
    for col_name, col_type in new_cols:
        try:
            cursor.execute(f"ALTER TABLE profiles ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except Exception:
            pass

    # Column migration safety check for interview_preferences table
    try:
        cursor.execute("ALTER TABLE interview_preferences ADD COLUMN experience_level TEXT DEFAULT 'Mid Level'")
        conn.commit()
    except Exception:
        pass

    # Column migration safety check for salary_prediction table
    sal_cols = [
        ("prediction_id", "TEXT"),
        ("resume_score", "INTEGER DEFAULT 0"),
        ("ats_score", "INTEGER DEFAULT 0"),
        ("minimum_salary", "REAL DEFAULT 0.0"),
        ("maximum_salary", "REAL DEFAULT 0.0"),
        ("confidence", "INTEGER DEFAULT 85")
    ]
    for col_name, col_type in sal_cols:
        try:
            cursor.execute(f"ALTER TABLE salary_prediction ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except Exception:
            pass

    # Column migration safety check for interview_questions table
    iq_cols = [
        ("question_id", "INTEGER"),
        ("session_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("domain", "TEXT"),
        ("target_role", "TEXT"),
        ("question_type", "TEXT DEFAULT 'Technical'"),
        ("model_answer", "TEXT"),
        ("explanation", "TEXT"),
        ("example", "TEXT"),
        ("key_points", "TEXT"),
        ("interview_tip", "TEXT"),
        ("user_answer", "TEXT"),
        ("user_score", "INTEGER DEFAULT 0"),
        ("score", "INTEGER DEFAULT 0"),
        ("feedback", "TEXT"),
        ("created_at", "TIMESTAMP")
    ]
    for col_name, col_type in iq_cols:
        try:
            cursor.execute(f"ALTER TABLE interview_questions ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except Exception:
            pass

    # Column migration safety check for users table
    user_migration_cols = [
        ("full_name", "VARCHAR(100)"),
        ("password_hash", "VARCHAR(255)"),
        ("mobile", "VARCHAR(20)"),
        ("age", "INT DEFAULT 22"),
        ("role", "VARCHAR(50) DEFAULT 'user'")
    ]
    for col_name, col_type in user_migration_cols:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except Exception:
            pass

    # Synchronize fullname/full_name and password/password_hash if needed
    try:
        cursor.execute("UPDATE users SET full_name = fullname WHERE (full_name IS NULL OR full_name = '') AND fullname IS NOT NULL")
        conn.commit()
    except Exception:
        pass

    try:
        cursor.execute("UPDATE users SET password_hash = password WHERE (password_hash IS NULL OR password_hash = '') AND password IS NOT NULL")
        conn.commit()
    except Exception:
        pass

    # Column migration safety check for certificates table
    cert_migration_cols = [
        ("user_id", "INT"),
        ("certificate_name", "VARCHAR(255)"),
        ("issuing_organization", "VARCHAR(255)"),
        ("issue_date", "DATE"),
        ("expiry_date", "DATE"),
        ("credential_id", "VARCHAR(100)"),
        ("credential_url", "VARCHAR(255)"),
        ("certificate_path", "VARCHAR(500)"),
        ("title", "VARCHAR(255)"),
        ("issuer", "VARCHAR(255)"),
        ("file_path", "VARCHAR(500)")
    ]
    for col_name, col_type in cert_migration_cols:
        try:
            cursor.execute(f"ALTER TABLE certificates ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except Exception:
            pass

    # Column migration safety check for resumes table
    res_migration_cols = [
        ("user_id", "INT"),
        ("filename", "VARCHAR(255)"),
        ("file_path", "VARCHAR(500)"),
        ("file_type", "VARCHAR(50) DEFAULT '.pdf'"),
        ("file_size", "VARCHAR(50) DEFAULT '0 KB'"),
        ("version", "INT DEFAULT 1"),
        ("resume_score", "INT DEFAULT 0"),
        ("ats_score", "INT DEFAULT 0"),
        ("extracted_text", "LONGTEXT"),
        ("is_active", "BOOLEAN DEFAULT TRUE"),
        ("status", "VARCHAR(50) DEFAULT 'Active'"),
        ("resume_name", "VARCHAR(255)"),
        ("resume_path", "VARCHAR(500)")
    ]
    for col_name, col_type in res_migration_cols:
        try:
            cursor.execute(f"ALTER TABLE resumes ADD COLUMN {col_name} {col_type}")
            conn.commit()
        except Exception:
            pass

    cursor.close()
    conn.close()


def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Unified parameterized query executor supporting both MySQL and SQLite."""
    conn, engine = get_connection()
    if not conn:
        logger.error("Failed to establish database connection.")
        return None

    if engine == "mysql":
        cursor = conn.cursor(dictionary=True)
    else:
        cursor = conn.cursor()
        query = query.replace("%s", "?")

    result = None
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
            last_id = cursor.lastrowid
            result = last_id if (last_id is not None and last_id > 0) else True
        elif fetchone:
            res = cursor.fetchone()
            if res is not None:
                result = dict(res) if hasattr(res, 'keys') or isinstance(res, dict) else res
            else:
                result = None
        elif fetchall:
            res = cursor.fetchall()
            if res is not None:
                result = [dict(r) if hasattr(r, 'keys') or isinstance(r, dict) else r for r in res]
            else:
                result = []
        else:
            result = None
    except Exception as e:
        logger.error(f"Database query error: {e} | Query: {query} | Params: {params}")
        result = None
    finally:
        close_connection(conn, cursor)

    return result

def fetch_one(query: str, params: tuple = ()):
    """Fetch a single record as a dictionary."""
    return execute_query(query, params, fetchone=True)

def fetch_all(query: str, params: tuple = ()):
    """Fetch all matching records as a list of dictionaries."""
    return execute_query(query, params, fetchall=True) or []

def insert_record(query: str, params: tuple = ()):
    """Insert a record into the database and return row ID or True."""
    return execute_query(query, params, commit=True)

def update_record(query: str, params: tuple = ()):
    """Update a record in the database."""
    return execute_query(query, params, commit=True)

def delete_record(query: str, params: tuple = ()):
    """Delete a record from the database."""
    return execute_query(query, params, commit=True)

# Initialize database on module import
init_db()

def get_user_by_email(email: str):
    """Fetch user dict by email."""
    user = execute_query("SELECT * FROM users WHERE email = %s", (email,), fetchone=True)
    if user:
        if not user.get("full_name") and user.get("fullname"):
            user["full_name"] = user["fullname"]
        if not user.get("password_hash") and user.get("password"):
            user["password_hash"] = user["password"]
    return user

def create_user(full_name: str, email: str, mobile: str, age: int, password: str):
    """Creates a new user and returns user_id."""
    from utils.password_hash import hash_password
    pwd_hash = hash_password(password)
    
    # Try inserting with dual column support (fullname/full_name & password/password_hash)
    try:
        user_id = execute_query(
            "INSERT INTO users (full_name, fullname, email, mobile, age, password_hash, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (full_name, full_name, email, mobile, age, pwd_hash, pwd_hash),
            commit=True
        )
    except Exception:
        user_id = execute_query(
            "INSERT INTO users (full_name, email, mobile, age, password_hash) VALUES (%s, %s, %s, %s, %s)",
            (full_name, email, mobile, age, pwd_hash),
            commit=True
        )

    if user_id:
        execute_query("INSERT INTO profiles (user_id, completion_percentage) VALUES (%s, %s)", (user_id, 20), commit=True)
    return user_id

def get_user_profile(user_id: int):
    """Fetch combined user and profile record."""
    if not user_id:
        return {}
    
    u = execute_query("SELECT * FROM users WHERE id = %s", (user_id,), fetchone=True) or {}
    p = execute_query("SELECT * FROM profiles WHERE user_id = %s", (user_id,), fetchone=True) or {}
    
    combined = dict(u)
    combined.update(p)
    combined["full_name"] = p.get("full_name") or u.get("full_name") or "Candidate Name"
    combined["email"] = p.get("email") or u.get("email") or "candidate@example.com"
    combined["mobile"] = p.get("mobile") or u.get("mobile") or ""
    combined["age"] = p.get("age") or u.get("age") or 24
    return combined

def update_user_profile(user_id: int, profile_data: dict) -> bool:
    """
    Updates profile and user fields robustly.
    Splits fields between 'users' table and 'profiles' table without SQL errors.
    """
    if not user_id or not profile_data:
        return False

    # Check if user exists in users table first
    user_exists = execute_query("SELECT id FROM users WHERE id = %s", (user_id,), fetchone=True)
    if not user_exists:
        # Create minimal user shell to satisfy foreign key constraint
        execute_query(
            "INSERT INTO users (id, full_name, email, mobile, age, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, "Candidate User", f"user_{user_id}@example.com", "9999999999", 22, "temp_hash"),
            commit=True
        )

    user_table_fields = {"full_name", "email", "mobile", "age"}
    
    # 1. Separate user and profile fields
    user_updates = {}
    profile_updates = {}

    for k, v in profile_data.items():
        if k in user_table_fields:
            user_updates[k] = v
        else:
            profile_updates[k] = v

    # 2. Update users table if user fields provided
    if user_updates:
        u_fields = [f"{k} = %s" for k in user_updates.keys()]
        u_values = list(user_updates.values()) + [user_id]
        u_query = f"UPDATE users SET {', '.join(u_fields)} WHERE id = %s"
        execute_query(u_query, tuple(u_values), commit=True)

    # 3. Update or Insert profiles table
    if profile_updates:
        existing = execute_query("SELECT id FROM profiles WHERE user_id = %s", (user_id,), fetchone=True)
        if not existing:
            cols = ["user_id"] + list(profile_updates.keys())
            placeholders = ["%s"] * len(cols)
            vals = [user_id] + list(profile_updates.values())
            ins_query = f"INSERT INTO profiles ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
            execute_query(ins_query, tuple(vals), commit=True)
        else:
            p_fields = [f"{k} = %s" for k in profile_updates.keys()]
            p_values = list(profile_updates.values()) + [user_id]
            p_query = f"UPDATE profiles SET {', '.join(p_fields)} WHERE user_id = %s"
            execute_query(p_query, tuple(p_values), commit=True)

    return True

def save_resume_metadata(user_id: int, filename: str, file_path: str, file_type: str, extracted_text: str = ""):
    """Save resume metadata in DB."""
    execute_query("UPDATE resumes SET is_active = 0 WHERE user_id = %s", (user_id,), commit=True)
    return execute_query(
        "INSERT INTO resumes (user_id, filename, file_path, file_type, extracted_text, is_active) VALUES (%s, %s, %s, %s, %s, 1)",
        (user_id, filename, file_path, file_type, extracted_text),
        commit=True
    )

def get_user_resumes(user_id: int):
    """Fetch all uploaded resumes for a user, active first."""
    return execute_query("SELECT * FROM resumes WHERE user_id = %s ORDER BY is_active DESC, uploaded_at DESC", (user_id,), fetchall=True)

def save_full_resume_analysis(resume_id: int, user_id: int, resume_score: int, ats_score: int, quality: str, completeness: int, skills: str, edu: str, exp: str, proj: str, missing: str, strengths: str, weaknesses: str, tips: str, summary: str):
    """Saves complete resume analysis record into MySQL/SQLite."""
    return execute_query(
        """
        INSERT INTO resume_analysis (resume_id, user_id, resume_score, ats_score, resume_quality, completeness_pct, extracted_skills, extracted_education, extracted_experience, extracted_projects, missing_skills, strengths, weaknesses, improvement_tips, summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (resume_id, user_id, resume_score, ats_score, quality, completeness, skills, edu, exp, proj, missing, strengths, weaknesses, tips, summary),
        commit=True
    )

def get_latest_resume_analysis(user_id: int):
    """Fetch latest resume analysis record for a user."""
    return execute_query("SELECT * FROM resume_analysis WHERE user_id = %s ORDER BY analyzed_at DESC LIMIT 1", (user_id,), fetchone=True)

def save_salary_prediction(user_id: int, resume_id: int, expected: float, min_sal: float, max_sal: float, exp_level: str):
    """Saves salary prediction into database."""
    return save_salary_prediction_record(
        user_id=user_id,
        resume_id=resume_id,
        predicted_salary=expected,
        minimum_salary=min_sal,
        maximum_salary=max_sal,
        experience_level=exp_level
    )

def save_salary_prediction_record(
    user_id: int,
    resume_id: int = None,
    prediction_id: str = None,
    resume_score: int = 85,
    ats_score: int = 88,
    predicted_salary: float = 8.5,
    minimum_salary: float = 6.5,
    maximum_salary: float = 11.5,
    confidence: int = 88,
    experience_level: str = "Mid-Level Professional"
):
    """Saves comprehensive salary prediction record into MySQL / SQLite database."""
    import uuid
    prediction_id = prediction_id or f"PRED-{uuid.uuid4().hex[:8].upper()}"
    return execute_query(
        """
        INSERT INTO salary_prediction (prediction_id, user_id, resume_id, resume_score, ats_score, predicted_salary, minimum_salary, maximum_salary, confidence, experience_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (prediction_id, user_id, resume_id, resume_score, ats_score, predicted_salary, minimum_salary, maximum_salary, confidence, experience_level),
        commit=True
    )

def get_latest_salary_prediction(user_id: int):
    """Fetches latest salary prediction for user."""
    return execute_query("SELECT * FROM salary_prediction WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,), fetchone=True)


def log_activity(user_id: int, action: str, details: str = ""):
    """Logs user actions into activity_logs table."""
    return execute_query("INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)", (user_id, action, details), commit=True)

def get_all_jobs():
    """Fetch all jobs stored in database."""
    return execute_query("SELECT * FROM jobs ORDER BY id DESC", fetchall=True) or []

def insert_job(title, company, location, experience, qualification, salary, skills, description):
    """Inserts a new job posting into database."""
    return execute_query(
        "INSERT INTO jobs (job_title, company, location, experience_level, qualification, salary_range, required_skills, job_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (title, company, location, experience, qualification, salary, skills, description),
        commit=True
    )

def save_job_match_history(user_id: int, job_id: int, resume_score: int, ats_score: int, match_pct: float, matching_skills: list, missing_skills: list, recommended_skills: list):
    """Saves job match record into database."""
    return execute_query(
        "INSERT INTO job_matching (user_id, job_id, resume_score, ats_score, match_percentage, matching_skills, missing_skills, recommended_skills) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (user_id, job_id, resume_score, ats_score, match_pct, ", ".join(matching_skills), ", ".join(missing_skills), ", ".join(recommended_skills)),
        commit=True
    )

def save_user_certificate(user_id: int, cert_data_or_title=None, issuer: str = "", issue_date: str = "", file_path: str = ""):
    """Stores user certificate record with full field support for dict or positional parameters."""
    if isinstance(cert_data_or_title, dict):
        c_name = cert_data_or_title.get("certificate_name") or cert_data_or_title.get("title", "")
        c_org = cert_data_or_title.get("issuing_organization") or cert_data_or_title.get("issuer", "")
        i_date = str(cert_data_or_title.get("issue_date", "") or "")
        e_date = str(cert_data_or_title.get("expiry_date", "") or "")
        c_id = cert_data_or_title.get("credential_id", "")
        c_url = cert_data_or_title.get("credential_url", "")
        c_path = cert_data_or_title.get("certificate_path") or cert_data_or_title.get("file_path", "")
    else:
        c_name = cert_data_or_title or ""
        c_org = issuer
        i_date = str(issue_date or "")
        e_date = ""
        c_id = ""
        c_url = ""
        c_path = file_path or ""

    return execute_query(
        """
        INSERT INTO certificates (
            user_id, certificate_name, issuing_organization, issue_date, expiry_date,
            credential_id, credential_url, certificate_path, title, issuer, file_path
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, c_name, c_org, i_date, e_date, c_id, c_url, c_path, c_name, c_org, c_path),
        commit=True
    )

def set_active_resume_db(user_id: int, resume_id: int):
    """Sets target resume as active and all others as inactive / archived."""
    execute_query("UPDATE resumes SET is_active = 0, status = 'Archived' WHERE user_id = %s", (user_id,), commit=True)
    return execute_query("UPDATE resumes SET is_active = 1, status = 'Active' WHERE id = %s AND user_id = %s", (resume_id, user_id), commit=True)

def delete_resume_record(user_id: int, resume_id: int):
    """Deletes resume record and associated records from database."""
    execute_query("DELETE FROM resume_analysis WHERE resume_id = %s AND user_id = %s", (resume_id, user_id), commit=True)
    execute_query("DELETE FROM salary_prediction WHERE resume_id = %s AND user_id = %s", (resume_id, user_id), commit=True)
    execute_query("DELETE FROM resume_history WHERE resume_id = %s AND user_id = %s", (resume_id, user_id), commit=True)
    return execute_query("DELETE FROM resumes WHERE id = %s AND user_id = %s", (resume_id, user_id), commit=True)

def save_resume_history(user_id: int, resume_id: int, version: int, action: str, ats_score: int = 0, status: str = 'Archived'):
    """Logs entry in resume_history table."""
    return execute_query(
        "INSERT INTO resume_history (resume_id, user_id, version, action, ats_score, status) VALUES (%s, %s, %s, %s, %s, %s)",
        (resume_id, user_id, version, action, ats_score, status),
        commit=True
    )

def get_user_resume_history(user_id: int, resume_id: int = None):
    """Fetches version history records for a user's resume."""
    if resume_id:
        return execute_query("SELECT * FROM resume_history WHERE user_id = %s AND resume_id = %s ORDER BY created_at DESC", (user_id, resume_id), fetchall=True) or []
    return execute_query("SELECT * FROM resume_history WHERE user_id = %s ORDER BY created_at DESC", (user_id,), fetchall=True) or []

def get_resume_by_id(resume_id: int):
    """Fetch single resume row by ID."""
    return execute_query("SELECT * FROM resumes WHERE id = %s", (resume_id,), fetchone=True)

def update_resume_version_and_scores(resume_id: int, version: int, filename: str, file_path: str, file_size: str, file_type: str, extracted_text: str, resume_score: int, ats_score: int):
    """Updates existing resume row upon file replacement."""
    return execute_query(
        """
        UPDATE resumes
        SET version = %s, filename = %s, file_path = %s, file_size = %s, file_type = %s, extracted_text = %s, resume_score = %s, ats_score = %s, uploaded_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (version, filename, file_path, file_size, file_type, extracted_text, resume_score, ats_score, resume_id),
        commit=True
    )

def save_chat_message(user_id: int, session_id: str, question: str, answer: str, session_title: str = "New Chat Session"):
    """Saves user question and AI response into chat_history table."""
    import uuid
    chat_id = f"MSG-{uuid.uuid4().hex[:8].upper()}"
    return execute_query(
        """
        INSERT INTO chat_history (chat_id, user_id, session_id, session_title, question, answer)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (chat_id, user_id, session_id, session_title, question, answer),
        commit=True
    )

def get_user_chat_sessions(user_id: int):
    """Fetches unique chat sessions for user grouped by session_id."""
    return execute_query(
        """
        SELECT session_id, session_title, is_favorite, MAX(timestamp) as last_updated, COUNT(id) as msg_count
        FROM chat_history
        WHERE user_id = %s
        GROUP BY session_id, session_title, is_favorite
        ORDER BY last_updated DESC
        """,
        (user_id,),
        fetchall=True
    ) or []

def get_chat_session_messages(user_id: int, session_id: str):
    """Fetches all message turns in a specific chat session."""
    return execute_query(
        "SELECT * FROM chat_history WHERE user_id = %s AND session_id = %s ORDER BY id ASC",
        (user_id, session_id),
        fetchall=True
    ) or []

def rename_chat_session(user_id: int, session_id: str, new_title: str):
    """Updates session title across all messages in session."""
    return execute_query(
        "UPDATE chat_history SET session_title = %s WHERE user_id = %s AND session_id = %s",
        (new_title, user_id, session_id),
        commit=True
    )

def delete_chat_session(user_id: int, session_id: str):
    """Deletes all messages in session."""
    return execute_query(
        "DELETE FROM chat_history WHERE user_id = %s AND session_id = %s",
        (user_id, session_id),
        commit=True
    )

def toggle_favorite_chat(user_id: int, session_id: str, is_fav: bool):
    """Toggles favorite flag on session."""
    fav_val = 1 if is_fav else 0
    return execute_query(
        "UPDATE chat_history SET is_favorite = %s WHERE user_id = %s AND session_id = %s",
        (fav_val, user_id, session_id),
        commit=True
    )

# --- PROJECTS HELPERS ---

def save_user_project(user_id: int, project_data: dict) -> int:
    """Inserts a new project for a user and returns project_id."""
    return execute_query(
        """
        INSERT INTO projects (
            user_id, project_name, description, technologies, project_role,
            start_date, end_date, github_url, live_demo_url, project_type,
            key_contributions, project_outcome
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            project_data.get("project_name", ""),
            project_data.get("description", ""),
            project_data.get("technologies", ""),
            project_data.get("project_role", ""),
            str(project_data.get("start_date", "") or ""),
            str(project_data.get("end_date", "") or ""),
            project_data.get("github_url", ""),
            project_data.get("live_demo_url", ""),
            project_data.get("project_type", "Web App"),
            project_data.get("key_contributions", ""),
            project_data.get("project_outcome", "")
        ),
        commit=True
    )

def get_user_projects(user_id: int) -> list:
    """Fetches all projects for a user."""
    return execute_query("SELECT * FROM projects WHERE user_id = %s ORDER BY created_at DESC", (user_id,), fetchall=True) or []

def get_project_by_id(project_id: int, user_id: int = None) -> dict:
    """Fetches single project by ID."""
    if user_id:
        return execute_query("SELECT * FROM projects WHERE id = %s AND user_id = %s", (project_id, user_id), fetchone=True) or {}
    return execute_query("SELECT * FROM projects WHERE id = %s", (project_id,), fetchone=True) or {}

def update_user_project(project_id: int, user_id: int, project_data: dict) -> bool:
    """Updates an existing project record."""
    res = execute_query(
        """
        UPDATE projects SET
            project_name = %s,
            description = %s,
            technologies = %s,
            project_role = %s,
            start_date = %s,
            end_date = %s,
            github_url = %s,
            live_demo_url = %s,
            project_type = %s,
            key_contributions = %s,
            project_outcome = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s AND user_id = %s
        """,
        (
            project_data.get("project_name", ""),
            project_data.get("description", ""),
            project_data.get("technologies", ""),
            project_data.get("project_role", ""),
            str(project_data.get("start_date", "") or ""),
            str(project_data.get("end_date", "") or ""),
            project_data.get("github_url", ""),
            project_data.get("live_demo_url", ""),
            project_data.get("project_type", "Web App"),
            project_data.get("key_contributions", ""),
            project_data.get("project_outcome", ""),
            project_id,
            user_id
        ),
        commit=True
    )
    return res is not None

def delete_user_project(user_id: int, project_id: int) -> bool:
    """Deletes a project record."""
    res = execute_query("DELETE FROM projects WHERE id = %s AND user_id = %s", (project_id, user_id), commit=True)
    return res is not None


# --- ENHANCED CERTIFICATE HELPERS ---

def get_user_certificates(user_id: int):
    """Fetches user certificate records."""
    return execute_query("SELECT * FROM certificates WHERE user_id = %s ORDER BY id DESC", (user_id,), fetchall=True) or []

def get_certificate_by_id(cert_id: int, user_id: int = None) -> dict:
    """Fetches single certificate by ID."""
    if user_id:
        return execute_query("SELECT * FROM certificates WHERE id = %s AND user_id = %s", (cert_id, user_id), fetchone=True) or {}
    return execute_query("SELECT * FROM certificates WHERE id = %s", (cert_id,), fetchone=True) or {}

def update_user_certificate(cert_id: int, user_id: int, cert_data: dict) -> bool:
    """Updates certificate details."""
    c_name = cert_data.get("certificate_name") or cert_data.get("title", "")
    c_org = cert_data.get("issuing_organization") or cert_data.get("issuer", "")
    i_date = str(cert_data.get("issue_date", "") or "")
    e_date = str(cert_data.get("expiry_date", "") or "")
    c_id = cert_data.get("credential_id", "")
    c_url = cert_data.get("credential_url", "")
    c_path = cert_data.get("certificate_path") or cert_data.get("file_path", "")

    res = execute_query(
        """
        UPDATE certificates SET
            certificate_name = %s,
            issuing_organization = %s,
            issue_date = %s,
            expiry_date = %s,
            credential_id = %s,
            credential_url = %s,
            certificate_path = %s,
            title = %s,
            issuer = %s,
            file_path = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s AND user_id = %s
        """,
        (c_name, c_org, i_date, e_date, c_id, c_url, c_path, c_name, c_org, c_path, cert_id, user_id),
        commit=True
    )
    return res is not None

def delete_user_certificate(user_id: int, cert_id: int) -> bool:
    """Deletes a certificate record."""
    res = execute_query("DELETE FROM certificates WHERE id = %s AND user_id = %s", (cert_id, user_id), commit=True)
    return res is not None

# --- LOGIN & ADMIN ACTIVITY TRACKING HELPERS ---

def record_login_activity(user_id: int, login_status: str = "SUCCESS", session_id: str = "", ip_address: str = "127.0.0.1"):
    """Records user login event in login_activity and activity_logs tables."""
    execute_query(
        "INSERT INTO login_activity (user_id, login_status, session_id, ip_address) VALUES (%s, %s, %s, %s)",
        (user_id, login_status, session_id, ip_address),
        commit=True
    )
    execute_query(
        "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
        (user_id, "LOGIN", f"User logged in successfully (Session: {session_id[:12]})"),
        commit=True
    )

def record_logout_activity(user_id: int, session_id: str = ""):
    """Updates login_activity logout_time and records logout in activity_logs."""
    if user_id:
        execute_query(
            "UPDATE login_activity SET logout_time = CURRENT_TIMESTAMP WHERE user_id = %s AND logout_time IS NULL",
            (user_id,),
            commit=True
        )
        execute_query(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
            (user_id, "LOGOUT", "User logged out of platform"),
            commit=True
        )

def seed_admin_user_if_not_exists():
    """Seeds default admin user into database if no admin exists."""
    from utils.password_hash import hash_password
    existing_admin = execute_query("SELECT id FROM users WHERE role = 'admin' OR email = 'admin@careerintel.ai'", fetchone=True)
    if not existing_admin:
        pwd_hash = hash_password("Admin@123456")
        admin_id = execute_query(
            "INSERT INTO users (full_name, email, mobile, age, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s)",
            ("Platform Administrator", "admin@careerintel.ai", "9999999999", 30, pwd_hash, "admin"),
            commit=True
        )
        if admin_id:
            execute_query("INSERT INTO profiles (user_id, completion_percentage) VALUES (%s, 100)", (admin_id,), commit=True)
            logger.info("Admin user 'admin@careerintel.ai' created successfully.")

# Run admin seed check on load
try:
    seed_admin_user_if_not_exists()
except Exception as e:
    logger.warning(f"Could not seed admin user: {e}")








