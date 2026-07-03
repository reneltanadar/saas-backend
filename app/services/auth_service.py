from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest,LoginRequest
from app.auth.hashing import hash_password,verify_password
from app.errors import ConflictError
from fastapi import HTTPException,status
from app.auth.jwt import create_access_token

def register_user(db:Session,data:RegisterRequest)->User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ConflictError("Email already Registered")
    new_user=User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db:Session,data:LoginRequest)-> User:
    user = db.query(User).filter(User.email==data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not verify_password(data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return user

def create_token(user:User)->dict:
    token=create_access_token(data={"sub":str(user.id)})
    return{
        "access_token":token,
        "token_type":"bearer"
    }