from utils.gemini import generate_content
from string import Template

def extract_requirements(pdf_text: str) -> str:
    with open("prompts/extract_requirements.txt") as f:
        template = Template(f.read())
    
    prompt = template.substitute(document_text=pdf_text)
    return generate_content(prompt, temperature=0.1)