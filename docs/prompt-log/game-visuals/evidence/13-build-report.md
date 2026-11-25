> Worker report as delivered; links to local files removed. Contains the solution path.

# Presenting the case to Captain Morgan

The click-only investigation ended on turn 55 at both viewport sizes. Unsupported accusations left the player on the bridge with the same reaction for every suspect. The engine’s alternate failure policy closed the case on turn 5.

## Acceptance checks

| Check | Observed at 1280×720 and 1440×900 |
|---|---|
| 1 · Worked examples | Four moves reached Sarah. Thomas at turn 4 and Maya at turn 5 each sent one accusation and received identical wording. The signed full-chain fixture ended at 55 with 10 entries and 1 statement. Reload sent one resume and added zero turns. 1280 · 1440 |
| 2 · Fairness | 480 browser submissions, 20 per suspect per evidence state per size. The 440 failures produced one screenshot hash per viewport and one identical 137-byte JSON body after removing the save. Fixtures shared the bridge and turn number. Their notebooks contained 1 and 10 entries respectively. All 40 supported Maya submissions ended the game. |
| 3 · Alternate rule | With continuation disabled in a test content copy, Sarah recorded an inconclusive account. Reload restored the same text, 5 turns, 1 entry and 0 statements. |
| 4 · Refusals | Absent captain, unknown person and client-supplied verdict each returned only the generic action error. Altering the signed payload returned the save error. No refusal supplied a replacement save. |
| 5 · Races | Two tabs queued confirmations while the save lock was held. Repeated Enter and double activation produced one accusation request total and turn 5 in both tabs. |
| 6 · Closed game | Only Read the journal and New investigation appeared. Opening an unread entry preserved the exact token. Direct attempts at all six mutation endpoints/actions returned the closed response. |
| 7 · Sarah | “Accuse Capt. Sarah Morgan?” identifies her unambiguously. Her reaction says “Sarah hears you out, then asks for corroboration. She won't record an accusation she can't support.” The engine gives her no self-accusation response. |
| 8 · Walkthrough | 100 clicks, 55 turns, 10 entries, 1 statement. The fake model supplied the voice. Each run scanned 315 page, storage and network samples for private markers. Every click at 1280 · 1440 |
| 9 · Restart | Cancelling kept the signed save. Confirming sent one new-game request. Both tabs returned to Your cabin at turn 0, with Elena’s warning, the engine’s opening lead and no statements. |
| 10 · Access | Keyboard reached all six radio choices through arrow keys. Focus returned to the journal link and to Continue after cancellation. The reaction was focused and exposed as a status. Native 200% zoom gave 640×360 and 720×450 CSS pixels with zero horizontal overflow. Session-only restart worked. The fallback read-only tab followed the owner from turn 5 to 0. 1280 · 1440 |
| 11 · Regression | 140 tests passed with Playwright. Without it, 135 passed and five browser cases skipped. Both viewport runs exercised 388 hotspot edges across 23 rooms, dialogue, notebook review races, focus and save recovery. Final browser logs contained zero warnings or errors. Suite · Optional-browser suite |

### Median HTTP time in milliseconds

Browser request start to last response byte on loopback, randomized order. Each cell reports 20 runs. “Opening” uses the opening notebook at the matched turn. These timings describe this machine. 1280 samples · 1440 samples

| Person | 1280 opening | 1280 full | 1440 opening | 1440 full |
|---|---:|---:|---:|---:|
| Daniel Reyes | 1.55 | 1.65 | 1.62 | 1.80 |
| Lucas Weber | 1.55 | 1.64 | 1.66 | 1.87 |
| Dr. Maya Chen | 1.56 | 1.61 | 1.74 | 1.70 |
| Olivia Hart | 1.47 | 1.76 | 2.03 | 1.72 |
| Capt. Sarah Morgan | 1.50 | 1.71 | 1.55 | 1.73 |
| Thomas Blake | 1.41 | 1.66 | 1.66 | 1.88 |

## Click-only route

Each review opened Journal → Evidence → named entry → Close journal. Each topic used Topics, then its displayed choice. Leave closed the conversation before moving.

1. Cabin → Crew Quarters → Main corridor → Upper stairs → Bridge. Speak to Sarah. Request engineering records, medical comparison, supervised wet lab inspection, shared project records and Elena’s cabin search.
2. Upper stairs → Main corridor → Lower stairs → Lower corridor → Engineering Workshop. Inspect Maintenance terminal. Return via Lower corridor → Lower stairs → Main corridor → Medical Bay.
3. Ask Olivia about her initial observations. Review Apparatus cycle log and Olivia’s preliminary observations. Ask her to compare the injury with the apparatus record.
4. Main corridor → Wet Laboratory. Inspect Calibration station. Main corridor → Medical Bay. Ask Olivia to compare the injury with the calibration observation. Review Injury and object comparison.
5. Main corridor → Dry Laboratory. Inspect Shared workstation. Main corridor → Crew Quarters → Elena’s cabin. Inspect Desk. Review Draft transfer agreement and Elena’s preserved notes.
6. Crew Quarters → Main corridor → Dry Laboratory. Ask Maya where she was last night. Main corridor → Editing Room. Ask Lucas for recordings, leave and inspect Editing workstation.
7. Main corridor → Dry Laboratory. Show Maya the partial corridor recording. Review Maya’s contradictory statement. Main corridor → Upper stairs → Bridge. Sarah → Present your case → Dr. Maya Chen → Continue → Confirm.

Olivia’s comparison gains an explicit lead after two reviews. A player has no equivalent signal that reading an already collected agreement or statement advances the case. Revisiting Maya with footage requires inference.

## Screenshots and assessment

Opened both sizes. The summary gives the notebook and suspect list separate space. Long evidence lists require scrolling and the last visible line is clipped at 720px height. Confirmation keeps the chosen name above the fold. The reaction stays with Sarah’s silhouette. Both endings leave generous space around the text and counts.

| Screen | 1280 | 1440 |
|---|---|---|
| Case summary | View | View |
| Confirmation | View | View |
| Reaction | View | View |
| Inconclusive | View | View |
| Substantiated | View | View |

Tension **7/10**. The named confirmation gives the accusation weight, though repeat refusals feel mechanical. Fairness **9/10**. Equal failed responses protect against guessing, while review gates can be obscure. Clarity **9/10**. The confirmation states the turn cost and risk of closure. Dialogue fit **8/10**. Sarah’s restraint suits the scene, including when accused herself, though her wording never acknowledges that distinction.

**Files changed.** `frontend/{server,journal,saves}.py`, `frontend/static/{player,dialogue,journal,case}.js`, `frontend/static/{index.html,case.css}` and `tests/test_frontend_accusation.py`. Evidence is in the locally Git-excluded `course/` directory.

**Limits.** Engine actions after closure consume turns, so the adapter refuses them before invoking the engine. Signed saves remain inspectable and replayable. New saves omit the private verdict on previous guesses. A valid signed action can also be submitted directly. Screen-reader speech, other browser engines and real model responses were untested. All verification browsers and servers were closed.
