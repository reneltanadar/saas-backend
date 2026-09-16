import pytest
from tests.conftest import create_tenant, register_and_login, auth_headers


def test_company_visible_only_to_own_tenant(client):
    # create two tenants
    tenant_a = create_tenant(client, "Acme Corp", "acme-corp")
    tenant_b = create_tenant(client, "Globex", "globex")

    # Alice belongs to tenant A
    token_a = register_and_login(client, "Alice", "alice@acme.com", "secret123", tenant_a["id"])

    # Bob belongs to tenant B
    token_b = register_and_login(client, "Bob", "bob@globex.com", "secret123", tenant_b["id"])

    # Alice creates a company
    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(token_a),
    )
    assert resp.status_code == 201
    acme_company_id = resp.json()["id"]

    # Alice can see her company
    resp = client.get("/companies", headers=auth_headers(token_a))
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
    assert resp.json()["companies"][0]["name"] == "Acme Solutions"

    # Bob cannot see Alice's company in list
    resp = client.get("/companies", headers=auth_headers(token_b))
    assert resp.status_code == 200
    assert resp.json()["total"] == 0

    # Bob cannot fetch Alice's company by ID
    resp = client.get(f"/companies/{acme_company_id}", headers=auth_headers(token_b))
    assert resp.status_code == 404


def test_user_visible_only_to_own_tenant(client):
    tenant_a = create_tenant(client, "Acme Corp", "acme-corp")
    tenant_b = create_tenant(client, "Globex", "globex")

    token_a = register_and_login(client, "Alice", "alice@acme.com", "secret123", tenant_a["id"])
    token_b = register_and_login(client, "Bob", "bob@globex.com", "secret123", tenant_b["id"])

    # Alice lists users — should only see herself
    resp = client.get("/users", headers=auth_headers(token_a))
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
    assert resp.json()["users"][0]["email"] == "alice@acme.com"

    # Bob lists users — should only see himself
    resp = client.get("/users", headers=auth_headers(token_b))
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
    assert resp.json()["users"][0]["email"] == "bob@globex.com"


def test_bob_cannot_fetch_alice_by_id(client):
    tenant_a = create_tenant(client, "Acme Corp", "acme-corp")
    tenant_b = create_tenant(client, "Globex", "globex")

    token_a = register_and_login(client, "Alice", "alice@acme.com", "secret123", tenant_a["id"])
    token_b = register_and_login(client, "Bob", "bob@globex.com", "secret123", tenant_b["id"])

    # get Alice's user id
    resp = client.get("/users", headers=auth_headers(token_a))
    alice_id = resp.json()["users"][0]["id"]

    # Bob tries to fetch Alice directly
    resp = client.get(f"/users/{alice_id}", headers=auth_headers(token_b))
    assert resp.status_code == 404


def test_bob_cannot_delete_alice_company(client):
    tenant_a = create_tenant(client, "Acme Corp", "acme-corp")
    tenant_b = create_tenant(client, "Globex", "globex")

    token_a = register_and_login(client, "Alice", "alice@acme.com", "secret123", tenant_a["id"])
    token_b = register_and_login(client, "Bob", "bob@globex.com", "secret123", tenant_b["id"])

    # Alice creates a company
    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(token_a),
    )
    acme_company_id = resp.json()["id"]

    # Bob tries to delete it
    resp = client.delete(f"/companies/{acme_company_id}", headers=auth_headers(token_b))
    assert resp.status_code == 404

    # Confirm it still exists for Alice
    resp = client.get(f"/companies/{acme_company_id}", headers=auth_headers(token_a))
    assert resp.status_code == 200


def test_bob_cannot_update_alice_company(client):
    tenant_a = create_tenant(client, "Acme Corp", "acme-corp")
    tenant_b = create_tenant(client, "Globex", "globex")

    token_a = register_and_login(client, "Alice", "alice@acme.com", "secret123", tenant_a["id"])
    token_b = register_and_login(client, "Bob", "bob@globex.com", "secret123", tenant_b["id"])

    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(token_a),
    )
    acme_company_id = resp.json()["id"]

    # Bob tries to update Alice's company
    resp = client.patch(
        f"/companies/{acme_company_id}",
        json={"name": "Hacked"},
        headers=auth_headers(token_b),
    )
    assert resp.status_code == 404

    # Confirm name unchanged for Alice
    resp = client.get(f"/companies/{acme_company_id}", headers=auth_headers(token_a))
    assert resp.json()["name"] == "Acme Solutions"


def test_unauthenticated_cannot_access_companies(client):
    resp = client.get("/companies")
    assert resp.status_code == 401


def test_user_without_tenant_cannot_access_companies(client):
    # register without tenant_id
    client.post("/auth/register", json={
        "name": "NoTenant",
        "email": "notenant@test.com",
        "password": "secret123",
    })
    login = client.post("/auth/login", json={
        "email": "notenant@test.com",
        "password": "secret123",
    })
    token = login.json()["access_token"]

    resp = client.get("/companies", headers=auth_headers(token))
    assert resp.status_code == 403