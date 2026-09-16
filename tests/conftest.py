import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine=create_engine(TEST_DATABASE_URL,
                     connect_args={"check_same_thread":False})

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="function")
def db():

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def overrride_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db]= overrride_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create_tenant(client, name: str, slug: str) -> dict:
    response = client.post("/tenants", json={"name": name, "slug": slug})
    assert response.status_code == 201
    return response.json()


def register_and_login(client, name: str, email: str, password: str, tenant_id: int) -> str:
    client.post("/auth/register", json={
        "name": name,
        "email": email,
        "password": password,
        "tenant_id": tenant_id,
    })
    response = client.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    return response.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}