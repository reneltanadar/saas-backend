from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.errors import NotFoundError, ConflictError
from app.auth.hashing import hash_password
from app.logger import logger


def get_all_users(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
) -> dict:
    valid_sort_fields = {"id", "name", "email"}
    if sort_by not in valid_sort_fields:
        sort_by = "id"

    column = getattr(User, sort_by)
    query = db.query(User).filter(User.tenant_id == tenant_id)
    total = query.count()
    users = query.order_by(column).offset(skip).limit(limit).all()

    logger.debug(f"Fetched {len(users)} users for tenant_id: {tenant_id}")
    return {"total": total, "skip": skip, "limit": limit, "users": users}


def search_users(db: Session, tenant_id: int, name: str | None, limit: int) -> dict:
    query = db.query(User).filter(User.tenant_id == tenant_id)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    results = query.limit(limit).all()

    logger.debug(f"Search users by name='{name}' for tenant_id: {tenant_id} — {len(results)} results")
    return {"users": results, "count": len(results)}


def get_user_by_id(db: Session, tenant_id: int, user_id: int) -> User:
    user = db.query(User).filter(
        User.id == user_id,
        User.tenant_id == tenant_id,
    ).first()
    if not user:
        logger.warning(f"User not found: id={user_id} tenant_id={tenant_id}")
        raise NotFoundError("User")
    return user


def create_user(db: Session, tenant_id: int, user_data: UserCreate) -> User:
    logger.info(f"Creating user: {user_data.email} | tenant_id: {tenant_id}")
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        logger.warning(f"Create user failed - email exists: {user_data.email}")
        raise ConflictError("Email already exists")

    data = user_data.model_dump()
    plain_password = data.pop("password")
    data["hashed_password"] = hash_password(plain_password)
    data["tenant_id"] = tenant_id

    new_user = User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created: id={new_user.id} email={new_user.email}")
    return new_user


def update_user(db: Session, tenant_id: int, user_id: int, updates: UserUpdate) -> User:
    user = get_user_by_id(db, tenant_id, user_id)
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    logger.info(f"User updated: id={user_id} tenant_id={tenant_id}")
    return user


def delete_user(db: Session, tenant_id: int, user_id: int) -> None:
    user = get_user_by_id(db, tenant_id, user_id)
    db.delete(user)
    db.commit()
    logger.info(f"User deleted: id={user_id} tenant_id={tenant_id}")