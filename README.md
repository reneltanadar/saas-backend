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

Database Setup

1. Install PostgreSQL

2. Create database:

CREATE DATABASE saas_backend;

3. Create a .env file:

DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/saas_backend

4. Run migrations:

alembic upgrade head

5. Start server:

uvicorn main:app --reload

Docs

Visit:
http://localhost:8000/docs

