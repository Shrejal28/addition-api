# test_main.py - Pytest tests for Addition API

import pytest
from fastapi.testclient import TestClient
from main import app, add_numbers

client = TestClient(app)


# ── Unit tests for core logic ──────────────────────────────────────────────

class TestAddNumbers:
    def test_positive_numbers(self):
        assert add_numbers(3, 5) == 8

    def test_negative_numbers(self):
        assert add_numbers(-4, -6) == -10

    def test_mixed_sign(self):
        assert add_numbers(-3, 7) == 4

    def test_floats(self):
        assert round(add_numbers(1.5, 2.5), 2) == 4.0

    def test_zero(self):
        assert add_numbers(0, 0) == 0

    def test_large_numbers(self):
        assert add_numbers(1_000_000, 2_000_000) == 3_000_000


# ── Integration tests via FastAPI TestClient ───────────────────────────────

class TestAddEndpointGET:
    def test_basic_addition(self):
        response = client.get("/add?num1=10&num2=5")
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 15.0
        assert data["operation"] == "addition"

    def test_float_addition(self):
        response = client.get("/add?num1=1.5&num2=2.5")
        assert response.status_code == 200
        assert response.json()["result"] == 4.0

    def test_negative_addition(self):
        response = client.get("/add?num1=-3&num2=-7")
        assert response.status_code == 200
        assert response.json()["result"] == -10.0

    def test_zero_addition(self):
        response = client.get("/add?num1=0&num2=0")
        assert response.status_code == 200
        assert response.json()["result"] == 0.0

    def test_missing_param(self):
        response = client.get("/add?num1=5")
        assert response.status_code == 422  # Unprocessable Entity


class TestAddEndpointPOST:
    def test_basic_addition(self):
        response = client.post("/add", json={"num1": 10, "num2": 20})
        assert response.status_code == 200
        assert response.json()["result"] == 30.0

    def test_negative_numbers(self):
        response = client.post("/add", json={"num1": -5, "num2": -15})
        assert response.status_code == 200
        assert response.json()["result"] == -20.0

    def test_missing_body_field(self):
        response = client.post("/add", json={"num1": 5})
        assert response.status_code == 422

    def test_response_fields(self):
        response = client.post("/add", json={"num1": 4, "num2": 6})
        data = response.json()
        assert "num1" in data
        assert "num2" in data
        assert "result" in data
        assert "operation" in data


class TestHealthEndpoint:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
