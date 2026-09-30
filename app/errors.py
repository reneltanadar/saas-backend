from fastapi import FastAPI,HTTPException,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.logger import logger

def create_error_response(
        status_code:int,
        message:str,
        path:str
) -> JSONResponse:
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error":True,
            "status_code":status_code,
            "message":message,
            "path":path
        }
    )

def register_exception_handlers(app:FastAPI):
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request:Request,exc:RateLimitExceeded):
        logger.warning(f"Rate limit exceeded: {request.url.path} from {request.client.host}")

        return create_error_response(
            status_code=429,
            message="Too many requests - please slow down",
            path=str(request.url.path),
        )

    @app.exception_handler(HTTPException)
    async def http_exxcetion_handler(
        request:Request,
        exc:HTTPException
    ):
        if exc.status_code >= 500:
            logger.error(f"HTTP {exc.status_code} on {request.url.path}: {exc.detail}")
        elif exc.status_code >= 400:
            logger.warning(f"HTTP {exc.status_code} on {request.url.path}: {exc.detail}")
        return create_error_response(
            status_code=exc.status_code,
            message=exc.detail,
            path=str(request.url.path)
        )
    
    @app.exception_handler(RequestValidationError)
    async def request_validation_error(
        request:Request,
        exc:RequestValidationError
    ):
        errors=exc.errors()
        first=errors[0]

        location="->".join(
            str(l) for l in first["loc"]
        )

        message=f"{location}: {first['msg']}"
        logger.warning(f"Validation error on {request.url.path}: {message}")
        return create_error_response(
            status_code=422,
            message=message,
            path=str(request.url.path)

        )
    
    @app.exception_handler(Exception)
    async def excption_handler(
        request:Request,
        exc:Exception
    ):
        logger.error(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)
        return create_error_response(
            status_code=500,
            message="Internal Server Error",
            path=str(request.url.path)
        )

class NotFoundError(HTTPException):
    def __init__(self,resource:str="Resource"):
        super().__init__(
            status_code=404,
            detail=f"{resource} not found"
        ) 


class ConflictError(HTTPException):
    def __init__(self,message:str="Conflict"):
        super().__init__(
            status_code=409,
            detail=message
        ) 
