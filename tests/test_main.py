from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_greet_default():
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hello, World!"}


def test_greet_with_name():
    response = client.get("/greet?name=SRE")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hello, SRE!"}


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_requests_latency_seconds" in response.text