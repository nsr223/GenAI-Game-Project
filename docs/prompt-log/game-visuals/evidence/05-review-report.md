> Worker report as delivered; links to local files removed.

# Player UI foundation review

**Accept with named fixes.** The engine-backed room interaction is ready to build on. Before enabling dialogue, make conversations fit the save contract and give the player a way to dismiss a failed action. Before integrating room art, separate the clickable area from its opaque placeholder. Before a shared playtest, use a stable signing key, handle browsers without Web Locks, and make action feedback visible at high zoom. If the course requires a functional Gradio integration, settle the runtime choice before building the next API.

## Defects ordered by player effect

| Priority | Smallest reproduction observed | Effect and smallest practical change |
| --- | --- | --- |
| 1. An ordinary restart can strand the entire investigation | Start without `SAVE_SECRET`, play, restart without it, resume. A different configured key also reproduces the refusal. | The player gets “Save unavailable” and only **New game**. The bytes survive until reset. An ephemeral key disappears with its process. Configure one randomly generated, stable secret for the shared deployment and fail deployment startup if missing. If ephemeral local play stays, tell the player when they start. |
| 2. Two tabs can erase an acknowledged move | On a plain HTTP hostname without Web Locks, start a slow Desk inspection in tab A. Move to Crew Quarters in B and wait for A to finish. | B visibly reached Crew Quarters, turn 1. Both tabs then reverted to Your cabin, turn 1. One completed action vanished. Use HTTPS for the hosted game and guard unsupported clients against concurrent editing of a shared slot. A stale read followed by an unconditional write allows the rollback. Player save coordination |
| 3. A long investigation can get stuck retrying a dialogue submission | Resume the last accepted fixture after 356 exchanges. Submit the next 60-word message and receive a 60-word fake reply. Press Retry. | The server rejects the new save after generating the reply. The player never sees it, all five hotspots dim, and Retry repeats the rejected operation. Reload restored the prior 356 exchanges and allowed movement. Add **Return to investigation** for a permanent save-limit error. Bound the history included in each save before shipping dialogue, retaining journal facts and providing a separate transcript if the player must be able to reread earlier lines. Increasing the cap only postpones this failure. Size check · Recovery dispatch · History append |
| 4. Denied or full storage prevents play with little guidance | Block site storage in Chrome and open the game. Independently, fill this origin's quota and try a move that grows the existing token by eight characters. | Both conditions produce the same connection/storage advice. Retrying while storage is full leaves the screen disabled. Freeing the test padding and pressing Retry completed that move once, using the old save. Handle permission and quota errors separately, offer a truthful session-only option if acceptable, and direct players to enable storage or free space without deleting their investigation. Save write and catch |
| 5. At 200% zoom the result of an inspection is offscreen | At 1280×720, zoom to 200% and view the Mess Hall. The observation starts at y=637 CSS px in a 360-CSS-px viewport. | A player looking at the upper hotspots cannot see the result or busy text. Put the current observation or a “Read observation” control with an update indicator beside the scene on the single-column layout. Responsive rule |
| 6. Approved art would still be hidden behind placeholder fills | Supply a room image via the existing `image` slot. Compare pixels inside and outside Mess Hall's five targets. | The image loaded. Its solid test colour showed in open space. A sample inside Mess table stayed the opaque button colour. The five target boxes cover **31.6%** of the room. Keep their full pointer/focus areas and render only a compact label or marker when artwork is present. Hotspot styles |
| 7. A long action has no evolving sign of life | Inspect Desk with a 15 s server delay. Compare the screen near 0, 7 and 14 s. | “Action in progress…” and disabled controls acknowledge the click. The text stays identical with zero running animations. Add an elapsed indicator or a delayed, action-specific status near the source of the action, available at high zoom and with reduced motion. Busy state |

## A. Independent behaviour tests

| Check | Observed result |
| --- | --- |
| Hotspot edges | **388/388** real pointer clicks at 1280×720, two pixels inside the midpoint of all four edges of all 97 targets across 23 rooms. Each reached the intended target in an HTTP action and produced a ready view. Signed room fixtures made restricted rooms reachable. |
| Held Enter | Focus Desk, hold Enter for about two seconds with 40 repeated key-downs, then release. **One** inspect request and turn 0 → 1. |
| Reload and second tab | Walked to Mess Hall. Reload and a new tab showed Mess Hall, turn 4, with the identical token. |
| Refused saves and direct move | Truncated, damaged, oversized and foreign-signed saves each cleared hotspots, showed the refusal, and retained their original bytes. Enter on New game took each to Your cabin, turn 0. A direct move from Mess Hall to the unconnected Wet Laboratory returned “You can't get to Wet Laboratory directly from here.” The room stayed Mess Hall. The engine counted the attempt as turn 5. |
| Dialogue capacity | See the measured table below. The encoded cap was reached first. Reload preserved every previously committed message and reply. The rejected exchange and its newly generated reply were discarded. |
| 15 s action and closing a tab | Sampled busy at 0.07, 7.28 and 13.89 s. The complete call displayed the Desk observation at 15.08 s. During a second call, closed the tab after ~1.5 s. A new tab resumed the identical prior token, obtained the Web Lock and reached Crew Quarters by 1.83 s from click. The old server worker finished its 15 s call. A later reload still showed Crew Quarters, turn 2. A future paid model call could run to completion after the player leaves. |
| Two tabs, 20 alternating inputs | With Web Locks, clicked as soon as the next tab displayed the latest turn. **20 inspections in 1.362 s**, ten per tab, turn 4 → 24 in both, identical token. Separately, 20 raw alternating mouse clicks in 15 ms yielded **one** inspection and turn 25 in both. Busy or stale clicks are discarded. No doubled or reverted committed turn in these secure-context runs. The no-lock run did revert an acknowledged turn, as above. |
| Browser storage blocked or full | Chrome's site-data policy produced a real `SecurityError`. On first load the title stayed “Opening scene…”, no hotspots appeared, and Retry was the sole control. In a separate, repeatable permission-fault test, restoring read access then Retry started the game. A real quota fill of 5,242,877 padding characters gave the same UI. Removing the padding and retrying started the game. Mid-game, the previous Mess Hall token survived a failed write and Retry completed the move after space was freed. |
| Stop and restart | Stopped the process at Crew Quarters, turn 1. An attempted move showed the generic error and left the token untouched. Restart on the same origin and key, then Retry, reached Main corridor, turn 2. Restart on the same origin with a different key displayed Save unavailable. The token survived until New game. Two no-key processes also refused one another's saves. |
| 20 simultaneous players | **0 errors** in 20 isolated Chrome contexts clicking Desk concurrently. All 20 received HTTP 200 and displayed turn 1. Slowest click-to-updated DOM was **412.2 ms** on this machine. In a separate barrier-synchronized HTTP run, slowest complete response was **11.66 ms**. Browser timing includes 20 local renderer processes and server timing includes loopback transport. These measure cheap inspections. |
| Gradio | Shipped runner serves the custom page and action. In the installed 6.32.0, plain `app.launch()` kept the page but broke the first action with HTTP 500. Explicitly passing the lifespan fixed the launcher in the test copy. API, queue, telemetry and hosting details follow. |
| Startup secrets | A short canary stopped startup with exit 3 and a length/whitespace message, without echoing the canary in stdout/stderr. An absent key started with a temporary-key log warning. The player received the normal game screen. Both a random valid value and a predictable 32-byte repeated-character value started and completed an inspection. Neither supplied value appeared in captured logs, page text, root HTML or new-game responses. Validation enforces byte length and surrounding whitespace. |

### Dialogue size and persistence

Both sides provided exactly 60 words per exchange. The deterministic fake sampled an 800-word vocabulary derived from the copied game data. This models varied token sizes, not human sentence structure. The engine's real `Game.talk()` appended both messages. We used its real serialization and compression on every turn. The browser boundary test mapped an existing inspection button to `talk()` in the test copy, preserving the shipped HTTP route, size checks, browser writes and recovery UI. Three prior moves reached Thomas in Mess Hall.

| Dialogue exchanges | Raw JSON / 524,288 B | Encoded token / 131,072 B | Save result |
| ---: | ---: | ---: | --- |
| 50 | 47,706 | 20,696 | Accepted |
| 150 | 139,807 | 56,792 | Accepted |
| 356 | 330,212 | 130,744 | Last accepted in this fixture |
| 357 | 331,127 | 131,104 | First refusal, 32 B over the encoded cap |
| 400 | 370,862 | 146,580 | Over cap, measured by continuing the engine simulation in memory |

The player remained at game turn 359 on refusal, retained all 712 prior history entries, and reached turn 360 with a move after reload. The exact failure turn depends on wording, character encoding, other collected state and compressibility. The model receives a recent-history window while the save retains the whole conversation. Engine save · LLM history window

### Runner and hosting decision

| In Gradio 6.32.0 | Shipped `uvicorn.run(app)` | Test-copy `app.launch()` |
| --- | --- | --- |
| Player page and actions | Custom HTML/JS loads. New and move both work. | Same page at `/`. New returns 500. Gradio replaces the ASGI lifespan during launch. `app.launch(app_kwargs={"lifespan": lifespan})` restored new and move. |
| Gradio client and queue | `/config`, `/gradio_api/info` and `/gradio_api/queue/status` returned 404. The FastAPI route runs in a Starlette thread pool. | All three returned 200. Config listed zero dependencies, named endpoints were empty and the queue reported size 0. The game's `fetch("/action")` still calls the custom route directly. Launching alone adds no queueing or streaming to gameplay. |
| Telemetry | With analytics enabled and Gradio's sender instrumented, observed zero Gradio version-check or initiation/launch telemetry hooks. | Observed the version check, initiated analytics and launched telemetry. `GRADIO_ANALYTICS_ENABLED=False` suppressed all three. The probe intercepted these hooks locally. |
| Meaningful Gradio use | The instantiated server class is Gradio's FastAPI subclass. On the tested player path, HTML, controls, requests, state transitions and concurrency all come from custom code or FastAPI/Starlette. | Gradio supports a custom frontend. To make Gradio provide a course-relevant feature, register a gameplay operation such as dialogue through `@app.api` and call it from the UI, then test saves, errors and queueing through that path. [Gradio Server mode](https://gradio.app/guides/server-mode) |

**Spaces is a deployment choice.** The current repo README lacks a Space SDK/application entrypoint declaration. A Docker Space can run this ASGI app, binding to `0.0.0.0` on the configured exposed port (default 7860). For a managed Gradio Space, provide an `app_file` that imports the package and runs the verified launcher with its lifespan, and exercise the game inside the hosted iframe. Use a stable Space secret for persistent saves. These are deployment implications from the local runtime and provider docs. A real Space was outside this read-only review. [Spaces configuration](https://huggingface.co/docs/hub/spaces-config-reference) · [Docker Spaces](https://huggingface.co/docs/hub/spaces-sdks-docker) · [Spaces secrets](https://huggingface.co/docs/hub/spaces-overview)

## B. Game-screen judgment

Scored the frame with placeholder shapes expected. The same inspected Mess Hall state shows an object response, an exit and a named character together.

| Criterion | Score | Concrete reason and change where below 7 |
| --- | ---: | --- |
| Confined ship in a gale | **5/10** | The double bulkhead and dark teal suggest a ship, but the broad, still cream surround feels calm. Carry the dark bulkhead colour into a compact ship-status header and surface the engine's current weather there. |
| Scene dominates | **7/10** | The scene is the first visual anchor and nearly fills the left side at 1280×720 (888×500). The 1440 px content cap leaves it at 1063×598 on a 1920×1080 screen, about 31% of the viewport. |
| Feels like a game | **6/10** | Inspecting an object puts its result in a detached editorial column headed “Field notes / Observation”. Put the current result in a compact scene-attached caption and reserve the notebook for deliberate review. |
| Text readability | **8/10** | Dark, 19 px observation text reads cleanly at all four desktop sizes. At 1024 the short observation wraps to three lines and the hotspot labels are comparatively small. At 200% the text reflows without horizontal scrolling. |
| Specific to this game | **6/10** | RV Meridian, deck number and the bolted-down table ground the screen, but the two generic field-note headings use prime space. Replace them with the selected object's actual name, or the speaker's name during conversation. |
| Room for portrait, dialogue, evidence and journal | **4/10** | At 1024 the entire sidebar is 229 px wide. At 200% it falls below the scene. Use a separate portrait-and-dialogue panel with an evidence-picker action, and a full-width journal view the player can close to return to the same room. |

### Screenshots opened and inspected

| Screenshot | What is visible |
| --- | --- |
| 1280×720 | Five targets, legend near the lower edge, the table observation and Thomas in the same viewport. |
| 1440×900 | The 1000×562 scene remains dominant. The short side note leaves substantial spare space below the character name. |
| 1920×1080 | 240 px side gutters and a large empty lower margin surround the capped scene. |
| 1024×768 | Full scene and legend fit. Hotspot labels are small and the narrow note wraps the table description onto three lines. |
| 200% initial view | Browser-native zoom from 1280×720 gives a 640×360 CSS viewport. Header and upper scene fill the screen. Observation is below it. |
| 200% scrolled to feedback | The same observation and Thomas's name read cleanly after scrolling. Only the bottom strip of the scene remains visible. |
| 7 s into an action | The cabin targets are dim and the adjacent note reads “Action in progress…”. |
| Rejected dialogue save | All Mess Hall targets dim. The size-limit explanation and Retry replace the observation. The displayed turn remains 359. |

## Evidence and limits

Review scripts, logs and raw observations are in this temporary review folder. The repository was read-only for this review. Chrome 158.0.8127.89 ran the standard screenshots and gameplay. Native 200% zoom used Chrome for Testing's `chrome.tabs.setZoom`, confirmed by the browser's zoom factor, halved CSS viewport and doubled device pixel ratio. Startup, delay and fake-dialogue tests used isolated processes and free ports. No production LLM, real Hugging Face deployment, final artwork, future dialogue UI, screen reader, touch device or other browser engine was exercised. The existing project's test-suite count was the author's result. This review used independently written tests.

Edge results · Browser actions and restart · Storage and no-lock fallback · Dialogue sizes · Delay and boundary recovery · HTTP timings and launch variants · 20 browser timings · Key and telemetry checks · Layout measurements · Image integration probe

