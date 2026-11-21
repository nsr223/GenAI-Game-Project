"""OpenRouter chat-completions client (OpenAI-compatible API)."""

from __future__ import annotations

import time
from typing import Callable

import httpx

from game.llm import LLMError

from ._http import post_json

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterClient:
    name = "openrouter"

    def __init__(
        self,
        api_key: str,
        model: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 400,
        timeout: float = 60.0,
        retries: int = 2,
        backoff: float = 1.5,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        if not api_key:
            raise ValueError("OpenRouter API key is missing")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retries = retries
        self.backoff = backoff
        self._sleep = sleep
        self._api_key = api_key
        self._http = httpx.Client(timeout=timeout, transport=transport)

    def chat(self, system_prompt: str, messages: list[dict]) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}, *messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        headers = {"Authorization": f"Bearer {self._api_key}"}
        data = post_json(
            self._http, OPENROUTER_URL, payload, headers,
            provider="OpenRouter", retries=self.retries, backoff=self.backoff, sleep=self._sleep,
        )
        if "error" in data:
            raise LLMError(f"OpenRouter error: {data['error']}")
        try:
            return data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected OpenRouter response: {str(data)[:200]}") from exc
