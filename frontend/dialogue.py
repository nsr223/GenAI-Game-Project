"""Player-facing conversation history and the boundary around provider failures."""

import logging

from .saves import MAX_CONVERSATION_MESSAGES

log = logging.getLogger(__name__)
NO_ANSWER = "There is a pause. No answer comes."
VOICE_ERROR = "voice unavailable"


def _safe_retry_log(record):
    # The HTTP client logs transport exceptions before chat() returns. Its retry
    # count and delay are useful, but the exception text can contain a credential.
    if isinstance(record.args, tuple):
        record.args = tuple(type(arg).__name__ if isinstance(arg, Exception) else arg
                            for arg in record.args)
    return True


class PlayerVoice:
    def __init__(self, client):
        self.client = client
        logging.getLogger("backend.llm._http").addFilter(_safe_retry_log)

    def chat(self, system_prompt, messages):
        try:
            reply = self.client.chat(system_prompt, messages)
            if not isinstance(reply, str) or not reply.strip():
                raise ValueError("empty response")
            return reply
        except Exception as error:
            # The engine logs its exception verbatim. Keep arbitrary provider bodies,
            # URLs, keys and player input out of both that log and the ActionResult.
            response = getattr(error.__cause__, "response", None)
            status = getattr(response, "status_code", None)
            log.warning("Voice request failed (client=%s, error=%s, HTTP=%s)",
                        type(self.client).__name__, type(error).__name__,
                        status if isinstance(status, int) else "unknown")
            raise RuntimeError(VOICE_ERROR) from None


def notices(events, view):
    lines = []
    for event in events:
        kind = event["type"]
        if kind == "evidence_collected":
            lines.append("New evidence · " + event["name"])
        elif kind == "claim_recorded":
            # The topic is an internal id and can hint at the solution.
            lines.append("Statement recorded")
        elif kind == "lead_added":
            lead = next((lead for lead in view["leads"] if lead["id"] == event["id"]), None)
            if lead:
                lines.append("New lead · " + lead["text"])
    return lines


def line(role, content):
    return {"role": role, "content": content}


def record_notes(notes, npc, position, lines):
    """Anchor UI narration to engine speech without feeding it back to the model."""
    if lines:
        entries = notes.setdefault(npc, [])
        entries.append({"at": position, "lines": lines})
        del entries[:-MAX_CONVERSATION_MESSAGES]


def transcripts(view, conversations, notes):
    visible = {}
    for person in view["npcs_present"]:
        npc = person["id"]
        speech = conversations.get(npc, [])
        entries = notes.get(npc, [])
        lines = []
        note_index = 0
        for index in range(len(speech) + 1):
            while note_index < len(entries) and entries[note_index]["at"] == index:
                lines.extend(entries[note_index]["lines"])
                note_index += 1
            if index < len(speech):
                lines.append(line(speech[index]["role"], speech[index]["content"]))
        visible[npc] = lines
    return visible
