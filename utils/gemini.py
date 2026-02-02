import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash"

def get_model():
    return genai.GenerativeModel(MODEL)

def generate_content(prompt: str, temperature: float = 0.2) -> str:
    model = get_model()
    response = model.generate_content(
        prompt,
        generation_config={"temperature": temperature, "max_output_tokens": 8192}
    )
    return response.text.strip()