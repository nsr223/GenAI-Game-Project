# Task: the player's journal

## Goal and why
The player solves the case by comparing what people said with what records show. Build the journal where they read evidence, statements and leads, notice what belongs together, and return to the scene without losing their place. Opening an entry also matters to the rules: the engine's gates depend on evidence being reviewed.

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md`, Evidence Bible 7.3 (search the heading), `docs/engine-api.md` (`journal()`, `review`, `leads`, events) and `frontend/`. This task is approved inside its scope: no plan approval needed.
- Earlier report: `docs/prompt-log/game-visuals/evidence/10-build-report.md`. The final art is not approved: no images.
- Facts checked in the engine: `review()` uses a turn on every call, also for an entry already reviewed and for one you do not have. `interpretation` is always empty for now. A claim carries an internal `topic` id such as `whereabouts_critical_window`, and texts can contain `[TBD …]` markers, as in "[TBD] Maya's account of where she was during the evening."

## Build
- A "Journal" button in the room and in the dialogue, with the number of unread entries, and the key J when no text field has focus. It opens a full-screen notebook with three sections: Evidence, Statements, Leads.
- **Evidence:** list with name and unread mark; an entry shows Observed, Interpretation (only if not empty), Questions, and Related people and evidence. Related evidence is a link to that entry. Opening an unread entry calls `review()` once, through the server.
- **Statements:** grouped by speaker, newest last, with the turn and the words. The internal topic stays hidden.
- **Leads:** the engine's texts as they are.
- `[TBD …]` markers never reach the page: use the same rule as `strip_tbd` in `game/prompts.py`; if nothing is left, show "No details recorded yet." Add nothing in their place.
- Compare: the player can place any two entries, evidence or statement, side by side.
- New entries since the last visit are marked. Closing returns to the same room or conversation, with a typed but unsent question intact.

## Worked examples
1. New game: the journal shows one evidence entry, "Elena's warning about M-17", unread, with one question ("What do the original M-17 readings show?") and one lead. Opening it: turn 0 → 1, the mark goes away. Closing and opening it again: still turn 1 and no request.
2. Medical bay, ask Olivia about her initial observations (turn 3 → 4): the badge counts one more; "Olivia's preliminary observations" shows Olivia Hart as a related person. Opening it: turn 5. Reload: still read.
3. Dry lab, "Ask Maya where she was last night": Statements shows Dr. Maya Chen, the turn, and "Maya's account of where she was during the evening." Neither "TBD" nor "critical window" appears anywhere in the page or the network.

## Constraints
Edit only `frontend/` and `tests/test_frontend_*.py`. No new dependency. Treat every engine string and id as data for display only after checking it is meant for players: names, observed, questions, related names, claim speaker, text and turn, lead text. Everything else stays on the server, also in responses. Text is set as text. No accusation, map or player notes yet. No real model call.

## Pass/fail checks (real browser, 1280×720 and 1440×900 unless noted)
1. The three worked examples exactly, including turns and request counts.
2. Rapid double-opening of an unread entry, and opening the same entry in two tabs at once, call `review()` once per tab at most and never lose the mark or a later action.
3. A forged review for evidence not collected reveals no name or text; the response contains no uncollected evidence, flags, topics, or `supports`, `verified_facts`, `not_established` fields.
4. All collected evidence of the essential chain, reached by signed fixture saves: every entry shows without "TBD", without internal ids as labels, and without broken characters.
5. With 30 evidence entries and 60 statements: opens in under 300 ms, scrolls, and stays usable.
6. Compare works for evidence with evidence, evidence with statement, and statement with statement, and survives opening another entry.
7. Opening from a conversation and closing keeps a half-typed question, the scroll position and a waiting answer; a reply that arrives meanwhile is there afterwards.
8. J types a letter in text fields, opens the journal elsewhere, and does nothing while an action is running.
9. Keyboard only, Escape closes, focus returns; headings and lists are announced properly; unread state is not shown by colour alone.
10. 200% zoom: list, entry and close reachable without horizontal scrolling.
11. Session-only mode, read-only second tab and an unusable save each show a correct, calm state.
12. HTML, 4,000 characters, emoji and right-to-left text in an entry appear as text.
13. The review gate works end to end through the UI with fixture saves: after reviewing the needed entries, the engine's lead to return to Olivia appears.
14. Earlier frontend checks still hold (edges, held Enter, reload, tabs, saves, dialogue examples); full suite passes with new tests for 2, 3 and 4; console clean.

## Return
Check table with observed values; screenshots (opened and described, including flaws) of the list, an entry, compare, statements, and 200% zoom; scores 1–10 with reasons for: feels like an investigator's notebook, easy to find a contradiction, readable, fits the dialogue panel; files changed; engine gaps; untested points; next steps. Evidence in `course/evidence/06-journal/`. Stop after two failed fixes of one check and report it.
