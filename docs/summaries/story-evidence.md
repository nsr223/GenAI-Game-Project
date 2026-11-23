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
1. **Maya's false alibi** and **Lucas's clip** (camera position, time, what it shows). Remember the internal wet/dry lab door (World §8.3).
2. **Physical/medical mechanism**: the trace on the reference mass, and what excludes a cover-induced fall.
3. **Reconstruction access**: what `medical_mechanical_detail_sufficient` and `medical_comparison_authorized` mean in-story.
4. **Placement and permissions**: where Elena's preserved notes are (EV-17) and where the draft agreement is (EV-16). No password guessing.
5. **Numbers and wording**: readable M-17 values and document text.
6. **Ending**: accusation flow; what happens after a wrong or unsupported accusation.

Also open: alibis for everyone at 22:35–23:10 (the 23:10 clunk must stay unheard), how Olivia and Thomas learned of the 22:00 Daniel meeting, Daniel's record alterations.

## Hand-off to code
Once decided, put clue records into `data/evidence.yaml` and rooms into `data/locations.yaml` (formats: Evidence §10.1, World §10.1). The engine reads data, not prose.
