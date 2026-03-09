from services.llama_service import get_llama_reply
from services.openai_service import get_openai_reply

def get_ai_reply(user_message: str) -> tuple[str, int]:
    """Legacy function - defaults to OpenAI"""
    return get_openai_reply(user_message)

def generate_ai_reply(model: str, message: str):
    
    if model == "openai":
        return get_openai_reply(message)
    
    elif model == "llama":
        reply = get_llama_reply(message)
        return reply, 0   # no token tracking for local model
    
    else:
        return "Model not supported", 0
