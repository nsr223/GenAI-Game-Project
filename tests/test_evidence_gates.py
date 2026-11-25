"""Evidence collection and the protected EV-11 revelation (Evidence §6, §10.2, §10.4)."""

import pytest

from game import Game
from tests.helpers import do, goto, inspect_at, offered


@pytest.fixture
def game(content):
    return Game.new(content=content)


def test_inspect_unknown_or_remote_object(game):
    assert not game.inspect("dry_lab_experiment_index").ok  # not in the player's cabin
    assert not game.inspect("murder_weapon").ok


def test_inspect_gives_description_without_evidence(game):
    result = inspect_at(game, "mess_hall", "mess_table")
    assert result.events == []
    assert "table" in result.message


def test_ev09_requires_record_access(game):
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert not game.state.has_collected("EV-09")
    do(game, "request_engineering_records")
    result = inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert game.state.has_collected("EV-09")
    assert {"type": "evidence_collected", "id": "EV-09", "name": "Apparatus cycle log"} in result.events


def test_locked_evidence_shows_hint_until_access(game):
    hint = game.content.evidence["EV-09"].locked_hint
    locked = inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert hint and hint in locked.message
    assert not [e for e in locked.events if e["type"] == "evidence_collected"]
    assert not game.state.has_collected("EV-09")

    do(game, "request_engineering_records")
    opened = inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert hint not in opened.message
    assert "New evidence: Apparatus cycle log." in opened.message

    again = inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert hint not in again.message and "New evidence" not in again.message


def test_no_request_topics_at_start(game):
    requests = {i.id for i in game.content.interactions.values()
                if i.trigger == "topic" and (i.id.startswith("request_") or i.id.endswith(("_records", "_footage")))}
    assert requests and not requests & set(game.state.offered_topics)
    goto(game, "bridge")
    assert [t["id"] for t in game.view()["topics"]] == ["ask_sarah_whereabouts"]


def test_inspecting_the_terminal_offers_requests_to_sarah_and_daniel(game):
    result = inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    new = {(e["id"], e["npc"]) for e in result.events if e["type"] == "topic_offered"}
    assert new == {("request_engineering_records", "sarah_morgan"), ("ask_daniel_for_records", "daniel_reyes")}
    assert "ask_daniel_for_records" in offered(game)  # Daniel works here
    again = inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert not [e for e in again.events if e["type"] == "topic_offered"]  # announced once


def test_locked_door_offers_the_wet_lab_request(game):
    goto(game, "main_corridor")
    result = game.move("wet_lab")
    assert not result.ok
    assert ("request_wet_lab_inspection", "sarah_morgan") in {
        (e["id"], e["npc"]) for e in result.events if e["type"] == "topic_offered"}


def test_unoffered_topic_cannot_be_forced(game):
    goto(game, "bridge")
    result = game.interact("request_wet_lab_inspection")
    assert not result.ok
    assert not game.state.flag("wet_lab_inspection_authorized")


def test_objects_without_evidence_get_no_hint(game):
    result = inspect_at(game, "engineering_workshop", "engineering_workbench")
    assert result.message == game.content.objects["engineering_workbench"].description


def test_ev09_via_daniel_sharing(game):
    do(game, "ask_daniel_for_records")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert game.state.has_collected("EV-09")


def test_review_requires_collection(game):
    assert not game.review("EV-09").ok
    assert game.review("EV-00").ok
    assert game.state.has_reviewed("EV-00")


def test_reconstruction_blocked_before_prerequisites(game):
    goto(game, "medical_bay")
    assert "discuss_reconstruction_with_olivia" not in offered(game)  # follows her first answer
    do(game, "ask_olivia_initial_observations")
    assert "discuss_reconstruction_with_olivia" in offered(game)
    result = game.interact("discuss_reconstruction_with_olivia")
    assert not result.ok
    assert "I can't give you a reliable cause yet" in result.message
    assert not game.state.has_collected("EV-11")
    assert not game.state.flag("machinery_cause_excluded")


def _get_ev09_and_ev10(game, review=True):
    do(game, "request_engineering_records")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    do(game, "ask_olivia_initial_observations")
    if review:
        assert game.review("EV-09").ok
        assert game.review("EV-10").ok


def test_reconstruction_needs_reviewed_not_just_collected(game):
    do(game, "request_medical_comparison")
    _get_ev09_and_ev10(game, review=False)
    assert game.state.has_collected("EV-09") and game.state.has_collected("EV-10")
    assert not game.interact("discuss_reconstruction_with_olivia").ok
    assert not game.state.has_collected("EV-11")


def test_reconstruction_needs_authorization(game):
    _get_ev09_and_ev10(game)
    goto(game, "medical_bay")
    assert not game.interact("discuss_reconstruction_with_olivia").ok


def test_ev11_unlocks_with_prerequisites_and_both_motive_flags_false(game):
    do(game, "request_medical_comparison")
    _get_ev09_and_ev10(game)
    assert not game.state.flag("thomas_motive_investigated")
    assert not game.state.flag("daniel_motive_investigated")
    assert game.state.flag("medical_reconstruction_available")
    assert "return_to_olivia" in [lead["id"] for lead in game.leads()]

    goto(game, "medical_bay")
    result = game.interact("discuss_reconstruction_with_olivia")
    assert result.ok
    assert game.state.has_collected("EV-11")
    assert game.state.flag("medical_reconstruction_completed")
    assert game.state.flag("machinery_cause_excluded")
    assert not game.state.flag("thomas_motive_investigated")
    assert not game.state.flag("daniel_motive_investigated")
    assert "return_to_olivia" not in [lead["id"] for lead in game.leads()]
    # internal flags never leak into events
    assert all("machinery" not in repr(e) for e in result.events)


def test_tbd_flag_is_configurable(content):
    """With the TBD detail flag switched off the gate stays closed even with everything else."""
    import dataclasses
    rules = dict(content.rules)
    rules["tbd_flags"] = {"medical_mechanical_detail_sufficient": {"value": False, "note": "test"}}
    game = Game.new(content=dataclasses.replace(content, rules=rules))
    do(game, "request_medical_comparison")
    _get_ev09_and_ev10(game)
    assert not game.state.flag("medical_reconstruction_available")
    goto(game, "medical_bay")
    assert not game.interact("discuss_reconstruction_with_olivia").ok


def test_ev14_needs_ev11_and_ev13(game):
    goto(game, "medical_bay")
    assert not game.interact("compare_injury_with_calibration_object").ok
    do(game, "request_wet_lab_inspection")
    inspect_at(game, "wet_lab", "wet_lab_calibration_station")
    assert game.state.has_collected("EV-13")
    goto(game, "medical_bay")
    # EV-11 still missing: the topic (whose label names the station) isn't even offered yet.
    assert "compare_injury_with_calibration_object" not in offered(game)
    assert not game.interact("compare_injury_with_calibration_object").ok


def test_topic_requires_npc_present(game):
    result = game.interact("ask_olivia_initial_observations")  # player is in their cabin
    assert not result.ok
    assert not game.state.has_collected("EV-10")


def test_interaction_effects_apply_once(game):
    do(game, "ask_olivia_initial_observations")
    assert "ask_olivia_initial_observations" not in offered(game)  # done topics leave the menu
    again = game.interact("ask_olivia_initial_observations")
    assert again.ok and again.events == []
    assert game.state.collected_evidence_ids.count("EV-10") == 1
