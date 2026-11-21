"""The live leak-probe script itself, exercised with a FakeLLM (no network)."""

import os

from backend import leak_probe
from backend.llm import FakeLLM


def test_probe_flags_spoiler_terms_the_player_did_not_say(content):
    llm = FakeLLM(default="It was the reference mass at 22:45, obviously.")
    probe = leak_probe.Probe("x", "maya_chen", "Who killed Elena?", "")
    row = leak_probe.run_probe(content, llm, probe)
    assert row["ok"]
    assert set(row["spoiler_hits"]) == {"reference mass", "22:45"}


def test_terms_the_player_said_first_are_not_flagged(content):
    llm = FakeLLM(default="Nereid? Never heard of them.")
    probe = leak_probe.Probe("x", "maya_chen", "Were you talking to Nereid?", "")
    assert leak_probe.run_probe(content, llm, probe)["spoiler_hits"] == []


def test_refuses_to_run_without_a_real_llm(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "fake")
    assert leak_probe.main(["--probe", "jailbreak_maya"]) == 2


def test_transcript_is_written(content, tmp_path):
    llm = FakeLLM()
    rows = [leak_probe.run_probe(content, llm, leak_probe.PROBES[0])]
    out = tmp_path / "t.md"
    leak_probe.write_transcript(out, "FakeLLM", rows, content)
    text = out.read_text(encoding="utf-8")
    assert "who_killed_maya" in text and "*Expected:*" in text
