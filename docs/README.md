# Beneath the Surface — Documentation Guide (v0.2)

This folder contains the narrative and design references for the AI murder mystery *Beneath the Surface*. The bibles describe the same game from different perspectives: what happened, what each character knows, what exists aboard the ship, and what the player can discover.

These are internal development documents and contain the complete solution. They are not player-facing material.

## Document structure

| Document | What belongs here |
|---|---|
| [Story Bible](story_bible.md) | Setting, project background, canonical events, murder solution, timeline, and overall narrative logic. |
| [World Bible](world_bible.md) | Ship layout, connected rooms, objects, environmental conditions, physical constraints, and access boundaries. |
| [Evidence Bible](evidence_bible.md) | Clue IDs, contents, sources, discovery conditions, what evidence supports, and how investigative conclusions become available. |
| [Character Bibles](characters/) | One file per living suspect: personality, voice, relationships, private knowledge, beliefs, secrets, testimony, and responses to evidence. |

The character files cover [Sarah Morgan](characters/sarah_morgan.md), the captain; [Daniel Reyes](characters/daniel_reyes.md), the engineer; [Maya Chen](characters/maya_chen.md), the scientist; [Thomas Blake](characters/thomas_blake.md), the investor representative; [Olivia Hart](characters/olivia_hart.md), the medic; and [Lucas Weber](characters/lucas_weber.md), the filmmaker.

Start with the Story Bible for context, then consult the documents relevant to your task. Task-specific summaries should reference these sources and distinguish settled facts from open decisions; they do not replace the bibles.

## Narrative overview

An independent scientific auditor joins Pelagos Carbon’s research expedition aboard the *RV Meridian*. Lead scientist Elena Fischer is found dead while severe weather prevents outside investigators from boarding. The player investigates through conversations, records, and examination of the ship.

The mystery connects misleading investor claims, an earlier ecological cover-up, and Maya’s secret negotiations to transfer confidential research to Nereid Technologies. Maya impulsively kills Elena and improvises an apparent equipment accident. A genuine apparatus failure gives Daniel a sincere but mistaken fear that his negligence caused the death. Other characters have their own compromises and reasons to withhold information.

The central distinction is between misconduct and murder: a secret, a lie, or a plausible motive does not establish who killed Elena. The solution must follow from combined evidence, with a confession optional.

## Core principles

- **Separate truth, perspective, and proof.** The Story Bible owns objective events; character bibles define individual knowledge and beliefs; the World Bible defines physical possibilities; the Evidence Bible defines what the player can establish.
- **Keep knowledge local.** NPCs know only their established experiences, expertise, and information explicitly received during play. Player discovery does not automatically inform every NPC. Build runtime prompts from the relevant character and permitted state, not the complete author-facing story or other characters’ private bibles.
- **Let rules control state.** The game engine owns evidence collection, permissions, persistent admissions, and conclusion prerequisites. Language models express character responses within those boundaries rather than inventing facts or granting access.
- **Preserve a fair investigation.** The suggested clue order is a preferred dramatic progression, not a mandatory sequence. Conclusions require supporting evidence. Restricted spaces and private records need an authored access route.
- **Distinguish backstory from player knowledge.** Play begins after the discovery response. The player remembers Elena’s earlier warning but learns discovery details through witnesses; there is no automatic eyewitness knowledge.
- **Keep changes consistent across documents.** An event change may affect testimony, room access, and clues. Update the relevant bibles together and provide reviewable changes. Keep authors’ spoilers out of public-facing assets.

## Remaining TBDs

**TBD** means unresolved; **PROPOSED** marks a candidate rather than confirmed canon. Neither is permission for an NPC or implementation to invent an answer. Detailed decision lists remain in Story §12, World §11, Evidence §12, and each character’s §9.

| Area | Main decisions still open |
|---|---|
| Movements and alibis | Actual locations, Maya’s false account, corroboration, essential watch duties, relevant door behavior, and sound/recording consistency. |
| Footage | Camera position, clip content, timestamps, retention, and authorized review; how recordings contradict claims without showing everything. |
| Physical reconstruction | Scene geometry and traces, evidence linking the reference mass to the attack, and observations excluding both the apparatus and a secondary fall. |
| Evidence access and presentation | Storage and discovery of Elena’s preserved materials, access to the draft agreement, readable M-17 comparisons, approval records, and maintenance evidence. |
| Character disclosures and actions | Remaining admission conditions, Daniel’s possible record alterations, how witnesses learned of certain conversations, and optional investigative hints. |
| Solution and endings | Evidence sufficient to distinguish Maya from alternative attackers, accusation requirements, responses to incomplete or wrong accusations, and optional confession. |
| World and implementation detail | Clue-relevant dimensions and sightlines, searchable cabins, examination facilities, post-discovery NPC placement, and visual assets. |

A small technical prototype can proceed with an explicitly defined subset of rooms, clues, and conversations. A complete solvable investigation needs the alibi, physical-proof, access, and accusation decisions resolved together. Exact calendar dates and additional detail about settled historical incidents are deliberately unnecessary unless a specific clue requires them.
