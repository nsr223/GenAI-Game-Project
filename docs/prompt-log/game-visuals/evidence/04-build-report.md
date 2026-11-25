> Worker report as delivered; links to local files removed.

# Player UI foundation

All 13 acceptance checks passed in Chrome 158.0.8127.89 on macOS at 1280×720 and 1440×900. The full Python suite passed 113 tests, including nine new frontend cases. The implementation is uncommitted in the dispatched workspace. Run it with `python -m frontend.server` from the repository root.

| Check | 1280×720 | 1440×900 |
| --- | --- | --- |
| 1. Start and return | Your cabin, turn 0 → Crew Quarters → Main corridor → Mess Hall, turn 3 → back along the same path, turn 6 | Same rooms and turns |
| 2. Full hotspot area | 485/485 real clicks advanced the turn. Each of the 97 hotspots in 23 rooms received a centre click and a click 4 px inside the midpoint of each edge. | 485/485 |
| 3. Held keys | Enter and Space each produced one inspection request and one turn during a two-second hold with repeated keydowns. | One request and one turn for each key |
| 4. Slow inspection | Busy DOM in 0.1 ms, observed at a frame boundary by 19.4 ms. Slow action took 3,028.6 ms. Another player's click updated in 39.9 ms. | 0.1 ms, 21.9 ms, 3,020.7 ms and 35.2 ms respectively |
| 5. Reload and cross-tab resume | Reload and a newly opened tab showed Mess Hall, turn 23. Moving in the first updated both to Main corridor, turn 24. | Same rooms and turns |
| 6. Refused saves and recovery | Changed, truncated, oversized and foreign-signed saves all displayed the refusal. The stored token survived until Enter on New game started Your cabin, turn 0. | All four recovered |
| 7. Restart with the same secret | Restarted the Python process on the same origin and reloaded. The exact token restored Main corridor, turn 24. | Same result after a second process restart |
| 8. Engine enforcement | The secured Wet Laboratory displayed the captain's exact refusal and stayed closed. A direct move request from Mess Hall returned “You can't get to Wet Laboratory directly from here.” The room remained Mess Hall. | Both refusals matched |
| 9. Literal game text | A fixture supplied an object name containing an HTML emphasis tag. The button showed the literal markup before and after inspection. Zero matching elements appeared. | Same result |
| 10. Keyboard and announcements | 97/97 hotspots reached using Tab and activated with Enter, each with a solid focus outline. Retry and New game worked with Enter. The polite live region updated to “Current location: Main corridor.” | 97/97 hotspots and both recovery controls |
| 11. Browser data | Zero matches across all 19 engine flag names in 23 room DOMs, stored tokens, and 29 HTTP responses plus their requests, including static assets. A separate all-hotspot sweep checked action requests and responses against 15 initial and derived flag names. | Same counts |
| 12. Console and suite | Zero console warnings, errors or uncaught page errors in the main browser run. Orca's embedded browser also opened Your cabin with an empty console. All 113 Python tests passed, including save and route coverage without an LLM. | Zero console warnings, errors or uncaught page errors |
| 13. Stored representation | The turn-24 save was 768 ASCII characters with zero flag name matches. Decoding and decompressing it recovered the engine state and 15 stored flags. | Same length and decoded flag count |

Browser-reported double-clicks at 350 ms and 500 ms intervals each produced one inspection request and one turn at both sizes.

During the slow action, the active tab retained keyboard focus on Mess table and all hotspots exposed their unavailable state. The other tab sharing its save also showed busy controls until the Web Lock released. The independent player used a separate browser storage context against the same server and inspected Desk during the delay. A transient action error exposed Retry and completed exactly one inspection on retry.

Plain HTTP was exercised at a non-loopback hostname mapped to the fixture server. Chrome reported an insecure context and an unavailable Web Locks API. During a delayed Mess table inspection, the other tab moved to Main corridor. Both tabs then converged on Mess Hall, turn 4, when the slower inspection wrote last. This fallback can discard a simultaneous move. With Web Locks, a stale queued activation refreshes from the newer shared save.

A technical player can read the complete saved state, including internal flag names, their values and collected evidence. The HMAC authenticates the compressed payload. It permits replay of a previously valid save, and altering the payload invalidates its signature. Encoded saves are limited to 128 KiB and decompressed data to 512 KiB. An unset or empty `SAVE_SECRET` generates a temporary key. A configured key must be at least 32 bytes and have no leading or trailing whitespace. A stable random secret preserves saves across process restarts.

## Click-to-update measurements

Elapsed milliseconds from the browser's trusted click event to the ready DOM with the updated turn. Ten clicks alternated between Mess table and Galley counter on localhost.

| Viewport | Ten consecutive clicks, ms |
| --- | --- |
| 1280×720 | 20.7, 15.4, 10.4, 20.9, 12.2, 14.4, 17.4, 14.7, 20.8, 14.1 |
| 1440×900 | 19.3, 17.7, 18.3, 17.7, 17.9, 17.2, 18.2, 18.6, 18.0, 18.6 |

## Screenshots

Opened all ten PNGs and inspected both sizes. The cabin and mess hall use authored percentage positions. The corridor demonstrates the automatic layout.

| State | Visible result | 1280×720 | 1440×900 |
| --- | --- | --- | --- |
| Start | Your cabin, turn 0, with a desk to inspect and the Crew Quarters exit. | Start | Start |
| Mess Hall | Four inspection buttons, Main corridor exit and Thomas Blake listed as present. | Mess Hall | Mess Hall |
| Locked exit | Wet Laboratory has a lock, hatching and focus ring. The adjacent observation gives the captain's refusal. | Locked exit | Locked exit |
| Busy | All five controls are dimmed. The focus ring remains on Mess table and the observation reads “Action in progress…”. | Busy | Busy |
| Refused save | The title reads “Save unavailable”. The empty scene has no actionable hotspots and New game has the focus ring. | Refusal | Refusal |

## Files changed

| Files | Purpose |
| --- | --- |
| `frontend/server.py`, `frontend/saves.py` | Serve the Gradio ASGI app, static files and stateless action route. Validate the startup secret and authenticate saves before decoding, decompression or JSON parsing. |
| `frontend/scenes.json`, `frontend/static/scene.js` | Percentage hitboxes, automatic placement, native buttons, safe text rendering and the optional room-image layer. |
| `frontend/static/index.html`, `frontend/static/scene.css`, `frontend/static/player.js` | Scene shell, schematic placeholder art, persistent audio element, interaction feedback, keyboard handling, local saves and cross-tab synchronization. |
| `requirements.txt`, `.env.example` | Requested Gradio range and blank secret placeholder. |
| `tests/test_frontend_saves.py`, `tests/test_frontend_route.py` | Nine save and route test cases. |

## Coverage limits and next steps

The 23-room input sweep used signed fixture saves to reach restricted rooms. The start, round trip and locked-exit checks used normal gameplay. Browser timing is local. Physical keyboard repeat settings, spoken output from an actual screen reader, touch input and other browser engines remain untested. The room-image and audio elements are integration points for future assets. No narrative TBDs were decided.

1. Have a teammate review the save format, browser fallback and action contract.
2. Fit the first approved room artwork to the percentage hitboxes and repeat the edge-click checks.
3. Exercise keyboard navigation and room announcements with a screen reader before extending the controls.

The browser scripts, fixtures, and raw timing and scan results are alongside this report. Main observations · Insecure-context fallback and 19-flag scan · Held-key request counts
