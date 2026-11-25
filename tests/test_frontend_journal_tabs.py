"""Browser regressions using optional Playwright and Chromium."""

import os
import shutil
import socket
from pathlib import Path
from threading import Thread

import pytest
import uvicorn

from frontend.server import app
from frontend.saves import pack_game
from game import Game
from tests.helpers import do, inspect_at

SAVE_SECRET = "local-journal-browser-fixture".ljust(32, ".")
SLOT = "beneath-the-surface.save.v1"


@pytest.fixture
def playwright():
    return pytest.importorskip("playwright.sync_api", reason="Playwright is optional")


@pytest.fixture
def browser(playwright):
    chrome = (os.environ.get("CHROME_BIN") or shutil.which("google-chrome") or shutil.which("chromium")
              or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    with playwright.sync_playwright() as pw:
        executable = chrome if Path(chrome).is_file() else pw.chromium.executable_path
        if not Path(executable).is_file():
            pytest.skip("Chrome or Chromium required for the browser regression")
        instance = pw.chromium.launch(executable_path=executable)
        try:
            yield instance
        finally:
            instance.close()


@pytest.fixture
def local_game(playwright, monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "fake")
    monkeypatch.setenv("SAVE_SECRET", SAVE_SECRET)
    server = uvicorn.Server(uvicorn.Config(app, log_level="error"))
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{listener.getsockname()[1]}"
        finally:
            server.should_exit = True
            thread.join(timeout=10)


def hold_review_lock(page):
    page.evaluate("""slot => new Promise(acquired => {
        navigator.locks.request(slot, () =>
            new Promise(release => { window.releaseReviewLock = release; acquired(); }));
    })""", SLOT)


def test_two_tabs_double_open_one_entry(browser, local_game, playwright):
    with browser.new_context() as context:
        first, second = context.new_page(), context.new_page()
        counts = []
        for page in (first, second):
            page.goto(local_game)
            page.locator("body[data-mode=ready]").wait_for()
            page.locator(".masthead .journal-open").click()

            requests = []
            counts.append(requests)
            def log_review(request, requests=requests):
                if request.url.endswith("/action") and request.post_data_json["action"] == "review":
                    requests.append(request.post_data_json["target"])
            page.on("request", log_review)

        # Make the two intents overlap independently of CPU speed or network timing.
        hold_review_lock(first)
        for page in (first, second):
            page.locator(".index-entry").evaluate("button => { button.click(); button.click(); }")
            page.locator("body[data-mode=busy]").wait_for()
        first.evaluate("window.releaseReviewLock()")
        for page in (first, second):
            playwright.expect(page.locator("#turn")).to_have_text("1")
            page.locator("body[data-mode=ready]").wait_for()
            page.locator("[data-section=evidence]").click()
            playwright.expect(page.locator(".index-entry")).not_to_contain_text("Unread", ignore_case=True)
        assert sorted(map(len, counts)) == [0, 1]

        second.locator("#close-journal").click()
        second.locator("[data-target=player_desk]").click()
        for page in (first, second):
            playwright.expect(page.locator("#turn")).to_have_text("2")
        assert first.evaluate("slot => localStorage.getItem(slot)", SLOT) == second.evaluate(
            "slot => localStorage.getItem(slot)", SLOT)


def test_review_keeps_focus_on_related_evidence(browser, local_game, playwright, content):
    game = Game.new(content=content)
    do(game, "request_engineering_records")
    do(game, "request_medical_comparison")
    inspect_at(game, "engineering_workshop", "engineering_maintenance_terminal")
    do(game, "ask_olivia_initial_observations")
    token = pack_game(game, SAVE_SECRET.encode())

    page = browser.new_page()
    page.add_init_script(f"localStorage.setItem({SLOT!r}, {token!r})")
    page.goto(local_game)
    page.locator("body[data-mode=ready]").wait_for()
    page.locator(".masthead .journal-open").click()
    hold_review_lock(page)
    link = page.get_by_role("link", name="Olivia's preliminary observations")
    try:
        page.get_by_role("button", name="Apparatus cycle log", exact=False).click()
        page.locator("body[data-mode=busy]").wait_for()
        page.keyboard.press("Tab")
        playwright.expect(link).to_be_focused()
    finally:
        page.evaluate("window.releaseReviewLock()")
    playwright.expect(page.locator("#turn")).to_have_text(str(game.state.turn + 1))
    page.locator("body[data-mode=ready]").wait_for()
    playwright.expect(link).to_be_focused()
