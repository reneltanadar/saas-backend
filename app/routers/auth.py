from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest,LoginRequest,TokenResponse
from app.schemas.user import UserResponse
from app.services import auth_service
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router=APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def register(data:RegisterRequest,db:Session=Depends(get_db)):
    return auth_service.register_user(db,data)

@router.post("/login",response_model=TokenResponse)
async def login(data:LoginRequest,db:Session=Depends(get_db)):
    user=auth_service.login_user(db,data)
    return auth_service.create_token(user)

@router.get("/profile",response_model=UserResponse)
async def get_profile(current_user:User=Depends(get_current_user)):
    return current_user