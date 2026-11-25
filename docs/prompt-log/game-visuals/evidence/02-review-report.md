> Worker report as delivered; links to local files removed.

# Independent hotspot spike review

**Keep the method with changes.** Use a native button across the full hotspot shape, accept one action per physical activation, show a pending state and disable ready-looking controls until the request completes, serialize actions per game so one game can’t stall another, and restore server-side game state on reload. Keep engine validation and the live revision check. Decide explicitly whether a second tab resumes an existing game or starts a different game. The resize duplicate reproduced in the screenshot pipeline, including on plain HTML.

Independent Playwright checks ran against Gradio 6.32.0 in headless Chrome 158.0.8127.36 on macOS. The unmodified spike and the two fixtures ran on separate loopback ports 52593, 52594 and 52595. The fixture changes lived in separate server processes. The repository and port 7870 were outside the test setup.

## Part A — Repeat checks

| Check | Smallest reproduction | Observed | Result |
| --- | --- | --- | --- |
| A2 · Inspect | Open Mess Hall and click **Mess table**. | Turn 3 → 4, revision 0 → 1. “The bolted-down communal table where everyone eats and talks.” | Holds |
| A4 · Navigate and reuse | With Mess Hall at turn 4, click **Main corridor**, then the newly rendered **Mess Hall** exit. | Main corridor had 8 buttons at turn 5. Returned to Mess Hall at turn 6. | Holds |
| A5 · Locked room | Enter Main corridor and click **Wet Laboratory**. | At turn 7 in the sequence, the click advanced to turn 8 and stayed in `main_corridor`. “The captain has secured the wet lab. Nobody goes in without her authorization.” | Holds |
| A7 · Separate sessions | Open independent browser contexts. In A, move to Main corridor and then Dry Laboratory. In B, inspect Mess table and then Coffee station. Interleave actions and read both tabs again. | Distinct Gradio session IDs. A stayed in Dry Laboratory at turn 5, B stayed in Mess Hall at turn 5 with the Coffee station result. | Holds |
| A8 · Forged target in page | In fresh Mess Hall, change the Main corridor button’s target ID to the Wet Laboratory ID and activate it. | Current revision 0 reached the handler. “You can't get to Wet Laboratory directly from here.” Mess Hall stayed open and ticked to turn 4. | Holds |
| A8 · Direct server request | Start a throwaway game via HTTP alone, inspect once, then submit the same out-of-room exit with the current revision 1 through the Gradio queue. Read the completion stream. | Direct submission was possible. Both HTTP stages returned 200 and Gradio completed the call. The engine returned the same refusal, stayed in Mess Hall and advanced turn 4 → 5 and revision 1 → 2. The listener’s private API visibility therefore allows the UI’s queue route to receive the request. | Holds for the engine access check |
| A9 · Escaping | In a fixture with an image-tag string as the Mess table display name, load Mess Hall and activate that label. | The string rendered literally before and after inspection, scene image count stayed 0 and `typeof window.pwned` stayed `undefined`. The click advanced to turn 4. | Holds |

## Part B — Player-impact order

| Check | Smallest reproduction | Observed | Result |
| --- | --- | --- | --- |
| B5 · Reload and second tab | Move **Main corridor → Dry Laboratory** and open the same URL in a second tab in the same browser context. Reload the first tab. | Original tab stayed at Dry Laboratory, turn 5, revision 2, until reload. The new tab and subsequently the reloaded original both showed fresh Mess Hall, turn 3, revision 0. All three loads used different Gradio session IDs. | **Defect for resumable play** |
| B4 · Invisible pending state and dropped input | Delay Mess table inspection by 3 seconds in the fixture. Click **Mess table**, then **Coffee station** and **Main corridor** while the first click runs. Click **Coffee station** from a second session during that same delay. | The old scene and arrival message stayed visible. Buttons were enabled, used the pointer cursor and received trusted clicks. The progress tracker had zero height and opacity 0. The original tab sent just Mess table and ended in Mess Hall at turn 4. Both later clicks disappeared before the network. The second session sent its request and rendered its fast response after 2.67 s while the first action took 3.01 s. One listener-wide concurrency slot serialized the two sessions. | **Defect** |
| B2 · Shape hit area | In 1280×720 Mess Hall, click inside the table panel at viewport x=179, y=212, then click its white button. | The panel click sent no request and left turn 3 and the arrival message visible. The label click reached turn 4. A 150×150 hit-test grid per shape measured clickable areas of 7.0% for Mess table, 8.9% Galley counter, 7.8% Noticeboard, 8.7% Coffee station, 10.8% Thomas Blake and 8.2% Main corridor. The delegated handler recognizes only the nested button. | **Defect** |
| B1 · Held Enter | Focus **Mess table** and hold Enter for 2 seconds with a 500 ms repeat onset and 30 repeats/s, reproduced with Playwright keyboard events. | 46 trusted button clicks, all with detail 0, and 46 requests. Turn 3 → 49 in three validation runs. At 15 repeats/s, turn 3 → 26. A key-down/key-up control without repeat reached turn 4. The click guard only checks nonzero detail. | **Defect** |
| B3 · Same hotspot at 350 ms and 500 ms | From fresh Mess Hall, click **Mess table** twice with each gap. Also repeat with Chrome reporting the second click as part of a double-click. | Both clicks advanced turns 3 → 5 in all five trials at each gap. The trusted double-click controls logged Chrome’s `dblclick` at gaps of 352 ms and 510 ms, and each still ran both inspections. The 100 ms control ran one. The guard uses a fixed 300 ms window. | **Defect when intended as a double-click** |
| B3 · Same hotspot at 1,000 ms | Click **Mess table** twice about a second apart. | Two requests and turn 3 → 5 in 5/5 trials, with a measured gap of 1,009–1,013 ms. | Holds |
| B3 · Different hotspots at 50 ms | Click **Mess table**, then **Coffee station**, with a 50 ms target interval. | Both ran in order in 5/5 local trials, at 54–58 ms measured gaps. Turn 3 → 5 and the Coffee station message was last. Overlap during a pending request is covered by B4. | Holds with a fast response |
| B6 · Extra scene in a resize capture | Cycle 1280×720 → 1440×900 → 800×600 → 1280×720 and capture immediately after each resize for 20 iterations. Repeat while navigating between Mess Hall and Main corridor. | The extra heading and top of the scene appeared in 4/20 idle captures and 0/20 navigation captures. Each affected image’s bottom 87 rows were a pixel-for-pixel repeat of its top 87. The DOM and mutation trace showed one scene. Plain HTML reproduced the same 87-row tile in 10/20 clipped CDP captures, and standard Playwright screenshots of the spike reproduced it in 6/20 controls. Unclipped CDP captures were 87 pixels shorter than requested. A capture after a 120 ms wait showed the complete viewport in the paired control. The evidence attributes the duplicate to immediate Chrome capture during viewport resizing. | **Defect in the capture path.** Scene count holds. |
| B7 · Browser data | Capture the DOM, Gradio config, and network on load and after **Mess table → Main corridor → Dry Laboratory → Experiment index**. | No matches for the 19 engine flag names, sampled internal-state field names, or the names and summaries of the 9 uncollected evidence entries. Each of the five completed SSE responses delivered a null state output plus scene markup. The only matching solution-related string was Maya’s name and corresponding NPC button ID once she was visibly present in Dry Laboratory. | Holds for the captured scenes and payloads |
| B8 · Console | Record browser warnings, errors and unhandled page errors throughout the cases, including delay and resize controls. | Zero console warnings, errors or page errors. Network monitoring recorded `ERR_ABORTED` on queue SSE after completions and on a heartbeat during reload or teardown. The captured queue completions arrived and no case saw an HTTP error. | Holds |

The visible busy state and per-game serialization should be designed together. With a busy indicator, disable activation until the scene can accept input again and keep focus usable. Suppress Enter auto-repeat while preserving ordinary keyboard activation. Use the browser’s double-click signal or an explicit input policy that handles the tested gaps. Server-side persistence should retain the current location, turn and investigation state under a stable game identity.

## Screenshots opened and verified

| Case | Full path | Visible result |
| --- | --- | --- |
| B5 before | B5-before-reload.png | Dry Laboratory, turn 5, with its hotspots and arrival message. |
| B5 after | B5-after-reload.png | Same tab after reload shows the opening Mess Hall, turn 3. |
| B4 pending | B4-pending-no-feedback.png | Mid-request, the screen still shows turn 3, the arrival message and ordinary-looking buttons. |
| B4 finished | B4-lost-clicks.png | Only the table inspection is shown, at turn 4. Main corridor never opens. |
| B2 blank click | B2-blank-shape-click.png | The large top-left table panel surrounds a small white button. Clicking to its left inside the panel left turn 3 and the arrival message on screen. |
| B1 held Enter | B1-hold-30hz.png | The table button still has the yellow keyboard focus ring. The counter reads turn 49. |
| B3 350 ms pair | B3-repeat-350ms.png | Same table inspection result at turn 5. |
| B6 800×600 | idle-02-800x600.png | The first scene and arrival message are complete. A second Mess Hall heading and the top of its dark panel are visible in the last 87 rows. |
| B6 1280×720 | idle-09-1280x720.png | The first scene ends abruptly. The duplicate heading starts in the repeated top strip below it. |
| B6 static control | static-clip-1-1440x900.png | A plain HTML heading and dark panel repeat in the last 87 rows. |
| B6 settled control | static-clip-1-1440x900-settled.png | The same page has one heading, one panel and its ending caption. |

Both resize contact sheets were opened. 20 idle captures · 20 navigation captures

## Reproducibility and coverage limits

The independent scripts are interaction checks, keyboard repeat, confirmation checks, resize and browser data, and resize controls. Their underlying observations are in interaction results, keyboard results, confirmation results, resize measurements, resize control results, and browser data results. The direct HTTP response is saved in HTTP-only results.

To rerun, use the repository’s `.venv/bin/python`, include the repo root and tools in `PYTHONPATH`, and set `PYTHONDONTWRITEBYTECODE=1`. Start serve.py separately with `baseline`, `delay` and `escaping`. Set `HOTSPOT_REVIEW_BASE`, `HOTSPOT_REVIEW_SLOW` and `HOTSPOT_REVIEW_ESC` to the three printed loopback URLs.

Other browser engines, a physical keyboard’s OS repeat settings, visible-window drag resizing, touch, screen readers, remote latency and unvisited game branches were outside the run. The earlier anomalous screenshot was unavailable for a direct comparison. The review covered the supplied spike and its routes, with no assessment of unimplemented UI flows.
