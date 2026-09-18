from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,DateTime,Boolean,ForeignKey
from datetime import datetime,timezone
from app.database import Base
from app.models.enums import UserRole

class User(Base):
    __tablename__="users"

    id : Mapped[int]= mapped_column(primary_key=True,index=True)

    name: Mapped[str] = mapped_column(String(255),nullable=False)

    email: Mapped[str]= mapped_column(String(255),
                                      unique=True,
                                      nullable=False,
                                      index=True)
    
    age: Mapped[int | None]= mapped_column(nullable= True)

    hashed_password: Mapped[str]= mapped_column(String(255),nullable=False)

    role: Mapped[str]= mapped_column(String(50),nullable=False,default=UserRole.employee)

    is_active:Mapped[bool] =mapped_column(Boolean,default=True)

    created_at:Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        default=lambda:
        datetime.now(timezone.utc)
    )

    company_id : Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True
    )

    company : Mapped["Company | None"] = relationship(
        "Company",
        back_populates="users"
    )

    tenant_id: Mapped[int|None]= mapped_column(
        ForeignKey("tenants.id"),nullable=True,index=True
    )

    tenant: Mapped["Tenant|None"]= relationship("Tenant",back_populates="users")