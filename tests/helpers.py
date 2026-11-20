"""Test helpers: navigation by shortest accessible path."""

from collections import deque

from game import Game


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


def do(game: Game, interaction_id: str):
    """Go to the interaction's NPC and run it, asserting success."""
    npc = game.content.interactions[interaction_id].npc
    goto(game, game.state.npc_locations[npc])
    result = game.interact(interaction_id)
    assert result.ok, f"{interaction_id} blocked: {result.message}"
    return result


def inspect_at(game: Game, location_id: str, object_id: str):
    goto(game, location_id)
    result = game.inspect(object_id)
    assert result.ok, result.message
    return result
