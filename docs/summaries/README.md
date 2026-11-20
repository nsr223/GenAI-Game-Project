# Task Summaries

Short, task-focused digests of the bibles in `docs/`. They exist so that AI agents (and humans) **don't load ~2,300 lines of bibles into every session**.

| File | For |
|---|---|
| [canon.md](canon.md) | **Everyone**: solution, cast, timeline, global rules |
| [engine.md](engine.md) | Game engine / backend |
| [npc-prompts.md](npc-prompts.md) | NPC persona prompt writers |
| [frontend.md](frontend.md) | UI / Gradio frontend |
| [visuals-audio.md](visuals-audio.md) | Images, music, voices |
| [story-evidence.md](story-evidence.md) | Resolving TBDs, maintaining the bibles |
| [presentation.md](presentation.md) | Prompt log, Moodle PDF, final talk |

## Rules
- Summaries are **derived**. The bibles are the source of truth, and if they disagree, the bible wins.
- When you change a bible, update the affected summaries **in the same PR**.
- Summaries cite sections (e.g. *Evidence §6.2*). Open the bible at that section when you need detail; don't read the whole file.
