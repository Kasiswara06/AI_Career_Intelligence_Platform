from typing import Dict, Any
from ai_assistant.context_manager import assemble_user_context
from ai_assistant.chat_engine import process_chat_query
from ai_assistant.conversation_memory import save_chat_message

def ask_ai_career_assistant(user_id: int, user_query: str) -> Dict[str, Any]:
    """
    Main entry point for asking the AI Career Assistant:
    1. Assembles user profile & active resume context.
    2. Runs NLP Chat Engine to generate structured response.
    3. Persists conversation interaction in database.
    """
    context = assemble_user_context(user_id)
    structured_response = process_chat_query(user_query, context)

    # Persist in DB
    try:
        save_chat_message(user_id, "user", user_query)
        save_chat_message(user_id, "assistant", structured_response.get("answer", ""), structured_response)
    except Exception:
        pass

    return structured_response
