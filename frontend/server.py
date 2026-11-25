"""Run locally with python -m frontend.server."""

import hashlib
import json
import os
import secrets
from contextlib import asynccontextmanager
from functools import partial
from pathlib import Path

os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

import gradio as gr
from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from backend.config import make_llm
from game import Game, load_content

from .dialogue import NO_ANSWER, PlayerVoice, line, notices, record_notes, transcripts
from .journal import journal_page, offered_topics, player_events, player_text, scene_view
from .saves import MAX_TOKEN, InvalidSave, pack_snapshot, startup_secret, unpack

DIALOGUE_CONCURRENCY = 4
MAX_MESSAGE = 500

ROOT = Path(__file__).resolve().parent
BAD_SAVE = {"error": "invalid_save", "message": "This save could not be opened. Start a new game to continue."}
BAD_ACTION = {"error": "invalid_action", "message": "This action could not be read."}


def load_credentials():
    load_dotenv(ROOT.parent / ".env")
    return startup_secret()


@asynccontextmanager
async def lifespan(app, credentials=None):
    app.state.key, app.state.temporary_save = credentials if credentials is not None else load_credentials()
    app.state.content = load_content()
    # Server.launch builds the Blocks queue before entering this lifespan.
    if getattr(app, "blocks", None) is not None:
        app.get_blocks().api_open = False
    app.state.voice = PlayerVoice(make_llm()[0])
    yield


app = gr.Server(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/scenes.json")
def scenes():
    return FileResponse(ROOT / "scenes.json")


def act(body, key, content, *, endpoint="action", voice=None):
    if not isinstance(body, dict):
        return BAD_ACTION
    action = body.get("action") if endpoint == "action" else endpoint
    token, target = body.get("save"), body.get("target")
    if endpoint == "action" and action not in ("new", "resume", "move", "inspect", "review"):
        return BAD_ACTION
    if action in ("move", "inspect", "topic", "talk", "review"):
        if not isinstance(target, str) or not 0 < len(target) <= 128:
            return BAD_ACTION
    if action == "talk":
        message, present = body.get("message", ""), body.get("present", [])
        if (not isinstance(message, str) or not isinstance(present, list) or len(present) > 1
                or any(not isinstance(item, str) or not 0 < len(item) <= 128 for item in present)):
            return BAD_ACTION
        if len(message) > MAX_MESSAGE or not (message.strip() or present):
            return {"error": "invalid_message", "message": "Write 1–500 characters or choose evidence."}

    notes = {}
    if action == "new" and token is None:
        game = Game.new(content=content)
        case = secrets.token_hex(12)
    else:
        try:
            data = unpack(token, key)
            game = Game.from_dict(data, content=content, llm=voice)
            notes = data.get("dialogue_notes", {})
            case = data.get("journal_case") or hashlib.sha256(token.encode()).hexdigest()[:24]
            game.view()
            journal_page(game)
        except (InvalidSave, KeyError, TypeError, ValueError, AttributeError):
            return BAD_SAVE
        if action == "new":
            return BAD_ACTION

    result = None
    extra = []
    if action == "move":
        result = game.move(target)
    elif action == "inspect":
        result = game.inspect(target)
    elif action == "review":
        if not game.state.has_collected(target):
            return {"error": "unavailable_entry", "message": "This entry is unavailable."}
        if not game.state.has_reviewed(target):
            result = game.review(target)
    elif action == "topic":
        topic = body.get("topic")
        if not isinstance(topic, str) or len(topic) > 128:
            return BAD_ACTION
        # Also accept the offered engine ID from pages loaded before this update.
        offered = next(((choice, engine_id) for choice, engine_id in offered_topics(game.view())
                        if choice["npc"] == target and topic in (choice["id"], engine_id)), None)
        if offered is None:
            return BAD_ACTION
        choice, engine_id = offered
        extra.append(line("user", choice["label"]))
        result = game.interact(engine_id)
    elif action == "talk":
        result = game.talk(target, message, present=present)

    view = game.view()
    snapshot = game.to_dict()
    snapshot["journal_case"] = case
    conversations = snapshot["state"]["conversations"]
    events = result.events if result else []
    narration = result.message if result else ""
    failed = action == "talk" and not result.ok and "(LLM error:" in narration
    if failed:
        narration = NO_ANSWER
    if action == "talk" and not result.ok and any(not game.state.has_collected(item) for item in present):
        narration = "You don't have that evidence."
    if narration:
        narration = player_text(narration)
    if endpoint != "action" and any(p["id"] == target for p in view["npcs_present"]):
        if narration:
            extra.append(line("narration", narration))
        extra.extend(line("notice", notice) for notice in notices(events, view))
        if result.ok or failed or action == "topic":
            record_notes(notes, target, len(conversations.get(target, [])), extra)
    try:
        unchanged = action == "resume" or (action == "review" and result is None)
        save = token if unchanged else pack_snapshot(snapshot, notes, key)
    except InvalidSave:
        return {"error": "save_limit", "message": "This action would exceed the save size limit."}
    history = transcripts(view, conversations, notes)
    if action == "talk" and not result.ok and not failed and target in history:
        history[target].extend(extra)
    for npc, lines in history.items():
        history[npc] = [line(entry["role"], player_text(entry["content"])) for entry in lines
                        if entry["role"] in ("user", "assistant", "narration", "notice")]
    journal = journal_page(game)
    return {"save": save, "case": case, "view": scene_view(view, journal), "journal": journal,
            "message": narration, "events": player_events(events, view),
            "history": history, "retryable": failed,
            "reply": player_text(result.reply) if result and result.reply else None}


@app.api(name="talk", concurrency_limit=DIALOGUE_CONCURRENCY, concurrency_id="dialogue")
def talk(body: dict) -> dict:
    return act(body, app.state.key, app.state.content, endpoint="talk", voice=app.state.voice)


@app.api(name="topic", concurrency_limit=DIALOGUE_CONCURRENCY, concurrency_id="dialogue")
def topic(body: dict) -> dict:
    return act(body, app.state.key, app.state.content, endpoint="topic")


@app.post("/action")
async def action(request: Request):
    # Bound incoming bytes even when the client streams without a Content-Length.
    body = bytearray()
    async for chunk in request.stream():
        if len(body) + len(chunk) > MAX_TOKEN + 1024:
            return BAD_SAVE
        body.extend(chunk)
    try:
        parsed = json.loads(body)
    except (ValueError, RecursionError):
        return BAD_ACTION
    state = request.app.state
    result = await run_in_threadpool(act, parsed, state.key, state.content)
    if state.temporary_save:
        return {**result, "temporary_save": state.temporary_save}
    return result


if __name__ == "__main__":
    try:
        credentials = load_credentials()
    except ValueError as error:
        raise SystemExit(str(error)) from None
    app.launch(app_kwargs={"lifespan": partial(lifespan, credentials=credentials)}, share=False, pwa=False, run_history=False)
