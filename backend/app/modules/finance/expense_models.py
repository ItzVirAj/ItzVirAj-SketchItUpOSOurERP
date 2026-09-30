from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import DateTime,ForeignKey,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel
class Expense(BaseModel):
 __tablename__="expenses"
 id:Mapped[UUID]=mapped_column(primary_key=True)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
 project_id:Mapped[UUID|None]=mapped_column(ForeignKey("projects.id",ondelete="SET NULL"))
 category:Mapped[str]=mapped_column(String(80))
 description:Mapped[str]=mapped_column(Text)
 amount:Mapped[float]=mapped_column(Numeric(14,2))
 currency:Mapped[str]=mapped_column(String(3),default="INR")
 incurred_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
 status:Mapped[str]=mapped_column(String(30),default="recorded")
 created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
