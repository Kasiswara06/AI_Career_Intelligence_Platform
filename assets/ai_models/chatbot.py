from ai_assistant.assistant import ask_ai_career_assistant

def get_chatbot_response(user_id: int, query: str) -> dict:
    """Wrapper function for chatbot module compatibility."""
    return ask_ai_career_assistant(user_id, query)
