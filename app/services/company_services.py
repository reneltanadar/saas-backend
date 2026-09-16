from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.errors import NotFoundError


def get_all_companies(
    db: Session,
    tenant_id: int,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
) -> dict:
    valid_sort_fields = {"id", "name", "industry"}
    if sort_by not in valid_sort_fields:
        sort_by = "id"

    column = getattr(Company, sort_by)
    query = db.query(Company).filter(Company.tenant_id == tenant_id)
    total = query.count()
    companies = query.order_by(column).offset(skip).limit(limit).all()

    return {"total": total, "skip": skip, "limit": limit, "companies": companies}


def get_company_by_id(db: Session, tenant_id: int, company_id: int) -> Company:
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.tenant_id == tenant_id,
    ).first()
    if not company:
        raise NotFoundError("Company")
    return company


def create_company(db: Session, tenant_id: int, data: CompanyCreate) -> Company:
    new_company = Company(**data.model_dump(), tenant_id=tenant_id)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


def update_company(db: Session, tenant_id: int, company_id: int, updates: CompanyUpdate) -> Company:
    company = get_company_by_id(db, tenant_id, company_id)
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, tenant_id: int, company_id: int) -> None:
    company = get_company_by_id(db, tenant_id, company_id)
    db.delete(company)
    db.commit()