"""Smoke test for the Gradio debug app handlers (no server, FakeLLM)."""

import os

import pytest


@pytest.fixture(scope="module")
def app():
    os.environ["LLM_PROVIDER"] = "fake"  # load_dotenv never overrides an existing variable
    from backend import debug_app
    from backend.llm import FakeLLM
    assert isinstance(debug_app.LLM, FakeLLM)
    return debug_app


def test_handlers_walk_move_inspect_talk_present_accuse(app):
    saved, log, *_ = app.new_game()
    for target in ["crew_quarters", "main_corridor", "mess_hall"]:
        saved, log, *_ = app.do_move(saved, log, target)
    saved, log, *_ = app.do_inspect(saved, log, "mess_table")
    saved, log, *_ = app.do_talk(saved, log, "thomas_blake", "Hello.", [])
    saved, log, *_ = app.do_talk(saved, log, "thomas_blake", "Remember this?", ["EV-00"])
    saved, log, *_ = app.do_review(saved, log, "EV-00")
    for target in ["main_corridor", "upper_stairs", "bridge"]:
        saved, log, *_ = app.do_move(saved, log, target)
    saved, log, *_ = app.do_talk(saved, log, "sarah_morgan", "May I inspect the wet lab?", [])
    saved, log, *_ = app.do_topic(saved, log, "request_wet_lab_inspection")
    out = app.do_accuse(saved, log, "maya_chen")
    saved, log = out[0], out[1]
    assert saved["state"]["location"] == "bridge"
    assert saved["state"]["accusations_made"][0]["result"] == "correct_but_unsupported"
    assert "(failed)" not in "".join(log)
    assert any("> (FakeLLM)" in entry for entry in log)


def test_empty_selection_does_not_spend_a_turn(app):
    saved, log, *_ = app.new_game()
    turn = saved["state"]["turn"]
    saved, log, *_ = app.do_move(saved, log, None)
    assert saved["state"]["turn"] == turn
    assert log[-1] == "*Select something first.*"


def test_suspect_order_does_not_follow_data_order(content):
    from game import Game
    ids = [s["id"] for s in Game.new(content=content).view()["suspects"]]
    assert ids == sorted(ids)
