# Task: verify and finish the journal

## Goal and why
The journal's builder was stopped by a usage limit after writing the code and most checks, without a report. You did not build it: look at it as a fresh reviewer, close the open checks, and fix only what fails. It will be committed on your evidence.

## Context
- Read `AGENTS.md`, the original task `docs/prompt-log/game-visuals/11-journal.md` (its checks are numbered 1–14) and the uncommitted journal code (`git diff`, `frontend/journal.py`, `frontend/static/journal.*`, `tests/test_frontend_journal*.py`). This task is approved inside its scope: no plan approval needed.
- Decision made during that task: the signed browser save stays as it is; every response field outside it follows the allowlist.
- Builder's data: `course/evidence/06-journal/`. Coordinator's test, `jr.py` there, already showed: worked example 1 with request counts, forged review, 238 responses without a leak, draft and late reply kept while the journal is open, clean console. Repeat none of that.
- Playwright: `PYTHONPATH=/tmp/beneath-hotspots.YzVsSwb2/tools`; use your own free ports and fake models only.

## Do
1. From the builder's JSON files, list which of checks 1–14 have evidence and which do not. Trust a check only if the data shows it.
2. Test what is open, in any case: 2 (two tabs opening the same unread entry at once, 10 runs), 11 (session-only, read-only second tab, unusable save), 10 (200% zoom), and 13 (the gate through the UI).
3. Try to break it in three ways of your own that the checks do not cover; say why you chose them.
4. Fix confirmed failures with the smallest change. The browser test file must skip cleanly without Playwright and depend on nothing in `course/`.

## Constraints
Edit only `frontend/` and `tests/test_frontend_*.py`. No new feature, no visual rework, no new dependency. Leave everything uncommitted.

## Pass/fail checks
1. Every one of the 14 checks is marked: shown by builder data, shown by you, failed and fixed, or open with the reason.
2. Each fix has a failing observation before it and a passing one after it.
3. The full suite passes with and without Playwright; the console is clean.
4. No process you started is still running.

## Return
The table, your three attacks with results, fixes with before and after, two opened and described screenshots of states from check 11, and what stays untested. Write it to `course/evidence/06-journal/report.md`, under 900 words.
