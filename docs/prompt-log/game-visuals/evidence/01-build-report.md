> Worker report as delivered; links to local files removed.

# Gradio 6 scene hotspot spike

**Use this method.** Delegated `gr.HTML` custom events reached Python and redrew the scene on Gradio 6.32.0. Keep the engine-owned session state, duplicate-click guard, and explicit focus handling. Gradio can reuse a focused button node for a different hotspot on navigation. The final code moves focus to the new room heading when the scene revision changes.

All 12 checks passed. Run `source .venv/bin/activate` followed by `python -m frontend.spike_hotspots` and open port 7870. The only repository change is the uncommitted `frontend/spike_hotspots.py`. The test-only fixture server was stopped.

| # | Check | Result | Observed |
|---|---|---|---|
| 1 | Initial hotspots | Pass | Mess Hall at turn 3. Exactly six buttons for Mess table, Galley counter, Noticeboard, Coffee station, Thomas Blake, and Main corridor. |
| 2 | Inspect mess table | Pass | Turn 3 → 4. “The bolted-down communal table where everyone eats and talks.” |
| 3 | Select Thomas | Pass | “Thomas Blake — Investor representative.” Turn stayed at 4. |
| 4 | Navigate and use a new hotspot | Pass | Main corridor at turn 5 with eight exits. Its Mess Hall button returned to Mess Hall at turn 6. |
| 5 | Locked Wet Laboratory | Pass | Still in `main_corridor` at turn 8. “The captain has secured the wet lab. Nobody goes in without her authorization.” |
| 6 | Rapid double-click | Pass | Two trusted pointer clicks on the same button. Turn 3 → 4 and still 4 after one second. |
| 7 | Separate browser sessions | Pass | Independent Chrome contexts. A moved from Main corridor at turn 8 to Dry Laboratory at turn 9. B stayed in Mess Hall and independently moved from turn 4 to 5. Both were rechecked after the other acted. |
| 8 | Forged Wet Laboratory target | Pass | Changed the exit ID in the local test tab and sent the normal custom event. The engine replied “You can't get to Wet Laboratory directly from here.” Location stayed `mess_hall`. |
| 9 | Display-name escaping | Pass | The supplied image-tag string rendered literally before and after an inspection. Zero image elements were created and `typeof window.pwned` was `undefined`. |
| 10 | Tab and Enter | Pass | All six Mess Hall and all eight Main corridor hotspots received focus via Tab and activated via Enter. Focus moved to the room heading on navigation. |
| 11 | Responsive alignment | Pass | All 14 button centers remained inside their shapes at 1440×900, within 0.01 CSS px of shape center. The scene grew from approximately 1045×588 to 1192×671 CSS px and stayed 16:9. |
| 12 | Existing test suite | Pass | 104 passed under Python 3.12.15 and Gradio 6.32.0. |

Ten local object clicks in Chrome measured from the pointer event to the updated DOM revision. Median **35.8 ms**, slowest **51.4 ms**. Samples in ms were 51.4, 35.8, 35.7, 37.4, 34.5, 34.6, 39.0, 34.7, 38.5, and 34.3.

Opened all four final screenshots.

- 01-mess-hall.png shows turn 3, four rounded object shapes, Thomas in an oval, the exit in a green panel, and the arrival message. The heading and message start to the left of the inset scene.
- 04-main-corridor.png shows turn 5, eight exit buttons in two rows, and the arrival message. The brown Wet Laboratory panel distinguishes it by color before the click.
- 05-wet-lab-locked.png shows the same corridor at turn 8 with the full engine refusal visible below.
- 11-mess-hall-1440x900.png shows the same six buttons centered on their larger shapes with space beneath the scene and no clipping. An earlier capture made immediately after resize showed part of a second scene at the bottom. The final capture did not reproduce it.

The acceptance run used Playwright with headless Chrome 158.0.8127.36. Orca's resized viewport misrouted automated pointer coordinates during the initial smoke test. The final run covered every requested check. Other browser engines, touch, screen readers, and remote latency were outside that run.
