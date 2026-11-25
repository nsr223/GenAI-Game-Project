# Task: visual identities for 8 rooms and 6 people

## Goal and why
Earlier images looked alike: same lamp, camera, pose and gaze. A player should recognize every room from a thumbnail and every person from a silhouette, and feel a different atmosphere in each, while one hand has drawn them all. Write one identity per room and person for an illustrator.

## Output
Only the JSON required by the schema, all 14 ids exactly once. Choose the closest value for each axis. `description`: 25–40 words an illustrator can draw from; concrete shapes, light, objects and, for people, build, face, hair, clothing and gesture. No earlier work, files or tools are needed: answer from this text alone.

## Context
*Beneath the Surface* is a point-and-click murder mystery aboard a modern working research ship, the RV Meridian, in a North Atlantic winter gale, on the grey morning after a death. Art style: ink and wash. Maintained but used; bolted furniture; contemporary equipment; living spaces warm, technical rooms cooler. No body, weapon, readable text or science fiction. The player reads rooms as full-screen scenes and people as portraits beside dialogue.

Rooms (id: what it is)
- bridge: compact; navigation and radar screens, weather display, log station, radio, noticeboard, windows over the sea
- wet_lab: seawater-processing lab; anti-slip floor, steel benches, water lines, pumps, sample containers, sampling apparatus; humid, noisy
- dry_lab: quiet, climate-controlled data workspace; computers, monitor wall, scientific notes
- mess_hall: dining and small galley; bolted table, coffee, refrigerator, noticeboard, personal mugs; warmer, ordinary clutter
- medical_bay: compact infirmary; examination bed, secured cabinets, diagnostic workstation, report desk
- crew_quarters: short passage with eight compact cabins
- editing_room: former survey office turned media workspace; laptop, monitors, cameras, headphones, charging gear, pinned shot lists
- engineering_workshop: spare parts, tools, maintenance terminal, diagrams, test equipment; loud, utilitarian

People (id: role; manner)
- thomas_blake: investor representative; articulate, persuasive, status-aware, impatient; polished and personable
- sarah_morgan: captain; controlled, direct, protective, disciplined; speaks carefully, rarely raises her voice
- maya_chen: research scientist; brilliant, observant, warm in public, ambitious; approachable, helpful, exhausted but composed
- daniel_reyes: chief engineer; competent, blunt, pragmatic, proud, exhausted; easier with machines than feelings, often grease-stained
- olivia_hart: medic; empathetic, analytical, discreet, reserved; soft-spoken, attentive to pauses
- lucas_weber: documentary filmmaker; curious, quick-witted, personable, restless; strikes up conversations

The sources give no physical appearance. Nobody may look guilty or innocent.

## What the sources do say (use at least one per person; never their private secrets)
- thomas_blake: treats every crisis as a communications problem; talks to strangers as if they might invest; sees practical consequences quickly; wants his name on something world-changing
- sarah_morgan: the only person who can give orders aboard; listens before she answers; calm that is mistaken for indifference; growing more tired; proud of bringing crews home
- maya_chen: was mentored by the dead lead scientist and mourns her; explains clearly and patiently; wants to be seen as a scientist in her own right
- daniel_reyes: has been with the apparatus since its first trials; explains machines with everyday comparisons; sarcastic with people who ask without understanding
- olivia_hart: chose ships for practical care in a small team; notices pauses; dislikes speculation; firm about what she does not know
- lucas_weber: remembers gestures and framing better than facts; tests people with innocent questions; quick, ironic, wants his work to matter

## Used up: an earlier round produced these for almost everyone. Use none of them
Rooms: teal hoses; a view from near the floor; a frontal grid of violet or blue monitors; a round or oval table; mugs standing on a table; pale green or an empty pale floor; light from an ajar door; two ranks of four doors; a view past a chair; coiled headphones; a caged work light; tall parts bins; a band of windows over a dark console.
People: silver hair, tapering shoulders, blazer, pocket square or open palm (Thomas); hands behind the back, cropped hair, gaze past the viewer (Sarah); fleece, teal, tired eyes, notebook or mug (Maya); wiping hands, stocky, stubble, coveralls (Daniel); bob, auburn, sage, scrubs, folded hands, finger to cheek (Olivia); lanky, curls, blond, red accent (Lucas).

## Personality rules
- Give every person one visible habit that follows from a source line, and one small contradiction that makes them memorable.
- Give every room one trace of who uses it, and one quality no other room aboard has.
- Everything movable is secured for a gale: racked, latched, strapped or railed.
- Believable crew and passengers of a working ship: varied ages, builds and origins; no costume, no caricature.
- In `feeling`, name the habit or trace and the contradiction in one sentence.

## How to work
Think step by step. 1. Draft all 14 in a few words each. 2. Compare every pair of rooms and every pair of people and name the pairs that share the most axes or the same first impression. 3. Revise the weaker one of each such pair to be bolder and more distinct while still true to its role. 4. Repeat the comparison once. Write the draft, the named pairs and what you changed in `work`, then the final identities.
