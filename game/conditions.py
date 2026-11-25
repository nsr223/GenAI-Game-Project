"""A tiny, deterministic condition language shared by all data files.

Conditions are plain YAML values:

    always / {} / null            -> true
    "some_flag"                   -> flag is true
    [c1, c2]                      -> shorthand for all_of
    {all_of: [c1, c2]}
    {any_of: [c1, c2]}
    {not: c}
    {evidence_collected: EV-09}
    {evidence_reviewed: EV-09}
    {claim_recorded: {speaker: maya_chen, topic: whereabouts_critical_window}}
    {cabin_authorized: cabin_elena}
    {world_equals: {weather: severe}}
    {npc_present: olivia_hart}    -> NPC is in the player's current location
    {noticed: engineering_maintenance_terminal}
                                  -> the player inspected this object or tried to enter this location
    {mentioned: {npc: sarah_morgan, about: engineering_records}}
                                  -> the player's own message to that NPC used a word of that keyword group
    {completed: ask_olivia_initial_observations}
                                  -> that interaction has succeeded

The engine evaluates these; an LLM never does.
"""

from __future__ import annotations

from typing import Any, Iterator, Protocol


class ConditionError(ValueError):
    """Raised for malformed conditions."""


class ConditionContext(Protocol):
    """What a condition can ask about. Implemented by :class:`game.state.GameState`."""

    def flag(self, name: str) -> bool: ...
    def has_collected(self, evidence_id: str) -> bool: ...
    def has_reviewed(self, evidence_id: str) -> bool: ...
    def has_claim(self, speaker: str, topic: str) -> bool: ...
    def cabin_authorized(self, cabin_id: str) -> bool: ...
    def world_value(self, key: str) -> Any: ...
    def npc_present(self, npc_id: str) -> bool: ...
    def has_noticed(self, thing_id: str) -> bool: ...
    def has_mentioned(self, npc_id: str, group: str) -> bool: ...
    def has_completed(self, interaction_id: str) -> bool: ...


LEAF_KEYS = {
    "evidence_collected",
    "evidence_reviewed",
    "claim_recorded",
    "cabin_authorized",
    "world_equals",
    "npc_present",
    "noticed",
    "mentioned",
    "completed",
}
GROUP_KEYS = {"all_of", "any_of", "not"}


def is_trivially_true(cond: Any) -> bool:
    return cond is None or cond == "always" or cond == {} or cond == []


def evaluate(cond: Any, ctx: ConditionContext) -> bool:
    """Evaluate ``cond`` against ``ctx``."""
    if is_trivially_true(cond):
        return True
    if isinstance(cond, str):
        return ctx.flag(cond)
    if isinstance(cond, list):
        return all(evaluate(c, ctx) for c in cond)
    if not isinstance(cond, dict) or len(cond) != 1:
        raise ConditionError(f"A condition must be a string, list or single-key mapping: {cond!r}")

    (key, value), = cond.items()
    if key == "all_of":
        return all(evaluate(c, ctx) for c in _as_list(value, key))
    if key == "any_of":
        return any(evaluate(c, ctx) for c in _as_list(value, key))
    if key == "not":
        return not evaluate(value, ctx)
    if key == "evidence_collected":
        return ctx.has_collected(value)
    if key == "evidence_reviewed":
        return ctx.has_reviewed(value)
    if key == "claim_recorded":
        _require_keys(value, {"speaker", "topic"}, key)
        return ctx.has_claim(value["speaker"], value["topic"])
    if key == "cabin_authorized":
        return ctx.cabin_authorized(value)
    if key == "world_equals":
        if not isinstance(value, dict) or not value:
            raise ConditionError(f"world_equals needs a mapping: {value!r}")
        return all(ctx.world_value(k) == v for k, v in value.items())
    if key == "npc_present":
        return ctx.npc_present(value)
    if key == "noticed":
        return ctx.has_noticed(value)
    if key == "mentioned":
        _require_keys(value, {"npc", "about"}, key)
        return ctx.has_mentioned(value["npc"], value["about"])
    if key == "completed":
        return ctx.has_completed(value)
    raise ConditionError(f"Unknown condition key {key!r}")


def iter_references(cond: Any) -> Iterator[tuple[str, Any]]:
    """Yield ``(kind, value)`` for everything a condition refers to (used by content validation).

    Kinds: flag, evidence, claim, cabin, world, npc, noticed, mention, interaction.
    """
    if is_trivially_true(cond):
        return
    if isinstance(cond, str):
        yield ("flag", cond)
        return
    if isinstance(cond, list):
        for c in cond:
            yield from iter_references(c)
        return
    if not isinstance(cond, dict) or len(cond) != 1:
        raise ConditionError(f"A condition must be a string, list or single-key mapping: {cond!r}")
    (key, value), = cond.items()
    if key in ("all_of", "any_of"):
        for c in _as_list(value, key):
            yield from iter_references(c)
    elif key == "not":
        yield from iter_references(value)
    elif key in ("evidence_collected", "evidence_reviewed"):
        yield ("evidence", value)
    elif key == "claim_recorded":
        _require_keys(value, {"speaker", "topic"}, key)
        yield ("claim", (value["speaker"], value["topic"]))
    elif key == "cabin_authorized":
        yield ("cabin", value)
    elif key == "world_equals":
        for k in value:
            yield ("world", k)
    elif key == "npc_present":
        yield ("npc", value)
    elif key == "noticed":
        yield ("noticed", value)
    elif key == "mentioned":
        _require_keys(value, {"npc", "about"}, key)
        yield ("mention", (value["npc"], value["about"]))
    elif key == "completed":
        yield ("interaction", value)
    else:
        raise ConditionError(f"Unknown condition key {key!r}")


def _as_list(value: Any, key: str) -> list:
    if not isinstance(value, list):
        raise ConditionError(f"{key} needs a list, got {value!r}")
    return value


def _require_keys(value: Any, keys: set[str], key: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise ConditionError(f"{key} needs exactly the keys {sorted(keys)}, got {value!r}")
