"""Movement and access checks (World §2.3, §3.2, §5, §10.3-10.4)."""

import pytest

from game import Game
from tests.helpers import do, goto


@pytest.fixture
def game(content):
    return Game.new(content=content)


def test_start_state(game):
    assert game.state.location == "cabin_player"
    assert game.state.collected_evidence_ids == ["EV-00"]
    assert game.state.flag("wet_lab_secured")


def test_non_adjacent_move_fails(game):
    result = game.move("bridge")
    assert not result.ok
    assert game.state.location == "cabin_player"


def test_unknown_location_fails(game):
    assert not game.move("secret_passage").ok


def test_wet_lab_locked_from_main_corridor(game):
    goto(game, "main_corridor")
    result = game.move("wet_lab")
    assert not result.ok
    assert "secured" in result.message
    assert game.state.location == "main_corridor"


def test_wet_lab_locked_from_dry_lab_internal_door(game):
    goto(game, "dry_lab")
    assert not game.move("wet_lab").ok
    assert game.state.location == "dry_lab"


def test_wet_lab_opens_after_authorization(game):
    do(game, "request_wet_lab_inspection")
    goto(game, "dry_lab")
    assert game.move("wet_lab").ok
    assert game.move("main_corridor").ok


def test_other_cabins_locked_own_cabin_open(game):
    goto(game, "crew_quarters")
    for cabin in ["cabin_elena", "cabin_maya", "cabin_sarah", "cabin_thomas"]:
        assert not game.move(cabin).ok, cabin
    assert game.move("cabin_player").ok


def test_elena_cabin_opens_only_after_authorization(game):
    goto(game, "crew_quarters")
    assert not game.move("cabin_elena").ok
    do(game, "request_cabin_elena_search")
    goto(game, "cabin_elena")
    assert game.state.location == "cabin_elena"


def test_aft_deck_closed_by_storm_and_engine_room_locked(game):
    goto(game, "equipment_storage")
    assert not game.move("aft_work_deck").ok
    goto(game, "lower_corridor")
    assert not game.move("engine_room").ok


def test_view_marks_locked_exits(game):
    goto(game, "main_corridor")
    exits = {e["id"]: e for e in game.view()["exits"]}
    assert exits["wet_lab"]["accessible"] is False
    assert exits["wet_lab"]["locked_text"]
    assert exits["mess_hall"]["accessible"] is True


def test_view_has_no_internal_flags(game):
    view = game.view()
    text = repr(view)
    for flag in game.state.flags:
        assert flag not in text
    assert "maya_chen" not in repr(view["topics"])  # Maya isn't in the player's cabin
