from sqlalchemy.orm import Session
from app.models.tenants import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.errors import NotFoundError, ConflictError


def get_all_tenants(db: Session) -> list[Tenant]:
    return db.query(Tenant).all()


def get_tenant_by_id(db: Session, tenant_id: int) -> Tenant:
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise NotFoundError("Tenant")
    return tenant


def get_tenant_by_slug(db: Session, slug: str) -> Tenant:
    tenant = db.query(Tenant).filter(Tenant.slug == slug).first()
    if not tenant:
        raise NotFoundError("Tenant")
    return tenant


def create_tenant(db: Session, data: TenantCreate) -> Tenant:
    existing = db.query(Tenant).filter(Tenant.slug == data.slug).first()
    if existing:
        raise ConflictError("Tenant slug already exists")

    tenant = Tenant(name=data.name, slug=data.slug)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def update_tenant(db: Session, tenant_id: int, updates: TenantUpdate) -> Tenant:
    tenant = get_tenant_by_id(db, tenant_id)
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tenant, field, value)
    db.commit()
    db.refresh(tenant)
    return tenant