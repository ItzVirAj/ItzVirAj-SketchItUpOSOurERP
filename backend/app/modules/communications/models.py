from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..core.base import BaseModel

class Channel(BaseModel):
 __tablename__="communication_channels"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
 name:Mapped[str]=mapped_column(String(120))
 description:Mapped[str|None]=mapped_column(Text)
 channel_type:Mapped[str]=mapped_column(String(20),default="public")
 created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
 updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class ChannelMember(BaseModel):
 __tablename__="communication_channel_members"
 channel_id:Mapped[UUID]=mapped_column(ForeignKey("communication_channels.id",ondelete="CASCADE"),primary_key=True)
 user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
 joined_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class ChannelReadState(BaseModel):
 __tablename__="communication_channel_read_states"
 channel_id:Mapped[UUID]=mapped_column(ForeignKey("communication_channels.id",ondelete="CASCADE"),primary_key=True)
 user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
 last_read_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Message(BaseModel):
 __tablename__="communication_messages"
 id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
 channel_id:Mapped[UUID]=mapped_column(ForeignKey("communication_channels.id",ondelete="CASCADE"),index=True)
 sender_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
 body:Mapped[str]=mapped_column(Text)
 is_edited:Mapped[bool]=mapped_column(Boolean,default=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
 updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
