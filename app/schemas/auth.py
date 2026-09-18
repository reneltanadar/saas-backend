from pydantic import BaseModel,EmailStr,field_validator
from typing import Optional
from app.models.enums import UserRole

class RegisterRequest(BaseModel):
    name:str
    email:EmailStr
    password:str
    age:Optional[int]=None
    tenant_id:Optional[int]=None
    role:UserRole=UserRole.employee

    @field_validator("name")
    @classmethod
    def empty_name(cls,v):
        if not v.strip():
            raise ValueError("Name Cannot be empty")
        return v.strip()
    
    @field_validator("password")
    @classmethod
    def valid_password(cls,v):
        if len(v) < 8:
            raise ValueError("Password must be atleast of 8 characters")
        return v
    
    @field_validator("age")
    @classmethod
    def valid_age(cls,v):
        if v is not None and v<0:
            raise ValueError("Age must be Positive")
        return v

class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type :str ="bearer"