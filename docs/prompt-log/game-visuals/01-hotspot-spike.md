# Task: prove that scene hotspots work in Gradio 6 (throwaway spike)

## Goal and why
We are building the player UI for *Beneath the Surface*, a point-and-click murder mystery. The riskiest unknown is whether clicking a hotspot in a scene reaches Python and updates that scene reliably in Gradio. Answer that with evidence. If it fails, we change approach before building more, so an honest "no" is as useful as a "yes".

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md`, and in `docs/engine-api.md` only "Game: public methods", "view() shape" and "Guarantees". The bibles are not needed.
- The engine owns all state and rules. The UI sends an action, then renders what `Game.view()` returns. `backend/debug_app.py` shows the session pattern with `to_dict()` / `from_dict()`.
- Gradio 6 documents custom click events: `gr.HTML` with `html_template`, `js_on_load`, `trigger('<event>', {...})`, read in Python through `gr.EventData`. Listeners attach once, so delegate from the parent element. https://www.gradio.app/guides/custom-HTML-components

## Build
One file, `frontend/spike_hotspots.py`, run with `python -m frontend.spike_hotspots` on port 7870.
- Start scene: `Game.new()`, then move `crew_quarters` → `main_corridor` → `mess_hall`. This gives turn 3, four objects, Thomas Blake and one exit.
- Draw the scene as a 16:9 placeholder (plain shapes, no image files). Create one hotspot per object, NPC and exit in `view()`, as real `<button>` elements placed in percentages.
- Object click calls `inspect()`, exit click calls `move()`, NPC click shows name and role only (no LLM call, no turn). Show the engine's message under the scene.

## Constraints
- Edit only `frontend/`. Leave `requirements.txt` and all other files as they are.
- Environment: `uv venv --python 3.12 .venv`, then install `gradio==6.32.0` and the other packages in `requirements-dev.txt`. `.venv` is git-ignored.
- Use `Game.view()` and action results only; `debug_state()` stays out of the UI.
- Treat every string and every id from the browser as untrusted: escape text, let the engine decide whether an action is allowed.
- Leave everything uncommitted and unpushed.

## Pass/fail checks (real browser, 1280×720)
1. The mess hall shows hotspots for exactly its 4 objects, Thomas and 1 exit.
2. Clicking the mess table shows its description and raises the turn from 3 to 4.
3. Clicking Thomas shows name and role; the turn stays the same.
4. Clicking the exit shows the main corridor. A hotspot in the new scene then works too.
5. Clicking the wet lab there shows the engine's locked text; the location stays `main_corridor`.
6. A rapid double-click on one object raises the turn by exactly 1.
7. Two separate browser sessions keep separate turns and locations.
8. A forged click event for `wet_lab`, sent while in the mess hall, leaves the location unchanged.
9. A display name of `<img src=x onerror="window.pwned=1">`, injected in a test only, appears as text and `window.pwned` stays undefined.
10. Every hotspot is reachable with Tab and works with Enter.
11. Hotspots stay on their placeholder shapes at 1440×900.
12. The existing test suite passes.

## Return
- A table with each check: pass, fail or not run, and the observed value.
- Screenshots of checks 1, 4, 5 and 11 in a temporary folder outside the repo, with full paths. Open each one and describe what it actually shows, including anything that looks wrong.
- Click-to-update time for 10 clicks: median and slowest.
- Recommendation: use this method, use it with changes, or use another method, with the reason.
- Anything you could not test. A failed check is a valid result: report it and stop after two fix attempts.
