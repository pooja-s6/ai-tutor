from services.llama_service import get_llama_reply
from services.openai_service import get_openai_reply
from services.gemini_service import get_gemini_reply

def get_ai_reply(user_message: str) -> tuple[str, int]:
    """Legacy function - defaults to OpenAI"""
    return get_openai_reply(user_message)

def generate_ai_reply(model: str, message: str):
    normalized_model = (model or "").strip().lower()

    if normalized_model == "openai":
        reply, tokens = get_openai_reply(message)
        return reply, tokens, "gpt-4o-mini"

    if normalized_model == "llama":
        reply = get_llama_reply(message)
        return reply, 0, "llama3"  # no token tracking for local model

    if normalized_model == "gemini":
        reply, tokens, resolved_model = get_gemini_reply(message)
        return reply, tokens, resolved_model

    return "Model not supported", 0, "unsupported"
