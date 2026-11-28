const byId = (id) => document.getElementById(id);
const hotspots = byId("hotspots");
const image = byId("room-image");
image.addEventListener("load", () => { image.hidden = false; });
image.addEventListener("error", () => { image.hidden = true; });
let locationId;
let previousItems;
let layout;

// Each tuple is [left, top, width, height], as percentages of the scene.
function autoPosition(index, count) {
  const columns = Math.ceil(Math.sqrt(count * 1.45));
  const rows = Math.ceil(count / columns);
  const width = 84 / columns, height = 78 / rows;
  return [9.5 + (index % columns) * width, 13 + Math.floor(index / columns) * height,
    width - 3, height - 4];
}

export async function loadLayout() {
  if (layout) return;
  const response = await fetch("/scenes.json");
  if (!response.ok) throw new Error("Scene layout unavailable");
  layout = await response.json();
}

function buttonFor(action, item, box) {
  const button = document.createElement("button");
  const locked = action === "move" && !item.accessible;
  const symbol = locked ? "locked" : action;
  button.type = "button";
  button.className = "hotspot " + action + (locked ? " locked" : "");
  button.dataset.action = action;
  button.dataset.target = item.id;
  const verb = locked ? "Locked exit" : action === "move" ? "Exit to" : "Inspect";
  button.setAttribute("aria-label", verb + " " + item.name);
  button.title = locked ? item.locked_text : item.name;
  const icon = document.createElement("i");
  icon.className = "symbol " + symbol;
  icon.setAttribute("aria-hidden", "true");
  const label = document.createElement("span");
  label.className = "hotspot-label";
  label.textContent = item.name;
  button.append(icon, label);
  ["left", "top", "width", "height"].forEach((key, i) => button.style[key] = box[i] + "%");
  return button;
}

export function showRoom(view) {
  const room = view.location;
  const changed = room.id !== locationId;
  const focused = document.activeElement;
  const hadFocus = hotspots.contains(focused);
  const items = [...view.objects.map(item => ["inspect", item]), ...view.exits.map(item => ["move", item])];
  const custom = layout[room.id];
  // If content grows before the art does, lay out the whole room to avoid overlaps.
  const mapped = items.every(([, item]) => custom?.[item.id]);
  const signature = JSON.stringify(items);
  if (changed || signature !== previousItems) {
    const buttons = items.map(([action, item], i) =>
      buttonFor(action, item, mapped ? custom[item.id] : autoPosition(i, items.length)));
    hotspots.replaceChildren(...buttons);
    // Auto-placed hotspots don't line up with the art, so they keep visible labels.
    hotspots.classList.toggle("auto", !mapped);
    if (hadFocus) {
      const next = !changed && buttons.find(b => b.dataset.target === focused.dataset.target);
      (next || byId("room")).focus({preventScroll: true});
    }
    previousItems = signature;
  }
  byId("deck").textContent = "Deck " + room.deck.map(n => String(n).padStart(2, "0")).join(" / ");
  byId("room").textContent = room.name;
  byId("turn").textContent = view.turn;
  byId("present").hidden = !view.npcs_present.length;
  const people = byId("people");
  if (people.dataset.roster !== JSON.stringify(view.npcs_present)) {
    people.dataset.roster = JSON.stringify(view.npcs_present);
    people.replaceChildren(...view.npcs_present.map(person => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.npc = person.id;
      button.setAttribute("aria-haspopup", "dialog");
      button.setAttribute("aria-label", "Talk to " + person.name);
      const face = document.createElement("img");
      face.alt = "";
      face.src = "/static/art/characters/" + person.id + ".webp";
      face.addEventListener("error", () => { face.hidden = true; });
      const name = document.createElement("span");
      name.className = "person-name";
      name.textContent = person.name;
      const talk = document.createElement("span");
      talk.className = "talk";
      talk.setAttribute("aria-hidden", "true");
      talk.textContent = "Talk";
      button.append(face, name, talk);
      return button;
    }));
  }
  if (changed) {
    image.hidden = true;
    if (custom?.image) image.src = custom.image;
    else image.removeAttribute("src");
    byId("arrival").textContent = "Current location: " + room.name + ".";
  }
  locationId = room.id;
  document.body.dataset.room = room.id; // audio.js plays this room's ambience
}

export function clearRoom() {
  locationId = undefined;
  delete document.body.dataset.room;
  hotspots.replaceChildren();
  byId("deck").textContent = "Saved investigation";
  byId("room").textContent = "Save unavailable";
  byId("turn").textContent = "—";
  image.hidden = true;
  image.removeAttribute("src");
  byId("present").hidden = true;
  byId("people").replaceChildren();
  delete byId("people").dataset.roster;
  byId("arrival").textContent = "";
}
