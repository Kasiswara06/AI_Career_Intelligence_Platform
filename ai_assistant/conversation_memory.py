import streamlit as st
from typing import List, Dict, Any

def get_session_memory(session_id: str) -> List[Dict[str, str]]:
    """Retrieves in-memory conversation history for active session."""
    key = f"chat_memory_{session_id}"
    if key not in st.session_state:
        st.session_state[key] = []
    return st.session_state[key]

def append_to_session_memory(session_id: str, question: str, answer: str):
    """Appends question and answer to active session memory."""
    memory = get_session_memory(session_id)
    memory.append({"role": "user", "content": question})
    memory.append({"role": "assistant", "content": answer})

def clear_session_memory(session_id: str):
    """Clears in-memory history for active session."""
    key = f"chat_memory_{session_id}"
    if key in st.session_state:
        st.session_state[key] = []
