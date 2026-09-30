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
from .expense_models import Expense
from .expense_schemas import ExpenseCreate,ExpenseRead
from .schemas import InvoiceCreate,InvoiceRead,InvoiceStatusUpdate,MilestoneCreate,MilestoneRead,PaymentCreate,PaymentRead
router=APIRouter()
def org_obj(db,model,user,obj_id): return db.scalar(select(model).where(model.id==obj_id,model.organization_id==user.organization_id))

@router.post("/contracts/{contract_id}/invoice",response_model=InvoiceRead,status_code=201)
def create_contract_invoice(contract_id:UUID,user:User=Depends(require_permission("finance.create")),db:Session=Depends(get_db)):
 from ..sales.models import Contract
 contract=org_obj(db,Contract,user,contract_id)
 if not contract: raise HTTPException(404,"Contract not found")
 if contract.status not in {"signed","active"}: raise HTTPException(400,"Contract must be signed or active before invoicing")
 existing=db.scalar(select(Invoice).where(Invoice.organization_id==user.organization_id,Invoice.contract_id==contract.id))
 if existing: raise HTTPException(409,"An invoice already exists for this contract")
 number=f"INV-{datetime.now(timezone.utc):%Y%m%d}-{str(contract.id)[:8].upper()}"
 total=float(contract.value or 0)
 invoice=Invoice(organization_id=user.organization_id,client_id=contract.client_id,project_id=contract.project_id,contract_id=contract.id,invoice_number=number,status="draft",currency=contract.currency,subtotal=total,total_amount=total,created_by_user_id=user.id)
 db.add(invoice);db.flush()
 if total>0:
  milestone=InvoiceMilestone(organization_id=user.organization_id,invoice_id=invoice.id,name="Contract billing milestone",percentage=100,amount=total,due_at=contract.start_date,status="pending")
  db.add(milestone)
 record(db,user.organization_id,user.id,"create","invoice",invoice.id,{"contract_id":str(contract.id),"invoice_number":number})
 db.commit();db.refresh(invoice);return invoice


@router.get("/expenses",response_model=list[ExpenseRead])
def list_expenses(user:User=Depends(require_permission("finance.expenses.read")),db:Session=Depends(get_db)):
 return db.scalars(select(Expense).where(Expense.organization_id==user.organization_id).order_by(Expense.incurred_at.desc())).all()

@router.post("/expenses",response_model=ExpenseRead,status_code=201)
def create_expense(payload:ExpenseCreate,user:User=Depends(require_permission("finance.expenses.create")),db:Session=Depends(get_db)):
 if payload.project_id:
  from ..projects.models import Project
  if not org_obj(db,Project,user,payload.project_id): raise HTTPException(400,"Project not found")
 expense=Expense(organization_id=user.organization_id,created_by_user_id=user.id,**payload.model_dump())
 db.add(expense);db.flush();record(db,user.organization_id,user.id,"create","expense",expense.id,{"category":expense.category,"amount":float(expense.amount)});db.commit();db.refresh(expense);return expense

@router.get("/summary")
def finance_summary(user:User=Depends(require_permission("finance.read")),db:Session=Depends(get_db)):
 invoiced=float(db.scalar(select(func.coalesce(func.sum(Invoice.total_amount),0)).where(Invoice.organization_id==user.organization_id,Invoice.status!="cancelled")) or 0)
 collected=float(db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.organization_id==user.organization_id)) or 0)
 expenses=float(db.scalar(select(func.coalesce(func.sum(Expense.amount),0)).where(Expense.organization_id==user.organization_id)) or 0)
 outstanding=max(invoiced-collected,0)
 return {"invoiced":invoiced,"collected":collected,"outstanding":outstanding,"expenses":expenses,"net_collected":collected-expenses}

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

@router.post("/invoices/{invoice_id}/status",response_model=InvoiceRead)
def update_invoice_status(invoice_id:UUID,payload:InvoiceStatusUpdate,user:User=Depends(require_permission("finance.create")),db:Session=Depends(get_db)):
 invoice=org_obj(db,Invoice,user,invoice_id)
 if not invoice: raise HTTPException(404,"Invoice not found")
 allowed={"draft":{"sent","cancelled"},"sent":{"cancelled"},"partially_paid":{"cancelled"},"paid":set(),"overdue":{"cancelled"},"cancelled":set()}
 current=invoice.status
 if payload.status not in allowed.get(current,set()): raise HTTPException(400,f"Invalid invoice transition: {current} -> {payload.status}")
 invoice.status=payload.status;invoice.updated_at=datetime.now(timezone.utc)
 record(db,user.organization_id,user.id,"status_change","invoice",invoice.id,{"from":current,"to":payload.status})
 db.commit();db.refresh(invoice);return invoice

@router.get("/invoices/{invoice_id}/balance")
def invoice_balance(invoice_id:UUID,user:User=Depends(require_permission("finance.read")),db:Session=Depends(get_db)):
 invoice=org_obj(db,Invoice,user,invoice_id)
 if not invoice: raise HTTPException(404,"Invoice not found")
 if invoice.status not in {"sent","partially_paid","overdue"}: raise HTTPException(400,"Invoice must be sent before recording payment")
 paid=float(db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.invoice_id==invoice.id,Payment.organization_id==user.organization_id)) or 0)
 total=float(invoice.total_amount)
 return {"invoice_id":invoice.id,"total_amount":total,"paid_amount":paid,"balance_amount":max(total-paid,0),"status":invoice.status}

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
