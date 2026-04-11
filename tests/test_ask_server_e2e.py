import os

import httpx
import pytest


class TestHealthEndpoints:
    def test_root_returns_html(self, ask_server: str) -> None:
        r = httpx.get(f"{ask_server}/", timeout=5)
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert "team-pulse-ask-server" in r.text

    def test_health_returns_json(self, ask_server: str) -> None:
        r = httpx.get(f"{ask_server}/health", timeout=5)
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert "uptime" in data


class TestAskValidation:
    def test_invalid_json_returns_400(self, ask_server: str) -> None:
        r = httpx.post(
            f"{ask_server}/ask",
            content=b"not json",
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert r.status_code == 400

    def test_missing_question_returns_400(self, ask_server: str) -> None:
        r = httpx.post(
            f"{ask_server}/ask",
            json={"question": ""},
            timeout=5,
        )
        assert r.status_code == 400

    def test_unknown_route_returns_404(self, ask_server: str) -> None:
        r = httpx.post(f"{ask_server}/nope", json={}, timeout=5)
        assert r.status_code == 404


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set; skipping live integration test",
)
class TestLiveIntegration:
    def test_post_ask_streams_sse(self, ask_server: str) -> None:
        with httpx.stream(
            "POST",
            f"{ask_server}/ask",
            json={"question": "Who are the contributors?"},
            timeout=60,
        ) as r:
            assert r.status_code == 200
            body = r.read().decode()
            assert "event: result" in body
            assert "event: done" in body
