"""LLM clients: request shape and error handling, with httpx.MockTransport (no network)."""

import json

import httpx
import pytest

from backend.config import DEFAULT_OPENROUTER_MODEL, make_llm
from backend.llm import FakeLLM, GeminiClient, OpenRouterClient
from game import LLMClient, LLMError

MESSAGES = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi."},
    {"role": "user", "content": "Where were you?"},
]


def mock(handler):
    seen = {}

    def wrapped(request: httpx.Request):
        seen["request"] = request
        seen["body"] = json.loads(request.content) if request.content else None
        return handler(request)

    return httpx.MockTransport(wrapped), seen


def test_openrouter_request_and_reply():
    transport, seen = mock(lambda r: httpx.Response(200, json={"choices": [{"message": {"content": "In my cabin."}}]}))
    client = OpenRouterClient("sk-test", "some/model", transport=transport)
    assert client.chat("SYSTEM", MESSAGES) == "In my cabin."
    req, body = seen["request"], seen["body"]
    assert str(req.url) == "https://openrouter.ai/api/v1/chat/completions"
    assert req.headers["authorization"] == "Bearer sk-test"
    assert body["model"] == "some/model"
    assert body["messages"][0] == {"role": "system", "content": "SYSTEM"}
    assert body["messages"][1:] == MESSAGES


def test_openrouter_http_error_raises_llm_error():
    transport, _ = mock(lambda r: httpx.Response(401, json={"error": {"message": "bad key"}}))
    with pytest.raises(LLMError, match="401"):
        OpenRouterClient("sk-test", "m", transport=transport).chat("S", MESSAGES)


def test_openrouter_error_body_raises_llm_error():
    transport, _ = mock(lambda r: httpx.Response(200, json={"error": {"message": "rate limited"}}))
    with pytest.raises(LLMError, match="rate limited"):
        OpenRouterClient("sk-test", "m", transport=transport).chat("S", MESSAGES)


def test_gemini_request_and_reply():
    reply = {"candidates": [{"content": {"parts": [{"text": "In the "}, {"text": "dry lab."}]}}]}
    transport, seen = mock(lambda r: httpx.Response(200, json=reply))
    client = GeminiClient("g-key", "gemini-test", transport=transport)
    assert client.chat("SYSTEM", MESSAGES) == "In the dry lab."
    req, body = seen["request"], seen["body"]
    assert req.url.path.endswith("/models/gemini-test:generateContent")
    assert "g-key" not in str(req.url)
    assert req.headers["x-goog-api-key"] == "g-key"
    assert body["system_instruction"]["parts"][0]["text"] == "SYSTEM"
    assert [c["role"] for c in body["contents"]] == ["user", "model", "user"]
    assert body["generationConfig"]["thinkingConfig"] == {"thinkingLevel": "minimal"}


def test_gemini_thinking_level_can_be_omitted_and_thought_parts_are_dropped():
    reply = {"candidates": [{"content": {"parts": [{"text": "hidden", "thought": True}, {"text": "Visible."}]}}]}
    transport, seen = mock(lambda r: httpx.Response(200, json=reply))
    client = GeminiClient("g", "m", thinking_level=None, transport=transport)
    assert client.chat("S", MESSAGES) == "Visible."
    assert "thinkingConfig" not in seen["body"]["generationConfig"]


def test_make_llm_reads_gemini_thinking_level():
    client, _ = make_llm({"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "g"})
    assert client.thinking_level == "minimal"
    client, _ = make_llm({"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "g", "GEMINI_THINKING_LEVEL": "none"})
    assert client.thinking_level is None


def test_gemini_no_candidates_raises():
    transport, _ = mock(lambda r: httpx.Response(200, json={"promptFeedback": {"blockReason": "SAFETY"}}))
    with pytest.raises(LLMError, match="no candidates"):
        GeminiClient("g-key", "m", transport=transport).chat("S", MESSAGES)


def no_sleep(_seconds):
    pass


def test_network_error_raises_llm_error_after_retries():
    attempts = []

    def fail(request):
        attempts.append(1)
        raise httpx.ConnectError("no network")
    client = OpenRouterClient("k", "m", transport=httpx.MockTransport(fail), sleep=no_sleep)
    with pytest.raises(LLMError):
        client.chat("S", MESSAGES)
    assert len(attempts) == 3  # first try + 2 retries


@pytest.mark.parametrize("status", [429, 503])
def test_transient_status_is_retried_then_succeeds(status):
    responses = iter([
        httpx.Response(status, json={"error": {"message": "high demand"}}),
        httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": "Recovered."}]}}]}),
    ])
    waits = []
    client = GeminiClient("g", "m", transport=httpx.MockTransport(lambda r: next(responses)), sleep=waits.append)
    assert client.chat("S", MESSAGES) == "Recovered."
    assert waits == [1.5]


def test_persistent_overload_gives_llm_error_after_retries():
    calls = []

    def overloaded(request):
        calls.append(1)
        return httpx.Response(503, json={"error": {"message": "high demand"}})
    waits = []
    client = GeminiClient("g", "m", transport=httpx.MockTransport(overloaded), sleep=waits.append)
    with pytest.raises(LLMError, match="503"):
        client.chat("S", MESSAGES)
    assert len(calls) == 3 and waits == [1.5, 3.0]


def quota_response(delay: str) -> httpx.Response:
    return httpx.Response(429, json={"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "details": [
        {"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": delay},
    ]}})


def test_daily_quota_fails_fast_without_retrying():
    """Live run hit the free tier's 20 requests/day; retrying a 14 h wait is pointless."""
    calls, waits = [], []

    def exhausted(request):
        calls.append(1)
        return quota_response("51647s")
    client = GeminiClient("g", "m", transport=httpx.MockTransport(exhausted), sleep=waits.append)
    with pytest.raises(LLMError, match="retry in 14h20m"):
        client.chat("S", MESSAGES)
    assert len(calls) == 1 and waits == []


def test_short_server_requested_delay_is_honoured():
    responses = iter([quota_response("7s"), httpx.Response(200, json={"choices": [{"message": {"content": "ok"}}]})])
    waits = []
    client = OpenRouterClient("k", "m", transport=httpx.MockTransport(lambda r: next(responses)), sleep=waits.append)
    assert client.chat("S", MESSAGES) == "ok"
    assert waits == [7.0]


def test_client_errors_are_not_retried():
    calls = []

    def bad_request(request):
        calls.append(1)
        return httpx.Response(400, json={"error": {"message": "bad"}})
    with pytest.raises(LLMError, match="400"):
        GeminiClient("g", "m", transport=httpx.MockTransport(bad_request), sleep=no_sleep).chat("S", MESSAGES)
    assert len(calls) == 1


def test_make_llm_falls_back_to_fake_without_key():
    client, label = make_llm({"LLM_PROVIDER": "openrouter"})
    assert isinstance(client, FakeLLM)
    assert "no API key" in label
    client, _ = make_llm({"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": ""})
    assert isinstance(client, FakeLLM)


def test_make_llm_builds_configured_clients():
    client, label = make_llm({"OPENROUTER_API_KEY": "sk"})
    assert isinstance(client, OpenRouterClient) and client.model == DEFAULT_OPENROUTER_MODEL
    client, _ = make_llm({"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "g", "GEMINI_MODEL": "x"})
    assert isinstance(client, GeminiClient) and client.model == "x"
    client, _ = make_llm({"LLM_PROVIDER": "fake"})
    assert isinstance(client, FakeLLM)
    with pytest.raises(ValueError):
        make_llm({"LLM_PROVIDER": "nope"})


def test_all_clients_satisfy_protocol():
    assert isinstance(FakeLLM(), LLMClient)
    assert isinstance(OpenRouterClient("k", "m"), LLMClient)
    assert isinstance(GeminiClient("k", "m"), LLMClient)
