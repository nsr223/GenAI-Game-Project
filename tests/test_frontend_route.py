from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from frontend import saves
from frontend.saves import MAX_TOKEN
from frontend.server import app
from game import Game


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SAVE_SECRET", "unit-test-key".ljust(32, "."))
    with TestClient(app) as client:
        yield client


def send(client, action, save=None, target=None):
    response = client.post("/action", json={"action": action, "save": save, "target": target})
    assert response.status_code == 200
    return response.json()


def test_action_sequence(client):
    fresh = send(client, "new")
    start = Game.new().view()
    for key in ("turn", "exits", "objects", "npcs_present", "evidence", "topics"):
        assert fresh["view"][key] == start[key]
    assert fresh["view"]["location"] == {k: start["location"][k] for k in ("id", "name", "deck")}
    result = send(client, "inspect", fresh["save"], "player_desk")
    assert result["view"]["turn"] == 1 and result["message"]
    for target in ("crew_quarters", "main_corridor"):
        result = send(client, "move", result["save"], target)
        assert result["events"][0]["type"] == "moved"
    locked = next(e for e in result["view"]["exits"] if e["id"] == "wet_lab")
    refused = send(client, "move", result["save"], "wet_lab")
    assert refused["view"]["location"]["id"] == "main_corridor"
    # The locked door also reveals a question for the captain (topic discovery).
    assert refused["message"] == (locked["locked_text"] + "\nNew topic for Capt. Sarah Morgan · "
                                  "Ask for a supervised inspection of the wet lab")
    assert {"type": "topic_offered", "npc": "sarah_morgan",
            "label": "Ask for a supervised inspection of the wet lab"} in refused["events"]
    moved = send(client, "move", refused["save"], "mess_hall")
    forged = send(client, "move", moved["save"], "wet_lab")
    assert forged["view"]["location"]["id"] == "mess_hall"
    assert send(client, "resume", forged["save"])["view"] == forged["view"]


def test_startup_key_retained_then_reloaded(client, monkeypatch):
    saved = send(client, "new")
    monkeypatch.setenv("SAVE_SECRET", "other-test-key".ljust(32, "."))
    assert send(client, "resume", saved["save"])["view"] == saved["view"]
    with TestClient(app) as other:
        assert send(other, "resume", saved["save"])["error"] == "invalid_save"


def test_temporary_save_notice_metadata(monkeypatch):
    monkeypatch.setattr("frontend.server.load_dotenv", lambda _: None)
    monkeypatch.delenv("SAVE_SECRET", raising=False)
    with TestClient(app) as temporary:
        fresh = send(temporary, "new")
        assert fresh["temporary_save"]
        moved = send(temporary, "move", fresh["save"], "crew_quarters")
        assert moved["temporary_save"] == fresh["temporary_save"]
    monkeypatch.setenv("SAVE_SECRET", "unit-test-key".ljust(32, "."))
    with TestClient(app) as configured:
        assert "temporary_save" not in send(configured, "new")
    monkeypatch.setenv("SAVE_SECRET", "weak-canary")
    with pytest.raises(ValueError, match="32 bytes") as error:
        with TestClient(app):
            pytest.fail("weak key accepted")
    assert "weak-canary" not in str(error.value)


def test_save_limit_leaves_prior_investigation_usable(client, monkeypatch):
    fresh = send(client, "new")
    with monkeypatch.context() as limit:
        limit.setattr(saves, "pack", Mock(side_effect=saves.InvalidSave))
        rejected = send(client, "inspect", fresh["save"], "player_desk")
        assert rejected["error"] == "save_limit"
        assert "save" not in rejected and "view" not in rejected
    assert send(client, "resume", fresh["save"])["view"] == fresh["view"]
    moved = send(client, "move", fresh["save"], "crew_quarters")
    assert moved["view"]["location"]["id"] == "crew_quarters"
    assert moved["view"]["turn"] == 1


def test_invalid_inputs(client):
    for token in (None, "broken", "x" * (MAX_TOKEN + 5000)):
        assert send(client, "resume", token)["error"] == "invalid_save"
    assert send(client, "talk")["error"] == "invalid_action"
    assert send(client, "inspect", target={})["error"] == "invalid_action"
    assert client.post("/action", content="[").json()["error"] == "invalid_action"
    for url in ("/docs", "/redoc", "/openapi.json"):
        assert client.get(url).status_code == 404
