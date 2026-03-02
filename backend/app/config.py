"""Application configuration via environment variables."""

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve backend/.env so it's found whether the app is run from repo root or backend/
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_ENV_FILE = _BACKEND_DIR / ".env"


class Settings(BaseSettings):
    """Settings loaded from env (e.g. backend/.env)."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE if _ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, validation_alias="ANTHROPIC_API_KEY")
    openrouter_api_key: str | None = Field(default=None, validation_alias="OPENROUTER_API_KEY")
    tavily_api_key: str | None = Field(default=None, validation_alias="TAVILY_API_KEY")

    port: int = 8001
    # Max LLM request rounds per run. Keep low so agent does 1–2 searches, a few fetches, then reports.
    max_agent_steps: int = 30
    http_timeout_seconds: float = 30.0

    # Search (Tavily): max results per query and max chars per result snippet
    search_max_results: int = 5
    search_description_max_len: int = 3000

    # Default LLM: used when the request does not specify provider/model
    default_llm_provider: str | None = None  # e.g. openai, anthropic, openrouter
    default_llm_model: str | None = None  # e.g. gpt-4o, claude-3-5-sonnet, openai/gpt-4o (OpenRouter)

    def apply_to_env(self) -> None:
        """Set API key settings into os.environ so os.getenv() and libraries see them."""
        env_vars = [
            ("OPENAI_API_KEY", self.openai_api_key),
            ("ANTHROPIC_API_KEY", self.anthropic_api_key),
            ("OPENROUTER_API_KEY", self.openrouter_api_key),
            ("TAVILY_API_KEY", self.tavily_api_key),
        ]
        for name, value in env_vars:
            if value is not None and value != "":
                os.environ[name] = value
