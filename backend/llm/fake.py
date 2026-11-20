"""A deterministic stand-in for a real LLM. Used by all tests and as the no-key fallback."""

from __future__ import annotations

from typing import Callable


class FakeLLM:
    """Returns scripted replies and records every call for assertions.

    replies    replies returned in order; once exhausted, ``default`` is returned
    responder  optional ``f(system_prompt, messages) -> str`` used instead of the script
    """

    name = "fake"

    def __init__(
        self,
        replies: list[str] | None = None,
        default: str = "(FakeLLM) I'd rather not say more right now.",
        responder: Callable[[str, list[dict]], str] | None = None,
    ):
        self.replies = list(replies or [])
        self.default = default
        self.responder = responder
        self.calls: list[dict] = []

    def chat(self, system_prompt: str, messages: list[dict]) -> str:
        self.calls.append({"system_prompt": system_prompt, "messages": [dict(m) for m in messages]})
        if self.responder is not None:
            return self.responder(system_prompt, messages)
        if self.replies:
            return self.replies.pop(0)
        return self.default

    @property
    def last_system_prompt(self) -> str:
        return self.calls[-1]["system_prompt"] if self.calls else ""
