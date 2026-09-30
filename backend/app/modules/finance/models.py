from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import DateTime,ForeignKey,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from ..core.base import BaseModel

class Invoice(BaseModel):
 __tablename__="invoices"
 id:Mapped[UUID]=mapped_column(primary_key=True)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
 client_id:Mapped[UUID]=mapped_column(ForeignKey("clients.id"))
 project_id:Mapped[UUID|None]=mapped_column(ForeignKey("projects.id",ondelete="SET NULL"))
 contract_id:Mapped[UUID|None]=mapped_column(ForeignKey("contracts.id",ondelete="SET NULL"))
 invoice_number:Mapped[str]=mapped_column(String(80),unique=True)
 status:Mapped[str]=mapped_column(String(30),default="draft")
 currency:Mapped[str]=mapped_column(String(3),default="INR")
 subtotal:Mapped[float]=mapped_column(Numeric(14,2),default=0)
 tax_amount:Mapped[float]=mapped_column(Numeric(14,2),default=0)
 total_amount:Mapped[float]=mapped_column(Numeric(14,2),default=0)
 due_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 notes:Mapped[str|None]=mapped_column(Text)
 created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
 updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class InvoiceMilestone(BaseModel):
 __tablename__="invoice_milestones"
 id:Mapped[UUID]=mapped_column(primary_key=True)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
 invoice_id:Mapped[UUID]=mapped_column(ForeignKey("invoices.id",ondelete="CASCADE"))
 name:Mapped[str]=mapped_column(String(160))
 percentage:Mapped[float|None]=mapped_column(Numeric(5,2))
 amount:Mapped[float]=mapped_column(Numeric(14,2))
 due_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
 status:Mapped[str]=mapped_column(String(30),default="pending")
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))

class Payment(BaseModel):
 __tablename__="payments"
 id:Mapped[UUID]=mapped_column(primary_key=True)
 organization_id:Mapped[UUID]=mapped_column(ForeignKey("organizations.id"))
 invoice_id:Mapped[UUID]=mapped_column(ForeignKey("invoices.id",ondelete="CASCADE"))
 amount:Mapped[float]=mapped_column(Numeric(14,2))
 currency:Mapped[str]=mapped_column(String(3),default="INR")
 payment_method:Mapped[str]=mapped_column(String(40))
 reference:Mapped[str|None]=mapped_column(String(120))
 paid_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
 notes:Mapped[str|None]=mapped_column(Text)
 created_by_user_id:Mapped[UUID]=mapped_column(ForeignKey("users.id"))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
