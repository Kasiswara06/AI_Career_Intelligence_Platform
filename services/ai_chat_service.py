import logging
from typing import Dict, Any, List
from ai_assistant.chatbot import process_chatbot_query
from database.database import (
    save_chat_message,
    get_chat_session_messages,
    log_activity
)
from utils.export_chat import export_chat_to_txt, export_chat_to_pdf

logger = logging.getLogger(__name__)

def handle_user_chat_message(user_id: int, session_id: str, session_title: str, question: str) -> Dict[str, Any]:
    """
    Orchestrates user message handling:
    1. Executes chatbot query pipeline
    2. Saves message into chat_history table
    3. Logs activity
    """
    response = process_chatbot_query(user_id, session_id, question)
    
    # Save into DB
    save_chat_message(
        user_id=user_id,
        session_id=session_id,
        question=question,
        answer=response["answer"],
        session_title=session_title
    )

    log_activity(user_id, "AI Chat Query", f"Asked AI Assistant: '{question[:40]}...'")
    return response

def fetch_session_conversation(user_id: int, session_id: str) -> List[Dict[str, Any]]:
    """Fetches messages for session."""
    return get_chat_session_messages(user_id, session_id)

def get_session_export_data(session_title: str, messages: List[Dict[str, Any]]) -> Tuple_Or_Dict:
    """Generates TXT and PDF export payloads."""
    txt = export_chat_to_txt(session_title, messages)
    pdf_bytes = export_chat_to_pdf(session_title, messages)
    return {"txt": txt, "pdf": pdf_bytes}
