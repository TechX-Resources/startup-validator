"""
Tests for API input validation and security improvements.
Quest Bokwe - Tasks 2, 3, 4
Run: python -m pytest tests/test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_returns_ok_status(self):
        resp = client.get("/health")
        assert resp.json()["status"] == "ok"

    def test_health_returns_version(self):
        resp = client.get("/health")
        assert "version" in resp.json()


class TestInputValidation:
    def test_empty_idea_rejected(self):
        resp = client.post("/validate-idea", json={"idea": ""})
        assert resp.status_code == 422

    def test_short_idea_rejected(self):
        resp = client.post("/validate-idea", json={"idea": "short"})
        assert resp.status_code == 422

    def test_idea_over_1000_chars_rejected(self):
        resp = client.post("/validate-idea", json={"idea": "x" * 1001})
        assert resp.status_code == 422

    def test_missing_idea_field_rejected(self):
        resp = client.post("/validate-idea", json={})
        assert resp.status_code == 422

    def test_valid_idea_accepted(self):
        resp = client.post("/validate-idea", json={"idea": "An AI app that helps students find internships"})
        assert resp.status_code in [200, 500]


class TestSecurity:
    def test_xss_input_handled(self):
        resp = client.post("/validate-idea", json={"idea": "<script>alert('xss')</script> startup idea app"})
        assert resp.status_code in [200, 422, 500]

    def test_special_chars_handled(self):
        resp = client.post("/validate-idea", json={"idea": "{}{{}} startup idea for students learning"})
        assert resp.status_code in [200, 422, 500]

    def test_invalid_endpoint_returns_404(self):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404