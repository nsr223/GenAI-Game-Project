# Task Summary: Game Engine (Backend)

> Read `canon.md` first. This file condenses what the engine owner needs from the bibles. Bibles win on conflict.
> Deep dives: World §2.3 (room graph), World §5 (access/state), World §10 (data and LLM input), Evidence §4 (catalog), Evidence §5–7 (dependencies, gates, dialogue), Evidence §9–10 (accusation, data examples).

## Core principle
**The engine governs state; the LLM only voices characters.** (Story §13, Evidence §7.4)
- Evidence collection, room access, flags, admissions and the accusation check are **deterministic code**.
- The LLM never sets flags, unlocks evidence or grants access. A conversation can only set a flag through an explicit, rule-checked event (Evidence §6.2).
- Each NPC prompt contains **only** that character's knowledge plus what they have legitimately learned in play. Never paste whole bibles into a prompt (World §10.2).

## Planned data files (from the bibles)
| File | Content | Source |
|---|---|---|
| `data/locations.yaml` | Room IDs, connections, objects, base access rules | World §2.3, §3, §10.1 |
| `data/evidence.yaml` | EV records: location/object, access, prerequisites, player-visible text, facts set | Evidence §4, §10.1 |
| `data/timeline.yaml` | Fixed events | Story §7 |
| NPC prompt data | Per-character persona and knowledge | `docs/characters/*.md` (see `npc-prompts.md`) |

Markdown is for humans. Don't parse bible prose at runtime (Evidence §10).

## Room graph (World §2.3, bidirectional)
```
bridge — upper_stairs — main_corridor
main_corridor — wet_lab, dry_lab, mess_hall, medical_bay, crew_quarters, editing_room, lower_stairs
wet_lab — dry_lab            (shared internal door: one object `lab_internal_door`)
lower_stairs — lower_corridor — engineering_workshop, engine_room, equipment_storage
equipment_storage — aft_work_deck
crew_quarters — cabin_player, cabin_elena, cabin_sarah, cabin_daniel, cabin_maya, cabin_thomas, cabin_olivia, cabin_lucas
```
MVP core rooms (World §9): `bridge, wet_lab, dry_lab, mess_hall, medical_bay, crew_quarters, editing_room, engineering_workshop`. Corridors and stairs are traversal nodes only. **Unimplemented rooms must not hold mandatory evidence.**

## State (World §5.2 + Evidence §10.3, suggestions)
```yaml
world_state:
  phase: early_investigation        # pre_murder | early_investigation | later_investigation
  weather: severe
  wet_lab_secured: true
  wet_lab_inspection_authorized: false
  private_cabin_search_authorized: []
  bridge_record_review_authorized: false
  engineering_record_review_authorized: false
  selected_media_access_granted: false
investigation_state:
  collected_evidence_ids: []
  reviewed_evidence_ids: []
  thomas_motive_investigated: false
  daniel_motive_investigated: false
  medical_reconstruction_available: false
  medical_reconstruction_completed: false
  machinery_cause_excluded: false
  maya_motive_established: false
  maya_alibi_contradicted: false
  blunt_force_method_supported: false
  accusations_made: []
```
Also persist **NPC claims** (speaker, time, topic) so later contradictions can be checked (Evidence §7.4). EV-19 depends on this.

## Evidence quick map (Evidence §4)
| ID | What | Where | Gate |
|---|---|---|---|
| EV-00 | Elena's M-17 warning | journal at start | none |
| EV-01–03 | M-17 index, raw data, investor summary | dry_lab | audit access |
| EV-04–05 | Revision history, Thomas's pressure message | dry_lab | audit/specific access |
| EV-06, 17, 21–23 | Elena's preserved notes (incl. C-2, Maya, Sarah, Lucas, Noah entries) | **storage TBD** (cabin_elena?) | authorization TBD |
| EV-07 | Sarah/Daniel testimony on C-2 | conversation | — |
| EV-08–09 | Apparatus fault record, 23:10 cycle log | engineering_workshop | `engineering_record_review_authorized` or Daniel shares |
| EV-10 | Olivia's preliminary observations | medical_bay | conversation |
| EV-11 | Medical–technical reconstruction | medical_bay | needs EV-09 + EV-10 + detail + authorization |
| EV-12–13 | Scene inspection, reference-mass anomaly | wet_lab | `wet_lab_inspection_authorized` |
| EV-14 | Injury/weapon correspondence | medical_bay | EV-11 + EV-13 |
| EV-15 | Maya's improvement history | dry_lab | audit access |
| EV-16 | Draft Nereid agreement | dry_lab or cabin_maya (**TBD**) | authorized route |
| EV-18 | Lucas's partial corridor recording | editing_room | Lucas shares or Sarah authorizes |
| EV-19 | Maya's contradictory statement | conversation | persisted claim vs EV-18 |
| EV-20, 24, 26 | Dinner, Noah and discovery testimony | conversation | optional |

## Key gate (Evidence §10.2)
```yaml
medical_reconstruction_available:
  all_of: [reviewed EV-09, reviewed EV-10, medical_mechanical_detail_sufficient, medical_comparison_authorized]
on discuss_reconstruction_with_olivia:
  unlock: EV-11
  set: [medical_reconstruction_completed, machinery_cause_excluded]
```
The motive flags (`thomas_/daniel_motive_investigated`) are **not** prerequisites (Evidence §6.1).

## Talking and presenting evidence (Evidence §7.1)
When the player presents evidence, send the **evidence ID plus its verified content** to the NPC prompt. The NPC reacts but can't change the record. A validated outcome may set a confrontation flag.

## Accusation (Evidence §9, partly TBD)
- Correct and substantiated means all four flags in `canon.md` are set. The ending is the player handing the reconstruction to Sarah, not an arrest.
- A wrong accusation means Sarah asks for corroboration, or an inconclusive ending. Can the player continue? **TBD.**
- A correct guess without evidence is not a full win.

## Validation tests worth writing (Evidence §10.4, §11; World §10.4)
- Every location/object/evidence ID referenced exists, and every connection is reciprocal.
- Fixed times match: 18:10, 21:10, 22:20, 22:35, ~22:45, 23:10, 06:50.
- `machinery_cause_excluded` is reachable with both motive flags false.
- Casual talk to Thomas or Daniel does **not** unlock EV-11.
- A correct accusation without the four flags does not count as a win.
- A restricted room can't be entered via conversation alone.

## Open decisions that affect the engine
Ending/accusation flow · storage and access of Elena's notes · EV-16 placement · Maya's alibi (EV-19) · what authorizes the wet-lab and cabin searches · `medical_mechanical_detail_sufficient` content. **Stub these as config, don't invent canon.**
