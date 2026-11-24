"""Assemble an NPC's system prompt from gated knowledge.

The prompt contains, in this order (template: prompts/system/npc_template/vN.md):
  rules     fixed global rules (prompts/system/npc_rules/vN.md), spoiler-free
  cast      the eight people aboard (names and roles only; canon, not a spoiler) so the model
            never invents crew. Template v1 has no $cast slot and ignores it.
  persona   the NPC writer's persona file, or a one-line stub if it doesn't exist yet
  facts     only facts whose ``unlock`` condition is true right now; locked and TBD facts are
            left out entirely (a fact that isn't in the prompt can't leak)
  claims    this NPC's own recorded claims (non-TBD), so they stay consistent
  scene     current room and who else is present
  evidence  evidence presented this turn: ID, name and player-visible summary only. Developer
            fields (verified_facts, not_established, ...) and [TBD ...] markers are never included.
"""

from __future__ import annotations

import logging
import re
from string import Template
from typing import Iterable

from .conditions import evaluate
from .content import Content
from .state import GameState

log = logging.getLogger(__name__)

_TBD_MARKER = re.compile(r"\s*\[TBD[^\]]*\]")
NONE = "Nothing."


def strip_tbd(text: str) -> str:
    """Remove ``[TBD ...]`` placeholders so the LLM isn't invited to fill undecided gaps."""
    return _TBD_MARKER.sub("", text).strip()


def _read(content: Content, rel_path: str) -> str:
    return content.path(rel_path).read_text(encoding="utf-8").strip()


def persona_text(content: Content, npc_id: str) -> str:
    npc = content.npcs[npc_id]
    path = content.path(npc.persona_prompt) if npc.persona_prompt else None
    if path and path.exists():
        return path.read_text(encoding="utf-8").strip()
    log.warning("Persona prompt %s for %s not found; using stub", npc.persona_prompt, npc_id)
    return f"You are {npc.name}, {npc.role.lower()} aboard the RV Meridian."


def cast_list(content: Content, npc_id: str) -> str:
    """All eight people aboard (Story §8): the six NPCs, the victim and the player."""
    lines = []
    for other in sorted(content.npcs.values(), key=lambda n: n.name):
        you = " (you)" if other.id == npc_id else ""
        lines.append(f"- {other.name}, {other.role.lower()}{you}")
    lines.append("- Dr. Elena Fischer, lead scientist (found dead this morning)")
    lines.append("- The auditor (the person you are talking to)")
    return "\n".join(lines)


def unlocked_facts(content: Content, state: GameState, npc_id: str) -> list[str]:
    return [
        f.text for f in content.npcs[npc_id].facts
        if not f.tbd and f.text and evaluate(f.unlock, state)
    ]


def build_npc_prompt(
    content: Content,
    state: GameState,
    npc_id: str,
    presented_ids: Iterable[str] = (),
) -> str:
    cfg = content.rules.get("prompts", {})
    npc = content.npcs[npc_id]

    facts = unlocked_facts(content, state, npc_id)
    claims = [c.text for c in state.claims if c.speaker == npc_id and not c.tbd and c.text]

    loc = content.locations[state.location]
    others = [content.npcs[n].name for n in content.npcs if n != npc_id and state.npc_present(n)]
    scene = f"You are in the {loc.display_name}. The auditor is here with you."
    if others:
        scene += " Also present: " + ", ".join(others) + "."

    evidence_lines = []
    for ev_id in presented_ids:
        ev = content.evidence[ev_id]
        summary = strip_tbd(ev.player_visible_summary)
        evidence_lines.append(f"- [{ev.id}] {ev.name}: {summary}")
    if evidence_lines:
        evidence_lines.append("React in character. You cannot change what this evidence shows.")

    template = Template(_read(content, cfg.get("npc_template", "prompts/system/npc_template/v1.md")))
    return template.safe_substitute(
        rules=_read(content, cfg.get("npc_rules", "prompts/system/npc_rules/v1.md")),
        name=npc.name,
        cast=cast_list(content, npc_id),
        persona=persona_text(content, npc_id),
        facts="\n".join(f"- {t}" for t in facts) or NONE,
        claims="\n".join(f"- {t}" for t in claims) or NONE,
        scene=scene,
        evidence="\n".join(evidence_lines) or "None.",
    ).strip() + "\n"
