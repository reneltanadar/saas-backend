from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,DateTime
from datetime import timezone,datetime
from app.database import Base
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.models.user import User

class Company(Base):
    __tablename__="companies"

    id:Mapped[int]=mapped_column(primary_key=True ,index= True)

    name:Mapped[str]=mapped_column(String(255),nullable=False)

    industry:Mapped[str | None]=mapped_column(String(255),nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:
        datetime.now(timezone.utc)
    )

    users: Mapped[list["User"]]=relationship("User", back_populates="company")