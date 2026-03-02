"""System prompt and other prompt assets for the research agent."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_prompt.txt"


def load_system_prompt() -> str:
    """Load the research agent system prompt from the prompts directory."""
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
