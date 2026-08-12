# AI Resume Screening & Career Intelligence Platform

A production-ready, full-stack AI platform built using **Python, Streamlit, MySQL, Sentence Transformers (`all-MiniLM-L6-v2`), Scikit-Learn, PyMuPDF, and Plotly**.

Designed specifically for **Final Year Computer Science Projects**, **Infosys Springboard Internship Submissions**, **Portfolio Showcase**, and **GitHub Repositories**.

---

## 🌟 Executive Summary & Key Highlights

Modern recruitment relies heavily on Automated Applicant Tracking Systems (ATS) and semantic matching algorithms. The **AI Resume Screening & Career Intelligence Platform** provides an end-to-end intelligence suite that allows job seekers and recruiters to parse resumes, evaluate ATS scores, execute transformer-based job description matching, predict salary trajectories, and generate custom interview questions.

### Core Capabilities

- 📄 **Multi-Format Resume Ingestion**: Native parsing for **PDF** and **DOCX** files using PyMuPDF (fitz), pdfplumber, and python-docx.
- ⚡ **Sentence Transformers Matching**: High-precision semantic similarity between candidate resumes and job descriptions using 384-dimensional `all-MiniLM-L6-v2` embeddings and Cosine Similarity.
- 🎯 **ATS Compatibility & Keyword Audit**: Automated calculation of ATS score (0-100), formatting check, section completeness, strengths, weaknesses, and improvement tips.
- 📊 **Random Forest Salary Predictor**: Machine learning regression model trained on industry salary trends to predict expected LPA salary based on experience and technical skills.
- 🎙️ **AI Interview Simulator**: Generates role-specific Technical, HR, Behavioral, Coding, and Scenario-based interview questions with model answers and confidence tips.
- 🗄️ **Production-Ready Relational Database**: Complete MySQL schema support with automatic SQLite fallback for zero-configuration local execution.
- 🎨 **Glassmorphic UI/UX**: Custom responsive Streamlit interface with Plotly interactive charts, dark mode glassmorphism, progress indicators, and PDF report downloads.

---

## 🤖 AI & Machine Learning Models Explanation

### 1. `all-MiniLM-L6-v2` (Sentence Transformers)
- **Purpose**: Semantic similarity evaluation between candidate resume text and target Job Description (JD).
- **Internal Working**: Converts resume text and JD text into 384-dimensional dense vector embeddings. Computes the Cosine Similarity angle between the vectors:
  $$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
- **Why Used**: Captures deep contextual semantics rather than relying solely on exact keyword overlaps.
- **Advantages**: Extremely fast inference (sub-50ms), low memory footprint, handles synonyms naturally.
- **Limitations**: Max sequence length limit of 256 tokens; truncated text is handled via section chunking.

### 2. TF-IDF (Term Frequency - Inverse Document Frequency)
- **Purpose**: Skill taxonomy matching and keyword density analysis.
- **Internal Working**: Measures how important a skill word is to a resume relative to the general skill dataset.
- **Advantages**: Fast, deterministic, no GPU requirements.

### 3. Random Forest Regressor
- **Purpose**: Predictive salary modeling (LPA).
- **Internal Working**: An ensemble of 100 decision trees trained on experience years, skill counts, and project complexities.
- **Advantages**: Robust against outliers, non-linear feature handling.

### 4. Rule-Based NLP & Regex Parsing Engine
- **Purpose**: Entity extraction (Name, Email, Phone, Skills, Education, Experience years).
- **Internal Working**: Combines regex pattern matching with token dictionary lookups from `datasets/skills.csv`.

---

## 📁 Directory Architecture

```text
AI_Career_Intelligence_Platform/
│── app.py                         # Main Streamlit Entry Point & Router
│── config.py                      # Global Environment Configurations
│── requirements.txt               # Dependencies
│── environment.yml                # Conda Environment Specification
│── README.md                      # Detailed Project Documentation
│── .env                           # Active Environment Settings
│── .env.example                   # Environment Template
│
├── database/                      # Relational Persistence Layer
│   ├── database.py                # MySQL Connector with SQLite Auto-Fallback
│   ├── schema.sql                 # Master Unified SQL DDL Script
│   ├── users.sql                  # Users Table DDL
│   ├── profiles.sql               # Profiles Table DDL
│   ├── resumes.sql                # Resumes Table DDL
│   ├── resume_analysis.sql        # Analysis Table DDL
│   ├── certificates.sql           # Certificates Table DDL
│   ├── jobs.sql                   # Jobs Table DDL
│   ├── career_recommendations.sql # Career Recommendations DDL
│   ├── interview_questions.sql    # Interview Q&A DDL
│   └── activity_logs.sql          # User Activity Logs DDL
│
├── auth/                          # Authentication Modules
│   ├── register.py                # Account Registration with bcrypt Hashing
│   ├── login.py                   # User Sign-In & Session Setup
│   ├── forgot_password.py         # Security Password Recovery
│   └── logout.py                  # Session Teardown
│
├── pages_modules/                 # Feature Pages
│   ├── home.py                    # Landing & Tech Highlights
│   ├── dashboard.py               # Main Telemetry Overview
│   ├── profile.py                 # Candidate Profile Management
│   ├── resume_upload.py           # Drag & Drop Ingestion
│   ├── resume_management.py       # Active Selection, View, Download, Delete
│   ├── resume_analysis.py         # ATS Audit & Keyword Extraction
│   ├── job_matching.py            # SentenceTransformers Job Matcher
│   ├── career_dashboard.py        # Analytics & Plotly Charts
│   ├── interview.py               # AI Practice Portal & Mock Simulator
│   ├── ai_tools.py                # Chatbot, Resume Builder, Cover Letter, Roadmap
│   ├── reports.py                 # PDF Report & Excel Export Center
│   └── settings.py                # User & System Preferences
│
├── ai_models/                     # ML / NLP Core Modules
│   ├── train_models.py            # Random Forest & TF-IDF Model Trainer Script
│   ├── resume_parser.py           # PDF/DOCX Parser Engine
│   ├── ats_score.py               # ATS Scoring Logic
│   ├── skill_gap.py               # Skill Matrix Comparison
│   ├── salary_prediction.py       # Random Forest Salary Regressor
│   ├── job_matching.py            # MinLM Semantic Matcher
│   ├── interview_generator.py     # Question Synthesizer
│   ├── learning_recommendation.py # Course Recommender
│   ├── all_minilm.py              # SentenceTransformers Embedding Wrapper
│   └── tfidf_model.py             # TF-IDF Utilities
│
├── datasets/                      # Seed Datasets
│   ├── jobs.csv                   # Job Postings Dataset
│   ├── salary.csv                 # Salary Regressor Training Dataset
│   ├── skills.csv                 # Technical Skills Taxonomy
│   └── courses.csv                # Upskilling Courses Dataset
│
├── static/                        # Visual Assets & Styling
│   └── css/style.css              # Custom Glassmorphic Dark Theme
│
└── utils/                         # Helper Services
    ├── helper.py                  # Validation & Cleaners
    ├── charts.py                  # Plotly Interactive Visuals
    ├── email_service.py           # SMTP Email Service
    ├── password_hash.py           # bcrypt Password Utilities
    ├── file_upload.py             # File Security & Directory Storage
    └── pdf_generator.py           # FPDF Report Exporter
```

---

## 🛠️ Installation & Setup Guide

### Option A: Using Standard Python Virtual Environment (pip)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/AI_Career_Intelligence_Platform.git
   cd AI_Career_Intelligence_Platform
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train ML Models**:
   ```bash
   python ai_models/train_models.py
   ```

5. **Run the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```

---

### Option B: Using Conda Environment

1. **Create Conda Environment**:
   ```bash
   conda env create -f environment.yml
   conda activate ai_career_platform
   ```

2. **Train Models and Start Application**:
   ```bash
   python ai_models/train_models.py
   streamlit run app.py
   ```

---

## 🗄️ Database Configuration (MySQL & SQLite)

The system automatically operates out-of-the-box using **SQLite** (`database/ai_career.db`).

To switch to **MySQL**:
1. Open `.env` and set `DB_TYPE=mysql`.
2. Provide your MySQL host, port, user, and password credentials:
   ```env
   DB_TYPE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=ai_career_db
   ```
3. Import `database/schema.sql` into your MySQL server instance:
   ```bash
   mysql -u root -p ai_career_db < database/schema.sql
   ```

---

## 🚀 Deploying to Streamlit Cloud

1. Push code to GitHub repository.
2. Visit [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Connect your GitHub repository, select `app.py` as main file path.
4. Add environment variables from `.env` into Streamlit Advanced Settings Secrets.
5. Click **Deploy**!

---

## 📜 License & Credits

Developed for academic submission and GitHub portfolio showcase.
- **Author**: AI Engineer & Full Stack Developer
- **Tech Stack**: Streamlit, PyTorch, Sentence-Transformers, Scikit-learn, PyMuPDF, Plotly.
