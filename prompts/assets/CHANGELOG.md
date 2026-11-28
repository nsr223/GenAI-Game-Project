# Asset prompt changelog

## Ink-and-wash style lock

The first option study is in [the original prompt log](style/CHANGELOG.md). Production v1 starts a fresh series against the approved secured-ship brief. The first paragraph of all six production prompts is the shared style block v2. Each row links the exact generator input and original output.

| Asset | Version | Drawing reference | Reason from the visible image | Selection |
| --- | --- | --- | --- | --- |
| Mess hall | [v1](rooms/mess_hall/v1.md) | [Option v1](style/ink-wash/mess_hall/v1.webp) | The option shows casters, loose mugs, similarly mottled wood and steel, and bright fittings across the frame. The option screen also shows a kink in the extended tabletop. Establish the secured, dim production baseline. | [PNG](rooms/mess_hall/v1.webp). The rail, fixed base and straight table read clearly. Slanting lines in the exit pane suggest exterior rain. |
| Thomas Blake | [v1](characters/thomas_blake/v1.md) | [Option v1](style/ink-wash/thomas_blake/v1.webp) | The source cuts sleeves and torso above the waist. Retain the face and pull back to the belt so the panel can occlude the waist naturally. | [Final source](characters/thomas_blake/v1.webp). Open jacket, left-side light and eyes turned toward the auditor survive the smaller crop. |
| Bridge | [v1](rooms/bridge/v1.md) | [Production mess hall v1](rooms/mess_hall/v1.webp) | The warm wall and secured worktop read together in the mess. Test the same light and pen marks on five separate instruments/fixtures and a stair door. | [PNG](rooms/bridge/v1.webp). The log terminal is small but separate. The door inset repeats the slanted glass marks from the sea windows. |
| Sarah Morgan | [v1](characters/sarah_morgan/v1.md) | [Production Thomas v1](characters/thomas_blake/v1.webp) | Thomas's open lapels and wavy hair establish a narrow outline. Test the same scale and lighting on a sturdier captain with a high zipped collar and cropped curls. | [Final source](characters/sarah_morgan/v1.webp). Broad shoulders, raised collar and warm cheek read at dialogue size. |
| Mess hall | [v2](rooms/mess_hall/v2.md) | [Production v1](rooms/mess_hall/v1.webp) | Rain-like diagonal lines in the far-right pane suggest an exterior route. Change only the view through that pane to the main corridor wall and rail. | [Final source](rooms/mess_hall/v2.webp). Horizontal rail visible. The gale remains at the sink window. |
| Bridge | [v2](rooms/bridge/v2.md) | [Production v1](rooms/bridge/v1.webp) | The stair door's glazed inset carries the same diagonal marks as the bridge windows. Change only the view through the inset to an interior landing wall and rail. | [Final source](rooms/bridge/v2.webp). The door leads inboard. Weather glass and console spacing are intact. |

Six ImageGen outputs. The four runtime WebPs are resized encodings of the selected PNGs. Browser screenshots and inspection sheets are proof exports. See the [acceptance observations](../../docs/prompt-log/game-visuals/evidence/07-build-report.md).

## Review after the run (not accepted)

| Asset | Failure seen | Cause in the prompt | Next change |
|---|---|---|---|
| Mess hall v2 | Cold and empty although living spaces are warm (World §7.1); mean luminance 0.09 against 0.31 in the option the team chose | The brief asked for "clearly lower" luminance and darker corners | Warm, lighter living rooms with a brightness range per room |
| Bridge v2 | Same lamp, door and viewpoint as the mess hall | The mess hall was the reference image; lamp left, door far right and quiet left quarter were repeated in words | Own viewpoint, light and dominant form; no finished room as reference |
| Sarah Morgan v1 | Same framing, similar pose and gaze as Thomas | Thomas's portrait was the reference; the pose was hardly described | Own silhouette, posture, hands and gaze |
| Style block v2 | Every room and person inherits one lamp and one lens | Camera and light were part of the repeated block | Block reduced to line, paper, wash and finish |

## Proposed identity sheets

Four built-in ImageGen outputs drawn from words. The four inputs share a 34-word first paragraph about marks and materials. Both v2 sheets are selected for team review. [Check results](../../docs/prompt-log/game-visuals/evidence/09-build-report.md).

| Sheet and input | Output | Visible flaw that prompted this version | Likely cause | Change |
|---|---|---|---|---|
| [People v1](concepts/people/v1.md) | [WebP](concepts/people/v1.webp) | Earlier Thomas and Sarah shared framing, posture and gaze. | One portrait supplied the visual reference for the next. | Draw six separate gestures and face structures on blank paper from the selected draft. |
| [Rooms v1](concepts/rooms/v1.md) | [WebP](concepts/rooms/v1.webp) | Earlier bridge and mess repeated a lamp, viewpoint and exit placement. | The previous room and common lighting directions anchored the composition. | Give each room its own viewpoint, depth, silhouette, local light and value. |
| [Rooms v2](concepts/rooms/v2.md) | [WebP](concepts/rooms/v2.webp) | Quarters, editing and workshop measured 0.185, 0.050 and 0.094. Dense surface rendering and repeated ceiling fixtures competed with the forms. | Numeric targets gave less guidance than words such as “dark indigo” and “dense gunmetal.” | Specify the area and colour of lighter surfaces, simplify marks, strengthen the editing desk angle and retain four cabin doors per side. Mess overshot to 0.333. |
| [People v2](concepts/people/v2.md) | [WebP](concepts/people/v2.webp) | Daniel's back met the sheet edge. Warm modelling across the six faces obscured some of the intended light directions. | The figures occupied most of their cells and light instructions seldom said where shadow fell. | Request larger margins and draw the specific lit and shaded planes on each face. Daniel now fits, and Sarah's cool rim separates her from Thomas's warmer lower face. |

### Review after the run (identities accepted as a basis for comments, not as final looks)

| Sheet | Failure seen | Cause | Next change |
|---|---|---|---|
| Rooms: workshop | A spoked flywheel reads as a steam engine; canon equipment is contemporary (World §7.1) | The draft says "spoked pump flywheel" | A modern pump or generator part with the same large, readable shape |
| Rooms: bridge | A row of about nine consoles and three chairs; canon says compact | The draft names a viewpoint but no size | Two stations, close walls |
| Rooms: dry lab | A neat sine wave on one display; monitors, terminals and shelf of World 3.3 missing | "One long display with a thin tide trace" | Keep the stillness, use ordinary screens with uneven data, show the canon workstations |
| Rooms: all | Brown blotches on walls and metal again; canon says well maintained | Nothing in the prompt limits wear | State where wear may appear, and nowhere else |
| Rooms: crew quarters | Two regular rows of doors, although this default was banned in text | The eight-door check outweighed the staggered recesses | Recessed doors drawn explicitly, doors still all reachable |
| People: Thomas, Daniel | Light from below, which can look sinister | The prompts assigned light directions only to differ | No light from below on faces; nobody looks guilty |
| People: Sarah | Looks upward and away, reads as haughty rather than listening | "Turns one ear" drawn as a full profile | Three-quarter view, eyes near the player |
| People: Maya | Reads as very young for an accomplished scientist | The prompt gave no age | State an age for every person |

## Remaining dialogue sprites (prompts ready, images pending)

The dialogue panel still shows a silhouette for Maya, Daniel, Olivia and Lucas. These four prompts start from the accepted identity basis in [People v2](concepts/people/v2.md) and apply the fixes listed in the review above. The first paragraph is the same 34-word block as the identity sheets (line, paper, wash, finish; no camera or lamp). Each prompt gets only that person's crop of [People v2](concepts/people/v2.webp) as identity reference, never a finished portrait, so no pose or framing is inherited from Thomas or Sarah. Looks remain PROPOSED until the team signs off on the concept sheet.

| Asset | Version | Identity reference | Reason from the review | Selection |
| --- | --- | --- | --- | --- |
| Maya Chen | [v1](characters/maya_chen/v1.md) | Maya crop, People v2 | "Reads as very young": state an age (about 33) and add tiredness under the eyes. Keep her diagram-tracing hand as her own gesture, now aimed at the listener. Warm and patient; nothing in face or light suggests guilt. | Pending |
| Daniel Reyes | [v1](characters/daniel_reyes/v1.md) | Daniel crop, People v2 | "Light from below can look sinister": light now from screen-right and above. The steel pipe coupling is removed, because a compact metal object in his hands could read as a clue. His touch-habit becomes a thumb working at grease on his knuckles. | Pending |
| Olivia Hart | [v1](characters/olivia_hart/v1.md) | Olivia crop, People v2 | Keeps her accepted crossed-forearm posture and side light. Age stated (about 45). Stethoscope, medical symbols and red cross excluded (props rule; protected emblem). | Pending |
| Lucas Weber | [v1](characters/lucas_weber/v1.md) | Lucas crop, People v2 | Keeps the framing gesture, but the raised hand must stay inside the sprite margin. Age stated (about 27). No camera, so the gesture carries his job without a prop. | Pending |

Each of the four has its own silhouette against the two finished sprites: Thomas has an open V jacket and a straight stance, Sarah a closed high collar and level shoulders. Maya leans forward with one raised hand, Daniel rounds his shoulders over low hands, Olivia makes a horizontal arm oval, Lucas twists away with a high hand. Run-time target as for Thomas and Sarah: 480 × 525 WebP with true alpha in `frontend/static/art/characters/<id>.webp`.

### Pre-run review of the v1 sprite prompts → v2 (no images generated yet)

v1 was checked against the two accepted sprites and against known generator behaviour before spending any generations. Measured on the final Thomas and Sarah WebPs (480 × 525): hair top 2–4 px below the edge, waist crop at 518–524 px, head about 106–137 px wide (≈ 28 % of the width), figure spanning 77–89 % of the width.

| Asset | Version | Problem found in v1 | Cause in the prompt | Change in v2 |
| --- | --- | --- | --- | --- |
| All four | [Maya v2](characters/maya_chen/v2.md), [Daniel v2](characters/daniel_reyes/v2.md), [Olivia v2](characters/olivia_hart/v2.md), [Lucas v2](characters/lucas_weber/v2.md) | Would come out smaller than Thomas and Sarah in the same panel | "A small transparent margin on every side" with no scale; the finals fill the canvas | Scale stated in words that survive any canvas size: hair just below the top edge, head about a quarter of the width, shoulders across most of it. Square canvas, cropped to 480 × 525 afterwards. |
| All four | v2 | Risk of copying the sketchiness of the concept sheet | The concept sheet asked for "hardly any marks" and a few thin washes; v1 used it as the only reference | Take face, hair and colours from the crop but draw "a finished dialogue portrait: more resolved face and hands than the sketch". |
| All four | v2 | Long "No …" list at the end (12–14 items) | Image models often draw what a negative names; a long list also dilutes the prompt | Background stated positively ("empty transparent background"); a short "Exclude" list of only the items that matter for each person. |
| All four | v2 | One dense paragraph mixed identity, pose, light and framing | Hard to edit one aspect without touching the others, and hard to compare versions | Fixed order with labels: identity, Pose, Light, Framing, background. Later versions can change one line and log it. |
| Maya | v2 | "Warm and patient, no smile and no frown" asks for warmth and forbids its usual sign | Contradictory expression words | "A quiet, tired warmth around the eyes, lips relaxed": warmth without a smile that could read as smug. |
| Daniel | v2 | "Draw a new pose without the pipe coupling" still names the object | Mentioning the coupling invites it back | Asks for "empty hands"; tools and metal objects only in Exclude. |
| Lucas | v2 | The raised L-hand is the part most likely to be cut by the edge | Hand position given relative to the eye line, not the canvas | Hand beside the shoulder, "fingertips clear of the edge". |

## Music and sound (v1 and v2)

Generated locally with the open models the course recommends: **MusicGen** (`facebook/musicgen-small`, music) and **AudioLDM** (`cvssp/audioldm-s-full-v2`, ambience and effects), seed 1, on CPU. The scripts, both prompt specs and the measurement tool are in [`docs/prompt-log/audio/`](../../docs/prompt-log/audio/). Each generation has its own file in `music/<id>/vN.md` or `sfx/<id>/vN.md` with the exact prompt, settings and result. Selected files are in `frontend/static/audio/`, listed in its `audio.json`.

**How results were judged.** Nobody listened to v1 inside the game yet. Every clip was measured instead: loudness (RMS, peak), loudness spread over time, energy share per frequency band, spectral flatness (hiss-like near 1, tonal near 0), plus a spectrogram ([v1](../../docs/prompt-log/audio/img/01-spectrograms-v1.webp), [v2](../../docs/prompt-log/audio/img/02-spectrograms-v2.webp)). A clip was rejected when the numbers contradicted the World Bible audio direction (§7.2): constant low hums, audible but not fatiguing, dialogue stays audible. **Please listen and overrule.**

| Asset | Version | What the measurement showed | Cause in the prompt | Change | Selection |
| --- | --- | --- | --- | --- | --- |
| Title theme | [v1](music/title_theme/v1.md) | Tonal, sparse, no drums | — | — | Selected |
| Investigation loop | [v1](music/investigation_loop/v1.md) | Low, steady, quiet; fits under dialogue | — | — | Selected, made into a seamless loop |
| Accusation | [v1](music/accusation/v1.md) | Fast broadband ticking through the whole clip; abrupt cut at 28 s | "insistent", "deep timpani hits", 90 bpm | Slower, softer percussion, "restrained", "no fast percussion" | Rejected |
| Accusation | [v2](music/accusation/v2.md) | Smooth, low, no ticking | — | — | Selected |
| Ending | [v1](music/ending/v1.md) | Calm, tonal piano and strings | — | — | Selected |
| Storm (window) | [v1](sfx/storm_window/v1.md) | Steady rain and wind with gusts | — | — | Selected, base layer in every room |
| Ship hum | [v1](sfx/ship_hum/v1.md) | 99 % below 200 Hz, steady | — | — | Selected, base layer in every room |
| Wet lab | [v1](sfx/wet_lab/v1.md) | Flat hiss with whistling tones | Nothing said the hum should be low or gentle | "low steady", "gentle", "muffled"; negative "hiss, whine" | Rejected |
| Wet lab | [v2](sfx/wet_lab/v2.md) | Low pump hum with a regular stroke | — | — | Selected |
| Dry lab | [v1](sfx/dry_lab/v1.md) | Almost silent (-71 dBFS) | "Quiet" and "soft" taken literally | Steady fans, no "quiet"; negative "silence" | Rejected |
| Dry lab | [v2](sfx/dry_lab/v2.md) | Audible, but bright fan hiss | Fan noise is broadband by nature | 2.5 kHz low-pass in post instead of a third generation | Selected |
| Bridge | [v1](sfx/bridge/v1.md) | Radio static, crackle bursts, wind | — | — | Selected |
| Workshop | [v1](sfx/engineering_workshop/v1.md) | Dense grinding, 90 % above 1 kHz | "tools clanking" drew grinding/cutting noise | "steady low rumble … occasional metal clank"; negative "grinding" | Rejected |
| Workshop | [v2](sfx/engineering_workshop/v2.md) | Low rumble, regular clank | — | — | Selected, also used for the engine room |
| Mess hall | [v1](sfx/mess_hall/v1.md) | Rain texture with small clinks, quieter | — | — | Selected |
| Steel door | [v1](sfx/door_steel/v1.md) | Four door events in one clip | 5 s and "opening and closing" invite several events | "A single … closing", 3 s | Rejected |
| Steel door | [v2](sfx/door_steel/v2.md) | One heavy slam | — | Cut to 1.6 s | Selected |
| Footsteps | [v1](sfx/footsteps_metal/v1.md) | Even steps with metallic ring | — | Cut to 2.5 s | Selected |
| Page turn | [v1](sfx/page_turn/v1.md) | Two paper rustles | — | First rustle only, 1.0 s | Selected |

Nineteen generations, five rejected. Not yet made: voices (TTS) and a room layer for the medical bay, crew quarters and editing room (they play the base layers only).

## Music and sound, round 2 (28 Nov): new title theme, thinking hum, events and remaining rooms

Team feedback on round 1: everything kept except the title theme, which should be **more exciting**. New requests: a "Hmmm" while NPCs think, a sound when the accusation opens, and the remaining effects and room layers. Same tools and measurements as round 1 (spectrograms: [batch 2](../../docs/prompt-log/audio/img/03-spectrograms-batch2.webp), [locked hint v2](../../docs/prompt-log/audio/img/04-locked-hint-v2.webp), [hum takes](../../docs/prompt-log/audio/img/05-thinking-hum-takes.webp)), plus **Bark** (`suno/bark-small`) for the hum. All sounds are now **wired into the player UI** (`frontend/static/audio.js`), with a "Sound on/off" button.

| Asset | Version | What the measurement showed | Cause / reason | Change | Selection |
| --- | --- | --- | --- | --- | --- |
| Title theme | [v2](music/title_theme/v2.md) | Regular drum hits at ~120 bpm, denser after 17 s | v1 asked for "slow, sparse, no drums" | Driving strings, drums, brass, 120 bpm | **Selected**, replaces v1 |
| Title theme | [v3](music/title_theme/v3.md) | Wall of fast ticks, 9 dB louder | Same prompt, seed 2: checks whether v2 was luck | — | Rejected |
| Thinking hum | [v1](voice/thinking_hum/v1.md) | Six takes; two have a steady 1.5–2.9 s hum | Bark often breathes or trails off | Loop cut from the steady part | **Selected**: female_c, male_a |
| Accusation sting | [v1](music/accusation_sting/v1.md) | One hit and decay, unrelated burst at 5.85 s | — | Cut at 4.5 s | Selected |
| Evidence found | [v1](music/evidence_found/v1.md) | Three bell-like notes | — | First 1.9 s | Selected (not triggered yet, see below) |
| Locked hint | [v1](sfx/locked_hint/v1.md) | Silent | Too abstract for AudioLDM | Concrete source, negative "silence" | Rejected |
| Locked hint | [v2](sfx/locked_hint/v2.md) | Rolling rumble, not one knock | — | First 0.4 s as a thump | Selected (not triggered yet) |
| Medical bay | [v1](sfx/medical_bay/v1.md) | Hum under bright hiss | Same as dry lab v2 | 2 kHz low-pass | Selected |
| Editing room | [v1](sfx/editing_room/v1.md) | Hum with 4–6 kHz whine | — | 3 kHz low-pass | Selected |
| Crew quarters | [v1](sfx/crew_quarters/v1.md) | Rain ticks and creaks | — | — | Selected, also all cabins |
| Aft work deck | [v1](sfx/aft_work_deck/v1.md) | Wind and wave swells | — | Loudest room layer (outdoors) | Selected |
| Thunder | [v1](sfx/thunder/v1.md) | Rumble with cracks | — | — | Selected (not triggered yet) |
| Radio crackle | [v1](sfx/radio_crackle/v1.md) | Band-limited static | — | First 1.4 s | Selected (not triggered yet) |
| Hull groan | [v1](sfx/hull_groan/v1.md) | Low straining drone | No sharp clunk on purpose: could hint at the 23:10 cover fall | — | Selected (not triggered yet) |

**Considered and not made:** a spoken "Whodunit?" when the accusation opens. The thinking hum is already the one comic touch; the accusation is the climax of a real death, so it gets an orchestral sting instead. Easy to add later if the team wants it.

**Triggered automatically** (audio.js watches the UI): title → investigation music, room ambience, footsteps on room change, thinking hum, accusation sting and music, journal page turn, ending music. **Not triggered yet**, because the UI does not show these moments clearly: evidence found, locked hint, thunder, radio, hull groan. Call `window.gameAudio.play("evidence_found")` etc. where the frontend knows the event happened.

Sixteen new generations (title 2, hum 6, effects 8 + 1 retry), five rejected. Round 1 + 2: 37 generations, 10 rejected.
