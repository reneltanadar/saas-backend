from fastapi import APIRouter,status,Query
from app.schemas.user import UpdateUser,UserCreate,UserResponse,PaginatedUsers
from app.services import user_services

router=APIRouter(prefix="/users",tags=["Users"])

# to get all users
@router.get("",response_model=PaginatedUsers)
async def get_users(skip:int=Query(0,ge=0),
                    limit:int=Query(10,ge=1,le=100),
                    sort_by:str="id"):
    
    return user_services.get_all_users(skip,limit,sort_by)


# to get specific users by name
@router.get("/search")
async def search_users(name: str =None,limit:int=10):
    return user_services.search_user(name,limit)


# to get user by id
@router.get("/{user_id}",response_model=UserResponse)
async def get_user(user_id:int):
    return user_services.get_user_by_id(user_id)


# to create users
@router.post("",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_users(user :UserCreate):
    return user_services.create_user(user)


# to update user
@router.patch("/{user_id}",response_model=UserResponse)
async def user_update(user_id:int,updates:UpdateUser):
    return user_services.update_user(user_id,updates)


# to delete user by id
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int):
    return user_services.delete_user(user_id)

    