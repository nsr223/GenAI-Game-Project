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
