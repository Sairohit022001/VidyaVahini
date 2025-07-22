import os

PROMPT_DIR = os.path.join(os.path.dirname(__file__), '../prompts')

def load_prompt(filename: str) -> str:
    path = os.path.abspath(os.path.join(PROMPT_DIR, filename))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

