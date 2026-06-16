SaaS Backend

A multi-tenant SaaS backend built with FastAPI.

Stack

- FastAPI
- PostgreSQL + SQLAlchemy + Alembic (Week 3+)
- JWT Authentication (Week 4+)
- Docker (Week 7+)

Setup

python -m venv venv
pip install -r requirements.txt
uvicorn main:app --reload

Endpoints

Users

- GET /users
- GET /users/{id}
- POST /users
- PATCH /users/{id}
- DELETE /users/{id}

Companies

- GET /companies
- GET /companies/{id}
- POST /companies
- PATCH /companies/{id}
- DELETE /companies/{id}

Docs

Visit:
http://localhost:8000/docs