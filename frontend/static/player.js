import {setupJournal} from "./journal.js";
import {setupDialogue} from "./dialogue.js";
import {clearRoom, loadLayout, showRoom} from "./scene.js";
import {isSlotChange, openFallback, readSave, slot, StorageUnavailable, writeSave} from "./save-slot.js";

const locks = navigator.locks;
const channel = locks && typeof BroadcastChannel === "function" ? new BroadcastChannel(slot) : null;
const scene = document.querySelector(".scene");
const recovery = document.getElementById("recovery");
const withoutSaving = document.getElementById("without-saving");
const message = document.getElementById("message");
const elapsed = document.getElementById("elapsed");
const room = document.getElementById("room");
const note = document.getElementById("session-note");
const notice = document.getElementById("temporary-notice");
const defaultMessage = "Select an object to inspect it, or an exit to move.";
const elsewhere = "The game is open in another tab. Take over to play here.";
const recoveryLabels = {
  error: "Retry", storage: "Retry", invalid: "New game",
  limit: "Return to investigation", readonly: "Take over",
};
let displayed;
let currentCase;
let actionDone;
let running = false;
let syncPending = false;
let retry;
let continueSession;
let fallback;
let established = false;
let sessionOnly = false;
let mode = "busy";
let lastObservation = defaultMessage;
let timer;
let seenTemporaryKey;

const dialogue = setupDialogue({
  currentSave: () => displayed, canPlay: () => mode === "ready",
  saving: () => !sessionOnly, commit: commitDialogue
});

const journal = setupJournal({
  review: async (id, caseId) => {
    await dialogue.afterReply();
    while (running) await actionDone;
    if (mode === "ready" && currentCase === caseId && journal.unread(id)) await perform("review", id);
  },
  waiting: () => dialogue.waiting(), saving: () => !sessionOnly
});

function status(next, text) {
  mode = next;
  journal.mode(next);
  document.body.dataset.mode = next;
  scene.setAttribute("aria-busy", String(next === "busy"));
  for (const button of scene.querySelectorAll("button")) {
    button.setAttribute("aria-disabled", String(next !== "ready"));
  }
  for (const button of document.querySelectorAll("#people button")) button.disabled = next !== "ready";
  message.textContent = text;
  if (next === "busy") {
    // Keep an activated recovery button mounted and focused during its request.
    recovery.setAttribute("aria-disabled", "true");
    return;
  }
  clearInterval(timer);
  elapsed.hidden = true;
  withoutSaving.hidden = next !== "storage";
  recovery.hidden = !recoveryLabels[next];
  recovery.setAttribute("aria-disabled", "false");
  if (!recovery.hidden) {
    recovery.textContent = recoveryLabels[next];
    if (next !== "readonly" || scene.contains(document.activeElement)) {
      recovery.focus({preventScroll: true});
    }
  }
}

function startTimer(button) {
  if (!button) return;
  const started = performance.now();
  elapsed.style.setProperty("--origin-x", button.offsetLeft + button.offsetWidth / 2 + "px");
  elapsed.style.setProperty("--origin-y", button.offsetTop + button.offsetHeight / 2 + "px");
  timer = setInterval(() => {
    const seconds = Math.floor((performance.now() - started) / 1000);
    if (seconds < 2) return;
    elapsed.textContent = `Working… ${seconds} s`;
    elapsed.hidden = false;
  }, 250);
}

function showTemporaryNotice(id) {
  if (!id || seenTemporaryKey === id) return;
  seenTemporaryKey = id;
  const key = slot + ".temporary-key-seen";
  if (!sessionOnly) {
    try {
      if (localStorage.getItem(key) === id) return;
      localStorage.setItem(key, id);
    } catch { /* Session storage can still remember the notice. */ }
  }
  try {
    if (sessionStorage.getItem(key) === id) return;
    sessionStorage.setItem(key, id);
  } catch { /* The in-memory check still prevents repeat notices on this page. */ }
  notice.hidden = false;
}

async function request(action, save, target) {
  const response = await fetch("/action", {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({action, save, target})
  });
  if (!response.ok) throw new Error("Request failed");
  const result = await response.json();
  showTemporaryNotice(result.temporary_save);
  return result;
}

function render(result, save, writable, ownDialogue = false, keepObservation = false) {
  currentCase = result.case;
  displayed = save;
  const recoveryFocused = document.activeElement === recovery || document.activeElement === withoutSaving;
  showRoom(result.view);
  lastObservation = ownDialogue || keepObservation ? lastObservation : result.message || defaultMessage;
  status(writable ? "ready" : "readonly", writable ? lastObservation : elsewhere);
  dialogue.update(result, writable, ownDialogue);
  journal.update(result);
  if (writable && recoveryFocused) room.focus({preventScroll: true});
}

// Slow model calls run outside the save lock. Only the compare-and-write is serialized.
async function commitDialogue(result, expected, current) {
  async function commit() {
    if (!current() || running || mode !== "ready") return false;
    if (!sessionOnly) {
      if (fallback) {
        if (!await fallback.commit(expected, result.save, current)) return false;
      } else {
        if (readSave() !== expected) return false;
        writeSave(result.save);
      }
    }
    render(result, result.save, true, true);
    return true;
  }
  try {
    const applied = locks && !sessionOnly ? await locks.request(slot, commit) : await commit();
    if (!applied) synchronize();
    return applied;
  } catch (error) {
    if (!(error instanceof StorageUnavailable)) throw error;
    dialogue.leave();
    retry = () => perform("sync");
    continueSession = () => {
      sessionOnly = true;
      note.hidden = false;
      fallback?.release().catch(() => {});
      render(result, result.save, true);
    };
    status("storage", error.message);
    return false;
  }
}

async function perform(intent = "sync", target, expected = displayed, button) {
  if (running) {
    if (intent === "sync") syncPending = true;
    return;
  }
  running = true;
  let done;
  actionDone = new Promise(resolve => { done = resolve; });
  const expectedCase = currentCase;
  const previousMode = mode;
  let pending;
  status("busy", intent === "sync" ? "Updating the scene…" : "Action in progress…");
  startTimer(button);
  retry = () => perform(intent, target, expected, button?.isConnected ? button : undefined);
  const execute = async () => {
    while (true) {
      let stored;
      let writable = true;
      if (sessionOnly) {
        stored = displayed ?? null;
      } else if (locks) {
        stored = readSave();
      } else {
        fallback ??= openFallback();
        ({stored, writable} = await fallback.read({initial: !established, takeover: intent === "takeover"}));
        established = true;
        if (intent === "takeover") intent = "sync";
      }

      let action = intent;
      if (intent === "sync" || stored !== expected || !writable) {
        if (stored === displayed && previousMode === "ready" && writable && intent === "sync") {
          status("ready", lastObservation);
          return;
        }
        if (stored === null && !writable) {
          status("readonly", elsewhere);
          return;
        }
        action = stored === null ? "new" : "resume";
      }

      if (action !== "resume" && !sessionOnly) channel?.postMessage("updating");
      await loadLayout();
      let result = await request(action, action === "new" ? null : stored, target);
      if (intent === "review" && action === "resume" && writable && result.case === expectedCase &&
          result.journal?.evidence.some(e => e.id === target && !e.reviewed)) {
        action = "review";
        result = await request(action, stored, target);
      }
      if (!sessionOnly && fallback && (action === "resume" || result.error)) {
        const latest = await fallback.read();
        if (latest.stored !== stored || latest.writable !== writable) {
          intent = "sync";
          continue;
        }
      }
      if (result.error) {
        if (result.error === "invalid_save") {
          // Retain the refused token until the player explicitly starts a new game.
          displayed = stored;
          dialogue.leave();
          journal.clear();
          clearRoom();
        }
        const next = {invalid_save: "invalid", save_limit: "limit"}[result.error] || "error";
        status(writable ? next : "readonly", writable ? result.message : elsewhere);
        return;
      }

      if (action !== "resume" && !sessionOnly) {
        pending = result;
        if (fallback) {
          if (!await fallback.commit(stored, result.save)) {
            pending = undefined;
            intent = "sync";
            continue;
          }
        } else {
          writeSave(result.save);
        }
      }
      render(result, action === "resume" ? stored : result.save, writable, false, intent === "review");
      return;
    }
  };

  try {
    if (locks && !sessionOnly) await locks.request(slot, execute);
    else await execute();
  } catch (error) {
    if (error instanceof StorageUnavailable || error?.name === "SecurityError") {
      continueSession = async () => {
        sessionOnly = true;
        note.hidden = false;
        fallback?.release().catch(() => {});
        if (pending) render(pending, pending.save, true);
        else if (previousMode === "invalid") await perform("new");
        else {
          if (displayed === undefined) {
            try { displayed = readSave(); } catch { /* Start fresh if the save cannot be read. */ }
          }
          await perform();
        }
      };
      const failure = error instanceof StorageUnavailable ? error : new StorageUnavailable(error);
      status("storage", failure.message);
    } else {
      status("error", "The scene could not be updated. Check the connection, then retry.");
    }
  } finally {
    running = false;
    done();
    if (syncPending) {
      syncPending = false;
      synchronize();
    }
  }
}

function synchronize() {
  if (sessionOnly || mode === "storage") return;
  // Events can arrive after a newer write. Always read the current slot.
  try {
    if (locks && !running && mode === "ready" && readSave() === displayed) return;
  } catch { /* perform() displays the storage error and retry control. */ }
  perform();
}

document.addEventListener("keydown", event => {
  if (event.repeat && (event.key === "Enter" || event.key === " ")) event.preventDefault();
});
scene.addEventListener("click", event => {
  const button = event.target.closest(".hotspot");
  if (!button || mode !== "ready" || event.detail > 1) return;
  perform(button.dataset.action, button.dataset.target, displayed, button);
});
recovery.addEventListener("click", () => {
  if (mode === "invalid") perform("new");
  else if (mode === "readonly") perform("takeover");
  else if (mode === "limit") {
    if (displayed != null) {
      status("ready", lastObservation);
      room.focus({preventScroll: true});
    } else {
      perform();
    }
  } else if (mode === "error" || mode === "storage") retry();
});
withoutSaving.addEventListener("click", () => {
  if (mode === "storage") continueSession();
});
document.getElementById("dismiss-temporary").addEventListener("click", () => {
  notice.hidden = true;
  room.focus({preventScroll: true});
});
window.addEventListener("storage", event => {
  if (isSlotChange(event.key)) synchronize();
});
channel?.addEventListener("message", synchronize);
window.addEventListener("pagehide", () => {
  fallback?.release().catch(() => {});
});
window.addEventListener("pageshow", event => { if (event.persisted) synchronize(); });
perform();
