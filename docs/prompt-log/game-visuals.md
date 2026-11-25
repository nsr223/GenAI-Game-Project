# Prompt log: game and visuals (`feature/game-visuals`)

Sessions for the player UI and the visual style, 2026-11-24. Owner: Erik Söhner. Agent: Codex workers on the named model; whoever builds never reviews its own work. Each prompt is stored word for word. Image prompts have their own versions in [`prompts/assets/`](../../prompts/assets/CHANGELOG.md), with every version's image next to it.

**Shared structure:** goal and why, context, what to build, constraints, pass/fail checks written before the run, what to return. Prompts 1–7 are zero-shot: no worked examples; prompt 7 adds reference images. Prompt 8 compares three techniques.

## UI series

### 1. [Hotspot spike](game-visuals/01-hotspot-spike.md) · gpt-6.2-sol
- **Purpose:** test the riskiest unknown first, in throwaway code.
- **Technique:** zero-shot; 12 measurable checks; permission to report "no".
- **Result:** 12 of 12 passed; 10 clicks, median 35.8 ms, slowest 51.4 ms ([report](game-visuals/evidence/01-build-report.md), [image](game-visuals/img/01-spike.webp)).
- **Failure observed:** reading the code and screenshots showed that only the label was clickable and held keys were unguarded. The checks could not catch either.
- **Change, and why:** a second prompt that attacks those gaps, because a builder's own checks share its blind spots.

### 2. [Independent review](game-visuals/02-hotspot-review.md) · gpt-6.2-sol, new session
- **Technique:** zero-shot; adversarial reviewer who writes its own tests; named suspicions.
- **Result:** clickable area 7–11% of a shape; 46 actions while Enter was held for 2 s; reload returned to the start; two later clicks lost during a 3 s action; another session waited 2.67 s ([report](game-visuals/evidence/02-review-report.md)).
- **Change, and why:** all became checks in prompt 4. A scratch prototype on `gr.Server` with our own frontend (one run) avoided them, so the approach changed too.

### 4. [UI foundation](game-visuals/04-ui-foundation.md) · gpt-6.2-astra
- **Technique:** zero-shot; 13 checks, most taken from observed failures.
- **Result:** 13 of 13 passed at two screen sizes, 970 hotspot clicks, 113 tests ([report](game-visuals/evidence/04-build-report.md), [image](game-visuals/img/04-ui.webp)).
- **Question answered:** plan approved; verify the signature before unpacking, keep working without Web Locks, show a busy state in the second tab.
- **Failure observed:** it looked like a document, and it started outside Gradio's `launch()`.

### 5. [UI review](game-visuals/05-ui-review.md) · gpt-6.2-astra, new session
- **Technique:** adversarial reviewer plus a scored visual rubric, where anything below 7 needs a specific change.
- **Result:** accept with fixes; seven ranked defects; visual scores from 4 to 8 of 10; `launch()` returned error 500 on the first action; dialogue stopped at exchange 357 ([report](game-visuals/evidence/05-review-report.md)). One usage limit interrupted the run.
- **Change, and why:** prompt 6 fixes behaviour only, so a later restyle cannot hide a behaviour change.

### 6. [UI fixes](game-visuals/06-ui-fixes.md) · gpt-6.2-sol
- **Technique:** zero-shot; one check per reviewed defect, plus a regression check.
- **Result:** 11 of 11 passed; 800 fake exchanges saved; 10 of 10 two-tab trials lost nothing; 117 tests ([report](game-visuals/evidence/06-build-report.md), [image](game-visuals/img/06-ui.webp)). A separate browser run by the coordinator confirmed start, movement, edge click, held Enter, reload, second tab and locked room.
- **Open:** other browsers, touch, screen readers, hosting and a live model.

## Visual series

### 3. [Three visual directions](game-visuals/03-visual-style.md) · gpt-6.2-astra + imagegen
- **Technique:** zero-shot; one variable at a time (technique), with room, person and dialogue text held constant.
- **Result:** gouache, ink and wash, cut paper; 14 images ([comparison](game-visuals/img/03-styles.webp), [versions](../../prompts/assets/style/CHANGELOG.md)). The team chose ink and wash.
- **Question answered:** plan approved; report where a technique weakens the face.
- **Failure observed:** the worker passed a coffee trolley on wheels, against canon. Its own image prompt had asked for a "coffee cart".
- **Change, and why:** prompt 7 lists every visible flaw as a required change instead of a general check.

### 7. [Style lock](game-visuals/07-style-lock.md) · gpt-6.2-astra + imagegen
- **Technique:** zero-shot with reference images; transfer test on a second room and person.
- **Result:** six images; trolley, rust, loose dishes and table fixed ([mess hall](game-visuals/img/07-mess-hall.webp), [bridge](game-visuals/img/07-bridge.webp), [report](game-visuals/evidence/07-build-report.md)).
- **Failure observed:** too dark and cold (mean luminance 0.31 in the chosen option, 0.09 now), and rooms and people look alike.
- **Cause in the prompt:** it required one camera and light rule for everything; finished images were references for the next subject; layout was repeated in words; the check asked whether images match, never whether they differ.
- **Change, and why:** prompt 8 separates a short constant block from individual identities and measures difference.

### 8. Visual identities: zero-shot, few-shot and chain-of-thought compared · gpt-6.2-sol
- **Purpose:** prompt 7 made rooms and people look alike. Find out in text, before drawing, which technique gives the most distinct identities for 8 rooms and 6 people.
- **Prompts:** [A zero-shot](game-visuals/08-identities/A-zero-shot.md), [B few-shot](game-visuals/08-identities/B-few-shot.md) (A plus two examples from a night train), [C chain-of-thought](game-visuals/08-identities/C-chain-of-thought.md) (A plus draft, compare pairs, revise). Same context, [schema](game-visuals/08-identities/schema.json), model and reasoning effort (medium); no files visible to the model; three fresh runs each.
- **Planned measure:** pairs that differ on at least 4 of 8 axes. **It could not tell the prompts apart:** all nine runs scored 28 of 28 room pairs and 15 of 15 people pairs. The axes were chosen by the model itself and were too easy to vary.
- **Stricter counts** (added afterwards): room pairs differing on at least 6 axes, per run: A 27, 27, 28; B 27, 26, 25; C 28, 28, 28. Differences this small with three runs prove nothing.
- **Anonymised reading, one judge, ranking written before the key was opened:** C 1st, 2nd and 4th; B 3rd, 5th and 6th; A 7th, 8th and 9th ([ranking](game-visuals/08-identities/blind-judgement.txt), [key](game-visuals/08-identities/key.json)). Limits: one judge, and the opening and last lines of the run ranked 9th (A1) had been seen in a technical test.
- **Failure observed:** within a set everything differs, but the nine sets are nearly the same set. The same subject shares 69% (rooms) and 59% (people) of its axes across runs. Teal hoses in the wet lab, mugs on a round or oval mess table, and a stubbled, stocky Daniel wiping grease appear in 9 of 9; a silver-haired Thomas in 7 of 9; a sage or scrubs Olivia in 9 of 9. Mugs stand loose in a gale in 9 of 9, the same canon error as in the first images.
- **Cause in the prompt:** it gave each subject a job and manner only, so the model filled in its default picture of that job. Daniel's "grease-stained" in the context explains part of his case. No technique can add what the prompt does not contain.
- **Change, and why:** keep chain-of-thought, name these defaults as used up, and anchor every identity in details specific to the bibles, because distinct from each other is not the same as distinct from the cliché.
- **Evidence:** [all nine outputs](game-visuals/08-identities/runs/), [measurement script](game-visuals/08-identities/measure.py).

### 8, version 2: [chain-of-thought v2](game-visuals/08-identities/D-chain-of-thought-v2.md) · gpt-6.2-sol
- **Change:** C plus source lines per person, a list of used-up defaults, one habit and one contradiction per person, one trace per room, everything secured for a gale. Several additions at once, so their separate effects are unknown.
- **Measure, fixed before the run:** hits against [35 default patterns](game-visuals/08-identities/defaults.json) found in versions A–C; target at most 2 per set.
- **Result, three runs:** 3, 3 and 7 hits; before, 27–33 in all nine runs. **Target missed.** Reading the hits, several are false: racked mugs are allowed, and "blue" matched note tabs. Real ones left: about 2, 1 and 3. The list was made from A–C, so it favours version 2 by design.
- **Second check:** the same subject shares 53% (rooms) and 46% (people) of its axes across the three runs, against 66% and 53% for C. Pairs differing on at least 6 axes stay at 27–28 of 28 and 15 of 15.
- **Failure observed:** new shared ideas appeared, such as Sarah's long braid in 3 of 3 runs; some follow from the source lines, such as her turned ear in 2 of 3. Run D1 invented details that read as clues: a freshly scrubbed drain in the wet lab and an erratic trace in the dry lab. It also hid most cabin doors.
- **Change, and why:** [the selected draft](game-visuals/08-identities/selected-draft.md) is combined by hand, without those details; people decide the looks, because the model's variety ends where its sources end. The drawing prompt must check clue-like details and reachable exits.

### 9. [Concept sheets](game-visuals/09-concept-sheets.md) · gpt-6.2-astra + imagegen
- **Technique:** detailed zero-shot image prompts from the selected draft; a 34-word constant block; no image references.
- **Result:** four images, two versions per sheet ([sheets](game-visuals/img/09-identities.webp), [prompts and versions](../../prompts/assets/CHANGELOG.md), [report](game-visuals/evidence/09-build-report.md)). Six distinguishable silhouettes, all eight cabin doors visible. The worker reported three misses itself: repeated ceiling lights, loose objects, mess hall luminance 0.333 (limit 0.32).
- **Compared with prompt 7:** rooms and people are clearly different from each other, and the paper white is back. No numbers were taken for this comparison.
- **Failure observed in review:** a steam-age flywheel, an oversized bridge, a sine wave on the dry-lab screen, blotches on walls, light from below on two faces, an unstated age for Maya. The worker passed all of these.
- **Cause in the prompt:** some came straight from the selected draft, which no one had checked against "compact" and "contemporary"; the neutrality check named glances and objects, but not light.
- **Change, and why:** the team comments first; the final prompts state age, size and light for each subject and check them against canon before drawing.

### 10. [Dialogue with suspects](game-visuals/10-dialogue.md) · gpt-6.2-astra
- **Technique:** few-shot; two worked examples with exact expected results, because earlier specifications left turns and event texts open.
- **Result:** 15 of 15 checks passed, 125 tests ([report](game-visuals/evidence/10-build-report.md), [image](game-visuals/img/10-dialogue.webp)). One usage limit interrupted the run; before that, one interim run by the coordinator confirmed both examples ([image](game-visuals/img/10-dialogue-interim.webp)).
- **Own tests by the coordinator, one run each:** forged evidence, an absent person and 501 characters refused; a failing model leaks no key into reply, page or log; a claimed open door stays shut; six 6 s talks took 6 s and 12 s (limit 4) while a move took 0.01 s; leaving and moving was not undone by the late answer; HTML shown as text. All held.
- **Failure observed:** after asking Maya where she was, the player saw "Statement recorded · whereabouts critical window", an internal topic id that hints at the solution. The worker had passed the privacy check.
- **Cause in the prompt:** the check listed engine flags, evidence, prompts and knowledge, but not labels built from event fields. The prompt had asked for notices from `events`.
- **Change, and why:** the notice now says only "Statement recorded", with a test; later prompts name every event field as untrusted for display. Fixed by the coordinator.
- **Open:** real models, real personas (none exist on `dev`), other browsers, touch, screen readers; the talk endpoint has no limit per player, so a public deployment could use up the model quota.

### 11. [Journal](game-visuals/11-journal.md) · gpt-6.2-astra
- **Technique:** few-shot; three worked examples, their data and turns taken from engine runs. Unlike prompt 10, it lists the fields that may be shown instead of the ones that may not.
- **Question answered:** keep the signed browser save; filter every response outside it, including the `events` list that still carried internal topic ids after the fix in entry 10.
- **Result:** code, tests and most browser checks were done when a weekly usage limit stopped the worker; it wrote no report. 132 tests pass, 1 browser test is skipped without Playwright ([entry](game-visuals/img/11-journal.webp), [compare](game-visuals/img/11-compare.webp)).
- **Own tests by the coordinator, one run:** 238 server responses from playing through the reachable ship, scanned outside the save for engine flags, uncollected evidence ids, interaction ids, "TBD" and the internal topic: none found, with 9 evidence entries collected and none empty. Reviewing twice uses one turn and one request; forged review refused; a typed question and a late reply survive opening the journal; console clean.
- **What this shows:** naming what is allowed caught what a list of forbidden things had missed twice.
- **Open:** the worker's own scores, the two-tab and session-only checks in my run, a screen reader, other browsers. It still looks more like a document than an investigator's notebook.

### 12. [Verify and finish the journal](game-visuals/12-journal-finish.md) · gpt-6.2-sol, new session
- **Technique:** zero-shot; independent reviewer who audits the builder's data, invents three attacks and fixes only confirmed failures.
- **Result:** all 14 checks of prompt 11 shown; ten two-tab races with one review each; the gate leads back to Olivia ([report](game-visuals/evidence/12-review-report.md)). 134 tests with Playwright, 132 and two clean skips without. The coordinator reran the suite both ways and the 238-response scan.
- **Failure observed:** following a related entry with the keyboard while a review was saved lost the focus. Found by one of the reviewer's own attacks, not by the 14 checks.
- **Change, and why:** one line gives each link a stable key, with a test that failed before and passes after.
- **What this shows:** the audit marked several of the builder's checks as only partly supported by its data; asking for evidence per check found that, a pass/fail list had not.

### 13. [Accusation, ending and restart](game-visuals/13-accusation.md) · gpt-6.2-astra
- **Technique:** few-shot; two worked examples from engine runs; fairness defined as a measurable comparison instead of a wish.
- **Result:** 11 of 11 checks; 440 failed submissions gave one screenshot per screen size and one response body outside the save; the case was won by clicking in 55 turns; 140 tests with Playwright ([report](game-visuals/evidence/13-build-report.md), [case](game-visuals/img/13-case.webp), [ending](game-visuals/img/13-ending.webp)).
- **Own test by the coordinator, one run:** won from a new game through the server; every failed accusation identical for all six people without findings, and for the five others with all findings; no verdict readable in the decoded save of two failed accusations; closed game, forged verdict and missing captain refused; ending kept after reload; restart works; console clean.
- **Better than asked:** the builder found that the engine stores whether a guess was "correct but unsupported" in the state, so a decoded save would have revealed the culprit. New saves leave it out.
- **Failure observed:** a list of small design points rather than errors: nothing tells the player that reading a collected entry moves the case forward, the summary is clipped at 720 px, and Sarah's reaction to being accused herself is the same as for others.
- **Cause:** partly the engine (review gates without a hint, no text for Sarah), partly the prompt, which forbade restyling.
- **Change, and why:** reported to the engine and story owners; the clipping goes into the restyle.
