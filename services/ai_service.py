from openai import OpenAI
from config.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
def get_ai_reply(user_message: str) -> str:
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
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Sorry, I couldn't process your question. Error: {str(e)}"
