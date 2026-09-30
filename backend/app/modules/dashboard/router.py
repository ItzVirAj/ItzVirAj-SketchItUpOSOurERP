from datetime import datetime,timezone
from fastapi import APIRouter,Depends
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User
from ..core.dependencies import require_permission
from ..projects.models import Project,Task
from ..calendar.models import Event
from ..crm.models import Client,Lead,LeadFollowUp,PipelineStage
from ..sales.models import Proposal,Contract
from ..finance.models import Invoice,Payment
from ..finance.expense_models import Expense

router=APIRouter()

@router.get("/overview")
def overview(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db)):
 org=user.organization_id
 now=datetime.now(timezone.utc)
 def count(model,*conditions):
  return int(db.scalar(select(func.count()).select_from(model).where(model.organization_id==org,*conditions)) or 0)
 projects=count(Project)
 active_projects=count(Project,Project.status=="active")
 clients=count(Client,Client.status=="active")
 leads=count(Lead)
 open_leads=int(db.scalar(select(func.count()).select_from(Lead).join(PipelineStage,Lead.stage_id==PipelineStage.id).where(Lead.organization_id==org,PipelineStage.is_closed_won==False,PipelineStage.is_closed_lost==False)) or 0)
 tasks=count(Task,Task.status.not_in(["done","completed"]))
 overdue_tasks=count(Task,Task.due_date<now,Task.status.not_in(["done","completed"]))
 upcoming_events=int(db.scalar(select(func.count()).select_from(Event).where(Event.organization_id==org,Event.starts_at>=now)) or 0)
 proposals=int(db.scalar(select(func.count()).select_from(Proposal).where(Proposal.organization_id==org,Proposal.status.in_([ "sent","accepted"]))) or 0)
 contracts=int(db.scalar(select(func.count()).select_from(Contract).where(Contract.organization_id==org,Contract.status.in_([ "signed","active"]))) or 0)
 invoiced=float(db.scalar(select(func.coalesce(func.sum(Invoice.total_amount),0)).where(Invoice.organization_id==org,Invoice.status!="cancelled")) or 0)
 collected=float(db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.organization_id==org)) or 0)
 expenses=float(db.scalar(select(func.coalesce(func.sum(Expense.amount),0)).where(Expense.organization_id==org)) or 0)
 overdue_invoices=int(db.scalar(select(func.count()).select_from(Invoice).where(Invoice.organization_id==org,Invoice.due_at<now,Invoice.status.in_([ "sent","partially_paid","overdue"]))) or 0)
 overdue_followups=int(db.scalar(select(func.count()).select_from(LeadFollowUp).where(LeadFollowUp.organization_id==org,LeadFollowUp.due_at<now,LeadFollowUp.completed_at.is_(None))) or 0)
 return {"projects":{"total":projects,"active":active_projects},"clients":{"active":clients},"crm":{"leads":leads,"open_leads":open_leads,"overdue_followups":overdue_followups},"sales":{"open_proposals":proposals,"active_contracts":contracts},"finance":{"invoiced":invoiced,"collected":collected,"outstanding":max(invoiced-collected,0),"expenses":expenses,"net_collected":collected-expenses,"overdue_invoices":overdue_invoices},"work":{"open_tasks":tasks,"overdue_tasks":overdue_tasks,"upcoming_events":upcoming_events},"generated_at":now}
