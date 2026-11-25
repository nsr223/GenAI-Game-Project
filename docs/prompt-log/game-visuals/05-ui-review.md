# Task: independently review the player UI foundation

## Goal and why
Another agent built `frontend/` and reported 13 of 13 checks passed. Dialogue, journal, map and art will be built on it, so find what would hurt later. A confirmed defect is the most useful result; report "holds" only for what you observed.

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md`, the code in `frontend/` (ignore `spike_hotspots.py`) and the author's report at `course/evidence/03-ui-foundation/build/report.md`. This task is already approved: no plan approval needed.
- Use `.venv/bin/python`; Playwright with `PYTHONPATH=/tmp/beneath-hotspots.YzVsSwb2/tools`. Use your own free ports; leave 7870 alone. Another worker is writing to `prompts/assets/` and `course/`.
- The repository is read-only for you. Scripts, screenshots and the report go to a new temporary folder. Write your own tests.

## Part A: behaviour
1. Repeat with your own test: hotspot edges, held Enter, reload, second tab, refused saves, forged move.
2. Dialogue ahead: with a fake LLM in a test copy, simulate 50, 150 and 400 `talk()` turns with 60-word messages and replies. Report save size against the limits, and exactly what a player experiences when the limit is reached. Is progress lost?
3. A 15 s action: can the player tell the game is alive? Close the tab mid-action, then open a new one: is the save valid and the lock free?
4. Two tabs acting alternately 20 times as fast as possible: any lost, doubled or reverted turn?
5. Browser storage blocked or full: what does the player see, and is there a way out?
6. Server stopped mid-game, then restarted with and without the same `SAVE_SECRET`.
7. 20 players acting at once: errors and slowest response.
8. The server runs through `uvicorn.run(app)` rather than `app.launch()`. What does that change (Gradio API, queue, hosting on Hugging Face Spaces, telemetry), and is Gradio still used in any meaningful way? Try `launch()` in a test copy and report.
9. Startup with a weak, missing and valid `SAVE_SECRET`: do messages or logs ever show the value?

## Part B: judge it as a game screen
Look at fresh screenshots at 1280×720, 1440×900, 1920×1080, 1024×768 and 200% zoom. Placeholder shapes are expected; judge the frame around them. Score 1–10 with one concrete reason each: mood fits a confined ship in a gale; scene dominates the screen; feels like a game rather than a document or form; text readable; nothing generic; space for a character portrait, dialogue, evidence and journal. Anything below 7 gets a specific change.

## Return
Tables for A and B, defects ordered by effect on the player with the smallest reproduction, screenshots (path, opened, described), a recommendation (accept, accept with named fixes, rework) and what you could not test.
