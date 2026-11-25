# Task Summary: Story, Evidence and Bible Maintenance

> For whoever resolves TBDs and maintains `docs/*_bible.md` and `docs/characters/`. Read `canon.md` first.

## Ownership of facts
| Document | Owns |
|---|---|
| `story_bible.md` | What really happened: solution, timeline, scandals |
| `characters/*.md` | Per-person knowledge, beliefs, lies, voice, disclosure |
| `world_bible.md` | Rooms, connections, objects, access, atmosphere |
| `evidence_bible.md` | EV-IDs, clue content, gates, what each clue proves |

**Editing rule:** change the Story Bible first (or in the same PR) when a change touches the murder, the timeline or someone's knowledge. Check the four questions in Evidence §13: Story, Character, World, Progression.

## Essential vs optional evidence (Evidence §5.2)
| Requirement | Route | Essential |
|---|---|---|
| Machinery theory fails | EV-09 + EV-10 → EV-11 | **Yes** |
| Maya's transfer motive | EV-16 + EV-17 | **Yes** |
| Maya present in the critical window | EV-18 + EV-19 | **Yes** |
| Fatal blow / weapon | EV-11 + EV-13 + EV-14 | **Yes** |
| Thomas's financial motive | EV-02 + EV-03 (+ EV-04/05) | No |
| Daniel's reason to fear | EV-08/09 (+ EV-06/07) | No |
| Sarah / Lucas / Olivia side secrets | EV-07, EV-21–24 | No |

**MVP tip:** build the essential chain first; optional threads add depth later.

## TBDs blocking a solvable MVP (recommended order, Evidence §12)
1. **Maya's false alibi** and evidence-team implementation of **Lucas's clip**. The shot of Maya heading toward the labs around 22:30–22:35 is fixed; camera position, coverage, metadata, audio, and review/access remain open. Remember the internal wet/dry lab door (World §8.3).
2. **Physical/medical mechanism**: the trace on the reference mass, and what excludes a cover-induced fall.
3. **Reconstruction access**: what `medical_mechanical_detail_sufficient` and `medical_comparison_authorized` mean in-story.
4. **Placement and permissions**: where Elena's preserved notes are (EV-17) and where the draft agreement is (EV-16). No password guessing.
5. **Numbers and wording**: readable M-17 values and document text.
6. **Ending**: accusation flow; what happens after a wrong or unsupported accusation.

Actual evening movements are fixed in Story §7.1. Elena announces her intended Daniel visit to Olivia/Thomas; they do not witness it. Lucas learns Wednesday’s severe-weather forecast during his roughly 45-minute bridge session with Sarah. Sarah stays on the bridge overnight; the others retire by 23:00. Dinner coverage is settled: nobody on the bridge, propulsion engine on hold, electrical/monitoring systems powered, and Sarah connected directly for notifications of unexpected monitored events (intentional story simplification).

Still open: claimed accounts and independent corroboration; dinner dialogue beyond Elena’s refusal; exact additional bridge briefing details; relief/rest, lookout, and discovery watch coverage; earlier argument/strike audibility; Daniel’s post-discovery record alterations. The 23:10 clunk stays unheard. Olivia’s fictional *Clinical Care Review* magazine is atmosphere, not evidence.

## Hand-off to code
Once decided, put clue records into `data/evidence.yaml` and rooms into `data/locations.yaml` (formats: Evidence §10.1, World §10.1). The engine reads data, not prose.
