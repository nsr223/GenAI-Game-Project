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
1. Evidence-team implementation of **Lucas's clip** and Maya’s post-contradiction response. Her initial false alibi is fixed (Story §7.1 / EV-19). The shot of Maya inside the wet lab around 22:35 is fixed; few-second corridor-window view of Maya inside, invisible partner and footsteps/movement-only audio are fixed; framing, timestamp validation and authorized review remain open. Remember the internal wet/dry lab door (World §8.3).
2. **Physical/medical mechanism**: the trace on the reference mass, and what excludes a cover-induced fall.
3. **Reconstruction access**: what `medical_mechanical_detail_sufficient` and `medical_comparison_authorized` mean in-story.
4. **Placement and permissions**: exact containers/media for Elena’s notes and Maya’s draft, both fixed in their personal belongings; Sarah’s grant routes are fixed. No password guessing.
5. **Numbers and wording**: readable M-17 values and document text.
6. **Ending**: accusation flow; what happens after a wrong or unsupported accusation.

Actual evening movements are fixed in Story §7.1. Elena announces her intended Daniel visit to Olivia/Thomas; they do not witness it. Lucas learns Wednesday’s severe-weather forecast during his roughly 45-minute bridge session with Sarah. Sarah stays on the bridge overnight; the others retire by 23:00. Dinner coverage is settled: nobody on the bridge, propulsion engine on hold, electrical/monitoring systems powered, and Sarah connected directly for notifications of unexpected monitored events (intentional story simplification).

Still open: remaining claimed accounts and corroboration beyond the fixed bedtime observations; dinner dialogue beyond Elena’s refusal; exact additional bridge briefing details; opening speech/reminder presentation; Daniel’s past maintenance-record artifact details and hiding location. The 23:10 clunk stays unheard. Olivia’s fictional *Clinical Care Review* magazine is atmosphere, not evidence.


**Sleeping rooms / alibi (Story §7.1, World §3.6):** Two rooms, two bunk beds each. Room A: Olivia above Maya, Lucas above Elena. Room B: Sarah above Thomas, Daniel above the player. Olivia sees Maya in bed and Elena’s bunk empty around 22:20; she sleeps before Maya leaves around 22:30. Maya returns around 22:57. Lucas organizes his equipment and the day’s recording files around 22:35–22:55 as part of his usual daily routine, without reviewing any footage; around 23:00 he sees Maya and Olivia apparently asleep. Maya is awake and hears him arrive. Her fixed lie is: “I was already in bed when Olivia came in. I did not leave the room again that night.” EV-18 contradicts it. Neither bedtime sighting proves continuous presence. Daniel sees Thomas snoring around 22:20. Sarah’s watch assignment is public, not continuous independent corroboration. Lucas wakes around 06:40–06:45, sees Elena’s empty bunk, assumes she rose earlier, gets ready, checks the mess and then the labs, discovering her at 06:50.

**Daniel/Elena sighting:** Their workshop confrontation is 21:50–22:00; maintenance is 22:05–22:15; Daniel and Olivia talk around 22:15–22:20. Daniel and Elena notice each other during maintenance while she works in the dry lab. If told Olivia’s later empty-bunk observation, Daniel can offer his earlier sighting as context, not proof of Elena’s exact location at 22:20 or afterward.

## Hand-off to code
Once decided, put clue records into `data/evidence.yaml` and rooms into `data/locations.yaml` (formats: Evidence §10.1, World §10.1). The engine reads data, not prose.

**Opening and permissions (Story §7.3):** Everyone except Lucas and Sarah is in bed at the call; different waking/reaction times explain direct-route arrivals. Maya deliberately avoids being first and never mentions why. Sarah’s briefing gives only the basic discovery/door-opening facts while Olivia continues examining Elena; no cover exchange or cause of death is disclosed. After the cut NPCs stay at fixed stations: Sarah/bridge, Olivia/medical bay, Thomas/mess, Lucas/editing room, Daniel/workshop, Maya/dry lab. Elena remains behind barrier tape in the wet lab. NPC conversations are available without search permission; no doorway-dialogue mechanic is needed. The player starts in Room B with access to their own belongings. Elena’s warning leads Sarah to authorize dry-lab investigation and Elena’s belongings. Owners may consent to searches; only Sarah may override refusal on serious evidence. EV-18 authorizes a search of Maya’s belongings for EV-16. Wet-lab permission permits close inspection; a separate reference-mass gate after EV-11 remains TBD. No other personal belongings currently hold evidence. Daniel does not tamper with murder-night records after discovery.
