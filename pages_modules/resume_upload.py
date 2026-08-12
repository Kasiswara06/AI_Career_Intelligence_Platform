import streamlit as st
from services.resume_service import process_and_save_resume

def render_resume_upload_page():
    st.header("📄 Resume Upload")
    st.caption("Upload your resume in PDF, DOCX, or TXT format for automatic AI extraction and parsing.")

    uploaded_file = st.file_uploader("Choose a Resume file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        if st.button("Process & Parse Resume", type="primary", use_container_width=True):
            user_id = st.session_state.get("user_id", 1)
            with st.spinner("Extracting text, contact details, and technical skills..."):
                data = process_and_save_resume(user_id, uploaded_file)
                st.success("Resume processed successfully!")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Email:** {data.get('email', 'N/A')}")
                    st.markdown(f"**Phone:** {data.get('phone', 'N/A')}")
                    st.markdown(f"**Experience:** {data.get('experience_years', 0.0)} Years")
                with c2:
                    st.markdown(f"**LinkedIn:** {data.get('linkedin', 'N/A')}")
                    st.markdown(f"**GitHub:** {data.get('github', 'N/A')}")
                
                st.write("---")
                st.subheader("Extracted Skills")
                st.write(", ".join(data.get("skills", [])))

if __name__ == "__main__":
    render_resume_upload_page()
