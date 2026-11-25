import base64
import hmac
import json
import random
import string
import zlib

import pytest

from frontend import saves
from backend.llm import FakeLLM
from game import Game
from tests.helpers import do, goto, inspect_at

KEY = b"A" * 32


def sign(raw):
    body = b"v1." + base64.urlsafe_b64encode(zlib.compress(raw))
    return body.decode() + "." + hmac.digest(KEY, body, "sha256").hex()


def test_save_roundtrip():
    game = Game.new()
    token = saves.pack(game.to_dict(), KEY)
    assert "wet_lab_secured" not in token
    assert Game.from_dict(saves.unpack(token, KEY)).view() == game.view()


def test_invalid_tokens_never_reach_decompression(monkeypatch):
    token = saves.pack(Game.new().to_dict(), KEY)
    monkeypatch.setattr(zlib, "decompressobj", lambda: pytest.fail("unauthenticated payload unpacked"))
    for broken in [token[:-1], token.replace("v1.", "v2."), "x" * (saves.MAX_TOKEN + 1),
                   saves.pack({}, b"B" * 32), None, "☃"]:
        with pytest.raises(saves.InvalidSave):
            saves.unpack(broken, KEY)


@pytest.mark.parametrize("raw", [b"x" * (saves.MAX_RAW + 1), b"invalid", json.dumps({"version": 99}).encode()])
def test_signed_but_unusable_payload(raw):
    with pytest.raises(saves.InvalidSave):
        saves.unpack(sign(raw), KEY)


def test_secret_lifetime_and_validation(monkeypatch, caplog):
    monkeypatch.delenv("SAVE_SECRET", raising=False)
    first, notice = saves.startup_secret()
    second, other_notice = saves.startup_secret()
    assert len(first) >= 32 and first != second
    assert notice and notice != other_notice
    assert "saves end" in caplog.text
    monkeypatch.setenv("SAVE_SECRET", "too short")
    with pytest.raises(ValueError, match="32 bytes"):
        saves.startup_secret()
    monkeypatch.setenv("SAVE_SECRET", "s" * 32)
    assert saves.startup_secret() == (b"s" * 32, None)
    assert "s" * 32 not in caplog.text


@pytest.mark.parametrize("npc_count", [1, 6])
def test_repeated_dialogue_saves_preserve_investigation(content, npc_count):
    rng = random.Random(3401)
    vocabulary = ["".join(rng.choices(string.ascii_lowercase, k=rng.randint(3, 12))) for _ in range(800)]
    llm = FakeLLM()
    baseline = Game.new(content=content, llm=llm)
    do(baseline, "request_engineering_records")
    do(baseline, "request_medical_comparison")
    do(baseline, "ask_maya_whereabouts")
    inspect_at(baseline, "engineering_workshop", "engineering_maintenance_terminal")
    do(baseline, "ask_olivia_initial_observations")
    for evidence in ("EV-09", "EV-10"):
        baseline.review(evidence)
    trimmed = Game.from_dict(baseline.to_dict(), content=content, llm=llm)
    npcs = ["olivia_hart", *(npc for npc in content.npcs if npc != "olivia_hart")][:npc_count]

    for exchange in range(400):
        npc = npcs[exchange % npc_count]
        message = " ".join(rng.choices(vocabulary, k=60))
        llm.default = " ".join(rng.choices(vocabulary, k=60))
        for game in (baseline, trimmed):
            goto(game, game.state.npc_locations[npc])
            assert game.talk(npc, message).ok
        data = saves.unpack(saves.pack_game(trimmed, KEY), KEY)
        assert data["state"]["conversations"] == {
            person: messages[-60:] for person, messages in baseline.state.conversations.items()
        }
        trimmed = Game.from_dict(data, content=content, llm=llm)

    for game in (baseline, trimmed):
        do(game, "discuss_reconstruction_with_olivia")
        assert game.state.has_collected("EV-11")
        assert game.state.claims
    expected, actual = baseline.state.to_dict(), trimmed.state.to_dict()
    del expected["conversations"], actual["conversations"]
    assert actual == expected
