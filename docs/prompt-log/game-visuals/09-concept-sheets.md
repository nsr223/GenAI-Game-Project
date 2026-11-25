# Task: draw two concept sheets from the selected identities

## Goal and why
The team will comment on looks from these sheets before any final art is made. Every room should be recognizable from a thumbnail and every person from a silhouette, each with its own atmosphere, while one hand has drawn them all. Earlier finals failed because one lamp, camera, pose and layout was repeated.

## Context
Read `AGENTS.md`, `docs/prompt-log/game-visuals/08-identities/selected-draft.md` (the content to draw), "Cause in the prompt" under entry 7 in `docs/prompt-log/game-visuals.md`, World Bible 3.1–3.8 and 7.1 (search the headings), and the objects and exits of each room in `data/locations.yaml`. This task is approved inside its scope: no plan approval needed.

## Build
1. **Constant block**, at most 45 words: line, paper, wash, finish of `course/style-options/ink-wash/`, with its visible paper white and clear line. No camera, lamp, layout, pose or fixed darkness in it.
2. **Rooms sheet:** one image, 4×2 colour studies with gaps, low detail, no text, in the order of the draft. Describe each study in its own words: viewpoint, depth shape, dominant form, light source and colour, accent, brightness.
3. **People sheet:** one image, six waist-up figures with clear gaps on plain paper, low detail, in the order of the draft. Describe build, face, hair, clothing, posture, hands, gaze, accent and own light separately for each.
4. **Crops** for judging: each study at 160 px wide, each figure as a solid black shape, each face enlarged.

Draw from words. If a reference is needed for the drawing hand, use only a crop of `course/style-options/ink-wash/` that shows line and wash on a plain surface, never a room, object or person. At most 2 versions per sheet; a second version fixes named flaws of the first.

## Constraints
- Prompts in `prompts/assets/concepts/<sheet>/vN.md` with each image beside it as `vN.webp` (at most 1600 px wide, under 400 KB); entries in `prompts/assets/CHANGELOG.md` (version, visible flaw, cause, change). Full-size images and crops in `course/identities/`. Edit nothing else and no final art. Leave everything uncommitted. At most 4 generated images; finish the people sheet first if the usage limit is near.
- Looks are PROPOSED. Nobody looks guilty or innocent.

## Pass/fail checks
1. Each study and figure shows its own identity from the draft: name for each what carries it, and what is missing.
2. No viewpoint, light position or pose is used by more than 2 rooms or 2 people.
3. Thumbnails: list for each what makes it recognizable without its name, and the two most confusable rooms.
4. Silhouettes: at least 5 of 6 distinguishable; name the two closest.
5. Faces: six different people; name the two closest, since models repeat faces in groups.
6. Nothing reads as a clue: no cleaned or disturbed spot, single odd reading, hidden object, suspicious glance, body or weapon. In the wet lab, equipment looks ordinary and the reference mass is not singled out.
7. Crew quarters show all eight cabin doors and the way back; other rooms show at least one exit.
8. Furniture bolted, movable things secured, contemporary equipment, no readable text, no extra person in rooms.
9. Mean luminance per study: living spaces (mess hall, crew quarters) 0.20–0.32, medical bay 0.25–0.40, others 0.10–0.22; the editing room is the darkest. Report each value even if outside.
10. All 14 look drawn by one hand: same line, paper and wash.
11. Saved prompts match their images word for word.

## Return
A table of the checks with what you observed, both sheets opened and described including flaws, the luminance values, the three weakest identities with a concrete fix each, and the number of generated images.
