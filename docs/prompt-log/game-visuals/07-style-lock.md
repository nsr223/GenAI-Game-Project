# Task: lock the ink-and-wash style of Beneath the Surface

## Goal and why
The team chose ink and wash. Turn the first attempt into a style that 8 rooms and 6 suspects can follow without drifting. It must also carry tension: the first room reads bright and tidy, while the story is a confined ship in a gale the morning after a death. Prove the style on a second room and a second person before anything is produced in bulk.

## Context
- Read `AGENTS.md`, `docs/summaries/visuals-audio.md`, World Bible sections 3.1, 3.4 and 7.1 (search the headings), and sections 1–2 of `docs/characters/sarah_morgan.md`. This task is approved: no plan approval needed inside its scope.
- Start from `course/style-options/ink-wash/` and `prompts/assets/style/ink-wash/`. Keep what works: fine carbon line, hatching, translucent wash, paper texture, clear objects, rain-streaked window.

## Known flaws of the first attempt (each is a required change)
1. The prompt asked for a coffee cart, so it is on wheels: make it a fixed counter with a raised edge. Canon furniture is bolted.
2. Loose dishes, plates and mugs: secure them in racks or rails, as on a ship in a gale.
3. Brown speckles on metal and even wood read as rust everywhere; canon says well maintained. Keep wear local and plausible.
4. The table top is bent: a plain rectangle in correct perspective.
5. Walls and table compete with the face. Dim grey storm morning outside, a few warm lamps inside, darker corners, one clear pool of light near the speaker.
6. Thomas looks pasted on: waist cut at the panel edge, light from the lamp side, soft contact shadow, gaze toward the player's side.

## Build
1. `style block v2`: one paragraph reused word for word in every prompt, plus a fixed camera rule (eye level, same lens feel) and light rule.
2. Final `mess_hall` and `thomas_blake`, made with the first versions as references.
3. Transfer test with the finished block: `bridge` (its 5 canon objects and one exit as separate clickable areas, no readable screens) and `sarah_morgan`, waist-up, transparent. If a transfer image drifts, improve the block, not only that image, and regenerate what it affects.
4. `docs/visual-style.md`, at most 150 lines: palette with roles, line, wash, light, camera, style block, image sizes and file names, how to prompt and check a room or a person, spoiler rules, and a table of proposed looks for all six suspects marked PROPOSED (the bibles give none). Vary age, build and features; let look follow role and manner; nobody looks guilty.
5. Two HTML screens at 1280×720, full-bleed art with a dialogue panel: Thomas in the mess hall, Sarah on the bridge.

## Constraints
At most 3 versions per image, one change per version, each with a reason from what is visible. Prompts in `prompts/assets/rooms/<id>/` and `prompts/assets/characters/<id>/` with one `prompts/assets/CHANGELOG.md`; every version image and screen in `course/style-lock/`; only final files in `frontend/static/art/` as WebP (rooms 1920 px wide, under 500 KB; people with alpha, under 300 KB). Edit nothing else; leave everything uncommitted. If the usage limit is near, finish the mess hall and Thomas first.

## Pass/fail checks
1. Flaws 1–6 are gone, each confirmed on the opened image.
2. Every canon object of both rooms and each exit is present, separate, unobstructed, at least 5% of the image width.
3. Four images side by side look like one artist and one ship: line weight, paper, palette, light direction.
4. Mood: at thumbnail size the face or lit area is the first thing seen; average luminance of the mess hall is clearly lower than in the first attempt (report both).
5. Face readable at 95 px tall; both people have distinct silhouettes; alpha corners are 0; no halo over a dark background.
6. No readable text, body, weapon, extra person, luxury or science fiction.
7. Dialogue text contrast at least 4.5:1.
8. Every saved prompt matches its image; the changelog names the visible flaw behind each change.

## Return
Check table with observations, full paths of the four finals and both screens, each opened and described including flaws, luminance values, images generated in total, and the weakest point of the style for the remaining rooms and people.
