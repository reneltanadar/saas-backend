from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Boolean,DateTime
from datetime import datetime, timezone
from app.database import Base

class Tenant(Base):
    __tablename__="tenants"

    id: Mapped[int]=mapped_column(primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(255),nullable=False,unique=True)
    slug: Mapped[str]=mapped_column(String(100),nullable=False,unique=True,index=True)

    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
    )
    users:Mapped[list["User"]]=relationship("User", back_populates="tenant")
    companies: Mapped[list["Company"]] = relationship("Company",back_populates="tenant")