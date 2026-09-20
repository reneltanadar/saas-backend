from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.orm import Session
from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
    PaginatedCompanies,
)
from app.services import company_services
from app.database import get_db
from app.auth.dependencies import require_employee,require_admin
from app.models.user import User

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=PaginatedCompanies)
async def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = "id",
    db: Session = Depends(get_db),
    current_user:User=Depends(require_employee),
):
    return company_services.get_all_companies(db, current_user.tenant_id, skip, limit, sort_by)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user:User=Depends(require_employee),
):
    return company_services.get_company_by_id(db, current_user.tenant_id, company_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user:User=Depends(require_admin),
):
    return company_services.create_company(db, current_user.tenant_id, company)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    updates: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user:User=Depends(require_admin),
):
    return company_services.update_company(db, current_user.tenant_id, company_id, updates)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user:User=Depends(require_admin),
):
    company_services.delete_company(db, current_user.tenant_id, company_id)