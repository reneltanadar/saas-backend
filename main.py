from fastapi import FastAPI,Depends
from app.routers import users,companies,auth
from app.errors import register_exception_handlers
from app.auth.dependencies import get_current_user
from app.models.user import User

app=FastAPI(title="SaaS Backend")

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)

@app.get("/")
async def root():
    return{
        "message": "SAAS Backend is Running "
    }

@app.get("/whoami")
async def whoami(current_user: User = Depends(get_current_user)):
    return{
        "id":current_user.id,
        "email":current_user.email
    }