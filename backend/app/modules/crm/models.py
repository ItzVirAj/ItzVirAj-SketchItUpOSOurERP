from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel

class Client(BaseModel):
    __tablename__="clients"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    name:Mapped[str]=mapped_column(String(240))
    industry:Mapped[str|None]=mapped_column(String(120))
    website:Mapped[str|None]=mapped_column(String(500))
    email:Mapped[str|None]=mapped_column(String(320))
    phone:Mapped[str|None]=mapped_column(String(40))
    gst_number:Mapped[str|None]=mapped_column(String(30))
    notes:Mapped[str|None]=mapped_column(Text)
    status:Mapped[str]=mapped_column(String(30),default="active")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Contact(BaseModel):
    __tablename__="contacts"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    client_id:Mapped[UUID]=mapped_column(ForeignKey("clients.id",ondelete="CASCADE"))
    name:Mapped[str]=mapped_column(String(200))
    role:Mapped[str|None]=mapped_column(String(80))
    email:Mapped[str|None]=mapped_column(String(320))
    phone:Mapped[str|None]=mapped_column(String(40))
    communication_preference:Mapped[str|None]=mapped_column(String(30))
    birthday:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    anniversary:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    is_primary:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Pipeline(BaseModel):
    __tablename__="crm_pipelines"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    name:Mapped[str]=mapped_column(String(120))
    description:Mapped[str|None]=mapped_column(Text)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)

class PipelineStage(BaseModel):
    __tablename__="crm_pipeline_stages"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    pipeline_id:Mapped[UUID]=mapped_column(ForeignKey("crm_pipelines.id",ondelete="CASCADE"))
    name:Mapped[str]=mapped_column(String(80))
    position:Mapped[int]=mapped_column(Integer)
    probability:Mapped[float]=mapped_column(Numeric(5,2),default=0)
    is_closed_won:Mapped[bool]=mapped_column(Boolean,default=False)
    is_closed_lost:Mapped[bool]=mapped_column(Boolean,default=False)

class Lead(BaseModel):
    __tablename__="leads"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    pipeline_id:Mapped[UUID]=mapped_column(ForeignKey("crm_pipelines.id"))
    stage_id:Mapped[UUID]=mapped_column(ForeignKey("crm_pipeline_stages.id"))
    client_id:Mapped[UUID|None]=mapped_column(ForeignKey("clients.id",ondelete="SET NULL"))
    contact_id:Mapped[UUID|None]=mapped_column(ForeignKey("contacts.id",ondelete="SET NULL"))
    name:Mapped[str]=mapped_column(String(240))
    company:Mapped[str|None]=mapped_column(String(240))
    industry:Mapped[str|None]=mapped_column(String(120))
    phone:Mapped[str|None]=mapped_column(String(40))
    email:Mapped[str|None]=mapped_column(String(320))
    source:Mapped[str]=mapped_column(String(80))
    campaign:Mapped[str|None]=mapped_column(String(160))
    estimated_value:Mapped[float|None]=mapped_column(Numeric(14,2))
    expected_close_date:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    requirement_summary:Mapped[str|None]=mapped_column(Text)
    owner_user_id:Mapped[UUID|None]=mapped_column(ForeignKey("users.id"))
    temperature:Mapped[str]=mapped_column(String(10),default="Cold")
    next_follow_up_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    lost_reason:Mapped[str|None]=mapped_column(String(80))
    lost_notes:Mapped[str|None]=mapped_column(Text)
    tags:Mapped[str|None]=mapped_column(Text)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class LeadActivity(BaseModel):
    __tablename__="lead_activities"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    lead_id:Mapped[UUID]=mapped_column(ForeignKey("leads.id",ondelete="CASCADE"))
    actor_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
    activity_type:Mapped[str]=mapped_column(String(30))
    subject:Mapped[str]=mapped_column(String(240))
    notes:Mapped[str|None]=mapped_column(Text)
    occurred_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class LeadFollowUp(BaseModel):
    __tablename__="lead_follow_ups"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    lead_id:Mapped[UUID]=mapped_column(ForeignKey("leads.id",ondelete="CASCADE"))
    assigned_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
    due_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
    action:Mapped[str]=mapped_column(String(240))
    completed_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    notes:Mapped[str|None]=mapped_column(Text)
