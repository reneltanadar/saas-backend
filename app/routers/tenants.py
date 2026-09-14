from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from app.services import tenant_service
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.get("", response_model=list[TenantResponse])
async def get_tenants(db: Session = Depends(get_db)):
    return tenant_service.get_all_tenants(db)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    return tenant_service.get_tenant_by_id(db, tenant_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TenantResponse)
async def create_tenant(
    data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return tenant_service.create_tenant(db, data)


@router.patch("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    updates: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return tenant_service.update_tenant(db, tenant_id, updates)