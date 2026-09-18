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

6. Endpoints

Auth
POST /auth/register
POST /auth/login
GET  /auth/profile

Tenants
GET  /tenants
GET  /tenants/{id}
POST /tenants
PATCH /tenants/{id}

Users
GET    /users
GET    /users/{id}
GET    /users/search
POST   /users
PATCH  /users/{id}
DELETE /users/{id}

Companies
GET    /companies
GET    /companies/{id}
POST   /companies
PATCH  /companies/{id}
DELETE /companies/{id}

Multi-Tenancy
Every user belongs to a tenant. All data (users, companies) is scoped
to the tenant — cross-tenant access returns 404.
Tenant flow:

Create a tenant: POST /tenants
Register a user with that tenant: POST /auth/register with tenant_id
Login to get a token: POST /auth/login
All subsequent requests are automatically scoped to that tenant

Docs

Visit:
http://localhost:8000/docs

