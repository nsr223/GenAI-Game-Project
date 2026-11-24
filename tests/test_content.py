"""Static content checks (World §10.4, Evidence §10.4)."""

import shutil

import pytest
import yaml

from game.content import ContentError, load_content

MVP_ROOMS = {
    "bridge", "wet_lab", "dry_lab", "mess_hall", "medical_bay",
    "crew_quarters", "editing_room", "engineering_workshop",
}

# World §2.3, transcribed independently of data/locations.yaml.
WORLD_2_3_EDGES = {
    ("bridge", "upper_stairs"),
    ("upper_stairs", "main_corridor"),
    ("main_corridor", "lower_stairs"),
    ("main_corridor", "wet_lab"),
    ("main_corridor", "dry_lab"),
    ("main_corridor", "mess_hall"),
    ("main_corridor", "medical_bay"),
    ("main_corridor", "crew_quarters"),
    ("main_corridor", "editing_room"),
    ("wet_lab", "dry_lab"),
    ("lower_stairs", "lower_corridor"),
    ("lower_corridor", "engineering_workshop"),
    ("lower_corridor", "engine_room"),
    ("lower_corridor", "equipment_storage"),
    ("equipment_storage", "aft_work_deck"),
}
CABINS = {
    "cabin_player", "cabin_elena", "cabin_sarah", "cabin_daniel",
    "cabin_maya", "cabin_thomas", "cabin_olivia", "cabin_lucas",
}
SUSPECTS = {"maya_chen", "daniel_reyes", "thomas_blake", "sarah_morgan", "olivia_hart", "lucas_weber"}
ESSENTIAL_EVIDENCE = {"EV-00", "EV-09", "EV-10", "EV-11", "EV-13", "EV-14", "EV-16", "EV-17", "EV-18", "EV-19"}


def test_content_loads_without_errors(content):
    assert content.locations and content.evidence and content.npcs


def test_room_graph_is_reciprocal(content):
    for loc in content.locations.values():
        for other in loc.connects_to:
            assert loc.id in content.locations[other].connects_to, f"{loc.id} -> {other} not reciprocal"


def test_room_graph_matches_world_bible(content):
    edges = set()
    for loc in content.locations.values():
        for other in loc.connects_to:
            edges.add(tuple(sorted((loc.id, other))))
    expected = {tuple(sorted(e)) for e in WORLD_2_3_EDGES}
    expected |= {tuple(sorted(("crew_quarters", c))) for c in CABINS}
    assert edges == expected


def test_all_ids_resolve(content):
    for loc in content.locations.values():
        for obj_id in loc.object_ids:
            assert obj_id in content.objects
    for ev in content.evidence.values():
        if ev.location_id:
            assert ev.location_id in content.locations
        if ev.object_id:
            assert ev.location_id in content.objects[ev.object_id].location_ids
    for npc in content.npcs.values():
        assert npc.default_location in content.locations


def test_mvp_rooms_exist_and_are_flagged(content):
    for room in MVP_ROOMS:
        assert room in content.locations
        assert content.locations[room].mvp


def test_essential_evidence_present_and_not_in_unimplemented_rooms(content):
    assert ESSENTIAL_EVIDENCE <= set(content.evidence)
    for ev_id in ESSENTIAL_EVIDENCE:
        ev = content.evidence[ev_id]
        if ev.location_id:
            assert content.locations[ev.location_id].mvp, f"{ev_id} sits in non-MVP {ev.location_id}"


def test_exactly_six_suspects(content):
    assert set(content.npcs) == SUSPECTS


def test_player_facing_text_does_not_call_the_mass_a_weapon(content):
    texts = [o.description for o in content.objects.values()]
    texts += [o.name for o in content.objects.values()]
    texts += [e.player_visible_summary for e in content.evidence.values()]
    texts += [e.name for e in content.evidence.values()]
    texts += [i.label for i in content.interactions.values()]
    texts += [i.result_text for i in content.interactions.values()]
    for text in texts:
        assert "weapon" not in text.lower(), text


def test_validation_catches_one_way_connection(tmp_path, repo_root):
    data = tmp_path / "data"
    shutil.copytree(repo_root / "data", data)
    locs = yaml.safe_load((data / "locations.yaml").read_text(encoding="utf-8"))
    locs["locations"]["mess_hall"]["connects_to"].append("bridge")
    (data / "locations.yaml").write_text(yaml.safe_dump(locs), encoding="utf-8")
    with pytest.raises(ContentError, match="mess_hall -> bridge is not reciprocal"):
        load_content(data, root=tmp_path)


def test_validation_catches_unknown_flag(tmp_path, repo_root):
    data = tmp_path / "data"
    shutil.copytree(repo_root / "data", data)
    ev = yaml.safe_load((data / "evidence.yaml").read_text(encoding="utf-8"))
    ev["evidence"][1]["access"] = "typo_flag"
    (data / "evidence.yaml").write_text(yaml.safe_dump(ev), encoding="utf-8")
    with pytest.raises(ContentError, match="unknown flag 'typo_flag'"):
        load_content(data, root=tmp_path)


def test_tbd_report(content):
    """Not a pass/fail check: prints every provisional decision (run with -s to see it)."""
    report = content.tbd_report()
    print("\nTBD / provisional content:\n  " + "\n  ".join(report))
    assert any("EV-16" in line for line in report)
