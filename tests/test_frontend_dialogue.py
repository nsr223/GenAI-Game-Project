import json
import logging
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from backend.llm import FakeLLM
from frontend import server
from frontend.dialogue import NO_ANSWER
from frontend.saves import unpack


@pytest.fixture
def session(monkeypatch):
    model = FakeLLM()
    factory = Mock(return_value=(model, "fake"))
    monkeypatch.setattr(server, "make_llm", factory)
    with TestClient(server.app) as client:
        def start(room="mess_hall"):
            state = client.post("/action", json={"action": "new"}).json()
            for target in ("crew_quarters", "main_corridor", room):
                state = client.post("/action", json={"action": "move", "save": state["save"],
                                                      "target": target}).json()
            return state
        yield start, model
    factory.assert_called_once_with()


def talk(state, message, npc="thomas_blake", present=()):
    return server.talk({"save": state["save"], "target": npc,
                        "message": message, "present": list(present)})


def test_forged_evidence_and_absent_person(session):
    start, model = session
    before = start()
    for args in ({"present": ["EV-11"]}, {"npc": "olivia_hart"}):
        refused = talk(before, "Can you explain this?", **args)
        previous = unpack(before["save"], server.app.state.key)
        previous["state"]["turn"] += 1
        assert refused["message"] and not refused["retryable"]
        assert unpack(refused["save"], server.app.state.key) == previous
    assert not model.calls


def test_topic_refusal_and_evidence_are_engine_results(session):
    start, model = session
    state = start("medical_bay")
    def topic(state, topic_id):
        return server.topic({"save": state["save"], "target": "olivia_hart", "topic": topic_id})
    refused = topic(state, "discuss_reconstruction_with_olivia")
    assert "I can't give you a reliable cause yet" in refused["message"]
    assert refused["view"]["evidence"] == state["view"]["evidence"]
    result = topic(refused, "ask_olivia_initial_observations")
    assert result["message"] == "Olivia shares what she can from her initial examination."
    assert result["view"]["turn"] == 5
    evidence = next(event for event in result["events"] if event["type"] == "evidence_collected")
    assert result["history"]["olivia_hart"][-1]["content"] == "New evidence · " + evidence["name"]
    resumed = server.act({"action": "resume", "save": result["save"]}, server.app.state.key,
                         server.app.state.content)
    assert resumed["history"] == result["history"]
    assert not model.calls


@pytest.mark.parametrize("message", ["", "  \t", "x" * 501, "🐟" * 501])
def test_invalid_message(session, message):
    start, model = session
    assert talk(start(), message)["error"] == "invalid_message"
    assert not model.calls


def test_empty_reply_and_sensitive_failure(session, caplog):
    start, model = session
    sentinel = "sk-test-private-provider-key"
    responses = iter([RuntimeError(sentinel), "   ", "Good morning."])

    def respond(prompt, messages):
        reply = next(responses)
        if isinstance(reply, Exception):
            logging.getLogger("backend.llm._http").warning("Network retry: %s", reply)
            raise reply
        return reply

    model.responder = respond
    state = start()
    for turn in (4, 5):
        state = talk(state, "Hello.")
        assert state["message"] == NO_ANSWER and state["retryable"]
        assert state["view"]["turn"] == turn
        assert sentinel not in json.dumps(state)
        assert sentinel not in json.dumps(unpack(state["save"], server.app.state.key))
    assert sentinel not in caplog.text
    assert "Voice request failed" in caplog.text
    reply = talk(state, "Hello.")
    assert reply["reply"] == "Good morning." and reply["view"]["turn"] == 6


def test_model_words_cannot_change_access(session):
    start, model = session
    model.default = "The wet lab is open now"
    state = talk(start(), "Did the door open?")
    assert state["reply"] == model.default
    corridor = server.act({"action": "move", "save": state["save"], "target": "main_corridor"},
                          server.app.state.key, server.app.state.content)
    exit_ = next(place for place in corridor["view"]["exits"] if place["id"] == "wet_lab")
    assert not exit_["accessible"]
    assert not corridor["history"]


def test_statement_notice_hides_internal_topic():
    from frontend.dialogue import notices

    events = [{"type": "claim_recorded", "speaker": "Dr. Maya Chen", "topic": "whereabouts_critical_window"}]
    assert notices(events, {"leads": []}) == ["Statement recorded"]
