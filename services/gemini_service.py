import google.generativeai as genai
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def _pick_gemini_model() -> str:
    """Pick a generateContent-capable Gemini model with stable preference order."""
    preferred = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]

    available = {
        m.name.replace("models/", "")
        for m in genai.list_models()
        if "generateContent" in getattr(m, "supported_generation_methods", [])
    }

    for candidate in preferred:
        if candidate in available:
            return candidate

    if available:
        return sorted(available)[0]

    raise RuntimeError("No Gemini models with generateContent support are available for this API key")


def get_gemini_reply(user_message: str) -> tuple[str, int, str]:
    # Detect if student is asking for simpler explanation
    simplify_keywords = ["didn't understand", "don't understand", "explain more", 
                         "explain simply", "simpler", "confused", "example"]
    needs_simplification = any(keyword in user_message.lower() for keyword in simplify_keywords)
    
    simplification_note = ""
    if needs_simplification:
        simplification_note = """STUDENT IS CONFUSED - USE EXTRA SIMPLE LANGUAGE:
• Avoid ALL technical jargon
• Use everyday analogies
• Give multiple simple examples
• Break into very small steps
"""
    
    prompt = f"""
You are a friendly AI Tutor helping students learn step-by-step.

{simplification_note}

FORMAT RULES:
• Start with a simple definition (1-2 sentences)
• Then explain how it works
• Then give a practical example
• Use bullet points for clarity
• Keep answer under 200 words
• End with encouragement

TEACHING STYLE:
• Explain in simple language
• Give real-world examples
• If topic is complex, break into steps
• Use analogies when helpful

STUDENT QUESTION:
{user_message}
"""
    
    try:
        model_name = _pick_gemini_model()
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        
        reply = response.text
        
        # Gemini provides token count in the response
        if hasattr(response, 'usage_metadata'):
            tokens_used = response.usage_metadata.total_token_count
        else:
            tokens_used = len(reply) // 4
        
        return reply, tokens_used, model_name
    
    except Exception as e:
        error_message = f"Sorry, I couldn't process your question. Error: {str(e)}"
        return error_message, 0, "gemini_error"
