"""Shared HTTP helper for the LLM clients: POST JSON with retries on transient failures."""

from __future__ import annotations

import logging
import time
from typing import Callable

import httpx

from game.llm import LLMError

log = logging.getLogger(__name__)

# Rate limits and server-side overload ("model is experiencing high demand") are usually brief.
TRANSIENT_STATUS = {429, 500, 502, 503, 504}
# If the provider asks us to wait longer than this (e.g. a daily free-tier quota), fail fast.
MAX_RETRY_WAIT = 20.0


def retry_delay_seconds(response: httpx.Response) -> float | None:
    """Server-requested wait: Google's RetryInfo.retryDelay ("51647s") or a Retry-After header."""
    header = response.headers.get("retry-after")
    if header:
        try:
            return float(header)
        except ValueError:
            pass
    try:
        details = response.json().get("error", {}).get("details", [])
    except ValueError:
        return None
    for detail in details if isinstance(details, list) else []:
        delay = detail.get("retryDelay") if isinstance(detail, dict) else None
        if isinstance(delay, str) and delay.endswith("s"):
            try:
                return float(delay[:-1])
            except ValueError:
                return None
    return None


def _human(seconds: float) -> str:
    hours, rest = divmod(int(seconds), 3600)
    return f"{hours}h{rest // 60:02d}m" if hours else f"{rest // 60}m{rest % 60:02d}s"


def post_json(
    http: httpx.Client,
    url: str,
    payload: dict,
    headers: dict,
    *,
    provider: str,
    retries: int = 2,
    backoff: float = 1.5,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """POST ``payload`` and return the decoded JSON body.

    Retries ``retries`` times on transient HTTP status codes and network errors, waiting
    ``backoff``, ``2*backoff``, ... seconds. Raises :class:`LLMError` on final failure.
    """
    for attempt in range(retries + 1):
        last = attempt == retries
        try:
            response = http.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            requested = retry_delay_seconds(exc.response)
            if requested is not None and requested > MAX_RETRY_WAIT:
                raise LLMError(
                    f"{provider} HTTP {status}: quota or rate limit reached, provider says retry in "
                    f"{_human(requested)}. {exc.response.text[:160]}"
                ) from exc
            if status in TRANSIENT_STATUS and not last:
                wait = max(backoff * 2**attempt, requested or 0.0)
                log.warning("%s HTTP %s, retrying in %.1fs (%d/%d)", provider, status, wait, attempt + 1, retries)
                sleep(wait)
                continue
            raise LLMError(f"{provider} HTTP {status}: {exc.response.text[:200]}") from exc
        except httpx.TransportError as exc:
            if not last:
                log.warning("%s network error, retrying (%d/%d): %s", provider, attempt + 1, retries, exc)
                sleep(backoff * 2**attempt)
                continue
            raise LLMError(f"{provider} request failed: {exc}") from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise LLMError(f"{provider} request failed: {exc}") from exc
    raise AssertionError("unreachable")
