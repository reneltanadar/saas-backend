import pytest

def test_register_success(client):
    response = client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "secret123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@test.com"
    assert data["name"] == "Alice"
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "secret123",
    })
    response = client.post("/auth/register", json={
        "name": "Alice2",
        "email": "alice@test.com",
        "password": "secret123",
    })
    assert response.status_code == 409


def test_register_short_password(client):
    response = client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "short",
    })
    assert response.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "secret123",
    })
    response = client.post("/auth/login", json={
        "email": "alice@test.com",
        "password": "secret123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "secret123",
    })
    response = client.post("/auth/login", json={
        "email": "alice@test.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "secret123",
    })
    assert response.status_code == 401


def test_get_profile_authenticated(client):
    client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "secret123",
    })
    login = client.post("/auth/login", json={
        "email": "alice@test.com",
        "password": "secret123",
    })
    token = login.json()["access_token"]

    response = client.get(
        "/auth/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "alice@test.com"


def test_get_profile_unauthenticated(client):
    response = client.get("/auth/profile")
    assert response.status_code == 401