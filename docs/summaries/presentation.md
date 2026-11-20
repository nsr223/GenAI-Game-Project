# Task Summary: Prompt Log, Moodle PDF and Presentation

> No spoilers needed for most of this task. `canon.md` has the story if you need it.

## Course requirements
- **15 min** presentation on the last day; not everyone must speak, but **everyone must attend**.
- **One** team member submits a free-format **PDF in Moodle** before the first presentation: team names, code links, task distribution, how to run the code, prompt examples.
- No final integrated system is required. Independent modules may be shown. Slides are optional.

## Peer-evaluation rubric (1–10 each, every student grades us)
1. **Quality and variety of prompts**: clear, structured, diverse
2. **Iterative prompt design**: iterations **documented** and changes **justified**
3. **Quality of final result**: functional, coherent prototype or demo
4. **Creativity and innovation**: originality, and how we handled model limitations
5. **Clarity and structure of the presentation**
6. **Task division and integration**

Criteria 1, 2 and part of 4 are about **prompts and their history**, so collect them continuously.

## Where the prompt material lives
| Kind | Location |
|---|---|
| NPC prompts + changelog | `prompts/npc/<character>/` |
| Engine system prompts (rules, assembly) | `prompts/system/` |
| Image / music / voice prompts | `prompts/assets/` |
| Coding-agent prompts worth showing | `docs/prompt-log/<name>.md` |

## Story hooks for the talk
- "The truth lives in code, not in the LLM": gated knowledge against leaks and hallucination.
- Before/after leak tests (e.g. "v1 leaked in 4 of 10 tests, v3 in 0 of 10").
- Daniel's false confession as an example of an NPC that is sincerely *wrong*, not lying.
- 7 people, 7 coding agents, one repo: how the bibles, summaries and `AGENTS.md` kept agents consistent.
