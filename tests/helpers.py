"""Test helpers: navigation by shortest accessible path, and topic discovery the way a player would."""

from collections import deque

from game import Game

# What a player might say to make a request topic appear (keyword discovery, data/interactions.yaml).
ASK = {
    "request_engineering_records": "Could I look at the maintenance records?",
    "ask_daniel_for_records": "Can you show me the apparatus log?",
    "request_medical_comparison": "I need a proper medical examination of her injuries.",
    "request_wet_lab_inspection": "May I inspect the wet lab?",
    "request_shared_records_review": "I need to see the shared project records.",
    "request_cabin_elena_search": "Could we preserve Elena's notes in her cabin?",
    "ask_lucas_for_footage": "Did you film anything last night?",
    "request_media_preservation": "Lucas may have footage from last night.",
}


def goto(game: Game, target: str) -> None:
    """Walk to ``target`` through accessible rooms, asserting every move succeeds."""
    content = game.content
    start = game.state.location
    if start == target:
        return
    prev = {start: None}
    queue = deque([start])
    while queue:
        here = queue.popleft()
        for other in content.locations[here].connects_to:
            if other not in prev and game.can_enter(other):
                prev[other] = here
                queue.append(other)
    assert target in prev, f"no accessible path from {start} to {target}"
    path = []
    node = target
    while node != start:
        path.append(node)
        node = prev[node]
    for step in reversed(path):
        result = game.move(step)
        assert result.ok, f"move to {step} failed: {result.message}"


def offered(game: Game) -> list[str]:
    """Ids of the topics in the menu right now."""
    return [t["id"] for t in game.view()["topics"]]


def do(game: Game, interaction_id: str):
    """Go to the interaction's NPC, make the topic appear if needed (by asking), and run it."""
    npc = game.content.interactions[interaction_id].npc
    goto(game, game.state.npc_locations[npc])
    if interaction_id not in game.state.offered_topics and interaction_id in ASK:
        assert game.talk(npc, ASK[interaction_id]).ok
    assert interaction_id in offered(game), f"{interaction_id} is not offered"
    result = game.interact(interaction_id)
    assert result.ok, f"{interaction_id} blocked: {result.message}"
    return result


def inspect_at(game: Game, location_id: str, object_id: str):
    goto(game, location_id)
    result = game.inspect(object_id)
    assert result.ok, result.message
    return result
