from fastapi import FastAPI,HTTPException,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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
    @app.exception_handler(HTTPException)
    async def http_exxcetion_handler(
        request:Request,
        exc:HTTPException
    ):
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
