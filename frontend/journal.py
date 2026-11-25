"""Project engine records onto the fields used by the player's notebook."""

from game.prompts import strip_tbd


def player_text(value):
    return strip_tbd(value) or "No details recorded yet."


def journal_page(game):
    journal = game.journal()
    collected = {item["id"] for item in journal["evidence"]}
    return {
        "evidence": [{
            "id": item["id"], "name": player_text(item["name"]),
            "observed": player_text(item["observed"]),
            "interpretation": player_text(item["interpretation"]) if item["interpretation"] else "",
            "questions": [player_text(q) for q in item["questions"]],
            "people": [player_text(name) for name in item["related"]["characters"]],
            "related": [key for key in item["related"]["evidence"] if key in collected],
            "reviewed": item["reviewed"],
        } for item in journal["evidence"]],
        "statements": [{"speaker": player_text(item["speaker"]), "text": player_text(item["text"]),
                        "turn": item["turn"]} for item in journal["claims"]],
        "leads": [player_text(lead["text"]) for lead in journal["leads"]],
    }


def offered_topics(view):
    # The engine's interaction IDs can describe undiscovered clues. The signed
    # snapshot fixes the order of the offered actions for this particular menu.
    return [
        ({"id": f"option-{index}", "label": player_text(topic["label"]), "npc": topic["npc"]}, topic["id"])
        for index, topic in enumerate(view["topics"])
    ]


def scene_view(view, journal):
    def named(item):
        return {"id": item["id"], "name": player_text(item["name"])}

    return {
        "turn": view["turn"],
        "location": {**named(view["location"]), "deck": view["location"]["deck"]},
        "exits": [{**named(item), "accessible": item["accessible"],
                  "locked_text": player_text(item["locked_text"]) if item["locked_text"] else None}
                 for item in view["exits"]],
        "objects": [named(item) for item in view["objects"]],
        "npcs_present": [{**named(item), "role": player_text(item["role"])} for item in view["npcs_present"]],
        "topics": [choice for choice, _ in offered_topics(view)],
        "evidence": [{key: e[key] for key in ("id", "name", "reviewed")} for e in journal["evidence"]],
    }


def player_events(events, view):
    leads = {lead["id"]: player_text(lead["text"]) for lead in view["leads"]}
    public = []
    for event in events:
        kind = event["type"]
        if kind == "evidence_collected":
            public.append({"type": kind, "name": player_text(event["name"])})
        elif kind == "lead_added" and event["id"] in leads:
            public.append({"type": kind, "text": leads[event["id"]]})
        elif kind in ("moved", "claim_recorded", "evidence_reviewed"):
            public.append({"type": kind})
    return public
