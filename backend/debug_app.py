"""Minimal Gradio debug UI that drives the engine end to end.

    .venv\\Scripts\\python -m backend.debug_app      (then open http://127.0.0.1:7860)

This is a developer tool, NOT the game UI: it shows internal flags and therefore spoilers.
The real UI belongs to the frontend owner and should use only Game.view() / Game.journal().
"""

from __future__ import annotations

import json
import logging
import os

# No usage telemetry to Gradio/Hugging Face from a local debug tool. Must be set before import.
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

import gradio as gr  # noqa: E402

from game import Game, load_content

from .config import make_llm

logging.basicConfig(level=logging.INFO)

CONTENT = load_content()
LLM, LLM_LABEL = make_llm()
MAX_LOG = 40


def _game(saved: dict | None) -> Game:
    if saved:
        return Game.from_dict(saved, content=CONTENT, llm=LLM)
    return Game.new(content=CONTENT, llm=LLM)


def _location_md(game: Game) -> str:
    v = game.view()
    lines = [f"### {v['location']['name']}  ·  turn {v['turn']}  ·  weather: {v['weather']}"]
    if v["game_over"]:
        lines.append(f"**Investigation closed: {v['ending']}**")
    lines.append("**Exits:** " + ", ".join(
        e["name"] if e["accessible"] else f"~~{e['name']}~~ (locked)" for e in v["exits"]
    ))
    lines.append("**Objects:** " + (", ".join(o["name"] for o in v["objects"]) or "none"))
    lines.append("**People here:** " + (", ".join(f"{n['name']} ({n['role']})" for n in v["npcs_present"]) or "nobody"))
    if v["leads"]:
        lines.append("**Leads:**\n" + "\n".join(f"- {lead['text']}" for lead in v["leads"]))
    return "\n\n".join(lines)


def _journal_md(game: Game) -> str:
    j = game.journal()
    out = ["### Journal"]
    for e in j["evidence"]:
        mark = "" if e["reviewed"] else " *(not reviewed)*"
        out.append(f"**{e['id']} · {e['name']}**{mark}\n\n{e['observed']}")
        if e["questions"]:
            out.append("Questions: " + "; ".join(e["questions"]))
    if j["claims"]:
        out.append("**Recorded statements**\n" + "\n".join(
            f"- {c['speaker']} (turn {c['turn']}): {c['text']}" for c in j["claims"]
        ))
    return "\n\n".join(out)


def _debug(game: Game) -> dict:
    s = game.debug_state()
    return {
        "flags_true": sorted(k for k, v in s["flags"].items() if v),
        "collected": s["collected_evidence_ids"],
        "reviewed": s["reviewed_evidence_ids"],
        "cabins_authorized": s["private_cabin_search_authorized"],
        "completed_interactions": s["completed_interactions"],
        "accusations": s["accusations_made"],
    }


def _render(game: Game, log: list[str]):
    v = game.view()
    evidence = [(f"{e['id']} · {e['name']}", e["id"]) for e in v["evidence"]]
    npcs = [(n["name"], n["id"]) for n in v["npcs_present"]]
    return (
        game.to_dict(),
        log,
        _location_md(game),
        "\n\n---\n\n".join(reversed(log)) or "*Nothing yet.*",
        _journal_md(game),
        _debug(game),
        gr.update(choices=[(e["name"] + ("" if e["accessible"] else " (locked)"), e["id"]) for e in v["exits"]], value=None),
        gr.update(choices=[(o["name"], o["id"]) for o in v["objects"]], value=None),
        gr.update(choices=evidence, value=None),
        gr.update(choices=[(f"{t['label']}  [{t['npc']}]", t["id"]) for t in v["topics"]], value=None),
        gr.update(choices=npcs, value=npcs[0][1] if npcs else None),
        gr.update(choices=evidence, value=[]),
    )


def _act(saved, log, title, fn, selection=True):
    game = _game(saved)
    if not selection:  # nothing picked in the dropdown: don't spend a turn
        return _render(game, (log + ["*Select something first.*"])[-MAX_LOG:])
    result = fn(game)
    entry = f"**Turn {game.state.turn} · {title}** {'' if result.ok else '(failed)'}\n\n{result.message}"
    if result.reply is not None:
        entry += f"\n\n> {result.reply}"
    events = [e for e in result.events if e["type"] in ("evidence_collected", "lead_added", "claim_recorded")]
    if events:
        entry += "\n\n`events: " + json.dumps(events) + "`"
    log = (log + [entry])[-MAX_LOG:]
    return _render(game, log)


def new_game(_saved=None, _log=None):
    return _render(Game.new(content=CONTENT, llm=LLM), [f"New game. LLM: {LLM_LABEL}"])


def do_move(saved, log, target):
    return _act(saved, log, f"Move → {target}", lambda g: g.move(target), bool(target))


def do_inspect(saved, log, obj):
    return _act(saved, log, f"Inspect {obj}", lambda g: g.inspect(obj), bool(obj))


def do_review(saved, log, ev):
    return _act(saved, log, f"Review {ev}", lambda g: g.review(ev), bool(ev))


def do_topic(saved, log, topic):
    return _act(saved, log, f"Topic {topic}", lambda g: g.interact(topic), bool(topic))


def do_talk(saved, log, npc, message, present):
    shown = f" (showing {', '.join(present)})" if present else ""
    return _act(saved, log, f"Talk to {npc}{shown}: “{message}”",
                lambda g: g.talk(npc, message, present=present or []), bool(npc))


def do_accuse(saved, log, suspect):
    return _act(saved, log, f"Accuse {suspect}", lambda g: g.accuse(suspect), bool(suspect))


with gr.Blocks(title="Beneath the Surface: engine debug") as demo:
    gr.Markdown(
        f"## Beneath the Surface · engine debug UI\n"
        f"LLM: **{LLM_LABEL}**. Developer tool: the right column shows internal flags (spoilers)."
    )
    saved = gr.State(None)
    log = gr.State([])
    with gr.Row():
        with gr.Column(scale=3):
            location_md = gr.Markdown()
            with gr.Row():
                move_dd = gr.Dropdown(label="Go to", choices=[])
                move_btn = gr.Button("Move")
            with gr.Row():
                inspect_dd = gr.Dropdown(label="Inspect", choices=[])
                inspect_btn = gr.Button("Inspect")
            with gr.Row():
                topic_dd = gr.Dropdown(label="Ask / request (deterministic topics)", choices=[])
                topic_btn = gr.Button("Do")
            with gr.Group():
                with gr.Row():
                    npc_dd = gr.Dropdown(label="Talk to", choices=[])
                    present_dd = gr.Dropdown(label="Present evidence", choices=[], multiselect=True)
                message_tb = gr.Textbox(label="Message", placeholder="Say something…")
                talk_btn = gr.Button("Talk", variant="primary")
            with gr.Row():
                review_dd = gr.Dropdown(label="Review evidence", choices=[])
                review_btn = gr.Button("Review")
            with gr.Row():
                accuse_dd = gr.Dropdown(
                    label="Accuse (captain must be present)",
                    choices=[(s["name"], s["id"]) for s in Game.new(content=CONTENT).view()["suspects"]],
                    value=None,
                )
                accuse_btn = gr.Button("Accuse", variant="stop")
            new_btn = gr.Button("New game")
            gr.Markdown("### Log (newest first)")
            log_md = gr.Markdown()
        with gr.Column(scale=2):
            journal_md = gr.Markdown()
            debug_json = gr.JSON(label="Internal state (debug only)")

    outputs = [saved, log, location_md, log_md, journal_md, debug_json,
               move_dd, inspect_dd, review_dd, topic_dd, npc_dd, present_dd]
    demo.load(new_game, inputs=None, outputs=outputs)
    new_btn.click(new_game, inputs=None, outputs=outputs)
    move_btn.click(do_move, [saved, log, move_dd], outputs)
    inspect_btn.click(do_inspect, [saved, log, inspect_dd], outputs)
    review_btn.click(do_review, [saved, log, review_dd], outputs)
    topic_btn.click(do_topic, [saved, log, topic_dd], outputs)
    talk_btn.click(do_talk, [saved, log, npc_dd, message_tb, present_dd], outputs)
    accuse_btn.click(do_accuse, [saved, log, accuse_dd], outputs)


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=int(os.getenv("PORT", "7860")))
