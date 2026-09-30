from datetime import datetime,timezone
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..core.audit import record
from .models import Invoice,InvoiceMilestone,Payment
from .schemas import InvoiceCreate,InvoiceRead,MilestoneCreate,MilestoneRead,PaymentCreate,PaymentRead
router=APIRouter()
def org_obj(db,model,user,obj_id): return db.scalar(select(model).where(model.id==obj_id,model.organization_id==user.organization_id))
@router.get("/invoices",response_model=list[InvoiceRead])
def list_invoices(user:User=Depends(require_permission("finance.read")),db:Session=Depends(get_db)): return db.scalars(select(Invoice).where(Invoice.organization_id==user.organization_id).order_by(Invoice.created_at.desc())).all()
@router.post("/invoices",response_model=InvoiceRead,status_code=201)
def create_invoice(payload:InvoiceCreate,user:User=Depends(require_permission("finance.create")),db:Session=Depends(get_db)):
 from ..crm.models import Client
 from ..projects.models import Project
 from ..sales.models import Contract
 if not org_obj(db,Client,user,payload.client_id): raise HTTPException(400,"Client not found")
 if payload.project_id and not org_obj(db,Project,user,payload.project_id): raise HTTPException(400,"Project not found")
 if payload.contract_id and not org_obj(db,Contract,user,payload.contract_id): raise HTTPException(400,"Contract not found")
 if payload.total_amount<0 or payload.subtotal<0 or payload.tax_amount<0: raise HTTPException(400,"Invoice amounts cannot be negative")
 if db.scalar(select(Invoice).where(Invoice.invoice_number==payload.invoice_number)): raise HTTPException(409,"Invoice number already exists")
 invoice=Invoice(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump());db.add(invoice);db.flush();record(db,user.organization_id,user.id,"create","invoice",invoice.id,{"invoice_number":invoice.invoice_number});db.commit();db.refresh(invoice);return invoice
@router.post("/invoices/{invoice_id}/milestones",response_model=MilestoneRead,status_code=201)
def create_milestone(invoice_id:UUID,payload:MilestoneCreate,user:User=Depends(require_permission("finance.create")),db:Session=Depends(get_db)):
 invoice=org_obj(db,Invoice,user,invoice_id)
 if not invoice: raise HTTPException(404,"Invoice not found")
 if payload.amount<0 or payload.percentage is not None and not 0<=payload.percentage<=100: raise HTTPException(400,"Invalid milestone amount or percentage")
 milestone=InvoiceMilestone(organization_id=user.organization_id,invoice_id=invoice.id,**payload.model_dump());db.add(milestone);db.flush();record(db,user.organization_id,user.id,"create","invoice_milestone",milestone.id,{"invoice_id":str(invoice.id)});db.commit();db.refresh(milestone);return milestone
@router.get("/invoices/{invoice_id}/milestones",response_model=list[MilestoneRead])
def list_milestones(invoice_id:UUID,user:User=Depends(require_permission("finance.read")),db:Session=Depends(get_db)):
 invoice=org_obj(db,Invoice,user,invoice_id)
 if not invoice: raise HTTPException(404,"Invoice not found")
 return db.scalars(select(InvoiceMilestone).where(InvoiceMilestone.invoice_id==invoice.id,InvoiceMilestone.organization_id==user.organization_id).order_by(InvoiceMilestone.due_at)).all()
@router.post("/invoices/{invoice_id}/payments",response_model=PaymentRead,status_code=201)
def create_payment(invoice_id:UUID,payload:PaymentCreate,user:User=Depends(require_permission("finance.create")),db:Session=Depends(get_db)):
 invoice=org_obj(db,Invoice,user,invoice_id)
 if not invoice: raise HTTPException(404,"Invoice not found")
 paid=float(db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.invoice_id==invoice.id,Payment.organization_id==user.organization_id)) or 0)
 if paid+payload.amount>float(invoice.total_amount): raise HTTPException(400,"Payment exceeds invoice balance")
 payment=Payment(organization_id=user.organization_id,invoice_id=invoice.id,created_by_user_id=user.id,**payload.model_dump());db.add(payment)
 invoice.status="paid" if paid+payload.amount>=float(invoice.total_amount) else "partially_paid";invoice.updated_at=datetime.now(timezone.utc)
 db.flush();record(db,user.organization_id,user.id,"create","payment",payment.id,{"invoice_id":str(invoice.id),"amount":payload.amount});db.commit();db.refresh(payment);return payment
