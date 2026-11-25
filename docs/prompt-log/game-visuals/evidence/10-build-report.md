> Worker report as delivered; links to local files removed.

# Suspect dialogue verification

Thomas answered on turn 4 and both lines survived reload. Olivia’s initial-observations topic also advanced turn 3 to 4, collected her preliminary observations and made zero model calls. Both runs used Chrome 158 on loopback. Everything below used fake speech providers.

## Acceptance checks

| # | Result | Observed |
|---|---|---|
| 1 | Pass | At both sizes, “Good morning.” received “(FakeLLM) I'd rather not say more right now.” The player and Thomas each had one line after reload. In Medical Bay, Olivia’s topic yielded “Olivia shares what she can from her initial examination.” Her named evidence appeared in both the notice and the inventory. |
| 2 | Pass | Walked to all six suspects through room exits at both sizes. Each opened from the room roster. A queued request addressed to Olivia in Mess Hall returned “Olivia Hart isn't here.” |
| 3 | Pass | Selecting Olivia’s observations submitted only EV-10. A forged ID sent through Gradio returned a refusal. Comparing the two decoded saves showed exactly one change, the incremented turn. |
| 4 | Pass | Asking Olivia to compare the injury before meeting the prerequisites returned her engine refusal beginning “I can't give you a reliable cause yet.” The inventory stayed unchanged. Separate topic runs produced a Maya statement notice and the engine’s new lead to return to Olivia. |
| 5 | Pass | During a 15 s fake reply the player’s line entered the visible transcript in 1.5 ms at 1280 and 0.8 ms at 1440, measured from the submit event. The thinking line showed 2 s. Leave and a move reached Main corridor at turn 17. The save stayed identical after the original reply deadline. |
| 6 | Pass | A model exception containing a fake provider credential produced one in-world failure line and restored the original question. Retry received a reply on the following turn. The server log recorded the client and exception type. The fake key had zero matches across inspected responses, events, page, storage and server logs. |
| 7 | Pass | Eight simultaneous 3 s conversations reached peak concurrency 4. At 1280, all eight answered in 3.070–6.098 s and a ninth player moved in 7 ms. At 1440, answers took 3.044–6.071 s and the move took 5 ms. The direct Gradio route refused a queue bypass with HTTP 404. |
| 8 | Pass | A 4,021-code-point response displayed literal markup, a 4,000-character unbroken word, an emoji and Hebrew text. The reply created zero markup elements. The transcript and page fit their widths. |
| 9 | Pass | Whitespace and 501 Unicode characters generated zero talk POSTs from the composer. Direct queued requests returned invalid_message. The counter showed 501 / 500 for 501 fish emoji. An empty provider reply produced the in-world pause and enabled Retry. |
| 10 | Pass | Thomas said “The wet lab is open now.” After returning to Main corridor, the exit still showed Locked and the engine refused entry with the captain’s authorization message. |
| 11 | Pass | Reload restored completed conversation and explained an interrupted reply. A second tab reopened the same transcript. A concurrent move in another tab won under both Web Locks and IndexedDB takeover. With site storage blocked, the page explained the session lifetime and kept the exchange through Leave and reopen. After 70 exchanges, reload returned turn 73 and the latest 60 speech messages, starting at question 41. The largest token for that short dialogue was 1,016 bytes. |
| 12 | Pass | Used Tab, Enter, typing and Escape to open Olivia, talk, choose a topic, select evidence and return focus to her room button. Focus-visible checks passed. The live region received one player line and one Thomas reply. Reloading history added zero announcements. |
| 13 | Pass | Native 200% browser zoom produced 640 × 360 and 720 × 450 CSS viewports. The field, last reply and Leave were visible together. Document widths were 640 and 720 respectively. |
| 14 | Pass on the specified plain-text surfaces | At each size the privacy run checked 16 requests, 14 responses, 2 Gradio events, the DOM and browser storage. There were zero matches for 19 flag names, 8 uncollected evidence IDs, the assembled prompt, NPC knowledge text or the fake credential. The inherited signed, compressed save can be decoded by its owner. See the save limits below. |
| 15 | Pass | 125 tests passed. All 388 hotspot edge clicks reached the intended target at each size, across 97 targets in 23 rooms. Forty held-Enter keydowns produced one inspection. Twenty alternating tab actions ended at turn 24 with equal tokens. All four malformed/foreign save cases recovered. The earlier 800-exchange browser save test reached peak token sizes of 16,288 and 73,988 bytes, with the remaining investigation state intact. A forged room move was refused. The storage, delayed inspection and ten plain-HTTP takeover regressions passed. Browser checks recorded zero console warnings or errors. |

The two viewport records contain the observed replies, turns and input timings. Subsequent focused checks cover concurrency, native zoom, session-only play, plain-HTTP takeover and the privacy audit. 1280 checks · 1440 checks · Olivia and lead events · 1280 queue · 1440 queue · 1280 zoom · 1440 zoom · Cross-tab races · Privacy audit · Foundation save growth · Foundation regressions · Storage and takeover · 1280 edges · 1440 edges · Test output

## Screenshot inspection

Opened all twelve frames. The paired links show the same state at 1280 × 720 and 1440 × 900.

| State | What is visible and where the design falls short | Frames |
|---|---|---|
| Empty | Thomas’s name and role sit beside the neutral bust. The field has a visible focus ring and Leave is separate from Send. The empty history occupies a substantial area before the first line. | 1280 · 1440 |
| Conversation | The auditor’s short sans-serif question and Thomas’s larger serif reply read in sequence. The simple silhouette gives the speaker a position but conveys no expression. | 1280 · 1440 |
| Evidence | Olivia’s italic narration sits above the ochre evidence notice. Both collected items fit below Show evidence. The evidence buttons resemble the menu controls above them. | 1280 · 1440 |
| Waiting | The outgoing line, elapsed 2 s, active Leave and the consequence of leaving are visible together. The elapsed text is relatively quiet, especially across the wider panel. | 1280 · 1440 |
| Failure | Thomas’s previous answer stays in view. The pause appears as narration, the exact failed question returns to the field, and the action reads Retry. Retry shares Send’s placement and relies on the label change. | 1280 · 1440 |
| Native 200% zoom | The latest reply, field and Leave remain in view together. The compact layout hides the portrait to preserve reading space. At 640 CSS pixels wide, the panel partly covers the room title behind it. | 1280 · 1440 |

## Design scores

| Dimension | Score | Reason |
|---|---|---|
| Feels like facing a person | 6/10 | The fixed position, name, role and timed pause establish who is speaking. The expressionless bust cannot distinguish the six people visually. |
| Readable | 9/10 | Speaker labels, distinct type and a scrolling transcript let the player distinguish speech, their own words and narration. The narrow version preserves the last reply. Small role labels are less prominent. |
| Room for a portrait | 9/10 | Roughly one quarter of the desktop panel is reserved for a waist-up figure. An approved portrait can occupy the existing image slot. Compact mode prioritizes the conversation. |
| Fits a tense ship mystery | 7/10 | Ink-blue surfaces, muted brass and the visible room establish the setting. The schematic room and shared silhouette limit atmosphere. |

## Implementation and limits

- **Server and saves.** Changed `frontend/server.py` and `frontend/saves.py`. Added `frontend/dialogue.py`. The server constructs the voice client at startup. Talk and topic use Gradio’s four-slot queue. Movement and inspections keep their existing route.
- **Player UI.** Changed `frontend/static/index.html`, `player.js`, `scene.js` and `save-slot.js`. Added `frontend/static/dialogue.js` and `dialogue.css`. The approved-art slot points to the character’s future WebP via an inert data attribute. Existing art is never requested by this UI.
- **Tests.** Added `tests/test_frontend_dialogue.py` for the engine refusals, turn accounting, message boundaries, provider failure, saved topics and access claims.
- **Engine gaps.** There is no public query for a person’s conversation, no persisted record of topic narration and no typed provider-failure field. The frontend reads the serialized speech history, keeps topic and event lines next to it in the signed save, and translates a sanitized provider failure to an in-world pause.
- **Save limits.** Speech retains the foundation’s latest 60 messages per suspect. The HMAC authenticates the compressed browser token. A technical player can decode that token and inspect engine state, including flags. The privacy check covers exposed player data and literal saved text. It does not establish encryption. NPC prompt files currently use the engine’s fallback personas.
- **Coverage limits.** Keyboard operation and live-region mutations were verified in Chrome. Spoken output from an actual screen reader, Safari, Firefox, touch input, hosted latency, real providers and final artwork remain untested.

## Next steps

1. Run the same keyboard exchange with VoiceOver or NVDA and listen for focus and announcement order.
2. Once portraits are approved, populate the existing image slot and repeat the six-person composition check.
