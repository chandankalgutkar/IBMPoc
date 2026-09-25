# tests/test_auth.py
# SCRUM-40: User Login - Test Suite

import pytest
from unittest.mock import patch
from app import create_app  # TODO: Ensure create_app factory exists in app/__init__.py


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    with app.test_client() as client:
        yield client


def post_login(client, username, password):
    return client.post("/login", json={"username": username, "password": password})


# --- AC1: Valid login redirects to dashboard ---
def test_valid_login_redirects_to_dashboard(client):
    with patch("src.routes.auth._verify_credentials", return_value=True):
        response = post_login(client, "user1", "correct_password")
    assert response.status_code == 200
    data = response.get_json()
    assert "dashboard" in data.get("redirect", "")


# --- AC2: Invalid login shows error ---
def test_invalid_login_returns_error(client):
    with patch("src.routes.auth._verify_credentials", return_value=False):
        response = post_login(client, "user1", "wrong_password")
    assert response.status_code == 401
    assert "Invalid credentials" in response.get_json().get("error", "")


# --- AC3: 3 failed attempts locks the account ---
def test_account_locked_after_three_failed_attempts(client):
    with patch("src.routes.auth._verify_credentials", return_value=False):
        for _ in range(3):
            response = post_login(client, "lockme", "bad_pass")
    assert response.status_code == 423
    assert "locked" in response.get_json().get("error", "").lower()


# --- Edge: Missing credentials returns 400 ---
def test_missing_credentials_returns_400(client):
    response = post_login(client, "", "")
    assert response.status_code == 400


# --- Edge: Locked account stays locked ---
def test_locked_account_cannot_login(client):
    with patch("src.routes.auth._verify_credentials", return_value=False):
        for _ in range(3):
            post_login(client, "permlock", "bad")
    with patch("src.routes.auth._verify_credentials", return_value=True):
        response = post_login(client, "permlock", "correct")
    assert response.status_code == 423