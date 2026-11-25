"""Versioned, authenticated browser saves. The payload can be read by its owner."""

import base64
import binascii
import hashlib
import hmac
import json
import logging
import os
import secrets
import zlib

MAX_TOKEN = 128 * 1024
MAX_RAW = 512 * 1024
MAX_CONVERSATION_MESSAGES = 60


class InvalidSave(ValueError):
    pass


def startup_secret() -> tuple[bytes, str | None]:
    value = os.getenv("SAVE_SECRET")
    if value in (None, ""):
        logging.getLogger(__name__).warning("Temporary signing key: saves end when this server stops.")
        return secrets.token_bytes(32), secrets.token_hex(16)
    if value != value.strip() or len(value.encode()) < 32:
        raise ValueError("SAVE_SECRET must be at least 32 bytes with no surrounding whitespace.")
    return value.encode(), None


def pack_game(game, key: bytes) -> str:
    return pack_snapshot(game.to_dict(), {}, key)


def pack_snapshot(data, notes, key):
    if notes:
        data["dialogue_notes"] = notes
    conversations = data["state"]["conversations"]
    for npc, messages in conversations.items():
        dropped = max(0, len(messages) - MAX_CONVERSATION_MESSAGES)
        if dropped and npc in notes:
            notes[npc] = [dict(entry, at=entry["at"] - dropped) for entry in notes[npc]
                          if entry["at"] >= dropped]
        conversations[npc] = messages[-MAX_CONVERSATION_MESSAGES:]
    return pack(data, key)


def pack(data: dict, key: bytes) -> str:
    raw = json.dumps(data, separators=(",", ":")).encode()
    if len(raw) > MAX_RAW:
        raise InvalidSave()
    payload = b"v1." + base64.urlsafe_b64encode(zlib.compress(raw))
    tag = hmac.new(key, payload, hashlib.sha256).hexdigest()
    token = f"{payload.decode()}.{tag}"
    if len(token) > MAX_TOKEN:
        raise InvalidSave()
    return token


def unpack(token: str, key: bytes) -> dict:
    if not isinstance(token, str) or len(token) > MAX_TOKEN or not token.isascii():
        raise InvalidSave()
    payload, _, tag = token.rpartition(".")
    expected = hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, tag) or not payload.startswith("v1."):
        raise InvalidSave()
    try:
        compressed = base64.b64decode(payload[3:], altchars=b"-_", validate=True)
        decoder = zlib.decompressobj()
        raw = decoder.decompress(compressed, MAX_RAW + 1)
        if len(raw) > MAX_RAW or not decoder.eof or decoder.unused_data:
            raise InvalidSave()
        data = json.loads(raw)
        if not isinstance(data, dict) or data.get("version") != 1:
            raise InvalidSave()
        return data
    except (ValueError, binascii.Error, zlib.error, RecursionError) as exc:
        raise InvalidSave() from exc
