from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import Boolean,DateTime,ForeignKey,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel

class Event(BaseModel):
    __tablename__="events"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    project_id:Mapped[UUID|None]=mapped_column(ForeignKey("projects.id",ondelete="SET NULL"))
    created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
    title:Mapped[str]=mapped_column(String(240))
    description:Mapped[str|None]=mapped_column(Text)
    event_type:Mapped[str]=mapped_column(String(40),default="meeting")
    starts_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
    ends_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
    location:Mapped[str|None]=mapped_column(String(500))
    is_all_day:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
