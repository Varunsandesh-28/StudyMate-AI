
import requests
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma3:1b"

SKILL_FILE = Path(__file__).with_name("Skill.md")


def load_skills():
    if SKILL_FILE.exists():
        return SKILL_FILE.read_text(encoding="utf-8")

    return "Explain concepts clearly and honestly."


def ask_ai(prompt: str, timeout: int = 180) -> str:
    skills = load_skills()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "system": skills,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        },
        timeout=timeout
    )

    response.raise_for_status()
    data = response.json()

    return data.get("response", "").strip()
