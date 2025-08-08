import json
from pathlib import Path

def load_prompt(path: str) -> str:
    return Path(path).read_text()

def inject_variables(prompt: str, variables: dict) -> str:
    for key, value in variables.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", json.dumps(value, indent=2) if isinstance(value, (dict, list)) else str(value))
    return prompt
