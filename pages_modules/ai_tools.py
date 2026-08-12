import streamlit as st
from database.database import execute_query

def render_ai_tools_page():
    """Renders suite of AI Power Tools (Chatbot, Resume Builder, Cover Letter, Career Roadmap)."""
    st.markdown('<h1 class="gradient-text">AI Power Suite & Assistant Tools</h1>', unsafe_allow_html=True)
    st.write("Leverage intelligent AI generators to craft cover letters, build resume bullets, plan career roadmaps, or chat with your AI assistant.")

    tool_tab1, tool_tab2, tool_tab3, tool_tab4, tool_tab5 = st.tabs([
        "💬 AI Career Chatbot",
        "📄 AI Resume Builder",
        "✉️ AI Cover Letter Generator",
        "🗺️ AI Career Roadmap",
        "✨ Resume Improvement (Before vs After)"
    ])

    user_id = st.session_state.get("user_id")

    # 1. AI Chatbot
    with tool_tab1:
        st.subheader("💬 AI Career Intelligence Assistant")
        if "chat_messages" not in st.session_state:
            st.session_state["chat_messages"] = [
                {"role": "assistant", "content": "Hello! I am your AI Career Advisor. Ask me anything about resume tips, interview preparation, salary negotiation, or skill upskilling."}
            ]

        for msg in st.session_state["chat_messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("Ask career advisor..."):
            st.session_state["chat_messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Heuristic response generator
            response = "That is a great career query! "
            p_lower = prompt.lower()
            if "resume" in p_lower:
                response += "For resumes, focus on quantifiable metrics, standard ATS headings, and strong action verbs like 'Engineered' or 'Architected'."
            elif "interview" in p_lower:
                response += "In interviews, use the STAR methodology (Situation, Task, Action, Result) to structure your behavioral and technical project answers."
            elif "salary" in p_lower:
                response += "When negotiating salary, research market medians for your location, highlight unique skill overlaps, and frame your request around value creation."
            else:
                response += "To accelerate your growth, maintain a consistent upskilling habit, build hands-on portfolio projects, and optimize your LinkedIn profile."

            st.session_state["chat_messages"].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

    # 2. AI Resume Builder
    with tool_tab2:
        st.subheader("📄 AI Resume Summary & Bullet Point Generator")
        role = st.text_input("Target Role", value="Python Developer", key="rb_role")
        skills_str = st.text_input("Top Skills", value="Python, SQL, REST APIs, Streamlit", key="rb_skills")
        experience = st.text_input("Project / Experience Highlight", value="Built AI Resume Screening platform with Sentence Transformers.", key="rb_exp")

        if st.button("Generate Professional Resume Summary", key="btn_gen_res"):
            st.write("---")
            st.subheader("Generated Professional Summary:")
            st.success(
                f"Results-driven {role} with expertise in {skills_str}. Proven track record in designing "
                f"and deploying scalable applications, including {experience}. Adept at problem-solving, "
                f"optimizing backend systems, and collaborating in agile engineering teams."
            )
            st.subheader("Generated Impact Bullet Points:")
            st.info(f"• Engineered scalable {role} solutions utilizing {skills_str}, improving system processing efficiency by 35%.")
            st.info(f"• Successfully architected and deployed {experience}, serving end users with high availability.")

    # 3. AI Cover Letter Generator
    with tool_tab3:
        st.subheader("✉️ AI Cover Letter Generator")
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Target Company Name", value="TechCorp Systems")
            hiring_manager = st.text_input("Hiring Manager Name", value="Hiring Manager")
        with col2:
            position_title = st.text_input("Job Title", value="Software Engineer")

        if st.button("Generate Cover Letter", key="btn_gen_cl"):
            st.write("---")
            cl_text = f"""Dear {hiring_manager},

I am writing to express my enthusiastic interest in the {position_title} position at {company_name}. With my strong technical foundation in software engineering, machine learning pipelines, and backend development, I am confident in my ability to deliver immediate value to your engineering team.

In my recent work, I have spearheaded projects focused on high-performance data processing, AI modeling, and full-stack integration. My hands-on experience aligns directly with {company_name}'s commitment to innovation and technical excellence.

Thank you for your time and consideration. I welcome the opportunity to discuss how my background and technical skills make me a strong fit for this role.

Sincerely,
{st.session_state.get('user_name', 'Applicant')}
"""
            st.text_area("Generated Cover Letter (Ready to Copy)", value=cl_text, height=260)

    # 4. AI Career Roadmap
    with tool_tab4:
        st.subheader("🗺️ AI Career Growth Roadmap")
        target_goal = st.text_input("Dream Career Role", value="Lead AI Architect")

        if st.button("Generate Career Roadmap", key="btn_gen_map"):
            st.write("---")
            st.markdown(f"### 📍 3-Phase Roadmap to Become a **{target_goal}**")

            st.markdown("""
            <div class="glass-card">
                <h5>Phase 1: Foundations (Months 0 - 6)</h5>
                <p>Master Python, SQL, Data Structures, Git version control, and cloud fundamentals (AWS/Azure).</p>
            </div>
            <div class="glass-card">
                <h5>Phase 2: Specialization & ML Operations (Months 6 - 18)</h5>
                <p>Deep dive into PyTorch, Transformers, Scikit-learn, Docker, Kubernetes, and MLOps deployment pipelines.</p>
            </div>
            <div class="glass-card">
                <h5>Phase 3: System Design & Leadership (Months 18 - 36)</h5>
                <p>Architect high-availability distributed systems, lead engineering initiatives, and drive technical strategy.</p>
            </div>
            """, unsafe_allow_html=True)

    # 5. AI Resume Improvement Suggestions (Before vs After)
    with tool_tab5:
        st.subheader("✨ Module 6 – Resume Improvement Suggestions (Before vs After)")
        st.write("Compare raw un-optimized resume text against AI-optimized enterprise standards:")

        st.markdown("### 🔄 1. Resume Summary Improvement")
        c_b1, c_a1 = st.columns(2)
        with c_b1:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 12px; padding: 16px;">
                <h5 style="color: #EF4444;">🔴 BEFORE (Un-optimized)</h5>
                <p>"Looking for a job in software development where I can use my skills."</p>
            </div>
            """, unsafe_allow_html=True)
        with c_a1:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 12px; padding: 16px;">
                <h5 style="color: #10B981;">🟢 AFTER (AI Optimized)</h5>
                <p>"Results-driven Python & Machine Learning Engineer adept at architecting high-throughput NLP screening platforms, optimizing SQL queries, and deploying Dockerized cloud services."</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>### 🔄 2. Project Bullet Point Improvement", unsafe_allow_html=True)
        c_b2, c_a2 = st.columns(2)
        with c_b2:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 12px; padding: 16px;">
                <h5 style="color: #EF4444;">🔴 BEFORE (Vague)</h5>
                <p>"Made a Python project for machine learning using Streamlit and scikit-learn."</p>
            </div>
            """, unsafe_allow_html=True)
        with c_a2:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 12px; padding: 16px;">
                <h5 style="color: #10B981;">🟢 AFTER (Quantified Metrics)</h5>
                <p>"Engineered end-to-end AI Resume Screening platform using Streamlit, Sentence Transformers, and Random Forest; reduced candidate screening latency by 45%."</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>### 🔄 3. Missing Keywords & Certifications Added", unsafe_allow_html=True)
        c_b3, c_a3 = st.columns(2)
        with c_b3:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 12px; padding: 16px;">
                <h5 style="color: #EF4444;">🔴 BEFORE</h5>
                <p><b>Keywords:</b> Python, SQL, Coding</p>
                <p><b>Certs:</b> None</p>
            </div>
            """, unsafe_allow_html=True)
        with c_a3:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 12px; padding: 16px;">
                <h5 style="color: #10B981;">🟢 AFTER</h5>
                <p><b>Keywords:</b> Docker, Kubernetes, AWS, PyTorch, REST APIs, Microservices</p>
                <p><b>Certs:</b> Infosys Springboard ML Masterclass, AWS Certified Cloud Practitioner</p>
            </div>
            """, unsafe_allow_html=True)
