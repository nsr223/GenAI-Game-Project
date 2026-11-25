# Prompt log: engine skeleton (`feature/engine-core`)

Coding-agent session that built the first engine slice. Agent: Claude Code (Claude Opus 5.5), 2026-11-20.

## 1. Task prompt (by the engine owner)

> You are building the game-engine skeleton for our murder-mystery game "Beneath the Surface". I own the backend/engine.
>
> Before anything else, read: AGENTS.md, docs/summaries/canon.md, docs/summaries/engine.md. Open the full bibles only for the specific sections you need (search by heading); do not read them in full.
>
> **Goal:** A runnable, tested engine skeleton that the frontend person can build against and that the story/NPC people can fill with content later.
>
> **Branch:** Create `feature/engine-core` from the current branch (feature/agent-context). Do not touch main. Do not push.
>
> **Stack:** Python 3.11+, pytest, python-dotenv · Gradio only as a minimal debug UI to prove the engine works end to end (the real UI belongs to the frontend owner) · LLM client behind one interface, e.g. `chat(system_prompt, messages) -> str`, with implementations for OpenRouter (default model configurable via .env) and Gemini, plus a FakeLLM for tests. Keys only via .env; add .env.example.
>
> **Scope (MVP slice, data-driven):**
> 1. Data files in `data/` following the formats suggested in World §10.1 and Evidence §10.1: `locations.yaml` (the 8 MVP rooms + corridors/stairs with the exact IDs and connections from World §2.3); `evidence.yaml` (at least the essential chain EV-00, 09, 10, 11, 13, 14, 16, 17, 18, 19 with access/prerequisites/flags); `npcs.yaml` (the 6 suspects with id, name, default location, path to a persona prompt). Use only canon from the bibles. Where a bible says TBD, insert an explicit placeholder marked `TBD` and keep going. Never invent canon.
> 2. Engine (I'd suggest a `Game` class) with: state (World §5.2 + Evidence §10.3), move with access checks, inspect object, collect/review evidence, talk to NPC, present evidence to NPC, gated unlocks (e.g. the EV-11 rule from Evidence §10.2), persisted NPC claims (Evidence §7.4), accusation check (Evidence §9.1), and journal state.
> 3. Prompt assembly: build each NPC's system prompt from persona + that NPC's known facts + only unlocked facts + presented evidence + fixed rules. Locked facts must never appear in the prompt. Put the rule text in `prompts/system/` as versioned files.
> 4. Minimal Gradio debug app that can walk through: move, inspect, talk, present evidence, accuse.
>
> **Folder layout:** `backend/` and `game/` both exist and are empty; their purpose isn't agreed yet. Propose a layout in your plan and let me decide.
>
> **Verification (mandatory):** pytest suite with FakeLLM (no real API calls), covering at least: room graph is reciprocal and all IDs resolve; locked rooms can't be entered; EV-11 is NOT unlocked by casual talk and IS unlocked when its prerequisites are met even with both motive flags false; locked facts never appear in an assembled prompt; correct accusation without the four flags is not a win; correct accusation with them is. Run the tests yourself and show me the results. Start the debug app once and confirm it loads. If something doesn't work, fix it before claiming it's done.
>
> **How to work with me:** Start in plan mode: give me a short plan (layout, modules, public engine API, data schema) and wait for my OK. Then build in small steps. After each step: what changed, test results, TBDs you hit, and 2–3 proposed next steps. Ask me before decisions that affect other team members (data schema, engine API). Write the final engine API into `docs/engine-api.md` for the frontend owner. Log notable prompts you used or created as described in AGENTS.md.

**Why it worked well:** it pinned the context budget (summaries first, bibles only by heading), named the exact bible sections to follow, listed concrete pass/fail tests up front, and forced a plan-approval stop before any schema/API decision.

## 2. Decisions taken in plan mode (asked, then answered by the owner)

| Question | Choice |
|---|---|
| Use of `game/` vs `backend/` | `game/` = pure deterministic engine; `backend/` = LLM clients, config, debug app |
| Clues with TBD placement/authorization | Provisional (first bible option) + `tbd:` marker + stub requests that always succeed, so the chain is walkable |
| Where NPC knowledge lives | One file per NPC (`data/npc_knowledge/<id>.yaml`) to avoid merge conflicts between six writers |
| How conversations change state | Only via explicit deterministic topic/present actions; free-text chat never changes state |

## 3. Iterations and fixes during the session

| Problem found | Fix |
|---|---|
| The npc-prompts summary's global rule "never change the murderer, time (22:45 / 23:10), weapon…" would **leak the solution to every NPC** if copied into the shared rules prompt. | `prompts/system/npc_rules/v1.md` is written spoiler-free. A test asserts no base prompt contains "22:45", "reference mass", "Nereid", "calibration", "murderer"… |
| Evidence summaries with `[TBD …]` placeholders invite the model to fill gaps. | `strip_tbd()` removes markers before evidence goes into a prompt; TBD facts and claims are never sent. |
| A wrong accusation returning a different outcome than an unsupported correct one would let players brute-force the culprit. | Both return `not_substantiated` with identical text; the distinction is debug-only. |
| The suspect list in `view()` followed data order (Maya first), and the debug app preselected her. | Suspects are sorted by id; the Accuse dropdown starts empty. |
| Gradio sent usage telemetry to Hugging Face on launch (seen in server log). | `GRADIO_ANALYTICS_ENABLED=False` set before importing gradio; confirmed no outbound calls on restart. |
| Test "3 of 4 flags is not a win" first cleared a flag by hand, but derived flags are sticky and re-derived on the next action. | Test now plays the chain while skipping the EV-14 step, which is the honest way to miss a category. |
| YAML parse error: unquoted `tbd_note` containing `: `. | Quoted. (PyYAML already reports file and line, so these are quick to find.) |
| The World Bible uses three IDs for the shared lab door. | One `shared_objects.lab_internal_door`, flagged TBD for the world owner. |

## 4. Result (first session)

91 tests pass (FakeLLM only, no network). Debug app launched and clicked through: move, locked door, inspect, talk with presented evidence, accusation refused without the captain, `not_substantiated` with her.

## 5. Follow-up: first live LLM runs (Gemini)

Owner prompt: *"i added the key, do the rest on your own"* (after asking how to get a Gemini key).

| Problem found live | Fix |
|---|---|
| The key had been pasted into `.env.example` (committed file) instead of `.env`. Not yet committed. | Moved to the git-ignored `.env` without printing it; `.env.example` blanked; repo scanned: key only in `.env`. |
| `gemini-3.8-flash` / `3.7-flash`: HTTP 503 "high demand". | Retry with backoff for 429/5xx in both clients; local `.env` uses `gemini-3.5-flash`. |
| Replies cut off mid-sentence: 383 of 400 output tokens spent on hidden "thinking" (`finishReason: MAX_TOKENS`). | `thinkingConfig.thinkingLevel` = `GEMINI_THINKING_LEVEL` (default `minimal`); warning logged on `MAX_TOKENS`. |
| Free tier: **20 requests/day per model**; retrying a "retry in 14h" 429 is pointless. | Client reads Google's `RetryInfo` / `Retry-After`: fails fast with "retry in 14h20m" if the wait is > 20 s, otherwise waits as asked. |
| `gemini-3.7-flash` rejects `thinkingLevel: minimal` (HTTP 400); `gemini-2.5-flash` is closed to new users. | Documented in `.env.example`. |
| Leak probes: invented alibi, invented "Captain Vance", captain redirecting access to Maya, medic deflecting. | NPC rules v1 → v2 → v3 and template v2 (see `prompts/system/CHANGELOG.md`), each A/B-tested on the same model with `backend/leak_probe.py`; transcripts in `prompts/system/transcripts/`. |

Caveat: personas and knowledge are still stubs, and each probe is a single sample at temperature 0.7. The probes must be rerun once NPC writers add real personas.

## 6. Follow-up: integration with the player UI (`feature/app-integration`, 2026-11-25)

| Owner prompt (summary) | What was done |
|---|---|
| "Bring Erik's visuals with the backend together … a starting point" | Branch from Erik's `feature/game-visuals`; placeholder art cut from the concept sheets into `frontend/static/art/`; people shown as cards with portrait + Talk above the scene. |
| "Can I do something with the objects I can inspect?" → "Yes, add hints" | Optional `locked_hint` on inspect evidence, so a locked clue tells the player whom to ask (EV-09, EV-16, EV-18; wording PROPOSED). |
| "It's strange that you can simply click on each [request] directly … only depending on the conversation. Make a plan first." | Plan approved, then **topic discovery**: `offered_when` per topic, built from three new deterministic conditions: `noticed` (inspected / tried a locked door), `mentioned` (keyword group in the *player's* message) and `completed`. Requests start hidden; whereabouts questions exist for all six suspects so Maya is not singled out. |

**Design decision:** keywords instead of an LLM intent classifier. Evidence §7.4 requires discoveries to be deterministic. An extra classifier call per message would also halve the free Gemini quota (20 requests/day). Tests prove an NPC reply full of keywords offers nothing.
