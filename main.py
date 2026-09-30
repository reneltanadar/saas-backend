from fastapi import FastAPI,Request
import time
from app.routers import users,companies,auth,tenants
from app.errors import register_exception_handlers
from app.middleware.rate_limit import limiter
from app.logger import logger


app=FastAPI(title="SaaS Backend")

app.state.limiter=limiter

register_exception_handlers(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"({duration}ms)"
    )
    return response

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(tenants.router)

@app.get("/")
async def root():
    return{
        "message": "SAAS Backend is Running "
    }
