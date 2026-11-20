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

Can be postponed (World §9): engine room, exterior deck, art for all 8 cabins, NPC animation, equipment controls.

## The UI never decides game logic
All "can I enter / did I unlock / is this a win" questions go to the engine. The UI renders whatever state the engine returns. Agree on the engine API with the backend owner before building screens.

## Ship layout for the map (World §2.2)
```
DECK 03   Bridge
           | upper stairs
DECK 02   Main corridor → Wet Lab ⇄ Dry Lab · Mess Hall · Medical Bay · Cabins · Editing Room
           | lower stairs
DECK 01   Lower corridor → Engineering Workshop · Engine Room · Equipment Storage → Aft Deck
```
Corridors and stairs can be map lines or short transitions with no own art.

## Journal entries (Evidence §7.3)
Each item shows **Observed** (exact text/clip/statement), optional **Interpretation**, **Questions**, and **Related entries**.
**Never show developer fields** like `supports: maya_motive_established`. That would spoil the solution.

## Spoiler hygiene
- Don't label the reference mass as a "weapon" in player-facing text (World §3.2).
- The start state comes from the engine. Don't preload discovery-scene details into the journal (Story §7.2).
- Leads like "Return to Olivia to compare…" appear only when the engine says the gate is open (Evidence §6.5).

## Open decisions affecting UI
Accusation flow and endings · which cabins are explorable · whether wet-lab inspection is a separate "supervised" mode · how the 06:50 opening is presented (briefing or conversations).
