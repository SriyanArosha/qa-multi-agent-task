from utils.gemini import generate_content
from string import Template

PROMPT_TEMPLATE = """
Based on the following testable requirements, write complete, high-quality Playwright **synchronous** Python test code.

Rules:
- Use pytest style (test_ functions)
- Use fixtures if helpful
- Assume base_url is given via --base-url or env
- Use good selectors (role, text, test-id when possible)
- Handle waits properly (wait_for_selector, wait_for_load_state, etc.)
- Cover happy path + mentioned edge cases
- Include comments explaining non-obvious parts

Previous feedback to incorporate:
{{feedback}}

Requirements:
{{requirements}}

Output **only** the Python code (no markdown, no explanation).
"""

def generate_playwright_code(requirements: str, previous_feedback: str = "") -> str:
    with open("prompts/generate_playwright.txt") as f:
        template = Template(f.read() if 'feedback' in f.read() else PROMPT_TEMPLATE)
    
    prompt = template.substitute(requirements=requirements, feedback=previous_feedback)
    raw = generate_content(prompt, temperature=0.3)
    
    # Clean up common markdown fences
    if raw.startswith("```python"):
        raw = raw.split("```python", 1)[1].rsplit("```", 1)[0]
    return raw.strip()