# Task: independently review the hotspot spike

## Goal and why
Another agent built `frontend/spike_hotspots.py` and reported that all 12 checks passed. We will base the player UI on this method, so find what its author missed. A confirmed defect is the most useful result; report "holds" only for what you observed yourself.

## Context
- Read `AGENTS.md`, `docs/summaries/frontend.md` and `frontend/spike_hotspots.py`. The original checks are in `/tmp/beneath-hotspots.YzVsSwb2/report.md`.
- Use `.venv/bin/python` (Gradio 6.32.0). Playwright is available with `PYTHONPATH=/tmp/beneath-hotspots.YzVsSwb2/tools`.
- Start your own server on a free port (import `demo` and launch it, or use a small launcher in your temporary folder). Port 7870 may be in use by someone else; leave it alone.

## Constraints
- The repository is read-only for you: put scripts, screenshots and the report in a new temporary folder.
- Write your own tests instead of rerunning the author's script.

## Part A: repeat with your own test
Checks 2, 4, 5, 7, 8 and 9 from the report. For 8, also send the forged action to the Gradio server directly, outside the page, with a current revision, and report whether that is possible.

## Part B: likely gaps
For each, give the steps, the observed value, and holds / defect / not tested.
1. Hold Enter on a focused object hotspot for 2 seconds: how far does the turn rise?
2. Click inside a shape but outside its label: does anything happen? What share of the shape's area is clickable?
3. Two clicks on the same hotspot 350 ms, 500 ms and 1000 ms apart; two clicks on different hotspots 50 ms apart.
4. Add a 3-second delay to one action in a test copy: what can the player see or click meanwhile, and are other clicks lost?
5. Reload the page mid-game, and open the same game in a second tab: which state does each show?
6. The report mentions a capture after resizing that showed part of a second scene. Resize 20 times between 1280×720, 1440×900 and 800×600 and capture immediately each time. Is it ever visible, and what causes it?
7. Read what the browser receives on load and after a click (DOM, config, network). Is there any engine flag, evidence text not yet collected, or solution term?
8. Browser console errors or warnings during all of this.

## Return
- A table for parts A and B, defects ordered by effect on the player, each with the smallest reproduction.
- Screenshots for visible defects: full path, opened, and described.
- One recommendation: keep the method, keep it with named changes, or replace it.
- What you could not test.
