"""Read ``.env`` and build the configured LLM client.

Environment variables (see .env.example):
    LLM_PROVIDER        openrouter | gemini | fake   (default: openrouter)
    OPENROUTER_API_KEY, OPENROUTER_MODEL
    GEMINI_API_KEY, GEMINI_MODEL
    GEMINI_THINKING_LEVEL  minimal (default) | low | medium | high | none (= omit, model default)
    LLM_TEMPERATURE     default 0.7
    LLM_MAX_TOKENS      default 400
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from pathlib import Path

from dotenv import load_dotenv

from game.llm import LLMClient

from .llm import FakeLLM, GeminiClient, OpenRouterClient

log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OPENROUTER_MODEL = "anthropic/claude-haiku-5.5"
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"


def make_llm(env: Mapping[str, str] | None = None) -> tuple[LLMClient, str]:
    """Return ``(client, description)``. Falls back to :class:`FakeLLM` if no key is configured."""
    if env is None:
        load_dotenv(REPO_ROOT / ".env")
        env = os.environ
    provider = (env.get("LLM_PROVIDER") or "openrouter").strip().lower()
    temperature = float(env.get("LLM_TEMPERATURE") or 0.7)
    max_tokens = int(env.get("LLM_MAX_TOKENS") or 400)

    if provider == "fake":
        return FakeLLM(), "FakeLLM (LLM_PROVIDER=fake)"
    if provider == "openrouter":
        key = env.get("OPENROUTER_API_KEY", "").strip()
        model = (env.get("OPENROUTER_MODEL") or DEFAULT_OPENROUTER_MODEL).strip()
        if key:
            client = OpenRouterClient(key, model, temperature=temperature, max_tokens=max_tokens)
            return client, f"OpenRouter ({model})"
    elif provider == "gemini":
        key = env.get("GEMINI_API_KEY", "").strip()
        model = (env.get("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()
        thinking = env.get("GEMINI_THINKING_LEVEL", "minimal").strip().lower()
        thinking_level = None if thinking in ("", "none", "default") else thinking
        if key:
            client = GeminiClient(
                key, model, temperature=temperature, max_tokens=max_tokens, thinking_level=thinking_level,
            )
            return client, f"Gemini ({model})"
    else:
        raise ValueError(f"Unknown LLM_PROVIDER {provider!r} (use openrouter, gemini or fake)")

    log.warning("No API key for LLM_PROVIDER=%s; falling back to FakeLLM", provider)
    return FakeLLM(), f"FakeLLM (no API key for {provider})"
