from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import DateTime,ForeignKey,String,Text,JSON
from sqlalchemy.orm import Mapped,mapped_column
from .base import BaseModel
class Organization(BaseModel):
 __tablename__="organizations"; id:Mapped[UUID]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(200)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); deleted_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class Role(BaseModel):
 __tablename__="roles"; id:Mapped[UUID]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(100),unique=True); description:Mapped[str|None]=mapped_column(Text)
class User(BaseModel):
 __tablename__="users"; id:Mapped[UUID]=mapped_column(primary_key=True); organization_id:Mapped[UUID|None]=mapped_column(ForeignKey("organizations.id")); email:Mapped[str]=mapped_column(String(320),unique=True); display_name:Mapped[str]=mapped_column(String(200)); status:Mapped[str]=mapped_column(String(20),default="active"); password_hash:Mapped[str|None]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); deleted_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
class UserRole(BaseModel):
 __tablename__="user_roles"; user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True); role_id:Mapped[UUID]=mapped_column(ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True)
class AuditLog(BaseModel):
 __tablename__="audit_logs"; id:Mapped[UUID]=mapped_column(primary_key=True); organization_id:Mapped[UUID|None]=mapped_column(ForeignKey("organizations.id")); actor_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id")); action:Mapped[str]=mapped_column(String(100)); entity_type:Mapped[str]=mapped_column(String(100)); entity_id:Mapped[UUID|None]=mapped_column(); metadata_:Mapped[dict]=mapped_column("metadata",JSON,default=dict); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
