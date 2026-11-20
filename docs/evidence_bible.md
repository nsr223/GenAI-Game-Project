# Beneath the Surface — Evidence Bible

> **Status:** Initial draft (v0.1) · **Audience:** Development team only · **Spoilers:** Contains the true murderer, false leads, and solution logic.
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
- **Credible authority:** The player is an auditor, not a police officer. Restricted records, cabins, and the crime scene require consent or authorization.
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
| Daniel | He helped conceal damage from an earlier deployment, knew of an unresolved apparatus fault, and left the wet lab at **22:20**. | His misconduct is provable; his belief that he caused Elena's death is false. |
| Maya | She met Elena in the wet lab at **22:35**, killed her at approximately **22:45** using a heavy calibration object, and staged an accident before leaving by about **23:00**. | Clues must separately establish transfer motive, presence, and physical method. |
| Apparatus | An independent abnormal automated cycle occurred at **23:10**, after Elena was murdered. | The fault log is genuine but initially ambiguous. |
| Discovery | The body is discovered at **07:00** the next morning. | Exact discoverer and first response sequence are **TBD**. |
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
- **Type / source:** Conversation with Elena; recorded as a player-journal lead.
- **Location / time:** `dry_lab`, **18:10**, pre-murder.
- **Discovery:** Opening interaction; cannot be missed in the main scenario.
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
- **Player receives:** A small, readable set of original measurement results.
- **Supports:** `m17_raw_readings_found`.
- **Does not prove:** Deliberate fraud without comparison against published claims.
- **Preserved-record lead:** Elena's preserved M-17 records contain a reference to the research revision examined in `EV-15`. The reference identifies related scientific work, not misconduct. The preserved copy's storage, provenance, and fair discovery/access route remain **TBD**; ordinary access to `EV-02` does not automatically grant access to Elena's private archive.
- **Design note:** Use understandable quantities and a minimal visual comparison; exact scientific numbers are **TBD**.

#### `EV-03` — Investor-facing M-17 summary (FIXED concept; PROPOSED presentation)
- **Type / source:** Published/slated presentation excerpt.
- **Location / object:** `dry_lab` / `dry_lab_shared_workstation` or `dry_lab_document_shelf`.
- **Access:** Readable during audit.
- **Player receives:** A performance claim inconsistent with `EV-02`.
- **Supports (when compared with `EV-02`):** `m17_discrepancy_identified`.
- **Does not prove:** Who altered the claim or why.

#### `EV-04` — Revision / approval history (PROPOSED)
- **Type / source:** Document metadata or tracked edits.
- **Location / object:** `dry_lab` / `dry_lab_shared_workstation`.
- **Access:** Specific audit-related record access; exact permission **TBD**.
- **Player receives:** The misleading reporting language was introduced or approved through a deliberate workflow.
- **Supports:** `m17_misrepresentation_deliberate`.
- **Does not prove:** That Thomas killed Elena.

#### `EV-05` — Thomas's commercial pressure message (PROPOSED)
- **Type / source:** Authorized business communication excerpt or preserved record.
- **Location / object:** `dry_lab` / `dry_lab_shared_workstation`; potentially disclosed in discussion with Thomas.
- **Access:** Legitimate access or voluntary/authorized disclosure, not arbitrary opening of private accounts.
- **Player receives:** Thomas demanded favorable reporting and feared delay to the financing round.
- **Supports:** `thomas_financial_pressure_established`.
- **Does not prove:** His whereabouts at 22:45 or participation in the murder.

### 4.2 Environmental cover-up and equipment evidence

#### `EV-06` — Previous deployment incident summary (FIXED concept; PROPOSED artifact)
- **Type / source:** Archived environmental / expedition report.
- **Location / object:** `dry_lab` / `dry_lab_document_shelf` or `dry_lab_analysis_terminal`.
- **Access:** Audit search or a pointer from Daniel/Elena's materials.
- **Player receives:** An older experiment caused ecological damage that was not fully disclosed.
- **Supports:** `previous_ecological_incident_identified`.
- **Does not prove:** Daniel alone caused the incident, nor that it relates causally to Elena's death.

#### `EV-07` — Withheld maintenance or incident record (PROPOSED)
- **Type / source:** Archived service note / incomplete safety submission.
- **Location / object:** `engineering_workshop` / `engineering_maintenance_terminal`.
- **Access:** Sarah-authorized engineering record review, or Daniel's cooperation.
- **Player receives:** Daniel knew more about the prior ecological incident than the official summary admits.
- **Supports:** `daniel_coverup_involvement_supported`.
- **Does not prove:** Murder, or the timing of Elena's injury.

#### `EV-08` — Unresolved sampling-apparatus fault (FIXED concept; PROPOSED artifact)
- **Type / source:** Service ticket, diagnostic notice, or fault entry.
- **Location / object:** `engineering_workshop` / `engineering_maintenance_terminal`.
- **Access:** Authorized review or disclosure by Daniel.
- **Player receives:** Evidence that Daniel knew of the specific unresolved safety-related fault before Elena's death.
- **Supports:** `equipment_fault_known`.
- **Does not prove:** That this fault killed Elena.

#### `EV-09` — Abnormal automated cycle at 23:10 (FIXED)
- **Type / source:** Timestamped device or maintenance log.
- **Location / object:** `engineering_workshop` / `engineering_maintenance_terminal` (possibly mirrored at `wet_lab_workstation`, **TBD**).
- **Access:** Authorized log review; can be obtained **before** the final reconstruction.
- **Player receives:** The apparatus underwent an abnormal automated cycle at **23:10**.
- **Supports:** `apparatus_fault_2310_verified`.
- **Does not prove:** That Elena was alive, present, or injured during that cycle; **does not alone exclude** the machinery theory.
- **Presentation note:** Initially, this log should make Daniel's fear understandable, not settle the mystery.

### 4.3 Medical and crime-scene evidence

#### `EV-10` — Preliminary medical observations (PROPOSED)
- **Type / source:** Olivia's initial professional observations; possibly a short authorized report.
- **Location / object:** `medical_bay` / `medical_report_desk`.
- **Access:** Available early through conversation with Olivia (respecting confidentiality).
- **Player receives:** Cause of death remains uncertain; certain observations need to be compared with the equipment's actual behavior.
- **Supports:** `medical_review_pending` and a lead to examine technical records.
- **Does not prove:** Murder, exact time of death, or that the apparatus did not kill Elena.
- **Early-dialogue boundary:** Olivia may express qualified concerns, **not** a definitive accident-exclusion conclusion.

#### `EV-11` — Medical–technical reconstruction (PROPOSED mechanism; evidence-dependent conclusion)
- **Type / source:** Comparative finding assembled from Olivia's medical observations, verified apparatus behavior, and an assessment of temporal plausibility using the available observations and timestamps. These are combined within `EV-11`; no separate numbered timing clue is required by this design.
- **Location / interaction:** `medical_bay` / `medical_report_desk`; conversation with Olivia after relevant documents are available.
- **Prerequisites:** `EV-09` and `EV-10` reviewed; sufficient authored medical/mechanical detail for comparison (TBD); appropriate authorization/cooperation (Section 6).
- **Player receives:** Olivia compares the injury with what the apparatus physically did at 23:10 and assesses whether the proposed accident sequence fits the available timing information. The documented cycle **cannot account for Elena's fatal injury**. State separately what the mechanism excludes and what the timing merely permits or supports; the apparent accident scene demands another explanation.
- **Supports:** `machinery_cause_excluded`, `accident_theory_disproved`.
- **Does not prove:** Maya's identity or a minute-precise time of death. A death interval compatible with 22:45 does not by itself establish death before 23:10 if that interval also includes or extends beyond 23:10.
- **Forensic/timing design TBD:** Specify the defensible injury/mechanism contrast and the observations and timestamps supporting the temporal assessment, with their uncertainty. Check whether the combined reconstruction can establish death before 23:10, as Story §6.3 currently requires, or only exclude the apparatus as the cause. If only the latter is supported, explicitly revise the player-proof requirement in the Story Bible before finalizing the ending; do not silently promote temporal plausibility into proof. The canonical death remains approximately 22:45.

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
- **Player receives:** An object is not where its storage/inventory record suggests, or has an anomalous trace; exact presentation **TBD**.
- **Supports:** `calibration_object_anomaly_found`.
- **Does not prove:** Alone that it is the murder weapon or that Maya handled it.

#### `EV-14` — Fatal-injury / weapon correspondence (PROPOSED)
- **Type / source:** A documented comparison of the injury description, scene inventory, and calibration object.
- **Location / interaction:** `medical_bay` with authorized `wet_lab` observations.
- **Prerequisites:** `EV-11` complete and `EV-13` recorded; physical detail and access protocol **TBD**.
- **Player receives:** The injury is consistent with a blow from the type of calibration object present in the laboratory. Combined with `EV-11` excluding the apparatus and `EV-13` documenting the object anomaly, this supports its use as the weapon; exact physical corroboration remains **TBD**.
- **Supports:** `blunt_force_method_supported`. Staging may be supported separately by the scene observations and wider reconstruction; object correspondence alone does not establish it.
- **Does not prove:** Whose hand held the object, intent from injury correspondence alone, or the exact staging actions. Avoid claiming a shipboard medic performed an implausible full forensic lab analysis.

### 4.4 Maya's improvement and movement evidence

#### `EV-15` — Scientific revision / authorship history (FIXED concept; PROPOSED artifact)
- **Type / source:** Research code commit history, dataset annotations, or experiment revision log.
- **Location / object:** `dry_lab` / `dry_lab_analysis_terminal`.
- **Access:** Ordinary audit access to relevant shared research work. The reference in Elena's preserved M-17 records provides an authored lead here; direct discovery through legitimate research navigation remains possible. Exact revision identifier and reference wording are **TBD**.
- **Player receives:** Maya contributed a significant improvement separate from the project's inflated existing results.
- **Supports:** `maya_improvement_identified`.
- **Does not prove:** Theft, an unauthorized sale, or murder.

#### `EV-16` — Competitor transfer proposal (FIXED concept; PROPOSED artifact)
- **Type / source:** A draft agreement discovered during the investigation. A message trail may corroborate it but does not replace the established draft.
- **Location / object:** `dry_lab` shared project records **or** `cabin_maya` with appropriate authorization; placement **TBD**.
- **Access:** Specific permitted/consensual evidence disclosure; not free access to private accounts.
- **Player receives:** Maya discussed transferring nonpublic research to a competing organization in exchange for personal and career benefits.
- **Supports:** `maya_transfer_plan_supported`.
- **Does not prove:** That a transfer was completed, or that she killed Elena.

#### `EV-17` — Elena's preserved notes (FIXED concept; PROPOSED storage)
- **Type / source:** Notebook, independent data archive, or preserved correspondence; exact medium **TBD**.
- **Location / object:** `cabin_elena` / `cabin_desk_elena` **or** a valid research archive, **TBD**.
- **Access:** Permission from Sarah for evidence preservation, or a legitimate audit route. Provide an understandable lead to its storage.
- **Player receives:** Elena knew about Maya's negotiations and intended to prevent the planned transfer and report the negotiations. She had not seen the draft agreement found as `EV-16`; her notes must not imply otherwise. The notes may also point back to the M-17 discrepancy.
- **Supports:** `elena_knew_of_maya_negotiations`, `maya_motive_established` when combined with `EV-16`.
- **Does not prove:** Who physically attacked Elena.
- **TBD supporting entries:** Sarah's admission/audit concern and Lucas's recording incident may appear as separate entries here, linked to `EV-21` and `EV-22`. Exact content and independent corroboration remain open; notes are not automatic proof of every interpretation.

#### `EV-18` — Partial corridor recording / media metadata (FIXED possibility; PROPOSED clip)
- **Type / source:** Lucas's documented recording and its timestamp metadata.
- **Location / object:** `editing_room` / `editing_workstation` or `media_drive_case`.
- **Access:** Lucas willingly shares relevant footage or Sarah authorizes preservation/review; exact flow **TBD**.
- **Player receives (proposed):** A partial view indicating Maya moved toward the laboratory area during the critical window, without showing the actual confrontation or murder. Exact field of view/time **TBD**.
- **Supports:** `maya_wet_lab_area_presence_supported` when compared to her stated alibi.
- **Does not prove:** Entry through a specific door, the murder act, or precise time of death.
- **Consistency note:** The wet and dry labs also have an internal connecting door. Camera coverage must not imply an impossible view of both routes.

#### `EV-19` — Maya's contradictory statement (PROPOSED)
- **Type / source:** A persisted conversation admission or claim, compared with independent records.
- **Location / interaction:** Talk with Maya anywhere she is legitimately present.
- **Access:** Conversation; the game must persist her first material claim before permitting a contradiction check.
- **Player receives:** Maya's initial account is inconsistent with `EV-18` or another independently authored trace.
- **Supports:** `maya_alibi_contradicted`.
- **Does not prove:** Automatically that she murdered Elena.
- **Dependency:** Maya's precise claimed alibi is **TBD** and must be fixed across Story, Character, and Evidence Bibles before this clue is production-ready.

### 4.5 Support and optional clues

#### `EV-20` — Dinner argument testimony (PROPOSED)
- **Type / source:** Cross-checked recollections from participants.
- **Location / interaction:** `mess_hall` or permitted NPC conversations.
- **Player receives:** Elena refused to endorse publication at dinner; witnesses recall escalating tension.
- **Supports:** Context for Thomas's financial motive and general pressure.
- **Does not prove:** The murderer's identity or the timing of the fatal confrontation.

#### `EV-21` — Sarah's operational decision (PROPOSED, optional)
- **Type / source:** Bridge/weather log or Sarah's admission.
- **Location / object:** `bridge` / `bridge_log_station`.
- **Player receives:** Sarah continued operations under commercial pressure despite reservations.
- **Supports:** Her defensiveness and the ship's strained atmosphere.
- **TBD link to `EV-17`:** Prefer an entry in Elena's notes recording Sarah's private admission and Elena's intention to include the operational decision in the audit. Exact wording, detail, and corroborating records remain undecided; the underlying exchange is established in Story §4.3.
- **Does not prove:** Any causal link to Elena's murder.

#### `EV-22` — Lucas's unauthorized recording practice (PROPOSED, optional)
- **Type / source:** Shot list, file metadata, or a candid conversation.
- **Location / object:** `editing_room` / `editing_shot_list`.
- **Player receives:** Lucas recorded more than he openly disclosed, explaining why he initially withholds material.
- **Supports:** His conflicting incentives and access to some independent observations.
- **TBD link to `EV-17`:** Prefer an entry in Elena's notes about noticing Lucas recording beyond the agreed session and challenging him. Exact session, wording, detail, any threat to report him, and corroboration remain undecided. Do not assume this is the recording used for `EV-18`.
- **Does not prove:** That all rooms were monitored or that his recordings are complete.

### 4.6 Noah Bennett's injury — optional supporting thread

**Fixed history and boundaries:** Eight months before the murder, Noah Bennett sustained a hand injury and left for treatment and recovery without permanent disability. He is a former crew member, not aboard or an additional murder-night witness. Elena, Olivia, Maya, Daniel, Thomas, and Sarah know the basic history; Lucas joined later and initially knows nothing, as does the player. Among the established cast, only Elena and Olivia initially know that Olivia recorded an ordinary handling accident while omitting a prior report of an unsafe securing mechanism. Exact equipment, injury, reporting chain, and how Elena learned the truth remain TBD (Story §4.4).

#### `EV-23` — Lead about Noah's injury (PROPOSED, optional)
- **Type / source:** A possible note by Elena, or an explicitly requested account from a character who knows the incident; exact route TBD.
- **Location / object:** TBD; a note may share `EV-17`'s eventual authorized storage. No additional object or location is established here.
- **Player receives:** The basic injury, departure, and recovery history; any note's exact wording and separation of facts from suspicions remain TBD.
- **Supports:** A specific question about Noah and a lead to authorized incident-record review.
- **Does not prove:** Olivia's omission, negligence in treatment, or any connection to the murder.

#### `EV-24` — Noah's misleading incident account (FIXED concept; PROPOSED artifact, optional)
- **Type / source:** The account Olivia recorded as an ordinary handling accident.
- **Location / object:** Proposed authorized review through `medical_bay` / `medical_records_terminal`; actual record type, storage, and access TBD.
- **Player receives:** What the recorded account says; it does not mention the prior warning.
- **Does not prove:** By itself that a warning existed or that the omission was deliberate; requires corroboration.

#### `EV-25` — Corroboration of the prior safety warning (FIXED underlying fact; PROPOSED artifact, optional)
- **Type / source:** Preserved warning or other independently supported account; exact evidence, author, recipient, date, provenance, storage, and access TBD.
- **Player receives:** Evidence that the unsafe securing mechanism had been reported before Noah's injury.
- **Supports:** Comparison with `EV-24` and a specific confrontation about Olivia's misleading account. Define what supports her knowledge of the warning and the conditions for her admission before implementation.
- **Does not prove:** A connection to the ecological incident, the current sampling-apparatus fault, inadequate treatment, or Elena's murder. Do not assign knowledge of the warning to Sarah or Daniel by default.

**Disclosure and access:** Characters do not volunteer this incident in greetings or general equipment/Elena discussion. Reading a clue alone does not trigger disclosure; the player must explicitly ask about Noah or the incident. Maya, Daniel, Thomas, and Sarah provide only the basic history unless they receive more evidence in play. Olivia's admission follows authored evidence-response conditions. Lucas must not claim prior knowledge or firsthand recollection. Private records require specific authorization; clue acquisition does not automatically brief every NPC.

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
EV-06 Old environmental report -> EV-07 Withheld record (optional depth)
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
| Sarah's compromise, Lucas's privacy lapse, Daniel's full past cover-up, Olivia's misleading injury account | `EV-07`, `EV-21`–`EV-25` | **Optional depth** |

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
| `dry_lab` | `EV-00`–`EV-06`, `EV-15`; possibly `EV-16` | Existing scientific audit rights; sensitive accounts remain restricted. |
| `wet_lab` | `EV-12`, `EV-13` | Initially secured after the body is found; later supervised inspection only. |
| `medical_bay` | `EV-10`, `EV-11`, `EV-14` | Olivia provides appropriately scoped observations; definitive reconstruction is gated. |
| `engineering_workshop` | `EV-07`–`EV-09` | Sarah's permission or Daniel's supervised cooperation. |
| `editing_room` | `EV-18`, `EV-22` | Lucas's cooperation or authorized preservation. |
| `crew_quarters` / `cabin_elena` | `EV-17` if stored there | Permission/authorization; exact placement TBD. |
| `crew_quarters` / `cabin_maya` | `EV-16` only if placed there | No unrestricted cabin search; exact mechanism TBD. |
| `mess_hall` | `EV-20` | Open social area. |
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
- Fixed timestamps match the Story Bible: **18:10, 21:10, 22:20, 22:35, ~22:45, 23:10, 07:00**.
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
- [ ] Lucas cannot provide recordings from nonexistent cameras.
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
| **Exact medical / mechanical distinction and temporal plausibility** | Define EV-11's observations, timestamps, and uncertainty; check whether they establish death before 23:10 or require an explicit revision to the Story Bible's player-proof requirement. Supports EV-14 without inventing forensic precision. | Story, Olivia, Daniel, World |
| **Actual comparative evidence and authorized access needed for reconstruction** | Supports a defensible conclusion without requiring either motive confrontation. | Story, Olivia, Evidence |
| **Maya's exact false alibi** | Needed to make `EV-18` + `EV-19` a fair contradiction. | Maya, Lucas, Story |
| **Lucas's camera placement, clip contents, metadata, and recording time** | Prevents implausible coverage or an all-solving video. | Lucas, World |
| **Calibration object's specific trace / movement** | Connects staging and method without an unrealistic instant lab test. | Story, World, Olivia |
| **Elena's preserved notes and how the player finds them** | Ensures the initial hint leads fairly to the transfer motive. | Story, World |
| **Competitor agreement's storage and access permissions** | Prevents arbitrary search of Maya's private material. | Maya, World |
| **Exact evidence for Thomas's approval of misleading claims** | Supports a strong motive without implying he killed Elena. | Thomas, Story |
| **Who discovers Elena and how the scene is preserved** | Determines the first official report and initial observations. | Story, Sarah, Olivia |
| **Elena's notes linking Sarah and Lucas to their secrets** | Prefer entries within `EV-17`, linked to `EV-21`/`EV-22`; decide wording, discovery, and corroboration without inventing incident details. | Story §4.3, Sarah, Lucas |
| **Check that the combined evidence distinguishes Maya from another attacker** | Test whether the final reconstruction rules out a plausible later attacker or alternative sequence through authored alibis, timing, and/or attack/staging traces. Motive, nearby presence, and a lie alone are insufficient; precise clues remain TBD. | Story, all Character Bibles, World, Evidence |
| **Other suspects' exact alibis** | Needed for coherent interrogation and elimination. | All Character Bibles, Story |
| **Exact carbon-removal technology and example M-17 numbers** | Makes scientific evidence understandable without inventing unsound science. | Story, World |
| **Noah's incident evidence, potential Elena note, and disclosure thresholds** | Defines `EV-23`–`EV-25` without inventing warning recipients, shared secret knowledge, or a link to the murder. | Story §4.4, Olivia, other Character Bibles, World |
| **Final accusation behavior and optional ending variants** | Controls whether a wrong guess ends the game or allows further investigation. | Story, game design |

**Recommended order to resolve:** (1) precise alibis and recording, (2) physical/medical mechanism, (3) reconstruction evidence and access requirements, (4) clue placement and permission paths, (5) numeric data and presentation details.

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
