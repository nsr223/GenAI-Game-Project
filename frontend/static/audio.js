// Game audio: music, room ambience, sound effects and the "thinking" hum.
// Self-contained: it reads /static/audio/audio.json and reacts to what the UI already shows,
// so the dialogue, scene and case code need no audio calls. Other code may still call
// window.gameAudio.play("<sfx name>") for events the DOM does not reveal.

const base = "/static/audio/";
const el = id => document.getElementById(id);
let manifest, ctx, master, musicBus, ambienceBus, sfxBus;
const buffers = new Map();
let muted = false;
try { muted = localStorage.getItem("audio.muted") === "1"; } catch { /* storage off: default on */ }

function load(file) {
  if (!buffers.has(file)) {
    buffers.set(file, fetch(base + file)
      .then(r => { if (!r.ok) throw new Error(file); return r.arrayBuffer(); })
      .then(data => ctx.decodeAudioData(data))
      .catch(() => null));
  }
  return buffers.get(file);
}

function ramp(param, value, seconds) {
  const now = ctx.currentTime;
  param.cancelScheduledValues(now);
  param.setValueAtTime(param.value, now);
  param.linearRampToValueAtTime(value, now + seconds);
}

// A looping or one-off source with its own gain, faded in and out.
async function voice(file, bus, {loop = false, volume = 1, fadeIn = 0.02} = {}) {
  const buffer = await load(file);
  if (!buffer) return null;
  const source = ctx.createBufferSource();
  const gain = ctx.createGain();
  source.buffer = buffer;
  source.loop = loop;
  gain.gain.value = 0;
  source.connect(gain).connect(bus);
  source.start();
  ramp(gain.gain, volume, fadeIn);
  return {
    source, gain,
    stop(fade = 0.4) {
      ramp(gain.gain, 0, fade);
      source.stop(ctx.currentTime + fade + 0.05);
    }
  };
}

// ---- music --------------------------------------------------------------
let currentMusic = null, currentTrack = null, musicTicket = 0;
async function music(name, fade = 1.5) {
  if (!manifest || name === currentTrack) return;
  currentTrack = name;
  const ticket = ++musicTicket;
  currentMusic?.stop(fade);
  currentMusic = null;
  const track = manifest.music[name];
  if (!track) return;
  const next = await voice(track.file, musicBus, {loop: track.loop, volume: track.volume, fadeIn: fade});
  if (ticket !== musicTicket) { next?.stop(0.1); return; }
  currentMusic = next;
  // The title theme hands over to the investigation loop once it has played through.
  if (name === "title" && next) next.source.onended = () => { if (currentTrack === "title") music("investigation"); };
}

// ---- ambience -----------------------------------------------------------
const baseLayers = [];
let roomLayer = null, roomFile = null;
async function ambience(roomId) {
  if (!manifest) return;
  const amb = manifest.ambience;
  if (!baseLayers.length) {
    for (const file of amb.base) baseLayers.push(voice(file, ambienceBus, {loop: true, volume: amb.volume, fadeIn: 2}));
  }
  const file = amb.rooms[roomId] || null;
  if (file === roomFile) return;
  roomFile = file;
  roomLayer?.stop(1.2);
  roomLayer = file ? await voice(file, ambienceBus, {loop: true, volume: amb.volume, fadeIn: 1.2}) : null;
}

// ---- one-shot effects ---------------------------------------------------
function play(name) {
  const fx = manifest?.sfx[name];
  if (ctx && fx) voice(fx.file, sfxBus, {volume: fx.volume});
}

// ---- thinking hum -------------------------------------------------------
// Plays while "<name> is thinking…" is visible, so it lasts exactly as long as the model needs.
let hum = null, humTimer = null;
function speakerVoice() {
  const src = el("portrait")?.querySelector("img")?.getAttribute("src") || "";
  const id = src.split("/").pop().replace(".webp", "");
  const t = manifest?.thinking;
  return t?.voices[t.speakers[id]] || t?.voices[t.default];
}
function startHum() {
  const t = manifest?.thinking;
  if (!ctx || !t || hum || humTimer) return;
  // Short replies stay silent; the hum only starts once the wait is noticeable.
  humTimer = setTimeout(async () => {
    humTimer = null;
    const v = speakerVoice();
    if (!v || el("thinking").hidden) return;
    hum = await voice(v, sfxBus, {loop: true, volume: t.volume, fadeIn: 0.25});
    if (el("thinking").hidden) stopHum();
  }, t.delay_ms);
}
function stopHum() {
  clearTimeout(humTimer); humTimer = null;
  hum?.stop(0.3); hum = null;
}

// ---- wiring to the UI ---------------------------------------------------
function watch(node, attributes, callback) {
  if (node) new MutationObserver(callback).observe(node, {attributes: true, attributeFilter: attributes});
}

function currentScreen() {
  if (el("ending") && !el("ending").hidden) return "ending";
  if (el("case-file")?.open || el("decision")?.open) return "accusation";
  // The title theme opens every session and hands over to the investigation loop when it ends.
  return currentTrack === null || currentTrack === "title" ? "title" : "investigation";
}

function syncMusic() { music(currentScreen()); }

async function start() {
  if (ctx) return;
  ctx = new AudioContext();
  master = ctx.createGain();
  master.gain.value = muted ? 0 : 1;
  master.connect(ctx.destination);
  [musicBus, ambienceBus, sfxBus] = [0, 1, 2].map(() => { const g = ctx.createGain(); g.connect(master); return g; });
  manifest = await fetch(base + "audio.json").then(r => r.json()).catch(() => null);
  if (!manifest) return;
  syncMusic();
  if (document.body.dataset.room) ambience(document.body.dataset.room);
}

function toggle() {
  muted = !muted;
  try { localStorage.setItem("audio.muted", muted ? "1" : "0"); } catch { /* not persisted */ }
  if (ctx) ramp(master.gain, muted ? 0 : 1, 0.2);
  button.textContent = muted ? "Sound off" : "Sound on";
  button.setAttribute("aria-pressed", String(!muted));
  start();
}

const button = document.createElement("button");
button.type = "button";
button.id = "sound-toggle";
button.textContent = muted ? "Sound off" : "Sound on";
button.setAttribute("aria-pressed", String(!muted));
button.title = "Music and sound effects";
button.style.cssText = "position:fixed;right:1rem;bottom:1rem;z-index:50;font:inherit;font-size:.8rem;";
button.onclick = toggle;
document.body.append(button);

// Browsers only allow sound after a user gesture.
for (const type of ["pointerdown", "keydown"]) addEventListener(type, start, {once: true, capture: true});

let lastRoom = document.body.dataset.room;
new MutationObserver(() => {
  const roomId = document.body.dataset.room;
  if (roomId === lastRoom) return;
  if (lastRoom && roomId) play("move_room");
  lastRoom = roomId;
  if (!ctx) return;
  ambience(roomId);
  syncMusic();
}).observe(document.body, {attributes: true, attributeFilter: ["data-room"]});

watch(el("thinking"), ["hidden"], () => (el("thinking").hidden ? stopHum() : startHum()));
watch(el("dialogue"), ["open"], () => { if (!el("dialogue").open) stopHum(); });
watch(el("case-file"), ["open"], () => { if (el("case-file").open && currentTrack !== "accusation") play("accusation_open"); syncMusic(); });
watch(el("decision"), ["open"], syncMusic);
watch(el("ending"), ["hidden"], syncMusic);
watch(el("journal"), ["open"], () => { if (el("journal").open) play("journal_open"); });

window.gameAudio = {play, music, toggle};
