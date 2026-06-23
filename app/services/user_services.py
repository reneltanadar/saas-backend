from app.schemas.user import UserCreate,UpdateUser
from app.errors import NotFoundError,ConflictError
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.hashing import hash_password


def get_all_users(db:Session, skip:int=0,limit:int=10,sort_by:str="id")->dict:
    valid_sort_field ={"id","name","email"}

    if sort_by not in valid_sort_field:
        sort_by="id"

    column = getattr(User, sort_by)
    total = db.query(User).count()
    users = db.query(User).order_by(column).offset(skip).limit(limit).all()
    
    return{
        "total":total,
        "skip":skip,
        "limit": limit,
        "users":users
    }

def search_user(db:Session,name:str | None, limit:int)->dict:
    query =db.query(User)
    if name:
        query=query.filter(User.name.ilike(f"%{name}%"))

    results = query.limit(limit).all()

    return {
        "user": results,
        "count":len(results)
    }

def get_user_by_id(db:Session,user_id:int)->User:
    user =db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError("User")
    return user

def create_user(db:Session,user_data:UserCreate)->User:
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise ConflictError("Email Already Exists")
    
    data= user_data.model_dump()
    plain_password = data.pop("password")
    data["hashed_password"] = hash_password(plain_password)

    new_user =User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db:Session,user_id:int,updates:UpdateUser)->User:
    user=get_user_by_id(db,user_id)
    update_data= updates.model_dump(exclude_unset=True)

    for field,value in update_data.items():
        setattr(user,field,value)
    db.commit()
    db.refresh(user)
    return user
        

def delete_user(db:Session,user_id:int)->None:
    user= get_user_by_id(db,user_id)
    db.delete(user)
    db.commit()

