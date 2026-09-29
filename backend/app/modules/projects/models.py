from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import DateTime,ForeignKey,String,Text,JSON
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel
class Project(BaseModel):
 __tablename__="projects"
 id:Mapped[UUID]=mapped_column(primary_key=True)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
 client_name:Mapped[str|None]=mapped_column(String(200))
 client_id:Mapped[UUID|None]=mapped_column(ForeignKey("clients.id",ondelete="SET NULL"))
 name:Mapped[str]=mapped_column(String(200))
 description:Mapped[str|None]=mapped_column(Text)
 status:Mapped[str]=mapped_column(String(30),default="planned")
 owner_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id"))
 start_date:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 due_date:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
 updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class Task(BaseModel):
 __tablename__="tasks"
 id:Mapped[UUID]=mapped_column(primary_key=True)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
 project_id:Mapped[UUID]=mapped_column(ForeignKey("projects.id",ondelete="CASCADE"))
 title:Mapped[str]=mapped_column(String(240))
 description:Mapped[str|None]=mapped_column(Text)
 status:Mapped[str]=mapped_column(String(30),default="todo")
 priority:Mapped[str]=mapped_column(String(20),default="medium")
 assignee_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id"))
 due_date:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
 updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
