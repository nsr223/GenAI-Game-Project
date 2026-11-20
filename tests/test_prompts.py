"""NPC prompt assembly: gated knowledge must never leak (npc-prompts summary, World §10.2)."""

import dataclasses

import pytest

from backend.llm import FakeLLM
from game import Game
from game.content import Fact
from game.prompts import build_npc_prompt, strip_tbd
from tests.helpers import do, goto, inspect_at

ALWAYS = "SENTINEL_OLIVIA_ALWAYS"
LOCKED = "SENTINEL_OLIVIA_LOCKED_RECONSTRUCTION_DETAIL"
TBD = "SENTINEL_OLIVIA_TBD_GUESS"
MAYA_SECRET = "SENTINEL_MAYA_SECRET"


@pytest.fixture
def gated_content(content):
    npcs = dict(content.npcs)
    npcs["olivia_hart"] = dataclasses.replace(npcs["olivia_hart"], facts=(
        Fact(id="always", text=ALWAYS, unlock="always"),
        Fact(id="locked", text=LOCKED, unlock={"evidence_collected": "EV-11"}),
        Fact(id="tbd", text=TBD, unlock="always", tbd=True),
    ))
    npcs["maya_chen"] = dataclasses.replace(npcs["maya_chen"], facts=(
        Fact(id="secret", text=MAYA_SECRET, unlock="always"),
    ))
    return dataclasses.replace(content, npcs=npcs)


@pytest.fixture
def game(gated_content):
    return Game.new(content=gated_content, llm=FakeLLM())


def unlock_ev11(game):
    for inter in ["request_engineering_records", "request_medical_comparison"]:
        do(game, inter)
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    do(game, "ask_olivia_initial_observations")
    game.review("EV-09")
    game.review("EV-10")
    do(game, "discuss_reconstruction_with_olivia")


def test_locked_fact_absent_until_unlocked(game):
    goto(game, "medical_bay")
    assert game.talk("olivia_hart", "What happened to Elena?").ok
    prompt = game.llm.last_system_prompt
    assert ALWAYS in prompt
    assert LOCKED not in prompt
    assert TBD not in prompt
    assert MAYA_SECRET not in prompt

    unlock_ev11(game)
    game.talk("olivia_hart", "And now?")
    assert LOCKED in game.llm.last_system_prompt


def test_locked_fact_never_appears_in_any_prompt_before_unlock(game, gated_content):
    """Every NPC, every MVP room with that NPC present: the locked fact never shows up."""
    for npc_id in gated_content.npcs:
        prompt = build_npc_prompt(gated_content, game.state, npc_id)
        assert LOCKED not in prompt
        assert TBD not in prompt
        if npc_id != "maya_chen":
            assert MAYA_SECRET not in prompt
        if npc_id != "olivia_hart":
            assert ALWAYS not in prompt


def test_presented_evidence_content_included_without_developer_fields(game, gated_content):
    do(game, "request_engineering_records")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    game.present_evidence("daniel_reyes", "EV-09")
    prompt = game.llm.last_system_prompt
    ev = gated_content.evidence["EV-09"]
    assert "[EV-09] Apparatus cycle log" in prompt
    assert "resumed an interrupted weekly verification task" in prompt
    for dev_value in ev.verified_facts + ev.not_established:
        assert dev_value not in prompt
    # The user turn tells the model what was shown, too.
    assert "[I show you: Apparatus cycle log]" in game.llm.calls[-1]["messages"][-1]["content"]


def test_evidence_only_in_prompt_for_the_turn_it_is_presented(game):
    do(game, "request_engineering_records")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    game.present_evidence("daniel_reyes", "EV-09")
    game.talk("daniel_reyes", "Anything else?")
    assert "[EV-09]" not in game.llm.last_system_prompt


def test_tbd_markers_stripped_from_presented_evidence(game):
    do(game, "ask_lucas_for_footage")
    inspect_at(game, "editing_room", "editing_workstation")
    game.present_evidence("lucas_weber", "EV-18")
    prompt = game.llm.last_system_prompt
    assert "[EV-18]" in prompt
    assert "[TBD" not in prompt


def test_strip_tbd():
    assert strip_tbd("A clue. [TBD: exact trace.]") == "A clue."
    assert strip_tbd("[TBD, proposed] A view.") == "A view."


def test_tbd_claims_not_in_prompt(game):
    do(game, "ask_maya_whereabouts")
    game.talk("maya_chen", "Tell me again where you were.")
    assert "[TBD]" not in game.llm.last_system_prompt


@pytest.mark.parametrize("spoiler", ["22:45", "reference mass", "Nereid", "calibration", "Maya killed", "murderer"])
def test_base_prompts_contain_no_solution(content, spoiler):
    """With placeholder knowledge, nothing in rules/template/stub persona reveals the solution."""
    game = Game.new(content=content)
    for npc_id, npc in content.npcs.items():
        game.state.location = npc.default_location
        prompt = build_npc_prompt(content, game.state, npc_id)
        assert spoiler.lower() not in prompt.lower(), (npc_id, spoiler)


def test_persona_file_used_when_present(content, tmp_path):
    persona = tmp_path / "persona.md"
    persona.write_text("PERSONA_FILE_SENTINEL", encoding="utf-8")
    npcs = dict(content.npcs)
    npcs["thomas_blake"] = dataclasses.replace(npcs["thomas_blake"], persona_prompt=str(persona))
    c2 = dataclasses.replace(content, npcs=npcs)
    game = Game.new(content=c2)
    assert "PERSONA_FILE_SENTINEL" in build_npc_prompt(c2, game.state, "thomas_blake")
    assert "You are Daniel Reyes, chief engineer" in build_npc_prompt(c2, game.state, "daniel_reyes")


def test_prompt_files_exist(content):
    for key in ("npc_rules", "npc_template"):
        assert content.path(content.rules["prompts"][key]).exists()


def test_prompt_lists_exactly_the_eight_people_aboard(content):
    """Live probe found an invented 'Captain Vance' with rules v1; v2 gives every NPC the cast."""
    game = Game.new(content=content)
    prompt = build_npc_prompt(content, game.state, "thomas_blake")
    section = prompt.split("## People aboard")[1].split("## ")[0]
    people = [line for line in section.splitlines() if line.startswith("- ")]
    assert len(people) == 8
    assert "- Capt. Sarah Morgan, captain" in section
    assert "- Thomas Blake, investor representative (you)" in section
    assert "Elena Fischer" in section
