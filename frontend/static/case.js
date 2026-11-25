const el = id => document.getElementById(id);

export function setupCase({journal, perform, canAct, sessionOnly}) {
  const file = el("case-file"), decision = el("decision"), ending = el("ending");
  const menu = el("game-menu"), observation = document.querySelector(".observation");
  let state, chosen, intent, expected;

  function section(title, key, lines, empty) {
    const group = document.createElement("section");
    const link = document.createElement("a");
    link.href = "#journal";
    link.textContent = title;
    link.setAttribute("aria-label", title + " in the journal");
    link.onclick = event => { event.preventDefault(); journal.open(link, key, true); };
    const heading = document.createElement("h3");
    heading.append(link);
    group.append(heading);
    if (lines.length) {
      const list = document.createElement("ul");
      for (const line of lines) {
        const item = document.createElement("li");
        item.textContent = line;
        item.dir = "auto";
        list.append(item);
      }
      group.append(list);
    } else {
      const text = document.createElement("p");
      text.textContent = empty;
      group.append(text);
    }
    return group;
  }

  el("present-case").onclick = () => {
    if (!canAct() || state.ending || !el("dialogue").open || file.open) return;
    expected = state.save;
    chosen = null;
    const {evidence, statements, leads} = state.journal;
    el("case-records").replaceChildren(
      section("Evidence", "evidence", evidence.map(e => e.name + " · " + (e.reviewed ? "Read" : "Unread")), "No evidence collected."),
      section("Statements", "statements", statements.map(s => s.speaker + " · " + s.text), "No statements recorded."),
      section("Open leads", "leads", leads, "No active leads.")
    );
    el("suspects").replaceChildren(...state.view.suspects.map(person => {
      const label = document.createElement("label");
      const radio = document.createElement("input");
      radio.type = "radio";
      radio.name = "suspect";
      radio.onchange = () => { chosen = person; el("case-next").disabled = false; };
      label.append(radio, document.createTextNode(person.name));
      return label;
    }));
    el("case-next").disabled = true;
    file.showModal();
    el("case-title").focus();
  };
  el("case-back").onclick = () => file.close();

  function confirm(action) {
    if (!canAct() || decision.open) return;
    intent = action;
    if (action === "new") {
      expected = state.save;
      el("decision-title").textContent = "Start a new investigation?";
      el("decision-text").textContent = sessionOnly() ? "This will replace this tab’s investigation." :
        "This will replace the saved investigation in every tab.";
    } else {
      el("decision-title").textContent = "Accuse " + chosen.name + "?";
      el("decision-text").textContent = "Captain Morgan will hear your case. Presenting it takes one turn and may close the investigation.";
    }
    decision.showModal();
  }
  el("case-next").onclick = () => { if (chosen) confirm("accuse"); };
  el("ending-new").onclick = el("new-game").onclick = () => confirm("new");
  el("ending-journal").onclick = event => journal.open(event.currentTarget, "evidence", true);
  el("decision-cancel").onclick = () => decision.close();
  el("decision-confirm").onclick = () => {
    if (!decision.open || !canAct()) return;
    decision.close();
    file.close();
    menu.open = false;
    perform(intent, intent === "accuse" ? chosen.id : undefined, expected);
  };

  return {
    mode(mode) {
      el("new-game").disabled = el("ending-new").disabled = mode !== "ready";
      el("ending-journal").disabled = !["ready", "readonly"].includes(mode);
      el("ending-note").textContent = mode === "readonly" ? "Read-only in this tab." :
        sessionOnly() ? "Saving is off. This investigation lasts until you reload or close this tab." : "";
      if (mode !== "ready" && mode !== "readonly" && !ending.hidden)
        el("ending-note").textContent = el("message").textContent;
    },
    dismiss() {
      decision.close();
      file.close();
      menu.open = false;
      ending.hidden = true;
      el("investigation").hidden = document.querySelector(".masthead").hidden = false;
      observation.append(el("recovery"), el("without-saving"));
    },
    update(result, writable, reaction) {
      const changed = state?.save !== result.save;
      const wasClosed = !ending.hidden;
      const replaced = state && state.case !== result.case;
      if (changed || !writable) {
        if ((file.open || decision.open || wasClosed !== Boolean(result.ending)) && el("journal").open)
          journal.close();
        decision.close();
        file.close();
        menu.open = false;
      }
      if (state?.case !== result.case) {
        el("case-records").replaceChildren();
        el("suspects").replaceChildren();
        el("decision-title").textContent = el("decision-text").textContent = "";
        el("ending-text").textContent = el("ending-counts").textContent = "";
        chosen = null;
      }
      state = result;
      ending.hidden = !result.ending;
      el("investigation").hidden = document.querySelector(".masthead").hidden = !!result.ending;
      if (result.ending) {
        el("ending-recovery").append(el("recovery"), el("without-saving"));
        el("ending-text").textContent = result.ending;
        const counts = [[result.view.turn, "turn"], [result.journal.evidence.length, "entry"], [result.journal.statements.length, "statement"]];
        el("ending-counts").textContent = counts.map(([n, noun]) => n + " " +
          (n === 1 ? noun : noun === "entry" ? "entries" : noun + "s")).join(" · ");
        if (!wasClosed) el("ending-title").focus();
      } else if (wasClosed || replaced) {
        observation.append(el("recovery"), el("without-saving"));
        if (!el("journal").open) el("room").focus();
      }
      if (changed) {
        el("reaction").hidden = !reaction;
        el("reaction").textContent = reaction ? result.message : "";
        if (reaction && !result.ending) el("reaction").focus({preventScroll: true});
      }
    }
  };
}
