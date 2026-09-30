from datetime import datetime,timezone
from fastapi import APIRouter,Depends
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from ...db import get_db
from ..core.models import User,AuditLog
from ..core.dependencies import require_permission
from ..projects.models import Project,Task
from ..calendar.models import Event
from ..crm.models import Client,Lead,LeadFollowUp,PipelineStage
from ..sales.models import Proposal,Contract
from ..finance.models import Invoice,Payment
from ..finance.expense_models import Expense

router=APIRouter()


@router.get("/activity")
def recent_activity(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db),limit:int=20):
 limit=max(1,min(limit,50))
 rows=db.scalars(select(AuditLog).where(AuditLog.organization_id==user.organization_id).order_by(AuditLog.created_at.desc()).limit(limit)).all()
 return [{"id":r.id,"action":r.action,"entity_type":r.entity_type,"entity_id":r.entity_id,"metadata":r.metadata_,"created_at":r.created_at} for r in rows]

@router.get("/pipeline")
def pipeline(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db)):
 rows=db.execute(select(PipelineStage.id,PipelineStage.name,PipelineStage.position,PipelineStage.probability,PipelineStage.is_closed_won,PipelineStage.is_closed_lost,func.count(Lead.id),func.coalesce(func.sum(Lead.estimated_value),0)).outerjoin(Lead,(Lead.stage_id==PipelineStage.id)&(Lead.organization_id==user.organization_id)).where(PipelineStage.organization_id==user.organization_id).group_by(PipelineStage.id).order_by(PipelineStage.position)).all()
 return [{"stage_id":r[0],"stage":r[1],"position":r[2],"probability":float(r[3] or 0),"closed_won":r[4],"closed_lost":r[5],"lead_count":int(r[6] or 0),"estimated_value":float(r[7] or 0)} for r in rows]

@router.get("/projects")
def project_breakdown(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db)):
 rows=db.execute(select(Project.status,func.count(Project.id)).where(Project.organization_id==user.organization_id).group_by(Project.status)).all()
 return [{"status":r[0],"count":int(r[1])} for r in rows]

@router.get("/finance/aging")
def finance_aging(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db)):
 now=datetime.now(timezone.utc)
 rows=db.scalars(select(Invoice).where(Invoice.organization_id==user.organization_id,Invoice.status.in_([ "sent","partially_paid","overdue"]))).all()
 result={"current":0.0,"1_30":0.0,"31_60":0.0,"61_90":0.0,"90_plus":0.0}
 for invoice in rows:
  paid=float(db.scalar(select(func.coalesce(func.sum(Payment.amount),0)).where(Payment.invoice_id==invoice.id,Payment.organization_id==user.organization_id)) or 0)
  balance=max(float(invoice.total_amount)-paid,0)
  if not invoice.due_at: result["current"]+=balance; continue
  days=max((now-invoice.due_at).days,0)
  bucket="current" if days==0 else "1_30" if days<=30 else "31_60" if days<=60 else "61_90" if days<=90 else "90_plus"
  result[bucket]+=balance
 return result


@router.get("/attention")
def attention(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db),limit:int=10):
 now=datetime.now(timezone.utc);limit=max(1,min(limit,25));items=[]
 for t in db.scalars(select(Task).where(Task.organization_id==user.organization_id,Task.due_date<now,Task.status.not_in(["done","completed"])).order_by(Task.due_date).limit(limit)).all(): items.append({"type":"overdue_task","priority":"high","title":t.title,"due_at":t.due_date,"entity_id":t.id})
 for f in db.scalars(select(LeadFollowUp).where(LeadFollowUp.organization_id==user.organization_id,LeadFollowUp.due_at<now,LeadFollowUp.completed_at.is_(None)).order_by(LeadFollowUp.due_at).limit(limit)).all(): items.append({"type":"overdue_follow_up","priority":"high","title":f.action,"due_at":f.due_at,"entity_id":f.lead_id})
 for i in db.scalars(select(Invoice).where(Invoice.organization_id==user.organization_id,Invoice.due_at<now,Invoice.status.in_([ "sent","partially_paid","overdue"])).order_by(Invoice.due_at).limit(limit)).all(): items.append({"type":"overdue_invoice","priority":"high","title":i.invoice_number,"due_at":i.due_at,"entity_id":i.id})
 items.sort(key=lambda x:x["due_at"] or now);return items[:limit]

@router.get("/upcoming")
def upcoming(user:User=Depends(require_permission("dashboard.read")),db:Session=Depends(get_db),days:int=14,limit:int=20):
 now=datetime.now(timezone.utc);days=max(1,min(days,90));limit=max(1,min(limit,50));end=now.replace(hour=0,minute=0,second=0,microsecond=0)
 from datetime import timedelta
 end=end+timedelta(days=days+1);items=[]
 for e in db.scalars(select(Event).where(Event.organization_id==user.organization_id,Event.starts_at>=now,Event.starts_at<end).order_by(Event.starts_at).limit(limit)).all(): items.append({"type":"event","title":e.title,"starts_at":e.starts_at,"ends_at":e.ends_at,"entity_id":e.id})
 for p in db.scalars(select(Proposal).where(Proposal.organization_id==user.organization_id,Proposal.valid_until>=now,Proposal.valid_until<end,Proposal.status=="sent").order_by(Proposal.valid_until).limit(limit)).all(): items.append({"type":"proposal_expiry","title":p.title,"starts_at":p.valid_until,"entity_id":p.id})
 items.sort(key=lambda x:x["starts_at"]);return items[:limit]

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
