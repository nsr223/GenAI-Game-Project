"""Cross-document checks for the authored shared-room alibi, not runtime migration."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def test_world_berths_match_character_assignments():
    world = (DOCS / "world_bible.md").read_text()
    bunks = re.findall(
        r"^\| `sleeping_room_([ab])` \| [12] \| (\w+) \| (\w+) \|$",
        world, re.MULTILINE,
    )
    assert len(bunks) == 4
    occupants = [name for _, upper, lower in bunks for name in (upper, lower)]
    assert len(set(occupants)) == len(occupants) == 8
    for room, upper, lower in bunks:
        for name, position, roommate in ((upper, "upper", lower), (lower, "lower", upper)):
            files = list((DOCS / "characters").glob(f"{name.lower()}_*.md"))
            if not files:  # Elena and the player have no NPC character bible.
                assert name in {"Elena", "Player"}
                continue
            relation = "above" if position == "upper" else "beneath"
            roommate_label = "the player" if roommate == "Player" else roommate
            expected = f"Room {room.upper()}, {position} berth {relation} {roommate_label}"
            assert expected in files[0].read_text()


def test_maya_claim_agrees_across_authorities_and_summaries():
    files = ["story_bible.md", "evidence_bible.md", "characters/maya_chen.md",
             "summaries/canon.md", "summaries/story-evidence.md"]
    claims = []
    for file in files:
        text = (DOCS / file).read_text()
        matches = re.findall(r"“(I was already in bed[^”]+)”", text)
        assert len(matches) == 1, file
        claims.append(matches[0])
    assert len(set(claims)) == 1


def test_no_retired_private_room_references_in_current_design():
    files = ["world_bible.md", "evidence_bible.md", "summaries/engine.md"]
    for file in files:
        text = (DOCS / file).read_text()
        assert not re.search(r"\bcabin_(?:player|elena|maya|olivia|lucas|daniel|thomas|sarah)\b", text), file


def test_fixed_gameplay_stations_match_character_bibles():
    world = (DOCS / "world_bible.md").read_text()
    stations = re.findall(
        r"^\| (\w+) (?:Morgan|Hart|Blake|Weber|Reyes|Chen) \| `(\w+)` \|",
        world, re.MULTILINE,
    )
    assert len(stations) == 6
    for name, location in stations:
        character = next((DOCS / "characters").glob(f"{name.lower()}_*.md"))
        assert f"**Fixed gameplay location:** `{location}`" in character.read_text()


def test_current_documents_do_not_retain_superseded_discovery_rules():
    files = list(DOCS.glob("*_bible.md")) + list((DOCS / "characters").glob("*.md"))
    retired = [
        "Maya heading toward the labs",
        "preceding route TBD",
        "Preceding location/route remains TBD",
        "Relief/rest, additional lookout provision, and coverage during the discovery response remain TBD",
        "Any attempt to hide or alter maintenance documentation after the death",
    ]
    for file in files:
        text = file.read_text()
        for phrase in retired:
            assert phrase not in text, (file, phrase)
