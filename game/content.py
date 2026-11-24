"""Load and validate the static game content in ``data/``.

Content is read-only at runtime. All mutable state lives in :mod:`game.state`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .conditions import ConditionError, iter_references

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = REPO_ROOT / "data"

ACQUISITIONS = {"start", "inspect", "interaction"}
TRIGGERS = {"topic", "present"}
EFFECT_KEYS = {"collect_evidence", "set_flags", "authorize_cabin", "record_claim"}
LOCATION_KINDS = {"room", "corridor", "stairs", "cabin"}


class ContentError(ValueError):
    """Raised when the data files are inconsistent."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Invalid game content:\n  - " + "\n  - ".join(errors))


@dataclass(frozen=True)
class GameObject:
    id: str
    name: str
    description: str
    location_ids: tuple[str, ...]
    tbd: tuple[str, ...] = ()
    tbd_note: str = ""


@dataclass(frozen=True)
class Location:
    id: str
    display_name: str
    deck: tuple[int, ...]
    kind: str
    mvp: bool
    connects_to: tuple[str, ...]
    access: Any
    locked_text: str
    object_ids: tuple[str, ...]
    tbd: tuple[str, ...] = ()
    tbd_note: str = ""


@dataclass(frozen=True)
class Evidence:
    id: str
    slug: str
    status: str
    name: str
    location_id: str | None
    object_id: str | None
    source_type: str
    acquisition: str
    access: Any
    prerequisites: Any
    player_visible_summary: str
    questions: tuple[str, ...]
    verified_facts: tuple[str, ...]
    not_established: tuple[str, ...]
    linked_characters: tuple[str, ...]
    linked_clues: tuple[str, ...]
    tbd: tuple[str, ...] = ()
    tbd_note: str = ""


@dataclass(frozen=True)
class Fact:
    id: str
    text: str
    unlock: Any = "always"
    tbd: bool = False


@dataclass(frozen=True)
class Npc:
    id: str
    name: str
    role: str
    default_location: str
    persona_prompt: str
    knowledge_file: str
    facts: tuple[Fact, ...] = ()


@dataclass(frozen=True)
class Interaction:
    id: str
    trigger: str
    npc: str
    label: str = ""
    evidence: str | None = None
    requires: Any = None
    effects: dict = field(default_factory=dict)
    result_text: str = ""
    blocked_text: str = ""
    once: bool = True
    tbd: tuple[str, ...] = ()
    tbd_note: str = ""


@dataclass(frozen=True)
class Content:
    root: Path
    locations: dict[str, Location]
    objects: dict[str, GameObject]
    evidence: dict[str, Evidence]
    npcs: dict[str, Npc]
    interactions: dict[str, Interaction]
    rules: dict

    def path(self, relative: str) -> Path:
        """Resolve a repo-relative path from the data files."""
        return self.root / relative

    def known_flags(self) -> set[str]:
        flags = set(self.rules.get("initial_state", {}).get("flags", {}))
        flags |= set(self.rules.get("tbd_flags", {}))
        flags |= set(self.rules.get("derived_flags", {}))
        for inter in self.interactions.values():
            flags |= set(inter.effects.get("set_flags", []))
        return flags

    def tbd_report(self) -> list[str]:
        """Every provisional field, for the PR description and the test log."""
        lines: list[str] = []
        for obj in self.objects.values():
            if obj.tbd:
                lines.append(f"object {obj.id}: {', '.join(obj.tbd)} - {obj.tbd_note.strip()}")
        for loc in self.locations.values():
            if loc.tbd:
                lines.append(f"location {loc.id}: {', '.join(loc.tbd)} - {loc.tbd_note.strip()}")
        for ev in self.evidence.values():
            if ev.tbd:
                lines.append(f"evidence {ev.id}: {', '.join(ev.tbd)} - {ev.tbd_note.strip()}")
        for inter in self.interactions.values():
            if inter.tbd:
                lines.append(f"interaction {inter.id}: {', '.join(inter.tbd)} - {inter.tbd_note.strip()}")
        for name, spec in self.rules.get("tbd_flags", {}).items():
            lines.append(f"flag {name} = {spec.get('value')!r} - {spec.get('note', '').strip()}")
        for section in ("start", "accusation"):
            tbd = self.rules.get(section, {}).get("tbd", [])
            if tbd:
                lines.append(f"rules.{section}: {', '.join(tbd)}")
        for npc in self.npcs.values():
            if not self.path(npc.persona_prompt).exists():
                lines.append(f"npc {npc.id}: persona prompt {npc.persona_prompt} not written yet (stub used)")
            if all(f.tbd for f in npc.facts):
                lines.append(f"npc {npc.id}: knowledge file has only TBD placeholders")
        return lines


# --------------------------------------------------------------------------- loading


def _read_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _tuple(value: Any) -> tuple:
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return (value,)


def load_content(data_dir: str | Path | None = None, root: str | Path | None = None) -> Content:
    """Load every data file and validate cross-references. Raises :class:`ContentError`."""
    data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    root = Path(root) if root else data_dir.resolve().parent

    loc_raw = _read_yaml(data_dir / "locations.yaml")
    locations: dict[str, Location] = {}
    objects: dict[str, GameObject] = {}
    errors: list[str] = []

    for loc_id, spec in (loc_raw.get("locations") or {}).items():
        obj_specs = spec.get("objects") or {}
        for obj_id, ospec in obj_specs.items():
            if obj_id in objects:
                errors.append(f"object {obj_id} defined in more than one location (use shared_objects)")
            objects[obj_id] = GameObject(
                id=obj_id,
                name=ospec.get("name", obj_id),
                description=(ospec.get("description") or "").strip(),
                location_ids=(loc_id,),
                tbd=_tuple(ospec.get("tbd")),
                tbd_note=ospec.get("tbd_note", ""),
            )
        locations[loc_id] = Location(
            id=loc_id,
            display_name=spec.get("display_name", loc_id),
            deck=_tuple(spec.get("deck")),
            kind=spec.get("kind", "room"),
            mvp=bool(spec.get("mvp", False)),
            connects_to=_tuple(spec.get("connects_to")),
            access=spec.get("access"),
            locked_text=(spec.get("locked_text") or "You can't go there right now.").strip(),
            object_ids=tuple(obj_specs),
            tbd=_tuple(spec.get("tbd")),
            tbd_note=spec.get("tbd_note", ""),
        )

    for obj_id, ospec in (loc_raw.get("shared_objects") or {}).items():
        if obj_id in objects:
            errors.append(f"shared object {obj_id} also defined in a location")
        loc_ids = _tuple(ospec.get("locations"))
        objects[obj_id] = GameObject(
            id=obj_id,
            name=ospec.get("name", obj_id),
            description=(ospec.get("description") or "").strip(),
            location_ids=loc_ids,
            tbd=_tuple(ospec.get("tbd")),
            tbd_note=ospec.get("tbd_note", ""),
        )
        for loc_id in loc_ids:
            if loc_id in locations:
                loc = locations[loc_id]
                locations[loc_id] = Location(**{**loc.__dict__, "object_ids": loc.object_ids + (obj_id,)})

    evidence: dict[str, Evidence] = {}
    for spec in _read_yaml(data_dir / "evidence.yaml").get("evidence") or []:
        ev_id = spec.get("id")
        if ev_id in evidence:
            errors.append(f"duplicate evidence id {ev_id}")
        evidence[ev_id] = Evidence(
            id=ev_id,
            slug=spec.get("slug", ""),
            status=spec.get("status", ""),
            name=spec.get("name", ev_id),
            location_id=spec.get("location_id"),
            object_id=spec.get("object_id"),
            source_type=spec.get("source_type", ""),
            acquisition=spec.get("acquisition", ""),
            access=spec.get("access"),
            prerequisites=spec.get("prerequisites"),
            player_visible_summary=(spec.get("player_visible_summary") or "").strip(),
            questions=_tuple(spec.get("questions")),
            verified_facts=_tuple(spec.get("verified_facts")),
            not_established=_tuple(spec.get("not_established")),
            linked_characters=_tuple(spec.get("linked_characters")),
            linked_clues=_tuple(spec.get("linked_clues")),
            tbd=_tuple(spec.get("tbd")),
            tbd_note=spec.get("tbd_note", ""),
        )

    npcs: dict[str, Npc] = {}
    for npc_id, spec in (_read_yaml(data_dir / "npcs.yaml").get("npcs") or {}).items():
        knowledge_file = spec.get("knowledge_file", "")
        facts: tuple[Fact, ...] = ()
        kpath = root / knowledge_file if knowledge_file else None
        if kpath and kpath.exists():
            kraw = _read_yaml(kpath)
            if kraw.get("npc_id") not in (None, npc_id):
                errors.append(f"{knowledge_file}: npc_id {kraw.get('npc_id')!r} does not match {npc_id}")
            facts = tuple(
                Fact(
                    id=f.get("id"),
                    text=(f.get("text") or "").strip(),
                    unlock=f.get("unlock", "always"),
                    tbd=bool(f.get("tbd", False)),
                )
                for f in (kraw.get("facts") or [])
            )
        elif knowledge_file:
            errors.append(f"npc {npc_id}: knowledge file {knowledge_file} not found")
        npcs[npc_id] = Npc(
            id=npc_id,
            name=spec.get("name", npc_id),
            role=spec.get("role", ""),
            default_location=spec.get("default_location", ""),
            persona_prompt=spec.get("persona_prompt", ""),
            knowledge_file=knowledge_file,
            facts=facts,
        )

    interactions: dict[str, Interaction] = {}
    for spec in _read_yaml(data_dir / "interactions.yaml").get("interactions") or []:
        inter_id = spec.get("id")
        if inter_id in interactions:
            errors.append(f"duplicate interaction id {inter_id}")
        interactions[inter_id] = Interaction(
            id=inter_id,
            trigger=spec.get("trigger", ""),
            npc=spec.get("npc", ""),
            label=spec.get("label", ""),
            evidence=spec.get("evidence"),
            requires=spec.get("requires"),
            effects=dict(spec.get("effects") or {}),
            result_text=(spec.get("result_text") or "").strip(),
            blocked_text=(spec.get("blocked_text") or "").strip(),
            once=bool(spec.get("once", True)),
            tbd=_tuple(spec.get("tbd")),
            tbd_note=spec.get("tbd_note", ""),
        )

    rules = _read_yaml(data_dir / "rules.yaml")

    content = Content(
        root=root,
        locations=locations,
        objects=objects,
        evidence=evidence,
        npcs=npcs,
        interactions=interactions,
        rules=rules,
    )
    errors.extend(validate(content))
    if errors:
        raise ContentError(errors)
    return content


# --------------------------------------------------------------------------- validation


def validate(content: Content) -> list[str]:
    """Return a list of cross-reference problems (empty if the content is consistent)."""
    errors: list[str] = []
    locs, objs, evs, npcs = content.locations, content.objects, content.evidence, content.npcs
    world_keys = set(content.rules.get("initial_state", {}).get("world", {}))
    flags = content.known_flags()
    cabins = {lid for lid, loc in locs.items() if loc.kind == "cabin"}
    claim_topics = {
        (i.npc, i.effects["record_claim"].get("topic"))
        for i in content.interactions.values()
        if "record_claim" in i.effects
    }

    def check_condition(where: str, cond: Any) -> None:
        try:
            refs = list(iter_references(cond))
        except ConditionError as exc:
            errors.append(f"{where}: {exc}")
            return
        for kind, value in refs:
            if kind == "flag" and value not in flags:
                errors.append(f"{where}: unknown flag {value!r} (never initialised or set)")
            elif kind == "evidence" and value not in evs:
                errors.append(f"{where}: unknown evidence {value!r}")
            elif kind == "claim" and value not in claim_topics:
                errors.append(f"{where}: no interaction records claim {value!r}")
            elif kind == "cabin" and value not in cabins:
                errors.append(f"{where}: unknown cabin {value!r}")
            elif kind == "world" and value not in world_keys:
                errors.append(f"{where}: unknown world key {value!r}")
            elif kind == "npc" and value not in npcs:
                errors.append(f"{where}: unknown npc {value!r}")

    # Locations and the room graph
    for loc in locs.values():
        if loc.kind not in LOCATION_KINDS:
            errors.append(f"location {loc.id}: unknown kind {loc.kind!r}")
        for other in loc.connects_to:
            if other not in locs:
                errors.append(f"location {loc.id}: connects to unknown location {other!r}")
            elif loc.id not in locs[other].connects_to:
                errors.append(f"connection {loc.id} -> {other} is not reciprocal")
            if other == loc.id:
                errors.append(f"location {loc.id} connects to itself")
        check_condition(f"location {loc.id} access", loc.access)
        for obj_id in loc.object_ids:
            if obj_id not in objs:
                errors.append(f"location {loc.id}: unknown object {obj_id!r}")
    for obj in objs.values():
        for loc_id in obj.location_ids:
            if loc_id not in locs:
                errors.append(f"object {obj.id}: unknown location {loc_id!r}")

    # Evidence
    for ev in evs.values():
        if ev.acquisition not in ACQUISITIONS:
            errors.append(f"evidence {ev.id}: acquisition must be one of {sorted(ACQUISITIONS)}")
        if ev.location_id is not None:
            if ev.location_id not in locs:
                errors.append(f"evidence {ev.id}: unknown location {ev.location_id!r}")
            elif not locs[ev.location_id].mvp:
                errors.append(f"evidence {ev.id}: placed in non-MVP location {ev.location_id} (World §9)")
        if ev.object_id is not None:
            if ev.object_id not in objs:
                errors.append(f"evidence {ev.id}: unknown object {ev.object_id!r}")
            elif ev.location_id not in objs[ev.object_id].location_ids:
                errors.append(f"evidence {ev.id}: object {ev.object_id} is not in {ev.location_id}")
        if ev.acquisition == "inspect" and not ev.object_id:
            errors.append(f"evidence {ev.id}: acquisition 'inspect' needs an object_id")
        if not ev.player_visible_summary:
            errors.append(f"evidence {ev.id}: missing player_visible_summary")
        for clue in ev.linked_clues:
            if clue not in evs:
                errors.append(f"evidence {ev.id}: linked clue {clue!r} not defined")
        for npc_id in ev.linked_characters:
            if npc_id not in npcs:
                errors.append(f"evidence {ev.id}: linked character {npc_id!r} not an NPC")
        check_condition(f"evidence {ev.id} access", ev.access)
        check_condition(f"evidence {ev.id} prerequisites", ev.prerequisites)

    # NPCs
    for npc in npcs.values():
        if npc.default_location not in locs:
            errors.append(f"npc {npc.id}: unknown default_location {npc.default_location!r}")
        for fact in npc.facts:
            if not fact.id:
                errors.append(f"npc {npc.id}: fact without id")
            check_condition(f"npc {npc.id} fact {fact.id}", fact.unlock)

    # Interactions
    for inter in content.interactions.values():
        where = f"interaction {inter.id}"
        if inter.trigger not in TRIGGERS:
            errors.append(f"{where}: trigger must be one of {sorted(TRIGGERS)}")
        if inter.npc not in npcs:
            errors.append(f"{where}: unknown npc {inter.npc!r}")
        if inter.trigger == "present" and inter.evidence not in evs:
            errors.append(f"{where}: present trigger needs a defined evidence id")
        if inter.trigger == "topic" and not inter.label:
            errors.append(f"{where}: topic trigger needs a label")
        unknown = set(inter.effects) - EFFECT_KEYS
        if unknown:
            errors.append(f"{where}: unknown effects {sorted(unknown)}")
        for ev_id in inter.effects.get("collect_evidence", []):
            if ev_id not in evs:
                errors.append(f"{where}: collects unknown evidence {ev_id!r}")
        cabin = inter.effects.get("authorize_cabin")
        if cabin is not None and cabin not in cabins:
            errors.append(f"{where}: authorize_cabin {cabin!r} is not a cabin")
        claim = inter.effects.get("record_claim")
        if claim is not None and not claim.get("topic"):
            errors.append(f"{where}: record_claim needs a topic")
        check_condition(f"{where} requires", inter.requires)

    # Interaction-only evidence must be reachable by some interaction
    granted = {e for i in content.interactions.values() for e in i.effects.get("collect_evidence", [])}
    for ev in evs.values():
        if ev.acquisition == "interaction" and ev.id not in granted:
            errors.append(f"evidence {ev.id}: acquisition 'interaction' but no interaction grants it")

    # Rules
    rules = content.rules
    start = rules.get("start", {})
    if start.get("location") not in locs:
        errors.append(f"rules.start.location {start.get('location')!r} unknown")
    for ev_id in start.get("evidence", []):
        if ev_id not in evs:
            errors.append(f"rules.start.evidence: unknown {ev_id!r}")
    for name, cond in (rules.get("derived_flags") or {}).items():
        check_condition(f"derived flag {name}", cond)
    for lead in rules.get("leads") or []:
        check_condition(f"lead {lead.get('id')}", lead.get("when"))
    acc = rules.get("accusation", {})
    if acc.get("culprit") not in npcs:
        errors.append("rules.accusation.culprit must be an NPC")
    for flag in acc.get("required_flags", []):
        if flag not in flags:
            errors.append(f"rules.accusation.required_flags: unknown flag {flag!r}")
    if acc.get("requires_npc_present") and acc["requires_npc_present"] not in npcs:
        errors.append("rules.accusation.requires_npc_present must be an NPC")
    for cabin in rules.get("initial_state", {}).get("private_cabin_search_authorized", []):
        if cabin not in cabins:
            errors.append(f"initial private_cabin_search_authorized: unknown cabin {cabin!r}")

    return errors
