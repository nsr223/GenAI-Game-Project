# Task: fix the reviewed defects of the player UI foundation

## Goal and why
An independent review accepted `frontend/` with named fixes. Make it safe to build dialogue and art on. Keep the current look: a restyle follows separately.

## Context
Read `AGENTS.md`, `frontend/` (ignore `spike_hotspots.py`) and `course/evidence/03-ui-foundation/review/report.md`. This task is approved: no plan approval needed unless you must leave its scope.

## Fix
1. **Start through Gradio:** `python -m frontend.server` uses `app.launch()` with a working startup, and analytics off before Gradio is imported. Read and validate `SAVE_SECRET` once at startup.
2. **Save growth:** save only the most recent 60 messages of each conversation; collected evidence, claims and flags stay complete. A save-limit error offers "Return to investigation" instead of Retry and restores usable controls.
3. **Storage:** blocked and full storage get different, accurate messages. Offer to play this session without saving, with a permanent visible note.
4. **Temporary key:** when `SAVE_SECRET` is missing, the player sees once that progress lasts only until the server stops.
5. **No Web Locks:** a second tab is told the game is open elsewhere and stays read-only until the player takes over; an acknowledged action is never lost.
6. **Long actions:** after 2 s show elapsed seconds near the clicked object; respect reduced motion.
7. **Zoom:** at 200% the result and busy text are visible without scrolling from the hotspot used.
8. **Art:** when a room image exists, hotspots become transparent with a compact label or marker; hit areas and focus rings stay full size.

## Constraints
Edit only `frontend/` and `tests/test_frontend_*.py`. `frontend/static/art/` is read-only and its images may still change; use them as they are only for trying check 9 a second time. No new dependency. The engine stays untouched. No dialogue yet. Leave everything uncommitted.

## Pass/fail checks (real browser unless noted)
1. Start by the documented command: page, new game and a move work; no analytics request leaves the process.
2. Fake-LLM test copy, 400 exchanges of 60 words with one NPC and 400 spread over six: every save accepted, gates and claims identical to an untrimmed run.
3. Forced save-limit error: the player returns to a working room without reload.
4. Blocked and full storage: correct message each; session-only play completes three moves.
5. Missing secret: notice shown once; valid secret: none; a weak secret stops startup without showing its value.
6. Plain HTTP on a non-loopback hostname, two tabs, 3 s delay: no acknowledged action lost in 10 runs; takeover works.
7. 15 s action: the visible text changes at least every 2 s.
8. 200% zoom at 1280×720: result visible after inspecting each mess-hall object.
9. With a solid-colour test image: at least 90% of every hotspot shows it; edge clicks and focus still work.
10. The earlier checks still hold: hotspot edges, held Enter, reload, second tab with locks, forged move, refused saves.
11. Full test suite passes with new tests for 2, 3 and 5; console clean.

## Return
Check table with observed values, screenshots of 3, 4, 6, 8 and 9 opened and described, files changed, untested points. Stop after two failed fixes of the same check and report it. Copy all evidence to `course/evidence/04-ui-fixes/`.
