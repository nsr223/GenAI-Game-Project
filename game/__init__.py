"""Deterministic game engine for *Beneath the Surface*.

The engine owns all game state. LLMs only voice characters (see ``game.llm.LLMClient``).
Public API: :class:`Game` and :class:`ActionResult` (documented in docs/engine-api.md).
"""

from .content import Content, ContentError, load_content
from .engine import ActionResult, Game
from .llm import LLMClient, LLMError

__all__ = ["ActionResult", "Content", "ContentError", "Game", "LLMClient", "LLMError", "load_content"]
