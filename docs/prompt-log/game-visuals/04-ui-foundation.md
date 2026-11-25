# Task: build the player UI foundation (scene, movement, inspection, resume)

## Goal and why
Build the first real feature of the player UI, on which dialogue, journal, map and accusation will be added. An earlier spike proved the interaction and a review found five problems. This feature must solve them from the start.

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md`, and in `docs/engine-api.md` "Game: public methods", "view() shape" and "Guarantees".
- Review findings: `course/evidence/01-hotspot-spike/review/report.md`. The spike, `frontend/spike_hotspots.py`, is reference only.
- Stack: Gradio 6 `gr.Server` (https://www.gradio.app/guides/server-mode) serving our own HTML, CSS and plain JavaScript modules. A scratch prototype of this confirmed full-size hotspots, resume and no stalling between players.

## Build
- `frontend/server.py`: `gr.Server` with `/`, static files and one JSON action route; run with `python -m frontend.server`. Turn off the interactive API docs.
- Stateless actions: the browser sends its save and one action; the server verifies, acts through `Game`, and returns the new save, `view()`, message and events.
- Saves live in the browser's local storage: compressed `Game.to_dict()` with an HMAC signature, verified before it is unpacked or parsed, with a size limit. `SAVE_SECRET` is read and validated once at startup. If it is missing, generate one for this run and log that saves end with the server; the log never contains its value.
- `frontend/static/`: one 16:9 scene with placeholder art. Hotspots are real buttons covering the full object. Positions come from `frontend/scenes.json` in percentages; rooms without an entry get an automatic layout.
- Visible states: hover and focus, locked exit, busy, error with retry, and unusable save with a "new game" choice. Keep a place for a later room image and for sound that survives room changes.

## Constraints
- Edit only `frontend/`, `tests/test_frontend_*.py`, the gradio line in `requirements.txt` (`gradio>=6,<7`) and one placeholder line for `SAVE_SECRET` in `.env.example`.
- Use `view()` and action results; `debug_state()` stays out. The engine decides every rule.
- Put all game text into the page as text, never as HTML. No new dependency and no CDN.
- Build no dialogue, journal, map or accusation yet. Leave everything uncommitted.

## Pass/fail checks (real browser at 1280×720 and 1440×900 unless noted)
1. New game starts where `Game.new()` starts; walking to the mess hall and back works by clicking.
2. Every hotspot responds at its centre and 4 px inside each edge.
3. Holding Enter or Space for 2 s causes exactly one action.
4. With a 3 s delayed action: busy state visible within 100 ms, controls clearly unavailable, focus kept; a second player's action finishes in under 1 s.
5. Reload and a second tab show the same room and turn; after an action in one tab, the other shows it without reload.
6. A changed, truncated, oversized or foreign-signed save is refused with a clear message and no server error; "new game" recovers.
7. The same save works after a server restart with the same `SAVE_SECRET`.
8. The locked wet lab shows the engine's text and stays closed; a forged move sent straight to the route leaves the room unchanged.
9. Injected HTML in a name shows as text.
10. Every control works with Tab and Enter, with a visible focus ring; room changes are announced.
11. Network and DOM contain no engine flag names outside the opaque save.
12. No console errors or warnings; the whole test suite passes, with tests for saves and the action route using no real LLM.
13. Reading the stored save as text reveals no flag names. State in the report what a technical player could still decode.

## Return
Table of checks with observed values, screenshots (opened and described) of start, mess hall, locked exit, busy and refused save, click-to-update times for 10 clicks, files changed, untested points, and 2–3 next steps. Stop after two failed fixes of the same check and report.
