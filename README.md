# SaaS Backend

A multi-tenant SaaS REST API built with FastAPI, PostgreSQL, JWT authentication and role-based access control.

Live API docs: https://saas-backend-6jl4.onrender.com/docs

![Swagger UI](docs/swagger.png)

## Features

- JWT authentication with bcrypt password hashing
- Multi-tenancy: every query is scoped to the user's tenant
- Role-based access control (admin / employee)
- Rate limiting on auth routes
- Structured logging and a consistent error format
- Alembic migrations
- pytest test suite
- Dockerfile included
- Deployed on Render

## Architecture

```mermaid
flowchart LR
    Client --> Router
    Router --> Deps[Dependencies: JWT, role, tenant]
    Deps --> Service
    Service --> Models[SQLAlchemy models]
    Models --> DB[(PostgreSQL)]
```

| Layer        | Responsibility                               |
|--------------|----------------------------------------------|
| Router       | HTTP only: request in, response out          |
| Dependencies | Verify the token, check role, resolve tenant |
| Service      | Business rules and tenant-filtered queries   |
| Models       | Database tables                              |

Tenant isolation: every service query filters by `tenant_id`. A cross-tenant lookup returns 404.

## Tech Stack

FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT (python-jose), bcrypt, slowapi, pytest, Docker

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/saas_backend
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run migrations and start the server:

```bash
alembic upgrade head
uvicorn main:app --reload
```

Docs: http://localhost:8000/docs

## Running Tests

```bash
pytest tests/ -v
```

## Endpoints

### Auth
- POST /auth/register
- POST /auth/login
- GET /auth/profile

### Tenants
- GET /tenants
- GET /tenants/{id}
- POST /tenants
- PATCH /tenants/{id}

### Users
- GET /users
- GET /users/search
- GET /users/{id}
- POST /users (admin)
- PATCH /users/{id} (admin: any user, employee: self only)
- DELETE /users/{id} (admin)

### Companies
- GET /companies
- GET /companies/{id}
- POST /companies (admin)
- PATCH /companies/{id} (admin)
- DELETE /companies/{id} (admin)

## Roles and Permissions

| Role      | Companies | Users                             |
|-----------|-----------|-----------------------------------|
| admin     | Full CRUD | Full CRUD                         |
| employee  | Read only | Read all, update own profile only |


