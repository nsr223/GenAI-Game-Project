"""The one interface the engine needs from a language model.

Implementations live in ``backend/llm/`` (OpenRouter, Gemini, FakeLLM). The engine never imports
them, so it stays testable without network access.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class LLMError(RuntimeError):
    """Raised by LLM clients for any provider/network failure."""


@runtime_checkable
class LLMClient(Protocol):
    def chat(self, system_prompt: str, messages: list[dict]) -> str:
        """Return the assistant reply.

        ``messages`` is a list of ``{"role": "user" | "assistant", "content": str}`` in order.
        Raise :class:`LLMError` on failure.
        """
        ...
