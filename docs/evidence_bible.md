# Beneath the Surface — Evidence Bible

> **Status:** Initial draft (v0.3) · **Audience:** Development team only · **Spoilers:** Contains the true murderer, false leads, and solution logic.
>
> **Purpose of this document:** The Evidence Bible is the central reference for **everything the player can discover, how they discover it, and what it actually establishes**. It connects the fixed events of the Story Bible to searchable locations, inspectable objects, conversations, and game-state changes. Its job is to make the mystery **fair, coherent, and solvable** without allowing an NPC or an interactive object to reveal facts before the investigation has earned them.
>
> **Scope and authority:** `docs/story_bible.md` owns objective events and the murder solution; `docs/characters/*.md` owns personal knowledge, beliefs, and dialogue behavior; `docs/world_bible.md` owns physical rooms, connections, and objects. **This document owns evidence IDs, clue content, discovery mechanisms, prerequisites, evidentiary meaning, and reveal progression.** When a proposed clue would change the story or ship layout, revise the relevant Bible in the same pull request. **TBD** = unresolved; **PROPOSED** = useful design candidate, not confirmed canon; **FIXED** = already established in the Story Bible.

---

## 1. Evidence Design Goals

### 1.1 What the player should be able to prove

To reach the correct conclusion, the player must be able to independently establish:

1. **Motive:** Elena discovered Maya's unauthorized transfer of her technological improvement and intended to intervene.
2. **Opportunity:** Maya was at or near the wet laboratory during the critical period, contradicting her account.
3. **Method:** Elena sustained a fatal injury caused by a blow with a laboratory calibration object; the apparent equipment accident was staged.
4. **Exclusion of the accident theory:** The genuine **23:10** apparatus fault does **not** account for Elena's fatal injury.
5. **Alternative scandals:** Thomas manipulated investor-facing results and Daniel concealed environmental damage and an equipment fault. These facts make both credible suspects **without proving murder**.

The objective is **evidence-based deduction**, not obtaining an automatic confession or finding a single document that names the murderer.

### 1.2 Principles

- **Multiple clues per conclusion:** Motive, opportunity, method, and timing each require corroboration.
- **Truth versus interpretation:** A document can be genuine even when a suspect misinterprets it or lies about it.
- **Real red herrings:** Thomas's fraud and Daniel's misconduct are real; neither is fabricated solely to mislead the player.
- **Stable facts:** Evidence never changes its contents to match the player's current theory.
- **Preferred progression:** Story Bible §10 describes a preferred dramatic order, not a mandatory sequence. Conclusions require their supporting evidence and analysis; investigating or confronting Thomas and Daniel is not a prerequisite for the medical reconstruction.
- **Credible authority:** The player is an auditor, not a police officer. Restricted records, personal belongings, and the crime scene require consent or authorization.
- **No accidental spoilers:** LLM dialogue, room descriptions, evidence previews, and UI labels must obey discovery and revelation rules.
- **Not every prop is a clue:** Decorative objects need not produce meaningful evidence.

### 1.3 Terminology

| Term | Meaning |
|---|---|
| **Evidence item** | An authored discoverable object, file, statement, observation, or reconstructed finding with a stable ID. |
| **Fact** | A specific proposition established or supported by evidence. |
| **Lead** | A possible next question or location; not itself proof. |
| **Prerequisite** | A condition required before an item or interaction becomes available. |
| **Confrontation** | A topic-specific conversation in which the player challenges an NPC using relevant facts; not any conversation with that NPC. |
| **Revelation** | A narrative conclusion that becomes established only after the required corroboration. |
| **Gate** | A rule enforced in game state; the LLM must not bypass it. |
| **TBD / PROPOSED / FIXED** | Unresolved / candidate / already established in narrative canon. |

---

## 2. Canonical Evidence Anchors

These facts are **FIXED** and must remain consistent with the Story Bible:

| Anchor | Canonical fact | Evidence implication |
|---|---|---|
| Opening | Elena warns the player about experiment **M-17** at **18:10** in the dry lab. | This supplies the first lead; do not immediately explain all three scandals. |
| Thomas | He participated in deliberately misleading investor reporting and argued with Elena at **21:10**. | Give him an independently supported financial motive. |
| Daniel | He helped conceal damage from an earlier deployment, knew of an unresolved apparatus fault, and left the wet lab at **22:15**. | His misconduct is provable; his belief that he caused Elena's death is false. |
| Maya | She met Elena in the wet lab at **22:35**, killed her at approximately **22:45** using a heavy calibration object, and staged an accident before leaving by about **23:00**. | Clues must separately establish transfer motive, presence, and physical method. |
| Apparatus | An independent abnormal automated cycle occurred at **23:10**, after Elena was murdered. | The fault log is genuine but initially ambiguous. |
| Discovery | Lucas sees Elena through the wet-lab corridor-door panel at **06:50** and calls for help without opening the door. Thomas arrives a few seconds after Lucas calls; Olivia and Sarah arrive together next; Daniel arrives about half a minute after them; Maya arrives shortly after Daniel.; Sarah opens the lab and secures an unexplained-death scene after the initial response. | Witness content is fixed in Story §7.2 and EV-26; preceding locations/routes remain TBD; the arrival order and relative intervals are fixed. The player is not a discovery witness. |
| Cast | One player, Elena (victim), and **six living suspects** comprise the depicted shipboard cast. | No hidden eyewitness, surprise seventh suspect, or improvised crew member. |

**Important forensic qualification:** The Story Bible fixes the approximate death time for the writers. **A ship's preliminary medical assessment must not claim it can pinpoint a time of death to the minute.** The player should eventually exclude the *specific machinery mechanism* through a medically and technically supported reconstruction, then use other traces and testimony to reconstruct the broader time window. The exact physical details of that reconstruction are **TBD**.

---

## 3. Evidence Threads and Narrative Roles

### 3.1 Thread A — Research and financial fraud (Thomas)

**Player's initial lead:** Elena's warning to compare raw M-17 readings with investor-facing results.

**What this thread should establish:** The project's reported performance is overstated, Thomas knew or approved misleading claims, and Elena threatened the commercial timetable. This supplies a believable murder motive and helps explain his defensiveness.

**What it must not establish:** That Thomas was present for, caused, or arranged Elena's death.

### 3.2 Thread B — Ecological cover-up and apparent accident (Daniel)

**Player's initial lead:** Faulty sampling equipment at the scene and Daniel's suspicious behavior.

**What this thread should establish:** Earlier environmental damage was concealed; Daniel knew about the unresolved machinery fault; a genuine abnormal cycle occurred at 23:10; Daniel fears he caused Elena's death.

**Evidentiary limit:** A fault or cycle log alone does not exclude the machinery as the cause of death. That conclusion requires the comparative evidence and analysis in Section 6, regardless of whether either motive investigation has occurred.

### 3.3 Thread C — Unauthorized improvement and murder (Maya)

**Player's initial lead:** Research-version history and hints that someone produced a valuable technical improvement.

**What this thread should establish:** Maya's authorship or critical contribution, the proposed competitor transfer, Elena's objection, Maya's presence near the crime scene, and the physical inconsistencies in the staged accident.

**What it must not establish alone:** A draft contract by itself is not proof of murder; an ambiguous movement recording by itself is not proof of guilt.

### 3.4 Supporting thread — Other characters and ship context

Sarah controls scene preservation and permission to review sensitive systems; Olivia contributes preliminary and later comparative medical observations; Lucas may hold partial recordings and metadata. Their own secrets can complicate trust, but the MVP should not require an extensive fourth conspiracy.

---

## 4. Evidence Catalog (Initial Design)

**How to read the catalog:** Each entry has a stable **ID**, source, earliest intended discovery, the fact(s) it supports, and an explicit limit. **PROPOSED** specifics (file names, access, camera content, precise forensic traces) must be validated before implementation. Location and object IDs follow the World Bible.

### 4.1 Opening and M-17 evidence

#### `EV-00` — Elena's warning (FIXED)
- **Type / source:** The player's remembered conversation with Elena the previous evening; recorded as an initial journal lead.
- **Location / time:** `dry_lab`, **18:10**, pre-murder.
- **Discovery:** Remembered pre-game conversation, supplied as an initial M-17 lead when player control begins after the discovery response. No playable pre-murder scene or discovery-response knowledge is implied.
- **Player receives:** Elena asks for a comparison of original M-17 readings with investor-facing results and promises an explanation tomorrow.
- **Supports:** `elena_flagged_m17`; directs player to the experiment index and raw data.
- **Does not prove:** Fraud, Maya's transfer, or murder.

#### `EV-01` — M-17 experiment index (PROPOSED)
- **Type / source:** Digital research catalog.
- **Location / object:** `dry_lab` / `dry_lab_experiment_index`.
- **Access:** Ordinary audit permissions; available before or after the murder.
- **Player receives:** The experiment identifier, measurement dates, and links to the original dataset and reported summary.
- **Supports:** The player is comparing records from the same experiment.
- **Does not prove:** Any deliberate alteration.

#### `EV-02` — M-17 raw measurements (FIXED concept; PROPOSED presentation)
- **Type / source:** Read-only dataset and simple comparison chart.
- **Location / object:** `dry_lab` / `dry_lab_analysis_terminal`.
- **Access:** Audit permissions, via `EV-01` or direct dataset navigation.
- **Player receives:** Original results across multiple M-17 runs and observation times: variable early performance, later loss of retained alkalinity in some runs, and particle formation. Exact readable values and observation periods remain TBD; these are chemical measurements, not a direct weighing of atmospheric CO₂ removed.
- **Supports:** `m17_raw_readings_found`.
- **Does not prove:** Deliberate fraud without comparison against published claims.
- **Preserved-record lead:** Elena's preserved M-17 records contain a reference to the research revision examined in `EV-15`. The player-facing wording is **“The treatment works less well over time. See Maya Chen’s improved mixing tests.”** and points to EV-15. It identifies related work, not misconduct. The preserved copy's storage, provenance, and fair discovery/access route remain **TBD**; ordinary access to `EV-02` does not automatically grant access to Elena's private archive.
- **Design note:** Use understandable quantities and a minimal visual comparison; exact scientific numbers are **TBD**.

#### `EV-03` — Investor-facing M-17 summary (FIXED concept; PROPOSED presentation)
- **Type / source:** Published/slated presentation excerpt.
- **Location / object:** `dry_lab` / `dry_lab_shared_workstation` or `dry_lab_document_shelf`.
- **Access:** Readable during audit.
- **Player receives:** A summary built from the strongest early readings, excluding poorer runs and later losses, claiming consistent performance and presenting modelled potential uptake as verified carbon removal. Comparing it with EV-02 exposes these omissions and the changed claim.
- **Supports (when compared with `EV-02`):** `m17_discrepancy_identified`.
- **Does not prove:** Who altered the claim or why.

#### `EV-04` — Revision / approval history (PROPOSED)
- **Type / source:** Document metadata or tracked edits.
- **Location / object:** `dry_lab` / `dry_lab_shared_workstation`.
- **Access:** Specific audit-related record access; exact permission **TBD**.
- **Player receives:** Revision/approval records documenting deliberate selection of early results, exclusion of poorer runs/later measurements, and the change from predicted uptake to verified removal. Exact text and author/approval chain remain TBD.
- **Supports:** `m17_misrepresentation_deliberate`.
- **Does not prove:** That Thomas killed Elena.

#### `EV-05` — Thomas's commercial pressure message (PROPOSED)
- **Type / source:** Authorized business communication excerpt or preserved record.
- **Location / object:** `dry_lab` / `dry_lab_shared_workstation`; potentially disclosed in discussion with Thomas.
- **Access:** Legitimate access or voluntary/authorized disclosure, not arbitrary opening of private accounts.
- **Player receives:** Thomas demanded favorable reporting and feared delay to the financing round.
- **Supports:** `thomas_financial_pressure_established`.
- **Does not prove:** His whereabouts at 22:45 or participation in the murder.

### Fixed evening conversation leads

At 21:10, Lucas and Sarah saw Elena and Thomas conversing in the mess hall after dinner. Either can point the player to Thomas; neither heard the content or can independently establish its intensity. Thomas’s account concerns disputed reporting, correction, and financing (Story §6). No recording is established.

At 21:50, Elena confronted Daniel in his workshop about the C-2 override and omitted harm. Before leaving for the workshop, Elena tells Olivia and Thomas in the mess hall that she is going to speak to Daniel about an old report. They can report her stated intention and direct the player to Daniel, but did not witness or hear the workshop conversation. Daniel can confirm it occurred; neither Olivia nor Thomas knows its private content. Daniel initially minimizes an argument about an old report; his fuller admissions remain subject to authored disclosure conditions. Preserve speaker attribution and distinguish an announced intention from witnessed attendance.

These optional testimony leads do not require finding Elena’s notes first and do not gate the medical reconstruction. Elena’s rationale for postponement and Maya’s private reasoning are fixed in Story §6; neither becomes player knowledge without a supported source.

### 4.2 Environmental cover-up and equipment evidence

#### `EV-06` — Elena's note about Daniel's past incident (FIXED lead; storage TBD)
- **Type / source:** A short entry in Elena's preserved notes, sharing the eventual storage/access of `EV-17`.
- **Location / object:** Same authorized note source as `EV-17`; no separate technical archive search is required.
- **Access:** Discover the note through the authored route to Elena's preserved materials; exact route remains TBD.
- **Player receives:** “C-2 trial, about a year ago: revisit the incident involving Daniel. Sarah thought it had been dealt with. Ask Daniel what happened.”
- **Supports:** `previous_incident_lead_found`; explicit questions for Daniel and Sarah about Elena's renewed interest.
- **Does not prove:** Environmental harm, a safeguard override, a cover-up, or murder by itself.

#### `EV-07` — Follow-up testimony about the old incident (FIXED Sarah account; Daniel disclosure TBD)
- **Type / source:** Persisted, speaker-attributed responses to explicit questions, usually prompted by `EV-06`.
- **Location / interaction:** Speak with Daniel or Sarah wherever each is legitimately present; no mandatory engineering-record inspection.
- **Sarah's account:** There was a problem at C-2 about a year ago; Daniel said it was under control. Elena later asked Sarah about it, but Sarah could add little because she had considered the matter resolved. Sarah does not know the override, harm, or misleading report.
- **Daniel's account:** Initially minimizes the incident; further discussion may lead him to acknowledge his unsafe decision and concealment. Exact admission conditions remain TBD. Preserve any actual admission as testimony, not as an independent document finding.
- **Supports:** Sarah's response corroborates the incident's existence and Elena's inquiry. Set `daniel_coverup_involvement_supported` only if Daniel's actual testimony supports it, not from the note or Sarah's response alone.
- **Does not prove:** Murder or the timing of Elena's injury.
- **Scope:** Original flow, biological, and incident records remain part of how Elena uncovered the truth in the backstory. The player need not read excerpts. This optional thread is not a mandatory prerequisite for the medical reconstruction or ending.

#### `EV-08` — Unresolved sampling-apparatus fault (FIXED concept; PROPOSED artifact)
- **Type / source:** Service ticket, diagnostic notice, or fault entry.
- **Location / object:** `engineering_workshop` / `engineering_maintenance_terminal`.
- **Access:** Authorized review or disclosure by Daniel.
- **Player receives:** Evidence that Daniel knew the raised service cover's worn support catch could slip and required repair before Elena's death. Exact proof of his awareness remains TBD; general maintenance reputation is insufficient.
- **Supports:** `equipment_fault_known`.
- **Does not prove:** That this fault killed Elena.

#### `EV-09` — Abnormal automated cycle at 23:10 (FIXED)
- **Type / source:** Timestamped device or maintenance log.
- **Location / object:** `engineering_workshop` / `engineering_maintenance_terminal` (possibly mirrored at `wet_lab_workstation`, **TBD**).
- **Access:** Authorized log review; can be obtained **before** the final reconstruction.
- **Player receives:** At **23:10**, the controller resumed an interrupted weekly verification task left pending when automatic operation was restored. This was not the normal test day. The log establishes the retry, not the unsensed cover drop; the cover has no position sensor and no drop alert was generated.
- **Supports:** `apparatus_fault_2310_verified`.
- **Does not prove:** That Elena was alive, present, or injured during that cycle; **does not alone exclude** the machinery theory.
- **Presentation note:** Initially, this log should make Daniel's fear understandable, not settle the mystery.

### 4.3 Medical and crime-scene evidence

#### `EV-10` — Preliminary medical observations (PROPOSED)
- **Type / source:** Olivia's initial professional observations; possibly a short authorized report.
- **Location / object:** `medical_bay` / `medical_report_desk`.
- **Access:** Available early through conversation with Olivia (respecting confidentiality).
- **Player receives:** A significant localized head injury and scalp wound. Olivia cannot yet attribute it to the cover, a separate object, or another mechanism without comparison. The complete skull/brain injury is author canon, not an instant visual diagnosis.
- **Supports:** `medical_review_pending` and a lead to examine technical records.
- **Does not prove:** Murder, exact time of death, or that the apparatus did not kill Elena.
- **Early-dialogue boundary:** Olivia may express qualified concerns, **not** a definitive accident-exclusion conclusion.

#### `EV-11` — Medical–technical reconstruction (FIXED mechanism; comparative evidence details TBD)
- **Type / source:** Comparative finding assembled from Olivia's medical observations and verified apparatus behavior. Exclusion rests on the injury/mechanism mismatch, not an estimate proving death before 23:10.
- **Location / interaction:** `medical_bay` / `medical_report_desk`; conversation with Olivia after relevant documents are available.
- **Prerequisites:** `EV-09` and `EV-10` reviewed; sufficient authored medical/mechanical detail for comparison (TBD); appropriate authorization/cooperation (Section 6).
- **Player receives:** Olivia compares the injury with what the apparatus physically did at 23:10. The documented malfunction **cannot account for Elena's fatal injury**; the apparent accident scene demands another explanation. The player need not establish whether death preceded that cycle.
- **Supports:** `machinery_cause_excluded`, `accident_theory_disproved`.
- **Does not prove:** Maya's identity or an exact time of death. Neither temporal plausibility nor proof of death before 23:10 is a prerequisite for this conclusion.
- **Fixed comparison:** The broad straight cover edge and constrained hinged movement do not explain the localized compact-object head injury in the established scene. The physical cover failure is reconstructed through inspection; EV-09 alone does not record it.
- **Evidence-design TBD:** Specify the documented contact/reach observations and nearby surfaces that also exclude a cover-induced fall. Do not mark the reconstruction production-ready until that alternative is addressed. No exact time-of-death estimate, unique weapon identification, or full onboard autopsy is required.
- **Olivia's presentation:** Give the conclusion simply by default. Supply detailed comparisons only when explicitly asked, using her Character Bible examples; concise dialogue must not withhold an available finding.

#### `EV-12` — Sampling-apparatus scene inspection (PROPOSED)
- **Type / source:** Supervised physical observation and incident photographs.
- **Location / object:** `wet_lab` / `wet_lab_sampling_apparatus`, `wet_lab_workstation`.
- **Access:** After Sarah grants `wet_lab_inspection_authorized`.
- **Player receives:** The apparent accident scene has signs of disturbance; precise signs **TBD**.
- **Supports:** `wet_lab_scene_requires_review`.
- **Does not prove:** Which person disturbed the scene or that the apparatus could not cause the injuries.

#### `EV-13` — Calibration-object discrepancy (FIXED weapon category; PROPOSED traces)
- **Type / source:** Supervised inventory or visual inspection of calibration tools.
- **Location / object:** `wet_lab` / `wet_lab_calibration_station`.
- **Access:** After scene authorization; suspicious details may be inspectable before `EV-11`, but **definitive interpretation is gated**.
- **Player receives:** An anomalous trace or handling discrepancy involving the **2 kg stainless-steel reference mass**, which Maya returned to the calibration station. Exact trace/corroboration is **TBD**; do not describe the weapon as missing without a coordinated story change.
- **Supports:** `calibration_object_anomaly_found`.
- **Does not prove:** Alone that it is the murder weapon or that Maya handled it.

#### `EV-14` — Fatal-injury / weapon correspondence (PROPOSED)
- **Type / source:** A documented comparison of the injury description, scene inventory, and calibration object.
- **Location / interaction:** `medical_bay` with authorized `wet_lab` observations.
- **Prerequisites:** `EV-11` complete and `EV-13` recorded; exact trace corroboration and access protocol **TBD**. Weapon identity, weight, and fatal injury are fixed in Story §6.1.
- **Player receives:** The injury is consistent with a blow from the type of calibration object present in the laboratory. Combined with `EV-11` excluding the apparatus and `EV-13` documenting the object anomaly, this supports its use as the weapon; exact physical corroboration remains **TBD**.
- **Supports:** `blunt_force_method_supported`. Staging may be supported separately by the scene observations and wider reconstruction; object correspondence alone does not establish it.
- **Does not prove:** Whose hand held the object, intent from injury correspondence alone, or the exact staging actions. Avoid claiming a shipboard medic performed an implausible full forensic lab analysis.

### 4.4 Maya's improvement and movement evidence

#### `EV-15` — Scientific revision / authorship history (FIXED concept; PROPOSED artifact)
- **Type / source:** Research code commit history, dataset annotations, or experiment revision log.
- **Location / object:** `dry_lab` / `dry_lab_analysis_terminal`.
- **Access:** Ordinary audit access to relevant shared research work. The reference in Elena's preserved M-17 records provides an authored lead here; direct discovery through legitimate research navigation remains possible. The reference reads **“The treatment works less well over time. See Maya Chen’s improved mixing tests.”**; only the exact revision identifier and artifact presentation remain **TBD**.
- **Player receives:** Maya developed adaptive dosing software and a staged mixer. Limited controlled tests show less particle formation and better retained alkalinity than the existing system, not proven commercial readiness or universal safety.
- **Supports:** `maya_improvement_identified`.
- **Does not prove:** Theft, an unauthorized sale, or murder.

#### `EV-16` — Competitor transfer proposal (FIXED concept; PROPOSED artifact)
- **Type / source:** A draft agreement from Maya's email negotiations, discovered through an authorized route. Email correspondence may corroborate it but does not replace the draft; some exchanges predate this voyage.
- **Location / object:** `dry_lab` shared project records **or** `sleeping_room_a` / `personal_storage_maya` with appropriate authorization; placement **TBD**.
- **Access:** Specific permitted/consensual evidence disclosure; not free access to private accounts.
- **Player receives:** Maya offered unpublished control code, mixer drawings, operating parameters, and internal test datasets, with delivery proposed after final agreement, in return for compensation and a leading development role. Exact draft terms and excerpts remain TBD.
- **Supports:** `maya_transfer_plan_supported`.
- **Does not prove:** That a transfer was completed, or that she killed Elena.

#### `EV-17` — Elena's preserved notes (FIXED concept; PROPOSED storage)
- **Type / source:** Notebook, independent data archive, or preserved correspondence; exact medium **TBD**.
- **Location / object:** `sleeping_room_a` / `personal_storage_elena` **or** a valid research archive, **TBD**.
- **Access:** Permission from Sarah for evidence preservation, or a legitimate audit route. Provide an understandable lead to its storage.
- **Player receives:** Elena knew about Maya's negotiations and intended to prevent the planned transfer and report the negotiations. She had not seen the draft agreement found as `EV-16`; her notes must not imply otherwise. The notes may also point back to the M-17 discrepancy.
- **Supports:** `elena_knew_of_maya_negotiations`, `maya_motive_established` when combined with `EV-16`.
- **Does not prove:** Who physically attacked Elena.
- **Established supporting entry:** The C-2 note in `EV-06` is part of this note collection and leads to `EV-07` testimony, without requiring the historical technical records.
- **Fixed supporting entries:** Sarah’s admission/request (`EV-21`), Lucas’s repeated recording violations (`EV-22`), and the brief Noah incident lead (`EV-23`) share these notes. Text is fixed below; storage/access remains open. Notes do not automatically prove every interpretation.

#### `EV-18` — Partial corridor recording / media metadata (FIXED story content; implementation TBD)
- **Type / source:** Lucas's documented recording and its timestamp metadata.
- **Location / object:** `editing_room` / `editing_workstation` or `media_drive_case`.
- **Access:** Lucas willingly shares relevant footage or Sarah authorizes preservation/review; exact flow **TBD**.
- **Fixed story content:** Returning from the bridge toward the editing room around 22:30–22:35, Lucas captures a corridor shot showing Maya heading toward the labs, without noticing her. He spends roughly 22:35–22:55 organizing equipment/recordings and reviewing earlier Tuesday daytime footage, not the evening footage. He returns to Room A around 23:00, after Maya, and sees her and Olivia apparently asleep. The shot does not show the confrontation or murder. Exact camera position, coverage, timestamp metadata, audio, and review/access implementation are the evidence team’s **TBDs**.
- **Supports:** `maya_wet_lab_area_presence_supported` when compared to her stated alibi.
- **Does not prove:** Entry through a specific door, the murder act, or precise time of death.
- **Consistency note:** The wet and dry labs also have an internal connecting door. Camera coverage must not imply an impossible view of both routes.

#### `EV-19` — Maya's contradictory statement (FIXED claim; implementation TBD)
- **Type / source:** A persisted conversation admission or claim, compared with independent records.
- **Location / interaction:** Talk with Maya anywhere she is legitimately present.
- **Access:** Conversation; the game must persist her first material claim before permitting a contradiction check.
- **Player receives:** Maya's initial account is inconsistent with `EV-18` or another independently authored trace.
- **Supports:** `maya_alibi_contradicted`.
- **Does not prove:** Automatically that she murdered Elena.
- **Fixed claim:** “I was already in bed when Olivia came in. I did not leave the room again that night.” Olivia arrives around 22:20. EV-18 shows Maya heading toward the labs around 22:30–22:35 and directly contradicts continuous presence. Persist her claim before comparison. Exact recording metadata/access and post-confrontation disclosure remain TBD.

**Supporting bedtime testimony (speaker-attributed, not continuous alibis):** Olivia sees Maya in bed and Elena’s bunk empty in Room A around 22:20, then sleeps before Maya leaves. Lucas sees Maya and Olivia apparently asleep around 23:00 after Maya returns, and Elena’s bunk empty. Neither saw Maya’s bed empty; neither can verify continuous presence or actual sleep. Maya is awake when Lucas arrives. Daniel sees Thomas in his Room B bunk snoring around 22:20, not throughout the fatal window. Sarah’s public watch assignment is not continuous independent corroboration.

**Elena’s earlier whereabouts:** Daniel and Elena notice each other during his 22:05–22:15 maintenance check while she works in the dry lab. Daniel may report his sighting. If explicitly told Olivia’s empty-bunk observation, he may connect the earlier sighting as context, but cannot prove Elena’s location at 22:20 or later. This does not automatically share either witness’s knowledge with the other.

### 4.5 Support and optional clues

#### `EV-20` — Dinner argument testimony (PROPOSED)
- **Type / source:** Cross-checked recollections from participants.
- **Location / interaction:** `mess_hall` or permitted NPC conversations.
- **Player receives:** Elena refused to endorse publication during the 20:00–20:40 dinner. Exact other topics, wording, and participant reactions/recollections are **TBD** (Story §12); do not invent dialogue or import the separate 21:10 confrontation’s private content.
- **Supports:** Context for Thomas's financial motive and general pressure.
- **Does not prove:** The murderer's identity or the timing of the fatal confrontation.

#### `EV-21` — Sarah’s operational decision (FIXED, optional)
- **Source:** Elena’s note, stored with `EV-17`; shared storage/access remains TBD. No additional bridge/weather record is discoverable for this thread.
- **Text:** “Sarah admitted she let the final sampling operation continue despite her weather concerns, under pressure from Thomas. She asked me to leave it out of the audit. Revisit this with her.”
- **Follow-up:** Sarah explains the final sampling operation several weeks ago, worsening weather, commercial pressure, and absence of injury. Her private admission/request occurred ashore a few days before the voyage.
- **Meaning:** A lead to her judgment and defensiveness, not evidence of murder.

#### `EV-22` — Lucas’s unauthorized recording practice (FIXED background and note; optional)
- **Source:** Elena’s note with `EV-17`; shared storage/access remains TBD.
- **Text:** “Lucas has continued recording beyond agreed sessions more than once. I have raised this with him repeatedly. Ask what he has retained and arrange a review of the footage.”
- **Follow-up:** Repeated challenges over recent weeks are fixed. Maya and Sarah can report their own suspicions when asked about filming, but never checked or challenged it. They cannot identify file contents from these observations.
- **Meaning:** Grounds asking Lucas about retained material and arranging review; no automatic access to all files or proof of a specific recording. Review permissions, retention, storage, and technical implementation of the fixed murder-night footage remain TBD. This incident is not automatically `EV-18`.

### 4.6 Noah Bennett’s injury — optional supporting thread

Eight months before the murder, former sampling assistant **Noah Bennett** suffered a deep cut and a fracture to one finger when a heavy equipment-case lid slipped while he handled sampling supplies. He left for treatment and recovery, without permanent disability. The lid’s securing catch had previously been flagged as unreliable. Former equipment coordinator **Adrian Cole** had postponed replacement, expecting careful handling to suffice until a replacement arrived. Olivia described an ordinary handling accident and omitted the prior warning to protect Adrian from what she considered unfair disciplinary blame. She now acknowledges that deciding which circumstances mattered was not hers to do. Appropriate medical care is not in question. A warning does not establish that the injury was certainly preventable, but the story does not claim respecting it would have made no difference. Adrian and Noah are historical characters, not aboard or additional investigation witnesses. This incident is separate from C-2 and the current sampling-cover failure.

Elena, Olivia, Maya, Daniel, Thomas, and Sarah know the basic injury, departure, and recovery history. Lucas joined later and initially knows nothing, as does the player. Among the onboard cast, only Elena and Olivia initially know the omitted warning and Olivia’s reason. During the last week Elena raised the incident with Olivia, who acknowledged the omission without a major confrontation; Elena said the account should be corrected. Detailed historical reports are unavailable aboard and inaccessible to Olivia at present. She remembers the central omission and motive, not exact dates, wording, or the reporting chain; these peripheral details and Elena’s earlier research route need no additional evidence design.

#### `EV-23` — Elena’s Noah incident lead (FIXED, optional)
- **Source:** Elena’s note, stored with `EV-17`; shared storage/access remains TBD.
- **Exact text:** “Noah Bennett — follow up on the incident.”
- **Meaning:** Names Noah and an incident only; no mention of Olivia, injury, warning, or allegation.
- **Follow-up:** On explicit questioning, Sarah, Thomas, Daniel, or Maya recall the injury/departure/recovery and point to Olivia. Lucas initially knows nothing. Directly asking Olivia is also valid; no mandatory NPC sequence.

#### `EV-24` — Olivia’s account of Noah’s incident (FIXED testimony, optional)
- **Source:** Olivia’s honest answer when asked about Noah or the incident; no document or proof threshold required.
- **Player receives:** The case-lid injury, recovery, omitted prior warning, protection of Adrian Cole, and Elena’s discussion with her during the last week about correcting the account.
- **Meaning:** Speaker-attributed admission of a reporting lapse, not independent documentary verification or evidence of murder. Detailed reports are unavailable aboard; she cannot recall their exact wording/dates but remembers the substantive facts.

#### `EV-25` — Retired proposed warning artifact
- The warning remains a fixed historical fact explained by Olivia in `EV-24`. No separate warning document is accessible or required. Retain this ID only to avoid reusing an old clue identifier; remove it from gameplay dependencies.

**Disclosure:** Elena’s note reads only: **“Noah Bennett — follow up on the incident.”** It names neither Olivia nor the injury and makes no allegation. When explicitly asked about Noah or that incident, Maya, Daniel, Thomas, and Sarah recall the injury/departure/recovery and suggest asking Olivia. They do not know the hidden circumstances. Olivia explains the accident, omission, reason, and recent discussion with Elena honestly when asked, without a confrontation, proof threshold, or elaborate evasion. She does not volunteer it in greetings or unrelated discussion. Lucas cannot supply prior knowledge. Reading the note does not automatically trigger dialogue or brief the crew. The note shares Elena’s preserved notes; their storage/access remains TBD.

### 4.7 Discovery testimony

#### `EV-26` — Discovery and the cover exchange (FIXED events; presentation TBD)
- **Type / source:** Speaker-attributed recollections of the 06:50 discovery and subsequent response in the fixed order of Story §7.2, not an invented recording. Thomas first, Olivia/Sarah together, Daniel about half a minute later, then Maya shortly afterward.
- **Location / interaction:** Question relevant NPCs wherever legitimately present. Player control begins after the response; no opening replay or preloaded journal provides these details.
- **Lucas:** Saw Elena through the panel, could not open the door, and called for help. He does not reliably register the subsequent exchange/actions and cannot corroborate them firsthand. His question is why Elena was there, not an assertion of when she died.
- **Sarah, Olivia, Daniel, Maya, Thomas:** Hear “That cover was up when I left,” Sarah stopping Daniel before he touches the apparatus, “Could the cover have done that?”, and Olivia's “I can't tell that yet.” They know Olivia visibly considered the cover; this is not a diagnosis. These events occur after the witnesses have arrived.
- **Interpretations:** Thomas sees possible equipment responsibility; Maya may use Daniel's visible concern as misdirection; Sarah reports actions without assigning guilt; Olivia explains her uncertainty only as needed. Do not merge these interpretations into objective facts.
- **Supports:** A lead to ask why Daniel left the cover raised and whether the equipment could account for the injury; establishes the public statement and attempted approach, not the truth of every inference.
- **Does not prove:** The specific fault, that Daniel knew the 23:10 cycle ran, cause/time of death, or murder. Quiet/unheard remarks do not exist as evidence.
- **Presentation boundary:** A discovered body is not a confirmed murder scene. The player has no firsthand or preloaded knowledge of the response. Conversations supply the details, preserving speaker/source and Lucas's exception.

**MVP guidance:** Do not assume every numbered entry needs a separate interface. Several can be presented on the same terminal, and some can be conversation-derived clues. The IDs represent **logical evidence**, not necessarily separate physical props.

---

## 5. Evidence Dependencies and Investigation Paths

### 5.1 Primary clue chains

```text
OPENING / AUDIT
EV-00 Elena's M-17 warning
  -> EV-01 Experiment index
  -> EV-02 Raw readings + EV-03 Investor summary
  -> m17_discrepancy_identified
  -> EV-04 Revision history / EV-05 Thomas message
  -> confront Thomas about his motive
  -> thomas_motive_investigated

APPARENT ACCIDENT / DANIEL
EV-06 Elena's incident note -> EV-07 Sarah/Daniel testimony (optional depth)
EV-08 Known apparatus fault + EV-09 23:10 abnormal cycle
  -> confront Daniel about fault and/or cover-up
  -> daniel_motive_investigated

MEDICAL RECONSTRUCTION — WHEN SUPPORTING EVIDENCE IS AVAILABLE
EV-10 Preliminary medical observations + EV-09 Verified apparatus record
  + sufficient medical/mechanical detail and authorized comparison
  -> EV-11 Comparative medical–technical reconstruction
  -> machinery_cause_excluded
  -> EV-13 Calibration anomaly + EV-14 injury/tool comparison

MAYA'S MOTIVE / OPPORTUNITY
Elena's preserved M-17 records (EV-02 preserved-record lead; storage TBD)
  -> referenced research revision / EV-15 Improvement history
  -> EV-16 Transfer proposal + EV-17 Elena's preserved notes
  -> maya_motive_established
EV-18 Partial recording + EV-19 Claimed alibi
  -> maya_alibi_contradicted

FINAL ACCUSATION
maya_motive_established + maya_alibi_contradicted
+ machinery_cause_excluded + blunt_force_method_supported
  -> substantiated accusation of Maya
```

The branches show intended leads, not a mandatory discovery order. `EV-11` can be reached whenever its evidence and analysis requirements are met, including before either motive confrontation. `EV-14` requires its authored comparisons, not completion of unrelated investigation branches.

### 5.2 Suggested essential versus optional evidence

| Narrative requirement | At least one intended supporting route | Essential for success? |
|---|---|---|
| Thomas has a plausible financial motive | `EV-02` + `EV-03` + topic-specific confrontation (strengthened by `EV-04`/`EV-05`) | **No; preferred investigative context** |
| Daniel has plausible reason to fear responsibility | `EV-08` or `EV-09` + topic-specific confrontation; `EV-06`/`EV-07` adds ecological motive | **No; preferred investigative context** |
| Machinery theory fails | `EV-09` + `EV-10` + `EV-11` | **Yes** |
| Maya has unauthorized-transfer motive | `EV-16` + `EV-17` | **Yes** |
| Maya was present during the critical window | `EV-18` + persisted alibi `EV-19` (or a future equally strong authored alternative) | **Yes** |
| Fatal blow / weapon correspondence | `EV-11` + `EV-13` + `EV-14` | **Yes; a separate reconstruction of staging actions is not required** |
| Sarah's compromise, Lucas's privacy lapse, Daniel's full past cover-up, Olivia's misleading injury account | `EV-07`, `EV-21`–`EV-24` | **Optional depth** |

A future balancing pass may add **alternative routes** for a required fact, but each alternative must be explicitly authored and tested. Free-text NPC improvisation is not an alternative evidence source.

---

## 6. Protected Revelation: The Machinery Did Not Kill Elena

### 6.1 Preferred progression; evidence-based prerequisites

Investigating Thomas and Daniel before the definitive reconstruction is the preferred dramatic progression, not a requirement. Players may obtain and compare the necessary evidence in different orders. Olivia may express preliminary concerns early and must not withhold a supported finding solely because a motive conversation has not occurred.

The motive-investigation flags below track substantive inquiry, not access to `EV-11`. Merely greeting a suspect does not establish that their motive was investigated.

### 6.2 Specific state flags

| Flag | Set when | Must not be set by |
|---|---|---|
| `thomas_motive_investigated` | Player establishes M-17 discrepancy and **confronts Thomas** about misleading claims / consequences for Elena. | Just greeting Thomas, hearing gossip, or finding `EV-02` alone. |
| `daniel_motive_investigated` | Player has credible evidence of fault or ecological-cover-up involvement and **confronts Daniel** about negligence, concealment, or possible responsibility. | Just seeing the broken apparatus or having an unrelated conversation. |
| `medical_reconstruction_available` | `EV-09` and `EV-10` are reviewed, sufficient medical/mechanical detail is available, and needed access is granted; neither motive flag is required. | LLM judgment or number of interactions alone. |
| `medical_reconstruction_completed` | Player explicitly performs the approved reconstruction/discussion with Olivia. | Merely entering the medical bay. |
| `machinery_cause_excluded` | Completion of `EV-11` reveals its authored conclusion. | Preliminary notes, general scene descriptions, casual speculation, or another NPC's unsolicited line. |

**Implementation suggestion:** A structured dialogue-event detector or topic-specific interaction sets each confrontation flag after confirming both a relevant topic and an adequate evidence basis. Record the event in game state; never let the LLM set arbitrary flags directly.

### 6.3 Early-stage permissible information

While the evidence and analysis needed for the reconstruction are still incomplete (not a fixed act or conversation order):

- The player **may know** that the apparatus had a serious fault.
- The player **may know** the apparatus cycled abnormally at 23:10.
- Olivia **may express uncertainty** about whether the scene fully explains the injuries.
- Daniel **may sincerely fear** that his negligence killed Elena; he may even say something resembling a confession of responsibility.
- The player **may suspect** that the scene was staged, but does not yet have definitive evidence excluding the machinery.
- Maya's transfer motive **may be explored early**, but should not trigger a self-incriminating confession or definitive murder explanation before corroboration.

**Not allowed without supporting evidence and analysis:** A medical report, tool description, ambient narration, video, or NPC statement definitively declaring “Elena was already dead at 23:10,” “the machine could not have killed her,” or “Maya used the calibration object.”

### 6.4 In-world explanation for staged analysis

The reconstruction is not a fact Olivia secretly knows from the beginning. She has an **incomplete preliminary assessment**. The player later assembles validated equipment records, receives appropriate permission, and asks Olivia to compare the proposed accident mechanism with her observations.

Thomas/Daniel discussions may provide leads, records, or cooperation, but neither confrontation is mandatory. Define the actual missing medical/mechanical information and authorized routes to obtain it. Olivia must explain an outstanding evidentiary need truthfully rather than refuse a completed diagnosis for pacing. The required comparative detail remains **TBD**.

### 6.5 Re-check behavior

If a player asks Olivia for a definitive conclusion too soon, she should give a truthful, non-spoiling response such as:

> “I can't give you a reliable cause yet. We need to know exactly what that apparatus did, and compare it with the injuries. The initial scene isn't enough.”

Once the prerequisites are met, the journal may add a lead: **“Return to Olivia to compare medical observations with the confirmed apparatus log.”** The player does not need to guess that the same dialogue option has changed silently.

---

## 7. Dialogue and Evidence Interaction Rules

### 7.1 Evidence as a conversation topic

When the player presents an item to an NPC, the game should send the **evidence ID and verified content** alongside the message. NPCs react according to their Character Bibles; they cannot modify the source record.

Example:

```yaml
conversation_input:
  npc_id: daniel_reyes
  player_message: "You knew the sampling apparatus had a fault. Why didn't you fix it?"
  presented_evidence_ids: [EV-08]
  investigation_flags:
    thomas_motive_investigated: false
    daniel_motive_investigated: false
    medical_reconstruction_completed: false
```

A validated conversation outcome may set `daniel_motive_investigated`, but the evidence content itself stays unchanged.

### 7.2 Knowledge versus revelation

**Research explanation levels:** Maya alone among living NPCs explains the full scientific process. Daniel explains machinery, Thomas claims/financing, Sarah operations, Olivia general safety, and Lucas the documentary premise. Use their Character Bible examples. Authored evidence remains understandable and independently accessible; do not force a particular conversation order or make Maya's cooperation essential to solving the case.

- **Maya** privately knows what she did; this knowledge is not the player's knowledge.
- **Daniel** does not know he is mistaken until he receives credible contrary evidence; he should not spontaneously announce that he was definitely innocent.
- **Thomas** knows about deliberate data manipulation, not the murder.
- **Olivia** knows about Elena's fatal injury only what her observations and subsequent reconstruction allow. Separately, she knows the concealed circumstances of Noah's incident; apply §4.6 disclosure rules.
- **Lucas** knows what his actual recordings show, not hidden events outside the camera's view.
- **Sarah** manages authorization and preservation; she is not an omniscient narrator.

### 7.3 Player journal / evidence board

Each collected item should have:

1. **Observed:** the exact document text, clip summary, or statement the player actually saw.
2. **Interpretation:** optional cautious inference, clearly separate from verified facts.
3. **Questions:** follow-up leads or unresolved contradictions.
4. **Related entries:** links to other clue IDs and NPCs.

Avoid revealing developer-only fields such as `supports: maya_motive_established` in the player-facing UI before those conclusions are earned.

### 7.4 Persistence and anti-hallucination

- Dialogue-created testimony must be stored as a stable claim with speaker, time, and topic, so later contradictions can be checked.
- Records, screenshots, and videos must come from authored content, not be generated ad hoc by the NPC model.
- Discoveries and access permissions are determined by deterministic application logic.
- If the player asks to inspect an undefined object, the system may describe ordinary scenery but cannot invent a new decisive clue.
- Do not infer a culprit from trust/stress values alone. Those may affect presentation, not the solution.

---

## 8. Permissions, Locations, and World Consistency

### 8.1 Access matrix (initial proposal)

| Area | Relevant evidence | Intended access |
|---|---|---|
| `dry_lab` | `EV-00`–`EV-05`, `EV-15`; possibly `EV-16` and Elena's notes if placed there | Existing scientific audit rights; sensitive accounts remain restricted. |
| `wet_lab` | `EV-12`, `EV-13` | Initially secured after the body is found; later supervised inspection only. |
| `medical_bay` | `EV-10`, `EV-11`, `EV-14` | Olivia provides appropriately scoped observations; definitive reconstruction is gated. |
| `engineering_workshop` | `EV-08`–`EV-09` | Sarah's permission or Daniel's supervised cooperation. |
| `editing_room` | `EV-18`, `EV-22` | Lucas's cooperation or authorized preservation. |
| `crew_quarters` / `sleeping_room_a` / `personal_storage_elena` | `EV-17`, including `EV-06`, if stored there | Specific permission for Elena’s belongings; shared-room access alone is insufficient; exact placement TBD. |
| `crew_quarters` / `sleeping_room_a` / `personal_storage_maya` | `EV-16` only if placed there | Shared-room access does not permit searching Maya’s personal storage; exact mechanism TBD. |
| `mess_hall` | `EV-20`; `EV-07` if the relevant NPC is present | Open social area; testimony can also occur at other valid NPC locations. |
| `bridge` | `EV-21`, access approvals | Captain-controlled records. |

### 8.2 Doors, recording coverage, and alibis

The World Bible fixes a **secondary internal door connecting `wet_lab` and `dry_lab`**. Any statement about visibility, routes, door sensors, timestamps, or alibis must account for both entrances.

Do not introduce comprehensive CCTV, biometric tracking, GPS pins for everyone, or a perfect shipwide access log merely to solve a narrative gap. If a precise recording proves Maya passed the wet-lab corridor, it should establish **presence in an area**, not make all other evidence unnecessary.

### 8.3 Evidence handling

The captain secures the scene and reports the incident. The player may examine **authorized read-only copies**, make notes, and participate in supervised comparison. They do not remove a suspected murder weapon, alter medical records, or privately seize an NPC's property.

---

## 9. Accusation, Win Conditions, and Failure Modes

### 9.1 Proposed endgame rule

A **substantiated accusation** of Maya should require demonstrated findings for all four categories:

| Category | Suggested flag | Evidence basis |
|---|---|---|
| Motive | `maya_motive_established` | `EV-16` + `EV-17` |
| Opportunity / false alibi | `maya_alibi_contradicted` | `EV-18` + `EV-19` or approved equivalent |
| Death not due to machine | `machinery_cause_excluded` | `EV-11` after supporting evidence and analysis |
| Physical method | `blunt_force_method_supported` | `EV-13` + `EV-14` |

**Player-facing ending:** The player presents their reconstruction and collected evidence to Sarah; she records and secures it for the arriving investigators. The player is **not** portrayed as issuing an official conviction or personally performing a criminal arrest.

### 9.2 Wrong or unsupported accusations

- A **wrong accusation** should prompt Sarah to ask for corroboration or produce an inconclusive ending, rather than changing the canonical murderer.
- A **correct guess without evidence** should not count as a full solution.
- The player should normally be able to continue gathering missing evidence, depending on the team's chosen ending structure (**TBD**).
- Maya's confession can be an optional dramatic payoff, **not** a required solution step.

### 9.3 Avoiding softlocks

- Every required clue needs an accessible route that does not depend solely on an unprompted LLM confession.
- Each restricted source requires a documented way to obtain access.
- If a player misses an early optional conversation, there must still be a route to obtain essential post-murder information.
- The two motive conversations can happen in either order; neither should prevent the other.
- After gate conditions are met, show an explicit lead back to Olivia.

---

## 10. Suggested Structured Data for Implementation

The Markdown file is the **human-readable design source**. After agreement, export clue definitions to `data/evidence.yaml` (or JSON) and test them against game state. Do not try to parse prose paragraphs as runtime rules.

### 10.1 Example evidence record

```yaml
id: EV-09
slug: apparatus_cycle_log_2310
status: fixed_fact_proposed_ui
name: Apparatus Cycle Log
location_id: engineering_workshop
object_id: engineering_maintenance_terminal
source_type: machine_log
access:
  any:
    - engineering_record_review_authorized
    - daniel_shares_record
prerequisites: []
player_visible_summary: >
  An abnormal automated cycle was recorded at 23:10.
verified_facts:
  - apparatus_fault_2310_verified
not_established:
  - machinery_cause_excluded
  - exact_time_of_death_proven
linked_characters:
  - daniel_reyes
linked_clues:
  - EV-08
  - EV-10
  - EV-11
```

### 10.2 Example protected revelation rule

```yaml
id: medical_reconstruction_available
all_of:
  - evidence_reviewed: EV-09
  - evidence_reviewed: EV-10
  - medical_mechanical_detail_sufficient  # authored comparison requirements TBD
  - medical_comparison_authorized

on_completed_interaction:
  interaction_id: discuss_reconstruction_with_olivia
  unlock_evidence: EV-11
  set_flags:
    - medical_reconstruction_completed
    - machinery_cause_excluded
```

`medical_mechanical_detail_sufficient` represents the authored injury/mechanism evidence needed for a defensible comparison, not completion of motive conversations. `medical_comparison_authorized` is a **proposed access flag**; the story reason for granting it is **TBD**. The event handler should check the prerequisite flags itself; a dialogue model cannot invent a shortcut.

### 10.3 Suggested game-state fields

```yaml
investigation_state:
  collected_evidence_ids: []
  reviewed_evidence_ids: []
  thomas_motive_investigated: false
  daniel_motive_investigated: false
  medical_reconstruction_available: false
  medical_reconstruction_completed: false
  machinery_cause_excluded: false
  maya_motive_established: false
  maya_alibi_contradicted: false
  blunt_force_method_supported: false
  accusations_made: []
```

### 10.4 Suggested validation checks

- Every `location_id` and `object_id` exists in the World Bible/data.
- Every clue ID is unique and every link points to a defined ID.
- Fixed timestamps match the Story Bible: **18:10, 21:10, 21:50, 22:15, 22:35, ~22:45, 23:10, 06:50 discovery; fixed relative arrival order per Story §7.2**.
- Protected facts cannot appear in early player-visible summaries, ambient descriptions, or default NPC responses.
- `machinery_cause_excluded` requires the supported `EV-11` analysis, but remains reachable with either or both motive-confrontation flags false.
- The final accusation is reachable from discoverable evidence without relying on chance model output.
- No essential clue requires illegal or unapproved access without a supported alternative.
- Recording fields of view respect the World Bible's room connections.

---

## 11. Playtesting Checklist

### 11.1 Progression tests

- [ ] Player can start with M-17 and pursue Thomas's financial motive.
- [ ] Player can pursue Daniel's fault/cover-up motive first instead.
- [ ] Talking casually to Thomas and Daniel **does not** unlock `EV-11`.
- [ ] Sufficient reconstruction evidence and authorization unlock the route even when neither suspect has been confronted.
- [ ] Confronting both suspects without the necessary comparative evidence does not unlock the reconstruction.
- [ ] `EV-10` and `EV-09` never definitively eliminate Daniel by themselves.
- [ ] Olivia does not assert an unsupported conclusion or withhold a supported conclusion solely to enforce the preferred order.
- [ ] The player gets an understandable new lead when `EV-11` becomes available.
- [ ] The player can independently support Maya's motive, opportunity, and method.
- [ ] A correct accusation without required proof does not count as full success.

### 11.2 Dialogue consistency tests

- [ ] Daniel's fear is sincere; he does not know Maya's actions.
- [ ] Thomas may deny or rationalize fraud but cannot alter document contents.
- [ ] Maya can mislead and deflect, but cannot rewrite timestamped evidence.
- [ ] Lucas cannot provide recordings from nonexistent cameras or firsthand testimony about the cover exchange he did not register.
- [ ] Sarah, Olivia, Daniel, Maya, and Thomas retain the fixed public exchange; none treats Olivia's interest in the cover as a causal finding.
- [ ] Olivia never supplies an exact minute of death from a cursory exam.
- [ ] NPCs do not spontaneously invent new ship personnel, witnesses, or murder weapons.
- [ ] Noah's incident is discussed only on explicit questioning; Lucas has no initial knowledge and other suspects do not inherit Olivia's private knowledge.
- [ ] Past admissions remain consistent after switching rooms or restarting an NPC session.

### 11.3 Fairness tests

- [ ] At least two independent clue categories support the correct suspect.
- [ ] Every essential clue has a clear investigative lead or discoverable route.
- [ ] Red herrings remain believable once the solution is known.
- [ ] The player is never forced to guess a private password or randomly click every prop.
- [ ] The mystery is solvable even if Maya never confesses.

---

## 12. Open Decisions Before Production

| Decision | Why it matters | Related files |
|---|---|---|
| **Medical/scene corroboration of the established mechanism** | The fatal head injury, cover failure, and compact-object comparison are fixed. Define observable contact/reach evidence and exclude a secondary fall into nearby surfaces; proof of death before 23:10 is not required. | Story, Olivia, Daniel, World |
| **Actual comparative evidence and authorized access needed for reconstruction** | Supports a defensible conclusion without requiring either motive confrontation. | Story, Olivia, Evidence |
| **Maya’s response after contradiction** | Initial claim and bedtime observations are fixed in EV-19; author further disclosure without inventing a replacement alibi. | Maya, Lucas, Story |
| **Lucas’s camera placement, metadata, and coverage** | The return from the bridge and incidental shot of Maya heading toward the labs around 22:30–22:35 are fixed. Evidence team implements exact view, timing metadata, audio, and discovery/review without expanding the story content. | Lucas, World |
| **Reference mass trace and scene corroboration** | The 2 kg mass, strike, and return to the station are fixed. Define remaining discoverable traces without an unrealistic instant lab test. | Story, World, Olivia |
| **Elena's preserved notes and how the player finds them** | Ensures the initial hint leads fairly to the transfer motive. | Story, World |
| **Competitor agreement's storage and access permissions** | Prevents arbitrary search of Maya's private material. | Maya, World |
| **Exact evidence for Thomas's approval of misleading claims** | Supports a strong motive without implying he killed Elena. | Thomas, Story |
| **Discovery implementation and witness presentation** | Lucas and the initial response are fixed (Story §7.2, EV-26). Arrival order and relative intervals are fixed. Define preceding locations/routes and any clue-relevant examination movements; preserve the shared exchange, Lucas's exception, and the player's lack of discovery knowledge. | Story, Character Bibles, World |
| **Supporting Elena notes: shared storage/access** | Texts for Sarah, Lucas, and Noah are fixed in EV-21–EV-23; implement their access through EV-17 without adding historical document hunts. | Story, Characters, World |
| **Check that the combined evidence distinguishes Maya from another attacker** | Test whether the final reconstruction rules out a plausible later attacker or alternative sequence through authored alibis, timing, and/or attack/staging traces. Motive, nearby presence, and a lie alone are insufficient; precise clues remain TBD. | Story, all Character Bibles, World, Evidence |
| **Alibi verification and noise consistency** | Actual positions and movements are fixed in Story §7.1; establish claims/corroboration. Preserve both lab doors closed, unheard 23:10 clunk, and no alert. Separately settle whether the earlier argument/strike could be heard or recorded. | All Character Bibles, Story, World |
| **Readable M-17 values, periods, and artifact wording** | The treatment process, limitations, adaptive improvement, and fraud mechanism are fixed; choose illustrative measurements and clear charts without confusing potential uptake with verified removal. | Story, Maya, Thomas, World |
| **Final accusation behavior and optional ending variants** | Controls whether a wrong guess ends the game or allows further investigation. | Story, game design |

**Recommended order to resolve:** (1) claimed alibis, corroboration, and implementation of the established recording, (2) physical/medical mechanism, (3) reconstruction evidence and access requirements, (4) clue placement and permission paths, (5) numeric data and presentation details. The basic science and misconduct mechanisms are established; do not reopen them as unspecified technology.

---

## 13. Related Documents and Editing Rules

- **`docs/story_bible.md`** — Canonical events, backstory, three scandals, true murder solution, and major timeline.
- **`docs/characters/*.md`** — NPC-specific knowledge, misbeliefs, admissions, lies, disclosure boundaries, and personalities.
- **`docs/world_bible.md`** — Deck layout, room IDs, object IDs, door connections, and physical access constraints.
- **`data/evidence.yaml` (planned)** — Machine-readable version of approved clue records and gates.
- **`data/timeline.yaml` (planned)** — Machine-readable canonical event sequence.

### Change-control rule

When evidence is added or modified, check four questions in the pull request:

1. **Story:** Does the clue agree with what really happened and the fixed timestamps?
2. **Character:** Could the relevant NPC actually know this fact, and what can they say about it?
3. **World:** Does the object exist in that room, and is its access path physically and legally plausible?
4. **Progression:** Does each conclusion have supporting evidence and analysis, without imposing the preferred dramatic order as a mandatory sequence?

**Guiding principle:** *The Story Bible defines reality. The Character Bibles define perspectives. The World Bible defines what exists. The Evidence Bible defines what can be discovered and proven. The game engine controls when; the LLMs control how people respond.*

### Fixed organization, financing, and calendar context

**Calendar:** Mid-December, with no fixed year or exact calendar dates. The mission departed Galway on Sunday with the player aboard. Elena is murdered Tuesday evening; discovery is Wednesday at 06:50, with player control beginning after the initial response. Historical incidents retain their relative dates (about a year ago, eight months ago, and several weeks ago).

Pelagos Carbon seeks **roughly €8 million in its next funding round** to support further trials, engineering development, and a larger demonstration system. Thomas represents the prospective lead investor. Favorable expedition results matter to securing that commitment; correcting the claims could delay or derail the round and damage his credibility with other investors. This is prospective financing, not money already lost or Thomas’s personal investment. Exact commitments and terms are not fixed.

Maya’s negotiation counterpart in `EV-16` is **Nereid Technologies**, a competing marine carbon-removal company offering a lead research role and development autonomy. Negotiations and a draft are established, not a completed transfer. Keep nonessential dates approximate; preserve fixed clue-relevant event times. Only Sarah initially knows the forecast of severe conditions at least through Thursday evening; this is not a promised rescue time.
