"""Only the authenticated engine can decide or close a player's case."""

from copy import deepcopy
import json
from unittest.mock import patch

import pytest

from frontend.saves import pack_game, unpack
from frontend.server import BAD_ACTION, BAD_SAVE, act
from game import Game
from tests.helpers import goto
from tests.test_claims_accusation import play_full_chain
from tests.test_frontend_journal_tabs import SAVE_SECRET, SLOT, browser, hold_review_lock, local_game, playwright

KEY = SAVE_SECRET.encode()


def bridge(content, full=False):
    game = Game.new(content=content)
    goto(game, "bridge")
    if full:
        game.state.flags.update(dict.fromkeys(content.rules["accusation"]["required_flags"], True))
    return game


def accuse(content, save, target, **extra):
    return act({"action": "accuse", "save": save, "target": target, **extra}, KEY, content)


def test_failed_projection_is_identical_for_each_person_with_or_without_findings(content):
    responses = set()
    for full in (False, True):
        game = bridge(content, full)
        save = pack_game(game, KEY)
        for person in game.view()["suspects"]:
            result = accuse(content, save, person["id"])
            saved = unpack(result.pop("save"), KEY)
            assert saved["state"]["accusations_made"] == [{"suspect": person["id"], "turn": 5}]
            assert set(result) == {"message", "ending", "turn"}
            assert bool(result["ending"]) == (full and person["id"] == content.rules["accusation"]["culprit"])
            if not result["ending"]:
                responses.add(json.dumps(result))
    assert len(responses) == 1


def test_inconclusive_is_restored_and_all_mutations_are_refused(content):
    content = deepcopy(content)
    rules = content.rules["accusation"]
    rules["allow_continue_after_failure"] = False
    result = accuse(content, pack_game(bridge(content), KEY), "sarah_morgan")
    assert result["ending"] == rules["inconclusive_text"].strip()
    resumed = act({"action": "resume", "save": result["save"]}, KEY, content)
    assert resumed["ending"] == result["ending"]
    assert resumed["view"]["turn"] == result["turn"] == 5
    assert resumed["save"] == result["save"]
    for action in ("accuse", "move", "inspect", "review", "topic", "talk"):
        endpoint = action if action in ("talk", "topic") else "action"
        refused = act({"action": action, "save": resumed["save"], "target": "sarah_morgan",
                       **({"message": "Hello"} if action == "talk" else {})}, KEY, content, endpoint=endpoint)
        assert refused == {"error": "closed", "message": "The investigation is closed."}


def test_accusation_rejects_forged_input_and_ending(content):
    fresh = Game.new(content=content)
    assert accuse(content, pack_game(fresh, KEY), "maya_chen") == BAD_ACTION
    save = pack_game(bridge(content), KEY)
    assert accuse(content, save, "unknown") == BAD_ACTION
    with patch.object(Game, "accuse", side_effect=AssertionError):
        assert accuse(content, save, "maya_chen", outcome="substantiated") == BAD_ACTION
        assert accuse(content, save, "maya_chen", evidence=["EV-19"]) == BAD_ACTION
        forged = bridge(content)
        forged.state.game_over, forged.state.ending = True, "substantiated"
        inconsistent = pack_game(forged, KEY)
        assert act({"action": "resume", "save": inconsistent}, KEY, content) == BAD_SAVE
        payload = inconsistent.rsplit(".", 1)[0]
        assert act({"action": "resume", "save": payload + "." + save.rsplit(".", 1)[1]}, KEY, content) == BAD_SAVE


@pytest.mark.parametrize("width,height", [(1280, 720), (1440, 900)])
def test_simultaneous_confirmations_use_one_turn(browser, local_game, playwright, content, width, height):
    with browser.new_context(viewport={"width": width, "height": height}) as context:
        first, second = context.new_page(), context.new_page()
        counts = []
        for page in (first, second):
            page.goto(local_game)
            page.locator("body[data-mode=ready]").wait_for()
            if page == first:
                page.evaluate("([k,v]) => localStorage.setItem(k,v)", [SLOT, pack_game(bridge(content), KEY)])
                page.reload()
            page.locator("[data-npc=sarah_morgan]").click()
            page.locator("#present-case").click()
            page.get_by_role("radio", name="Capt. Sarah Morgan", exact=True).check()
            page.locator("#case-next").click()
            page.on("request", lambda req: counts.append(req.post_data_json["target"])
                    if req.url.endswith("/action") and req.post_data_json["action"] == "accuse" else None)
        hold_review_lock(first)
        try:
            for page in (first, second):
                page.locator("#decision-confirm").focus()
                for _ in range(8):
                    page.keyboard.down("Enter")
                page.keyboard.up("Enter")
                page.locator("#decision-confirm").evaluate("el => { el.click(); el.click(); }")
                page.locator("body[data-mode=busy]").wait_for()
        finally:
            first.evaluate("window.releaseReviewLock()")
        for page in (first, second):
            playwright.expect(page.locator("#turn")).to_have_text("5")
            page.locator("body[data-mode=ready]").wait_for()
        assert counts == ["sarah_morgan"]


def test_failed_reactions_match_with_a_populated_notebook(browser, local_game, playwright, content):
    full = Game.new(content=content)
    play_full_chain(full)
    goto(full, "bridge")
    early = bridge(content)
    early.state.turn = full.state.turn
    screens = set()
    with browser.new_page(viewport={"width": 1280, "height": 720}) as page:
        page.goto(local_game)
        page.locator("body[data-mode=ready]").wait_for()
        for game in (early, full):
            for person in game.view()["suspects"]:
                if game is full and person["id"] == content.rules["accusation"]["culprit"]:
                    continue
                page.evaluate("([k,v]) => { localStorage.setItem(k,v); sessionStorage.clear(); }",
                              [SLOT, pack_game(game, KEY)])
                page.reload()
                page.locator("[data-npc=sarah_morgan]").click()
                page.locator("#present-case").click()
                page.get_by_role("radio", name=person["name"], exact=True).check()
                page.locator("#case-next").click()
                page.locator("#decision-confirm").click()
                playwright.expect(page.locator("#reaction")).to_be_focused()
                screens.add(page.locator("#dialogue").aria_snapshot())
    assert len(screens) == 1
