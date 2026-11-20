"""Google Gemini client using the public REST ``generateContent`` endpoint (no SDK needed)."""

from __future__ import annotations

import logging
import time
from typing import Callable

import httpx

from game.llm import LLMError

from ._http import post_json

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

log = logging.getLogger(__name__)


class GeminiClient:
    name = "gemini"

    def __init__(
        self,
        api_key: str,
        model: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 400,
        thinking_level: str | None = "minimal",
        timeout: float = 60.0,
        retries: int = 2,
        backoff: float = 1.5,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        """``thinking_level``: Gemini 3.x thinking tokens count against ``max_tokens``; with the
        model default, a 400-token budget was used up by thinking and replies were cut off
        mid-sentence. "minimal" keeps short dialogue fast and complete. ``None`` omits the setting
        (needed for models that don't support thinkingLevel)."""
        if not api_key:
            raise ValueError("Gemini API key is missing")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.thinking_level = thinking_level
        self.retries = retries
        self.backoff = backoff
        self._sleep = sleep
        self._api_key = api_key
        self._http = httpx.Client(timeout=timeout, transport=transport)

    def chat(self, system_prompt: str, messages: list[dict]) -> str:
        contents = [
            {"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
            for m in messages
        ]
        generation_config: dict = {"temperature": self.temperature, "maxOutputTokens": self.max_tokens}
        if self.thinking_level:
            generation_config["thinkingConfig"] = {"thinkingLevel": self.thinking_level}
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": generation_config,
        }
        # Key goes in a header, not the URL, so it never ends up in logs of request URLs.
        headers = {"x-goog-api-key": self._api_key}
        data = post_json(
            self._http, GEMINI_URL.format(model=self.model), payload, headers,
            provider="Gemini", retries=self.retries, backoff=self.backoff, sleep=self._sleep,
        )
        candidates = data.get("candidates") or []
        if not candidates:
            raise LLMError(f"Gemini returned no candidates: {data.get('promptFeedback', data)}")
        if candidates[0].get("finishReason") == "MAX_TOKENS":
            usage = data.get("usageMetadata", {})
            log.warning(
                "Gemini reply cut off at max tokens (thinking=%s, output=%s); raise LLM_MAX_TOKENS "
                "or lower GEMINI_THINKING_LEVEL", usage.get("thoughtsTokenCount"), usage.get("candidatesTokenCount"),
            )
        parts = (candidates[0].get("content") or {}).get("parts") or []
        return "".join(p.get("text", "") for p in parts if not p.get("thought"))
