import streamlit as st
import uuid
import datetime
from services.ai_chat_service import (
    handle_user_chat_message,
    fetch_session_conversation
)
from ai_assistant.history_manager import (
    get_grouped_chat_sessions,
    update_session_title,
    remove_session,
    favorite_session
)
from utils.export_chat import export_chat_to_txt, export_chat_to_pdf

def render_ai_career_assistant_page():
    """Renders the commercial-grade Real AI Career Assistant Chatbot."""
    st.title("🤖 AI Career Assistant & Real-Time Chatbot")
    st.caption("Powered by Google Gemini / OpenAI / Ollama / Platform NLP Engine with multi-turn memory, context awareness, and date-grouped history.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to access the AI Career Assistant.")
        st.stop()

    # Session State Initialization
    if "current_session_id" not in st.session_state:
        st.session_state["current_session_id"] = f"SESS-{uuid.uuid4().hex[:8].upper()}"
    if "current_session_title" not in st.session_state:
        st.session_state["current_session_title"] = "New Chat Session"
    if "active_query_trigger" not in st.session_state:
        st.session_state["active_query_trigger"] = None
    if "search_chat_query" not in st.session_state:
        st.session_state["search_chat_query"] = ""

    session_id = st.session_state["current_session_id"]

    # ----------------------------------------------------
    # SIDEBAR – CHAT HISTORY & DATE GROUPING
    # ----------------------------------------------------
    with st.sidebar:
        st.markdown("## 💬 Chat History")
        
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state["current_session_id"] = f"SESS-{uuid.uuid4().hex[:8].upper()}"
            st.session_state["current_session_title"] = "New Chat Session"
            st.session_state["active_query_trigger"] = None
            st.rerun()

        st.markdown("---")
        search_term = st.text_input("🔍 Search Chats", placeholder="Filter chat titles...")
        
        grouped_sessions = get_grouped_chat_sessions(user_id, search_query=search_term)

        for group_name, sess_list in grouped_sessions.items():
            if sess_list:
                st.markdown(f"**{group_name}**")
                for s in sess_list:
                    s_id = s["session_id"]
                    s_title = s.get("session_title", "Chat Session")
                    is_fav = bool(s.get("is_favorite"))
                    fav_icon = "⭐ " if is_fav else ""
                    
                    is_active = (s_id == session_id)
                    btn_label = f"{fav_icon}💬 {s_title[:22]}"

                    c_btn, c_opt = st.columns([4, 1])
                    with c_btn:
                        if st.button(btn_label, key=f"sess_select_{s_id}", use_container_width=True):
                            st.session_state["current_session_id"] = s_id
                            st.session_state["current_session_title"] = s_title
                            st.rerun()
                    
                    with c_opt:
                        with st.popover("⚙️"):
                            st.caption(f"Session: `{s_id}`")
                            new_name = st.text_input("Rename Chat", value=s_title, key=f"rename_in_{s_id}")
                            if st.button("Save Name", key=f"save_name_{s_id}"):
                                update_session_title(user_id, s_id, new_name)
                                st.session_state["current_session_title"] = new_name
                                st.rerun()

                            if st.button("⭐ Toggle Favorite" if not is_fav else "❌ Remove Favorite", key=f"fav_toggle_{s_id}"):
                                favorite_session(user_id, s_id, not is_fav)
                                st.rerun()

                            if st.button("🗑️ Delete Session", key=f"del_sess_{s_id}"):
                                remove_session(user_id, s_id)
                                if st.session_state["current_session_id"] == s_id:
                                    st.session_state["current_session_id"] = f"SESS-{uuid.uuid4().hex[:8].upper()}"
                                    st.session_state["current_session_title"] = "New Chat Session"
                                st.rerun()
                st.write("---")

    # ----------------------------------------------------
    # MAIN CHAT HEADER & SUGGESTED QUESTIONS
    # ----------------------------------------------------
    st.markdown(f"### 💬 Session: `{st.session_state['current_session_title']}`")
    
    st.markdown("##### 💡 Suggested Questions")
    sug_cols = st.columns(4)
    suggested_queries = [
        "Review my Resume",
        "Explain ATS Score",
        "Find Matching Jobs",
        "Explain Machine Learning",
        "Explain SQL JOIN",
        "Conduct Mock Interview",
        "Predict Salary",
        "Recommend Courses"
    ]

    for idx, q in enumerate(suggested_queries):
        col_target = sug_cols[idx % 4]
        with col_target:
            if st.button(f"📌 {q}", key=f"sug_{idx}", use_container_width=True):
                st.session_state["active_query_trigger"] = q

    st.write("---")

    # ----------------------------------------------------
    # CHAT MESSAGE HISTORY CONTAINER
    # ----------------------------------------------------
    db_messages = fetch_session_conversation(user_id, session_id)

    chat_container = st.container()
    with chat_container:
        if not db_messages:
            st.info("👋 **Welcome to AI Career Assistant!** Ask any question about programming, AI/ML, resume reviews, ATS optimization, or career guidance below.")
        else:
            for msg in db_messages:
                q = msg.get("question")
                a = msg.get("answer")
                
                with st.chat_message("user", avatar="👤"):
                    st.markdown(q)

                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(a)

    # ----------------------------------------------------
    # USER INPUT ENGINE & RESPONSE GENERATION
    # ----------------------------------------------------
    user_input = st.chat_input("Ask AI Assistant any question...")
    query_to_process = user_input or st.session_state["active_query_trigger"]

    if query_to_process:
        # Reset trigger
        st.session_state["active_query_trigger"] = None
        
        # Display User Input
        with st.chat_message("user", avatar="👤"):
            st.markdown(query_to_process)

        # Generate Response with Animation
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI Assistant is analyzing context and generating structured response..."):
                if st.session_state["current_session_title"] == "New Chat Session":
                    auto_title = query_to_process[:25] + "..." if len(query_to_process) > 25 else query_to_process
                    st.session_state["current_session_title"] = auto_title
                    update_session_title(user_id, session_id, auto_title)

                response = handle_user_chat_message(
                    user_id=user_id,
                    session_id=session_id,
                    session_title=st.session_state["current_session_title"],
                    question=query_to_process
                )

                st.caption(f"⚡ Provider: **{response.get('provider', 'Google Gemini / Platform AI')}**")
                
                # Render 7-Part Structured Response
                st.markdown(f"### 🎯 Core Answer\n{response['answer']}")
                st.markdown(f"### 📘 Detailed Explanation\n{response['explanation']}")
                st.markdown(f"### 💻 Code / Practical Example\n{response['example']}")
                st.markdown(f"### 📌 Industry Best Practice\n> {response['best_practice']}")
                st.markdown(f"### 💡 Interview Tip\n> {response['interview_tip']}")
                
                st.markdown("### 🔗 Related Topics")
                st.write(", ".join([f"`{t}`" for t in response.get("related_topics", [])]))

                st.markdown("### 🌐 Useful Resources")
                for res in response.get("resources", []):
                    st.markdown(f"- [{res['title']}]({res['url']})")

                # Action Buttons
                st.write("---")
                act_c1, act_c2, act_c3, act_c4 = st.columns(4)
                with act_c1:
                    if st.button("📋 Copy Response", key=f"copy_latest"):
                        st.toast("Response copied to clipboard!")
                with act_c2:
                    if st.button("👍 Like", key=f"like_latest"):
                        st.toast("Thanks for your feedback!")
                with act_c3:
                    txt_data = export_chat_to_txt(st.session_state["current_session_title"], db_messages)
                    st.download_button("📥 Export TXT", txt_data, file_name=f"{session_id}.txt", mime="text/plain", key="dl_txt")
                with act_c4:
                    pdf_data = export_chat_to_pdf(st.session_state["current_session_title"], db_messages)
                    st.download_button("📥 Export PDF", pdf_data, file_name=f"{session_id}.pdf", mime="application/pdf", key="dl_pdf")

        st.rerun()

if __name__ == "__main__":
    render_ai_career_assistant_page()
