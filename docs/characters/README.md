# Beneath the Surface — Character Bibles (v0.2)

These six Markdown files define the **subjective perspective** of each living NPC: personality, voice, goals, relationships, knowledge, secrets, alibis, response-to-evidence rules and limits on improvisation.

The shared objective story, including the murder time and method, is owned by `docs/story_bible.md`. The bibles intentionally preserve **TBD** markers for unfixed alibis and clues rather than creating conflicting canon.

| File | Role in mystery |
|---|---|
| [`sarah_morgan.md`](sarah_morgan.md) | Captain: ship authority and questionable safety decisions |
| [`daniel_reyes.md`](daniel_reyes.md) | Engineer: cover-up, fault, sincere mistaken guilt |
| [`maya_chen.md`](maya_chen.md) | Scientist: breakthrough, secret transfer, murderer |
| [`thomas_blake.md`](thomas_blake.md) | Investor: intentional financial misrepresentation |
| [`olivia_hart.md`](olivia_hart.md) | Medic: cautious medical observations and confidentiality |
| [`lucas_weber.md`](lucas_weber.md) | Filmmaker: footage, timestamps, unauthorized recording |

## Usage guidance

**Research knowledge levels:** After Elena's death, only Maya explains the full science and adaptive improvement. Others use their role-specific simplified explanations, preserving engineering, commercial, operational, medical, or filming expertise without inventing chemical expertise. Do not load Story §2.2 wholesale into their prompts. Documents can still convey evidence independently of Maya's cooperation; learning a quoted result does not make another NPC a scientific expert.


**Captain-only navigation/weather details:** Do not include the exact route, position, operating status, or forecast/36-hour outlook in other NPCs' initial prompts. They describe observable conditions and refer detailed questions to Sarah. Any later knowledge transfer must be explicit and source-attributed.


1. **Human authorship:** Review changes to knowledge, alibis or clues against the Story Bible in the same pull request.
2. **NPC prompting:** Build each NPC's prompt from their own bible and relevant state. **Never load other NPCs' private bibles** or the complete Story Bible into their runtime context.
3. **Consistency:** The game engine—not the NPC—owns discovered evidence, room access, relationships and persistent admissions.
4. **Historical injury:** Story §4.4 defines Noah Bennett's incident eight months before the murder. He is not aboard. Sarah, Daniel, Maya, and Thomas know only the basic injury/departure/recovery history; Elena and Olivia know the concealed circumstances; Lucas and the player initially know nothing. NPCs discuss it only when explicitly asked. Do not import Olivia's private details into other NPC prompts.
5. **TBD fields:** Resolve before enabling conversations that require those details; the LLM must not invent them to fill gaps.

## Shared open decision: NPC curiosity and hints (TBD)

Choose one or more NPCs who may naturally ask the player what Elena was doing in the wet lab so late, once the speaker has a legitimate basis for that timing. Until then, they may wonder what brought her there without asserting when. Define speakers, evidence/state triggers, useful authored leads, repetition limits, and responses when the player already knows the answer. This may provide gentle guidance when the player struggles, without inventing testimony, leaking another character's secret, or imposing clue order. Carry the chosen behavior into the relevant Character Bibles and evidence/gameplay rules when resolved (Story §12).

**Development-only:** These files contain spoilers, especially `maya_chen.md`; keep them out of public-facing game assets.
