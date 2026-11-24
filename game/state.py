"""Mutable game state. Only the engine writes to it.

Mirrors World §5.2 (``world_state``) and Evidence §10.3 (``investigation_state``), plus persisted
NPC claims (Evidence §7.4), conversation history and the journal-relevant bookkeeping.
Everything here is JSON-serialisable via :meth:`GameState.to_dict`.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .content import Content


@dataclass
class Claim:
    """A statement an NPC made in play, stored so later contradictions can be checked (Evidence §7.4)."""

    speaker: str
    topic: str
    text: str
    turn: int
    tbd: bool = False


@dataclass
class GameState:
    location: str
    world: dict[str, Any]
    flags: dict[str, bool]
    private_cabin_search_authorized: list[str]
    npc_locations: dict[str, str]
    collected_evidence_ids: list[str] = field(default_factory=list)
    reviewed_evidence_ids: list[str] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    accusations_made: list[dict] = field(default_factory=list)
    completed_interactions: list[str] = field(default_factory=list)
    active_leads: list[str] = field(default_factory=list)
    conversations: dict[str, list[dict]] = field(default_factory=dict)
    turn: int = 0
    game_over: bool = False
    ending: str | None = None

    # ------------------------------------------------------------------ construction

    @classmethod
    def initial(cls, content: Content) -> "GameState":
        rules = content.rules
        init = rules.get("initial_state", {})
        flags = {name: bool(v) for name, v in (init.get("flags") or {}).items()}
        for name, spec in (rules.get("tbd_flags") or {}).items():
            flags[name] = bool(spec.get("value", False))
        state = cls(
            location=rules["start"]["location"],
            world=dict(init.get("world") or {}),
            flags=flags,
            private_cabin_search_authorized=list(init.get("private_cabin_search_authorized") or []),
            npc_locations={npc.id: npc.default_location for npc in content.npcs.values()},
        )
        state.collected_evidence_ids = list(rules["start"].get("evidence", []))
        return state

    # ------------------------------------------------------------------ ConditionContext

    def flag(self, name: str) -> bool:
        return bool(self.flags.get(name, False))

    def has_collected(self, evidence_id: str) -> bool:
        return evidence_id in self.collected_evidence_ids

    def has_reviewed(self, evidence_id: str) -> bool:
        return evidence_id in self.reviewed_evidence_ids

    def has_claim(self, speaker: str, topic: str) -> bool:
        return any(c.speaker == speaker and c.topic == topic for c in self.claims)

    def cabin_authorized(self, cabin_id: str) -> bool:
        return cabin_id in self.private_cabin_search_authorized

    def world_value(self, key: str) -> Any:
        return self.world.get(key)

    def npc_present(self, npc_id: str) -> bool:
        return self.npc_locations.get(npc_id) == self.location

    # ------------------------------------------------------------------ persistence

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        data = dict(data)
        data["claims"] = [Claim(**c) for c in data.get("claims", [])]
        return cls(**data)
