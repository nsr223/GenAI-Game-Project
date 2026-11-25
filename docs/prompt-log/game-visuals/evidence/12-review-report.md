> Worker report as delivered; links to local files removed.

# Journal verification

The journal passed the required browser checks at 1280×720 and 1440×900 with fake models. A delayed review exposed one keyboard focus regression, now fixed. Changes are uncommitted.

## Checks 1–14

Builder coverage refers to the recorded JSON. Partial means a measurement or state was missing from that record. 1280 checks · 1440 checks · Earlier regressions

| # | Builder coverage | Result |
|---|---|---|
| 1 | Partial. Elena's turns and review count, Olivia's turns and badge, and Maya's statement were recorded. | **Shown by reviewer**, using the coordinator's Elena run (0→1→1, one review) and direct browser checks for Olivia (3→4→5→5, one topic and one review, still read after reload) and Maya (one topic, turn 4, zero marker or internal-topic matches in page text, JSON and SSE). |
| 2 | Partial. Two overlaps with a matching later save. | **Shown by reviewer.** Ten overlaps with a double-open in each tab. Each run sent one review total, both tabs cleared Unread at turn 1, and the second action and reviewed state survived reload at turn 2. |
| 3 | Forged review returned only the generic error and message. | **Shown by builder.** Coordinator also reported zero disallowed matches across 238 responses outside the signed save. |
| 4 | Partial. All ten entry names were recorded. | **Shown by reviewer.** Opened all ten entries from a signed chain save and checked visible names and bodies for TBD, internal evidence IDs and replacement characters. |
| 5 | 30 evidence entries, 60 statements, scrolling and successful pins. | **Shown by builder.** Open took 21.0 and 19.1 ms through two animation frames. |
| 6 | All three pairings and persistence across navigation. | **Shown by builder.** Evidence/evidence, evidence/statement and statement/statement rendered with both titles. |
| 7 | Draft text, scroll at 82 px, delivered answer and queued review at turn 2. | **Shown by builder.** Coordinator independently confirmed the draft and late reply. |
| 8 | J opened the journal, typed into the draft and was ignored during a pending request. | **Shown by builder.** Held action completed at turn 1. |
| 9 | Partial. Focus return and accessible headings and list for an open entry. | **Failed and fixed** for related-link focus during a refresh. Keyboard-only navigation and Escape focus return passed at both sizes. The Chromium accessibility tree exposed headings, lists and Unread text. Screen-reader speech remains open. |
| 10 | Native 200% zoom, dimensions and reachable actions at both sizes. | **Shown by reviewer.** Native zoom produced 640×360 and 720×450 CSS viewports, zero horizontal overflow in the index and entry, and operable pin, index and close controls. |
| 11 | Partial. All three state messages recorded. | **Shown by reviewer.** Session-only review reset on reload. The read-only tab sent zero reviews until takeover. The invalid token stayed in storage with the journal disabled until explicit New game. |
| 12 | Partial. 4,019 characters and zero injected elements recorded. | **Shown by reviewer.** Exact 4,019-character fixture rendered as text, including the HTML-looking tag, emoji and Hebrew. Computed direction was RTL and the paragraph contained zero child elements. |
| 13 | Lead and 17→18→19 turns recorded. | **Shown by reviewer.** The lead was absent before either review and after EV-09. It appeared after EV-10 and survived reload. |
| 14 | Earlier room edges, 40 held Enter events yielding one request, reload, tabs, saves and dialogue regressions recorded. | **Shown by reviewer.** Full suite with Playwright passed 134 tests. Without Playwright, 132 passed and the two browser tests skipped cleanly. Browser warnings, errors and page exceptions were empty. |

Browser measurements · Supplemental browser checks

## Three additional stress cases

- **Retry a failed review.** A rejected response can consume a turn or clear Unread prematurely. The injected retryable error left the saved turn at 0. The second attempt saved turn 1 and cleared Unread.
- **Replace the save while a review waits for the lock.** Both cases contain EV-00, so a stale intent could review the wrong case. The replacement stayed at turn 0 with EV-00 unread and zero review requests.
- **Tab to a related entry while the current review is pending.** An asynchronous redraw can interrupt keyboard navigation. Before the fix the active element became BODY. After adding a stable key for each source and target link, the focused link survived the redraw. The new Playwright regression failed before and passed after. Before

## Screenshots opened at 1440×900

- The read-only banner explains takeover above Elena's visible evidence entry. Takeover requires closing the journal and using the room control. Read-only tab
- The session-only banner names reload and tab close as the expiry points. The notice, entry heading, observed text and question all fit above the fold. Session-only journal

Untested here are screen-reader speech, browsers other than Chromium, and real model responses. All verification servers and browser sessions were closed.
