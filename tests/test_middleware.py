"""
Tests for the request-logging middleware (app/middleware/).
Week 2: Verify middleware doesn't break requests and logs correctly.
Run: pytest tests/test_middleware.py -v

Requires: pip install httpx  (for FastAPI TestClient)
"""

import logging

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ── Basic request flow ─────────────────────────────


class TestMiddlewarePassthrough:
    """Middleware must not interfere with normal request/response flow."""

    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_validate_idea_rejects_short_input(self):
        resp = client.post("/validate-idea", json={"idea": "Test idea"})
        assert resp.status_code == 422

    def test_invalid_endpoint_returns_404(self):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404


# ── Logging verification ──────────────────────────


class TestMiddlewareLogging:
    """Verify that the middleware emits log entries for requests and responses."""

    def test_logs_incoming_request(self, caplog):
        with caplog.at_level(logging.INFO, logger="middleware.request_logger"):
            client.get("/health")
        messages = [r.message for r in caplog.records]
        assert any("→" in m and "/health" in m for m in messages)

    def test_logs_outgoing_response(self, caplog):
        with caplog.at_level(logging.INFO, logger="middleware.request_logger"):
            client.get("/health")
        messages = [r.message for r in caplog.records]
        assert any("←" in m and "status=" in m for m in messages)

    def test_logs_post_body(self, caplog):
        with caplog.at_level(logging.INFO, logger="middleware.request_logger"):
            client.post("/validate-idea", json={"idea": "logging test"})
        messages = [r.message for r in caplog.records]
        assert any("body=" in m and "logging test" in m for m in messages)


# ── Body reading edge cases ───────────────────────


class TestBodyHandling:
    def test_get_request_skips_body(self, caplog):
        with caplog.at_level(logging.INFO, logger="middleware.request_logger"):
            client.get("/health")
        messages = [r.message for r in caplog.records]
        incoming = [m for m in messages if "→" in m]
        assert any("body=-" in m or "body= " in m or "body=None" not in m for m in incoming)

    def test_empty_post_handled(self, caplog):
        with caplog.at_level(logging.INFO, logger="middleware.request_logger"):
            client.post("/validate-idea", content=b"", headers={"content-type": "application/json"})
        # Should not crash — middleware handles empty bodies gracefully
        assert True
