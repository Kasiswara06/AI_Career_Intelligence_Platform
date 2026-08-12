import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def generate_llm_response(prompt: str, system_context: str = "") -> Dict[str, Any]:
    """
    Multi-provider LLM client:
    1. Tries Google Gemini API (if GEMINI_API_KEY / GOOGLE_API_KEY environment variable is set)
    2. Tries OpenAI API (if OPENAI_API_KEY environment variable is set)
    3. Tries Ollama local model (if local server running)
    4. Falls back to deterministic intelligent Career AI NLP engine.
    """
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # 1. Google Gemini API
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            full_prompt = f"{system_context}\n\nUser Question:\n{prompt}"
            response = model.generate_content(full_prompt)
            if response and response.text:
                return {"provider": "Google Gemini API", "text": response.text}
        except Exception as e:
            logger.warning(f"Gemini API execution note: {e}")

    # 2. OpenAI API
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": prompt}
                ]
            )
            text = completion.choices[0].message.content
            if text:
                return {"provider": "OpenAI API", "text": text}
        except Exception as e:
            logger.warning(f"OpenAI API execution note: {e}")

    # 3. Ollama Local Model
    try:
        import urllib.request
        import json
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({
                "model": "llama3",
                "prompt": f"{system_context}\n\n{prompt}",
                "stream": False
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if "response" in data:
                return {"provider": "Ollama Local (LLaMA3)", "text": data["response"]}
    except Exception:
        pass

    # 4. Fallback: Intelligent Career & Technical NLP Engine
    return {"provider": "Platform Career AI (NLP Engine)", "text": None}
