> Worker report as delivered; links to local files removed.

# Proposed identity sheets for team review

Open the room sheet · Open the people sheet · 160 px room studies · Black silhouettes · Enlarged faces

Four images generated with built-in ImageGen, two versions of each sheet. Both v2 sheets were reopened and checked against the individual crops. No image reference was supplied. The rooms read first through eight different large shapes. The people read first through the direction of each torso and the spaces around the hands. The rooms retain more small fittings, hard edges and ceiling lights than the people sheet suggests.

## Room studies

The values are mean linear sRGB relative luminance, on a scale of 0 to 1. Each measurement uses the same 418 × 422 interior pixels used for its 160 px thumbnail, before resizing, excluding the paper gutter. The weights after sRGB linearization are 0.2126 red, 0.7152 green and 0.0722 blue.

| Room | What identifies the 160 px study | What is missing or weak | Mean | Target |
|---|---|---|---:|---|
| Bridge | Raked mullions, rough grey sea and console arc lead into the stairwell. | Sea horizon is almost level. The ship's heel is easier to read in the window frame than on the water. | 0.197 | 0.10–0.22 |
| Wet lab | Transparent braided hoses, orange pump guards and green-lit tanks crowd the space under and over the bench. | Condensation and thumb wear are indistinct. The general calibration setup blends into the workbench. | 0.217 | 0.10–0.22 |
| Dry lab | A long uninterrupted blue tide curve floats above a graphite counter and repeated blue tabs. | The wall reads as grey panelling. Reflections and ceiling light compete with the quieter felt finish. | 0.211 | 0.10–0.22 |
| Mess hall | A honey-coloured table dominates the foreground, with a row of hanging mugs, snapshots and a warm wall lamp behind it. | A loose fruit bowl sits on the table. Mug chips and spring clips are hard to resolve. | **0.333** | **0.20–0.32, high** |
| Medical bay | A crooked examination lamp bends towards a mint berth and white pillow. The view down from the desk also picks up its parallel pen. | The whole bed is quite bright, and the pen appears loose. | 0.372 | 0.25–0.40 |
| Crew quarters | The return hatch frames four handles and door leaves per side. Low amber pools shrink towards a blank end wall. | The passage is regular and symmetrical. The recesses make weak sawtooth shadows, and the picture appears uncovered. | 0.297 | 0.20–0.32 |
| Editing room | Violet ear cups and the strapped camera flank a laptop under a small amber pool. | The pinned sheets resemble landscape photographs more than shot sketches. | 0.146 | 0.10–0.22, darkest |
| Workshop | A large spoked wheel in a fixed cradle breaks across the parts drawers. A white strip catches the rim. | The rim highlight survives reduction. Wear on one spoke is much harder to pick out. | 0.173 | 0.10–0.22 |

## People studies

| Person | What carries the identity | What is missing or weak |
|---|---|---|
| Thomas Blake | Full cheek, swept side part, knit vest, backward tilt and frayed mustard cuff. Two fingertips rise as he counts. | His hands overlap his vest in silhouette, reducing the count to a small projection. |
| Sarah Morgan | Long narrow profile, lifted chin, trailing braid and long navy shirt. One thumb draws the side seam out. | The listening ear is visible, though the head reads as looking up. Her lowered hand ends in the waist crop. |
| Maya Chen | Rounded cheeks below a blunt fringe, low ponytail, rust henley and two lowered fingers meeting over an imaginary diagram. | Both fingers show the endpoint. Their meeting conveys less of the tracing motion. |
| Daniel Reyes | Lean curved back, heavy brow, long clean jaw, worn vest and two careful hands around a coupling. | The vest shows general wear more clearly than grease. |
| Olivia Hart | Round face, close twists, plum shoulders, loose crossed forearms and a steady level gaze. | The arms merge into the torso when blacked out. The seat itself is inferred. |
| Lucas Weber | Slight build, turned back, crooked smile and a raised finger frame with open paper below the forearm. | The cuff repair is subtle. The raised hand and twist carry most of the recognition. |

## Pass/fail observations

| Check | Result | Observation |
|---|---|---|
| 1. Identities present | Pass at concept scale | All fourteen have a visible identifying form. The two tables record the missing details individually. |
| 2. Viewpoint, pose and light repetition | Fail for rooms; pass for people | The room poses are inapplicable. Several technical rooms use a similar oblique interior view. Ceiling fixtures above the benches and consoles recur on the bridge and in both labs. The people have six different gestures. Shared light families top out at two each, with light from below on Thomas and Daniel, a cool edge on Sarah and Lucas, overhead light on Maya and side light on Olivia. |
| 3. Rooms at 160 px | Pass | The closest pair is the wet and dry labs because their long benches terminate at similar doors. Under-bench orange pumps and the horizontal blue display separate them. |
| 4. Black silhouettes | Pass, six distinguishable by inspection | Thomas and Olivia are closest, with broad shoulders and hands mostly inside the torso. His tilted head and projecting fingertips separate him from her level head and even lower contour. |
| 5. Enlarged faces | Pass, six distinct | Maya and Lucas are closest through their straight dark fringes and age read. Her rounded cheeks and small mouth differ from his tapered jaw, longer nose and crooked smile. |
| 6. Neutrality and clue control | Pass | Equipment looks routine, tide curves repeat evenly, and the wet lab gives its pumps and tanks equal attention. No isolated mass, disturbed patch, hidden object, weapon, body or accusatory glance stood out. |
| 7. Exits and eight cabins | Pass | Four cabin doors per wall and a foreground return coaming are visible. Elsewhere the bridge shows its descending stair, both labs have doors, the mess and infirmary open into passages, editing shows a door and lever, and the workshop opens onto the lower corridor. |
| 8. Securing, technology, text and occupants | Fail for securing | Straps, pedestals, rails and latched cases read well. Loose fruit, desk pen and small desk devices lack visible restraints. Equipment is contemporary. No room contains a person or clearly readable text. |
| 9. Luminance | Fail, seven of eight within range | Editing is darkest. Mess exceeds the upper limit by 0.013. All selected-source values appear above. |
| 10. Shared drawing hand | Pass for medium, weaker for detail level | Both sheets show broken fine contours, pale paper and pooling watercolour. The rooms are denser, particularly their fixtures and cabinet hardware. |
| 11. Prompt and image traceability | Pass | All four saved prompt texts were checked against their respective generator inputs. Each sibling WebP is a resized or compressed encoding of its full-size PNG. Prompts and versions |

## Three weakest identities and proposed fixes

1. **Crew quarters.** Keep all eight leaves and the return coaming. Move alternate door frames deeper into their walls so the low amber lamps cast a visible zigzag. Put the photograph behind an opaque cover.
2. **Mess hall.** Clear the fruit bowl, use visible spring clips on the mug handles and reserve the brightest amber for the lamp-facing edge of the table. Bring the tabletop's broad middle wash down until the panel mean approaches 0.28.
3. **Dry lab.** Show the display and worktop nearly in elevation. Give the felt a flat, absorbent grey wash and let the blue screen cast the only strong light. This also separates its geometry from the wet lab at 160 px.
