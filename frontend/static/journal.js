import {slot} from "./save-slot.js";

const el = id => document.getElementById(id);
const dialog = el("journal");
const page = el("book-page");
const scroll = el("book-scroll");
const openers = document.querySelectorAll(".journal-open");
const names = {evidence: "Evidence", statements: "Statements", leads: "Leads", compare: "Compare entries"};

function node(tag, text, cls) {
  const out = document.createElement(tag);
  if (text !== undefined) out.textContent = text;
  if (cls) out.className = cls;
  return out;
}

function button(text, action, key, cls) {
  const out = node("button", text, cls);
  out.type = "button";
  out.onclick = action;
  out.dataset.key = key;
  return out;
}

function words(tag, text, cls) {
  const out = node(tag, text, cls);
  out.dir = "auto";
  return out;
}

export function setupJournal({review, waiting, saving}) {
  let book, caseId, opener, section = "evidence", selected, mode = "busy";
  let browsingOnly = false;
  let pins = [], prior = new Set(), offsets = new Map();
  const pending = new Set();
  let reviewQueue = Promise.resolve();

  function stamp() {
    return [
      ...book.evidence.map(e => e.id),
      ...book.statements.map((_, i) => "statement-" + i),
      ...book.leads.map(text => "lead-" + text)
    ];
  }

  function hint(text) {
    const status = el("book-status");
    status.textContent = text;
    status.hidden = !text;
  }

  function availability() {
    const available = book && (mode === "ready" || mode === "readonly");
    const count = book?.evidence.filter(e => !e.reviewed).length || 0;
    const showCount = book && el("reaction").hidden;
    for (const opener of openers) {
      opener.disabled = !available;
      opener.textContent = showCount ? 'Journal · ' + count : "Journal";
      opener.setAttribute("aria-label", showCount ? 'Journal, ' + count + ' unread evidence' : "Journal");
    }
    if (!book || !dialog.open) return;
    if (browsingOnly) hint("Read-only journal.");
    else if (mode === "readonly") hint("Read-only in this tab. Take over in the room to mark evidence as reviewed.");
    else if (mode === "busy") hint("Updating the investigation…");
    else if (mode !== "ready") hint("Close the journal to return to the investigation and continue.");
    else if (pending.size && waiting()) hint("Your review will be recorded after the reply.");
    else if (!saving()) hint("Saving is off. Journal progress lasts until you reload or close this tab.");
    else hint("");
  }

  function mark(item) {
    if (browsingOnly || item.reviewed || !["ready", "busy"].includes(mode) || pending.has(item.id)) return;
    const investigation = caseId;
    pending.add(item.id);
    availability();
    reviewQueue = reviewQueue.then(async () => {
      if (caseId === investigation && !book.evidence.find(e => e.id === item.id)?.reviewed) {
        await review(item.id, investigation);
      }
    }).finally(() => {
      pending.delete(item.id);
      availability();
    });
  }

  function currentPage() { return selected || section; }

  function navigate(destination, entry) {
    offsets.set(currentPage(), scroll.scrollTop);
    section = destination;
    selected = entry;
    draw();
    scroll.scrollTop = offsets.get(currentPage()) || 0;
    page.querySelector("h3").focus({preventScroll: true});
  }

  function openEvidence(id) {
    const entry = book.evidence.find(e => e.id === id);
    if (!entry) return;
    navigate("evidence", id);
    mark(entry);
  }

  function pinControl(id) {
    const included = pins.includes(id);
    const control = button(included ? "Remove from comparison" : "Add to comparison", () => {
      if (included) pins = pins.filter(key => key !== id);
      else if (pins.length < 2) pins.push(id);
      draw();
      (page.querySelector('[data-key="' + CSS.escape("pin-" + id) + '"]') || el("compare-open")).focus();
    }, "pin-" + id, "pin-control");
    control.disabled = !included && pins.length === 2;
    return control;
  }

  function list(values, render, ordered = false) {
    const out = node(ordered ? "ol" : "ul");
    for (const value of values) {
      const li = node("li");
      li.append(render(value));
      out.append(li);
    }
    return out;
  }

  function evidenceBody(e) {
    const body = node("div", undefined, "record-body");
    function field(label, content) {
      body.append(node("h4", label), content);
    }
    field("Observed", words("p", e.observed));
    if (e.interpretation) field("Interpretation", words("p", e.interpretation));
    if (e.questions.length) field("Questions", list(e.questions, q => words("span", q)));
    if (e.people.length) field("Related people", list(e.people, n => words("span", n)));
    if (e.related.length) field("Related evidence", list(e.related, id => {
      const linked = book.evidence.find(item => item.id === id);
      const link = node("a", linked.name);
      link.href = "#book-page";
      link.dataset.key = "related-" + e.id + "-" + id;
      link.onclick = event => { event.preventDefault(); openEvidence(id); };
      return link;
    }));
    return body;
  }

  function badge(text) { return node("span", text, "book-mark" + (text === "Unread" ? " unread" : "")); }

  function heading(title) {
    const h = words("h3", title, "page-heading");
    h.tabIndex = -1;
    h.dataset.key = "heading";
    return h;
  }

  function draw() {
    const focus = page.contains(document.activeElement) && document.activeElement.dataset.key;
    const fragment = document.createDocumentFragment();
    for (const tab of dialog.querySelectorAll("[data-section]")) {
      tab.setAttribute("aria-current", String(section === tab.dataset.section));
    }
    const compare = el("compare-open");
    compare.setAttribute("aria-current", String(section === "compare"));
    compare.textContent = 'Compare (' + pins.length + '/2)';
    if (selected) {
      const e = book.evidence.find(item => item.id === selected);
      const actions = node("div", undefined, "entry-tools");
      actions.append(button("← Evidence index", () => navigate("evidence"), "index", "back-index"), pinControl(e.id));
      fragment.append(actions, heading(e.name), evidenceBody(e));
    } else {
      fragment.append(heading(names[section]));
      if (section === "evidence") {
        const index = list(book.evidence, e => {
          const row = button("", () => openEvidence(e.id), "open-" + e.id, "index-entry");
          row.append(words("span", e.name));
          const marks = node("span", undefined, "marks");
          if (!prior.has(e.id)) marks.append(badge("New"));
          if (!e.reviewed) marks.append(badge("Unread"));
          row.append(marks, node("span", "→", "row-arrow"));
          row.lastChild.setAttribute("aria-hidden", "true");
          return row;
        });
        index.className = "book-index";
        fragment.append(index);
      } else if (section === "statements") {
        const groups = new Map();
        book.statements.forEach((s, i) => {
          if (!groups.has(s.speaker)) groups.set(s.speaker, []);
          groups.get(s.speaker).push({...s, id: "statement-" + i});
        });
        if (!groups.size) fragment.append(node("p", "No statements recorded yet."));
        for (const [speaker, group] of groups) {
          const items = list(group.sort((a,b) => a.turn - b.turn), s => {
            const article = node("article");
            article.append(node("span", "Turn " + s.turn, "turn-label"));
            if (!prior.has(s.id)) article.append(badge("New"));
            article.append(words("p", s.text), pinControl(s.id));
            return article;
          }, true);
          items.className = "statement-list";
          fragment.append(words("h4", speaker, "speaker-heading"), items);
        }
      } else if (section === "leads") {
        if (!book.leads.length) fragment.append(node("p", "No active leads."));
        fragment.append(list(book.leads, text => {
          const lead = node("div", undefined, "lead-entry");
          lead.append(words("p", text));
          if (!prior.has("lead-" + text)) lead.append(badge("New"));
          return lead;
        }, true));
      } else {
        const spread = node("div", undefined, "compare-spread");
        for (const id of pins) {
          const article = node("article");
          const entry = book.evidence.find(e => e.id === id);
          if (entry) article.append(node("span", "Evidence", "turn-label"), words("h4", entry.name, "compare-title"), evidenceBody(entry));
          else {
            const s = book.statements[Number(id.slice("statement-".length))];
            article.append(node("span", "Statement · Turn " + s.turn, "turn-label"),
              words("h4", s.speaker, "compare-title"), words("p", s.text));
          }
          article.append(pinControl(id));
          spread.append(article);
        }
        if (pins.length < 2) spread.append(node("p", "Choose “Add to comparison” on an evidence entry or statement.", "compare-empty"));
        fragment.append(spread);
      }
    }
    page.replaceChildren(fragment);
    if (focus) page.querySelector('[data-key="' + CSS.escape(focus) + '"]')?.focus({preventScroll: true});
  }

  function rememberVisit(seen) {
    if (!saving()) return;
    try { sessionStorage.setItem(slot + ".visit", JSON.stringify({caseId, seen: [...seen]})); }
    catch { /* The current tab still remembers visits in memory. */ }
  }

  function open(from, destination, readOnly = false) {
    if (dialog.open || !book || !["ready", "readonly"].includes(mode)) return;
    browsingOnly = readOnly;
    if (destination) { section = destination; selected = null; }
    opener = from;
    draw();
    dialog.showModal();
    rememberVisit(stamp());
    scroll.scrollTop = offsets.get(currentPage()) || 0;
    availability();
  }

  function close() {
    if (!dialog.open) return;
    offsets.set(currentPage(), scroll.scrollTop);
    prior = new Set(stamp());
    rememberVisit(prior);
    dialog.close();
    page.replaceChildren();
    const destination = opener?.isConnected && !opener.disabled && opener.getClientRects().length
      ? opener : el("room");
    destination.focus({preventScroll: true});
  }

  for (const trigger of openers) trigger.onclick = () => open(trigger);
  for (const tab of dialog.querySelectorAll("[data-section]")) tab.onclick = () => navigate(tab.dataset.section);
  el("compare-open").onclick = () => navigate("compare");
  el("close-journal").onclick = close;
  dialog.addEventListener("cancel", event => { event.preventDefault(); close(); });
  document.addEventListener("keydown", event => {
    if (event.defaultPrevented || event.repeat || event.isComposing || event.key.toLowerCase() !== "j" ||
        event.ctrlKey || event.metaKey || event.altKey || waiting() ||
        event.target.closest("input, textarea, select, [contenteditable]:not([contenteditable=false])")) return;
    if (!dialog.open && !document.querySelector("#decision[open]") && ["ready", "readonly"].includes(mode)) {
      event.preventDefault();
      open(document.activeElement, undefined, !el("ending").hidden || el("case-file").open);
    }
  });

  return {
    open, close, refresh: availability,
    mode(next) { mode = next; availability(); },
    clear() { close(); book = null; caseId = null; page.replaceChildren(); availability(); },
    unread(id) { return Boolean(book?.evidence.some(e => e.id === id && !e.reviewed)); },
    update(result) {
      book = result.journal;
      if (caseId !== result.case) {
        caseId = result.case;
        pins = []; selected = null; section = "evidence"; prior = new Set(); offsets.clear();
        try {
          const previous = JSON.parse(sessionStorage.getItem(slot + ".visit"));
          if (previous?.caseId === caseId) prior = new Set(previous.seen);
        } catch { /* Optional visit history. */ }
      }
      const available = new Set(stamp());
      pins = pins.filter(id => available.has(id));
      if (selected && !available.has(selected)) selected = null;
      if (dialog.open) draw();
      availability();
    }
  };
}
