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
