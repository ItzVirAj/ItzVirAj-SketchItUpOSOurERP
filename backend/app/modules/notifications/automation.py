from datetime import datetime,timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Notification
from .service import create_notification
from ..crm.models import LeadFollowUp
from ..projects.models import Task
from ..finance.models import Invoice

def _already_sent(db,org_id,user_id,kind,entity_id):
 return db.scalar(select(Notification.id).where(Notification.organization_id==org_id,Notification.user_id==user_id,Notification.type==kind,Notification.entity_id==entity_id).limit(1)) is not None

def generate_overdue_notifications(db:Session,organization_id):
 now=datetime.now(timezone.utc);created=0
 followups=db.scalars(select(LeadFollowUp).where(LeadFollowUp.organization_id==organization_id,LeadFollowUp.completed_at.is_(None),LeadFollowUp.due_at<now)).all()
 for f in followups:
  if f.assigned_user_id and not _already_sent(db,organization_id,f.assigned_user_id,"crm.follow_up_overdue",f.id):
   create_notification(db,organization_id,f.assigned_user_id,"crm.follow_up_overdue","Overdue CRM follow-up",f"CRM follow-up '{f.action}' is overdue.","lead",f.lead_id,f"/crm/leads/{f.lead_id}");created+=1
 tasks=db.scalars(select(Task).where(Task.organization_id==organization_id,Task.due_date<now,Task.status.notin_(["done","completed"]),Task.assignee_user_id.is_not(None))).all()
 for t in tasks:
  if not _already_sent(db,organization_id,t.assignee_user_id,"tasks.overdue",t.id):
   create_notification(db,organization_id,t.assignee_user_id,"tasks.overdue","Overdue task",f"Task '{t.title}' is overdue.","task",t.id,f"/projects/{t.project_id}/tasks/{t.id}");created+=1
 invoices=db.scalars(select(Invoice).where(Invoice.organization_id==organization_id,Invoice.due_at<now,Invoice.status.in_(["sent","partially_paid"]))).all()
 for inv in invoices:
  if inv.created_by_user_id and not _already_sent(db,organization_id,inv.created_by_user_id,"finance.invoice_overdue",inv.id):
   create_notification(db,organization_id,inv.created_by_user_id,"finance.invoice_overdue","Overdue invoice",f"Invoice {inv.invoice_number} is overdue.","invoice",inv.id,f"/finance/invoices/{inv.id}");created+=1
 db.commit();return {"created":created}