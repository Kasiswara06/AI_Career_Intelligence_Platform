from typing import Dict, Any
from ai_assistant.context_manager import extract_user_career_context
from ai_assistant.prompt_builder import build_system_context_prompt
from ai_assistant.llm_client import generate_llm_response
from ai_assistant.response_formatter import format_ai_career_response
from ai_assistant.conversation_memory import append_to_session_memory

def process_chatbot_query(user_id: int, session_id: str, question: str) -> Dict[str, Any]:
    """
    Main Chatbot Execution Engine:
    1. Extracts candidate profile, active resume, ATS scores & skill gap context.
    2. Builds system prompt.
    3. Executes multi-provider LLM client (Gemini/OpenAI/Ollama/Fallback).
    4. Formats structured 7-part output.
    5. Saves interaction into session memory and database.
    """
    context_data = extract_user_career_context(user_id)
    system_prompt = build_system_context_prompt(context_data)
    
    llm_res = generate_llm_response(question, system_context=system_prompt)
    raw_text = llm_res.get("text", "")
    
    formatted_response = format_ai_career_response(raw_text, question, context_data)
    formatted_response["provider"] = llm_res.get("provider", "Platform Career AI")
    
    # Save into memory
    append_to_session_memory(session_id, question, formatted_response["answer"])

    return formatted_response
