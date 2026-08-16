import json
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database.database import execute_query
from utils.interview_utils import (
    DOMAINS,
    TARGET_ROLES,
    EXPERIENCE_LEVEL_OPTIONS,
    DIFFICULTY_OPTIONS,
    QUESTION_TYPE_OPTIONS,
    QUESTION_COUNT_OPTIONS,
    get_user_active_resume_data,
    get_badge_styles,
    clean_difficulty_str
)
from services.interview_preference_service import (
    get_user_interview_preference,
    save_user_interview_preference
)
from services.interview_service import prepare_personalized_user_interview
from ai_models.interview_evaluator import evaluate_user_interview_answer
from ai_models.interview_feedback import generate_final_interview_report
from services.interview_history_service import (
    save_interview_question_response,
    update_interview_session_results,
    get_user_interview_sessions_history,
    get_session_questions,
    delete_interview_session,
    save_question_bookmark,
    remove_question_bookmark,
    get_saved_questions
)

def render_question_card_component(idx: int, total: int, q: dict, user_id: int, show_answer_default: bool = False):
    """
    Renders question card according to Section 14 prompt specifications:
    Question Number, Domain, Role, Difficulty, QUESTION, ANSWER, SIMPLE EXPLANATION, EXAMPLE, KEY POINTS, INTERVIEW TIP.
    Action buttons: Show Answer, Save Question, Copy Question, Copy Answer.
    """
    domain = q.get("domain", "Software Development")
    role = q.get("role", "Developer")
    diff = q.get("difficulty", "Medium")
    badges = get_badge_styles(domain, diff)

    q_text = q.get("question", "")
    model_ans = q.get("model_answer", "")
    exp_text = q.get("explanation", "")
    ex_text = q.get("example", "")
    kp_data = q.get("key_points", [])
    tip_text = q.get("interview_tip", "")
    q_id = q.get("question_id", idx)

    # Format key points if string or JSON list
    if isinstance(kp_data, str):
        try:
            kp_data = json.loads(kp_data)
        except Exception:
            kp_data = [kp_data] if kp_data else []

    # Unique toggle key per question
    toggle_key = f"show_ans_{idx}_{abs(hash(q_text)) % 1000000}"
    if toggle_key not in st.session_state:
        st.session_state[toggle_key] = show_answer_default

    # Card Header & Question HTML (Section 14 specification)
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.88); border: 1px solid rgba(255, 255, 255, 0.15); border-left: 6px solid #3B82F6; border-radius: 14px; padding: 22px; margin-bottom: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <span style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">Question {idx}</span>
            <div>
                <span style="background: rgba(59, 130, 246, 0.2); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.4); padding: 4px 12px; border-radius: 16px; font-size: 0.85rem; font-weight: 600; margin-right: 6px;">
                    🎯 {domain}
                </span>
                <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 12px; border-radius: 16px; font-size: 0.85rem; font-weight: 600; margin-right: 6px;">
                    💼 {role}
                </span>
                <span style="background: {badges['diff_color']}22; color: {badges['diff_color']}; border: 1px solid {badges['diff_color']}55; padding: 4px 12px; border-radius: 16px; font-size: 0.85rem; font-weight: 600;">
                    {badges['diff_icon']} {diff}
                </span>
            </div>
        </div>
        <div style="font-size: 0.85rem; font-weight: 700; color: #94A3B8; letter-spacing: 1px; margin-top: 10px;">❓ QUESTION</div>
        <div style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF; line-height: 1.5; margin-top: 4px;">
            {q_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action Toolbar Buttons: 👁 Show Answer | ⭐ Save Question | 📋 Copy Question | 📋 Copy Answer
    col_act1, col_act2, col_act3, col_act4 = st.columns([1.2, 1.2, 1, 1])
    
    with col_act1:
        btn_label = "🙈 Hide Answer" if st.session_state[toggle_key] else "👁 Show Answer"
        if st.button(btn_label, key=f"btn_toggle_{idx}_{abs(hash(q_text)) % 1000000}", use_container_width=True):
            st.session_state[toggle_key] = not st.session_state[toggle_key]
            st.rerun()

    with col_act2:
        if st.button("⭐ Save Question", key=f"btn_save_{idx}_{abs(hash(q_text)) % 1000000}", use_container_width=True):
            save_question_bookmark(user_id, q_id, q_text, domain, role, model_ans)
            st.toast(f"Question #{idx} bookmarked in Saved Questions!")

    with col_act3:
        st.download_button("📋 Copy Question", data=f"Question: {q_text}", file_name=f"question_{idx}.txt", key=f"btn_cp_q_{idx}_{abs(hash(q_text)) % 1000000}", use_container_width=True)

    with col_act4:
        st.download_button("📋 Copy Answer", data=f"Question:\n{q_text}\n\nModel Answer:\n{model_ans}\n\nExplanation:\n{exp_text}", file_name=f"answer_{idx}.txt", key=f"btn_cp_a_{idx}_{abs(hash(q_text)) % 1000000}", use_container_width=True)

    # Answer Breakdown Content (revealed when toggled)
    if st.session_state[toggle_key]:
        st.markdown("#### 💡 ANSWER")
        st.info(model_ans)

        if exp_text:
            st.markdown("#### 📖 SIMPLE EXPLANATION")
            st.write(exp_text)

        if ex_text:
            st.markdown("#### 💻 EXAMPLE")
            if "```" in ex_text:
                st.markdown(ex_text)
            else:
                st.code(ex_text, language="python")

        if kp_data:
            st.markdown("#### ✅ KEY POINTS")
            for kp in kp_data:
                st.write(f"• {kp}")

        if tip_text:
            st.markdown("#### 🎯 INTERVIEW TIP")
            st.success(tip_text)

    st.write("---")


def render_ai_interview_preparation_page():
    """
    Renders AI Interview Preparation Question Bank System.
    """
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to access AI Interview Preparation.")
        st.stop()

    st.markdown('<h1 class="gradient-text">📚 AI Interview Preparation Question Bank</h1>', unsafe_allow_html=True)
    st.caption("Comprehensive domain-specific interview questions WITH complete model answers, simple explanations, code examples, key points, and delivery tips.")

    # Load User Preference from DB
    user_pref = get_user_interview_preference(user_id)
    resume_data = get_user_active_resume_data(user_id)

    # Top Selection Panel: Domain, Job Role, Experience, Difficulty, Question Type, Count (Sections 1 & 2)
    with st.expander("⚙️ Select Domain, Target Role & Preference Settings", expanded=True):
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.subheader("1. Select Your Domain")
            domain_idx = DOMAINS.index(user_pref["domain"]) if user_pref["domain"] in DOMAINS else 0
            selected_domain_option = st.selectbox("Select Domain", DOMAINS, index=domain_idx, key="pref_domain_select")
            
            if selected_domain_option == "Other":
                selected_domain = st.text_input("Enter Custom Domain", value="Custom Technology Stack", key="custom_domain_input")
            else:
                selected_domain = selected_domain_option

        with col_d2:
            st.subheader("2. Select Target Job Role")
            role_idx = TARGET_ROLES.index(user_pref["target_role"]) if user_pref["target_role"] in TARGET_ROLES else 0
            selected_role_option = st.selectbox("Select Target Role", TARGET_ROLES, index=role_idx, key="pref_role_select")
            
            if selected_role_option == "Other":
                selected_role = st.text_input("Enter Custom Target Role", value="Specialist Engineer", key="custom_role_input")
            else:
                selected_role = selected_role_option

        st.write("---")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1:
            exp_idx = EXPERIENCE_LEVEL_OPTIONS.index(user_pref["experience_level"]) if user_pref["experience_level"] in EXPERIENCE_LEVEL_OPTIONS else 1
            selected_exp = st.selectbox("Experience Level", EXPERIENCE_LEVEL_OPTIONS, index=exp_idx, key="pref_exp_select")
        with col_p2:
            selected_difficulty = st.selectbox("Difficulty", DIFFICULTY_OPTIONS, index=1, key="pref_diff_select")
        with col_p3:
            selected_qtype = st.selectbox("Question Type", QUESTION_TYPE_OPTIONS, index=7, key="pref_qtype_select")
        with col_p4:
            selected_count = st.selectbox("Number of Questions", QUESTION_COUNT_OPTIONS, index=1, key="pref_count_select")

        if st.button("💾 Save User Preference", use_container_width=True):
            clean_diff = clean_difficulty_str(selected_difficulty)
            save_user_interview_preference(user_id, selected_domain, selected_role, selected_exp, clean_diff, selected_qtype, selected_count)
            st.toast("Interview domain and preferences saved successfully!")

    # Active Resume Integration Banner (Section 11 requirement)
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 14px; margin-bottom: 20px;">
        <div style="font-weight: 700; color: #60A5FA; font-size: 1rem;">📄 Active Resume Integration Active</div>
        <div style="color: #E2E8F0; font-size: 0.9rem; margin-top: 4px;">
            <b>Active Resume:</b> {resume_data.get('active_resume_file') or 'Default Profile'} | 
            <b>Skills:</b> {', '.join((resume_data.get('skills') or [])[:5])} | 
            <b>Projects:</b> {(resume_data.get('projects') or 'N/A')[:60]}...
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Tabs
    tab_bank, tab_saved, tab_history, tab_mock = st.tabs([
        "📚 Interview Question Bank",
        "⭐ Saved Questions",
        "📜 Generation History",
        "🎤 Mock Interview (Sub-feature)"
    ])

    # Ensure questions initialized
    if "active_bank_questions" not in st.session_state:
        with st.spinner("Generating domain question bank with complete model answers..."):
            prep_res = prepare_personalized_user_interview(
                user_id=user_id,
                domain=selected_domain,
                target_role=selected_role,
                difficulty=selected_difficulty,
                question_type=selected_qtype,
                count=selected_count
            )
            st.session_state["active_session_id"] = prep_res["session_id"]
            st.session_state["active_bank_questions"] = prep_res["questions"]

    questions = st.session_state.get("active_bank_questions", [])

    # ==========================================================================
    # TAB 1: INTERVIEW QUESTION BANK (Primary Study System)
    # ==========================================================================
    with tab_bank:
        c_hdr1, c_hdr2 = st.columns([3, 1])
        with c_hdr1:
            st.subheader(f"📚 Question Bank for **{selected_domain}** ({selected_role})")
        with c_hdr2:
            if st.button("🔄 Generate New Questions", type="primary", use_container_width=True):
                with st.spinner("AI is generating a fresh question bank with model answers..."):
                    prep_res = prepare_personalized_user_interview(
                        user_id=user_id,
                        domain=selected_domain,
                        target_role=selected_role,
                        difficulty=selected_difficulty,
                        question_type=selected_qtype,
                        count=selected_count
                    )
                    st.session_state["active_session_id"] = prep_res["session_id"]
                    st.session_state["active_bank_questions"] = prep_res["questions"]
                    st.rerun()

        # Search and Filter Toolbar (Section 16 requirements)
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1:
            search_query = st.text_input("🔍 Search Interview Questions", placeholder="Search by topic (e.g. list, join, overfitting, decorator)...")
        with col_f2:
            filter_diff = st.selectbox("Filter Difficulty", ["All Difficulties", "Easy", "Medium", "Hard"])
        with col_f3:
            filter_qtype = st.selectbox("Filter Question Type", ["All Types", "Technical", "HR", "Behavioral", "Coding", "Scenario", "Project", "Resume"])

        # Global Show All / Hide All Controls (Section 15 requirements)
        col_ctl1, col_ctl2 = st.columns(2)
        with col_ctl1:
            if st.button("Show All Answers", use_container_width=True):
                for i, q in enumerate(questions, 1):
                    q_text = q.get("question", "")
                    st.session_state[f"show_ans_{i}_{abs(hash(q_text)) % 1000000}"] = True
                st.rerun()

        with col_ctl2:
            if st.button("Hide All Answers", use_container_width=True):
                for i, q in enumerate(questions, 1):
                    q_text = q.get("question", "")
                    st.session_state[f"show_ans_{i}_{abs(hash(q_text)) % 1000000}"] = False
                st.rerun()

        st.write("---")

        # Filter & Search Logic
        filtered_qs = questions
        if search_query.strip():
            sq_lower = search_query.lower().strip()
            filtered_qs = [
                q for q in filtered_qs
                if sq_lower in q.get("question", "").lower()
                or sq_lower in q.get("model_answer", "").lower()
                or sq_lower in q.get("explanation", "").lower()
            ]

        if filter_diff != "All Difficulties":
            filtered_qs = [q for q in filtered_qs if filter_diff.lower() in q.get("difficulty", "").lower()]

        if filter_qtype != "All Types":
            filtered_qs = [q for q in filtered_qs if filter_qtype.lower() in q.get("category", "").lower() or filter_qtype.lower() in q.get("question_type", "").lower()]

        st.caption(f"Displaying **{len(filtered_qs)}** of **{len(questions)}** questions")

        if filtered_qs:
            for idx, q in enumerate(filtered_qs, 1):
                render_question_card_component(idx, len(filtered_qs), q, user_id=user_id, show_answer_default=False)
        else:
            st.warning("No questions matched your search query or filter settings.")

    # ==========================================================================
    # TAB 2: SAVED / BOOKMARKED QUESTIONS
    # ==========================================================================
    with tab_saved:
        st.subheader("⭐ Saved / Bookmarked Questions")
        saved_list = get_saved_questions(user_id)

        if saved_list:
            for sq in saved_list:
                s_id = sq.get("saved_id")
                q_text = sq.get("question", "")
                m_ans = sq.get("model_answer", "")

                with st.expander(f"⭐ {q_text[:70]}..."):
                    st.write(f"**Domain:** `{sq.get('domain')}` | **Role:** `{sq.get('target_role')}`")
                    st.info(f"**Model Answer:** {m_ans}")
                    if st.button("🗑 Remove Bookmark", key=f"del_bm_{s_id}"):
                        remove_question_bookmark(user_id, q_text)
                        st.toast("Bookmark removed!")
                        st.rerun()
        else:
            st.info("No saved questions yet. Click '⭐ Save Question' on any question card to bookmark it here!")

    # ==========================================================================
    # TAB 3: GENERATION HISTORY
    # ==========================================================================
    with tab_history:
        st.subheader("📜 Question Bank Generation History")
        history = get_user_interview_sessions_history(user_id)

        if history:
            for s in history:
                sid = s.get("session_id")
                s_domain = s.get("domain", selected_domain)
                s_role = s.get("target_role", selected_role)
                s_date = str(s.get("created_at"))[:10]

                with st.expander(f"📅 {s_date} | {s_domain} ({s_role}) | {s.get('total_questions')} Questions"):
                    st.write(f"**Difficulty:** `{s.get('difficulty')}` | **Session ID:** `{sid}`")

                    col_h1, col_h2 = st.columns(2)
                    with col_h1:
                        if st.button("👁 View Stored Q&A Bank", key=f"hist_view_{sid}"):
                            st.session_state[f"view_hist_{sid}"] = not st.session_state.get(f"view_hist_{sid}", False)
                            st.rerun()

                    with col_h2:
                        if st.button("🗑 Delete History", key=f"hist_del_{sid}"):
                            delete_interview_session(sid)
                            st.toast(f"Deleted Session #{sid} history successfully!")
                            st.rerun()

                    if st.session_state.get(f"view_hist_{sid}", False):
                        stored_qs = get_session_questions(sid)
                        st.markdown("#### 📖 Stored Question Bank Details")
                        for idx_h, sq in enumerate(stored_qs, 1):
                            st.markdown(f"**Question {idx_h}:** {sq.get('question')}")
                            st.info(f"💡 **Model Answer:** {sq.get('model_answer')}")
                            if sq.get('explanation'):
                                st.caption(f"📖 **Explanation:** {sq.get('explanation')}")
                            st.write("---")
        else:
            st.info("No saved history yet. Generate question banks to build history!")

    # ==========================================================================
    # TAB 4: MOCK INTERVIEW SUB-FEATURE
    # ==========================================================================
    with tab_mock:
        st.subheader("🎤 Mock Interview Sub-feature")
        st.caption("Practice answering live interactive questions one by one with multi-metric AI evaluation.")

        if st.button("🎤 Start Interactive Mock Interview", type="primary", use_container_width=True):
            with st.spinner("Initializing Mock Interviewer..."):
                prep_res = prepare_personalized_user_interview(
                    user_id=user_id,
                    domain=selected_domain,
                    target_role=selected_role,
                    difficulty=selected_difficulty,
                    question_type=selected_qtype,
                    count=selected_count
                )
                st.session_state["mock_session_id"] = prep_res["session_id"]
                st.session_state["mock_questions"] = prep_res["questions"]
                st.session_state["mock_q_idx"] = 0
                st.session_state["mock_evals"] = []
                st.session_state["mock_finished"] = False
                st.rerun()

        mock_qs = st.session_state.get("mock_questions", [])
        mock_idx = st.session_state.get("mock_q_idx", 0)
        mock_total = len(mock_qs)
        is_finished = st.session_state.get("mock_finished", False)

        if mock_qs and not is_finished and mock_idx < mock_total:
            mq = mock_qs[mock_idx]
            st.progress((mock_idx + 1) / mock_total)
            st.caption(f"Question **{mock_idx + 1}** of **{mock_total}** | Domain: `{selected_domain}` | Role: `{selected_role}`")

            st.markdown(f"### 🤖 Interviewer Question {mock_idx + 1}:")
            st.info(mq.get("question"))

            user_ans_mock = st.text_area("Your Response:", height=140, key=f"mock_text_{mock_idx}")

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if st.button("Submit Answer & Next ➡", use_container_width=True):
                    if not user_ans_mock.strip():
                        st.warning("Please type your response before proceeding.")
                    else:
                        eval_res = evaluate_user_interview_answer(
                            question=mq.get("question"),
                            user_answer=user_ans_mock,
                            domain=selected_domain,
                            target_role=selected_role,
                            difficulty=mq.get("difficulty", "Medium"),
                            model_answer=mq.get("model_answer", "")
                        )
                        st.session_state["mock_evals"].append(eval_res)

                        save_interview_question_response(
                            session_id=st.session_state.get("mock_session_id", 0),
                            user_id=user_id,
                            question=mq.get("question"),
                            domain=selected_domain,
                            target_role=selected_role,
                            category=mq.get("category", "Technical"),
                            difficulty=mq.get("difficulty", "Medium"),
                            model_answer=mq.get("model_answer", ""),
                            explanation=mq.get("explanation", ""),
                            example=mq.get("example", ""),
                            key_points=mq.get("key_points", []),
                            interview_tip=mq.get("interview_tip", ""),
                            user_answer=user_ans_mock,
                            user_score=eval_res.get("overall_score_pct", 70),
                            feedback=eval_res.get("feedback", "")
                        )

                        if mock_idx < mock_total - 1:
                            st.session_state["mock_q_idx"] += 1
                        else:
                            st.session_state["mock_finished"] = True
                        st.rerun()

            with col_m2:
                if st.button("🏁 End Interview & See Report", use_container_width=True):
                    st.session_state["mock_finished"] = True
                    st.rerun()

        elif is_finished or (mock_qs and mock_idx >= mock_total):
            evals = st.session_state.get("mock_evals", [])
            rpt = generate_final_interview_report(evaluations=evals, domain=selected_domain, target_role=selected_role, total_questions=mock_total)
            
            update_interview_session_results(
                session_id=st.session_state.get("mock_session_id", 0),
                score=rpt["overall_score"],
                technical_score=rpt["technical_score"],
                communication_score=rpt["communication_score"],
                readiness_score=rpt["overall_score"]
            )

            st.balloons()
            st.markdown("## 📊 Final Interview Report")
            st.success(f"Interview Readiness: **{rpt['interview_readiness']}**")

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Overall Score", f"{rpt['overall_score']}%")
            with m2:
                st.metric("Technical Score", f"{rpt['technical_score']}%")
            with m3:
                st.metric("Communication", f"{rpt['communication_score']}%")
            with m4:
                st.metric("Confidence", f"{rpt['confidence']}%")

if __name__ == "__main__":
    render_ai_interview_preparation_page()
