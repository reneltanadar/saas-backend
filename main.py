from fastapi import FastAPI
from app.routers import users

app=FastAPI(title="SaaS Backend")
app.include_router(users.router)

@app.get("/")
async def root():
    return{
        "message": "SAAS Backend is Running "
    }

