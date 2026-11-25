# Mess hall visual directions

## Decision

**1. Gouache.** Thomas’s gaze, uneven brows and closed mouth carry a listening expression at dialogue size. His jacket and the room share broad, interrupted shadows. Its weakness is the high-contrast amber patch on the tabletop and ceiling that competes with his face. **2. Ink and wash.** Fine contours make the counter fittings, carafe and door handle easy to find. The uninterrupted long table and equal emphasis on rivets, crockery and face make the screen busier. **3. Cut paper.** The brewer, noticeboard and door have the clearest silhouettes. The eyes still point distinctly toward the player’s side, but the heavy eyebrows and single lip shape make Thomas look more guarded and give his neutral expression less nuance.

### Rendering briefs

**Gouache.** Paint in opaque gouache with broad square-ended brushstrokes, scraped dry-brush edges and directly adjacent shapes of value. Lose selected contours in shadow and leave small, precise light accents. Warm diffuse light from high camera-left and cold fill from camera-right sculpt the forms. Use slate #405663, deep green-grey #293C40, warm pewter #9AA8A4, lamp cream #F1CF95 and clay #AC7966. Make the light feel shared and domestic inside the confined ship, with human-scale marks that carry subtle expression.

**Ink and wash.** Draw in fine, irregular carbon-ink contours and short directional hatching, with thin pools of translucent watercolour on pale cold-pressed stock. Let the white of the sheet break through on lit edges. A soft amber practical from high camera-left and blue-grey fill from camera-right establish the form. Use midnight ink #25333A, Payne’s grey #637B84, paper #EEE6D2, ochre #C69A59 and muted terracotta #AA7867. Let meticulous marks reward the player for looking closely while sparse open washes keep the scene quiet.

**Cut paper.** Construct a shallow paper relief, photographed straight on: physically overlapping hand-cut sheets of dyed matte paper, clean bevel-like scissor cuts and narrow contact shadows, with fine paper fibres visible inside broad value shapes. Define details by nested silhouettes, without drawn outlines. Warm soft light from high camera-left casts tiny shadows down-right with cool fill from camera-right. Use graphite #29383C, storm #526C78, smoke #98A7A5, biscuit #DEC49A and russet #A36A50. Keep restrained natural proportions and spare facets so the working ship reads immediately in silhouette.

**Casting proposal across all three.** About 48, medium-brown skin, lean oval face, straight nose, brown eyes, short dark wavy hair with silver temples, clean-shaven, navy work jacket and open-necked pale blue shirt. The character bible establishes his polished, status-aware manner. Age, face, hair, build, wardrobe and poses are proposals. The cut-paper rendering broadens his jaw slightly and the gouache rendering shows clasped hands.

## Checks on the selected assets

| Check | Result | Observation |
|---|---|---|
| Greyscale | Pass | Compared all three game screens together in greyscale at 480 × 270 each. Gouache breaks light into broad strokes, ink draws fittings and edges with fine dark lines, and cut paper separates planes with narrow cast shadows. |
| Five room targets | Pass | Each empty room shows a bolted table in the foreground, a sink and galley worktop behind it, a blank noticeboard, a separate brewer with mugs, and a single door and handle on the right. Each has its own clear target area. The foreground table naturally overlaps the cabinet fronts below the worktop. Thomas covers some of the table on the left in dialogue mode. |
| Ship and spoilers | Pass | All three show rain or rough water, restrained metal interiors, bolted pedestals, ordinary galley appliances and warm practical lighting. The empty rooms contain no people, readable notices, weapons or crime imagery. Gouache’s heavy brush marks make the bulkheads look more worn than the other treatments. |
| Portrait alpha | Pass | Original 8-bit RGBA PNGs. In top-left, top-right, bottom-left, bottom-right order: gouache 0,0,0,0; ink 0,0,0,0; cut paper 0,0,1,0. Range 0–254 in each. Cut paper has one alpha count out of 255 in its bottom-left corner. No visible box, matte fringe or glow at the hair and shoulders in the screenshots. |
| Room and portrait pairing | Pass | Warm upper-left highlights recur on each portrait’s temple and jacket. Ink repeats the fine pen marks, gouache repeats broken planes of paint, and cut paper repeats layered edges. The ink face is more finely modelled than the room and the cut-paper face flattens the mouth and cheeks. |
| Dialogue panel | Pass | All three HTML mocks were opened in Orca. Actual captures are 1280 × 720, with a 533-pixel-high portrait element. The identical two sentences use #FAF4E7 on opaque #19272D for 13.99:1 WCAG contrast. The role label uses #DECEB4 for 9.93:1. |
| Provenance | Pass | 14 numbered prompt files and 14 original numbered PNGs. Each pair uses the same first paragraph verbatim. Each revision takes the preceding numbered PNG as its only input. The non-numbered room exports are centred 1600 × 900 resamples of the selected PNGs. Portraits retain their original alpha channels. |

Open the three screens side by side in greyscale. Left to right: gouache, ink and wash, cut paper.

## Full paths

| Direction | Room | Portrait | Captured screen | HTML mock |
|---|---|---|---|---|
| gouache | mess_hall.png | thomas_blake-v2.png | screen.png | screen.html |
| ink-wash | mess_hall.png | thomas_blake-v2.png | screen.png | screen.html |
| cut-paper | mess_hall.png | thomas_blake-v2.png | screen.png | screen.html |

## Generation log

All generations and edits used the built-in ImageGen tool. Room requests used an opaque background and portraits used transparent background mode. Prompt files contain the submitted prompt body. Tool input image and output are given by the preceding and current version in the same asset directory. Numbered PNGs retain the tool output bytes.

| Direction and asset | Version | Observed issue | Change and reason | Inspection of this version |
|---|---|---|---|---|
| Gouache room | v1 | First attempt | Establish the painted mess hall. | Brewer covers the board’s lower-right corner. |
| Gouache room | v2, selected | v1 overlaps the two targets. | Move the board left to expose its frame. | Clear strip of wall between board and brewer. Strong table highlight competes with Thomas. |
| Gouache Thomas | v1 | First attempt | Establish face, gesture and brushwork. | Crop stops above the belt with sleeves at the side edges. |
| Gouache Thomas | v2, selected | v1 is tightly cropped. | Widen the framing to include the waist. | Belt and loosely clasped hands are visible; neutral mouth and rightward gaze hold up in the screen. |
| Ink room | v1 | First attempt | Establish the pen and wash treatment. | Dark repeated floor circles draw attention to the lower third. |
| Ink room | v2 | v1 floor dominates. | Reduce deck-tread contrast to quiet the dialogue area. | Floor recedes. The initial game screenshot reveals that the sprite leaves little exposed tabletop. See screen-room-v2.png. |
| Ink room | v3, selected | v2 table ends just past Thomas’s shoulder in the composite. | Lengthen the table to leave an exposed clickable surface. | Top extends beyond the screen midpoint. The bright table now occupies more of the lower composition. |
| Ink Thomas | v1 | First attempt | Establish the portrait in ink and wash. | Bottom edge cuts through shirt and jacket above belt. |
| Ink Thomas | v2, selected | v1 crop omits waist. | Widen the framing to reveal the belt line. | Belt and sleeves are contained, fine brow lines and mouth survive reduction. |
| Cut-paper room | v1 | First attempt | Establish the layered-paper room. | Cart top nearly meets the door frame. |
| Cut-paper room | v2 | v1 gives the cart and door almost no breathing room. | Shift the cart left for clearer separation. | Door clears the cart, but the brewer now clips the board’s right edge. |
| Cut-paper room | v3, selected | v2 brewer overlaps board. | Shift the board left to recover the clear outline of each. | Visible wall separates board, brewer and door. The straight-on treatment makes the room feel staged. |
| Cut-paper Thomas | v1 | First attempt | Establish the nested facial shapes. | Sleeves and lower torso run off the frame. |
| Cut-paper Thomas | v2, selected | v1 crop ends early. | Widen framing to show the waist. | Belt and pocketed hands are visible. Eye direction reads clearly; the mouth and fixed brow lose subtlety. |

## Review after the run

The team chose **ink and wash** on 2026-11-24. Found afterwards in all three directions, although the checks had passed: the coffee station is a trolley on wheels, while canon furniture is bolted (World §7.1). Cause: the room prompts ask for a cart. In ink and wash also: rust speckles on metal and wood, a bent table top, and a portrait that looks pasted on. Changes: see [the next series](../CHANGELOG.md). The comparison shown to the team is [here](../../../docs/prompt-log/game-visuals/img/03-styles.webp). Each prompt version's image is stored next to it as `vN.webp`.
