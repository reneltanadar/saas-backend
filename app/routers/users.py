from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginatedUsers
from app.services import user_services
from app.database import get_db
from app.auth.dependencies import get_current_tenant_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PaginatedUsers)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = "id",
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
):
    return user_services.get_all_users(db, tenant_id, skip, limit, sort_by)


@router.get("/search")
async def search_users(
    name: str | None = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
):
    return user_services.search_users(db, tenant_id, name, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
):
    return user_services.get_user_by_id(db, tenant_id, user_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
):
    return user_services.create_user(db, tenant_id, user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    updates: UserUpdate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
):
    return user_services.update_user(db, tenant_id, user_id, updates)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant_id),
):
    user_services.delete_user(db, tenant_id, user_id)