import {slot} from "./save-slot.js";

const el = id => document.getElementById(id);
const panel = el("dialogue");
const field = el("question");
const choices = el("choices");
const transcript = panel.querySelector(".transcript");
const marker = slot + ".dialogue";
const limit = 500;
const failedLine = "There is a pause. No answer comes.";

async function queued(endpoint, body, signal) {
  const path = "/gradio_api/call/" + endpoint;
  const response = await fetch(path, {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({data: [body]}), signal
  });
  if (!response.ok) throw new Error("Queue unavailable");
  const {event_id: id} = await response.json();
  signal.throwIfAborted();
  return new Promise((resolve, reject) => {
    const stream = new EventSource(path + "/" + encodeURIComponent(id));
    const close = () => { stream.close(); signal.removeEventListener("abort", abort); };
    const abort = () => { close(); reject(new Error("Left conversation")); };
    signal.addEventListener("abort", abort, {once: true});
    stream.addEventListener("complete", event => {
      close();
      try { resolve(JSON.parse(event.data)[0]); } catch (error) { reject(error); }
    });
    stream.onerror = () => { close(); reject(new Error("Reply unavailable")); };
  });
}

export function setupDialogue({currentSave, commit, canPlay, saving, refreshJournal}) {
  let state, person, pending, timer, retry, menu, opening = true;

  let replyDone, finishReply;
  function remember(waiting = false) {
    try {
      if (person && saving()) sessionStorage.setItem(marker, JSON.stringify({npc: person.id, waiting}));
      else sessionStorage.removeItem(marker);
    } catch { /* Session-only mode carries the conversation in memory. */ }
  }

  function tell(text) {
    const line = document.createElement("p");
    line.textContent = text;
    el("spoken").append(line);
  }

  function note(text) {
    if (!text && !saving()) text = "Saving is off. This conversation lasts until you reload or close this tab.";
    el("dialogue-note").textContent = text;
    el("dialogue-note").hidden = !text;
  }

  function append({role, content}) {
    const item = document.createElement("li");
    item.className = "line-" + role;
    if (role === "assistant" || role === "user") {
      const label = document.createElement("span");
      label.className = "line-label";
      label.textContent = role === "user" ? "You" : person.name;
      item.append(label);
    }
    const text = document.createElement("p");
    text.dir = "auto";
    text.textContent = content;
    item.append(text);
    el("lines").append(item);
    el("empty").hidden = true;
  }

  function history() {
    const top = transcript.scrollTop;
    const reading = el("journal").open && top + transcript.clientHeight < transcript.scrollHeight - 2;
    el("lines").replaceChildren();
    el("empty").hidden = false;
    (state.history?.[person.id] || []).forEach(append);
    transcript.scrollTop = reading ? top : transcript.scrollHeight;
  }

  function buttons() {
    const length = Array.from(field.value).length;
    el("counter").textContent = length + " / " + limit;
    const invalid = length > limit;
    field.setAttribute("aria-invalid", String(invalid));
    field.readOnly = Boolean(pending);
    el("send").textContent = retry ? "Retry" : "Send";
    el("send").setAttribute("aria-disabled", String(Boolean(pending) || invalid ||
      (!field.value.trim() && !retry)));
    el("present-case").hidden = person?.id !== "sarah_morgan";
    el("present-case").disabled = Boolean(pending);
    el("topics-toggle").hidden = !state?.view.topics.some(t => t.npc === person?.id);
    for (const id of ["topics-toggle", "evidence-toggle"]) {
      el(id).disabled = Boolean(pending);
      el(id).setAttribute("aria-expanded", String(menu === id));
    }
  }

  function showMenu(id) {
    menu = id;
    choices.replaceChildren();
    choices.hidden = !id;
    if (id) {
      const topics = id === "topics-toggle";
      const options = topics ? state.view.topics.filter(t => t.npc === person.id) : state.view.evidence;
      for (const option of options) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = topics ? option.label : option.name;
        button.onclick = () => submit(topics ? "topic" : "talk", option);
        choices.append(button);
      }
      if (!options.length) choices.textContent = "You have no evidence to show.";
    }
    buttons();
  }

  function stopWaiting() {
    clearInterval(timer);
    pending?.abort();
    pending = null;
    finishReply?.();
    finishReply = null;
    el("thinking").hidden = true;
  }

  function clearReaction() {
    if (!el("reaction").hidden) {
      el("reaction").hidden = true;
      refreshJournal();
    }
  }

  function leave() {
    if (!person) return;
    const opener = document.querySelector('[data-npc="' + CSS.escape(person.id) + '"]');
    stopWaiting();
    clearReaction();
    person = null;
    remember();
    panel.close();
    (opener?.isConnected && !opener.disabled ? opener : el("room")).focus({preventScroll: true});
    el("spoken").replaceChildren();
    el("lines").replaceChildren();
    choices.replaceChildren();
  }

  function open(id, interrupted = false) {
    if (!canPlay()) return;
    person = state?.view.npcs_present.find(p => p.id === id);
    if (!person) return;
    el("speaker-role").textContent = person.role;
    el("speaker-name").textContent = person.name;
    // Approved portraits can later use this slot as the image source.
    el("portrait").querySelector("img").dataset.src = "/static/art/characters/" + person.id + ".webp";
    retry = null;
    field.value = "";
    showMenu(null);
    el("spoken").replaceChildren();
    panel.showModal();
    window.scrollTo(0, 0);
    history();
    note(interrupted ? "You left before the answer. Ask again to continue." : "");
    remember();
    field.focus({preventScroll: true});
  }

  async function submit(endpoint, option) {
    if (pending || !person || !canPlay()) return;
    const message = field.value;
    if (Array.from(message).length > limit || (endpoint === "talk" && !option && !message.trim())) return;
    clearReaction();
    const expected = currentSave();
    const ticket = new AbortController();
    const current = () => pending === ticket && !ticket.signal.aborted && currentSave() === expected;
    const data = {save: expected, target: person.id};
    let outgoing;
    if (endpoint === "topic") {
      data.topic = option.id;
      outgoing = option.label;
    } else {
      data.message = message;
      data.present = option ? [option.id] : [];
      outgoing = ((option ? "[I show you: " + option.name + "] " : "") + message.trim()).trim();
    }
    retry = null;
    pending = ticket;
    replyDone = new Promise(resolve => { finishReply = resolve; });
    const start = performance.now();
    showMenu(null);
    append({role: "user", content: outgoing});
    tell("You: " + outgoing);
    if (endpoint === "talk") field.value = "";
    field.focus({preventScroll: true});
    buttons();
    el("thinking").textContent = person.name + " is thinking…";
    el("thinking").hidden = false;
    transcript.scrollTop = transcript.scrollHeight;
    note("Leaving before the answer discards this exchange.");
    remember(true);
    timer = setInterval(() => {
      const seconds = Math.floor((performance.now() - start) / 1000);
      if (seconds >= 2) el("thinking").textContent = person.name + " is thinking… " + seconds + " s";
    }, 200);
    let acknowledged = false;
    try {
      const result = await queued(endpoint, data, ticket.signal);
      if (!current()) return;
      if (result.error) throw new Error(result.error);
      if (!await commit(result, expected, current)) {
        if (current()) {
          history();
          field.value = message;
          retry = {endpoint, option};
          note("The investigation has changed. Try your question again.");
        }
        return;
      }
      if (pending !== ticket) return;
      acknowledged = true;
      // The engine may retain deterministic evidence effects even if the voice failed.
      if (result.retryable) {
        field.value = message;
        retry = {endpoint, option};
      }
      if (result.reply) tell(person.name + ": " + result.reply);
      if (result.message) tell(result.message);
      for (const line of (result.history[person.id] || []).slice().reverse()) {
        if (line.role !== "notice") break;
        tell(line.content);
      }
      note("");
    } catch (error) {
      if (!current()) return;
      history();
      const explanation = error.message === "save_limit" ? "This exchange would exceed the save size limit." : failedLine;
      append({role: "narration", content: explanation});
      tell(explanation);
      field.value = message;
      retry = {endpoint, option};
      note("");
    } finally {
      if (pending === ticket) {
        stopWaiting();
        // Navigation can close the event stream before pagehide. A transport
        // failure must leave the reload marker until the player acknowledges it.
        remember(!acknowledged);
        buttons();
        if (!el("journal").open) transcript.scrollTop = transcript.scrollHeight;
      }
    }
  }

  el("people").addEventListener("click", e => {
    const button = e.target.closest("[data-npc]");
    if (button) open(button.dataset.npc);
  });
  panel.addEventListener("cancel", e => { e.preventDefault(); leave(); });
  el("leave").onclick = leave;
  window.addEventListener("resize", () => {
    if (panel.open) transcript.scrollTop = transcript.scrollHeight;
  });
  field.oninput = () => {
    const tooLong = Array.from(field.value).length > limit;
    if (tooLong || field.getAttribute("aria-invalid") === "true") {
      note(tooLong ? "Shorten your question to 500 characters." : "");
    }
    if (retry && !retry.option) retry = null;
    buttons();
  };
  el("composer").onsubmit = e => { e.preventDefault(); submit(retry?.endpoint || "talk", retry?.option); };
  for (const id of ["topics-toggle", "evidence-toggle"]) {
    el(id).onclick = () => { clearReaction(); showMenu(menu === id ? null : id); };
  }

  return {
    leave,
    waiting: () => Boolean(pending),
    afterReply: () => pending ? replyDone : undefined,
    update(result, writable, ownCommit = false) {
      const changed = state?.save !== result.save;
      const previousHistory = state?.history?.[person?.id];
      state = result;
      if (person && (!writable || !result.view.npcs_present.some(p => p.id === person.id))) leave();
      if (person && changed) {
        const interrupted = pending && !ownCommit;
        if (interrupted) {
          stopWaiting();
          remember();
          note("The investigation continued in another tab. Ask again to continue.");
        }
        if (interrupted || JSON.stringify(previousHistory) !== JSON.stringify(result.history?.[person.id])) history();
        showMenu(menu);
      }
      if (opening) {
        opening = false;
        if (!saving() || !writable) return;
        try {
          const saved = JSON.parse(sessionStorage.getItem(marker));
          if (saved) open(saved.npc, saved.waiting);
        } catch { /* Restoring a dialogue is optional. */ }
      }
    }
  };
}
