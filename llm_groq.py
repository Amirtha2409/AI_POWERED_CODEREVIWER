from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def llm_review(code):
    prompt = f"""
    You are an AI Code Reviewer.
    Analyze the following Python code.
    Give:
    1. Code Quality feedback
    2. Improvements
    3. Security issues
    4. Best practices suggestions

    Code:
    {code}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content