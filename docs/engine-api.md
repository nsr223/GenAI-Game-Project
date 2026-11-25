# Engine API (v0.1, skeleton)

For the frontend owner and anyone filling in content. The engine is a plain Python package (`game/`) with no UI and no network access. You import it and call methods. It owns **all** game state. LLMs only voice NPCs, and their replies never change state.

> Status: skeleton. Every essential clue is reachable, but many story decisions are still **TBD** and are marked as provisional in the data (see [Open TBDs](#open-tbds-provisional-in-the-data)).

## Quick start

```bash
py -3.11 -m venv .venv
```
```bash
.venv\Scripts\python -m pip install -r requirements-dev.txt
```
```bash
.venv\Scripts\python -m pytest
```
```bash
.venv\Scripts\python -m backend.debug_app
```
The last command starts the debug UI at http://127.0.0.1:7860. Without a `.env` it runs on the FakeLLM. To use a real model, copy `.env.example` to `.env` and add a key.

```python
from game import Game
from backend.config import make_llm

llm, label = make_llm()               # reads .env; falls back to FakeLLM without a key
game = Game.new(llm=llm)              # loads and validates data/
game.move("crew_quarters")
result = game.talk("thomas_blake", "Where were you last night?")
print(result.ok, result.message, result.reply)
```

## Folder layout

| Path | What | Owner |
|---|---|---|
| `game/` | Engine: content loader, conditions, state, `Game`, prompt assembly, `LLMClient` interface | backend |
| `backend/` | LLM clients (OpenRouter, Gemini, Fake), `.env` config, Gradio **debug** app | backend |
| `data/*.yaml` | Locations, evidence, interactions, rules, NPC list | backend + story/evidence |
| `data/npc_knowledge/<npc>.yaml` | Gated facts per NPC | each NPC writer |
| `prompts/npc/<npc>/vN.md` | Persona prompt (not created yet; a stub is used until it exists) | each NPC writer |
| `prompts/system/` | Global NPC rules and the prompt template (versioned) | backend |
| `tests/` | pytest suite (FakeLLM only, no network) | everyone |

## `Game`: public methods

Every **action** returns an `ActionResult` and increments `turn`. **Queries** have no side effects.

| Method | Kind | What it does |
|---|---|---|
| `Game.new(data_dir=None, llm=None, content=None)` | create | New game from `data/`. `llm` may be `None` (talk then returns no reply). |
| `game.view()` | query | Player-safe snapshot for rendering. Shape below. |
| `game.journal()` | query | Evidence board, recorded statements and leads. Shape below. |
| `game.leads()` | query | Active leads `[{id, text}]` (also inside `view()` and `journal()`). |
| `game.can_enter(location_id)` | query | Would a move there pass the access check (ignores adjacency)? |
| `game.available_topics()` | query | Topic interactions whose NPC is present. |
| `game.move(location_id)` | action | Moves to an adjacent location if its access condition holds. |
| `game.inspect(object_id)` | action | Describes an object in the current room. Collects any evidence on it whose access and prerequisites hold. While they don't, it adds that evidence's `locked_hint` (if any) to the message. |
| `game.review(evidence_id)` | action | Marks collected evidence as reviewed. **Gates use "reviewed"**, so call this when the player opens an entry. |
| `game.interact(interaction_id)` | action | Runs a deterministic topic ("Ask about…", "Ask for access…") with a present NPC. Blocked topics return `ok=False` and an in-world refusal. |
| `game.talk(npc_id, message, present=[...])` | action | Free-text chat with a present NPC, optionally showing collected evidence. Presentation rules run first (deterministically), then the LLM voices the reply. |
| `game.present_evidence(npc_id, evidence_id, message="")` | action | Shortcut for `talk(..., present=[evidence_id])`. |
| `game.accuse(suspect_id)` | action | Presents the case to the captain (she must be present). See [Accusation](#accusation). |
| `game.to_dict()` / `Game.from_dict(d, llm=...)` | save/load | JSON-serialisable save game (state only; content is reloaded from `data/`). |
| `game.debug_state()` | debug | Full internal state **including solution flags**. Never show this to players. |

### `ActionResult`

```python
ActionResult(
    ok: bool,            # False = not allowed / invalid / LLM failed
    message: str,        # player-facing narration or refusal ("The captain has secured the wet lab…")
    reply: str | None,   # NPC reply (talk only)
    outcome: str | None, # accusation only: "substantiated" | "not_substantiated" | "inconclusive"
    events: list[dict],  # player-safe events, see below
)
```
`result.to_dict()` gives a plain dict.

**Events** (player-safe; internal flags are never reported):

| `type` | Fields | When |
|---|---|---|
| `moved` | `id`, `name` | after a successful move |
| `evidence_collected` | `id`, `name` | new journal entry |
| `evidence_reviewed` | `id` | first review of an entry |
| `lead_added` | `id` | a new lead appears (e.g. "Return to Olivia…") |
| `claim_recorded` | `speaker`, `topic` | an NPC statement was stored |
| `interaction_completed` | `id` | a topic or presentation rule fired for the first time |
| `accusation` | `suspect`, `outcome` | after `accuse` |

### `view()` shape

```python
{
  "turn": 7, "game_over": False, "ending": None, "weather": "severe",
  "location": {"id": "main_corridor", "name": "Main corridor", "kind": "corridor", "deck": [2]},
  "exits": [{"id": "wet_lab", "name": "Wet Laboratory", "accessible": False,
             "locked_text": "The captain has secured the wet lab. …"}, ...],
  "objects": [{"id": "mess_table", "name": "Mess table"}, ...],
  "npcs_present": [{"id": "thomas_blake", "name": "Thomas Blake", "role": "Investor representative"}],
  "topics": [{"id": "ask_olivia_initial_observations", "label": "Ask about her initial observations", "npc": "olivia_hart"}],
  "evidence": [{"id": "EV-00", "name": "Elena's warning about M-17", "reviewed": False}],
  "leads": [{"id": "check_m17_records", "text": "Elena asked you to compare …"}],
  "suspects": [{"id": "daniel_reyes", "name": "Daniel Reyes"}, ...],   # sorted by id, never data order
}
```
Locked exits are listed with `accessible: False`, so the map can show them as blocked with an in-world reason (World §5.3, frontend summary).

### `journal()` shape (Evidence §7.3)

```python
{
  "evidence": [{"id", "name", "observed", "interpretation", "questions": [...],
                "related": {"evidence": [collected linked IDs], "characters": [names]},
                "reviewed": bool}],
  "claims":   [{"speaker": "Dr. Maya Chen", "topic": "...", "text": "...", "turn": 12}],
  "leads":    [{"id", "text"}],
}
```
`interpretation` is always `""` for now (a player-notes action is a proposed next step).

### Accusation

`accuse(suspect_id)` needs Sarah in the room. It's a **substantiated** win only if the suspect is the culprit **and** all four flags from Evidence §9.1 are set: `maya_motive_established`, `maya_alibi_contradicted`, `machinery_cause_excluded`, `blunt_force_method_supported`. Then `game_over = True`.

A wrong suspect and a correct but unsupported guess return the **same** `outcome` (`"not_substantiated"`) and the same text, so guessing can't reveal the culprit. The distinction is stored in `debug_state()["accusations_made"]`. Whether the player may continue afterwards is **TBD**: it's `rules.yaml → accusation.allow_continue_after_failure` (currently `true`; `false` ends the game as `"inconclusive"`).

## Guarantees the UI can rely on

- `view()`, `journal()` and `events` never contain internal flags, developer-only evidence fields (`verified_facts`, `not_established`) or the culprit.
- Nothing an LLM says changes state. Tests cover an NPC claiming "the wet lab is open" and claiming "the machine didn't kill her".
- Restricted rooms can't be entered from any side (the wet lab is locked from the corridor **and** through the internal dry-lab door).
- LLM failures come back as `ok=False` with a message. They never raise.

## How NPC prompts are built

`game/prompts.py → build_npc_prompt()` fills the active template (`rules.yaml → prompts`, currently `npc_template/v2.md` with `npc_rules/v3.md`) on **every** talk turn, in this order:

1. **Rules:** `prompts/system/npc_rules/v3.md`. Spoiler-free, because every NPC receives it.
2. **People aboard:** the eight people, names and roles only. Added after a live test where an NPC invented a "Captain Vance".
3. **Persona:** `prompts/npc/<npc>/v1.md`, or a one-line stub if that file doesn't exist yet.
4. **What you know:** only facts from `data/npc_knowledge/<npc>.yaml` whose `unlock` condition is true **now**. Locked facts and `tbd: true` facts are left out of the prompt entirely.
5. **What you already told the auditor:** this NPC's recorded claims (non-TBD).
6. **Scene:** the current room and who else is present.
7. **Evidence shown this turn:** `[ID] name: player-visible summary` only. `[TBD …]` markers are stripped.

The last 12 conversation messages with that NPC go along as chat history (`rules.yaml → prompts.history_turns`).

## Data formats

### Condition language (used everywhere)

```yaml
always                      # or {} / null: true
some_flag                   # flag is true
[a, b]                      # all_of shorthand
all_of: [ ... ]
any_of: [ ... ]
not: <condition>
evidence_collected: EV-09
evidence_reviewed: EV-09
claim_recorded: {speaker: maya_chen, topic: whereabouts_critical_window}
cabin_authorized: cabin_elena
world_equals: {weather: severe}
npc_present: olivia_hart     # NPC is in the player's room
```
The loader rejects unknown flags, evidence IDs, cabins, NPCs, world keys and claim topics that nothing records. Typos fail at startup, not mid-game.

### Files

- **`locations.yaml`** (World §10.1 plus `kind`, `mvp`, `access`, `locked_text`): rooms, reciprocal `connects_to`, objects with spoiler-free descriptions, and `shared_objects` for the one door both labs share.
- **`evidence.yaml`** (Evidence §10.1 plus `acquisition: start|inspect|interaction`, `questions`, `locked_hint`, `tbd`, `tbd_note`): `access` and `prerequisites` are checked whenever an item would be collected, however it's collected.
  - `locked_hint` (optional, `inspect` evidence only): player-facing line shown when the object is inspected but the evidence can't be collected yet. It should say *who could grant access*, never *what the evidence contains*. Current hints (EV-09, EV-16, EV-18) are PROPOSED wording, listed in the TBD report.
- **`interactions.yaml`**: `trigger: topic` (button while the NPC is present) or `trigger: present` (fires when `evidence` is shown to `npc`), plus `requires`, `effects` (`collect_evidence`, `set_flags`, `authorize_cabin`, `record_claim`), `result_text`, `blocked_text`, and `once` (default true).
- **`rules.yaml`**: start location and evidence, initial `world`/`flags`, configurable `tbd_flags`, sticky `derived_flags` (e.g. the EV-11 gate from Evidence §10.2), `leads`, `accusation`, prompt file versions.
- **`npcs.yaml`**: the six suspects with `default_location` (World §8.1, static for now), `persona_prompt` and `knowledge_file`.
- **`npc_knowledge/<npc>.yaml`**: `facts: [{id, text, unlock, tbd}]`.

### Adding NPC content (NPC writers)

1. Write `prompts/npc/<npc>/v1.md` (persona: §1–3 and §8 of the character bible) and log it in `prompts/npc/<npc>/CHANGELOG.md`.
2. Put knowledge in `data/npc_knowledge/<npc>.yaml`. Use `unlock: always` for what they know from the start, and a condition for what they only admit once evidence is presented or collected. Example: `unlock: {evidence_collected: EV-11}`.
3. Delete the `tbd: true` placeholder and run `pytest`. Never write guesses about a bible §9 TBD.

### The essential chain as data

```
EV-00 (start) ─ lead to M-17 records
EV-09 (inspect engineering_maintenance_terminal; needs records access) ─┐
EV-10 (topic: ask Olivia)                                               ├ reviewed + detail + authorization
                                         medical_reconstruction_available ┘ → topic with Olivia → EV-11
                                                                          → machinery_cause_excluded
EV-13 (inspect wet_lab_calibration_station; needs wet-lab inspection) + EV-11 → topic with Olivia → EV-14
                                                                          → blunt_force_method_supported
EV-16 (inspect dry_lab_shared_workstation*) + EV-17 (inspect cabin_desk_elena*) → maya_motive_established
claim (topic: ask Maya where she was) + EV-18 (inspect editing_workstation*) → present EV-18 to Maya → EV-19
                                                                          → maya_alibi_contradicted
* provisional placement
```

## LLM configuration (`.env`)

| Variable | Default | Notes |
|---|---|---|
| `LLM_PROVIDER` | `openrouter` | `openrouter`, `gemini` or `fake` |
| `OPENROUTER_API_KEY` | none | Without it the app falls back to FakeLLM |
| `OPENROUTER_MODEL` | `anthropic/claude-haiku-5.5` | Any OpenRouter model ID |
| `GEMINI_API_KEY` | none | Sent as the `x-goog-api-key` header, never in the URL |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Exists (checked 2026-11-20) but was overloaded (503) that day; `gemini-3.5-flash` worked |
| `GEMINI_THINKING_LEVEL` | `minimal` | Thinking tokens count against `LLM_MAX_TOKENS`; with the model default, replies were cut off. `gemini-3.7-flash` needs `low`. `none` = model default |
| `LLM_TEMPERATURE` / `LLM_MAX_TOKENS` | `0.7` / `400` | |

Both real clients retry twice on 429/5xx and network errors (1.5 s, then 3 s). If the provider asks for a longer wait (e.g. the Gemini free tier's **20 requests/day per model**), they fail at once with "retry in …". `talk()` then returns `ok=False` with that message.

Any object with `chat(system_prompt: str, messages: list[dict]) -> str` works as a client (`game.llm.LLMClient`). Tests use `backend.llm.FakeLLM`, which records every call.

## Open TBDs (provisional in the data)

Run `pytest -s tests/test_content.py::test_tbd_report` for the live list. Currently:

- **Story reasons for every authorization** (wet lab, engineering records, shared records, Elena's cabin, media, medical comparison). Each is a stub request that always succeeds (World §11, Evidence §12).
- **EV-16 placement** (`dry_lab` vs `cabin_maya`), **EV-17 storage** (`cabin_elena` vs archive), **EV-18 clip, object and sharing flow**. The first bible option is used provisionally.
- **Maya's alibi** (EV-19 claim text), **EV-13 trace**, **EV-14 protocol**, the EV-11 contact/reach detail. Placeholder text is marked `[TBD …]` and stripped from prompts.
- **`medical_mechanical_detail_sufficient`**: configurable in `rules.yaml → tbd_flags` (currently `true`).
- **Player start location** (`cabin_player`), **accusation flow** / continue after failure, **engineering-workshop escort rule**, **which cabins are explorable**, **NPC schedules** (NPCs are static).
- **Persona prompts and NPC knowledge** are not written yet (stubs and placeholders).

## Live leak probes (real LLM, not part of pytest)

`backend/leak_probe.py` runs the npc-prompts leak tests against the configured model and writes a transcript to `prompts/system/transcripts/`. NPC writers: run it after every persona or knowledge change and log the result.

```bash
.venv/Scripts/python -m backend.leak_probe --npc maya_chen
```
```bash
.venv/Scripts/python -m backend.leak_probe --model gemini-3.5-flash-lite --rules prompts/system/npc_rules/v2.md --probe tbd_alibi_maya --probe forecast_thomas
```
The second form A/B-tests a prompt version on the same model. Free-tier quotas are small, so pick probes with `--probe`. The automatic check only flags solution terms the player didn't say first. Invented details (alibis, people, records) need a human read: compare each reply with its *Expected* line.

## Not covered yet

- Live leak probes with **real personas**: the runs so far (rules v1 → v3) used stub personas and one sample per probe.
- `data/timeline.yaml` and its fixed-time checks, Thomas's confrontation (EV-02/03), optional evidence, player notes in the journal, time-based NPC movement.
