from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email:str
    age: Optional[int] =None
    company_id: Optional[int] =None

    @field_validator("name")
    @classmethod
    def empty_name(cls,v):
        if not v.strip():
            raise ValueError("Name Cannot be empty")
        return v.strip()
    
    @field_validator("age")
    @classmethod
    def valid_age(cls,v):
        if v is not None and v<0:
            raise ValueError("Age must be Positive")
        return v

class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    age: Optional[int] =None
    is_active:bool
    company_id: Optional[int] =None
    created_at:datetime

    model_config ={"from_attributes": True}


class UpdateUser(BaseModel):
    name:Optional[str] =None
    email:Optional[str] =None
    age:Optional[int] =None
    company_id: Optional[int] =None


class PaginatedUsers(BaseModel):
    total:int
    skip:int
    limit:int
    users:list[UserResponse]