# AGENTS.md: Instructions for AI coding agents

*Beneath the Surface*: an AI-driven murder mystery game (university GenAI course project, team of 7).
Stack: Python backend, Gradio frontend, LLM API for NPC dialogue.

> `CLAUDE.md` imports this file. Edit **this** file only, so Claude Code, Codex/ChatGPT and other agents share one set of rules.

## 1. Load context sparingly (important)
The design docs in `docs/` are long (~2,300 lines total). **Do not read them in full by default.**

1. Always start with `docs/summaries/canon.md` (short; solution, cast, timeline, rules).
2. Then read the one summary for your task in `docs/summaries/` (see its README).
3. Open a full bible **only when you need detail**, and only the cited section. Find it with a search on the heading (e.g. `## 6.` or `#### \`EV-11\``) instead of reading the whole file.
4. For NPC work, read only the character file you're working on in `docs/characters/`.

## 2. Source of truth
| Question | Authority |
|---|---|
| What really happened (solution, timeline) | `docs/story_bible.md` |
| What a character knows, hides, says | `docs/characters/<name>.md` |
| Rooms, connections, objects, access | `docs/world_bible.md` |
| Clues, gates, what evidence proves | `docs/evidence_bible.md` |

Summaries are derived; **the bibles win** on conflict. If you change a bible, update the affected summary in the same PR.

## 3. Canon rules (never break)
- One fixed solution (see `canon.md`). Never change the murderer, weapon, location or times.
- Exactly 8 people aboard. Never invent people, rooms, documents or decisive evidence.
- **The engine owns game state** (evidence, access, flags). LLM output must never set flags or grant access directly.
- NPC prompts contain only that character's knowledge plus unlocked facts. Never paste whole bibles into a runtime prompt.
- **TBD / PROPOSED** in a bible means *undecided*. Don't silently decide it in code or prompts: make it configurable or stubbed, and flag it in the PR description.
- No spoilers in player-facing text, UI labels or assets (e.g. don't call the reference mass a "weapon").

## 4. Git workflow
- `main`: only milestones and final submission. **Never commit or push to `main`.**
- `develop`: integration branch. Changes arrive only via pull request.
- Work on your own branch: `feature/<area>-<topic>` (e.g. `feature/engine-core`, `feature/npc-maya`).
- Small PRs, each reviewed by another team member. A human merges.
- Never commit secrets: API keys go in `.env` (git-ignored); keep `.env.example` up to date.

## 5. Stay in your lane
Each team member owns certain folders. Change files outside your task only when the issue says so. Changes to shared formats (data schemas, the engine API) need a PR that the affected owners review.

## 6. Tests
- Write or update tests with your change and run them before opening a PR.
- Engine tests must not call a real LLM: use a fake/stub client.
- NPC prompt changes: run the leak tests listed in `docs/summaries/npc-prompts.md`.

## 7. Work loop
- For anything bigger than a small fix: read the relevant summary, propose a short plan, and wait for approval before writing code.
- Work in small steps. After each step, run the tests (and the app, if the step touches it) and fix failures before moving on.
- Never claim something works without having run it. Report honestly what was tested and what wasn't.
- End each step with: what changed, test results, open questions/TBDs hit, and **2–3 proposed next steps**.
- Commit to your feature branch only when the human asks; never push without being asked.

## 8. Log prompts (part of the grade)
Course grading rewards documented prompt iteration. When you create or change a prompt, save it as a new version with a one-line reason:
- NPC prompts → `prompts/npc/<character>/` + `CHANGELOG.md`
- Engine/system prompts → `prompts/system/`
- Image/music/voice prompts → `prompts/assets/`
- Notable coding-agent prompts → `docs/prompt-log/<name>.md`
