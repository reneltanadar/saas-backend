from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,DateTime,Boolean,ForeignKey
from datetime import datetime,timezone
from app.database import Base
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.models.company import Company

class User(Base):
    __tablename__="users"

    id : Mapped[int]= mapped_column(primary_key=True,index=True)

    name: Mapped[str] = mapped_column(String(255),nullable=False)

    email: Mapped[str]= mapped_column(String(255),
                                      unique=True,
                                      nullable=True,
                                      index=True)
    
    age: Mapped[int | None]= mapped_column(nullable= True)

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