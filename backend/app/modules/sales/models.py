from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import DateTime,ForeignKey,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel

class Proposal(BaseModel):
    __tablename__="proposals"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    lead_id:Mapped[UUID|None]=mapped_column(ForeignKey("leads.id",ondelete="SET NULL"))
    client_id:Mapped[UUID|None]=mapped_column(ForeignKey("clients.id",ondelete="SET NULL"))
    project_id:Mapped[UUID|None]=mapped_column(ForeignKey("projects.id",ondelete="SET NULL"))
    title:Mapped[str]=mapped_column(String(240))
    status:Mapped[str]=mapped_column(String(30),default="draft")
    amount:Mapped[float|None]=mapped_column(Numeric(14,2))
    currency:Mapped[str]=mapped_column(String(3),default="INR")
    valid_until:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    terms:Mapped[str|None]=mapped_column(Text)
    notes:Mapped[str|None]=mapped_column(Text)
    created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Contract(BaseModel):
    __tablename__="contracts"
    id:Mapped[UUID]=mapped_column(primary_key=True)
    organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
    proposal_id:Mapped[UUID|None]=mapped_column(ForeignKey("proposals.id",ondelete="SET NULL"))
    lead_id:Mapped[UUID|None]=mapped_column(ForeignKey("leads.id",ondelete="SET NULL"))
    client_id:Mapped[UUID]=mapped_column(ForeignKey("clients.id"))
    project_id:Mapped[UUID|None]=mapped_column(ForeignKey("projects.id",ondelete="SET NULL"))
    title:Mapped[str]=mapped_column(String(240))
    status:Mapped[str]=mapped_column(String(30),default="draft")
    contract_number:Mapped[str|None]=mapped_column(String(80))
    signed_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    start_date:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    end_date:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    value:Mapped[float|None]=mapped_column(Numeric(14,2))
    currency:Mapped[str]=mapped_column(String(3),default="INR")
    terms:Mapped[str|None]=mapped_column(Text)
    created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
