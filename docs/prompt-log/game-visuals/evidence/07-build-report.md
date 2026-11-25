> Worker report as delivered; links to local files removed.

# Ink-and-wash acceptance review

Six generated images yielded four final assets. The two 1280 × 720 dialogue screens were opened in Orca, including directly from their local HTML files. The remaining six rooms and four portraits await production. All six casting descriptions are PROPOSED. The existing local Git exclude covers `/course/`, so the uncommitted screen and review files appear on disk but are omitted from ordinary Git status.

## Opened deliverables

| File | Observation and limitation |
| --- | --- |
| Mess hall WebP · 1920 × 1080 · 204,280 bytes | A hooded lamp lights the left bulkhead. The sole sea window, secured galley and matte table read clearly. The wood grain is more prominent than the other surfaces. |
| Thomas Blake WebP · 768 × 840 · 95,384 bytes | Open lapels, silver temples and the belt remain visible. Gaze is to screen-right. The lit shirt is his second-brightest feature. |
| Bridge WebP · 1920 × 1080 · 286,400 bytes | A sloped bank of storm windows identifies the bridge. The upright weather display, chart/radar pair, log laptop, radio and board have different outlines. The log terminal is the smallest. |
| Sarah Morgan WebP · 768 × 840 · 114,002 bytes | Cropped curls, broad shoulders and a high graphite collar distinguish her from Thomas. Their head turn and downward arm posture are similar. |
| Thomas in the mess hall · opened screen | Face and lamp form a single warm area. The waist goes behind the panel. His right sleeve overlaps the left end of the foreground furniture, clear of its clickable surface. |
| Sarah on the bridge · opened screen | Her cheek catches the lamp while her lower sleeve meets the panel. The left edge of the console cabinet sits behind her arm, with both displays and the target exposed. |

Absolute paths in this worktree:

```text
mess_hall.webp
thomas_blake.webp
bridge.webp
sarah_morgan.webp
mess_hall.html
bridge.html
```

## Acceptance checks

| Check | Result | Observations |
| --- | --- | --- |
| 1. Secured fittings and crockery | Pass | The coffee cabinet sits flush on a fixed plinth. A fiddle rail crosses the mugs, a band retains the brewer, and plates stand behind a separate wire rack. |
| 1. Materials and table | Pass | The steel has a continuous blue-grey wash and local edge highlights. Wood grain follows the seat and tabletop. The four tabletop edges describe one plane with a straight front edge and two converging sides. Bolted pedestal feet are visible in the empty room. |
| 1. Light and Thomas integration | Pass | Grey sea, subdued glass and ceiling lights, darker corners and a warm pool under the left lamp. The same side of Thomas's face catches it. A soft shadow falls down-right. His belt meets the panel and his eyes turn toward the player. |
| 2. Mess hall targets | Pass | Table 36%, galley 15%, board 17%, coffee 18%, main corridor door 12% of frame width. The rail through the door pane reads as an interior route. |
| 2. Bridge targets | Pass | Navigation console 17%, weather 10.5%, log station 7.5%, communications 13.4%, board 13%, upper stairs 12%. The smallest hit region is 96 px wide on the 1280 px screen. |
| 2. Click and keyboard | Pass | All eleven target centres passed browser hit testing and toggled their labels. No two target rectangles intersect. Checking the overlaid portrait alpha across each target found zero covered pixels above 32/255. Enter activated the mess board and bridge log controls. |
| 3. Style transfer | Pass | Viewed four exports together. Fine interrupted contours, paper tooth inside the washes, cool shadow planes and upper-left ochre recur. The bridge windows and Sarah's collar distinguish the second pair. Four finals together |
| 4. Mood and luminance | Pass | At 320 × 180, attention goes to the face and lamp area. Mean linear sRGB relative luminance Y, before compositing, is **0.2151** for the option's original v1 and **0.0935** for the final mess hall, a **56.5% reduction**. The prior selected option background measures **0.3058**. Computed per pixel after sRGB linearization using weights 0.2126, 0.7152, 0.0722. |
| 5. Face, silhouette, alpha | Pass | On a dark matte both faces retain distinct eyes, nose and mouth at about 95 px hairline to chin. Thomas's narrow jacket opens into a V. Sarah's high collar joins a broader, closed torso. The four corner alpha values are 0,0,0,0 on each decoded WebP. Hair and sleeves have no visible pale perimeter. Face crops |
| 6. Spoilers and setting | Pass | No legible writing on cards or instruments. The two room plates are empty. Each portrait shows a single conversational figure. Contemporary latches, consoles, practical workwear and restrained wear fit a working vessel. No body, weapon, luxury fittings or science-fiction devices appear. |
| 7. Dialogue contrast | Pass | Speech and speaker names are **12.23:1**, roles **7.71:1** against the opaque panel, calculated from decoded sRGB colour values using (L1 + .05) / (L2 + .05). |
| 8. Prompt provenance | Pass | Six saved generator inputs match six original PNGs. All begin with the verbatim paragraph in the style guide. Each room has two versions, each portrait one. Both room follow-ups change the exit pane. References, visible reasons and selected versions are in the changelog. |

The weakest point is repetition of staging. Both lamps, far-right doors and speaker poses fall in nearly the same places. For the next room, start with its defining work surface and plan the viewpoint around it. For the next portrait, vary the shoulder turn or resting-arm position while retaining the shared light and eyeline.
