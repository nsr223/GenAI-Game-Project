"""The public engine API: :class:`Game`.

Rules of the road (AGENTS.md §3, Evidence §6.2, §7.4):
* The engine owns all state. Evidence, access, flags and claims change only through the
  deterministic code paths below.
* LLM output is returned to the caller as text and is never parsed into state changes.
* Player-facing views never expose internal conclusion flags or developer-only evidence fields.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .conditions import evaluate
from .content import Content, Evidence, Interaction, load_content
from .llm import LLMClient
from .state import Claim, GameState

log = logging.getLogger(__name__)


@dataclass
class ActionResult:
    """Return value of every action.

    ok       False if the action was not allowed / not valid (state unchanged except ``turn``)
    message  player-facing narration or system text
    reply    NPC reply text (talk only)
    outcome  accusation outcome: "substantiated" | "not_substantiated" | "inconclusive"
    events   player-safe events, e.g. {"type": "evidence_collected", "id": "EV-09", "name": ...}
    """

    ok: bool
    message: str
    reply: str | None = None
    outcome: str | None = None
    events: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class Game:
    """One playthrough. Create with :meth:`Game.new`."""

    def __init__(self, content: Content, state: GameState, llm: LLMClient | None = None):
        self.content = content
        self.state = state
        self.llm = llm
        self._refresh_derived([])

    # ================================================================== construction

    @classmethod
    def new(
        cls,
        data_dir: str | Path | None = None,
        llm: LLMClient | None = None,
        content: Content | None = None,
    ) -> "Game":
        content = content or load_content(data_dir)
        return cls(content, GameState.initial(content), llm)

    def to_dict(self) -> dict:
        """JSON-serialisable save game (state only; content is reloaded from data/)."""
        return {"version": 1, "state": self.state.to_dict()}

    @classmethod
    def from_dict(
        cls,
        data: dict,
        data_dir: str | Path | None = None,
        llm: LLMClient | None = None,
        content: Content | None = None,
    ) -> "Game":
        content = content or load_content(data_dir)
        return cls(content, GameState.from_dict(data["state"]), llm)

    # ================================================================== queries (no side effects)

    def can_enter(self, location_id: str) -> bool:
        loc = self.content.locations.get(location_id)
        return loc is not None and evaluate(loc.access, self.state)

    def npcs_here(self) -> list[str]:
        return [npc_id for npc_id in self.content.npcs if self.state.npc_present(npc_id)]

    def available_topics(self) -> list[Interaction]:
        """Topic interactions offered right now (their NPC is present)."""
        return [
            i for i in self.content.interactions.values()
            if i.trigger == "topic" and self.state.npc_present(i.npc)
        ]

    def view(self) -> dict:
        """Player-safe snapshot for the UI. Contains no solution data or internal flags."""
        c, s = self.content, self.state
        loc = c.locations[s.location]
        return {
            "turn": s.turn,
            "game_over": s.game_over,
            "ending": s.ending,
            "weather": s.world.get("weather"),
            "location": {"id": loc.id, "name": loc.display_name, "kind": loc.kind, "deck": list(loc.deck)},
            "exits": [
                {
                    "id": other,
                    "name": c.locations[other].display_name,
                    "accessible": self.can_enter(other),
                    "locked_text": None if self.can_enter(other) else c.locations[other].locked_text,
                }
                for other in loc.connects_to
            ],
            "objects": [{"id": o, "name": c.objects[o].name} for o in loc.object_ids],
            "npcs_present": [
                {"id": n, "name": c.npcs[n].name, "role": c.npcs[n].role} for n in self.npcs_here()
            ],
            "topics": [{"id": i.id, "label": i.label, "npc": i.npc} for i in self.available_topics()],
            "evidence": [
                {"id": e, "name": c.evidence[e].name, "reviewed": s.has_reviewed(e)}
                for e in s.collected_evidence_ids
            ],
            "leads": self.leads(),
            # Sorted by id so list order never hints at the culprit (data order is arbitrary).
            "suspects": [{"id": n, "name": c.npcs[n].name} for n in sorted(c.npcs)],
        }

    def leads(self) -> list[dict]:
        texts = {lead["id"]: lead["text"] for lead in self.content.rules.get("leads") or []}
        return [{"id": lid, "text": texts[lid]} for lid in self.state.active_leads]

    def journal(self) -> dict:
        """Journal / evidence board (Evidence §7.3): evidence entries, recorded claims and leads."""
        c, s = self.content, self.state
        entries = []
        for ev_id in s.collected_evidence_ids:
            ev = c.evidence[ev_id]
            entries.append({
                "id": ev.id,
                "name": ev.name,
                "observed": ev.player_visible_summary,
                "interpretation": "",
                "questions": list(ev.questions),
                "related": {
                    "evidence": [x for x in ev.linked_clues if s.has_collected(x)],
                    "characters": [c.npcs[n].name for n in ev.linked_characters],
                },
                "reviewed": s.has_reviewed(ev.id),
            })
        claims = [
            {"speaker": c.npcs[cl.speaker].name, "topic": cl.topic, "text": cl.text, "turn": cl.turn}
            for cl in s.claims
        ]
        return {"evidence": entries, "claims": claims, "leads": self.leads()}

    def debug_state(self) -> dict:
        """Full internal state including conclusion flags. Debug UI and tests only."""
        return self.state.to_dict()

    # ================================================================== actions

    def move(self, location_id: str) -> ActionResult:
        if (blocked := self._begin()) is not None:
            return blocked
        c, s = self.content, self.state
        here = c.locations[s.location]
        if location_id not in c.locations:
            return ActionResult(False, f"There is no place called '{location_id}'.")
        if location_id not in here.connects_to:
            return ActionResult(False, f"You can't get to {c.locations[location_id].display_name} directly from here.")
        target = c.locations[location_id]
        if not self.can_enter(location_id):
            return ActionResult(False, target.locked_text)
        s.location = location_id
        events = [{"type": "moved", "id": location_id, "name": target.display_name}]
        self._refresh_derived(events)
        return ActionResult(True, f"You go to {target.display_name}.", events=events)

    def inspect(self, object_id: str) -> ActionResult:
        if (blocked := self._begin()) is not None:
            return blocked
        c, s = self.content, self.state
        obj = c.objects.get(object_id)
        if obj is None or s.location not in obj.location_ids:
            # Undefined objects get no invented clue (Evidence §7.4).
            return ActionResult(False, "There's nothing like that to inspect here.")
        events: list[dict] = []
        lines = [obj.description]
        for ev in c.evidence.values():
            if (
                ev.acquisition == "inspect"
                and ev.object_id == object_id
                and ev.location_id == s.location
                and not s.has_collected(ev.id)
                and self._collect(ev, events)
            ):
                lines.append(f"New evidence: {ev.name}.")
        self._refresh_derived(events)
        return ActionResult(True, "\n".join(lines), events=events)

    def review(self, evidence_id: str) -> ActionResult:
        if (blocked := self._begin()) is not None:
            return blocked
        s = self.state
        if not s.has_collected(evidence_id):
            return ActionResult(False, "You don't have that evidence.")
        events: list[dict] = []
        if not s.has_reviewed(evidence_id):
            s.reviewed_evidence_ids.append(evidence_id)
            events.append({"type": "evidence_reviewed", "id": evidence_id})
        self._refresh_derived(events)
        ev = self.content.evidence[evidence_id]
        return ActionResult(True, f"{ev.name}\n{ev.player_visible_summary}", events=events)

    def interact(self, interaction_id: str) -> ActionResult:
        """Run a topic interaction (ask/request) with an NPC who is present."""
        if (blocked := self._begin()) is not None:
            return blocked
        inter = self.content.interactions.get(interaction_id)
        if inter is None or inter.trigger != "topic":
            return ActionResult(False, "That isn't something you can do here.")
        if not self.state.npc_present(inter.npc):
            return ActionResult(False, f"{self.content.npcs[inter.npc].name} isn't here.")
        events: list[dict] = []
        ok = self._run_interaction(inter, events)
        self._refresh_derived(events)
        return ActionResult(ok, inter.result_text if ok else inter.blocked_text, events=events)

    def talk(self, npc_id: str, message: str, present: Iterable[str] = ()) -> ActionResult:
        """Say something to an NPC who is present, optionally presenting collected evidence.

        1. Presentation rules (``trigger: present`` interactions) run deterministically.
        2. The NPC's system prompt is rebuilt from scratch (persona + unlocked facts + presented evidence).
        3. The LLM voices the reply. Its text is returned and stored in the conversation history,
           but never interpreted: it cannot set flags, collect evidence or grant access.
        Without an LLM client the deterministic part still runs and ``reply`` is None.
        """
        if (blocked := self._begin()) is not None:
            return blocked
        c, s = self.content, self.state
        present = list(dict.fromkeys(present))
        if npc_id not in c.npcs:
            return ActionResult(False, "There's nobody by that name aboard.")
        if not s.npc_present(npc_id):
            return ActionResult(False, f"{c.npcs[npc_id].name} isn't here.")
        missing = [e for e in present if not s.has_collected(e)]
        if missing:
            return ActionResult(False, f"You don't have {', '.join(missing)}.")
        message = (message or "").strip()
        if not message and not present:
            return ActionResult(False, "Say something or show some evidence.")

        events: list[dict] = []
        narration: list[str] = []
        for ev_id in present:
            for inter in c.interactions.values():
                if inter.trigger == "present" and inter.npc == npc_id and inter.evidence == ev_id:
                    ok = self._run_interaction(inter, events)
                    narration.append(inter.result_text if ok else inter.blocked_text)
        self._refresh_derived(events)

        shown = "".join(f"[I show you: {c.evidence[e].name}] " for e in present)
        user_turn = {"role": "user", "content": (shown + message).strip()}
        history = s.conversations.setdefault(npc_id, [])
        history.append(user_turn)

        if self.llm is None:
            return ActionResult(True, "\n".join(narration) or "(No LLM configured: no reply.)", events=events)

        from .prompts import build_npc_prompt  # local import keeps engine import light

        system_prompt = build_npc_prompt(c, s, npc_id, present)
        window = int(c.rules.get("prompts", {}).get("history_turns", 12))
        try:
            reply = self.llm.chat(system_prompt, history[-window:])
        except Exception as exc:  # any provider failure must not crash the game
            history.pop()
            log.warning("LLM call failed for %s: %s", npc_id, exc)
            text = "\n".join(narration + [f"{c.npcs[npc_id].name} doesn't answer. (LLM error: {exc})"])
            return ActionResult(False, text, events=events)
        reply = (reply or "").strip()
        history.append({"role": "assistant", "content": reply})
        return ActionResult(True, "\n".join(narration), reply=reply, events=events)

    def present_evidence(self, npc_id: str, evidence_id: str, message: str = "") -> ActionResult:
        """Convenience wrapper: show one piece of evidence, with an optional message."""
        return self.talk(npc_id, message or "What can you tell me about this?", present=[evidence_id])

    def accuse(self, suspect_id: str) -> ActionResult:
        """Present a case against ``suspect_id`` (Evidence §9).

        Wrong and unsupported accusations return the same player-facing outcome, so guessing can't
        reveal the culprit. The precise result is kept in ``accusations_made`` (debug only).
        """
        if (blocked := self._begin()) is not None:
            return blocked
        c, s = self.content, self.state
        acc = c.rules["accusation"]
        if suspect_id not in c.npcs:
            return ActionResult(False, "You can only accuse someone aboard.")
        required_npc = acc.get("requires_npc_present")
        if required_npc and not s.npc_present(required_npc):
            return ActionResult(False, acc.get("requires_npc_text", "You need the captain present."))

        correct = suspect_id == acc["culprit"]
        supported = all(s.flag(f) for f in acc["required_flags"])
        if correct and supported:
            result, outcome, text = "substantiated", "substantiated", acc["substantiated_text"]
            s.game_over, s.ending = True, "substantiated"
        else:
            result = "correct_but_unsupported" if correct else "wrong"
            if acc.get("allow_continue_after_failure", True):
                outcome, text = "not_substantiated", acc["not_substantiated_text"]
            else:
                outcome, text = "inconclusive", acc["inconclusive_text"]
                s.game_over, s.ending = True, "inconclusive"
        s.accusations_made.append({"suspect": suspect_id, "turn": s.turn, "result": result})
        events = [{"type": "accusation", "suspect": suspect_id, "outcome": outcome}]
        return ActionResult(True, text.strip(), outcome=outcome, events=events)

    # ================================================================== internals

    def _begin(self) -> ActionResult | None:
        self.state.turn += 1
        if self.state.game_over:
            return ActionResult(False, "The investigation is closed.")
        return None

    def _evidence_obtainable(self, ev: Evidence) -> bool:
        return evaluate(ev.access, self.state) and evaluate(ev.prerequisites, self.state)

    def _collect(self, ev: Evidence, events: list[dict]) -> bool:
        if self.state.has_collected(ev.id):
            return True
        if not self._evidence_obtainable(ev):
            return False
        self.state.collected_evidence_ids.append(ev.id)
        events.append({"type": "evidence_collected", "id": ev.id, "name": ev.name})
        return True

    def _run_interaction(self, inter: Interaction, events: list[dict]) -> bool:
        """Check and apply one interaction. Returns False if blocked."""
        s = self.state
        if inter.once and inter.id in s.completed_interactions:
            return True  # repeat the outcome text, no new effects
        if not evaluate(inter.requires, s):
            return False
        to_collect = [self.content.evidence[e] for e in inter.effects.get("collect_evidence", [])]
        if not all(s.has_collected(ev.id) or self._evidence_obtainable(ev) for ev in to_collect):
            return False

        for ev in to_collect:
            self._collect(ev, events)
        # Flags are internal: they are set here but never reported in player-facing events.
        for flag in inter.effects.get("set_flags", []):
            s.flags[flag] = True
        cabin = inter.effects.get("authorize_cabin")
        if cabin and cabin not in s.private_cabin_search_authorized:
            s.private_cabin_search_authorized.append(cabin)
        claim = inter.effects.get("record_claim")
        if claim and not s.has_claim(inter.npc, claim["topic"]):
            s.claims.append(Claim(
                speaker=inter.npc,
                topic=claim["topic"],
                text=claim.get("text", ""),
                turn=s.turn,
                tbd=bool(claim.get("tbd", False)),
            ))
            events.append({"type": "claim_recorded", "speaker": inter.npc, "topic": claim["topic"]})
        if inter.id not in s.completed_interactions:
            s.completed_interactions.append(inter.id)
            events.append({"type": "interaction_completed", "id": inter.id})
        return True

    def _refresh_derived(self, events: list[dict]) -> None:
        """Re-evaluate derived flags (sticky) and active leads after every action."""
        s = self.state
        derived = self.content.rules.get("derived_flags") or {}
        changed = True
        while changed:  # derived flags may depend on each other
            changed = False
            for name, cond in derived.items():
                if not s.flag(name) and evaluate(cond, s):
                    s.flags[name] = True
                    changed = True
        active = [
            lead["id"] for lead in self.content.rules.get("leads") or []
            if evaluate(lead.get("when"), s)
        ]
        for lid in active:
            if lid not in s.active_leads:
                events.append({"type": "lead_added", "id": lid})
        s.active_leads = active
