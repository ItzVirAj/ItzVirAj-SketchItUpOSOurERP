from datetime import datetime,timezone
from uuid import UUID,uuid4
from sqlalchemy import Boolean,DateTime,ForeignKey,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel
class Notification(BaseModel):
 __tablename__="notifications"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
 user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
 type:Mapped[str]=mapped_column(String(60)); title:Mapped[str]=mapped_column(String(240)); body:Mapped[str|None]=mapped_column(Text)
 entity_type:Mapped[str|None]=mapped_column(String(80)); entity_id:Mapped[UUID|None]=mapped_column(nullable=True); action_url:Mapped[str|None]=mapped_column(Text)
 is_read:Mapped[bool]=mapped_column(Boolean,default=False,index=True); read_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))