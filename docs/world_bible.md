# Beneath the Surface — World Bible

> **Status:** Initial draft (v0.2) · **Suggested repository path:** `docs/world_bible.md`  
> **Audience:** Development team · **Spoilers:** Internal design reference; mentions the crime scene and restricted areas.
>
> **Purpose of this document:** The World Bible is the single source of truth for the **physical game world** of *Beneath the Surface*: the *RV Meridian*, its decks and rooms, how locations connect, what objects physically exist, which spaces can be accessed, and what environmental rules apply. It gives writers, artists, and developers a shared reference so navigation, dialogue, evidence placement, and visuals never contradict one another. The World Bible does **not** decide who committed the murder or what each clue proves; those facts belong to the Story Bible and Evidence Bible.
>
> **Scope and ownership:** This document owns physical locations, connections, room atmosphere, baseline object inventories, movement restrictions, and spatial consistency. The **Story Bible** owns historical events and the murder timeline; **Character Bibles** own NPC knowledge and behavior; the **Evidence Bible** owns clue content, precise placement, discovery requirements, and revelation gates; the **game state** owns which rooms and objects are currently accessible. Details marked **TBD** are proposals, not established canon.

---

## 1. World at a Glance

### 1.1 Setting

- **Primary location:** *RV Meridian*, a compact, privately operated oceanographic research vessel.
- **Project company:** Pelagos Carbon.
- **Calendar:** Mid-December, with no fixed year or exact calendar dates. The mission departed Galway on Sunday with the player aboard. Elena is murdered Tuesday evening; discovery is Wednesday at 06:50, with player control beginning after the initial response. Historical incidents retain their relative dates (about a year ago, eight months ago, and several weeks ago).
- **Region / route:** Galway, Ireland → offshore North Atlantic sampling stations west of Ireland → Galway. On the murder night the ship is approximately **53°N, 16°W**, roughly **400 km west of the Irish coast**. This is an approximate narrative position, not an exact stationary waypoint; intermediate sampling stations need no fixed coordinates for the MVP.
- **Mission:** Final-stage testing of an experimental ocean carbon-removal system.
- **Time:** Player control begins after the morning discovery response. Elena's previous-evening warning remains pre-game backstory; discovery details must be learned from witnesses. The setting is mid-December; the year and exact calendar dates are deliberately unspecified and do not require further decisions.
- **People aboard:** Exactly **eight**: the player, Dr. Elena Fischer, and the six living suspects — Sarah Morgan, Daniel Reyes, Maya Chen, Thomas Blake, Olivia Hart, and Lucas Weber.
- **Situation:** Bad weather makes a prompt return or safe transfer impractical; the captain remains in contact with authorities as conditions permit.
- **Visual tone:** Functional, lived-in, modern research vessel; not a luxury yacht, warship, or futuristic spaceship.

### 1.2 World design goals

1. **Small enough to learn:** The player should recognize major rooms and routes quickly.
2. **Believable as a working ship:** Rooms have everyday purposes beyond containing clues.
3. **Useful for investigation:** Location, access, and sightlines can support or challenge testimony.
4. **Consistent under AI dialogue:** NPCs refer only to established rooms, routes, objects, and ship capabilities.
5. **Compatible with a student-project MVP:** Eight core explorable areas; auxiliary passageways and a small number of optional subrooms.
6. **Not artificially isolated:** Weather delays outside assistance, but the vessel can still report the incident and is not in a supernatural communications blackout.

### 1.3 Fixed environmental facts

- The *Meridian* is a **single ship**; the player cannot disembark during the playable investigation.
- The **wet laboratory** is where Elena is found; the **dry laboratory** is where she gives her initial warning to the player.
- The **sampling apparatus** in the wet lab has an unresolved fault. Its abnormal automated cycle occurs at **23:10** on the murder night; the Story Bible fixes the significance of this time.
- The sampling apparatus is **not** the cause of Elena's death. Whether the player can establish that fact depends on narrative and evidence progression, **not** on changing what exists in the room.
- There are **no additional speaking crew members** or surprise witnesses beyond the defined cast. Background automation can simplify ship operations, but NPCs must not invent named deckhands or officers.
- Severe weather is an environmental constraint, not an excuse for every technical failure. Communications and safety systems must behave consistently.

---

## 2. Ship Layout and Navigation

### 2.1 Deck organization

The ship has **three confirmed playable levels**. The room connections in §2.3 are established world canon; this remains a gameplay layout rather than a naval architecture blueprint.

| Deck | Function | Main playable spaces |
|---|---|---|
| **Deck 03 — Command** | Navigation and contact with shore | Bridge / communications station |
| **Deck 02 — Research & Living** | Scientific work, social spaces, sleeping, medical care | Wet lab, dry lab, mess hall & galley, medical bay, accommodation corridor/cabins, documentary editing room |
| **Deck 01 — Engineering & Working Deck** | Maintenance, propulsion support, research equipment handling | Engineering workshop; auxiliary engine room, equipment storage, exterior aft work deck |

### 2.2 Schematic map

**This is a connectivity sketch, not to scale.** Doors, ladders, and corridor lengths can be adjusted as long as the connections in Section 2.3 stay consistent.

```text
                DECK 03 — COMMAND
          +-------------------------+
          | Bridge + Communications |
          +------------+------------+
                       |
                  Upper Stairs
                       |
                DECK 02 — MAIN
   +------------------------------------------------+
   |                 Main Corridor                  |
   +--+---------+---------+---------+---------+-----+
      |         |         |         |         |
   Wet Lab   Mess Hall  Medical   Cabins    Editing
      |      & Galley     Bay     Corridor    Room
   Dry Lab*                         |
      |                        Private cabins
      +---- Main Corridor      (controlled access)
                       |
                  Lower Stairs
                       |
                DECK 01 — LOWER
                Lower Corridor
            /          |          \
   Engineering       Engine     Equipment
    Workshop          Room       Storage
                                    |
                              Exterior Aft Deck
```

`*` The wet and dry laboratories have a **secondary internal connecting door**, in addition to their corridor doors. This route must be considered when designing alibis, camera coverage, and movement records. Its lock/log behavior is **TBD**.

**Shared door identity:** `wet_lab_door_internal` and `dry_lab_internal_door` are room-facing aliases for the same physical door, with canonical ID `lab_internal_door`. Both aliases use one shared open/closed and locked/unlocked state and the same access/log configuration. They must never be implemented as independent doors. Exact lock and logging behavior remains **TBD**.

### 2.3 Confirmed room connections

The existing connections below are **confirmed and bidirectional**. Permissions may restrict a route without removing its physical connection. Future topology changes require a coordinated Bible update. Stairs and corridors are traversal nodes, not separate mystery-solving scenes.

| Location ID | Connects directly to |
|---|---|
| `bridge` | `upper_stairs` |
| `upper_stairs` | `bridge`, `main_corridor` |
| `main_corridor` | `upper_stairs`, `lower_stairs`, `wet_lab`, `dry_lab`, `mess_hall`, `medical_bay`, `crew_quarters`, `editing_room` |
| `wet_lab` | `main_corridor`, `dry_lab` |
| `dry_lab` | `main_corridor`, `wet_lab` |
| `mess_hall` | `main_corridor` |
| `medical_bay` | `main_corridor` |
| `crew_quarters` | `main_corridor`, individual cabin doors |
| `editing_room` | `main_corridor` |
| `lower_stairs` | `main_corridor`, `lower_corridor` |
| `lower_corridor` | `lower_stairs`, `engineering_workshop`, `engine_room`, `equipment_storage` |
| `engineering_workshop` | `lower_corridor` |
| `engine_room` | `lower_corridor` |
| `equipment_storage` | `lower_corridor`, `aft_work_deck` |
| `aft_work_deck` | `equipment_storage` |

**Door viewing panels:** Most communal and working rooms have a small glazed panel in the corridor door, including the wet and dry labs. The wet-lab panel is `wet_lab_viewing_panel`; the dry-lab panel is `dry_lab_viewing_panel`. The wet-lab panel allows Lucas to notice Elena on the floor beside the apparatus from the corridor; it does not reveal the full room, precise injury, or every object. Other panel sightlines must be checked before being used as evidence. Private cabins and confidential medical spaces are exceptions; do not grant public views of private records or examinations. Panels do not grant entry or make closed doors acoustically transparent.

**Movement rule:** Nobody moves instantly between disconnected locations. Any route discussed by a character or represented in logs must be physically possible on this graph. A character can still lie about their route.

### 2.4 Traversal and pacing

- The player uses **room-to-room navigation**; free 3D movement is optional and not required for the MVP.
- Rooms may contain several **inspection hotspots** rather than allowing interaction with every decorative object.
- Corridors and stairs can be represented as a clickable map, short transition, or small illustrated scene.
- NPCs may change locations according to game events, but cannot teleport; exact schedules and alibis belong in the Story Bible and Character Bibles.
- Do not make the physical layout itself reveal the murderer. The solution should require comparing multiple kinds of evidence.

---

## 3. Core Explorable Areas

For every room below, **initial access** means the baseline permission at the beginning of an investigation phase, **not** a promise that the player can enter whenever they want. Access is controlled by game state and the captain's authorization when appropriate.

### 3.1 Bridge and Communications Station

| Field | Definition |
|---|---|
| **ID** | `bridge` |
| **Deck** | 03 — Command |
| **Connected to** | `upper_stairs` |
| **Main NPC association** | Captain Sarah Morgan |
| **Initial access** | Knock/request entry; ordinary conversation possible, consoles controlled |

**Purpose and appearance.** Compact ship's bridge with navigation screens, chart display, radar/AIS, weather readouts, radio and satellite communication equipment, and a captain's desk. Windows overlook the sea and make worsening weather visible.

**Baseline interactable objects:**
- `bridge_navigation_console` — current ship position and route display.
- `bridge_weather_display` — recorded and current conditions.
- `bridge_log_station` — official operational record interface.
- `bridge_comms_console` — communications equipment; player cannot independently contact arbitrary parties.
- `bridge_noticeboard` — shift notices and posted safety instructions (ambient details only unless defined as clues).

**World constraints.** The player cannot alter navigation, disable communications, or issue shipwide instructions. Any access to official records requires an authorized workflow. On the murder night and during the initial investigation, the ship remains under power at reduced speed in open water, maintaining steerage and adjusting its heading to the sea conditions. It is neither anchored nor precisely holding a fixed coordinate. Exterior research deployment is suspended; indoor records and the sampling station remain powered, allowing the pending 23:10 cycle. Exact headings and speeds are not clue-bearing facts and need not be simulated.

### 3.2 Wet Laboratory — Crime Scene

| Field | Definition |
|---|---|
| **ID** | `wet_lab` |
| **Deck** | 02 — Research & Living |
| **Connected to** | `main_corridor`, `dry_lab` |
| **Main NPC association** | Elena Fischer (before death); Daniel for equipment maintenance; Maya for experiments |
| **Initial access** | Accessible for routine audit work before the death; **secured after the body is found** |

**Purpose and appearance.** A practical seawater-processing laboratory with anti-slip flooring, stainless-steel benches, water lines, pumps, sample containers, and an industrial sampling apparatus. The air is humid; machinery noise and a faint chemical/metallic smell distinguish it from the dry lab.

**Baseline interactable objects:**
- `wet_lab_sampling_apparatus` — automated seawater sampling/filtration station with pump, rotary selector, collection weighing platform, and broad hinged metal service cover. Its worn support catch and pending verification task are author-facing facts; ordinary inspection does not automatically reveal them.
- `wet_lab_calibration_station` — tools and storage including a **2 kg squat cylindrical stainless-steel reference mass with a defined circular rim**, used to check the sampling station's weighing platform. Do not label it a weapon in ordinary player-facing descriptions.
- `wet_lab_sample_bench` — containers, sample rack, and controlled treated/untreated experimental tanks.
- `wet_lab_treatment_unit` — a small flow-through dosing-and-mixing unit using prepared sodium-hydroxide solution; distinct from the sampling station and its cover. Its research controls are not freely operable by the player. No additional explorable room is introduced.
- `wet_lab_workstation` — local equipment/status display.
- `wet_lab_storage_cabinet` — supplies and protective equipment.
- `wet_lab_door_main` and `wet_lab_door_internal` — two possible access routes.
- `wet_lab_viewing_panel` — small glazed panel in the main corridor door; permits the established discovery view. Lucas lacks entry authorization and cannot open this door; Sarah opens it after responding to his call.

**Discovery access:** At 06:50 Lucas sees Elena through the main-door panel but cannot open the door. Thomas arrives a few seconds after Lucas calls; Olivia and Sarah arrive together next; Daniel arrives about half a minute after them; Maya arrives shortly after Daniel. Sarah opens the door when she arrives with Olivia, who approaches Elena; the others remain near the doorway. The shared cover exchange occurs after Maya arrives. The player is not a discovery witness. Sarah stops Daniel before he touches the apparatus. This is an **unexplained-death scene**, not a confirmed murder finding (Story §7.2).

**World constraints.** After the initial assessment, Sarah secures **both entrances**: the main corridor door and the shared internal door from the dry lab (`lab_internal_door`). Both routes require the same wet-lab inspection authorization; ordinary dry-lab access cannot bypass the restriction. Scene security begins after discovery, not automatically at the hidden time of the murder. The player may later perform **supervised inspection**, but may not freely move the body, operate machinery, remove physical evidence, or contaminate the scene. Descriptions must reflect the current stage of scene preservation.

**Important separation:** This document establishes that a calibration station and sampling apparatus physically exist. The **Evidence Bible** must specify which specific item is evidentiary, what can be examined, and what it proves. Do not automatically tell the player that a calibration object was the murder weapon.

### 3.3 Dry Laboratory — Research Analysis

| Field | Definition |
|---|---|
| **ID** | `dry_lab` |
| **Deck** | 02 — Research & Living |
| **Connected to** | `main_corridor`, `wet_lab` |
| **Main NPC association** | Elena Fischer; Maya Chen; player during audit |
| **Initial access** | Generally accessible to the player for audit-related work |

**Purpose and appearance.** A quieter, climate-controlled data workspace with computers, instrument dashboards, monitor walls, scientific notes, and storage for electronic records. This is where Elena privately warns the player about **experiment M-17 at 18:10**.

**Baseline interactable objects:**
- `dry_lab_analysis_terminal` — review approved datasets and summaries.
- `dry_lab_experiment_index` — catalog of experiments, including M-17.
- `dry_lab_shared_workstation` — general research workspace.
- `dry_lab_document_shelf` — protocols and printed reference material.
- `dry_lab_internal_door` — access toward wet lab, subject to the same route rules.
- `dry_lab_viewing_panel` — small glazed panel in its corridor door; exact evidence-bearing sightlines remain to be checked.

**World constraints.** Access to a room does **not** imply unrestricted access to private drives, accounts, or deleted files. Dataset permissions and evidence unlocks are handled by the Evidence Bible and game state. The computers cannot freely access arbitrary real-world websites unless explicitly implemented.

### 3.4 Mess Hall and Galley

| Field | Definition |
|---|---|
| **ID** | `mess_hall` |
| **Deck** | 02 — Research & Living |
| **Connected to** | `main_corridor` |
| **Main NPC association** | Shared social space; Lucas often present |
| **Initial access** | Public to everyone aboard |

**Purpose and appearance.** Combined dining and small cooking area with a bolted-down table, compact galley, coffee equipment, refrigerator, and personal mugs. Warmer lighting and ordinary clutter contrast with the technical rooms.

**Baseline interactable objects:**
- `mess_table` — communal seating and conversation focal point.
- `galley_counter` — ordinary kitchen equipment.
- `mess_noticeboard` — shared notices and meal schedule.
- `mess_coffee_station` — ambient interaction hotspot.

**World constraints.** Ideal location for organic NPC encounters, group conversations, and reconstructing the dinner discussion. The room is public, so characters should not treat conversations here as automatically private. New decisive clues must not appear just because an LLM describes an interesting object.

### 3.5 Medical Bay

| Field | Definition |
|---|---|
| **ID** | `medical_bay` |
| **Deck** | 02 — Research & Living |
| **Connected to** | `main_corridor` |
| **Main NPC association** | Olivia Hart |
| **Initial access** | Player may enter to speak with Olivia; records and stored medical materials restricted |

**Purpose and appearance.** Compact infirmary with an examination bed, secured medical cabinets, basic instruments, diagnostic workstation, and limited treatment equipment.

**Baseline interactable objects:**
- `medical_exam_station` — Olivia's clinical workspace.
- `medical_records_terminal` — medical documentation with strict access control.
- `medical_supply_cabinet` — medications and consumables; not a free inventory.
- `medical_report_desk` — place to discuss authorized findings.

**World constraints.** Olivia does not instantly possess a complete forensic answer. The precise evidence and the conditions for a medical/technical reconstruction belong to the Evidence Bible. As in Story Bible §10, investigating Thomas's and Daniel's motives before the conclusive reconstruction is a **preferred progression, not a mandatory order**. The conclusion depends on the evidence and analysis available, not on completing both motive investigations. Olivia may share preliminary concerns early and must not withhold an established finding solely to preserve pacing. Physical facts remain unchanged regardless of discovery order.

### 3.6 Crew Quarters and Private Cabins

| Field | Definition |
|---|---|
| **ID** | `crew_quarters` |
| **Deck** | 02 — Research & Living |
| **Connected to** | `main_corridor`; individual private cabin doors |
| **Main NPC association** | All onboard individuals |
| **Initial access** | Corridor accessible; cabins are private and normally locked or access-controlled |

**Purpose and appearance.** A short accommodation passage with eight compact assigned cabins. Each contains a narrow bed, storage, small desk, and a few character-specific possessions. The player has their own cabin, which can serve as a quiet place to review notes.

**Proposed cabin IDs:**
- `cabin_player`
- `cabin_elena`
- `cabin_sarah`
- `cabin_daniel`
- `cabin_maya`
- `cabin_thomas`
- `cabin_olivia`
- `cabin_lucas`

**Baseline interactable objects:**
- `player_desk` — player case notes/journal (optional UI shortcut).
- `cabin_door_<character>` — access gate for each cabin.
- `cabin_desk_<character>` — character-specific furniture; contents not automatically accessible.
- `cabin_storage_<character>` — personal belongings; contents decided in Evidence Bible.

**World constraints.** The player may not search another person's possessions solely because that cabin appears on the map. Permission, consent, or a story-authorized investigation step is required. Elena's cabin can become an important late or mid-game scene, but the precise authorization and preserved files are **TBD**.

**MVP note.** Render the quarters as one corridor and make only cabins with meaningful interactions individually explorable. The others can remain doors with dialogue flavor, reducing art and navigation work.

### 3.7 Documentary Editing Room

| Field | Definition |
|---|---|
| **ID** | `editing_room` |
| **Deck** | 02 — Research & Living |
| **Connected to** | `main_corridor` |
| **Main NPC association** | Lucas Weber |
| **Initial access** | Conversation access generally possible; media drives and editing projects are controlled by Lucas |

**Purpose and appearance.** A former survey office converted into a small media workspace: editing laptop, monitors, camera storage, headphones, charging equipment, and a few pinned shot lists.

**Baseline interactable objects:**
- `editing_workstation` — video and audio editing surface.
- `camera_storage` — cameras and removable media.
- `media_drive_case` — organized drives; exact filenames/clips defined elsewhere.
- `editing_shot_list` — filming plans or harmless reference information.

**World constraints.** Lucas records selected areas and moments, not the entire ship continuously. Videos cannot reveal an angle that no camera captured. **Exact recording times, footage content, camera positions, and evidence access belong to the Evidence Bible.** The room is not an unlimited surveillance control center.

### 3.8 Engineering Workshop

| Field | Definition |
|---|---|
| **ID** | `engineering_workshop` |
| **Deck** | 01 — Engineering & Working Deck |
| **Connected to** | `lower_corridor` |
| **Main NPC association** | Daniel Reyes |
| **Initial access** | May enter with permission or while accompanied; maintenance systems remain controlled |

**Purpose and appearance.** An industrial workshop with spare parts, tools, maintenance records, equipment diagrams, and electronics test equipment. Louder and more utilitarian than the research spaces.

**Baseline interactable objects:**
- `engineering_maintenance_terminal` — authorized fault and service records.
- `engineering_parts_cabinet` — spare components and labeled storage.
- `engineering_workbench` — tools and ongoing repair work.
- `engineering_safety_board` — safety protocols and routine maintenance notices. Any notice revealing the current unresolved fault requires an authored evidence definition and discovery conditions.

**Maintenance knowledge boundary:** Past maintenance problems are familiar to Elena and all six suspects, but initially unknown to the player. That general history can be learned through appropriate conversation or authored records; it does not establish knowledge of the specific current fault or its severity. Daniel's detailed knowledge is separate. Ambient room descriptions, visible notices, and default equipment displays must not expose the concealed danger or imply that other characters knew it without supporting evidence.

**World constraints.** Engineering logs and scientific datasets are different systems. The 23:10 equipment cycle must not be accidentally moved in time by generated dialogue or UI. The player can read or discuss accessible records but cannot casually erase logs or damage ship systems.

---

## 4. Auxiliary Areas and Boundaries

These areas make the ship believable but need not receive full visual scenes in the first version.

### 4.1 Engine Room — `engine_room`

A machinery space containing propulsion and generator equipment. It is noisy, potentially hazardous, and normally requires an escort. It is **not** the wet-lab sampling apparatus location. Avoid confusing the research equipment fault with ship propulsion failure.

**MVP treatment:** Background doorway or brief supervised scene; no essential clue unless specifically added to the Evidence Bible.

### 4.2 Equipment Storage — `equipment_storage`

Secure storage for expedition gear, protective clothing, crates, hoses, and sample-handling equipment. Connects the lower corridor to the exterior aft working deck.

**MVP treatment:** Optional exploration hotspot and plausible transition to the outside.

### 4.3 Exterior Aft Working Deck — `aft_work_deck`

An exposed working area with rails, deck equipment, sea views, and storm ambience. This is a research working deck, not a recreational sun deck.

**MVP treatment:** Optional atmospheric conversation location. Weather or captain's safety orders can temporarily block access. The player cannot jump into the ocean, launch a tender, or use equipment to escape.

### 4.4 Corridors and stairways

`main_corridor`, `lower_corridor`, `upper_stairs`, and `lower_stairs` exist primarily to enforce sensible movement. They may be shown on a 2D ship map without separate art assets.

**Route consistency:** Room-to-room travel time can be abstracted, but not used to imply impossible instant movement. If later clues depend on precise traversal times, measure and fix them in a shared route table before writing alibis.

### 4.5 Areas outside player scope

Spaces such as ballast tanks, bilges, fuel systems, inaccessible service ducts, and the open sea exist in the fiction but are **not** explorable in the MVP. They cannot suddenly become secret shortcuts, hiding places, or new crime scenes through NPC improvisation.

---

## 5. Access, Permissions, and State Changes

### 5.1 General access model

Access is determined by **room ownership + current game phase + authorization**. Familiarity or high NPC trust alone does not grant authority to search a cabin or operate dangerous equipment.

| Area | Before death | After death, early investigation | Later authorized investigation |
|---|---|---|---|
| Mess hall, main corridors | Open | Open | Open |
| Dry laboratory | Audit-related access | Audit-related access; sensitive files still restricted | Specific additional records if granted/unlocked |
| Wet laboratory | Role-based routine access; Lucas lacks entry authorization | Secured unexplained-death scene after initial response | Supervised inspection only |
| Bridge | Request entry | Contact/briefings with Sarah | Authorized review of relevant records |
| Medical bay | Speak with Olivia | Speak with Olivia; private records restricted | Particular findings discussed when supported and unlocked |
| Engineering workshop | Limited/escorted | Limited/escorted | Relevant maintenance records as investigation permits |
| Editing room | Speak with Lucas | Speak with Lucas | Specific footage may be shared through Lucas/authorized preservation |
| Private cabins | Own cabin only by default | Others restricted | Only specified cabins with consent or appropriate authorization |
| Exterior aft deck | Conditions permitting | May be closed by storm | Opens only when safe and authorized |

### 5.2 Suggested state variables

These are **implementation suggestions**, not narrative canon. Prefer explicit state flags over asking an LLM to guess whether an area is open.

```yaml
world_state:
  phase: pre_murder  # pre_murder | early_investigation | later_investigation
  weather: worsening  # fair | worsening | severe
  wet_lab_secured: false
  wet_lab_inspection_authorized: false
  private_cabin_search_authorized: []
  bridge_record_review_authorized: false
  engineering_record_review_authorized: false
  selected_media_access_granted: false
```

A separate investigation/evidence state should govern revelations such as:

```yaml
investigation_state:
  thomas_motive_investigated: false
  daniel_motive_investigated: false
  medical_reconstruction_available: false
  medical_reconstruction_completed: false
```

The motive-investigation flags track progress only; they are not mandatory prerequisites for `medical_reconstruction_available`. Reconstruction availability depends on the necessary evidence and analysis, regardless of the order in which they are obtained.

**Important:** The World Bible defines *where* the reconstruction could be discussed (medical bay) and which systems physically exist. The **Evidence Bible and narrative logic define exactly when** the player can establish that the malfunction did not kill Elena. Do not disclose this as ambient room description or an automatic medical-bay interaction.

### 5.3 Authorization rules

1. **The player is an auditor, not a detective with unlimited search powers.**
2. **Sarah controls operational and safety access** aboard the ship.
3. **Personal and medical records are not public property** even during an investigation.
4. **Physical examination and information access are different:** entering the wet lab does not automatically unlock every clue there.
5. **Locked does not imply a puzzle solution:** avoid inventing keycards, PINs, or hidden passages unless explicitly designed.
6. **Restricted paths remain physically real:** a closed door may become usable after an approved state transition, without changing the ship's architecture.

---

## 6. Objects and Interaction Design

### 6.1 Interaction categories

| Type | Meaning | Example |
|---|---|---|
| **Ambient** | Adds atmosphere, no factual consequence | Coffee mug, warning poster |
| **Inspectable** | Provides stable descriptive information | Workbench, navigation display |
| **Evidence-bearing** | Can reveal a predefined clue | Maintenance terminal, selected media file |
| **Access gate** | Controls entry or permissions | Secured wet-lab door, cabin door |
| **Conversation anchor** | Gives a natural topic for questioning | M-17 analysis terminal, equipment fault board |
| **Safety-restricted** | Cannot be freely operated | Bridge controls, sampling apparatus, engines |

### 6.2 Interaction boundaries

- The player may **look, inspect, read, ask about, and compare** valid objects when access allows it.
- The player cannot fabricate evidence, permanently damage critical ship systems, or delete canonical records through unrestricted text commands.
- Objects cannot generate new crucial facts on demand. Evidence-bearing interactions use authored clue definitions.
- A character's response may refer to an object only if the object exists and the character could know about it.
- Decorative detail may be varied by an LLM, but it must not introduce new doors, new official documents, or new causes of death.

### 6.3 Evidence Bible interface

The World Bible supplies stable **location IDs** and **object IDs**. The Evidence Bible will reference these IDs rather than re-creating the room layout.

```yaml
# Illustrative reference only — NOT a completed evidence entry.
id: apparatus_fault_record
location_id: engineering_workshop
object_id: engineering_maintenance_terminal
# The Evidence Bible defines content, prerequisite flags,
# player-facing wording, and what the clue establishes.
```

### 6.4 Stable IDs and naming rules

- Keep `snake_case` IDs stable once referenced in code or other documents.
- Display names can be refined without changing IDs.
- Define each room and primary object in **one** canonical place, then reference IDs elsewhere.
- Changing a room connection or object location requires a coordinated update to the World Bible, Evidence Bible, and any dependent character alibis.

---

## 7. Atmosphere and Environmental Rules

### 7.1 Visual direction

- **Materials:** Metal bulkheads, anti-slip floors, utilitarian doors, sealed cabinets, bolted furniture.
- **Palette:** Muted gray and blue functional interiors with warmer light in living spaces.
- **Technology:** Contemporary research instruments, ordinary workstations, wired systems, and ship communications; no holographic AI controls or implausible supercomputers.
- **Condition:** Well maintained but visibly used; cables, labels, protective gear, handwritten notes, and occasional clutter.
- **Scale:** Tight corridors and small rooms help the player feel confined without making traversal frustrating.

### 7.2 Audio direction

- Constant low engine, generator, ventilation, or hull noise (exact running state depends on ship operation).
- Changing rain, wind, and waves near exterior spaces and windows.
- Distinct spaces: pump hum in wet lab, keyboard/fan noise in dry lab, tools in workshop, radio bursts on bridge.
- Character voices should remain audible; ambient audio should support tension rather than drown out dialogue.

**Fixed 23:10 sound event:** Both lab doors are closed. The resumed weekly verification task causes pump vibration; the worn support catch slips and the service cover drops with a brief metallic clunk. Tight door closure and ordinary ship noise prevent anyone elsewhere from hearing it. This is not perfect soundproofing: final positions, distances, microphones, and earlier argument/strike audibility must be checked. The controller has no cover-position sensor and generates no alert for the drop; its log records the resumed cycle, not the unsensed mechanical impact. The body is outside the cover's sweep and is not struck by the later closure.

### 7.3 Weather, sea, and visibility

The storm should worsen the feeling of isolation and plausibly delay assistance, but weather must follow a **fixed state progression**, not change with each generated description.

- **Opening and murder night:** Conditions deteriorate into a heavy gale with rough seas. Essential indoor activity remains possible; exterior research work is suspended.
- **Discovery at 06:50:** Heavy weather persists. The latest received offshore marine forecast predicts no meaningful easing for **at least through Thursday evening**. This is a forecast-based minimum outlook, not a promise that assistance arrives then.
- **Initial investigation:** Keep the weather state severe throughout that forecast period; do not introduce a convenient calm interval. After that period, any improvement or arrival of investigators belongs to the ending design.

**Forecast source:** Sarah receives marine weather forecasts/outlooks through the functioning communications system and reads them on `bridge_weather_display`. The ship's radar supports immediate navigation/observations; it does not itself provide the outlook through Thursday evening.

**Isolation and operation:** In this fictional incident, offshore distance and heavy weather prevent a safe boarding/transfer window for investigators, and Sarah cannot promise a prompt safe return to port. Shore authorities remain reachable for reporting and coordination. This is a delay in physical attendance, not a universal claim that emergency rescue is impossible in every storm. The vessel remains operational at reduced speed as defined in §3.1.

An NPC cannot claim perfect calm seas while the game's active weather state is severe. Storm effects also cannot erase important records unless the Story Bible and Evidence Bible specifically establish that event.

### 7.4 Communications and outside world

- Satellite/radio communications are **limited but functional enough** for Sarah to notify authorities.
- No outside investigator becomes an additional in-person NPC during the main investigation.
- A message from shore may be represented as an off-screen report or system message if explicitly scripted.
- The player cannot summon a helicopter or call an unlimited cast of outside experts to solve the case.

### 7.5 Research operations

The basic research process is fixed in Story §2.2: controlled sodium-hydroxide addition to seawater, untreated comparison samples, and tests of chemical stability and particle formation. Full ship-operating procedures remain **TBD**. The sampling/filtration station, mass-based sample check, project-required weekly verification, pending-task retry at 23:10 after Daniel restores automatic mode, and worn cover support are fixed in Story §5.2; the murder day is not the normal weekly test day. Detailed values and artifact wording remain open. Visual artists and LLM prompts must follow the established process rather than invent breakthroughs or experiments. Only Maya can explain the full science after Elena's death; generic room text and other NPCs provide plain-language observations or role-specific explanations, not omniscient research lectures.

---

## 8. NPC Presence and World Consistency

### 8.1 Natural character locations

These are **defaults for encounter design**, not alibis and not guaranteed positions at specific times.

| Character | Typical location(s) | Notes |
|---|---|---|
| Sarah Morgan | `bridge` | May meet player in mess hall or secure the wet lab after discovery |
| Daniel Reyes | `engineering_workshop` | May visit wet lab for maintenance when scripted |
| Maya Chen | `dry_lab` | May visit mess hall or other areas when supported by game state |
| Thomas Blake | `mess_hall`, `crew_quarters` | Exact workspace/cabin use TBD |
| Olivia Hart | `medical_bay` | May attend incident locations when required |
| Lucas Weber | `editing_room`, `mess_hall` | Can record in permitted spaces at specified times |
| Elena Fischer | `dry_lab`, `wet_lab` before death | Opening warning occurs in dry lab; murder occurs in wet lab |

### 8.2 Movement and knowledge boundaries

**Navigation/weather knowledge boundary:** Only Sarah initially knows the detailed route, coordinates, operating/navigation status, received forecast, and outlook through Thursday evening. These author-facing world facts are not shared NPC knowledge. Other characters may describe directly observable rough seas, wind, rain, ship motion, or communications they personally experienced; when asked for detailed position, forecast duration, or expected assistance, they refer the player to the captain. They may repeat a specific detail only after explicitly receiving it in play, attributing it to Sarah or the actual source. Being aboard or viewing generic room scenery does not automatically grant access to bridge information.


- A character does not automatically know what happened in another room.
- Hearing a noise, seeing someone in a corridor, and observing an event directly are **different evidence types**.
- Doorways, corridors, and camera coverage must support any claimed observation.
- No NPC can appear at a location inconsistent with a fixed Story Bible event or a confirmed alibi.
- A conversational model can **lie about** location, but the underlying actual world position stays fixed.
- Player navigation and NPC schedules are controlled by the game engine, not independently invented by LLM outputs.

### 8.3 Important observation constraint

The wet lab has a corridor door **and** an internal door to the dry lab. This complicates claims such as “anyone entering the wet lab must have appeared on the corridor camera.” Avoid such absolute statements until the team finalizes camera position and door-access logs. A partial recording may place Maya near the area without being an omniscient proof of the murder.

---

## 9. Minimum Viable World (MVP)

The first playable version should support these **eight core rooms**:

1. `bridge`
2. `wet_lab`
3. `dry_lab`
4. `mess_hall`
5. `medical_bay`
6. `crew_quarters` (with a few accessible sub-cabins)
7. `editing_room`
8. `engineering_workshop`

**Implement first:** A 2D ship map or location selection UI, a visual for each core room, a set of inspection hotspots, NPC conversations, permission-aware navigation, and a journal/evidence inventory.

**Can be simplified or postponed:** Detailed engine room, full exterior deck, individual art for all eight cabins, realistic navigation simulators, free-roaming NPC animation, and complex equipment controls.

**Scope rule:** An unimplemented area should not contain mandatory evidence. If the Evidence Bible relies on it, bring that area into the MVP or move the clue through an agreed narrative revision.

---

## 10. Implementation Guidance

### 10.1 Suggested structured data

The Markdown document is for people. Use a separate machine-readable file (e.g. `data/locations.yaml`) to store location IDs, labels, direct connections, baseline access rules, and object IDs.

```yaml
locations:
  wet_lab:
    display_name: Wet Laboratory
    deck: 2
    connects_to:
      - main_corridor
      - dry_lab
    access_rule: requires_authorization_after_discovery
    objects:
      - wet_lab_sampling_apparatus
      - wet_lab_viewing_panel
      - wet_lab_calibration_station
      - wet_lab_sample_bench
      - wet_lab_treatment_unit
      - wet_lab_workstation
      - wet_lab_storage_cabinet

  dry_lab:
    display_name: Dry Laboratory
    deck: 2
    connects_to:
      - main_corridor
      - wet_lab
    access_rule: audit_access
    objects:
      - dry_lab_analysis_terminal
      - dry_lab_viewing_panel
      - dry_lab_experiment_index
      - dry_lab_shared_workstation
      - dry_lab_document_shelf
```

This snippet is illustrative; do not maintain two independent sources of truth by hand indefinitely. Choose one authoritative structured representation once implementation begins, and keep the Markdown synchronized through review or generation.

### 10.2 What to supply to an LLM

For each exploration request, give the model only:

1. The current room's approved description and object list.
2. Allowed adjacent destinations and current access permissions.
3. The player's current investigation state and known discoveries.
4. Relevant NPC presence, knowledge, and conversation context.
5. Clear boundaries: no invented rooms, witnesses, evidence, hidden passages, or ship functions.

**Do not paste the entire World Bible plus full Story Bible into every NPC prompt.** That wastes context and risks revealing facts a character should not know.

### 10.3 Example interaction

**Player:** “I go from the dry laboratory to the wet laboratory and inspect the sampling apparatus.”

**Game-engine checks:**

- `dry_lab` is connected to `wet_lab`.
- The internal door is accessible in the current world state.
- Wet-lab inspection is permitted at this stage.
- `wet_lab_sampling_apparatus` is a defined object.

**If authorized:** Present a grounded inspection description and any evidence defined as discoverable in the Evidence Bible.

**If not authorized:** Explain the restriction through UI or an in-world response, without inventing another route or letting the LLM overrule the lock.

### 10.4 Validation checks for GitHub pull requests

- Every location referenced by dialogue, evidence, or code has a valid ID.
- All direct connections are reciprocal or intentionally one-way.
- Each object mentioned by an evidence entry exists in its assigned location.
- Restricted rooms cannot be entered solely by conversational persuasion.
- NPC positions are consistent with their time-dependent state.
- No outside or unnamed crew member is introduced as a new suspect/witness.
- The conclusion that machinery did not cause the death requires its supporting evidence and analysis, without imposing a mandatory Thomas-and-Daniel investigation order.

---

## 11. Open Decisions Before Production

**Settled context:** Pelagos Carbon operates the research project; Nereid Technologies is Maya’s private negotiation counterpart. The mission departed Galway on Sunday, the murder occurs Tuesday evening, and discovery is Wednesday morning in mid-December. Sarah’s received forecast indicates severe weather at least through Thursday evening, not a guaranteed assistance time. Exact calendar dates and detailed historical-incident locations are not outstanding world-design decisions. These author-facing facts do not expand NPC knowledge or grant access to private negotiations.

**Deferred by current scope:** General NPC locations, schedules, alibis, watch assignments, and noise/recording checks remain open. Fixed evening meetings also constrain future movements: Thomas and Elena converse in the mess hall at 21:10 on Tuesday, observed without hearing details by Lucas and Sarah; Elena confronts Daniel in his workshop at 22:00; Elena meets Maya in the wet lab at 22:35. How Olivia and Thomas learn of Daniel’s meeting remains open. The discovery response is another fixed sequence: Lucas at the wet-lab viewing panel at 06:50 and the fixed response order and relative intervals are established in Story §7.2. Preceding NPC locations/routes remain TBD; no further arrival-order decision is needed.

| Question | Why it matters | Proposed owner |
|---|---|---|
| Final drawing, dimensions, and walking distances | Connections are confirmed in §2.3; geometry can be refined later when alibis are addressed. | World / level design |
| Internal wet-to-dry lab door: lock and access-log behavior | Could change Maya's route and the value of surveillance footage | Narrative + world + evidence |
| Exact cameras, recording coverage, and blind spots | Prevents impossible video evidence | Evidence + world |
| Which cabins are individually explorable | Controls development scope and search permissions | Gameplay + evidence |
| Detailed apparatus/weapon visuals and surrounding scene geometry | Hardware, cover failure, and 2 kg reference mass are fixed; drawings must support reach/contact comparison and evaluation of a secondary fall. | Narrative + visual design + evidence |
| Alibis, door closure, and sound propagation | Preserve the unheard 23:10 clunk and no alert; separately settle earlier argument/strike audibility and microphone coverage. | Story + world + evidence |
| Discovery routes and examination blocking | Lucas discovers through the wet-lab panel at 06:50; Sarah opens the door after arrival. The response order is fixed in Story §7.2. Preceding locations/routes and clue-relevant examination movements remain TBD; preserve the witnesses and Lucas's confusion. | Story + world |
| Time-based NPC schedule after the murder | Prevents people appearing in impossible places | Character + gameplay |
| What authorizes wet-lab and private-cabin searches | Keeps player's auditor role believable | Story + gameplay |
| Credible operations of a vessel with only eight people | Small-cast premise needs a consistent degree of automation and watchkeeping | Story + world |
| Precise room/object artwork and asset style | Keeps generated assets visually consistent | Art + world |

Until these are agreed, avoid hard-coding decisions into NPC prompts or inventing them during playtests.

---

## 12. Related Documents and Editing Rules

- **`docs/story_bible.md` — Story Bible:** Objective events, motive, murderer, murder-night timeline, and narrative progression.
- **`docs/characters/*.md` — Character Bibles:** Individual character histories, knowledge, beliefs, secrets, voices, and behavior.
- **`docs/evidence_bible.md` — Evidence Bible:** Clues, exact placements, evidence meaning, prerequisites, and narrative unlocks.
- **`data/locations.yaml` — Locations data (planned):** Machine-readable navigation graph, objects, and baseline permissions.
- **`data/timeline.yaml` — Timeline data (planned):** Canonical events and movement constraints.

### Ownership and change process

1. **Change a room, connection, or object:** Update the World Bible and corresponding structured data.
2. **Change a clue's placement or unlock:** Update the Evidence Bible; confirm the location exists here.
3. **Change an actual character movement or murder event:** Update the Story Bible; check route feasibility here.
4. **Change a character's belief, disclosure, or dialogue:** Update that Character Bible; keep knowledge consistent with access and observation rules.
5. **Change revelation order:** Update narrative progression and evidence prerequisites, and only then adjust prompts or UI.

**Guiding principle:** *The Story Bible defines what happened. Character Bibles define perspectives. The World Bible defines what physically exists. The Evidence Bible defines what the player can establish. The game engine enforces the rules; the LLMs provide natural expression.*
