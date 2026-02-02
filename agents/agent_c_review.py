from utils.gemini import generate_content
from string import Template

def review_code(code: str, requirements: str) -> str:
    with open("prompts/review_code.txt", encoding="utf-8") as f:
        template = Template(f.read())
    
    prompt = template.substitute(code=code, requirements=requirements)
    return generate_content(prompt, temperature=0.15)