# Task: three visual directions for Beneath the Surface

## Goal and why
Erik will pick one direction that then fixes the look of 8 rooms, 6 suspects, portraits and icons. Show three options that differ in how they are drawn, not just in colour, so the choice is real. Judge them as a game screen, not as standalone pictures.

## Context
Read `AGENTS.md`, `docs/summaries/visuals-audio.md`, World Bible sections 3.4 and 7.1 (search the headings) and sections 1–2 of `docs/characters/thomas_blake.md`.
- Mood: a confined, modern working research ship in a winter gale. Maintained but used. The mess hall is the warm room: ordinary clutter against grey-blue metal.
- Canon gives Thomas's manner (polished, articulate, status-aware, a believable person rather than a cartoon villain) but no physical appearance. Any face, age, hair or clothing is a proposal: list it as such.

## Build, for each direction
1. One paragraph: rendering technique, line, light, palette as hex values, texture, and why it suits this story. The look is original: describe technique and light rather than naming artists, studios or games.
2. `mess_hall`, 16:9 landscape, empty of people, eye level, wide shot. The bolted-down table, galley counter, noticeboard, coffee station and one door must each be separate, unobstructed and recognizable, because each becomes a clickable area. Leave calmer space at the lower third for dialogue. Boards and labels carry no readable text.
3. `thomas_blake`, waist-up, facing slightly off camera, neutral expression, transparent background, lit like the room.
4. `screen`: an HTML mock at 1280×720 with the room, Thomas placed in it and a dialogue panel with two sentences of neutral placeholder text, captured as a screenshot.

Use the built-in `imagegen` skill. Make one style block per direction, reused word for word in both images; vary only the subject. Look at each result, then refine on a named flaw, one change per version, at most 3 versions per image. Keep every version.

## Constraints
- Write prompts to `prompts/assets/style/<direction>/<asset>/vN.md` and one `prompts/assets/style/CHANGELOG.md` (version, observed flaw, change and reason, model or tool used).
- Write images and mocks to `course/style-options/<direction>/` (git-ignored). Edit nothing else. Leave everything uncommitted.
- Spoiler rules of `AGENTS.md` section 3 apply: nothing hints at the crime.

## Pass/fail checks
1. Three directions; side by side, a viewer could tell them apart in greyscale.
2. In each room image, the 4 objects and the door are present, separate and unobstructed.
3. Contemporary technology, bolted furniture, no luxury, no science fiction, no body, no weapon, no people.
4. Thomas has real transparency (report the alpha range and corner values) and clean edges over the room.
5. Room and Thomas look as if one hand made them: same line, light direction and palette.
6. Dialogue text in the mock has a contrast of at least 4.5:1.
7. Every saved prompt matches the image it produced; changelog entries describe flaws visible in a kept file.

## Return
A table of checks with what you observed, full paths of the three screens and the images, each opened and described including flaws, and your ranking with the weakness of your first choice.
