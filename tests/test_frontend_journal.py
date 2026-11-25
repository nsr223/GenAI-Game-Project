import json
from unittest.mock import patch

import pytest

from frontend.journal import player_text
from frontend.saves import pack_game
from frontend.server import act
from game import Game
from tests.helpers import do, inspect_at
from tests.test_claims_accusation import play_full_chain

KEY = b"journal-fixture-only".ljust(32, b".")


def send(content, action, token=None, target=None):
    return act({"action": action, "save": token, "target": target}, KEY, content)


def test_review_is_idempotent_and_preserves_later_actions(content):
    fresh = send(content, "new")
    assert len(fresh["journal"]["leads"]) == 1
    assert fresh["journal"]["evidence"][0]["questions"] == ["What do the original M-17 readings show?"]
    with patch.object(Game, "review", autospec=True, side_effect=Game.review) as review:
        first = send(content, "review", fresh["save"], "EV-00")
        moved = send(content, "move", first["save"], "crew_quarters")
        again = send(content, "review", moved["save"], "EV-00")
        assert [x["view"]["turn"] for x in (fresh, first, moved, again)] == [0, 1, 2, 2]
        assert again["save"] == moved["save"]
        assert again["journal"]["evidence"][0]["reviewed"]
        assert review.call_count == 1


@pytest.mark.parametrize("target", ["EV-19", "bogus"])
def test_forged_review_discloses_no_game_data(content, target):
    fresh = send(content, "new")
    with patch.object(Game, "review", side_effect=AssertionError):
        assert send(content, "review", fresh["save"], target) == {
            "error": "unavailable_entry", "message": "This entry is unavailable."
        }


def test_claim_and_event_have_only_player_fields(content):
    g = Game.new(content=content)
    g.state.location = "dry_lab"
    result = act({"target": "maya_chen", "topic": "ask_maya_whereabouts", "save": pack_game(g, KEY)},
                 KEY, content, endpoint="topic")
    assert result["journal"]["statements"] == [{
        "speaker": "Dr. Maya Chen", "turn": 1, "text": "Maya's account of where she was during the evening."
    }]
    assert {"type": "claim_recorded"} in result["events"]
    result.pop("save")
    for secret in ("ask_maya_whereabouts", "whereabouts_critical_window", "[TBD", "verified_facts", "not_established", "EV-19"):
        assert secret not in json.dumps(result)


def test_every_collected_entry_uses_player_projection(content):
    g = Game.new(content=content)
    play_full_chain(g)
    result = send(content, "resume", pack_game(g, KEY))
    entries = result["journal"]["evidence"]
    assert {e["id"] for e in entries} == set(content.evidence)
    for e in entries:
        assert set(e) == {"id", "name", "observed", "interpretation", "questions",
                          "people", "related", "reviewed"}
        assert e["name"] != e["id"]
        assert e["observed"] == player_text(content.evidence[e["id"]].player_visible_summary)
        assert set(e["related"]) <= set(content.evidence)
        for text in (e["name"], e["observed"], *e["people"], *e["questions"]):
            assert "[TBD" not in text and "�" not in text
    assert player_text("[TBD: undecided]") == "No details recorded yet."


def test_review_triggers_engine_lead_and_filters_event(content):
    g = Game.new(content=content)
    do(g, "request_engineering_records")
    do(g, "request_medical_comparison")
    inspect_at(g, "engineering_workshop", "engineering_maintenance_terminal")
    do(g, "ask_olivia_initial_observations")
    first = send(content, "review", pack_game(g, KEY), "EV-09")
    second = send(content, "review", first["save"], "EV-10")
    lead = next(text for text in second["journal"]["leads"] if text.startswith("Return to Olivia"))
    assert lead not in first["journal"]["leads"]
    assert {"type": "lead_added", "text": lead} in second["events"]
