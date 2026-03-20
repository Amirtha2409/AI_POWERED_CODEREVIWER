import os
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_ai_docstring(name, params, style="google", model_type="Groq (Llama 3.3)", tone="Professional"):
    # 1. Define specific rules for each style
    style_rules = {
        "google": "Use Google Style: include 'Args:', 'Returns:', and 'Raises:' sections with 4-space indentation.",
        "numpy": "Use NumPy Style: include 'Parameters' and 'Returns' sections with underlined headers (---).",
        "rst": "Use reStructuredText (reST) Style: use :param name: and :return: fields."
    }
    
    # 2. Define specific rules for each tone
    tone_rules = {
        "Professional": "Write in a formal, technical, and objective tone.",
        "Short": "Keep it extremely concise. Only include the bare essentials.",
        "Detailed": "Provide exhaustive explanations for every parameter and the return value."
    }

    selected_style = style_rules.get(style.lower(), style_rules["google"])
    selected_tone = tone_rules.get(tone, tone_rules["Professional"])

    # 3. Build the Dynamic Prompt
    prompt = f"""
    Generate a Python docstring for the function '{name}' with parameters: {', '.join(params)}.
    
    STRICT GUIDELINES:
    - STYLE: {selected_style}
    - TONE: {selected_tone}
    - Output ONLY the docstring starting and ending with triple quotes.
    - Do not include any introductory text like 'Here is your docstring'.
    """

    try:
        # Determine which API to use
        if "Groq" in model_type:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            model_id = "llama-3.3-70b-versatile" # Use the latest stable ID
        else:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model_id = "gpt-4o"

        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3 # Lower temperature ensures stricter formatting
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"