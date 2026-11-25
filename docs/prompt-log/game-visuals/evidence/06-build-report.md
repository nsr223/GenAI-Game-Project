> Worker report as delivered; links to local files removed.

# Player UI foundation verification

All 11 checks passed. Browser runs used Chrome 158.0.8127.89. The zoom run used Chrome for Testing with native tab zoom. Delay, save-limit and fake-dialogue fixtures ran outside the delivery code.

| Check | Observed result |
| --- | --- |
| 1. Gradio launch and analytics | `python -m frontend.server` served the player page and returned HTTP 200 from `/config`. A fresh save opened Your cabin at turn 0. The Crew Quarters exit advanced to turn 1. The process had analytics disabled at the first Gradio import, even with analytics enabled in the parent environment. The socket audit recorded two loopback connects and zero external lookups or connects. Browser observations · Socket audit |
| 2. Save growth | Chrome submitted 400 exchanges with one NPC and 400 across six, using exactly 60 words for each message and fake reply. All 800 responses produced browser-storable saves. Peak token sizes were **16,288 B** and **73,988 B** against the 131,072 B cap. Every active NPC retained its latest 60 messages. Compared with untrimmed runs, evidence, claims, flags and the rest of the investigation state matched. The EV-11 gate opened in both runs. Measurements |
| 3. Save-limit recovery | Forced a save-limit error on Desk at turn 0. **Return to investigation** restored the room controls, and Crew Quarters opened at turn 1 on the same page. The rejected action left the previous token intact. Rejection · Next move |
| 4. Storage | Chrome's site-data block raised `SecurityError`. The message told the player to allow storage. Filling the localStorage quota with 5,242,094 padding characters caused a distinct full-storage message. Session-only play completed three moves in each case and kept **Saving is off** visible. The full-storage case reached turn 6 in memory and preserved its turn-3 persistent token. Browser observations |
| 5. Signing key | Missing key showed the temporary-save notice once. After dismissal, a move, a reload and a second tab kept it hidden and preserved the room. A configured key showed no notice. The weak-key process exited with status 1 and a validation message that omitted the supplied value. Browser observations |
| 6. Plain HTTP tabs | The non-loopback hostname had no secure context or Web Locks. In **10/10** trials with a 3 s delayed Desk action, the second tab opened read-only and became writable only after **Take over**. Five takeovers during the delay preserved the new owner's move when the delayed response returned. Five takeovers after acknowledgment kept both the Desk action and the move. Both tabs converged on the same token in every trial, and reload preserved it. Ten runs |
| 7. Long actions | The 15 s Desk inspection displayed elapsed time at about 2.03 s. It advanced in one-second increments through 15 s with a maximum gap of about 1.01 s. The reduced-motion browser reported zero active animations. The Desk observation appeared when the action completed. Timing · Desk timer |
| 8. 200% zoom | Native 200% zoom turned 1280×720 into a 640×360 CSS viewport. Busy text and each of the four Mess Hall results remained fully onscreen from the click position, with **0 px** scroll change after each click. Coordinates and text |
| 9. Art | With a solid pink room image, **98.05–99.27%** of each hit area matched the unobstructed image. With the supplied Mess Hall WebP, **97.49–98.79%** matched. Both trials registered **20/20** pointer clicks two pixels inside hotspot edges. Keyboard focus drew a **3 px** outline around the full hit area. Pixel measurements |
| 10. Regressions | **388/388** hotspot edge clicks hit their intended targets across 97 targets and 23 rooms. Forty held-Enter keydowns produced one inspect request. Reload and a new tab resumed the same save. With Web Locks, 20 alternating actions ended at turn 24 with matching tokens throughout. A direct Wet Laboratory move from Mess Hall was refused. All four bad tokens were retained until explicit reset. Edge audit · Browser regressions |
| 11. Tests and console | **117 tests passed**, including save growth, save-limit rollback and startup key cases. Browser error and warning counts were zero across the runs. Test run |

## Screenshots inspected

| Check | What the frame shows |
| --- | --- |
| 3 | The save-size message and **Return to investigation** appear beside the dimmed cabin controls. The following frame shows active Crew Quarters exits and the move acknowledgment at turn 1. Limit · Recovered |
| 4 | The blocked-storage screen offers to enable storage or continue. The full-storage screen identifies the quota problem on the existing Mess Hall save. The session frames show the persistent **Saving is off** note above the active room observation at turns 3 and 6. Blocked · Blocked session · Full · Full session |
| 6 | The second tab shows dimmed cabin hotspots, the open-elsewhere message and **Take over**. After takeover the new owner reaches Crew Quarters at turn 1 with active exits. Read-only · Takeover |
| 7 | The Desk hotspot shows **Working… 2 s** while the sidebar shows **Action in progress…**. Elapsed |
| 8 | Each frame shows its observation above the scene and the clicked object in view. The table and coffee frames retain the scroll position used to reach the lower objects. Galley · Noticeboard · Table · Coffee |
| 9 | The solid image and the supplied room image remain visible throughout the targets, with 20 px markers at their centers. The focus frames show the yellow outline around the full table target. The supplied artwork was loaded through the fixture layout, so marker alignment follows the placeholder coordinates. Solid · Solid focus · Room image · Room focus |

## Files changed

- `frontend/server.py` and `frontend/saves.py` configure Gradio startup, publish temporary-save metadata and cap serialized conversation history.
- `frontend/static/player.js` and `frontend/static/save-slot.js` handle recovery, elapsed status and IndexedDB ownership and save commits without Web Locks.
- `frontend/static/index.html`, `frontend/static/scene.css` and `frontend/static/scene.js` render the notices, sticky narrow-screen observation and transparent art hotspots.
- `tests/test_frontend_route.py` and `tests/test_frontend_saves.py` cover the launcher credentials, save-limit rollback and long fake conversations.

## Coverage limits

Firefox, Safari, touch devices, screen readers, a hosted deployment, browser or OS crash recovery, and a live LLM were outside the run. The art checks used a solid fixture and the existing Mess Hall WebP. Production room art and its final hotspot placement belong to the art integration task.
