# Task Summary: Frontend / UI

> Read `canon.md` first. Bibles win on conflict.
> Deep dives: World §2 (map), World §9 (MVP), Evidence §7.3 (journal), Evidence §9 (accusation).

## What the UI needs (World §9 "implement first")
1. **Ship map / location picker** with 2D room-to-room navigation. Free movement or 3D is **not** required (World §2.4).
2. **A visual per core room**: `bridge, wet_lab, dry_lab, mess_hall, medical_bay, crew_quarters, editing_room, engineering_workshop`.
3. **Inspection hotspots** per room: a few objects, not every prop (object IDs in World §3).
4. **NPC conversation**: chat with whoever is present, plus a "present evidence" action.
5. **Permission-aware navigation**: locked rooms are visible but blocked, with an in-world reason ("The captain has secured the wet lab").
6. **Journal / evidence inventory.**
7. **Accusation screen**: present reasoning and evidence to Sarah (exact flow **TBD**).

Can be postponed (World §9): engine room, exterior deck, detailed art for the two shared sleeping rooms, NPC animation, equipment controls.

## The UI never decides game logic
All "can I enter / did I unlock / is this a win" questions go to the engine. The UI renders whatever state the engine returns. Agree on the engine API with the backend owner before building screens.

## Ship layout for the map (World §2.2)
```
DECK 03   Bridge
           | upper stairs
DECK 02   Main corridor → Wet Lab ⇄ Dry Lab · Mess Hall · Medical Bay · Shared sleeping rooms · Editing Room
           | lower stairs
DECK 01   Lower corridor → Engineering Workshop · Engine Room · Equipment Storage → Aft Deck
```
Corridors and stairs can be map lines or short transitions with no own art.

## Journal entries (Evidence §7.3)
Each item shows **Observed** (exact text/clip/statement), optional **Interpretation**, **Questions**, and **Related entries**.
**Never show developer fields** like `supports: maya_motive_established`. That would spoil the solution.

## Spoiler hygiene
- Don't label the reference mass as a "weapon" in player-facing text (World §3.2).
- The start state comes from the engine. Only Sarah’s limited briefing facts may be supplied; do not preload the cover exchange, arrival order or reactions (Story §§7.2–7.3).
- Leads like "Return to Olivia to compare…" appear only when the engine says the gate is open (Evidence §6.5).

## Open decisions affecting UI
Accusation flow and endings · exact opening speech and reminder of Elena’s warning · optional EV-11 prerequisite for reference-mass inspection. Access progression and close wet-lab inspection are fixed.

**Fixed opening:** Show Sarah’s brief speech outside the open wet lab after the player arrives late; Olivia continues examining Elena. Sarah mentions Lucas’s discovery/call and her opening the door/keeping others out, but not the cover exchange or cause of death. Cut to Room B for player control. Elena’s body remains behind barrier tape. NPCs stay at their World §8 stations; conversations are available without search rights and require no entrance-dialogue flow. Room/record inspections and private searches require consent or Sarah’s evidence-based authorization. Elena’s warning unlocks the dry-lab/Elena-belongings grant through Sarah; EV-18 supports the Maya-belongings grant. The engine owns all state changes.
