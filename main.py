from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel,field_validator
from typing import Optional

app=FastAPI()

class UserCreate(BaseModel):
    name:str
    email:str
    age: Optional[int] =None

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

class UpdateUser(BaseModel):
    name:Optional[str] =None
    email:Optional[str] =None
    age:Optional[int] =None


users=[]
counter =1

@app.get("/")
async def root():
    return{
        "message": "SAAS Backend is Running "
    }

@app.get("/users",response_model=list[UserResponse])
async def get_users():
    return users

@app.get("/users/search")
async def search_users(name: str =None,limit:int=10):
    results=users

    if name:
        results=[u for u in users if name.lower() in u["name"].lower() ]

    return{
        "users": results[:limit],
        "count":len(results[:limit])
    }

@app.get("/users/{user_id}",response_model=UserResponse)
async def get_user(user_id:int):
    for user in users:
        if user["id"]==user_id:

            return user
        
    raise HTTPException(status_code=404,detail="User Not Found")

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_users(user :UserCreate):
    global counter
    new_user={
        "id":counter,
        **user.model_dump()
    }
    counter+=1
    for existing in users:
        if existing["email"]==new_user["email"]:
            raise HTTPException(status_code=404,detail="Email already Exists")
    users.append(new_user)
    return new_user


@app.patch("/users/{user_id}",response_model=UserResponse)
async def user_update(user_id:int,updates:UpdateUser):
    for user in users:
        if user["id"]==user_id:
            update_data=updates.model_dump(exclude_unset=True)
            user.update(update_data)
            return user
    raise HTTPException(status_code=404,detail="User Not Found")