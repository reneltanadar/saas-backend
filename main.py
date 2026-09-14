from fastapi import FastAPI,Depends
from app.routers import users,companies,auth,tenants
from app.errors import register_exception_handlers

app=FastAPI(title="SaaS Backend")

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(tenants.router)

@app.get("/")
async def root():
    return{
        "message": "SAAS Backend is Running "
    }
