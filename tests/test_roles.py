import pytest
from tests.conftest import create_tenant, register_and_login, auth_headers


def setup_tenant_with_users(client):
    """Creates a tenant, an admin, and an employee. Returns their tokens."""
    tenant = create_tenant(client, "Acme Corp", "acme-corp")
    tenant_id = tenant["id"]

    admin_token = register_and_login(
        client, "Alice", "alice@acme.com", "secret123", tenant_id, role="admin"
    )
    employee_token = register_and_login(
        client, "Bob", "bob@acme.com", "secret123", tenant_id, role="employee"
    )
    return admin_token, employee_token


# ── company permission tests ──────────────────────────────

def test_admin_can_create_company(client):
    admin_token, _ = setup_tenant_with_users(client)
    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 201


def test_employee_cannot_create_company(client):
    _, employee_token = setup_tenant_with_users(client)
    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 403
    assert resp.json()["message"] == "Admin access required"


def test_employee_can_read_companies(client):
    admin_token, employee_token = setup_tenant_with_users(client)

    client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(admin_token),
    )

    resp = client.get("/companies", headers=auth_headers(employee_token))
    assert resp.status_code == 200
    assert resp.json()["total"] == 1


def test_employee_cannot_delete_company(client):
    admin_token, employee_token = setup_tenant_with_users(client)

    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(admin_token),
    )
    company_id = resp.json()["id"]

    resp = client.delete(
        f"/companies/{company_id}",
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 403


def test_employee_cannot_update_company(client):
    admin_token, employee_token = setup_tenant_with_users(client)

    resp = client.post(
        "/companies",
        json={"name": "Acme Solutions", "industry": "Tech"},
        headers=auth_headers(admin_token),
    )
    company_id = resp.json()["id"]

    resp = client.patch(
        f"/companies/{company_id}",
        json={"name": "Hacked"},
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 403


# ── user permission tests ─────────────────────────────────

def test_employee_cannot_create_user(client):
    _, employee_token = setup_tenant_with_users(client)
    resp = client.post(
        "/users",
        json={"name": "New User", "email": "new@acme.com", "password": "secret123"},
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 403


def test_admin_can_create_user(client):
    admin_token, _ = setup_tenant_with_users(client)
    resp = client.post(
        "/users",
        json={"name": "New User", "email": "new@acme.com", "password": "secret123"},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 201


def test_employee_cannot_delete_user(client):
    admin_token, employee_token = setup_tenant_with_users(client)

    resp = client.get("/users", headers=auth_headers(admin_token))
    admin_id = resp.json()["users"][0]["id"]

    resp = client.delete(
        f"/users/{admin_id}",
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 403


def test_employee_can_update_own_profile(client):
    _, employee_token = setup_tenant_with_users(client)

    resp = client.get("/auth/profile", headers=auth_headers(employee_token))
    bob_id = resp.json()["id"]

    resp = client.patch(
        f"/users/{bob_id}",
        json={"name": "Bob Updated"},
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Bob Updated"


def test_employee_cannot_update_other_user(client):
    admin_token, employee_token = setup_tenant_with_users(client)

    resp = client.get("/users", headers=auth_headers(admin_token))
    users = resp.json()["users"]
    alice_id = next(u["id"] for u in users if u["email"] == "alice@acme.com")

    resp = client.patch(
        f"/users/{alice_id}",
        json={"name": "Hacked"},
        headers=auth_headers(employee_token),
    )
    assert resp.status_code == 403


def test_admin_can_update_any_user(client):
    admin_token, _ = setup_tenant_with_users(client)

    resp = client.get("/users", headers=auth_headers(admin_token))
    users = resp.json()["users"]
    bob_id = next(u["id"] for u in users if u["email"] == "bob@acme.com")

    resp = client.patch(
        f"/users/{bob_id}",
        json={"name": "Bob Updated By Admin"},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Bob Updated By Admin"
