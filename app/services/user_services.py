from fastapi import HTTPException
from app.schemas.user import UserCreate,UpdateUser

users=[]
_counter=1

def get_all_users():
    return users

def search_user(name:str | None, limit:int):
    result =users
    if name:
        result=[
            u for u in users if name.lower() in u["name"].lower()
        ] 

    return {
        "user": result[:limit],
        "count":len(result[:limit])
    }

def get_user_by_id(user_id:int):
    for user in users:
        if user["id"] == user_id:
            return user
        
    raise HTTPException(status_code=404,detail="User Not Found")

def create_user(user_data:UserCreate):
    global _counter
    for user in users:
        if user["email"]==user_data.email:
            raise HTTPException(status_code=400,detail="Email already exists")
        
    new_user={
        "id": _counter,
        **user_data.model_dump()
    }

    _counter+=1
    users.append(new_user)
    return new_user

def update_user(user_id:int,updates:UpdateUser):
    user=get_user_by_id(user_id)
    update_data= updates.model_dump(exclude_unset=True)

    user.update(update_data)

    return user
        

def delete_user(user_id:int):
    user= get_user_by_id(user_id)

    users.remove(user)