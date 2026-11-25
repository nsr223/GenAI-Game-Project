# Task: accusation, ending and restart

## Goal and why
Let the player finish the case: present it to Captain Morgan, live with an unsupported accusation, reach the ending, and start again. This is the dramatic end of the game and must be fair: the interface may never hint at the solution, and only the engine decides.

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md`, Evidence Bible 9 (search the heading), `docs/engine-api.md` (`accuse`, "Accusation", "Guarantees") and `frontend/`. This task is approved inside its scope: no plan approval needed.
- Earlier review: `docs/prompt-log/game-visuals/evidence/12-review-report.md`. Response fields outside the save follow the allowlist in `frontend/journal.py`; extend it the same way.
- Facts checked in the engine: `accuse()` takes only a suspect, uses a turn, and needs Sarah present. The six suspects include Sarah herself. Wrong and unsupported accusations return the same outcome and text. Whether play continues after one is undecided and set in `rules.yaml`; both settings must work without a code change. After the ending every action returns "The investigation is closed." and still counts a turn.

## Build
- **Present your case** appears in Sarah's dialogue, always in the same way, whatever the player has found. It shows what the player has, read-only (evidence with read state, statements, open leads), with links into the journal, and asks for one person. It says that everything collected is presented; it does not let the player pick evidence, because the engine would ignore the choice.
- **Confirm** names the person and can be cancelled without cost.
- **Not substantiated:** the engine's text as Sarah's reaction in the scene; the player can go on.
- **Inconclusive and substantiated:** a calm full-screen ending with the engine's text, the number of turns, entries and statements, and "Read the journal" (read-only) and "New investigation". Nothing else about the solution is revealed.
- **New investigation** is also in a small menu during play, asks once, and replaces the save in all tabs. A closed game reopens on its ending after reload.

## Worked examples
1. Bridge, turn 4, Sarah, accuse Thomas → "Sarah hears you out, then asks for corroboration. She won't record an accusation she can't support.", turn 5, play goes on. Accuse Maya next → exactly the same text and screen, turn 6.
2. A signed fixture save with all four required findings, accuse Maya → ending with "You lay out your reconstruction and the evidence behind it. Sarah records everything and secures it for the investigators who will come aboard once the storm allows." Reload → same ending, no turn added. New investigation → your cabin, turn 0, empty journal except Elena's warning.

## Constraints
Edit only `frontend/` and `tests/test_frontend_*.py`. No new dependency, no images, no visual restyle of other screens. Suspects in the engine's order, with nothing that singles one out. Text is set as text. Page, network and saved plain text never contain the culprit, required flags or the internal result. No real model call.

## Pass/fail checks (real browser, 1280×720 and 1440×900 unless noted)
1. Both worked examples exactly, including turns and request counts.
2. For all six suspects without and with full findings: screens and responses of every failed accusation are identical except the name the player chose, the turn and the save; compare them automatically, including response sizes outside the save and timing (20 runs each, report medians).
3. With `allow_continue_after_failure: false` in a test copy, the inconclusive ending works and reload keeps it.
4. Accusing without Sarah, an unknown suspect, and a forged accusation sent straight to the server are refused; a forged "ending" in a save is refused.
5. Double confirm, held Enter, two tabs confirming at once: one accusation, one turn.
6. After the ending no action changes anything through the page, and the page offers none.
7. Accusing Sarah to her face reads sensibly; report the wording and its limits.
8. The whole case is won through the page from a new game, by clicking only, with a fake model: list every step. Say where a player could not know what to do next.
9. New investigation in one tab updates the other; cancelling changes nothing.
10. Keyboard only, focus and announcements, 200% zoom, session-only mode, read-only tab.
11. Earlier frontend checks still hold; full suite passes with and without Playwright, with new tests for 2, 3, 4 and 5; console clean; no process left running.

## Return
Check table with observed values; the step list of check 8; screenshots (opened and described, including flaws) of the case summary, confirm, reaction, and both endings; scores 1–10 with reasons for: tension, fairness, clarity, fits the dialogue; files changed; engine gaps; untested points. Report under 1,200 words in `course/evidence/07-accusation/report.md`; copy evidence there as you go. Stop after two failed fixes of one check and report it.
