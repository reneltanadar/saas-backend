from fastapi import APIRouter,HTTPException,status
from app.schemas.user import UpdateUser,UserCreate,UserResponse

router=APIRouter(prefix="/users",tags=["Users"])

users=[]
counter =1


@router.get("",response_model=list[UserResponse])
async def get_users():
    return users

# to get specific users
@router.get("/search")
async def search_users(name: str =None,limit:int=10):
    results=users

    if name:
        results=[u for u in users if name.lower() in u["name"].lower() ]

    return{
        "users": results[:limit],
        "count":len(results[:limit])
    }

@router.get("/{user_id}",response_model=UserResponse)
async def get_user(user_id:int):
    for user in users:
        if user["id"]==user_id:

            return user
        
    raise HTTPException(status_code=404,detail="User Not Found")

@router.post("",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
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


@router.patch("/{user_id}",response_model=UserResponse)
async def user_update(user_id:int,updates:UpdateUser):
    for user in users:
        if user["id"]==user_id:
            update_data=updates.model_dump(exclude_unset=True)
            user.update(update_data)
            return user
    raise HTTPException(status_code=404,detail="User Not Found")


@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int):
    for index,user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="User Not Found"
    ) 