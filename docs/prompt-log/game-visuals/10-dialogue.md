# Task: talk to suspects in the player UI

## Goal and why
Conversation is the heart of the game: the player questions suspects in free text, uses ready topics and shows evidence. Build it on the reviewed foundation so that it feels like facing a person, survives slow or failing models, and leaves every rule to the engine.

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md`, `docs/engine-api.md` (`view()`, `talk`, `interact`, events, guarantees) and `frontend/`. This task is approved inside its scope: no plan approval needed.
- Start and checks of the foundation: `docs/prompt-log/game-visuals/evidence/06-build-report.md`.
- `Game.talk()` may take many seconds. On failure it returns `ok=False` with the provider's error inside `message`, and the turn still counts. There is no streaming.
- The final art is not approved: use a neutral placeholder portrait with a slot for `static/art/characters/<id>.webp`, and leave the existing files in `static/art/` unused.

## Build
- People in the room are clickable and open the dialogue. It covers the lower part of a full-width scene: portrait slot, name and role, the conversation, topics, a text field, and "Show evidence" listing what the player has collected.
- Server: `@app.api` endpoints for talk and topic, so that Gradio's queue limits parallel model calls (`concurrency_limit` from a named constant, default 4), with `make_llm()` created once at startup. Moves and inspections stay on `/action`. The page calls the endpoints with `fetch` and Gradio's event stream; no client library, no CDN.
- Speech, the player's words and engine narration look different from each other. New evidence, claims and leads from `events` appear as short notices.
- Earlier messages with that person return after a reload, read from the saved conversation.
- While waiting: the player's line appears at once, a visible sign that the person is thinking with elapsed seconds after 2 s, "Leave" still works, and a late answer never overwrites newer progress.
- On failure: one in-world line, the player's text back in the field, and Retry. Provider details go only to the server log, without keys.
- Messages are limited to 500 characters, with a counter. Escape closes; focus moves in and returns; new lines are announced once.

## Worked examples
1. Mess hall, turn 3, click Thomas, type "Good morning." → the line appears as yours, then as Thomas: "(FakeLLM) I'd rather not say more right now." Turn 4. Reload → both lines are still there.
2. Medical bay, click Olivia, choose "Ask about her initial observations" → narration "Olivia shares what she can from her initial examination.", notice "New evidence" with the evidence name from the event; "Show evidence" now lists it. No model call is made.

## Constraints
Edit only `frontend/` and `tests/test_frontend_*.py`. No new dependency. Use action results, `view()` and the saved conversation; `debug_state()` and engine flags stay out of the page. Page text is set as text, never HTML. No journal, map or accusation yet. Tests and checks use fake models only: make no real model call. If a public engine method is missing, work around it in `frontend/` and report it.

## Pass/fail checks (real browser, 1280×720 and 1440×900 unless noted)
1. Both worked examples exactly, including turns.
2. Each of the six suspects can be opened in their room; nobody can be opened who is not present.
3. Showing evidence sends only collected evidence; a forged id sent straight to the endpoint is refused and changes nothing but the turn the engine counts.
4. A topic whose condition fails shows the engine's refusal and collects nothing.
5. 15 s reply: your line within 100 ms, elapsed time visible, Leave works, and after leaving and moving, the late answer does not undo the move.
6. Failing model (error text containing a fake key): in-world line, text restored, Retry works; the key appears nowhere in page, network or logs.
7. 8 players talk at once with 3 s replies and limit 4: all answered, none over 8 s, moves by a ninth player stay under 1 s.
8. A reply containing HTML, 4,000 characters, emoji and right-to-left text is shown as text without breaking the layout.
9. An empty reply and whitespace-only messages are handled; 501 characters are refused before sending and by the server.
10. A fake model that says "The wet lab is open now" changes no access.
11. Reload mid-conversation, second tab and session-only mode keep or explain the conversation; 70 exchanges with one person still save.
12. Keyboard only: open, talk, choose a topic, show evidence, close; focus is always visible; a screen-reader live region gets each reply once.
13. At 200% zoom the field, the last reply and Leave are reachable without horizontal scrolling.
14. No engine flags, uncollected evidence, system prompt or other people's knowledge in DOM, network or saved plain text.
15. All earlier frontend checks for edges, held Enter, reload, tabs, saves and forged moves still hold; the full suite passes with new tests for 3, 4, 6, 9 and 10; console clean.

## Return
Check table with observed values; screenshots (opened and described, including flaws) of the empty dialogue, a conversation, evidence list, waiting, failure and 200% zoom; scores 1–10 with a reason for: feels like facing a person, readable, room for a portrait, fits a tense ship mystery; files changed; missing engine methods; untested points; 2–3 next steps. Evidence in `course/evidence/05-dialogue/`. Stop after two failed fixes of one check and report it.
