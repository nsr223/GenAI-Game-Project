# Canon Cheat Sheet (shared by every task)

> **Spoilers.** Condensed from the bibles in `docs/` (v0.3). If anything here disagrees with a bible, **the bible wins**: fix this file in the same PR.
> Section references like *Story §6* point to `docs/story_bible.md`, *World* to `docs/world_bible.md`, *Evidence* to `docs/evidence_bible.md`.

## The game in one paragraph
*Beneath the Surface* is a murder mystery aboard the research vessel **RV Meridian** (North Atlantic, ~400 km west of Ireland, mid-December, heavy storm). The player is an **independent scientific auditor**, not a police officer. The evening before her death, lead scientist **Dr. Elena Fischer** warned the player that experiment **M-17** "doesn't add up". Next morning she is found dead in the **wet lab**, beside a faulty sampling apparatus, and it looks like an accident. The player interrogates six AI-driven suspects and uncovers three real scandals, but only one of them led to murder.

## The solution (Story §6)
| | |
|---|---|
| **Murderer** | Dr. Maya Chen |
| **Weapon** | 2 kg stainless-steel **reference mass** (calibration object), returned to the calibration station afterwards |
| **Location** | Wet laboratory |
| **Time** | ~22:45 (meeting began 22:35, Maya gone by ~23:00) |
| **Motive** | Elena was going to report Maya's secret negotiations to sell her improvement to the competitor **Nereid Technologies** |
| **Staging** | Maya arranged the body to suggest the apparatus's service cover fell on Elena |

**Central twist:** At **23:10** a real apparatus malfunction occurs (the cover drops). Engineer **Daniel** believes his neglected fault killed Elena, which leads to a false quasi-confession. But the cover never hit her: she was already dead.

## Cast (exactly 8 people aboard, never invent more)
| ID (suggested) | Character | Role | Secret | Murderer? |
|---|---|---|---|---|
| `maya_chen` | Dr. Maya Chen | Research scientist | Selling her improvement to Nereid; **the murder** | **Yes** |
| `daniel_reyes` | Daniel Reyes | Chief engineer | Covered up ecological damage at trial C-2; left the apparatus fault unresolved | No (thinks he might be) |
| `thomas_blake` | Thomas Blake | Investor representative | Approved misleading M-17 investor summary (~€8M funding round) | No |
| `sarah_morgan` | Capt. Sarah Morgan | Captain | Continued an operation in bad weather under Thomas's pressure | No |
| `olivia_hart` | Olivia Hart | Medic | Misreported an old injury (Noah Bennett) to protect a colleague | No |
| `lucas_weber` | Lucas Weber | Documentary filmmaker | Kept recording without consent; holds key footage | No |
| — | Dr. Elena Fischer | Lead scientist | Victim | — |
| — | Player | Auditor | — | — |

Noah Bennett and Adrian Cole are **backstory only**, not aboard.

## Timeline (Story §7, fixed)
| Time | Event |
|---|---|
| 18:10 | Elena warns the player in the dry lab (backstory, not playable) |
| 20:00–20:40 | Dinner; Elena refuses to endorse publication; remaining discussion TBD |
| 21:10 | Thomas argues with Elena in the mess hall |
| ~21:30–22:15 | Lucas documents Sarah’s bridge preparations; learns Wednesday’s severe-weather forecast |
| 22:00 | Elena confronts Daniel in his workshop about C-2 |
| 22:20 | Daniel leaves the wet lab: cover left raised, pending cycle not cleared |
| ~22:30–22:35 | Lucas incidentally films Maya heading toward the labs; does not notice her or review footage that night |
| 22:35 | Maya meets Elena in the wet lab |
| ~22:45 | Maya kills Elena |
| 23:10 | Automated cycle resumes, cover drops (nobody hears it, no alert) |
| 06:50 | Lucas sees Elena through the door panel and calls for help |

Actual evening movements and retirements are fixed in Story §7.1; claims and corroboration remain separate. By 23:00 the surviving others are in their cabins; Sarah stays on the bridge overnight. During dinner nobody is on the bridge: the propulsion engine is on hold, electrical/monitoring systems remain powered, and Sarah receives bridge notifications through a direct connection. This is an intentional story simplification. Relief/rest and discovery-response coverage remain TBD; autopilot does not justify sleeping on watch. Lucas may repeat Sarah’s limited Wednesday forecast briefing, not all navigation/weather facts.

Play begins **after** the discovery response. The player learns the details only through witnesses.

## Winning (Evidence §9, ending mechanics still TBD)
A substantiated accusation of Maya needs four flags:
1. `maya_motive_established` (EV-16 + EV-17)
2. `maya_alibi_contradicted` (EV-18 + EV-19)
3. `machinery_cause_excluded` (EV-09 + EV-10 → EV-11)
4. `blunt_force_method_supported` (EV-13 + EV-14)

Guessing Maya without that evidence is **not** a full win. Confession is optional.

## Rules that apply everywhere (Story §11)
- One fixed solution; the LLM never changes the murderer, time, weapon or place.
- No omniscient NPCs: each one knows only their own bible section.
- **The engine owns state** (evidence, access, flags). The LLM only voices characters and never sets flags.
- No invented people, rooms, documents, or decisive evidence.
- **TBD** in a bible means *not decided*. Don't silently decide it in code or prompts; ask the team.

## Biggest open TBDs that block a complete game
Maya's false alibi · technical realization/access of Lucas’s fixed corridor shot · where Elena's preserved notes are stored · physical trace on the reference mass · how the accusation/ending works. Full lists: Story §12, World §11, Evidence §12, each character §9.
