"""Persisted claims (Evidence §7.4), EV-19 contradiction, accusation (Evidence §9), save/load."""

import json

import pytest

from game import Game
from tests.helpers import do, goto, inspect_at

REQUIRED = ["maya_motive_established", "maya_alibi_contradicted", "machinery_cause_excluded", "blunt_force_method_supported"]


@pytest.fixture
def game(content):
    return Game.new(content=content)  # no LLM: talk() still runs the deterministic rules


def _get_ev18(game):
    do(game, "ask_lucas_for_footage")
    inspect_at(game, "editing_room", "editing_workstation")
    assert game.state.has_collected("EV-18")


def play_full_chain(game, skip_ev14=False):
    """Collect every essential clue through the real data and rules (no flag shortcuts)."""
    # Machinery excluded (EV-09 + EV-10 -> EV-11)
    do(game, "request_engineering_records")
    do(game, "request_medical_comparison")
    do(game, "request_wet_lab_inspection")
    do(game, "request_shared_records_review")
    do(game, "request_cabin_elena_search")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    do(game, "ask_olivia_initial_observations")
    game.review("EV-09")
    game.review("EV-10")
    do(game, "discuss_reconstruction_with_olivia")
    # Method (EV-13 + EV-14)
    inspect_at(game, "wet_lab", "wet_lab_calibration_station")
    if not skip_ev14:
        do(game, "compare_injury_with_calibration_object")
        game.review("EV-14")
    # Motive (EV-16 + EV-17)
    inspect_at(game, "dry_lab", "dry_lab_shared_workstation")
    inspect_at(game, "cabin_elena", "cabin_desk_elena")
    game.review("EV-16")
    game.review("EV-17")
    # False alibi (claim + EV-18 -> EV-19)
    do(game, "ask_maya_whereabouts")
    _get_ev18(game)
    goto(game, "dry_lab")
    assert game.present_evidence("maya_chen", "EV-18").ok
    game.review("EV-19")


def test_maya_claim_is_persisted_with_speaker_turn_topic(game):
    do(game, "ask_maya_whereabouts")
    (claim,) = game.state.claims
    assert claim.speaker == "maya_chen"
    assert claim.topic == "whereabouts_critical_window"
    assert claim.turn > 0
    assert game.journal()["claims"][0]["speaker"] == "Dr. Maya Chen"


def test_ev19_not_unlocked_without_prior_claim(game):
    _get_ev18(game)
    goto(game, "dry_lab")
    result = game.present_evidence("maya_chen", "EV-18")
    assert result.ok
    assert not game.state.has_collected("EV-19")
    # Recording the claim afterwards and presenting again now works.
    game.interact("ask_maya_whereabouts")
    game.present_evidence("maya_chen", "EV-18")
    assert game.state.has_collected("EV-19")


def test_cannot_present_uncollected_evidence(game):
    goto(game, "dry_lab")
    result = game.present_evidence("maya_chen", "EV-18")
    assert not result.ok
    assert not game.state.has_collected("EV-19")


def test_presenting_cycle_log_to_daniel_sets_motive_flag(game):
    do(game, "request_engineering_records")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    assert not game.state.flag("daniel_motive_investigated")
    game.present_evidence("daniel_reyes", "EV-09")
    assert game.state.flag("daniel_motive_investigated")


def test_accusation_needs_sarah_present(game):
    goto(game, "mess_hall")
    result = game.accuse("maya_chen")
    assert not result.ok
    assert game.state.accusations_made == []


def test_correct_accusation_without_flags_is_not_a_win(game):
    goto(game, "bridge")
    result = game.accuse("maya_chen")
    assert result.ok
    assert result.outcome == "not_substantiated"
    assert not game.state.game_over
    assert game.state.accusations_made[-1]["result"] == "correct_but_unsupported"


def test_correct_accusation_with_three_of_four_flags_is_not_a_win(game):
    play_full_chain(game, skip_ev14=True)
    assert [f for f in REQUIRED if not game.state.flag(f)] == ["blunt_force_method_supported"]
    goto(game, "bridge")
    assert game.accuse("maya_chen").outcome == "not_substantiated"
    assert not game.state.game_over


def test_wrong_accusation_looks_identical_to_unsupported(game):
    goto(game, "bridge")
    wrong = game.accuse("daniel_reyes")
    unsupported = game.accuse("maya_chen")
    assert wrong.outcome == unsupported.outcome == "not_substantiated"
    assert wrong.message == unsupported.message
    assert game.state.accusations_made[0]["result"] == "wrong"


def test_full_walkthrough_reaches_substantiated_accusation(game):
    play_full_chain(game)
    for flag in REQUIRED:
        assert game.state.flag(flag), flag
    assert not game.state.flag("thomas_motive_investigated")
    goto(game, "bridge")
    result = game.accuse("maya_chen")
    assert result.outcome == "substantiated"
    assert game.state.game_over and game.state.ending == "substantiated"
    assert not game.move("upper_stairs").ok  # investigation closed


def test_save_and_load_round_trip(game, content):
    do(game, "ask_maya_whereabouts")
    do(game, "request_wet_lab_inspection")
    saved = json.loads(json.dumps(game.to_dict()))
    loaded = Game.from_dict(saved, content=content)
    assert loaded.debug_state() == game.debug_state()
    assert loaded.state.has_claim("maya_chen", "whereabouts_critical_window")
    assert loaded.can_enter("wet_lab")


def test_journal_entries_have_evidence_board_fields(game):
    entry = game.journal()["evidence"][0]
    assert entry["id"] == "EV-00"
    assert set(entry) >= {"observed", "interpretation", "questions", "related"}
    assert "verified_facts" not in repr(game.journal())
    assert "elena_flagged_m17" not in repr(game.journal())
